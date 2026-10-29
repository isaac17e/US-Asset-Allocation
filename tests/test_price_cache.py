"""Pruebas de la caché de precios por ticker, la fuente Yahoo y su integración en MarketDataLoader (sin red)."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import fmp_client  # noqa: E402
import price_cache  # noqa: E402

END = date(2026, 10, 28)  # miércoles
START = END - timedelta(days=400)


def _raw_prices(end: date, days: int = 700, seed: int = 3) -> pd.Series:
    """Precio 'raw' sintético en días hábiles hasta ``end``."""
    index = pd.bdate_range(end=pd.Timestamp(end), periods=days)
    rng = np.random.default_rng(seed)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, days))), index=index)


class FakeProvider:
    """Serie ajustada tipo Yahoo: cada dividendo (ex_date, fracción) reescala todo lo anterior por (1 - fracción)."""

    def __init__(self, raw: pd.Series, dividends=()):
        self.raw, self.dividends, self.calls = raw, list(dividends), []

    def adjusted(self, until: date) -> pd.Series:
        series = self.raw[self.raw.index <= pd.Timestamp(until)].copy()
        for ex_date, fraction in self.dividends:
            if pd.Timestamp(ex_date) <= series.index[-1]:
                series[series.index < pd.Timestamp(ex_date)] *= 1.0 - fraction
        return series

    def fetch(self, ticker: str, start: date, end: date) -> pd.Series:
        self.calls.append((ticker, start, end))
        full = self.adjusted(end)
        return full[(full.index >= pd.Timestamp(start)) & (full.index <= pd.Timestamp(end))]


class SymbolAndEnvTests(unittest.TestCase):
    def test_to_yahoo_symbol(self):
        self.assertEqual(price_cache.to_yahoo_symbol("BRK.B"), "BRK-B")
        self.assertEqual(price_cache.to_yahoo_symbol("spy"), "SPY")
        self.assertEqual(price_cache.to_yahoo_symbol("RY.TO"), "RY.TO")

    def test_cache_dir_from_env(self):
        self.assertEqual(price_cache.cache_dir_from_env({}), Path("/workspace/pipeline/state/prices"))
        self.assertEqual(price_cache.cache_dir_from_env({"USAA_PRICE_CACHE_DIR": "/tmp/x"}), Path("/tmp/x"))
        self.assertIsNone(price_cache.cache_dir_from_env({"USAA_PRICE_CACHE": "off"}))

    def test_resolve_price_sources(self):
        self.assertEqual(price_cache.resolve_price_sources({}), ("yahoo", "fmp"))
        self.assertEqual(price_cache.resolve_price_sources({"USAA_PRICE_SOURCE": "FMP"}), ("fmp",))
        with self.assertRaises(ValueError):
            price_cache.resolve_price_sources({"USAA_PRICE_SOURCE": "bloomberg"})


class IncrementalCacheTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.cache = price_cache.PriceCache(self.dir)
        self.raw = _raw_prices(END)

    def test_cold_run_downloads_everything_and_writes_csv(self):
        provider = FakeProvider(self.raw)
        series, used = self.cache.get("BRK.B", START, END, [("yahoo", provider.fetch)])
        self.assertEqual(used, "yahoo")
        self.assertEqual(provider.calls, [("BRK.B", START, END)])
        text = (self.dir / "BRK-B.csv").read_text()
        self.assertIn(f"# covered_from={START.isoformat()}", text)
        self.assertIn("date,adj_close", text)
        self.assertEqual(self.cache.stats["full"], 1)
        self.assertGreater(len(series), 250)

    def test_warm_run_only_downloads_overlap_and_matches_full_download(self):
        provider = FakeProvider(self.raw)
        fetchers = [("yahoo", provider.fetch)]
        self.cache.get("SPY", START, END - timedelta(days=14), fetchers)  # caché con 2 semanas de retraso
        provider.calls.clear()
        series, _ = self.cache.get("SPY", START, END, fetchers)
        (_, since, until), = provider.calls
        self.assertGreater(since, START + timedelta(days=300))  # no se vuelve a bajar todo
        self.assertLessEqual(since, END - timedelta(days=14))
        self.assertEqual(until, END)
        expected = provider.adjusted(END)
        expected = expected[expected.index >= pd.Timestamp(START)]
        pd.testing.assert_series_equal(series, expected, check_names=False, rtol=1e-9)
        self.assertEqual(self.cache.stats["incremental"], 1)
        self.assertEqual(self.cache.stats["rescaled"], 0)

    def test_dividend_inside_overlap_rescales_stored_history(self):
        base = FakeProvider(self.raw)
        self.cache.get("TLT", START, END - timedelta(days=10), [("yahoo", base.fetch)])
        with_div = FakeProvider(self.raw, dividends=[(END - timedelta(days=5), 0.0123)])  # ex-div tras el último guardado
        series, _ = self.cache.get("TLT", START, END, [("yahoo", with_div.fetch)])
        expected = with_div.adjusted(END)
        expected = expected[expected.index >= pd.Timestamp(START)]
        pd.testing.assert_series_equal(series, expected, check_names=False, rtol=1e-9)
        self.assertEqual(self.cache.stats["rescaled"], 1)
        # Los retornos diarios del historial viejo no cambian (solo el nivel): no hay saltos falsos en la unión.
        old = series[series.index < pd.Timestamp(END - timedelta(days=30))]
        np.testing.assert_allclose(old.pct_change().dropna().to_numpy(), base.adjusted(END).loc[old.index].pct_change().dropna().to_numpy(), rtol=1e-9)

    def test_absurd_ratio_triggers_full_redownload(self):
        first = FakeProvider(self.raw)
        self.cache.get("QQQ", START, END - timedelta(days=10), [("yahoo", first.fetch)])
        broken = FakeProvider(self.raw * 50.0)
        series, _ = self.cache.get("QQQ", START, END, [("yahoo", broken.fetch)])
        self.assertEqual(self.cache.stats["full"], 2)
        pd.testing.assert_series_equal(series, broken.adjusted(END).loc[lambda s: s.index >= pd.Timestamp(START)], check_names=False)

    def test_longer_window_than_cached_redownloads(self):
        provider = FakeProvider(self.raw)
        self.cache.get("GLD", START, END, [("yahoo", provider.fetch)])
        provider.calls.clear()
        earlier = START - timedelta(days=200)
        self.cache.get("GLD", earlier, END, [("yahoo", provider.fetch)])
        self.assertEqual(provider.calls, [("GLD", earlier, END)])

    def test_young_ticker_does_not_force_redownload_every_time(self):
        young = FakeProvider(self.raw[self.raw.index >= pd.Timestamp(END - timedelta(days=100))])
        self.cache.get("NEW", START, END, [("yahoo", young.fetch)])
        young.calls.clear()
        self.cache.get("NEW", START, END, [("yahoo", young.fetch)])
        self.assertGreater(young.calls[0][1], START)  # incremental gracias a covered_from

    def test_fallback_source_when_primary_fails_or_is_empty(self):
        def boom(*_args):
            raise RuntimeError("rate limited")
        backup = FakeProvider(self.raw)
        series, used = self.cache.get("EFA", START, END, [("yahoo", boom), ("fmp", backup.fetch)])
        self.assertEqual(used, "fmp")
        self.assertFalse(series.empty)
        empty = lambda *_args: pd.Series(dtype=float)  # noqa: E731
        _, used = price_cache.PriceCache(None).get("EFA", START, END, [("yahoo", empty), ("fmp", backup.fetch)])
        self.assertEqual(used, "fmp")

    def test_total_failure_uses_recent_cache_but_not_stale_cache(self):
        provider = FakeProvider(self.raw)
        self.cache.get("IEF", START, END - timedelta(days=2), [("yahoo", provider.fetch)])

        def boom(*_args):
            raise RuntimeError("sin red")
        with self.assertLogs("PrecioCache", level="WARNING"):
            series, used = self.cache.get("IEF", START, END, [("yahoo", boom)])
        self.assertEqual(used, "cache")
        self.assertFalse(series.empty)
        series, used = self.cache.get("IEF", START + timedelta(days=60), END + timedelta(days=30), [("yahoo", boom)])
        self.assertTrue(series.empty)
        self.assertEqual(used, "")

    def test_corrupt_file_is_treated_as_miss(self):
        (self.dir / "VNQ.csv").write_text("# covered_from=2020-01-01\ndate,adj_close\nbasura,xx\n")
        provider = FakeProvider(self.raw)
        with self.assertLogs("PrecioCache", level="WARNING"):
            series, _ = self.cache.get("VNQ", START, END, [("yahoo", provider.fetch)])
        self.assertFalse(series.empty)
        self.assertEqual(provider.calls[0][1], START)

    def test_disabled_cache_writes_nothing_and_always_downloads_all(self):
        provider = FakeProvider(self.raw)
        disabled = price_cache.PriceCache(None)
        disabled.get("SPY", START, END, [("yahoo", provider.fetch)])
        disabled.get("SPY", START, END, [("yahoo", provider.fetch)])
        self.assertEqual([c[1] for c in provider.calls], [START, START])
        self.assertEqual(list(self.dir.iterdir()), [])


class YahooFetchTests(unittest.TestCase):
    def _fake_yf(self, frame, calls):
        class Ticker:
            def __init__(self, symbol):
                calls.append(("ticker", symbol))

            def history(self, **kwargs):
                calls.append(("history", kwargs))
                if isinstance(frame, Exception):
                    raise frame
                return frame
        return types.SimpleNamespace(Ticker=Ticker)

    def test_uses_unadjusted_download_with_adj_close_and_exclusive_end(self):
        index = pd.DatetimeIndex(["2026-10-26", "2026-10-27"]).tz_localize("America/New_York") + pd.Timedelta(hours=0)
        frame = pd.DataFrame({"Close": [100.0, 101.0], "Adj Close": [99.0, 100.0]}, index=index)
        calls = []
        with mock.patch.dict(sys.modules, {"yfinance": self._fake_yf(frame, calls)}):
            with mock.patch.object(price_cache, "datetime") as fake_dt:
                fake_dt.now.return_value = datetime(2026, 10, 28, 20, 0, tzinfo=price_cache.NEW_YORK)
                series = price_cache.fetch_yahoo_adjusted_close("BRK.B", date(2026, 10, 1), date(2026, 10, 28))
        self.assertEqual(calls[0], ("ticker", "BRK-B"))
        kwargs = calls[1][1]
        self.assertIs(kwargs["auto_adjust"], False)
        self.assertEqual(kwargs["start"], "2026-10-01")
        self.assertEqual(kwargs["end"], "2026-10-29")
        self.assertEqual(list(series.values), [99.0, 100.0])  # Adj Close, no Close
        self.assertIsNone(series.index.tz)

    def test_empty_frame_returns_empty_series_and_errors_retry_then_raise(self):
        calls = []
        with mock.patch.dict(sys.modules, {"yfinance": self._fake_yf(pd.DataFrame(), calls)}):
            self.assertTrue(price_cache.fetch_yahoo_adjusted_close("ZZZ", date(2026, 1, 1), END).empty)
        calls = []
        sleeps = []
        with mock.patch.dict(sys.modules, {"yfinance": self._fake_yf(RuntimeError("429"), calls)}):
            with self.assertRaises(RuntimeError):
                price_cache.fetch_yahoo_adjusted_close("SPY", date(2026, 1, 1), END, retries=3, sleep=sleeps.append)
        self.assertEqual(len([c for c in calls if c[0] == "history"]), 3)
        self.assertEqual(len(sleeps), 2)

    def test_open_session_bar_is_dropped_until_after_close(self):
        series = pd.Series([1.0, 2.0], index=pd.DatetimeIndex(["2026-10-27", "2026-10-28"]))
        midday = datetime(2026, 10, 28, 11, 0, tzinfo=price_cache.NEW_YORK)
        after = datetime(2026, 10, 28, 17, 0, tzinfo=price_cache.NEW_YORK)
        self.assertEqual(list(price_cache._drop_open_session(series, midday).index), [pd.Timestamp("2026-10-27")])
        self.assertEqual(len(price_cache._drop_open_session(series, after)), 2)


def _load_manager():
    spec = importlib.util.spec_from_file_location("us_asset_manager_pc", ROOT / "US Asset Manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["us_asset_manager_pc"] = module
    spec.loader.exec_module(module)
    return module


mgr = _load_manager()


class LoaderIntegrationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.end = date.today()
        self.providers = {t: FakeProvider(_raw_prices(self.end, seed=i)) for i, t in enumerate(["SPY", "TLT", "GLD"])}

    def _yahoo(self, ticker, start, end):
        return self.providers[ticker].fetch(ticker, start, end)

    def _loader(self, cache, **kwargs):
        return mgr.MarketDataLoader(None, 3, 260, cache=cache, sources=("yahoo",), yahoo_fetch=self._yahoo, **kwargs)

    def test_results_identical_with_and_without_cache_and_second_run_is_incremental(self):
        tickers = ["SPY", "TLT", "GLD"]
        plain = self._loader(price_cache.PriceCache(None)).load(tickers)
        cache = price_cache.PriceCache(self.dir)
        cold = self._loader(cache).load(tickers)
        for provider in self.providers.values():
            provider.calls.clear()
        warm = self._loader(cache).load(tickers)
        pd.testing.assert_frame_equal(plain, cold)
        pd.testing.assert_frame_equal(plain, warm, rtol=1e-12)
        self.assertEqual(cache.stats["incremental"], 3)
        window = (self.end - timedelta(days=int(365.25 * 3) + 10))
        for provider in self.providers.values():
            self.assertGreater(provider.calls[0][1], window + timedelta(days=300))

    def test_yahoo_primary_fmp_fallback_only_with_key(self):
        calls = []

        def broken(*_args):
            raise RuntimeError("yahoo caído")

        class StubFMP:
            api_key = "k"

            def historical_adjusted_close(self, ticker, start, end):
                calls.append(ticker)
                return self_outer.providers[ticker].fetch(ticker, start, end)
        self_outer = self
        loader = mgr.MarketDataLoader(StubFMP(), 3, 260, sources=("yahoo", "fmp"), yahoo_fetch=broken)
        frame = loader.load(["SPY"])
        self.assertEqual(calls, ["SPY"])
        self.assertEqual(loader.source_counts, {"fmp": 1})
        self.assertFalse(frame.empty)
        no_key = StubFMP()
        no_key.api_key = "  "
        with self.assertRaises(RuntimeError):
            mgr.MarketDataLoader(no_key, 3, 260, sources=("yahoo", "fmp"), yahoo_fetch=broken).load(["SPY"])

    def test_fmp_only_authorization_error_still_aborts(self):
        class DeniedFMP:
            api_key = "k"

            def historical_adjusted_close(self, *_args):
                raise fmp_client.APIAuthorizationError("HTTP 402")
        with self.assertRaises(fmp_client.APIAuthorizationError):
            mgr.MarketDataLoader(DeniedFMP(), 3, 260, sources=("fmp",)).load(["SPY"])

    def test_short_history_is_dropped(self):
        short = FakeProvider(_raw_prices(self.end, days=100))
        loader = mgr.MarketDataLoader(None, 3, 260, sources=("yahoo",), yahoo_fetch=lambda t, s, e: short.fetch(t, s, e))
        with self.assertRaises(RuntimeError):
            loader.load(["XYZ"])


class OptimizerInputsTests(unittest.TestCase):
    """Con y sin caché (incluido un dividendo nuevo entre corridas) la cadena retornos -> Σ -> pesos es la misma."""

    def test_returns_covariance_and_weights_match(self):
        end = date.today()
        tickers = [f"E{i}" for i in range(10)]
        providers = {
            t: FakeProvider(_raw_prices(end, seed=20 + i), dividends=[(end - timedelta(days=5), 0.004 + 0.001 * (i % 3))])
            for i, t in enumerate(tickers)
        }

        def yahoo(ticker, start, until):
            return providers[ticker].fetch(ticker, start, until)

        def loader(cache):
            return mgr.MarketDataLoader(None, 3, 260, cache=cache, sources=("yahoo",), yahoo_fetch=yahoo)

        with tempfile.TemporaryDirectory() as tmp:
            cache = price_cache.PriceCache(tmp)
            window_start = end - timedelta(days=int(365.25 * 3) + 10)
            for t in tickers:  # corrida de hace 10 días: aún sin el dividendo
                cache.get(t, window_start, end - timedelta(days=10), [("yahoo", yahoo)])
            cached_prices = loader(cache).load(tickers)
            self.assertEqual(cache.stats["rescaled"], len(tickers))
        fresh_prices = loader(price_cache.PriceCache(None)).load(tickers)
        np.testing.assert_allclose(cached_prices.to_numpy(), fresh_prices.to_numpy(), rtol=1e-9)

        def solve(prices):
            returns = prices.pct_change(fill_method=None).dropna()
            cov, _info = mgr.cov_ewma_shrunk(returns, halflife=mgr.COVARIANCE_HALFLIFE_DAYS, scale=252.0)
            cov = pd.DataFrame(np.asarray(cov, dtype=float), index=tickers, columns=tickers)
            mu = returns.mean() * 252.0
            rng = np.random.default_rng(1)
            factors = pd.DataFrame(rng.uniform(0.1, 0.9, (len(tickers), len(mgr.FACTORS))), index=tickers, columns=list(mgr.FACTORS))
            profile = mgr.ProfileConfig("test", 4.0, 0.4, {f: 0.0 for f in mgr.FACTORS})
            return returns, cov, mgr.PortfolioOptimizer(mu, cov, factors, profile).solve("scipy").weights

        ret_a, cov_a, w_a = solve(cached_prices)
        ret_b, cov_b, w_b = solve(fresh_prices)
        np.testing.assert_allclose(ret_a.to_numpy(), ret_b.to_numpy(), atol=1e-10)
        np.testing.assert_allclose(cov_a.to_numpy(), cov_b.to_numpy(), atol=1e-10)
        np.testing.assert_allclose(w_a.to_numpy(), w_b.to_numpy(), atol=1e-6)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for pipeline_io. No network."""

from __future__ import annotations

import contextlib
import io
import json
import os
import random
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pipeline_io


BOGOTA = ZoneInfo("America/Bogota")
SAMPLE = datetime(2026, 10, 5, 16, 40, 12, tzinfo=BOGOTA)


class TimestampTests(unittest.TestCase):
    def test_iso_and_stamp_match_the_contract(self) -> None:
        self.assertEqual(pipeline_io.iso_bogota(SAMPLE), "2026-10-05T16:40:12-05:00")
        self.assertEqual(pipeline_io.stamp_bogota(SAMPLE), "20261005T164012")

    def test_naive_clock_is_bogota_and_utc_converts(self) -> None:
        naive = datetime(2026, 10, 5, 16, 40, 12)
        self.assertEqual(pipeline_io.iso_bogota(naive), "2026-10-05T16:40:12-05:00")
        utc = datetime(2026, 10, 5, 21, 40, 12, tzinfo=timezone.utc)
        self.assertEqual(pipeline_io.now_bogota(utc).utcoffset(), timedelta(hours=-5))
        self.assertEqual(pipeline_io.iso_bogota(utc), "2026-10-05T16:40:12-05:00")


class RiskFreeRateTests(unittest.TestCase):
    def test_default_without_env(self) -> None:
        self.assertEqual(pipeline_io.resolve_risk_free_rate(0.040, env={}), 0.040)
        self.assertEqual(pipeline_io.resolve_risk_free_rate(0.040, env={"RISK_FREE_RATE": " "}), 0.040)

    def test_env_override(self) -> None:
        with mock.patch.dict(os.environ, {"RISK_FREE_RATE": "0.052"}):
            self.assertAlmostEqual(pipeline_io.resolve_risk_free_rate(0.040), 0.052)
        self.assertEqual(pipeline_io.resolve_risk_free_rate(0.040, env={"RISK_FREE_RATE": "0"}), 0.0)

    def test_invalid_values_raise_a_clear_error(self) -> None:
        for value in ("abc", "5.2", "0.5", "-0.01", "nan", "inf"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "RISK_FREE_RATE"):
                pipeline_io.resolve_risk_free_rate(0.040, env={"RISK_FREE_RATE": value})

    def test_us_asset_manager_reads_env_and_records_rf(self) -> None:
        root = Path(__file__).resolve().parents[1]
        source = (root / "US Asset Manager.py").read_text(encoding="utf-8")
        self.assertIn("RISK_FREE_RATE: float = pipeline_io.resolve_risk_free_rate(0.040)", source)
        self.assertIn('"risk_free_rate": float(RISK_FREE_RATE),', source)


class WeightTests(unittest.TestCase):
    def test_drops_dust_renormalizes_and_orders(self) -> None:
        tickers, weights = pipeline_io.normalize_weights(
            {"SPY": 0.25, "DUST": 1e-9, "QQQ": 0.75, "ZERO": 0.0, "NEG": -0.2}
        )
        self.assertEqual(tickers, ["QQQ", "SPY"])
        self.assertEqual(list(weights), tickers)
        self.assertEqual(weights["QQQ"], 0.75)
        self.assertEqual(weights["SPY"], 0.25)
        self._assert_sums_to_one(weights)

    def test_rounding_remainder_sums_to_one(self) -> None:
        tickers, weights = pipeline_io.normalize_weights({"A": 1, "B": 1, "C": 1})
        self.assertEqual(tickers, ["A", "B", "C"])
        self.assertEqual(weights["A"], 0.333334)
        self.assertEqual(weights["B"], 0.333333)
        self.assertEqual(weights["C"], 0.333333)
        self._assert_sums_to_one(weights)

    def test_random_books_sum_to_one(self) -> None:
        rng = random.Random(0)
        for _ in range(200):
            raw = {f"T{i}": rng.random() for i in range(rng.randint(1, 30))}
            raw["DUST"] = 1e-8
            _, weights = pipeline_io.normalize_weights(raw)
            self._assert_sums_to_one(weights)
            ordered = sorted(weights, key=lambda ticker: (-weights[ticker], ticker))
            self.assertEqual(list(weights), ordered)

    def _assert_sums_to_one(self, weights: dict[str, float]) -> None:
        loaded = json.loads(json.dumps(weights))
        self.assertEqual(sum(Decimal(f"{value:.6f}") for value in loaded.values()), Decimal("1.000000"))
        self.assertEqual(sum(int(round(value * 1_000_000)) for value in loaded.values()), 1_000_000)


class AtomicWriteTests(unittest.TestCase):
    def test_writes_indent_2_and_replaces_without_leaving_tmp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "portfolio_latest.json"
            path.write_text("stale", encoding="utf-8")
            payload = {"schema_version": 1, "source_repo": "US-Asset-Allocation"}
            replaced: list[tuple[str, str]] = []
            real_replace = os.replace

            def spy(src: str, dst: str) -> None:
                replaced.append((str(src), str(dst)))
                self.assertTrue(str(src).endswith(".json.tmp"))
                real_replace(src, dst)

            with mock.patch("pipeline_io.os.replace", spy):
                self.assertTrue(pipeline_io.atomic_write_json(path, payload))
            self.assertEqual(replaced[0][1], str(path))
            self.assertFalse(Path(str(path) + ".tmp").exists())
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
            self.assertEqual(json.loads(text), payload)

    def test_pair_is_a_byte_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            moment = SAMPLE
            names = [
                "corp_fr_latest.json",
                f"corp_fr_{pipeline_io.stamp_bogota(moment)}.json",
            ]
            payload = {"schema_version": 1, "tickers": ["AAPL", "MSFT"], "run_ts": pipeline_io.iso_bogota(moment)}
            written = pipeline_io.write_json_files(tmp, names, payload)
            self.assertEqual(len(written), 2)
            bodies = [(Path(tmp) / name).read_bytes() for name in names]
            self.assertEqual(bodies[0], bodies[1])
            self.assertEqual(json.loads(bodies[0]), payload)

    def test_unwritable_directory_warns_and_does_not_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            blocked = Path(tmp) / "blocked"
            blocked.mkdir()
            blocked.chmod(stat.S_IRUSR | stat.S_IXUSR)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                written = pipeline_io.write_json_files(
                    blocked, ["portfolio_latest.json", "portfolio_us_asset_manager_x.json"], {"a": 1}
                )
            self.assertEqual(written, [])
            self.assertIn("WARNING", stderr.getvalue())
            self.assertFalse(any(blocked.iterdir()))

    def test_parent_not_a_directory_warns_and_does_not_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "not-a-directory"
            blocker.write_text("x", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                ok = pipeline_io.atomic_write_json(blocker / "out" / "portfolio_latest.json", {"a": 1})
            self.assertFalse(ok)
            self.assertIn("WARNING", stderr.getvalue())
            self.assertFalse(Path(str(blocker) + ".tmp").exists())

    def test_non_finite_payload_warns_and_does_not_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                ok = pipeline_io.atomic_write_json(path, {"volatility": float("nan")})
            self.assertFalse(ok)
            self.assertFalse(path.exists())
            self.assertIn("WARNING", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()

"""Offline browser checks for the generated Plotly HTML reports."""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from browser_test_helpers import (  # noqa: E402
    collect_page_errors,
    install_offline_route,
    launch_browser,
    load_playwright,
    wait_for_plotly,
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


corp = _load("corp_fr_optimization", "Corp_FR_Optimization.py")
mgr = _load("us_asset_manager", "US Asset Manager.py")


def _synthetic_corporate_inputs():
    symbols = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]
    top = pd.DataFrame({
        "Rank": range(1, 7), "symbol": symbols,
        "companyName": [f"Issuer {symbol}" for symbol in symbols],
        "rating": ["BBB"] * 6, "ratingSource": ["Sintético"] * 6,
        "ratingBucket": ["BBB"] * 6, "interestCoverage": np.linspace(3, 8, 6),
        "debtToEbitda": np.linspace(3, 1.5, 6), "fcfCAGR": np.linspace(0.02, 0.08, 6),
        "fcfCAGR_used": np.linspace(0.02, 0.08, 6), "CompositeScore": np.linspace(0.1, 0.9, 6),
        "Z_Coverage": np.linspace(-1, 1, 6), "Z_Debt": np.linspace(1, -1, 6),
        "Z_FCF": np.linspace(-0.5, 0.8, 6), "Z_Rating": np.linspace(0.2, 0.7, 6),
        "marketCap": np.linspace(2e9, 8e9, 6),
    })
    curve = corp.RiskFreeCurve(
        np.array([1.0, 5.0, 10.0]), np.array([4.1, 4.0, 4.2]),
        {1.0: "2026-10-01", 5.0: "2026-10-01", 10.0: "2026-10-01"},
    )
    top = corp.stage_weights(top)
    overlay = corp.stage_overlay(top, curve)
    return curve, top, overlay, corp.portfolio_summary(top, overlay)


def _synthetic_dashboard_inputs():
    tickers = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
    factors = list(mgr.FACTORS)
    weights = pd.Series(np.full(len(tickers), 1 / len(tickers)), index=tickers)
    profile = mgr.ProfileConfig("Prueba", 4.0, 0.4, {factor: 0.4 for factor in factors})
    result = mgr.OptimizationResult(
        "synthetic", weights, 0.08, 0.15, 0.5,
        pd.Series({factor: 0.5 for factor in factors}), 0.0, "optimal", 0.0,
    )
    rng = np.random.default_rng(7)
    moments = pd.DataFrame({
        "MFIV": rng.uniform(0.1, 0.3, len(tickers)),
        "MFIS": rng.uniform(-0.5, 0.5, len(tickers)),
        "MFIK": rng.uniform(2.0, 5.0, len(tickers)),
        "Fuente": ["Sintético"] * len(tickers),
    }, index=tickers)
    mu_table = pd.DataFrame({"Mu_Base": rng.uniform(0.04, 0.12, len(tickers))}, index=tickers)
    risk = pd.Series(np.full(len(tickers), 1 / len(tickers)), index=tickers)
    return profile, result, np.full(len(factors), 0.4), moments, mu_table, risk


class OfflineBrowserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("SKIP_BROWSER_TESTS") == "1":
            raise unittest.SkipTest("SKIP_BROWSER_TESTS=1")
        try:
            cls.sync_playwright, cls.expect = load_playwright()
            cls.playwright = cls.sync_playwright().start()
            cls.browser = launch_browser(cls.playwright)
        except Exception as exc:
            if hasattr(cls, "playwright"):
                cls.playwright.stop()
            raise unittest.SkipTest(f"Playwright Chromium unavailable: {exc}") from exc

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "browser"):
            cls.browser.close()
        if hasattr(cls, "playwright"):
            cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.blocked_requests = []
        self.page_errors = []
        self.console_errors = []
        install_offline_route(self.context, self.blocked_requests)
        self.page = self.context.new_page()
        collect_page_errors(self.page, self.page_errors, self.console_errors)

    def tearDown(self):
        self.context.close()

    def assert_browser_clean(self):
        self.assertEqual(self.page_errors, [])
        self.assertEqual(self.console_errors, [])
        self.assertEqual(self.blocked_requests, [])
        self.assertEqual(self.page.evaluate("typeof Plotly"), "object")


def _write_corporate_report(output: Path):
    curve, top, overlay, summary = _synthetic_corporate_inputs()
    with mock.patch.object(corp, "HTML_OUTPUT_PATH", str(output)):
        return corp.build_html_report(
            curve, [("Initial", 40), ("Selected", 6)], top, overlay, summary, 0
        )


class CorpFixedIncomeHTMLTests(unittest.TestCase):
    def test_report_embeds_plotly_without_a_cdn_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = _write_corporate_report(Path(tmp) / "corporate.html")
            html = report.read_text(encoding="utf-8")
            self.assertNotIn('<script src="https://cdn.plot.ly/plotly', html)
            self.assertEqual(html.count('class="plotly-graph-div"'), 6)


class CorpFixedIncomeReportTests(OfflineBrowserTestCase):
    def test_report_renders_six_offline_plotly_figures(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = _write_corporate_report(Path(tmp) / "corporate.html")
            self.page.goto(report.as_uri())
            wait_for_plotly(self.page, 6)
            self.assertEqual(self.page.locator(".js-plotly-plot").count(), 6)
            self.assertEqual(
                self.page.locator(".js-plotly-plot").evaluate_all("plots => plots.map(gd => gd.data.length)"),
                [3, 1, 5, 1, 2, 1],
            )
            self.assert_browser_clean()


class AllocationDashboardTests(OfflineBrowserTestCase):
    def test_dashboard_renders_title_subplots_and_trace_types(self):
        profile, result, targets, moments, mu_table, risk = _synthetic_dashboard_inputs()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "dashboard.html"
            mgr.DashboardBuilder().build(
                str(output), profile, result, targets, moments, mu_table, risk
            )
            self.page.goto(output.as_uri())
            wait_for_plotly(self.page, 1)
            details = self.page.locator(".js-plotly-plot").evaluate(
                "gd => ({title: gd.layout.title.text, subtitles: gd.layout.annotations.map(a => a.text), "
                "types: gd.data.map(trace => trace.type)})"
            )
            self.assertIn("Passive ETF Allocation · Perfil Prueba", details["title"])
            self.assertEqual(len(details["subtitles"]), 4)
            self.assertEqual(set(details["types"]), {"pie", "scatterpolar", "scatter", "bar"})
            self.assert_browser_clean()

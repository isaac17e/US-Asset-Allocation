"""Pruebas de la resolucion del horizonte del portafolio (USAA_HORIZON_*) y de su exportacion. Sin red."""
from __future__ import annotations

import importlib.util
import json
import math
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pipeline_io  # noqa: E402
from risk_estimators import to_years  # noqa: E402

HORIZON_VARS = ("USAA_HORIZON_DAYS", "USAA_HORIZON_MONTHS")


def _load_manager(env: dict[str, str] | None = None):
    """Importa 'US Asset Manager.py' desde cero con solo `env` como variables USAA_HORIZON_*."""
    with mock.patch.dict("os.environ", env or {}, clear=False) as patched:
        for name in HORIZON_VARS:
            if name not in (env or {}):
                patched.pop(name, None)
        spec = importlib.util.spec_from_file_location("us_asset_manager_horizon", ROOT / "US Asset Manager.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["us_asset_manager_horizon"] = module
        try:
            spec.loader.exec_module(module)
        finally:
            sys.modules.pop("us_asset_manager_horizon", None)
        return module


class ResolveHorizonTests(unittest.TestCase):
    def test_default_is_returned_untouched_when_nothing_is_set(self):
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={}), 60)
        blank = {"USAA_HORIZON_DAYS": " ", "USAA_HORIZON_MONTHS": ""}
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=blank, inputs={}), 60)

    def test_env_days(self):
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_DAYS": "90"}), 90)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_DAYS": " 45.0 "}), 45)

    def test_env_months_use_calendar_year_convention(self):
        cases = {"1": 30, "3": 91, "6": 183, "12": 365, "1.5": 46}
        for months, days in cases.items():
            self.assertEqual(pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_MONTHS": months}), days, months)

    def test_months_convention_matches_to_years(self):
        for months in (1, 2, 3, 6, 9, 12):
            days = pipeline_io.months_to_days(months)
            self.assertAlmostEqual(to_years(dte=days), to_years(months=months), delta=0.5 / 365.0 + 1e-12)

    def test_input_file_beats_env_beats_default(self):
        env = {"USAA_HORIZON_DAYS": "90"}
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env), 90)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env, inputs={"horizon_days": 120}), 120)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env, inputs={"horizon_months": 6}), 183)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={}, inputs={"horizon_days": 120}), 120)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env, inputs={"horizon_days": None}), 90)

    def test_env_months_vs_input_days_precedence(self):
        env = {"USAA_HORIZON_MONTHS": "6"}
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env), 183)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env, inputs={"horizon_days": 30}), 30)

    def test_days_and_months_in_one_source(self):
        env = {"USAA_HORIZON_DAYS": "91", "USAA_HORIZON_MONTHS": "3"}
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env=env), 91)
        with self.assertRaisesRegex(ValueError, "disagree"):
            pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_DAYS": "60", "USAA_HORIZON_MONTHS": "3"})
        with self.assertRaisesRegex(ValueError, "disagree"):
            pipeline_io.resolve_horizon_days(60, env={}, inputs={"horizon_days": 60, "horizon_months": 3})

    def test_bounds_are_inclusive(self):
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_DAYS": "7"}), 7)
        self.assertEqual(pipeline_io.resolve_horizon_days(60, env={"USAA_HORIZON_DAYS": "400"}), 400)

    def test_out_of_range_fails_clearly(self):
        for env in ({"USAA_HORIZON_DAYS": "6"}, {"USAA_HORIZON_DAYS": "401"}, {"USAA_HORIZON_DAYS": "0"},
                    {"USAA_HORIZON_DAYS": "-5"}, {"USAA_HORIZON_MONTHS": "0.1"}, {"USAA_HORIZON_MONTHS": "14"}):
            with self.subTest(env=env), self.assertRaisesRegex(ValueError, r"out of range.*7\.\.400"):
                pipeline_io.resolve_horizon_days(60, env=env)
        with self.assertRaisesRegex(ValueError, "out of range"):
            pipeline_io.resolve_horizon_days(60, env={}, inputs={"horizon_days": 1000})

    def test_malformed_values_fail_clearly(self):
        for env in ({"USAA_HORIZON_DAYS": "abc"}, {"USAA_HORIZON_DAYS": "nan"}, {"USAA_HORIZON_DAYS": "inf"},
                    {"USAA_HORIZON_DAYS": "60.5"}, {"USAA_HORIZON_MONTHS": "tres"}):
            with self.subTest(env=env), self.assertRaisesRegex(ValueError, "USAA_HORIZON"):
                pipeline_io.resolve_horizon_days(60, env=env)
        for inputs in ({"horizon_days": "abc"}, {"horizon_days": True}, {"horizon_months": [3]}, {"horizon_days": 60.5}):
            with self.subTest(inputs=inputs), self.assertRaisesRegex(ValueError, "horizon_"):
                pipeline_io.resolve_horizon_days(60, env={}, inputs=inputs)

    def test_reads_process_environment_by_default(self):
        with mock.patch.dict("os.environ", {"USAA_HORIZON_DAYS": "75"}):
            self.assertEqual(pipeline_io.resolve_horizon_days(60), 75)


class OptionWindowTests(unittest.TestCase):
    def test_default_window_is_untouched(self):
        self.assertEqual(pipeline_io.horizon_option_window(60, 60, 30, 90), (30, 90))
        self.assertEqual(pipeline_io.horizon_option_window(60, 60, 25, 100), (25, 100))

    def test_window_scales_and_always_brackets_the_horizon(self):
        self.assertEqual(pipeline_io.horizon_option_window(120, 60, 30, 90), (60, 180))
        self.assertEqual(pipeline_io.horizon_option_window(30, 60, 30, 90), (15, 45))
        for horizon in range(pipeline_io.HORIZON_MIN_DAYS, pipeline_io.HORIZON_MAX_DAYS + 1):
            low, high = pipeline_io.horizon_option_window(horizon, 60, 30, 90)
            self.assertTrue(0 < low <= horizon <= high, (horizon, low, high))


class ManagerHorizonTests(unittest.TestCase):
    def test_default_behavior_is_unchanged(self):
        mgr = _load_manager()
        self.assertEqual((mgr.OPTIONS_MIN_DAYS, mgr.OPTIONS_TARGET_DAYS, mgr.OPTIONS_MAX_DAYS), (30, 60, 90))

    def test_env_days_and_months_resolve_at_import(self):
        mgr = _load_manager({"USAA_HORIZON_DAYS": "120"})
        self.assertEqual((mgr.OPTIONS_MIN_DAYS, mgr.OPTIONS_TARGET_DAYS, mgr.OPTIONS_MAX_DAYS), (60, 120, 180))
        mgr = _load_manager({"USAA_HORIZON_MONTHS": "3"})
        self.assertEqual((mgr.OPTIONS_MIN_DAYS, mgr.OPTIONS_TARGET_DAYS, mgr.OPTIONS_MAX_DAYS), (46, 91, 137))

    def test_invalid_env_stops_the_script_with_a_clear_error(self):
        with self.assertRaisesRegex(ValueError, "out of range"):
            _load_manager({"USAA_HORIZON_DAYS": "5"})
        with self.assertRaisesRegex(ValueError, "USAA_HORIZON_MONTHS"):
            _load_manager({"USAA_HORIZON_MONTHS": "x"})

    def test_validate_configuration_accepts_resolved_windows(self):
        for env in ({}, {"USAA_HORIZON_DAYS": "7"}, {"USAA_HORIZON_DAYS": "400"}):
            mgr = _load_manager(env)
            with mock.patch.object(mgr, "FMP_API_KEY", "real-key-123456"), \
                    mock.patch.object(mgr, "_is_configured_key", return_value=True):
                mgr.validate_configuration()

    def test_expiry_interpolation_uses_the_configured_horizon(self):
        mgr = _load_manager({"USAA_HORIZON_DAYS": "120"})
        est = lambda d, v: {"days": float(d), "annualized_variance": v, "skewness": -0.4, "kurtosis": 4.0}
        out = mgr.ImpliedMomentsEngine._interpolate_to_target([est(100, 0.04), est(160, 0.07)])
        self.assertEqual((out["dte_low"], out["dte_high"]), (100, 160))
        self.assertAlmostEqual(out["annualized_variance"], 0.04 + (120 - 100) / 60 * 0.03)

    def test_tail_risk_scales_sigma_with_the_configured_horizon(self):
        sigmas = {}
        for days in (30, 120):
            mgr = _load_manager({"USAA_HORIZON_DAYS": str(days)})
            rng = np.random.default_rng(11)
            tickers = [f"E{i}" for i in range(4)]
            a = rng.normal(size=(4, 4))
            cov = pd.DataFrame(a @ a.T / 4 * 0.02 + np.eye(4) * 0.01, index=tickers, columns=tickers)
            moments = pd.DataFrame({"MFIS": [-0.5] * 4, "MFIK": [4.5] * 4}, index=tickers)
            mu = pd.Series([0.08] * 4, index=tickers)
            model = mgr.ImpliedTailModel(moments, cov, n_scenarios=2000, seed=1)
            weights = pd.Series([0.25] * 4, index=tickers)
            sigmas[days] = float(mgr.PortfolioTailRisk().compute(weights, model, mu)["σ horizonte"].iloc[0])
        self.assertAlmostEqual(sigmas[120] / sigmas[30], math.sqrt(120 / 30), places=9)


class ExportHorizonTests(unittest.TestCase):
    def _export(self, env):
        mgr = _load_manager(env)
        tickers = ["AAA", "BBB"]
        profile = mgr.ProfileConfig.from_registry("Crecimiento", mgr.PROFILES)
        result = mgr.OptimizationResult(
            "test", pd.Series([0.6, 0.4], index=tickers), 0.08, 0.15, 0.5,
            pd.Series(dtype=float), 0.0, "optimal", 0.0, portfolio_beta=0.9,
        )
        moment = datetime(2026, 10, 5, 16, 40, 12, tzinfo=pipeline_io.BOGOTA)
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.dict("os.environ", {"PORTFOLIO_OUT_DIR": tmp}), \
                mock.patch.object(pipeline_io, "now_bogota", return_value=moment):
            mgr.export_portfolio_json(profile, result, 0.5, None, None)
            latest = json.loads((Path(tmp) / "portfolio_latest.json").read_text(encoding="utf-8"))
        return latest, moment

    def test_default_export_keeps_60_days(self):
        payload, moment = self._export({})
        self.assertEqual(payload["horizon_days"], 60)
        self.assertEqual(payload["horizon_end"], (moment.date() + timedelta(days=60)).isoformat())

    def test_export_carries_the_configured_horizon(self):
        for env, days in (({"USAA_HORIZON_DAYS": "120"}, 120), ({"USAA_HORIZON_MONTHS": "3"}, 91),
                          ({"USAA_HORIZON_DAYS": "7"}, 7), ({"USAA_HORIZON_DAYS": "400"}, 400)):
            with self.subTest(env=env):
                payload, moment = self._export(env)
                self.assertIsInstance(payload["horizon_days"], int)
                self.assertEqual(payload["horizon_days"], days)
                self.assertEqual(payload["horizon_end"], (moment.date() + timedelta(days=days)).isoformat())


if __name__ == "__main__":
    unittest.main()

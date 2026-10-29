"""Contrato del portafolio JSON v1 entre este repo, AM-PM-Architecture y Portfolio-Manager.

Genera un portafolio de muestra con el export de este repo (``export_portfolio_json`` ->
``pipeline_io.write_json_files``) y, si existe el checkout, con ``pipeline_io.export_portfolio`` de
AM-PM-Architecture. Ambos se leen con ``pipeline_io.load_portfolio`` de Portfolio-Manager y se
comprueba que los campos que PM lee (schema_version, tickers, weights, optimizer, run_ts,
horizon_days, horizon_end) son válidos, que los pesos suman 1 y que la carga no cae al fallback.

Los módulos hermanos se importan por ruta con nombre único (los tres se llaman ``pipeline_io``) y
sus importaciones auxiliares (nyse_calendar, registry_view, ...) no se filtran a sys.modules.
Si falta un checkout, la prueba correspondiente se omite. Rutas: AM_PM_DIR y PORTFOLIO_MANAGER_DIR.
"""
from __future__ import annotations

import contextlib
import importlib.util
import json
import math
import os
import sys
import tempfile
import types
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest import mock

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

AM_PM_DIR = Path(os.environ.get("AM_PM_DIR", "/workspace/AM-PM-Architecture"))
PM_DIR = Path(os.environ.get("PORTFOLIO_MANAGER_DIR", "/workspace/Portfolio-Manager"))
FALLBACK = {"FALLBACK": 1.0}


@contextlib.contextmanager
def _sibling_imports(directory: Path):
    """``directory`` en sys.path; al salir, restaura sys.path y olvida los módulos que salieron de ahí."""
    saved_path = list(sys.path)
    before = set(sys.modules)
    sys.path.insert(0, str(directory))
    try:
        yield
    finally:
        sys.path[:] = saved_path
        for name in set(sys.modules) - before:
            origin = getattr(sys.modules[name], "__file__", None)
            if origin and Path(origin).resolve().is_relative_to(directory.resolve()):
                del sys.modules[name]


def _load_by_path(alias: str, directory: Path):
    with _sibling_imports(directory):
        spec = importlib.util.spec_from_file_location(alias, directory / "pipeline_io.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


def _load_us_manager():
    spec = importlib.util.spec_from_file_location("us_asset_manager_contract", ROOT / "US Asset Manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["us_asset_manager_contract"] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop("us_asset_manager_contract", None)
    return module


def _us_sample(tmp: str) -> Path:
    mgr = _load_us_manager()
    tickers = ["AAA", "BBB", "CCC"]
    profile = mgr.ProfileConfig.from_registry("Crecimiento", mgr.PROFILES)
    result = mgr.OptimizationResult(
        "test", pd.Series([0.5, 0.3, 0.2], index=tickers), 0.08, 0.15, 0.5,
        pd.Series(dtype=float), 0.0, "optimal", 0.0, portfolio_beta=0.9,
    )
    with mock.patch.dict(os.environ, {"PORTFOLIO_OUT_DIR": tmp}):
        mgr.export_portfolio_json(profile, result, 0.5, None, None)
    return Path(tmp) / "portfolio_latest.json"


def _am_pm_sample(tmp: str) -> Path:
    module = _load_by_path("am_pm_pipeline_io_contract", AM_PM_DIR)
    # La exportación de AM-PM registra el historial en Supabase (best effort): aquí nunca.
    stub = types.ModuleType("portfolio_runs")
    stub.record_from_export_payload = lambda *args, **kwargs: None
    with mock.patch.dict(sys.modules, {"portfolio_runs": stub}):
        latest = module.export_portfolio(
            "minimum_variance", {"AAA": 0.5, "BBB": 0.3, "CCC": 0.2},
            risk_profile="moderado", horizon_days=60,
            horizon_end=date.today() + timedelta(days=60), out_dir=tmp,
        )
    if latest is None:
        raise AssertionError("AM-PM export_portfolio no escribió el portafolio")
    return Path(latest)


class PortfolioContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pm = None
        if (PM_DIR / "pipeline_io.py").is_file():
            cls.pm = _load_by_path("portfolio_manager_pipeline_io_contract", PM_DIR)

    def _check(self, latest: Path, expected_optimizer: str):
        if self.pm is None:
            self.skipTest(f"no hay checkout de Portfolio-Manager ({PM_DIR / 'pipeline_io.py'} no existe)")
        self.assertTrue(latest.is_file(), f"no se escribió {latest}")
        payload = json.loads(latest.read_text(encoding="utf-8"))

        # Campos que PM lee, validados sobre el JSON crudo.
        self.assertEqual(payload["schema_version"], self.pm.SCHEMA_VERSION)
        weights = payload["weights"]
        self.assertIsInstance(weights, dict)
        self.assertTrue(weights)
        self.assertEqual(payload["tickers"], list(payload["tickers"]))
        self.assertTrue(all(isinstance(t, str) and t.strip() for t in payload["tickers"]))
        self.assertEqual(set(payload["tickers"]), set(weights), "tickers y weights deben coincidir")
        self.assertEqual(len(payload["tickers"]), len(set(payload["tickers"])), "tickers repetidos")
        for ticker, weight in weights.items():
            self.assertIsInstance(weight, (int, float), ticker)
            self.assertNotIsInstance(weight, bool, ticker)
            self.assertTrue(math.isfinite(weight) and weight > 0, f"peso inválido de {ticker}: {weight!r}")
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=9)
        self.assertEqual(payload["optimizer"], expected_optimizer)
        run_ts = datetime.fromisoformat(payload["run_ts"])
        self.assertIsNotNone(run_ts.utcoffset(), "run_ts debe llevar offset")
        days = payload["horizon_days"]
        self.assertIsInstance(days, int)
        self.assertNotIsInstance(days, bool)
        self.assertGreaterEqual(days, self.pm.MIN_OPTION_DAYS)
        end = date.fromisoformat(payload["horizon_end"])
        self.assertGreater(end, run_ts.date())

        # Carga con el loader de PM, aislado del registro y de /workspace/pipeline.
        with tempfile.TemporaryDirectory() as pipeline, \
                mock.patch.dict(os.environ, {"PORTFOLIO_FILE": str(latest), "PIPELINE_DIR": pipeline}), \
                _sibling_imports(PM_DIR):
            loaded = self.pm.load_portfolio(FALLBACK)

        self.assertEqual(loaded["portfolio_source"], str(latest), f"PM cayó al fallback: {loaded}")
        self.assertNotIn("FALLBACK", loaded["weights"])
        self.assertEqual(set(loaded["weights"]), set(payload["tickers"]))
        self.assertAlmostEqual(sum(loaded["weights"].values()), 1.0, places=9)
        for ticker, weight in weights.items():
            self.assertAlmostEqual(loaded["weights"][ticker], weight, places=6, msg=ticker)
        self.assertEqual(loaded["portfolio_optimizer"], payload["optimizer"])
        self.assertEqual(loaded["portfolio_run_ts"], payload["run_ts"])
        self.assertEqual(loaded["horizon_days"], days)
        self.assertEqual(loaded["horizon_end"], payload["horizon_end"])

    def test_us_export_loads_in_portfolio_manager(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._check(_us_sample(tmp), "us_asset_manager")

    def test_am_pm_export_loads_in_portfolio_manager(self):
        if not (AM_PM_DIR / "pipeline_io.py").is_file():
            self.skipTest(f"no hay checkout de AM-PM-Architecture ({AM_PM_DIR / 'pipeline_io.py'} no existe)")
        with tempfile.TemporaryDirectory() as tmp:
            self._check(_am_pm_sample(tmp), "minimum_variance")


if __name__ == "__main__":
    unittest.main()

"""Deriva de risk_estimators.py entre US-Asset-Allocation y AM-PM-Architecture.

Reutiliza scripts/check_risk_estimators_sync.py (comparación por AST): falla si alguna función o
constante presente en ambos archivos difiere. Los símbolos que solo existen en AM-PM se permiten
(y los que solo existen aquí no cuentan como deriva). Si no hay checkout de AM-PM, se omite.

Ruta del otro archivo: variable AM_PM_RISK_ESTIMATORS, o /workspace/AM-PM-Architecture/risk_estimators.py.
"""
from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_risk_estimators_sync.py"


def _load_sync_script():
    spec = importlib.util.spec_from_file_location("check_risk_estimators_sync", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync = _load_sync_script()


def _other_path() -> Path:
    return Path(os.environ.get("AM_PM_RISK_ESTIMATORS", sync.DEFAULT_OTHER))


class RiskEstimatorsSyncTests(unittest.TestCase):
    def test_shared_definitions_match_am_pm(self):
        other = _other_path()
        if not other.is_file():
            self.skipTest(
                f"no hay checkout de AM-PM-Architecture ({other} no existe); "
                "defina AM_PM_RISK_ESTIMATORS para comparar"
            )
        mine, theirs = sync.definitions(sync.HERE), sync.definitions(other)
        shared = mine.keys() & theirs.keys()
        self.assertTrue(shared, "ningún símbolo compartido: ¿se comparó el archivo correcto?")
        differ = sorted(name for name in shared if mine[name] != theirs[name])
        self.assertEqual(
            differ, [],
            f"risk_estimators.py difiere de {other} en: {', '.join(differ)}. "
            "Sincronice ambas copias (ver scripts/check_risk_estimators_sync.py).",
        )


if __name__ == "__main__":
    unittest.main()

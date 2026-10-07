"""Barrido de γ para la penalización de cola, con datos reales (necesita FMP_API_KEY; POLYGON_API_KEY opcional).

Corre las fases 0-2 una sola vez (`PassiveETFAllocationPipeline.prepare()`) y, para cada perfil y cada γ,
resuelve el óptimo con penalización de cola. No escribe dashboards ni JSON. Uso:

    python scripts/sweep_tail_penalty.py [--gammas 0,0.5,1,2,4] [--profiles Conservador,Crecimiento]

γ = 0 es la solución media-varianza de siempre. Columnas por fila:
  E[R], σ        retorno esperado y volatilidad implícita anuales del portafolio
  γ·P            término de penalización (γ · σ_p · (ES_CF − ES_gauss)), en unidades de utilidad
  1/2·λσ²        término de varianza, para comparar la magnitud con γ·P
  CVaR95 60d     CVaR Cornish-Fisher al 95% a 60 días (pérdida en positivo)
  skew, exkurt   asimetría y exceso de curtosis del portafolio al horizonte común
  Δw (L1)        distancia L1 de los pesos a la solución γ = 0 (máximo 2)
  ETFs, w_max    ETFs activos (> 0.01%) y mayor peso
"""
from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_manager():
    spec = importlib.util.spec_from_file_location("us_asset_manager", ROOT / "US Asset Manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["us_asset_manager"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gammas", default="0,0.5,1,2,4")
    parser.add_argument("--profiles", default="")
    args = parser.parse_args()
    gammas = [float(g) for g in args.gammas.split(",")]

    mgr = load_manager()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s", datefmt="%H:%M:%S")
    names = [n for n in args.profiles.split(",") if n] or list(mgr.PROFILES)

    pipeline = mgr.PassiveETFAllocationPipeline()
    inputs = pipeline.prepare()
    tickers = inputs.tickers
    model = mgr.ImpliedTailModel(inputs.moments.loc[tickers], inputs.covariance.loc[tickers, tickers])
    mu = inputs.mu_table["Mu_Base"]
    reporter = mgr.PortfolioTailRisk(confidence_levels=(0.95,))

    rows = []
    for name in names:
        profile = mgr.ProfileConfig.from_registry(name, mgr.PROFILES)
        optimizer = mgr.PortfolioOptimizer(mu, inputs.covariance, inputs.factor_matrix, profile, model)
        base = optimizer.solve(mgr.SOLVER)
        for gamma in gammas:
            tuned = dataclasses.replace(profile, tail_penalty=gamma)
            tail_optimizer = mgr.PortfolioOptimizer(mu, inputs.covariance, inputs.factor_matrix, tuned, model)
            result = tail_optimizer.solve_with_tail(base) if gamma > 0 else base
            w = result.weights.to_numpy(dtype=float)
            excess = model.excess_tail(w, tickers)[0]
            risk = reporter.compute(result.weights, model, mu).loc["95%"]
            rows.append({
                "Perfil": name, "γ": gamma,
                "E[R]": result.expected_return, "σ": result.volatility,
                "γ·P": gamma * excess, "½λσ²": 0.5 * profile.risk_aversion * result.volatility**2,
                "CVaR95 60d": risk["CVaR CF"], "skew": risk["Asimetría"], "exkurt": risk["Curtosis exc."],
                "Δw (L1)": float(np.abs(w - base.weights.to_numpy()).sum()),
                "ETFs": int((w > 1e-4).sum()), "w_max": float(w.max()),
            })
    table = pd.DataFrame(rows)
    pd.set_option("display.width", 200)
    print(table.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()

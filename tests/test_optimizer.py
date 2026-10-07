"""Pruebas del optimizador de 'US Asset Manager.py' con datos sintéticos (sin red)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load_manager():
    spec = importlib.util.spec_from_file_location("us_asset_manager", ROOT / "US Asset Manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["us_asset_manager"] = module
    spec.loader.exec_module(module)
    return module


mgr = _load_manager()


def _synthetic_inputs(n: int = 8, seed: int = 7):
    rng = np.random.default_rng(seed)
    tickers = [f"E{i}" for i in range(n)]
    mu = pd.Series(rng.uniform(0.04, 0.12, n), index=tickers)
    a = rng.normal(size=(n, n))
    cov = pd.DataFrame(a @ a.T / n * 0.02 + np.eye(n) * 0.01, index=tickers, columns=tickers)
    factors = pd.DataFrame(rng.uniform(0.1, 0.9, (n, len(mgr.FACTORS))), index=tickers, columns=list(mgr.FACTORS))
    return mu, cov, factors


def _profile(max_weight=0.4, risk_aversion=4.0, targets=None):
    targets = targets or {}
    return mgr.ProfileConfig(
        "test", risk_aversion, max_weight, {f: float(targets.get(f, 0.0)) for f in mgr.FACTORS}
    )


class PortfolioConstraintTests(unittest.TestCase):
    def setUp(self):
        self.mu, self.cov, self.factors = _synthetic_inputs()

    def _check_basic(self, result, max_weight):
        w = result.weights
        self.assertAlmostEqual(float(w.sum()), 1.0, places=6)
        self.assertGreaterEqual(float(w.min()), 0.0)
        self.assertLessEqual(float(w.max()), max_weight + 1e-6)

    def test_scipy_respects_budget_and_cap(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile())
        self._check_basic(opt.solve("scipy"), 0.4)

    @unittest.skipUnless(mgr.CVXPY_AVAILABLE, "cvxpy no instalado")
    def test_cvxpy_respects_budget_and_cap(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile())
        self._check_basic(opt.solve("cvxpy"), 0.4)

    def test_qubo_respects_budget_and_cap(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile())
        self._check_basic(opt.solve("qubo_sa"), 0.4)

    def test_cap_raised_when_too_small_for_full_investment(self):
        # n=8 activos con tope 5% no puede sumar 100%: el tope debe subir a 1/n.
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile(max_weight=0.05))
        self.assertGreaterEqual(opt.max_weight, 1.0 / 8)
        self._check_basic(opt.solve("scipy"), opt.max_weight)

    def test_unknown_solver_raises(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile())
        with self.assertRaises(ValueError):
            opt.solve("no_existe")


class FactorTargetTests(unittest.TestCase):
    def setUp(self):
        self.mu, self.cov, self.factors = _synthetic_inputs()

    def test_feasible_targets_are_not_relaxed(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile(targets={"Quality": 0.30}))
        self.assertTrue(np.allclose(opt.target_relaxation, 0.0))
        result = opt.solve("scipy")
        self.assertLessEqual(result.max_factor_violation, 1e-5)
        self.assertGreaterEqual(float(result.factor_exposure["Quality"]), 0.30 - 1e-5)

    def test_infeasible_targets_are_relaxed_minimally(self):
        # Ningún activo supera 0.9 en ningún factor: exigir 0.99 es infactible.
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile(targets={"Value": 0.99}))
        idx = list(mgr.FACTORS).index("Value")
        self.assertGreater(opt.target_relaxation[idx], 0.0)
        self.assertTrue(np.all(np.delete(opt.target_relaxation, idx) == 0.0))
        # El target efectivo debe poder alcanzarse: el solver no falla ni viola.
        result = opt.solve("scipy")
        self.assertLessEqual(result.max_factor_violation, 1e-4)

    @unittest.skipUnless(mgr.CVXPY_AVAILABLE, "cvxpy no instalado")
    def test_cvxpy_and_scipy_agree(self):
        opt = mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, _profile(targets={"Quality": 0.30}))
        a, b = opt.solve("cvxpy"), opt.solve("scipy")
        self.assertAlmostEqual(a.utility, b.utility, places=5)
        self.assertTrue(np.allclose(a.weights.to_numpy(), b.weights.to_numpy(), atol=1e-3))


class RiskContributionTests(unittest.TestCase):
    def test_contributions_sum_to_one(self):
        mu, cov, factors = _synthetic_inputs()
        weights = mgr.PortfolioOptimizer(mu, cov, factors, _profile()).solve("scipy").weights
        risk = mgr.ConsoleReporter.risk_contributions(weights, cov)
        self.assertAlmostEqual(float(risk.sum()), 1.0, places=10)
        self.assertTrue((risk[weights == 0.0] == 0.0).all())


def _tail_inputs(n=6, seed=11, skews=None, kurts=None):
    mu, cov, factors = _synthetic_inputs(n, seed)
    skews = skews if skews is not None else np.linspace(-1.2, 0.2, n)
    kurts = kurts if kurts is not None else np.linspace(6.0, 3.5, n)
    moments = pd.DataFrame({"MFIS": skews, "MFIK": kurts}, index=cov.index)
    return mu, cov, factors, moments


class TailModelTests(unittest.TestCase):
    def setUp(self):
        self.mu, self.cov, self.factors, self.moments = _tail_inputs()
        self.model = mgr.ImpliedTailModel(self.moments, self.cov, n_scenarios=20000, seed=1)
        self.tickers = list(self.cov.index)

    def test_marginals_reproduce_implied_skew_and_kurtosis(self):
        for i, ticker in enumerate(self.tickers):
            w = np.zeros(len(self.tickers))
            w[i] = 1.0
            m = self.model.portfolio_moments(w[w > 0], [ticker])
            self.assertAlmostEqual(m["skew"], self.moments.loc[ticker, "MFIS"], delta=0.12)
            self.assertAlmostEqual(m["exkurt"], self.moments.loc[ticker, "MFIK"] - 3.0, delta=0.6)

    def test_scenarios_reproduce_covariance_volatility(self):
        w = np.full(len(self.tickers), 1.0 / len(self.tickers))
        self.assertAlmostEqual(
            self.model.portfolio_moments(w, self.tickers)["sd"], self.model.volatility(w, self.tickers), delta=0.01
        )

    def test_inadmissible_moments_fall_back_to_gaussian(self):
        _, cov, _, moments = _tail_inputs(skews=np.full(6, np.nan), kurts=np.full(6, np.nan))
        model = mgr.ImpliedTailModel(moments, cov, n_scenarios=20000, seed=1)
        w = np.zeros(6)
        w[0] = 1.0
        m = model.portfolio_moments(w[w > 0], [cov.index[0]])
        self.assertAlmostEqual(m["skew"], 0.0, delta=0.1)
        self.assertAlmostEqual(m["exkurt"], 0.0, delta=0.2)

    def test_excess_tail_gradient_matches_finite_differences(self):
        rng = np.random.default_rng(5)
        w = rng.dirichlet(np.ones(len(self.tickers)))
        _, grad = self.model.excess_tail(w, self.tickers)
        h = 1e-5
        numeric = np.array([
            (self.model.excess_tail(w + h * np.eye(len(w))[i], self.tickers)[0]
             - self.model.excess_tail(w - h * np.eye(len(w))[i], self.tickers)[0]) / (2 * h)
            for i in range(len(w))
        ])
        self.assertTrue(np.allclose(grad, numeric, rtol=2e-2, atol=2e-3), (grad, numeric))


class TailPenaltySolveTests(unittest.TestCase):
    def setUp(self):
        self.mu, self.cov, self.factors, self.moments = _tail_inputs()
        self.model = mgr.ImpliedTailModel(self.moments, self.cov, n_scenarios=20000, seed=1)

    def _optimizer(self, gamma, with_model=True):
        profile = mgr.ProfileConfig("test", 4.0, 0.5, {f: 0.0 for f in mgr.FACTORS}, gamma)
        return mgr.PortfolioOptimizer(self.mu, self.cov, self.factors, profile, self.model if with_model else None)

    def test_gamma_zero_or_no_model_returns_base_unchanged(self):
        base = self._optimizer(0.0).solve("scipy")
        self.assertIs(self._optimizer(0.0).solve_with_tail(base), base)
        self.assertIs(self._optimizer(2.0, with_model=False).solve_with_tail(base), base)

    def test_penalty_keeps_constraints_and_lowers_excess_tail(self):
        optimizer = self._optimizer(3.0)
        base = optimizer.solve("scipy")
        tail = optimizer.solve_with_tail(base)
        self.assertTrue(tail.method.endswith("+colas"))
        self.assertAlmostEqual(float(tail.weights.sum()), 1.0, places=6)
        self.assertLessEqual(float(tail.weights.max()), 0.5 + 1e-6)
        tickers = optimizer.tickers
        before = self.model.excess_tail(base.weights.to_numpy(), tickers)[0]
        after = self.model.excess_tail(tail.weights.to_numpy(), tickers)[0]
        self.assertLessEqual(after, before + 1e-9)
        # El objetivo con penalización no puede empeorar respecto de la solución de partida.
        total = lambda r: optimizer.utility(r.weights.to_numpy()) - 3.0 * self.model.excess_tail(r.weights.to_numpy(), tickers)[0]
        self.assertGreaterEqual(total(tail), total(base) - 1e-7)


class TailRiskReportTests(unittest.TestCase):
    def test_cvar_exceeds_var_and_fat_tails_reported(self):
        mu, cov, _, moments = _tail_inputs()
        model = mgr.ImpliedTailModel(moments, cov, n_scenarios=20000, seed=1)
        weights = pd.Series(np.full(6, 1 / 6), index=cov.index)
        table = mgr.PortfolioTailRisk().compute(weights, model, mu)
        self.assertEqual(list(table.index), ["95%", "99%"])
        self.assertTrue((table["CVaR CF"] >= table["VaR CF"]).all())
        self.assertTrue((table["CVaR gaussiano"] >= table["VaR gaussiano"]).all())
        self.assertLess(float(table["Asimetría"].iloc[0]), 0.0)

    def test_ignores_zero_weight_assets(self):
        mu, cov, _, moments = _tail_inputs()
        model = mgr.ImpliedTailModel(moments, cov, n_scenarios=20000, seed=1)
        weights = pd.Series([1.0, 0, 0, 0, 0, 0], index=cov.index)
        self.assertFalse(mgr.PortfolioTailRisk().compute(weights, model, mu).empty)


class HorizonAlignmentTests(unittest.TestCase):
    def _estimate(self, days, var, skew, kurt):
        return {"days": float(days), "annualized_variance": var, "skewness": skew, "kurtosis": kurt}

    def test_interpolates_between_bracketing_expiries_and_records_dte(self):
        target = mgr.OPTIONS_TARGET_DAYS
        low, high = self._estimate(target - 20, 0.04, -0.6, 5.0), self._estimate(target + 20, 0.06, -0.2, 4.0)
        out = mgr.ImpliedMomentsEngine._interpolate_to_target([high, low])
        self.assertAlmostEqual(out["annualized_variance"], 0.05)
        self.assertEqual((out["dte_low"], out["dte_high"]), (target - 20, target + 20))

    def test_one_sided_uses_nearest_unless_bracket_required(self):
        target = mgr.OPTIONS_TARGET_DAYS
        estimates = [self._estimate(target + 10, 0.05, -0.3, 4.5), self._estimate(target + 30, 0.06, -0.2, 4.0)]
        out = mgr.ImpliedMomentsEngine._interpolate_to_target(estimates)
        self.assertEqual((out["dte_low"], out["dte_high"]), (target + 10, target + 10))
        with mock_patch(mgr, "OPTIONS_REQUIRE_BRACKET", True):
            self.assertIsNone(mgr.ImpliedMomentsEngine._interpolate_to_target(estimates))

    def test_iid_scaling_to_target_horizon(self):
        from risk_estimators import scale_moments, to_years
        out = scale_moments(to_years(dte=30), to_years(dte=mgr.OPTIONS_TARGET_DAYS), skew=-0.8, exkurt=2.0)
        h = mgr.OPTIONS_TARGET_DAYS / 30
        self.assertAlmostEqual(out["skew"], -0.8 / np.sqrt(h))
        self.assertAlmostEqual(out["exkurt"], 2.0 / h)

    def test_historical_fallback_is_scaled_to_target_horizon(self):
        rng = np.random.default_rng(0)
        prices = pd.DataFrame({"A": 100 * np.cumprod(1 + rng.standard_t(4, 400) * 0.01)})
        engine = mgr.ImpliedMomentsEngine(None, None, prices, 0.04)
        row = engine._historical_fallback("A")
        daily = prices["A"].pct_change().dropna().tail(mgr.VOLATILITY_LOOKBACK_DAYS)
        self.assertLess(abs(row["MFIS"]), abs(float(pd.Series(daily).skew())) + 1e-9)
        self.assertAlmostEqual(row["MFIK"] - 3.0, float(daily.kurt()) / mgr.OPTIONS_TARGET_DAYS * (365.0 / 252.0), delta=0.05)
        self.assertTrue(np.isnan(row["DTE bajo"]))


class mock_patch:
    """Cambia un atributo del módulo durante un bloque with."""

    def __init__(self, module, name, value):
        self.module, self.name, self.value = module, name, value

    def __enter__(self):
        self.old = getattr(self.module, self.name)
        setattr(self.module, self.name, self.value)

    def __exit__(self, *exc):
        setattr(self.module, self.name, self.old)


if __name__ == "__main__":
    unittest.main()

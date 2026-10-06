"""Tests de risk_estimators (Ledoit-Wolf con pesos EWMA). Sin red."""

from __future__ import annotations

import logging
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import risk_estimators as rk


def _retornos_shock_covid() -> np.ndarray:
    """367 semanas con un crash de 2 semanas (y 4 de resaca) al inicio de la serie."""
    rng = np.random.default_rng(5)
    T, n = 367, 10
    L = rng.normal(size=(n, n))
    C = L @ L.T / n + np.eye(n) * 0.5
    X = rng.standard_normal((T, n)) @ np.linalg.cholesky(C).T * 0.02
    X += rng.standard_normal(T)[:, None] * 0.01
    X[24:26] = -0.25 + rng.standard_normal((2, n)) * 0.08
    X[26:30] *= 4.0
    return X


def _retornos_normales() -> np.ndarray:
    rng = np.random.default_rng(11)
    T, n = 400, 6
    L = rng.normal(size=(n, n))
    C = L @ L.T / n + np.eye(n) * 0.5
    return rng.standard_normal((T, n)) @ np.linalg.cholesky(C).T * 0.01


def _delta_referencia(X: np.ndarray, w: np.ndarray) -> float:
    """delta bruto con bucles: pi, rho y S con los pesos w, divisor Kish."""
    T, n = X.shape
    w = w / w.sum()
    Xc = X - w @ X
    S = np.array([[np.sum(w * Xc[:, i] * Xc[:, j]) for j in range(n)] for i in range(n)])
    sd = np.sqrt(np.diag(S))
    rbar = np.mean([S[i, j] / (sd[i] * sd[j]) for i in range(n) for j in range(n) if i != j])
    F = rbar * np.outer(sd, sd)
    np.fill_diagonal(F, np.diag(S))
    pi = np.array([[np.sum(w * (Xc[:, i] * Xc[:, j] - S[i, j]) ** 2) for j in range(n)]
                   for i in range(n)])
    rho = np.trace(pi)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            th_ii = np.sum(w * (Xc[:, i] ** 2 - S[i, i]) * (Xc[:, i] * Xc[:, j] - S[i, j]))
            th_jj = np.sum(w * (Xc[:, j] ** 2 - S[j, j]) * (Xc[:, i] * Xc[:, j] - S[i, j]))
            rho += (rbar / 2.0) * (sd[j] / sd[i] * th_ii + sd[i] / sd[j] * th_jj)
    gamma = np.sum((F - S) ** 2)
    return float((pi.sum() - rho) / gamma / (1.0 / np.sum(w ** 2)))


class LedoitWolfEwmaTests(unittest.TestCase):
    def test_no_saturation_with_covid_shock(self) -> None:
        X = _retornos_shock_covid()
        cov_e, w = rk.ewma_cov(X, halflife=26)
        t_eff = rk.effective_sample_size(w)

        # Forma anterior (pi y rho sin pesos, divisor t_eff): se satura.
        with self.assertLogs("risk_estimators", level="WARNING"):
            _, delta_viejo, _, info_viejo = rk.ledoit_wolf_constant_correlation(
                X, S=cov_e, t_eff=t_eff, return_info=True)
        self.assertGreater(info_viejo["delta_raw"], 1.0)
        self.assertEqual(delta_viejo, 1.0)

        # Forma consistente: coincide con la referencia con bucles y no se satura.
        esperado = _delta_referencia(X, w)
        with self.assertNoLogs("risk_estimators", level="WARNING"):
            cov, info = rk.cov_ewma_shrunk(X, halflife=26)
        self.assertAlmostEqual(info["delta_raw"], esperado, delta=abs(esperado) * 1e-9)
        self.assertAlmostEqual(info["delta"], esperado, delta=abs(esperado) * 1e-9)
        self.assertTrue(0.0 < info["delta"] < rk.LW_DELTA_MAX)
        self.assertAlmostEqual(info["t_eff"], t_eff)

    def test_weights_none_vs_ewma_weights_reconstruct_same_matrix(self) -> None:
        X = _retornos_normales()
        cov_e, w = rk.ewma_cov(X, halflife=60)
        S_shr, delta, F = rk.ledoit_wolf_constant_correlation(
            X, S=cov_e, t_eff=rk.effective_sample_size(w), weights=w)
        self.assertTrue(0.0 <= delta <= 1.0)
        self.assertTrue(np.allclose(S_shr, delta * F + (1 - delta) * cov_e))
        # S=None con los mismos pesos reconstruye la misma matriz y el mismo delta
        S_def, delta_def, _ = rk.ledoit_wolf_constant_correlation(X, weights=w)
        self.assertAlmostEqual(delta_def, delta, delta=abs(delta) * 1e-10)
        self.assertTrue(np.allclose(S_def, S_shr, rtol=1e-10, atol=1e-14))

    def test_delta_cap_logs_raw_delta(self) -> None:
        X = _retornos_shock_covid()
        cov_e, w = rk.ewma_cov(X, halflife=26)
        with self.assertLogs("risk_estimators", level="WARNING") as cm:
            S_shr, delta, F, info = rk.ledoit_wolf_constant_correlation(
                X, S=cov_e, t_eff=rk.effective_sample_size(w), delta_max=0.9,
                return_info=True)
        self.assertGreater(info["delta_raw"], 1.0)
        self.assertAlmostEqual(delta, 0.9)
        self.assertEqual(delta, info["delta"])
        self.assertTrue(np.allclose(S_shr, 0.9 * F + 0.1 * cov_e))
        self.assertTrue(any("delta bruto" in m for m in cm.output))

        # La cota del pipeline tambien recorta y guarda ambos valores
        with self.assertLogs("risk_estimators", level="WARNING"):
            _, info_p = rk.cov_ewma_shrunk(X, halflife=26, lw_delta_max=0.05)
        self.assertAlmostEqual(info_p["delta"], 0.05)
        self.assertGreater(info_p["delta_raw"], 0.05)

    def test_classic_unweighted_case_unchanged(self) -> None:
        X = _retornos_normales()
        T, n = X.shape
        S_shr, delta, F, info = rk.ledoit_wolf_constant_correlation(X, return_info=True)

        # Referencia clasica (Ledoit-Wolf 2003, iid, divide por T) con bucles.
        delta_ref = _delta_referencia(X, np.full(T, 1.0 / T))
        self.assertAlmostEqual(info["delta_raw"], delta_ref, delta=abs(delta_ref) * 1e-9)
        self.assertEqual(delta, info["delta"])
        self.assertTrue(0.0 < delta < 1.0)

        # weights=None y pesos iguales explicitos dan lo mismo.
        S2, delta2, _ = rk.ledoit_wolf_constant_correlation(X, weights=np.full(T, 1.0 / T))
        self.assertAlmostEqual(delta2, delta, delta=1e-12)
        self.assertTrue(np.allclose(S2, S_shr, rtol=1e-12, atol=1e-18))

        # La salida de 3 elementos sigue siendo la de siempre.
        out = rk.ledoit_wolf_constant_correlation(X)
        self.assertEqual(len(out), 3)

    def test_weights_shape_validated(self) -> None:
        X = _retornos_normales()
        with self.assertRaises(ValueError):
            rk.ledoit_wolf_constant_correlation(X, weights=np.ones(X.shape[0] - 1))


if __name__ == "__main__":
    unittest.main()

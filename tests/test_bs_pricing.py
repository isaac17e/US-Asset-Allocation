"""Pruebas de equivalencia exacta para los precios de opciones extraídos."""
from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from unittest import mock
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import bs_pricing  # noqa: E402


class _Frozen:
    """Copia congelada del código previo a la extracción a bs_pricing.py; no editar."""

    MIN_TOTAL_VOL = 1e-3

    @staticmethod
    def bs_price(spot, strike, rate, carry, maturity, vol, side):
        if vol <= 0.0 or maturity <= 0.0:
            return max(0.0, (spot - strike) if side == "call" else (strike - spot))
        scaled_vol = vol * math.sqrt(maturity)
        d1 = (math.log(spot / strike) + (carry + 0.5 * vol**2) * maturity) / scaled_vol
        d2 = d1 - scaled_vol
        carry_factor = math.exp((carry - rate) * maturity)
        discount = math.exp(-rate * maturity)
        if side == "call":
            return spot * carry_factor * stats.norm.cdf(d1) - strike * discount * stats.norm.cdf(d2)
        return strike * discount * stats.norm.cdf(-d2) - spot * carry_factor * stats.norm.cdf(-d1)

    @staticmethod
    def bs93_phi(spot, maturity, gamma, boundary, trigger, rate, carry, vol, log_offset=0.0):
        variance = vol**2
        scaled_vol = vol * math.sqrt(maturity)
        lam = (-rate + gamma * carry + 0.5 * gamma * (gamma - 1.0) * variance) * maturity
        kappa = 2.0 * carry / variance + (2.0 * gamma - 1.0)
        d = -(math.log(spot / boundary) + (carry + (gamma - 0.5) * variance) * maturity) / scaled_vol
        d_reflected = d - 2.0 * math.log(trigger / spot) / scaled_vol
        log_scale = lam + gamma * math.log(spot) + log_offset
        reflected = math.exp(log_scale + kappa * math.log(trigger / spot) + stats.norm.logcdf(d_reflected))
        return math.exp(log_scale) * stats.norm.cdf(d) - reflected

    @classmethod
    def american_call(cls, spot, strike, rate, carry, maturity, vol):
        european = cls.bs_price(spot, strike, rate, carry, maturity, vol, "call")
        if carry >= rate:
            return european
        if vol * math.sqrt(maturity) < cls.MIN_TOTAL_VOL:
            return max(spot - strike, european)
        variance = vol**2
        beta = (0.5 - carry / variance) + math.sqrt((carry / variance - 0.5) ** 2 + 2.0 * rate / variance)
        boundary_inf = beta / (beta - 1.0) * strike
        boundary_now = max(strike, rate / (rate - carry) * strike)
        if boundary_inf <= boundary_now:
            return european
        h = -(carry * maturity + 2.0 * vol * math.sqrt(maturity)) * boundary_now / (boundary_inf - boundary_now)
        if h >= 0.0:
            return max(spot - strike, european)
        trigger = boundary_now + (boundary_inf - boundary_now) * (1.0 - math.exp(h))
        if spot >= trigger:
            return spot - strike
        premium, log_alpha = trigger - strike, -beta * math.log(trigger)
        return (
            premium * math.exp(beta * math.log(spot / trigger))
            - premium * cls.bs93_phi(spot, maturity, beta, trigger, trigger, rate, carry, vol, log_alpha)
            + cls.bs93_phi(spot, maturity, 1.0, trigger, trigger, rate, carry, vol)
            - cls.bs93_phi(spot, maturity, 1.0, strike, trigger, rate, carry, vol)
            - strike * cls.bs93_phi(spot, maturity, 0.0, trigger, trigger, rate, carry, vol)
            + strike * cls.bs93_phi(spot, maturity, 0.0, strike, trigger, rate, carry, vol)
        )

    @classmethod
    def american_price(cls, spot, strike, rate, carry, maturity, vol, side):
        if vol <= 0.0 or maturity <= 0.0:
            return max(0.0, (spot - strike) if side == "call" else (strike - spot))
        if side == "call":
            return cls.american_call(spot, strike, rate, carry, maturity, vol)
        return cls.american_call(strike, spot, rate - carry, -carry, maturity, vol)


def _outcome(fn, *args, **kwargs):
    try:
        return ("ok", repr(float(fn(*args, **kwargs))))
    except Exception as exc:
        return ("err", type(exc).__name__)


def _load_manager():
    spec = importlib.util.spec_from_file_location("us_asset_manager_bs", ROOT / "US Asset Manager.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["us_asset_manager_bs"] = module
    spec.loader.exec_module(module)
    return module


class BlackScholesPricingTests(unittest.TestCase):
    def test_bs_price_matches_frozen_grid(self):
        for strike in (50.0, 80.0, 95.0, 100.0, 105.0, 120.0, 200.0):
            for rate in (0.0, 0.01, 0.04, 0.08):
                for q in (0.0, 0.02, 0.06):
                    for maturity in (1 / 365, 7 / 365, 30 / 365, 60 / 365, 0.5, 2.0):
                        for vol in (0.02, 0.05, 0.2, 0.6, 1.5, 5.0):
                            for side in ("call", "put"):
                                args = (100.0, strike, rate, rate - q, maturity, vol, side)
                                with self.subTest(args=args):
                                    self.assertEqual(_outcome(bs_pricing.bs_price, *args), _outcome(_Frozen.bs_price, *args))

    def test_bs93_phi_matches_frozen_grid(self):
        for gamma in (0.0, 1.0, 2.5):
            for boundary, trigger in ((100, 130), (120, 130), (130, 130), (80, 110)):
                for maturity in (30/365, 0.5, 2.0):
                    for rate in (0.01, 0.05):
                        for carry in (rate, rate - 0.02):
                            for vol in (0.1, 0.3, 0.8):
                                for offset in (0.0, -5.0, 12.0):
                                    args = (100.0, maturity, gamma, boundary, trigger, rate, carry, vol, offset)
                                    with self.subTest(args=args):
                                        self.assertEqual(
                                            _outcome(bs_pricing.bs93_phi, *args),
                                            _outcome(_Frozen.bs93_phi, *args),
                                        )

    def test_american_price_matches_frozen_grid_and_branches(self):
        points = []
        for strike in (50.0, 80.0, 95.0, 100.0, 105.0, 120.0, 200.0):
            for rate in (0.0, 0.01, 0.04, 0.08):
                for q in (0.0, 0.02, 0.06):
                    for maturity in (1 / 365, 7 / 365, 30 / 365, 60 / 365, 0.5, 2.0):
                        for vol in (0.02, 0.05, 0.2, 0.6, 1.5, 5.0):
                            for side in ("call", "put"):
                                points.append((100.0, strike, rate, rate - q, maturity, vol, side))
        points.extend([
            (100.0, 100.0, 0.01, 0.03, 0.5, 0.3, "call"),
            (100.0, 100.0, 0.04, 0.0399, 1.0, 0.3, "call"),
            (100.0, 50.0, 0.05, 0.0, 1.0, 0.3, "call"),
            (100.0, 100.0, 0.05, 0.0, 1.0, 0.3, "call"),
            (100.0, 100.0, 0.01, 0.0, 1 / 365, 0.0005, "call"),
        ])
        for args in points:
            with self.subTest(args=args):
                actual = _outcome(bs_pricing.american_price, *args, min_total_vol=1e-3)
                expected = _outcome(_Frozen.american_price, *args)
                self.assertEqual(actual, expected)

    def test_degenerate_prices_and_european_parity(self):
        for strike in (50.0, 100.0, 200.0):
            for maturity in (0.0, -1.0, 0.5):
                for vol in (-0.1, 0.0, 0.2):
                    for side in ("call", "put"):
                        args = (100.0, strike, 0.04, 0.02, maturity, vol, side)
                        self.assertEqual(_outcome(bs_pricing.bs_price, *args), _outcome(_Frozen.bs_price, *args))
                        if vol <= 0 or maturity <= 0:
                            self.assertEqual(bs_pricing.bs_price(*args), max(0.0, 100.0-strike) if side == "call" else max(0.0, strike-100.0))
        for strike in (80.0, 100.0, 120.0):
            c = bs_pricing.bs_price(100, strike, .04, .02, .5, .3, "call")
            p = bs_pricing.bs_price(100, strike, .04, .02, .5, .3, "put")
            self.assertAlmostEqual(c-p, 100*math.exp((.02-.04)*.5)-strike*math.exp(-.04*.5), places=9)

    def test_frozen_golden_values(self):
        points = [
            ("bs_call", bs_pricing.bs_price(100, 100, .04, .02, .25, .2, "call"), 4.211051783165651),
            ("bs_put", bs_pricing.bs_price(100, 100, .04, .02, .25, .2, "put"), 3.7147872388142176),
            ("bs_wing", bs_pricing.bs_price(100, 120, .04, 0, 1, .6, "call"), 16.419704341459965),
            ("american_put", bs_pricing.american_price(100, 100, .05, 0, 1, .3, "put", 1e-3), 11.442345792431674),
            ("american_call", bs_pricing.american_price(100, 95, .05, 0, .5, .25, "call", 1e-3), 9.45714600587835),
            ("american_short_put", bs_pricing.american_price(100, 100, .04, .02, 60/365, .2, "put", 1e-3), 3.067738514208031),
        ]
        for label, actual, expected in points:
            with self.subTest(label=label):
                self.assertTrue(math.isclose(actual, expected, rel_tol=1e-12))

    def test_manager_delegates_pricing_to_module(self):
        manager = _load_manager()
        self.assertEqual(manager.MIN_TOTAL_VOL, 1e-3)
        for strike, rate, carry, maturity, vol, side in (
            (90, .05, .03, .5, .15, "put"), (100, .04, .02, 60/365, .4, "call"), (110, .05, .05, 1, .3, "put")
        ):
            price = _Frozen.american_price(100, strike, rate, carry, maturity, vol, side)
            implied = manager.BKMEstimator._implied_vol(price, 100, strike, rate, carry, maturity, side)
            self.assertTrue(math.isclose(implied, vol, rel_tol=1e-5, abs_tol=1e-5))


    def test_manager_moments_match_frozen_pricer_delegation(self):
        manager = _load_manager()
        strikes = np.arange(70.0, 135.0, 5.0)
        maturity, rate, q = 60/365, 0.04, 0.02
        vols = np.maximum(0.05, 0.20 + 0.0004 * (100.0 - strikes))
        calls = np.array([
            _Frozen.bs_price(100.0, k, rate, rate-q, maturity, vol, "call")
            for k, vol in zip(strikes, vols)
        ])
        puts = np.array([
            _Frozen.bs_price(100.0, k, rate, rate-q, maturity, vol, "put")
            for k, vol in zip(strikes, vols)
        ])
        args = (100.0, maturity, rate, strikes, calls, strikes, puts)
        actual = manager.BKMEstimator.moments(*args, div_yield=q)
        with mock.patch.object(bs_pricing, "bs_price", side_effect=_Frozen.bs_price), mock.patch.object(
            bs_pricing, "american_price", side_effect=lambda *a, min_total_vol: _Frozen.american_price(*a)
        ):
            frozen = manager.BKMEstimator.moments(*args, div_yield=q)
        self.assertEqual(actual, frozen)


if __name__ == "__main__":
    unittest.main()

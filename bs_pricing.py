"""Precios Black-Scholes (europeo) y Bjerksund-Stensland 1993 (americano) con costo de acarreo.

Lo usa BKMEstimator en 'US Asset Manager.py'. Extracción literal del código previo: conserva
las mismas fórmulas y el orden de operaciones.
"""
from __future__ import annotations

import math

from scipy.stats import norm

__all__ = ["bs_price", "bs93_phi", "american_call", "american_price"]


def bs_price(
    spot: float, strike: float, rate: float, carry: float, maturity: float, vol: float, side: str
) -> float:
    if vol <= 0.0 or maturity <= 0.0:
        return max(0.0, (spot - strike) if side == "call" else (strike - spot))
    scaled_vol = vol * math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (carry + 0.5 * vol**2) * maturity) / scaled_vol
    d2 = d1 - scaled_vol
    carry_factor = math.exp((carry - rate) * maturity)
    discount = math.exp(-rate * maturity)
    if side == "call":
        return spot * carry_factor * norm.cdf(d1) - strike * discount * norm.cdf(d2)
    return strike * discount * norm.cdf(-d2) - spot * carry_factor * norm.cdf(-d1)


def bs93_phi(
    spot: float, maturity: float, gamma: float, boundary: float, trigger: float,
    rate: float, carry: float, vol: float, log_offset: float = 0.0,
) -> float:
    variance = vol**2
    scaled_vol = vol * math.sqrt(maturity)
    lam = (-rate + gamma * carry + 0.5 * gamma * (gamma - 1.0) * variance) * maturity
    kappa = 2.0 * carry / variance + (2.0 * gamma - 1.0)
    d = -(math.log(spot / boundary) + (carry + (gamma - 0.5) * variance) * maturity) / scaled_vol
    d_reflected = d - 2.0 * math.log(trigger / spot) / scaled_vol
    # Todo se arma en logaritmos y log_offset absorbe el alpha del llamador: a vol baja beta crece
    # como 1/vol^2 y los factores sueltos (spot**beta, (trigger/spot)**kappa) desbordan por
    # separado aunque el producto siga siendo finito.
    log_scale = lam + gamma * math.log(spot) + log_offset
    reflected = math.exp(log_scale + kappa * math.log(trigger / spot) + norm.logcdf(d_reflected))
    return math.exp(log_scale) * norm.cdf(d) - reflected


def american_call(
    spot: float, strike: float, rate: float, carry: float, maturity: float, vol: float, min_total_vol: float
) -> float:
    european = bs_price(spot, strike, rate, carry, maturity, vol, "call")
    if carry >= rate:
        return european
    if vol * math.sqrt(maturity) < min_total_vol:  # régimen casi determinista: la frontera degenera
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
        - premium * bs93_phi(spot, maturity, beta, trigger, trigger, rate, carry, vol, log_alpha)
        + bs93_phi(spot, maturity, 1.0, trigger, trigger, rate, carry, vol)
        - bs93_phi(spot, maturity, 1.0, strike, trigger, rate, carry, vol)
        - strike * bs93_phi(spot, maturity, 0.0, trigger, trigger, rate, carry, vol)
        + strike * bs93_phi(spot, maturity, 0.0, strike, trigger, rate, carry, vol)
    )


def american_price(
    spot: float, strike: float, rate: float, carry: float, maturity: float,
    vol: float, side: str, min_total_vol: float,
) -> float:
    if vol <= 0.0 or maturity <= 0.0:
        return max(0.0, (spot - strike) if side == "call" else (strike - spot))
    if side == "call":
        return american_call(spot, strike, rate, carry, maturity, vol, min_total_vol)
    return american_call(strike, spot, rate - carry, -carry, maturity, vol, min_total_vol)

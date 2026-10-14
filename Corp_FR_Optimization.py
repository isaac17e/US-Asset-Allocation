#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 PIPELINE DE SCREENING, RANKING, BENCHMARK CREDITICIO Y SELECCIÓN DE
 PORTAFOLIO DE RENTA FIJA CORPORATIVA (INVESTMENT GRADE, USD)
===============================================================================
"""

from __future__ import annotations

# =============================================================================
#  BLOQUE DE CONFIGURACIÓN
# =============================================================================
import os

try:  # claves desde .env (junto al script); sin dotenv se usa os.environ
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

# --- Claves y URLs de APIs ---------------------------------------------------
FMP_API_KEY = os.getenv("FMP_API_KEY", "")
FRED_API_KEY = os.getenv("FRED_API_KEY", "")
FMP_BASE_URL = "https://financialmodelingprep.com/stable"

# --- Endpoints FMP -----------------------------------------------------------
FMP_EP_SCREENER = "company-screener"
FMP_EP_INCOME = "income-statement"
FMP_EP_BALANCE = "balance-sheet-statement"
FMP_EP_CASHFLOW = "cash-flow-statement"

# --- Red y límites de peticiones ---------------------------------------------
REQUEST_TIMEOUT_SEC = 20          # timeout por petición HTTP
MAX_RETRIES = 4                   # reintentos ante 429 / 5xx / errores de red
MIN_SECONDS_BETWEEN_CALLS = 0.25  # ~240 llamadas/min (ajusta a tu plan de FMP)

# --- Curva libre de riesgo (FRED) --------------------------------------------
TREASURY_SERIES = {               # madurez en años -> serie CMT de FRED
    1 / 12: "DGS1MO",
    0.25: "DGS3MO",
    0.50: "DGS6MO",
    1.0: "DGS1",
    2.0: "DGS2",
    3.0: "DGS3",
    5.0: "DGS5",
    7.0: "DGS7",
    10.0: "DGS10",
    20.0: "DGS20",
    30.0: "DGS30",
}
FRED_LOOKBACK_DAYS = 20            # ventana para encontrar el último dato válido
CURVE_INTERP_METHOD = "pchip"      # "pchip" (sin oscilaciones), "cubic", "linear"
BENCHMARK_TENORS = [3.0, 5.0, 10.0]  # horizontes del Yield Target Overlay (años)

# --- Screening base (FMP) ----------------------------------------------------
MIN_MARKET_CAP_USD = 10_000_000_000
SCREENER_EXCHANGES = ["NYSE", "NASDAQ"]  # una llamada al screener por bolsa
SCREENER_COUNTRY = "US"                  # None para no filtrar por país
SCREENER_LIMIT = 1000                    # máx. resultados por llamada
MAX_CANDIDATES = 300                     # tope de emisores a analizar (costo API)
EXCLUDE_SECTORS = ["Financial Services"]  # EBITDA/deuda no aplican a bancos/aseg.

# --- Exclusión de notas, preferentes y deuda listada -------------------------
NON_COMMON_NAME_PATTERN = (
    r"\d+(?:\.\d+)?\s*%|\bseries\b|\bnotes?\b|\bnts\b|\bjr\b|\bjrsub\b|debenture|"
    r"collateral|preferred|\bpfd\b|depositary|subordinated|perpetual"
)
NON_COMMON_SYMBOL_PATTERN = r"-P[A-Z]?$"  # preferentes: CTA-PA, CTA-PB…

# --- Apalancamiento y cobertura ----------------------------------------------
FUNDAMENTALS_PERIOD = "annual"   # período de los estados financieros
DEBT_DEFINITION = "total"        # "total" (Total Debt) o "net" (Net Debt)
MAX_DEBT_TO_EBITDA = 3.0         # x
MIN_TOTAL_DEBT_USD = 2_000_000_000  # solo emisores con bonos en circulación
MIN_INTEREST_COVERAGE = 2.5      # x  (EBITDA / Interest Expense)
COVERAGE_CAP = 100.0             # tope de cobertura (evita outliers/infinitos)

# --- Gasto de intereses nulo o ausente ---------------------------------------
ZERO_INTEREST_POLICY = "impute"  # "impute" (deuda × tasa) | "cap" | "exclude"
IMPUTED_INTEREST_RATE = 0.055    # costo de deuda supuesto para la imputación
ZERO_INTEREST_DEBT_TOL = 0.25    # deuda <= tol × EBITDA se considera inmaterial (-> cap)

# --- Filtro de FCF -----------------------------------------------------------
FCF_HISTORY_YEARS = 5            # años de Cash Flow Statement a descargar (3-5)
FCF_CAGR_YEARS = 3               # ventana del CAGR (t vs t-3)
MIN_FCF_CAGR = 0.03              # 3.0 %
FCF_FILTER_LOGIC = "OR"          # "OR": creciente O CAGR>min | "AND": ambos

# --- Filtro de rating --------------------------------------------------------
INVESTMENT_GRADE_RATINGS = {
    "AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-",
}
MANUAL_RATING_OVERRIDES: dict[str, str] = {}  # ratings de agencia, ej. {"AAPL": "AA+"}
RATING_SELECTION: Optional[list[str]] = ["A+", "A"]  # Top N solo con estos ratings, ej. ["A+", "A"]; None = todos

# --- Rating sintético (peor entre cobertura y apalancamiento) ----------------
SYNTHETIC_COVERAGE_TABLE = [     # EBIT/Intereses (Damodaran): (umbral mín., rating)
    (8.50, "AAA"), (6.50, "AA"), (5.50, "A+"), (4.25, "A"), (3.00, "A-"),
    (2.50, "BBB"), (2.25, "BB+"), (2.00, "BB"), (1.75, "B+"), (1.50, "B"),
    (1.25, "B-"), (0.80, "CCC"), (0.65, "CC"), (0.20, "C"), (float("-inf"), "D"),
]
SYNTHETIC_LEVERAGE_TABLE = [     # Deuda/EBITDA (aprox. S&P): (umbral máx., rating)
    (0.50, "AAA"), (1.00, "AA"), (1.50, "A+"), (2.00, "A"), (2.50, "A-"),
    (3.00, "BBB+"), (3.50, "BBB"), (4.00, "BBB-"), (5.00, "BB"), (float("inf"), "B"),
]
SYNTHETIC_MAX_RATING = "AA"      # techo: casi ningún corporativo de EE.UU. es AAA

# --- Scoring y ranking -------------------------------------------------------
SCORE_WEIGHTS = {"coverage": 0.30, "debt": 0.25, "fcf": 0.25, "rating": 0.20}
ZSCORE_CLIP = 3.0                # winsoriza Z-scores a ±3 desviaciones
WINSORIZE_QUANTILES = (0.05, 0.95)  # winsoriza métricas crudas antes del Z-score (None = off)
LOG_TRANSFORM_COVERAGE = True    # True: usa ln(cobertura) (reduce asimetría)
NAN_CAGR_FILL = "min"            # CAGR no definido (FCF base <= 0): "min" o "zero"
TOP_N = 25

# --- Ponderación del portafolio ----------------------------------------------
SCORE_WEIGHT_METHOD = "shift"    # "shift": (score - min + floor) | "softmax"
SCORE_SHIFT_FLOOR = 0.25         # piso (en unidades de score) para el peor emisor
SOFTMAX_TEMPERATURE = 1.0
MAX_SINGLE_ISSUER_WEIGHT = 0.15  # tope por emisor (None para desactivar)
PORTFOLIO_NOTIONAL_USD = 10_000_000

# --- Yield Target Overlay (spreads) ------------------------------------------
MIN_SPREAD_BPS_BY_BUCKET = {"AAA": 40, "AA": 60, "A": 90, "BBB": 140}  # bps sobre el Tesoro
TENOR_PREMIUM_BPS = {3.0: 0, 5.0: 10, 10.0: 25}  # prima por plazo sobre el bucket
SCORE_SPREAD_ADJ_BPS_PER_UNIT = -5.0  # bps por unidad de score (0 = off)

# --- Refinitiv / ejecución ---------------------------------------------------
MIN_AMOUNT_OUTSTANDING_USD = 500_000_000   # liquidez mínima por emisión
TENOR_WINDOW_YEARS = 1.0                   # ± años alrededor de cada tenor

# --- Salidas -----------------------------------------------------------------
HTML_OUTPUT_PATH = "reporte_portafolio_renta_fija.html"
OPEN_HTML_IN_BROWSER = True
LOG_LEVEL = "INFO"
# =============================================================================
# ████  FIN DEL BLOQUE DE CONFIGURACIÓN  ████
# =============================================================================


import html
import logging
import math
import sys
import time
import webbrowser
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fredapi import Fred
from scipy.interpolate import CubicSpline, PchipInterpolator

import pipeline_io
from fmp_client import APIAuthorizationError, APIError
from fmp_client import FMPClient as _FMPTransport

logging.basicConfig(
    level=LOG_LEVEL.upper(),
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ig_pipeline")

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
pd.set_option("display.max_rows", 200)


# =============================================================================
# UTILIDADES
# =============================================================================
def _to_float(x: Any) -> float:
    """Convierte a float de forma segura; devuelve NaN si no es posible."""
    try:
        if x is None or x == "" or x == ".":
            return float("nan")
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def _banner(title: str, char: str = "=") -> None:
    line = char * 96
    print(f"\n{line}\n {title}\n{line}")


def _fmt_pct(x: float, d: int = 2) -> str:
    return "n/d" if pd.isna(x) else f"{x * 100:.{d}f}%"


RATING_SCALE = [
    "AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-",
    "BB+", "BB", "BB-", "B+", "B", "B-", "CCC", "CC", "C", "D",
]


def _rating_rank(rating: str) -> int:
    """Posición en la escala (0 = AAA). Mayor = peor."""
    return RATING_SCALE.index(rating)


def synthetic_rating(ebit_coverage: float, debt_to_ebitda: float) -> Optional[str]:
    """Peor entre el rating por cobertura EBIT/Int y el rating por Deuda/EBITDA."""
    if math.isnan(ebit_coverage) or math.isnan(debt_to_ebitda):
        return None
    by_cov = next(r for floor, r in SYNTHETIC_COVERAGE_TABLE if ebit_coverage >= floor)
    by_lev = next(r for cap, r in SYNTHETIC_LEVERAGE_TABLE if debt_to_ebitda <= cap)
    worst = max(_rating_rank(by_cov), _rating_rank(by_lev), _rating_rank(SYNTHETIC_MAX_RATING))
    return RATING_SCALE[worst]


def rating_bucket(rating: Optional[str]) -> Optional[str]:
    """'AA-' -> 'AA', 'BBB+' -> 'BBB'. Devuelve None si no aplica."""
    if not rating:
        return None
    base = rating.strip().upper().rstrip("+-")
    return base if base in MIN_SPREAD_BPS_BY_BUCKET else None


# =============================================================================
# CLIENTE FMP (rate limiting, reintentos, caché y manejo de errores)
# =============================================================================
class FMPClient(_FMPTransport):
    """Cliente FMP tolerante: sobre el transporte compartido (fmp_client.py) devuelve None si la llamada falla."""

    def __init__(self, api_key: str, base_url: str = FMP_BASE_URL) -> None:
        super().__init__(api_key, base_url, MIN_SECONDS_BETWEEN_CALLS, REQUEST_TIMEOUT_SEC, MAX_RETRIES)
        self.n_failures = 0

    @staticmethod
    def _norm_params(params: dict) -> dict:
        """FMP espera booleanos en minúscula ('true'/'false') y sin Nones."""
        out = {}
        for k, v in params.items():
            if v is None:
                continue
            out[k] = str(v).lower() if isinstance(v, bool) else v
        return out

    def get(self, endpoint: str, **params: Any) -> Optional[Any]:
        """GET con caché, backoff exponencial ante 429/5xx y validación de JSON.

        Devuelve el JSON decodificado o None si la llamada falla definitivamente.
        """
        params = self._norm_params(params)
        try:
            data = self._get(endpoint, params)
        except APIAuthorizationError:
            log.error("FMP %s: API key inválida o endpoint fuera de tu plan.", endpoint)
            self.n_failures += 1
            return None
        except APIError as exc:
            log.warning("%s (%s)", exc, params)
            self.n_failures += 1
            return None
        if isinstance(data, dict) and "error" in data:
            log.warning("FMP %s: %s", endpoint, data["error"])
            self.n_failures += 1
            return None
        return data

    def get_records(self, endpoint: str, **params: Any) -> list[dict]:
        """Como get(), pero siempre devuelve una lista de diccionarios."""
        data = self.get(endpoint, **params)
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        if isinstance(data, dict):
            return [data]
        return []


# =============================================================================
# FASE 1 — CURVA LIBRE DE RIESGO (FRED)
# =============================================================================
@dataclass
class RiskFreeCurve:
    """Curva spot del Tesoro (CMT) con interpolación para cualquier madurez.

    Las tasas se almacenan en % (convención de FRED). `rate(t)` devuelve la
    tasa en decimal (0.0425 = 4.25%) para facilitar el cálculo de targets.
    """

    tenors: np.ndarray
    yields_pct: np.ndarray
    obs_dates: dict[float, str]
    method: str = "pchip"
    _f: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        order = np.argsort(self.tenors)
        self.tenors = np.asarray(self.tenors, dtype=float)[order]
        self.yields_pct = np.asarray(self.yields_pct, dtype=float)[order]
        if len(self.tenors) < 2:
            raise ValueError("Se requieren al menos 2 nodos para construir la curva.")
        m = self.method.lower()
        if m == "cubic" and len(self.tenors) >= 4:
            self._f = CubicSpline(self.tenors, self.yields_pct, bc_type="natural")
        elif m == "pchip" and len(self.tenors) >= 3:
            self._f = PchipInterpolator(self.tenors, self.yields_pct)
        else:
            if m != "linear":
                log.warning("Pocos nodos para '%s'; se usa interpolación lineal.", m)
            self._f = lambda t: np.interp(t, self.tenors, self.yields_pct)

    def rate_pct(self, t: float) -> float:
        """Rf en % para la madurez t (años). Fuera de rango: extrapolación plana."""
        t_c = float(np.clip(t, self.tenors.min(), self.tenors.max()))
        return float(self._f(t_c))

    def rate(self, t: float) -> float:
        """Rf en decimal para la madurez t (años)."""
        return self.rate_pct(t) / 100.0

    @property
    def as_of(self) -> str:
        return max(self.obs_dates.values()) if self.obs_dates else "n/d"


def build_risk_free_curve() -> RiskFreeCurve:
    """Descarga el último dato de cada nodo CMT y construye la curva."""
    start = (date.today() - timedelta(days=FRED_LOOKBACK_DAYS)).isoformat()
    fred = Fred(api_key=FRED_API_KEY)

    tenors, ylds, dates = [], [], {}
    for tenor, sid in TREASURY_SERIES.items():
        try:
            obs = fred.get_series(sid, observation_start=start).dropna()
        except Exception as exc:  # fredapi lanza ValueError genéricos
            log.warning("FRED %s: %s", sid, exc)
            obs = pd.Series(dtype=float)
        if obs.empty:
            log.warning("FRED %s sin dato válido en los últimos %d días; nodo omitido.",
                        sid, FRED_LOOKBACK_DAYS)
            continue
        tenors.append(tenor)
        ylds.append(float(obs.iloc[-1]))
        dates[tenor] = obs.index[-1].strftime("%Y-%m-%d")

    if len(tenors) < 3:
        raise RuntimeError("Curva libre de riesgo insuficiente (<3 nodos). Revisa FRED_API_KEY.")
    if len(set(dates.values())) > 1:
        log.warning("Los nodos de la curva tienen fechas distintas: %s", sorted(set(dates.values())))
    return RiskFreeCurve(np.array(tenors), np.array(ylds), dates, CURVE_INTERP_METHOD)


# =============================================================================
# FASE 2 — SCREENING BASE Y SOLVENCIA
# =============================================================================
def stage_screener(fmp: FMPClient) -> pd.DataFrame:
    """Universo base: Large Caps activas (sin ETFs/fondos) en las bolsas elegidas."""
    rows: list[dict] = []
    for exch in SCREENER_EXCHANGES:
        recs = fmp.get_records(
            FMP_EP_SCREENER,
            marketCapMoreThan=int(MIN_MARKET_CAP_USD),
            isActivelyTrading=True, isEtf=False, isFund=False,
            exchange=exch, country=SCREENER_COUNTRY, limit=SCREENER_LIMIT,
        )
        log.info("Screener %s: %d registros", exch, len(recs))
        rows.extend(recs)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df["marketCap"] = pd.to_numeric(df.get("marketCap"), errors="coerce")
    df = df[df["marketCap"] >= MIN_MARKET_CAP_USD]  # doble verificación local
    if "isActivelyTrading" in df:
        df = df[df["isActivelyTrading"].astype(str).str.lower().isin(["true", "1"])]
    for col in ("isEtf", "isFund"):
        if col in df:
            df = df[~df[col].astype(str).str.lower().isin(["true", "1"])]
    if EXCLUDE_SECTORS and "sector" in df:
        df = df[~df["sector"].isin(EXCLUDE_SECTORS)]

    names = df["companyName"].fillna("").astype(str)
    non_common = (names.str.contains(NON_COMMON_NAME_PATTERN, case=False, regex=True)
                  | df["symbol"].astype(str).str.contains(NON_COMMON_SYMBOL_PATTERN, regex=True))
    if non_common.any():
        log.info("Screener: %d emisiones no comunes excluidas (notas/preferentes): %s",
                 int(non_common.sum()), ", ".join(df.loc[non_common, "symbol"].astype(str)))
    df = df[~non_common]

    keep = [c for c in ("symbol", "companyName", "marketCap", "sector", "industry",
                        "exchangeShortName", "country", "avgVolume") if c in df.columns]
    df = df[keep].dropna(subset=["symbol"]).drop_duplicates("symbol")
    # Varias listas del mismo emisor (FOXA/FOX, SO/SOMN, MKC/MKC-V…): se conserva la de mayor
    # volumen promedio, que es la acción común; las demás son clases o híbridos poco líquidos.
    if "avgVolume" in df:
        df = df.sort_values("avgVolume", ascending=False, key=lambda v: pd.to_numeric(v, errors="coerce"))
    issuer_key = (df["companyName"].fillna("").astype(str).str.lower()
                  .str.replace(r"\bclass [a-z]\b|\(the\)|\bthe\b|[^a-z0-9 ]", " ", regex=True)
                  .str.split().str.join(" "))
    dup = issuer_key.duplicated(keep="first")
    if dup.any():
        log.info("Screener: %d clases de acciones duplicadas excluidas: %s",
                 int(dup.sum()), ", ".join(df.loc[dup, "symbol"].astype(str)))
    df = (df[~dup].drop(columns="avgVolume", errors="ignore")
          .sort_values("marketCap", ascending=False).head(MAX_CANDIDATES).reset_index(drop=True))
    return df


def _latest(records: list[dict]) -> Optional[dict]:
    """Último registro por fecha (FMP suele entregarlos del más reciente al más antiguo)."""
    if not records:
        return None
    return max(records, key=lambda r: str(r.get("date", "")))


def stage_solvency(fmp: FMPClient, universe: pd.DataFrame) -> pd.DataFrame:
    """Calcula Debt/EBITDA y EBITDA/Interest del último año fiscal y filtra."""
    out = []
    n = len(universe)
    for i, row in enumerate(universe.itertuples(index=False), start=1):
        sym = row.symbol
        if i % 25 == 0 or i == n:
            log.info("Solvencia: %d/%d", i, n)
        inc = _latest(fmp.get_records(FMP_EP_INCOME, symbol=sym, period=FUNDAMENTALS_PERIOD, limit=1))
        bal = _latest(fmp.get_records(FMP_EP_BALANCE, symbol=sym, period=FUNDAMENTALS_PERIOD, limit=1))
        if not inc or not bal:
            continue

        # EBIT = operatingIncome: el campo "ebit" de FMP a veces viene en 0 (p. ej. MU)
        ebit = _to_float(inc.get("operatingIncome"))
        if math.isnan(ebit) or ebit == 0:
            ebit = _to_float(inc.get("ebit"))
        ebitda = _to_float(inc.get("ebitda"))
        if math.isnan(ebitda):  # respaldo: EBIT + D&A
            ebitda = ebit + _to_float(inc.get("depreciationAndAmortization"))
        interest = abs(_to_float(inc.get("interestExpense")))
        gross_debt = _to_float(bal.get("totalDebt"))
        debt = _to_float(bal.get("netDebt" if DEBT_DEFINITION == "net" else "totalDebt"))
        if math.isnan(debt) and DEBT_DEFINITION == "net":
            debt = _to_float(bal.get("totalDebt")) - _to_float(bal.get("cashAndCashEquivalents"))

        if math.isnan(ebitda) or ebitda <= 0 or math.isnan(debt):
            continue  # EBITDA negativo/nulo: apalancamiento no interpretable

        interest_imputed = False
        if math.isnan(interest) or interest == 0:
            material_debt = debt > ZERO_INTEREST_DEBT_TOL * ebitda
            if ZERO_INTEREST_POLICY == "exclude":
                continue
            if ZERO_INTEREST_POLICY == "impute" and material_debt:
                interest, interest_imputed = debt * IMPUTED_INTEREST_RATE, True
        if math.isnan(interest) or interest == 0:
            coverage, ebit_coverage = COVERAGE_CAP, COVERAGE_CAP
        else:
            coverage = min(ebitda / interest, COVERAGE_CAP)
            ebit_coverage = min(ebit / interest, COVERAGE_CAP) if not math.isnan(ebit) else float("nan")
        debt_ebitda = max(debt, 0.0) / ebitda

        out.append({
            **row._asdict(),
            "fiscalDate": inc.get("date"),
            "ebit": ebit, "ebitda": ebitda, "interestExpense": interest,
            "interestImputed": interest_imputed, "debt": debt, "grossDebt": gross_debt,
            "debtToEbitda": debt_ebitda, "interestCoverage": coverage,
            "ebitCoverage": ebit_coverage,
        })

    df = pd.DataFrame(out)
    if df.empty:
        return df
    mask = (df["debtToEbitda"] <= MAX_DEBT_TO_EBITDA) & (df["interestCoverage"] >= MIN_INTEREST_COVERAGE)
    return df[mask].reset_index(drop=True)


# =============================================================================
# FASE 3 — TENDENCIA DEL FREE CASH FLOW
# =============================================================================
def fcf_metrics(fcf: list[float], years: int = FCF_CAGR_YEARS) -> tuple[float, bool]:
    """Devuelve (CAGR_FCF, estrictamente_creciente) sobre la ventana `years`.

    `fcf` debe venir en orden cronológico ascendente. El CAGR solo está definido
    si FCF_{t-n} > 0 y FCF_t > 0; en caso contrario es NaN.
    """
    window = fcf[-(years + 1):]
    if len(window) < years + 1 or np.isnan(window).any():
        return float("nan"), False
    increasing = bool((np.diff(window) > 0).all())
    base, last = window[0], window[-1]
    cagr = (last / base) ** (1.0 / years) - 1.0 if (base > 0 and last > 0) else float("nan")
    return cagr, increasing


def stage_fcf(fmp: FMPClient, df: pd.DataFrame) -> pd.DataFrame:
    """Calcula CAGR del FCF y la condición de crecimiento estricto; filtra."""
    rows = []
    for i, row in enumerate(df.itertuples(index=False), start=1):
        if i % 25 == 0 or i == len(df):
            log.info("FCF: %d/%d", i, len(df))
        recs = fmp.get_records(FMP_EP_CASHFLOW, symbol=row.symbol,
                               period=FUNDAMENTALS_PERIOD, limit=FCF_HISTORY_YEARS)
        cf = pd.DataFrame(recs, columns=["date", "freeCashFlow", "operatingCashFlow", "capitalExpenditure"])
        cf = cf.sort_values("date").drop(columns="date").apply(pd.to_numeric, errors="coerce")  # ascendente
        # respaldo: CFO + CapEx (CapEx viene negativo en FMP)
        series = cf["freeCashFlow"].fillna(cf["operatingCashFlow"] + cf["capitalExpenditure"]).tolist()
        cagr, inc = fcf_metrics(series)
        rows.append({**row._asdict(), "fcfCAGR": cagr, "fcfIncreasing": inc,
                     "fcfLatest": series[-1] if series else float("nan"),
                     "fcfHistory": series})

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    cagr_ok = out["fcfCAGR"].fillna(-np.inf) > MIN_FCF_CAGR
    mask = (out["fcfIncreasing"] & cagr_ok) if FCF_FILTER_LOGIC.upper() == "AND" else (out["fcfIncreasing"] | cagr_ok)
    return out[mask].reset_index(drop=True)


# =============================================================================
# FASE 4 — CALIFICACIÓN CREDITICIA (GRADO DE INVERSIÓN)
# =============================================================================
def stage_rating(df: pd.DataFrame) -> pd.DataFrame:
    """Asigna rating (override manual > sintético).

    Con los umbrales de solvencia actuales todo emisor ya es >= BBB-, así que no es
    una etapa del embudo; solo descarta (con aviso) si un override manual o umbrales
    más laxos dejan entrar a un emisor high yield.
    """
    ratings, sources = [], []
    for row in df.itertuples(index=False):
        if row.symbol in MANUAL_RATING_OVERRIDES:
            ratings.append(str(MANUAL_RATING_OVERRIDES[row.symbol]).strip().upper())
            sources.append("Agencia (manual)")
        else:
            ratings.append(synthetic_rating(row.ebitCoverage, row.debtToEbitda))
            sources.append("Sintético")

    df = df.copy()
    df["rating"] = ratings
    df["ratingSource"] = sources
    non_ig = ~df["rating"].isin(INVESTMENT_GRADE_RATINGS)
    if non_ig.any():
        log.warning("Excluidos por rating < BBB-: %s",
                    ", ".join(f"{s} ({r})" for s, r in zip(df.loc[non_ig, "symbol"], df.loc[non_ig, "rating"])))
    df = df[~non_ig].copy()
    df["ratingBucket"] = df["rating"].map(rating_bucket)
    return df.reset_index(drop=True)


# =============================================================================
# FASE 5 — Z-SCORES Y COMPOSITE CREDIT SCORE
# =============================================================================
def zscore(s: pd.Series) -> pd.Series:
    """Winsoriza la métrica cruda por cuantiles, estandariza y recorta a ±ZSCORE_CLIP."""
    s = pd.to_numeric(s, errors="coerce")
    if WINSORIZE_QUANTILES is not None and s.notna().sum() >= 3:
        lo, hi = s.quantile(WINSORIZE_QUANTILES[0]), s.quantile(WINSORIZE_QUANTILES[1])
        s = s.clip(lo, hi)
    mu, sd = s.mean(), s.std(ddof=1)
    if pd.isna(sd) or sd == 0:
        return pd.Series(0.0, index=s.index)
    return ((s - mu) / sd).clip(-ZSCORE_CLIP, ZSCORE_CLIP)


def stage_scoring(df: pd.DataFrame) -> pd.DataFrame:
    """Composite = Σ peso·Z (cobertura, deuda invertida, CAGR FCF, rating); ranking."""
    df = df.copy()
    cov = np.log(df["interestCoverage"]) if LOG_TRANSFORM_COVERAGE else df["interestCoverage"]

    cagr = df["fcfCAGR"].astype(float)
    if cagr.notna().any():  # CAGR no definido -> imputación conservadora
        fill = cagr.min() if NAN_CAGR_FILL == "min" else 0.0
    else:
        fill = 0.0
    df["fcfCAGR_used"] = cagr.fillna(fill)

    df["Z_Coverage"] = zscore(cov)
    df["Z_Debt"] = -1.0 * zscore(df["debtToEbitda"])
    df["Z_FCF"] = zscore(df["fcfCAGR_used"])
    # Rating por escalones (AAA = 0, AA+ = 1, …), invertido: mejor rating -> Z mayor
    df["Z_Rating"] = -1.0 * zscore(df["rating"].map(_rating_rank).astype(float))
    w = SCORE_WEIGHTS
    df["CompositeScore"] = (w["coverage"] * df["Z_Coverage"]
                            + w["debt"] * df["Z_Debt"]
                            + w["fcf"] * df["Z_FCF"]
                            + w["rating"] * df["Z_Rating"])
    df = df.sort_values("CompositeScore", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)
    return df


def _selected_ratings() -> list[str]:
    """RATING_SELECTION normalizado (mayúsculas, sin espacios ni duplicados)."""
    sel = [RATING_SELECTION] if isinstance(RATING_SELECTION, str) else RATING_SELECTION
    return list(dict.fromkeys(str(r).strip().upper() for r in sel or []))


def select_ratings(ranked: pd.DataFrame) -> pd.DataFrame:
    """Deja solo los ratings de RATING_SELECTION (Z-scores ya calculados sobre todo IG)."""
    sel = _selected_ratings()
    unknown = [r for r in sel if r not in INVESTMENT_GRADE_RATINGS]
    if unknown:
        log.warning("RATING_SELECTION contiene ratings no IG o inválidos (se ignoran): %s",
                    ", ".join(unknown))
    df = ranked[ranked["rating"].isin(sel)].reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df


# =============================================================================
# FASE 6 — PONDERACIÓN Y BENCHMARK OVERLAY
# =============================================================================
def cap_weights(w: pd.Series, cap: Optional[float]) -> pd.Series:
    """Aplica un tope por emisor redistribuyendo el exceso proporcionalmente."""
    w = w / w.sum()
    if cap is None or cap * len(w) < 1.0:
        if cap is not None:
            log.warning("Tope %.1f%% inviable con N=%d; se ignora.", cap * 100, len(w))
        return w
    w = w.copy()
    for _ in range(100):
        over = w > cap + 1e-12
        if not over.any():
            break
        excess = (w[over] - cap).sum()
        w[over] = cap
        free = w < cap - 1e-12
        if not free.any():
            break
        w[free] += excess * w[free] / w[free].sum()
    return w / w.sum()


def stage_weights(top: pd.DataFrame) -> pd.DataFrame:
    """Equal Weight (1/N) y Credit-Score Weight (normalizado a 100%)."""
    top = top.copy()
    n = len(top)
    top["W_Equal"] = 1.0 / n
    s = top["CompositeScore"]
    if SCORE_WEIGHT_METHOD == "softmax":
        raw = np.exp((s - s.max()) / SOFTMAX_TEMPERATURE)
    else:  # "shift": desplaza para que todos los scores sean positivos
        raw = s - s.min() + SCORE_SHIFT_FLOOR
    top["W_Score"] = cap_weights(raw, MAX_SINGLE_ISSUER_WEIGHT).values
    top["USD_Equal"] = top["W_Equal"] * PORTFOLIO_NOTIONAL_USD
    top["USD_Score"] = top["W_Score"] * PORTFOLIO_NOTIONAL_USD
    return top


def stage_overlay(top: pd.DataFrame, curve: RiskFreeCurve) -> pd.DataFrame:
    """Yield Target mínimo = Rf(t) + spread(bucket) + prima(plazo) + ajuste(score)."""
    rows = []
    for r in top.itertuples(index=False):
        base_bps = MIN_SPREAD_BPS_BY_BUCKET.get(r.ratingBucket, max(MIN_SPREAD_BPS_BY_BUCKET.values()))
        adj_bps = SCORE_SPREAD_ADJ_BPS_PER_UNIT * r.CompositeScore
        for t in BENCHMARK_TENORS:
            spread_bps = max(base_bps + TENOR_PREMIUM_BPS.get(t, 0) + adj_bps, 0.0)
            rf = curve.rate(t)
            rows.append({
                "symbol": r.symbol, "rating": r.rating, "tenor": t,
                "Rf": rf, "MinSpread_bps": spread_bps,
                "YieldTarget": rf + spread_bps / 10_000,
            })
    return pd.DataFrame(rows)


def portfolio_summary(top: pd.DataFrame, overlay: pd.DataFrame) -> pd.DataFrame:
    """Métricas agregadas por esquema de ponderación."""
    res = {}
    for scheme, col in (("Equal Weight", "W_Equal"), ("Credit-Score Weight", "W_Score")):
        w = top.set_index("symbol")[col]
        hhi = float((w ** 2).sum())
        d = {
            "Composite Score (pond.)": float((top[col] * top["CompositeScore"]).sum()),
            "Cobertura EBITDA/Int (x)": float((top[col] * top["interestCoverage"]).sum()),
            "Deuda/EBITDA (x)": float((top[col] * top["debtToEbitda"]).sum()),
            "CAGR FCF": float((top[col] * top["fcfCAGR_used"]).sum()),
            "Peso máximo": float(w.max()),
            "N efectivo (1/HHI)": 1.0 / hhi if hhi > 0 else float("nan"),
        }
        for t in BENCHMARK_TENORS:
            sub = overlay[overlay["tenor"] == t].set_index("symbol")
            d[f"Yield Target {t:g}Y"] = float((w * sub["YieldTarget"].reindex(w.index)).sum())
        res[scheme] = d
    return pd.DataFrame(res)


# =============================================================================
# SALIDAS: CONSOLA
# =============================================================================
def print_curve(curve: RiskFreeCurve) -> None:
    _banner(f"FASE 1 · CURVA LIBRE DE RIESGO (UST CMT) — fecha {curve.as_of} — interp. {curve.method}")
    tbl = pd.DataFrame({
        "Tenor (años)": curve.tenors,
        "Serie": [TREASURY_SERIES[t] for t in curve.tenors],
        "Yield %": curve.yields_pct,
        "Fecha": [curve.obs_dates[t] for t in curve.tenors],
    })
    print(tbl.to_string(index=False, float_format=lambda x: f"{x:,.4g}"))
    print("\nRf interpolada en tenores benchmark: " +
          " | ".join(f"{t:g}Y = {curve.rate_pct(t):.3f}%" for t in BENCHMARK_TENORS))
    s2, s10 = curve.rate_pct(2), curve.rate_pct(10)
    print(f"Pendiente 2s10s: {(s10 - s2) * 100:+.1f} pb")


def print_funnel(funnel: list[tuple[str, int]]) -> None:
    _banner("EMBUDO DE SCREENING")
    base = funnel[0][1] or 1
    for name, n in funnel:
        bar = "█" * int(40 * n / base)
        print(f"  {name:<42} {n:>5}  {bar}")


def print_ranking(top: pd.DataFrame) -> None:
    _banner(f"FASE 5 · RANKING — TOP {len(top)} POR COMPOSITE CREDIT SCORE")
    view = pd.DataFrame({
        "#": top["Rank"], "Ticker": top["symbol"],
        "Emisor": top["companyName"].astype(str).str.slice(0, 28),
        "Sector": top.get("sector", pd.Series("", index=top.index)).astype(str).str.slice(0, 20),
        "Rating": top["rating"],
        "Cob.(x)": top["interestCoverage"].round(1).astype(str) + top["interestImputed"].map({True: "*", False: ""}),
        "EBIT/Int": top["ebitCoverage"].round(1),
        "D/EBITDA": top["debtToEbitda"].round(2),
        "CAGR FCF": top["fcfCAGR"].map(_fmt_pct),
        "FCF↑": top["fcfIncreasing"].map({True: "Sí", False: "No"}),
        "Z_Cov": top["Z_Coverage"].round(2), "Z_Debt": top["Z_Debt"].round(2),
        "Z_FCF": top["Z_FCF"].round(2), "Z_Rtg": top["Z_Rating"].round(2),
        "Score": top["CompositeScore"].round(3),
    })
    print(view.to_string(index=False))
    if top["interestImputed"].any():
        print(f"\n*  Gasto de intereses reportado = 0 con deuda material: se imputó "
              f"deuda × {IMPUTED_INTEREST_RATE:.1%}.")
    if (top["ratingSource"] == "Sintético").any():
        print("\n⚠  Rating SINTÉTICO = peor entre cobertura EBIT/Int (Damodaran) y Deuda/EBITDA, "
              f"con techo {SYNTHETIC_MAX_RATING}. No es calificación de agencia: valida en Refinitiv.")


def print_weights(top: pd.DataFrame, summary: pd.DataFrame) -> None:
    _banner(f"FASE 6 · PONDERACIÓN (Nocional USD {PORTFOLIO_NOTIONAL_USD:,.0f})")
    view = pd.DataFrame({
        "Ticker": top["symbol"], "Rating": top["rating"],
        "Score": top["CompositeScore"].round(3),
        "EW %": (top["W_Equal"] * 100).round(2),
        "EW USD": top["USD_Equal"].map(lambda x: f"{x:,.0f}"),
        "CSW %": (top["W_Score"] * 100).round(2),
        "CSW USD": top["USD_Score"].map(lambda x: f"{x:,.0f}"),
    })
    print(view.to_string(index=False))
    print(f"\nMétodo CSW: '{SCORE_WEIGHT_METHOD}' | tope por emisor: "
          f"{'n/a' if MAX_SINGLE_ISSUER_WEIGHT is None else f'{MAX_SINGLE_ISSUER_WEIGHT:.0%}'}")

    _banner("MÉTRICAS DEL PORTAFOLIO", "-")
    is_pct = summary.index.str.contains("CAGR|Peso|Yield")
    fmt = summary.astype(object)
    fmt[is_pct] = summary[is_pct].map(_fmt_pct)
    fmt[~is_pct] = summary[~is_pct].map("{:,.2f}".format)
    print(fmt.to_string())


def _overlay_pivot(overlay: pd.DataFrame, col: str) -> pd.DataFrame:
    """Emisor × tenor para una columna del overlay, en el orden del ranking."""
    return overlay.pivot_table(index="symbol", columns="tenor", values=col, sort=False)


def print_overlay(overlay: pd.DataFrame) -> None:
    _banner("FASE 6 · BENCHMARK OVERLAY — YIELD TARGET MÍNIMO POR EMISOR")
    rf, sp, yt = (_overlay_pivot(overlay, c) for c in ("Rf", "MinSpread_bps", "YieldTarget"))
    view = pd.DataFrame(index=yt.index)
    view.insert(0, "Rating", overlay.drop_duplicates("symbol").set_index("symbol")["rating"])
    for t in BENCHMARK_TENORS:
        view[f"Rf {t:g}Y"] = rf[t].map(_fmt_pct)
        view[f"Spr {t:g}Y (pb)"] = sp[t].round(0).astype(int)
        view[f"Target {t:g}Y"] = yt[t].map(_fmt_pct)
    print(view.to_string())
    print("\nRegla: comprar solo bonos con YTM (o YTW si son callables) >= Target y "
          "OAS >= Spread mínimo del tenor más cercano a su duración.")


def print_refinitiv_instructions(top: pd.DataFrame, overlay: pd.DataFrame) -> None:
    _banner("INSTRUCCIONES PARA EL ANALISTA — EXTRACCIÓN EN REFINITIV WORKSPACE")
    tenors = ", ".join(f"{t:g}Y (±{TENOR_WINDOW_YEARS:g})" for t in BENCHMARK_TENORS)
    print(f"""
 1) BÚSQUEDA DE EMISIONES (app de búsqueda de bonos / Fixed Income Screener):
    • Emisor: ticker o "Ultimate Parent" de cada nombre de la lista (incluye
      subsidiarias financieras que emitan con garantía de la matriz).
    • Moneda: USD | Tipo: Corporate, Senior Unsecured (evita subordinados/híbridos).
    • Madurez objetivo: {tenors}.
    • Amount Outstanding >= USD {MIN_AMOUNT_OUTSTANDING_USD:,.0f} (liquidez).
    • Excluye: convertibles, bonos en default, emisiones privadas 144A sin
      registro si tu mandato no las permite.

 2) CAMPOS A EXTRAER POR EMISIÓN (usa el Data Item Browser para el código exacto):
    • Identificadores: ISIN, CUSIP, RIC.
    • Condiciones: cupón, frecuencia, fecha de vencimiento, calendario de call
      (make-whole / par call), seniority.
    • Mercado: precio Bid/Ask, YTM y Yield-to-Worst (bid).
    • Spreads: OAS vs curva del Tesoro, G-Spread, Z-Spread.
    • Riesgo: Modified Duration (y Effective Duration si es callable), Convexity.
    • Tamaño/liquidez: Amount Outstanding, fecha de emisión, número de dealers.
    • Rating de agencias: S&P, Moody's y Fitch (reemplaza el rating sintético en
      MANUAL_RATING_OVERRIDES y vuelve a correr el pipeline).

 3) CRITERIO DE COMPRA POR BONO:
    • Asigna cada bono al tenor benchmark más cercano a su Modified Duration.
    • Compra si YTW >= Yield Target y OAS >= Spread mínimo (tabla anterior).
    • Si hay varias emisiones elegibles del mismo emisor, prioriza la de mayor
      OAS por unidad de duración (OAS / ModDur) y mayor monto en circulación.
    • Respeta el monto USD del esquema de pesos elegido (EW o CSW).
""")
    print(" CHECKLIST POR EMISOR")
    print(" " + "-" * 94)
    yt, sp = _overlay_pivot(overlay, "YieldTarget"), _overlay_pivot(overlay, "MinSpread_bps")
    for r in top.itertuples(index=False):
        targets = " | ".join(f"{t:g}Y: YTW≥{yt.loc[r.symbol, t] * 100:.2f}% OAS≥{sp.loc[r.symbol, t]:.0f}pb"
                             for t in BENCHMARK_TENORS)
        print(f" [ ] {r.symbol:<6} {str(r.companyName)[:30]:<30} {r.rating:<5} "
              f"CSW USD {r.USD_Score:>12,.0f}\n       {targets}")


# =============================================================================
# SALIDAS: HTML INTERACTIVO
# =============================================================================
def _figure(traces: list, height: int = 380, **layout: Any) -> go.Figure:
    """Figura con el estilo común del reporte (plantilla, márgenes y leyenda horizontal)."""
    layout = {"margin": {"l": 55, "r": 20, "t": 10, "b": 50}, "legend": {"orientation": "h", "y": -0.2}, **layout}
    return go.Figure(traces, layout=go.Layout(template="plotly_white", height=height, **layout))


def build_html_report(curve: RiskFreeCurve, funnel: list[tuple[str, int]],
                      top: pd.DataFrame, overlay: pd.DataFrame,
                      summary: pd.DataFrame, fmp_calls: int) -> Path:
    """Genera un único HTML con los gráficos (Plotly; plotly.js vía CDN) y las tablas."""
    grid = np.linspace(curve.tenors.min(), curve.tenors.max(), 300)
    syms = top["symbol"].tolist()
    yt = _overlay_pivot(overlay, "YieldTarget").reindex(syms)[BENCHMARK_TENORS]
    w = SCORE_WEIGHTS

    score_parts = [("Z_Coverage", "coverage", "Cobertura"), ("Z_Debt", "debt", "Deuda (inv.)"),
                   ("Z_FCF", "fcf", "FCF"), ("Z_Rating", "rating", "Rating")]
    figs = [
        _figure([
            go.Scatter(x=grid, y=[curve.rate_pct(t) for t in grid], mode="lines", name="Interpolada",
                       line_width=2.5),
            go.Scatter(x=curve.tenors, y=curve.yields_pct, text=[TREASURY_SERIES[t] for t in curve.tenors],
                       mode="markers", name="Nodos FRED", marker_size=8,
                       hovertemplate="%{text}<br>%{x:.2f}a: %{y:.3f}%<extra></extra>"),
            go.Scatter(x=BENCHMARK_TENORS, y=[curve.rate_pct(t) for t in BENCHMARK_TENORS], mode="markers",
                       name="Benchmark", marker={"size": 12, "symbol": "diamond"},
                       hovertemplate="Rf %{x}Y: %{y:.3f}%<extra></extra>"),
        ], xaxis_title="Madurez (años)", yaxis_title="Yield (%)"),
        _figure([go.Funnel(y=[f[0] for f in funnel], x=[f[1] for f in funnel], textinfo="value+percent initial")],
                margin={"l": 220, "r": 20, "t": 10, "b": 30}),
        _figure([go.Bar(x=syms, y=top[col] * w[key], name=f"{w[key]:.2f}·Z {label}") for col, key, label in score_parts]
                + [go.Scatter(x=syms, y=top["CompositeScore"], mode="markers", name="Composite",
                              marker={"size": 11, "symbol": "line-ew-open", "line_width": 3},
                              text=top["companyName"].astype(str),
                              hovertemplate="%{text}<br>Score %{y:.3f}<extra></extra>")],
                barmode="relative", yaxis_title="Contribución (Z)"),
        _figure([go.Scatter(x=top["debtToEbitda"], y=top["interestCoverage"], text=syms,
                            mode="markers+text", textposition="top center", customdata=top["rating"],
                            marker={"size": np.maximum(8, np.sqrt(top["marketCap"] / 1e9) * 2.2),
                                    "color": top["CompositeScore"], "colorscale": "Viridis",
                                    "showscale": True, "colorbar": {"title": "Score"}, "opacity": 0.8},
                            hovertemplate="%{text} (%{customdata})<br>D/EBITDA %{x:.2f}x"
                                          "<br>Cobertura %{y:.1f}x<extra></extra>")],
                xaxis_title="Deuda / EBITDA (x)", yaxis={"title": "EBITDA / Intereses (x)", "type": "log"}),
        _figure([go.Bar(x=syms, y=top["W_Equal"] * 100, name="Equal Weight"),
                 go.Bar(x=syms, y=top["W_Score"] * 100, name="Credit-Score Weight")],
                barmode="group", yaxis_title="Peso (%)"),
        _figure([go.Heatmap(x=syms, y=[f"{t:g}Y" for t in BENCHMARK_TENORS], z=(yt * 100).T.to_numpy(),
                            colorscale="Blues", texttemplate="%{z:.2f}", colorbar={"title": "%"},
                            hovertemplate="%{x} · %{y}<br>Target %{z:.3f}%<extra></extra>")],
                height=320, margin={"l": 50, "r": 20, "t": 10, "b": 40}),
    ]
    # plotly.js se incluye una sola vez (vía CDN) en el primer gráfico del documento
    plots = [f.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False,
                       config={"displaylogo": False, "responsive": True}) for i, f in enumerate(figs)]

    summ_html = summary.map(lambda v: f"{v:,.4f}" if isinstance(v, (float, int)) else v).to_html(
        classes="tbl", border=0)
    tbl = top[["Rank", "symbol", "companyName", "rating", "ratingSource", "interestCoverage",
               "debtToEbitda", "fcfCAGR", "CompositeScore", "W_Equal", "W_Score"]].copy()
    tbl["fcfCAGR"] = tbl["fcfCAGR"].map(_fmt_pct)
    tbl["W_Equal"] = tbl["W_Equal"].map(lambda x: f"{x:.2%}")
    tbl["W_Score"] = tbl["W_Score"].map(lambda x: f"{x:.2%}")
    tbl_html = tbl.to_html(classes="tbl", border=0, index=False, float_format=lambda x: f"{x:,.2f}")

    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    doc = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Portafolio IG Renta Fija</title>
<style>
:root {{ --bg:#f6f7f9; --card:#ffffff; --ink:#1b2430; --muted:#5b6675; --line:#e3e6eb; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
       font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
header {{ padding:28px 16px 8px; max-width:1200px; margin:0 auto; }}
h1 {{ margin:0 0 4px; font-size:22px; }} .sub {{ color:var(--muted); }}
main {{ max-width:1200px; margin:0 auto; padding:8px 16px 40px;
       display:grid; grid-template-columns:repeat(auto-fit,minmax(520px,1fr)); gap:16px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px; min-width:0; }}
.card.wide {{ grid-column:1/-1; }} .card h2 {{ margin:0 0 6px; font-size:15px; }}
.note {{ color:var(--muted); font-size:12px; margin:4px 0 0; }}
.tblwrap {{ overflow-x:auto; }}
table.tbl {{ border-collapse:collapse; width:100%; font-size:12.5px; }}
table.tbl th, table.tbl td {{ padding:6px 8px; border-bottom:1px solid var(--line); text-align:right; white-space:nowrap; }}
table.tbl th:first-child, table.tbl td:first-child {{ text-align:left; }}
@media (max-width:600px) {{ main {{ grid-template-columns:1fr; }} }}
</style></head><body>
<header>
  <h1>Portafolio de Renta Fija Corporativa — Investment Grade</h1>
  <div class="sub">Curva UST al {html.escape(curve.as_of)} · Top {len(top)} emisores ·
  generado {generated} · {fmp_calls} llamadas a FMP</div>
</header>
<main>
  <section class="card"><h2>Curva libre de riesgo (UST CMT)</h2>{plots[0]}
    <p class="note">Nodos FRED e interpolación {html.escape(curve.method)}; diamantes = tenores benchmark.</p></section>
  <section class="card"><h2>Embudo de screening</h2>{plots[1]}</section>
  <section class="card wide"><h2>Composite Credit Score y contribución de Z-scores</h2>{plots[2]}</section>
  <section class="card"><h2>Cobertura vs. apalancamiento</h2>{plots[3]}
    <p class="note">Tamaño = market cap (USD bn); color = Composite Score.</p></section>
  <section class="card"><h2>Pesos: Equal vs. Credit-Score</h2>{plots[4]}</section>
  <section class="card wide"><h2>Yield Target mínimo por emisor y tenor (%)</h2>{plots[5]}</section>
  <section class="card wide"><h2>Emisores seleccionados</h2><div class="tblwrap">{tbl_html}</div>
    <p class="note">Si la fuente es "Sintético", el rating es el peor entre cobertura EBIT/Intereses (tabla Damodaran) y Deuda/EBITDA, con techo {html.escape(SYNTHETIC_MAX_RATING)}; no es de agencia.</p></section>
  <section class="card wide"><h2>Métricas del portafolio</h2><div class="tblwrap">{summ_html}</div></section>
</main>
<script>window.dispatchEvent(new Event('resize'));</script>  <!-- re-mide los gráficos con la página completa -->
</body></html>"""

    path = Path(HTML_OUTPUT_PATH).resolve()
    path.write_text(doc, encoding="utf-8")
    return path


# =============================================================================
# ORQUESTACIÓN
# =============================================================================
def _check_keys() -> None:
    missing = [n for n, k in (("FMP_API_KEY", FMP_API_KEY), ("FRED_API_KEY", FRED_API_KEY))
               if not k.strip()]
    if missing:
        log.error("Faltan API keys: %s. Agrégalas al archivo .env (o como variables de entorno).",
                  ", ".join(missing))
        sys.exit(1)
    if abs(sum(SCORE_WEIGHTS.values()) - 1.0) > 1e-9:
        log.warning("SCORE_WEIGHTS no suman 1.0 (suman %.3f).", sum(SCORE_WEIGHTS.values()))


def _abort_if_empty(df: pd.DataFrame, stage: str, funnel: list) -> None:
    if df is None or df.empty:
        print_funnel(funnel)
        log.error("El universo quedó vacío en la fase '%s'. Relaja los parámetros o revisa tu plan de FMP.", stage)
        sys.exit(2)


def export_universe_json(top: pd.DataFrame) -> None:
    """Contrato v1: corp_fr_latest.json y una copia con marca de tiempo. Nunca aborta la corrida."""
    try:
        moment = pipeline_io.now_bogota()
        cols = {"symbol": "ticker", "Rank": "rank", "companyName": "name", "sector": "sector",
                "CompositeScore": "score"}
        df = top.reindex(columns=list(cols)).rename(columns=cols)
        df["ticker"] = df["ticker"].astype(str).str.strip()
        df = df[~df["ticker"].str.lower().isin(["", "nan"])]
        df[["name", "sector"]] = df[["name", "sector"]].fillna("").astype(str)
        df["score"] = df["score"].where(np.isfinite(df["score"]))  # NaN/inf -> null
        payload = {
            "schema_version": 1,
            "source_repo": "US-Asset-Allocation",
            "source": "Corp_FR_Optimization",
            "run_ts": pipeline_io.iso_bogota(moment),
            "tickers": df["ticker"].tolist(),
            "details": df.astype(object).where(df.notna(), None).to_dict("records"),
        }
        out_dir = os.getenv("UNIVERSE_OUT_DIR", "/workspace/pipeline/universe")
        written = pipeline_io.write_json_files(
            out_dir,
            ["corp_fr_latest.json", f"corp_fr_{pipeline_io.stamp_bogota(moment)}.json"],
            payload,
        )
        if written:
            log.info("Universo JSON: %s", ", ".join(written))
    except Exception as exc:
        print(f"WARNING: no se pudo exportar el JSON del pipeline: {exc}", file=sys.stderr)


def run_pipeline() -> None:
    t0 = time.time()
    _check_keys()
    fmp = FMPClient(FMP_API_KEY)
    funnel: list[tuple[str, int]] = []

    # --- Fase 1: curva libre de riesgo ---------------------------------------
    log.info("Fase 1: construyendo curva libre de riesgo desde FRED…")
    curve = build_risk_free_curve()
    print_curve(curve)

    # --- Fase 2: screening base + solvencia ----------------------------------
    log.info("Fase 2: screener FMP (Market Cap >= %.0f bn)…", MIN_MARKET_CAP_USD / 1e9)
    universe = stage_screener(fmp)
    funnel.append((f"Large caps activas (≥ USD {MIN_MARKET_CAP_USD / 1e9:.0f} bn)", len(universe)))
    _abort_if_empty(universe, "screener", funnel)

    solvent = stage_solvency(fmp, universe)
    funnel.append((f"D/EBITDA ≤ {MAX_DEBT_TO_EBITDA}x y Cobertura ≥ {MIN_INTEREST_COVERAGE}x", len(solvent)))
    _abort_if_empty(solvent, "solvencia", funnel)

    solvent = solvent[solvent["grossDebt"] >= MIN_TOTAL_DEBT_USD].reset_index(drop=True)
    funnel.append((f"Deuda total ≥ USD {MIN_TOTAL_DEBT_USD / 1e9:g} bn (emisor de bonos)", len(solvent)))
    _abort_if_empty(solvent, "deuda mínima", funnel)

    # --- Fase 3: tendencia del FCF -------------------------------------------
    log.info("Fase 3: tendencia del FCF para %d emisores…", len(solvent))
    growth = stage_fcf(fmp, solvent)
    funnel.append((f"FCF creciente {FCF_FILTER_LOGIC} CAGR > {MIN_FCF_CAGR:.0%}", len(growth)))
    _abort_if_empty(growth, "FCF", funnel)

    # --- Fase 4: rating sintético ---------------------------------------------
    log.info("Fase 4: rating sintético para %d emisores…", len(growth))
    ig = stage_rating(growth)
    _abort_if_empty(ig, "rating", funnel)

    # --- Fase 5: scoring y Top N ---------------------------------------------
    ranked = stage_scoring(ig)
    if RATING_SELECTION:
        ranked = select_ratings(ranked)
        funnel.append((f"Rating ∈ {{{', '.join(_selected_ratings())}}}", len(ranked)))
        _abort_if_empty(ranked, "selección de rating", funnel)
    top = ranked.head(TOP_N).reset_index(drop=True)
    funnel.append((f"Top {TOP_N} por Composite Credit Score", len(top)))
    if len(top) < TOP_N:
        log.warning("Solo %d emisores superaron todos los filtros (TOP_N=%d).", len(top), TOP_N)

    # --- Fase 6: pesos + overlay ---------------------------------------------
    top = stage_weights(top)
    overlay = stage_overlay(top, curve)
    summary = portfolio_summary(top, overlay)

    # --- Reportes -------------------------------------------------------------
    print_funnel(funnel)
    print_ranking(top)
    print_weights(top, summary)
    print_overlay(overlay)
    print_refinitiv_instructions(top, overlay)

    path = build_html_report(curve, funnel, top, overlay, summary, fmp.n_calls)
    export_universe_json(top)
    _banner("FIN DEL PIPELINE")
    print(f"  Reporte interactivo: {path}")
    print(f"  Llamadas FMP: {fmp.n_calls} (fallidas: {fmp.n_failures}) · Tiempo: {time.time() - t0:,.1f}s")
    if OPEN_HTML_IN_BROWSER:
        webbrowser.open(path.as_uri())  # sin navegador (contenedor) devuelve False, no lanza


if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        log.warning("Ejecución interrumpida por el usuario.")
        sys.exit(130)

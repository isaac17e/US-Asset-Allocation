# ══════════════════════════════════════════════════════════════════════════════════════════════
# LIBRERÍAS
# ══════════════════════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import logging
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, List, Literal, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
from scipy import stats
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq, linprog, minimize

try:
    import cvxpy as cp
    CVXPY_AVAILABLE: bool = True
except ImportError:
    cp = None
    CVXPY_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE: bool = True
except ImportError:
    TABULATE_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · CREDENCIALES Y ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════════════════════

FMP_API_KEY: str = os.getenv("FMP_API_KEY", "PEGA_AQUI_TU_API_KEY_DE_FMP")
POLYGON_API_KEY: str = os.getenv("POLYGON_API_KEY", "PEGA_AQUI_TU_API_KEY_DE_POLYGON")
FMP_BASE_URL: str = "https://financialmodelingprep.com/stable"
POLYGON_BASE_URL: str = "https://api.polygon.io"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · PERFIL, SOLVER Y SUPUESTOS DE MERCADO
# ══════════════════════════════════════════════════════════════════════════════════════════════

INVESTMENT_PROFILE: Literal["Conservador", "Crecimiento", "Momentum/Agresivo"] = "Crecimiento"
SOLVER: Literal["cvxpy", "scipy", "qubo_sa"] = "cvxpy"
RUN_SOLVER_COMPARISON: bool = True

BENCHMARK_TICKER: str = "SPY"
RISK_FREE_RATE: float = 0.040
EQUITY_RISK_PREMIUM: float = 0.050
HISTORICAL_MU_BLEND: float = 0.25
PRICE_HISTORY_YEARS: int = 3
MIN_PRICE_OBSERVATIONS: int = 260


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · UNIVERSO HÍBRIDO
# ══════════════════════════════════════════════════════════════════════════════════════════════

MIN_DOLLAR_VOLUME_USD: float = 1_000_000.0
US_EXCHANGES: Tuple[str, ...] = ("NYSE", "NASDAQ", "AMEX")
SCREENER_LIMIT_PER_EXCHANGE: int = 1000
DYNAMIC_CANDIDATE_POOL: int = 90
MAX_DYNAMIC_ETFS: int = 25
REDUNDANCY_CORRELATION_THRESHOLD: float = 0.985
EXCLUDE_LEVERAGED_INVERSE: bool = True


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · FACTORES
# ══════════════════════════════════════════════════════════════════════════════════════════════

FACTORS: Tuple[str, ...] = ("Value", "Growth", "Momentum", "Quality", "LowVol")
TOP_HOLDINGS_PER_ETF: int = 10
FETCH_GROWTH_FUNDAMENTALS: bool = True
NEUTRAL_FACTOR_SCORE: float = 0.50
MOMENTUM_LOOKBACK_DAYS: int = 252
MOMENTUM_SKIP_DAYS: int = 21
VOLATILITY_LOOKBACK_DAYS: int = 252


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · OPCIONES (BKM), COVARIANZA Y TILT DE RETORNOS
# ══════════════════════════════════════════════════════════════════════════════════════════════

OPTIONS_MIN_DAYS: int = 30
OPTIONS_MAX_DAYS: int = 90
OPTIONS_TARGET_DAYS: int = 60
MIN_OTM_STRIKES_PER_SIDE: int = 4
MAX_OPTION_PAGES: int = 8
BKM_SPLINE_POINTS: int = 200

COVARIANCE_MODE: Literal["correlation", "beta"] = "correlation"
CORRELATION_LOOKBACK_DAYS: int = 252
CORRELATION_SHRINKAGE: float = 0.10

SKEW_THRESHOLD: float = -1.0
SKEW_PENALTY: float = 0.010
KURTOSIS_THRESHOLD: float = 6.0
KURTOSIS_PENALTY: float = 0.002


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · QUBO / SIMULATED ANNEALING
# ══════════════════════════════════════════════════════════════════════════════════════════════

QUBO_BITS_PER_ASSET: int = 5
SA_ITERATIONS: int = 80_000
SA_BUDGET_PENALTY: float = 25.0
SA_FACTOR_PENALTY: float = 25.0
SA_FACTOR_PENALTY_MAX_MULT: float = 50.0
SA_RANDOM_SEED: int = 42


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · RED, LOGS Y SALIDA
# ══════════════════════════════════════════════════════════════════════════════════════════════

FMP_MIN_INTERVAL_SECONDS: float = 0.25
POLYGON_MIN_INTERVAL_SECONDS: float = 0.0
HTTP_TIMEOUT_SECONDS: int = 30
HTTP_MAX_RETRIES: int = 4
DASHBOARD_FILE: str = "portfolio_dashboard.html"
LOG_LEVEL: str = "INFO"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · PERFILES DE INVERSIÓN (Target_k mínimos sobre scores 0-1)
# ══════════════════════════════════════════════════════════════════════════════════════════════

PROFILES: Dict[str, Dict[str, Any]] = {
    "Conservador": {
        "risk_aversion": 8.0,
        "max_weight": 0.15,
        "targets": {"Value": 0.45, "Growth": 0.00, "Momentum": 0.00, "Quality": 0.55, "LowVol": 0.70},
    },
    "Crecimiento": {
        "risk_aversion": 4.0,
        "max_weight": 0.20,
        "targets": {"Value": 0.00, "Growth": 0.60, "Momentum": 0.45, "Quality": 0.55, "LowVol": 0.00},
    },
    "Momentum/Agresivo": {
        "risk_aversion": 2.0,
        "max_weight": 0.25,
        "targets": {"Value": 0.00, "Growth": 0.55, "Momentum": 0.70, "Quality": 0.00, "LowVol": 0.00},
    },
}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PARÁMETROS EDITABLES · LISTA MAESTRA DE ETFs (ticker: (categoría, clase de activo))
# ══════════════════════════════════════════════════════════════════════════════════════════════

MASTER_ETF_LIST: Dict[str, Tuple[str, str]] = {
    "SPY": ("Core EE.UU.", "Equity"),
    "QQQ": ("Core EE.UU.", "Equity"),
    "IWM": ("Core EE.UU.", "Equity"),
    "DIA": ("Core EE.UU.", "Equity"),
    "RSP": ("Core EE.UU.", "Equity"),
    "VTV": ("Factor / Estilo", "Equity"),
    "VUG": ("Factor / Estilo", "Equity"),
    "MTUM": ("Factor / Estilo", "Equity"),
    "QUAL": ("Factor / Estilo", "Equity"),
    "USMV": ("Factor / Estilo", "Equity"),
    "XLK": ("Sector", "Equity"),
    "XLF": ("Sector", "Equity"),
    "XLV": ("Sector", "Equity"),
    "XLE": ("Sector", "Equity"),
    "XLI": ("Sector", "Equity"),
    "XLY": ("Sector", "Equity"),
    "XLP": ("Sector", "Equity"),
    "XLU": ("Sector", "Equity"),
    "XLB": ("Sector", "Equity"),
    "XLRE": ("Sector", "Real Estate"),
    "XLC": ("Sector", "Equity"),
    "SMH": ("Megatendencia", "Equity"),
    "IGV": ("Megatendencia", "Equity"),
    "IBB": ("Megatendencia", "Equity"),
    "ICLN": ("Megatendencia", "Equity"),
    "ARKK": ("Megatendencia", "Equity"),
    "CIBR": ("Megatendencia", "Equity"),
    "LIT": ("Megatendencia", "Equity"),
    "ITA": ("Megatendencia", "Equity"),
    "EFA": ("Internacional", "Equity"),
    "EEM": ("Internacional", "Equity"),
    "VGK": ("Internacional", "Equity"),
    "EWJ": ("Internacional", "Equity"),
    "FXI": ("Internacional", "Equity"),
    "INDA": ("Internacional", "Equity"),
    "EWZ": ("Internacional", "Equity"),
    "GLD": ("Commodities", "Commodity"),
    "SLV": ("Commodities", "Commodity"),
    "USO": ("Commodities", "Commodity"),
    "DBC": ("Commodities", "Commodity"),
    "TLT": ("Renta Fija", "Fixed Income"),
    "IEF": ("Renta Fija", "Fixed Income"),
    "SHY": ("Renta Fija", "Fixed Income"),
    "AGG": ("Renta Fija", "Fixed Income"),
    "LQD": ("Renta Fija", "Fixed Income"),
    "HYG": ("Renta Fija", "Fixed Income"),
    "TIP": ("Renta Fija", "Fixed Income"),
    "EMB": ("Renta Fija", "Fixed Income"),
    "VNQ": ("Real Estate", "Real Estate"),
}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# UTILIDADES GENERALES
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _to_float(value: Any) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return result if math.isfinite(result) else float("nan")


def _first_number(record: Mapping[str, Any], keys: Sequence[str]) -> float:
    for key in keys:
        if key in record:
            value = _to_float(record[key])
            if math.isfinite(value):
                return value
    return float("nan")


def _clip(value: float, lower: float, upper: float) -> float:
    return float(min(max(value, lower), upper)) if math.isfinite(value) else float("nan")


def _is_configured_key(key: str) -> bool:
    return bool(key) and not key.startswith("PEGA_AQUI")


def _percentile_score(series: pd.Series) -> pd.Series:
    valid = series.replace([np.inf, -np.inf], np.nan).dropna()
    scores = pd.Series(np.nan, index=series.index, dtype=float)
    if valid.empty:
        return scores
    if len(valid) == 1:
        scores.loc[valid.index] = 0.5
        return scores
    ranks = valid.rank(method="average")
    scores.loc[valid.index] = (ranks - 1.0) / (len(valid) - 1.0)
    return scores


def _combine_scores(scores: Sequence[pd.Series]) -> pd.Series:
    return pd.concat(list(scores), axis=1).mean(axis=1, skipna=True)


def _nearest_psd(matrix: np.ndarray, floor: float = 1e-10) -> np.ndarray:
    symmetric = 0.5 * (matrix + matrix.T)
    original_diag = np.clip(np.diag(symmetric).copy(), floor, None)
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    repaired = eigenvectors @ np.diag(np.clip(eigenvalues, floor, None)) @ eigenvectors.T
    scaling = np.sqrt(original_diag / np.clip(np.diag(repaired), floor, None))
    repaired = repaired * np.outer(scaling, scaling)
    return 0.5 * (repaired + repaired.T)


def _project_capped_simplex(vector: np.ndarray, cap: float) -> np.ndarray:
    values = np.clip(vector, 0.0, None)
    lower, upper = float(values.min()) - 1.0, float(values.max())
    for _ in range(200):
        tau = 0.5 * (lower + upper)
        if np.clip(values - tau, 0.0, cap).sum() > 1.0:
            lower = tau
        else:
            upper = tau
    projected = np.clip(values - 0.5 * (lower + upper), 0.0, cap)
    return projected / projected.sum()


def _historical_betas(returns: pd.DataFrame, benchmark: pd.Series) -> pd.Series:
    variance = float(benchmark.var())
    if not math.isfinite(variance) or variance <= 0:
        raise ValueError("Varianza del benchmark inválida para calcular betas.")
    return returns.apply(lambda column: column.cov(benchmark) / variance)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# EXCEPCIONES Y ESTRUCTURAS DE DATOS
# ══════════════════════════════════════════════════════════════════════════════════════════════

class APIError(Exception):
    """Error genérico de comunicación con un proveedor de datos."""


class APIAuthorizationError(APIError):
    """Clave inválida o endpoint no incluido en el plan contratado."""


class OptimizationError(Exception):
    """Fallo del motor de optimización."""


@dataclass(frozen=True)
class ProfileConfig:
    name: str
    risk_aversion: float
    max_weight: float
    factor_targets: Dict[str, float]

    @classmethod
    def from_registry(cls, name: str, registry: Mapping[str, Mapping[str, Any]]) -> "ProfileConfig":
        if name not in registry:
            raise ValueError(f"Perfil '{name}' no definido. Opciones: {list(registry)}")
        spec = registry[name]
        targets = {factor: float(spec["targets"].get(factor, 0.0)) for factor in FACTORS}
        return cls(name, float(spec["risk_aversion"]), float(spec["max_weight"]), targets)

    def target_vector(self) -> np.ndarray:
        return np.array([self.factor_targets[factor] for factor in FACTORS], dtype=float)


@dataclass
class ETFDescriptor:
    ticker: str
    name: str
    category: str
    asset_class: str
    source: str
    dollar_volume: float = float("nan")
    priority: int = 0


@dataclass
class OptimizationResult:
    method: str
    weights: pd.Series
    expected_return: float
    volatility: float
    utility: float
    factor_exposure: pd.Series
    max_factor_violation: float
    status: str
    runtime_seconds: float


# ══════════════════════════════════════════════════════════════════════════════════════════════
# CLIENTE HTTP BASE (THROTTLING, REINTENTOS Y MANEJO DE ERRORES)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class BaseHTTPClient:
    def __init__(self, api_key: str, provider: str, min_interval: float, timeout: int, max_retries: int) -> None:
        self.api_key = api_key
        self.provider = provider
        self.min_interval = min_interval
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ETF-Passive-Allocator/1.0"})
        self.logger = logging.getLogger(provider)
        self._last_request_ts: float = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request_ts = time.monotonic()

    @staticmethod
    def _backoff(attempt: int, retry_after: Optional[str]) -> None:
        wait = _to_float(retry_after) if retry_after is not None else float("nan")
        time.sleep(max(wait if math.isfinite(wait) else 0.0, min(2.0 ** attempt, 60.0)))

    def _request_json(self, url: str, params: Optional[Dict[str, Any]], endpoint: str) -> Any:
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = exc
                self._backoff(attempt, None)
                continue
            status = response.status_code
            if status == 429 or status >= 500:
                last_error = APIError(f"HTTP {status}")
                self.logger.debug("%s %s: HTTP %s, reintento %d", self.provider, endpoint, status, attempt)
                self._backoff(attempt, response.headers.get("Retry-After"))
                continue
            if status in (401, 402, 403):
                raise APIAuthorizationError(f"{self.provider} {endpoint}: HTTP {status} (clave inválida o plan sin acceso)")
            if status == 404:
                raise APIError(f"{self.provider} {endpoint}: recurso no encontrado (404)")
            if not response.ok:
                raise APIError(f"{self.provider} {endpoint}: HTTP {status}")
            try:
                return response.json()
            except ValueError as exc:
                raise APIError(f"{self.provider} {endpoint}: respuesta no es JSON válido") from exc
        raise APIError(f"{self.provider} {endpoint}: agotados {self.max_retries} reintentos ({last_error})")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# CLIENTE FINANCIAL MODELING PREP
# ══════════════════════════════════════════════════════════════════════════════════════════════

class FMPClient(BaseHTTPClient):
    PLAN_ERROR_TOKENS: Tuple[str, ...] = ("api key", "subscription", "premium", "legacy", "upgrade")

    def __init__(self, api_key: str, base_url: str, min_interval: float, timeout: int, max_retries: int) -> None:
        super().__init__(api_key, "FMP", min_interval, timeout, max_retries)
        self.base_url = base_url.rstrip("/")
        self._cache: Dict[Tuple[str, str], Any] = {}

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        query = dict(params or {})
        cache_key = (endpoint, repr(sorted(query.items())))
        if cache_key in self._cache:
            return self._cache[cache_key]
        query["apikey"] = self.api_key
        payload = self._request_json(f"{self.base_url}/{endpoint}", query, endpoint)
        if isinstance(payload, dict) and "Error Message" in payload:
            message = str(payload["Error Message"])
            if any(token in message.lower() for token in self.PLAN_ERROR_TOKENS):
                raise APIAuthorizationError(f"FMP {endpoint}: {message}")
            raise APIError(f"FMP {endpoint}: {message}")
        self._cache[cache_key] = payload
        return payload

    @staticmethod
    def _as_records(payload: Any) -> List[Dict[str, Any]]:
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        if isinstance(payload, dict):
            for key in ("historical", "data", "results"):
                if isinstance(payload.get(key), list):
                    return [row for row in payload[key] if isinstance(row, dict)]
            return [payload] if payload else []
        return []

    def _single_record(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        records = self._as_records(self._get(endpoint, params))
        return records[0] if records else {}

    def screen_etfs(self, exchange: str, limit: int, min_share_volume: int) -> List[Dict[str, Any]]:
        params = {
            "isEtf": "true",
            "isActivelyTrading": "true",
            "exchange": exchange,
            "volumeMoreThan": min_share_volume,
            "limit": limit,
        }
        return self._as_records(self._get("company-screener", params))

    def etf_info(self, symbol: str) -> Dict[str, Any]:
        return self._single_record("etf/info", {"symbol": symbol})

    def etf_holdings(self, symbol: str) -> List[Dict[str, Any]]:
        return self._as_records(self._get("etf/holdings", {"symbol": symbol}))

    def ratios_ttm(self, symbol: str) -> Dict[str, Any]:
        return self._single_record("ratios-ttm", {"symbol": symbol})

    def key_metrics_ttm(self, symbol: str) -> Dict[str, Any]:
        return self._single_record("key-metrics-ttm", {"symbol": symbol})

    def financial_growth(self, symbol: str) -> Dict[str, Any]:
        return self._single_record("financial-growth", {"symbol": symbol, "period": "annual", "limit": 1})

    def historical_adjusted_close(self, symbol: str, start: date, end: date) -> pd.Series:
        params = {"symbol": symbol, "from": start.isoformat(), "to": end.isoformat()}
        try:
            records = self._as_records(self._get("historical-price-eod/dividend-adjusted", params))
        except APIAuthorizationError:
            records = []
        if not records:
            records = self._as_records(self._get("historical-price-eod/full", params))
        frame = pd.DataFrame(records)
        if frame.empty or "date" not in frame.columns:
            return pd.Series(dtype=float, name=symbol)
        price_column = next((col for col in ("adjClose", "close", "price") if col in frame.columns), None)
        if price_column is None:
            return pd.Series(dtype=float, name=symbol)
        series = pd.Series(
            pd.to_numeric(frame[price_column], errors="coerce").to_numpy(),
            index=pd.to_datetime(frame["date"]),
            name=symbol,
        ).dropna().sort_index()
        return series[~series.index.duplicated(keep="last")]


# ══════════════════════════════════════════════════════════════════════════════════════════════
# CLIENTE POLYGON.IO
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PolygonClient(BaseHTTPClient):
    def __init__(self, api_key: str, base_url: str, min_interval: float, timeout: int, max_retries: int) -> None:
        super().__init__(api_key, "Polygon", min_interval, timeout, max_retries)
        self.base_url = base_url.rstrip("/")

    def options_chain_snapshot(self, underlying: str, expiration_gte: date, expiration_lte: date, max_pages: int) -> List[Dict[str, Any]]:
        endpoint = f"v3/snapshot/options/{underlying}"
        url: Optional[str] = f"{self.base_url}/{endpoint}"
        params: Dict[str, Any] = {
            "expiration_date.gte": expiration_gte.isoformat(),
            "expiration_date.lte": expiration_lte.isoformat(),
            "limit": 250,
            "apiKey": self.api_key,
        }
        contracts: List[Dict[str, Any]] = []
        pages = 0
        while url and pages < max_pages:
            payload = self._request_json(url, params, endpoint)
            if not isinstance(payload, dict):
                break
            status = str(payload.get("status", "")).upper()
            if status == "NOT_AUTHORIZED":
                raise APIAuthorizationError(f"Polygon {endpoint}: {payload.get('message', 'sin autorización')}")
            if status == "ERROR":
                raise APIError(f"Polygon {endpoint}: {payload.get('error') or payload.get('message')}")
            contracts.extend(row for row in (payload.get("results") or []) if isinstance(row, dict))
            url = payload.get("next_url")
            params = {"apiKey": self.api_key}
            pages += 1
        return contracts


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 0 · UNIVERSO HÍBRIDO (LISTA MAESTRA + SCREENER DINÁMICO FMP)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class UniverseBuilder:
    ISSUER_TOKENS: Tuple[str, ...] = (
        "ishares", "vanguard", "spdr", "invesco", "schwab", "state street", "select sector", "global x",
        "vaneck", "wisdomtree", "first trust", "proshares", "direxion", "jpmorgan", "fidelity", "franklin",
        "dimensional", "avantis", "pacer", "ark", "sprott", "abrdn", "goldman sachs", "xtrackers",
        "janus henderson", "capital group", "amplify", "roundhill", "defiance", "simplify", "neos",
    )
    STOPWORDS: frozenset = frozenset({"etf", "fund", "trust", "shares", "portfolio", "index", "the", "inc", "llc", "core", "ucits", "usd"})
    LEVERAGE_PATTERN: re.Pattern = re.compile(
        r"(\b-?[123](\.\d)?x\b|\bultra(pro)?\b|\binverse\b|\bbear\b|\bbull\b|\bleveraged\b|\bdaily\b|\bvix\b|"
        r"\bvolatility futures\b|\bshort\b(?![\s-](term|duration|maturity)))",
        re.IGNORECASE,
    )

    def __init__(self, fmp: FMPClient, master_list: Mapping[str, Tuple[str, str]]) -> None:
        self.fmp = fmp
        self.master_list = master_list
        self.logger = logging.getLogger("Universo")

    def build_candidates(self) -> List[ETFDescriptor]:
        master = [
            ETFDescriptor(ticker, category, category, asset_class, "Maestra", priority=index)
            for index, (ticker, (category, asset_class)) in enumerate(self.master_list.items())
        ]
        dynamic = self._dynamic_candidates(set(self.master_list))
        self.logger.info("Lista Maestra: %d ETFs | Candidatos dinámicos FMP: %d", len(master), len(dynamic))
        return master + dynamic

    def _dynamic_candidates(self, master_set: set) -> List[ETFDescriptor]:
        raw: Dict[str, Dict[str, Any]] = {}
        for exchange in US_EXCHANGES:
            try:
                records = self.fmp.screen_etfs(exchange, SCREENER_LIMIT_PER_EXCHANGE, 10_000)
            except APIAuthorizationError as exc:
                self.logger.error("Screener FMP no disponible, se usa solo la Lista Maestra: %s", exc)
                return []
            except APIError as exc:
                self.logger.warning("Screener FMP falló para %s: %s", exchange, exc)
                continue
            for record in records:
                candidate = self._parse_screener_record(record, master_set)
                if candidate and candidate["dollar_volume"] > raw.get(candidate["symbol"], {}).get("dollar_volume", -1.0):
                    raw[candidate["symbol"]] = candidate
        ordered = sorted(raw.values(), key=lambda row: row["dollar_volume"], reverse=True)
        return self._enrich_and_deduplicate(ordered)

    def _parse_screener_record(self, record: Mapping[str, Any], master_set: set) -> Optional[Dict[str, Any]]:
        symbol = str(record.get("symbol", "")).upper().strip()
        if not symbol or symbol in master_set or not re.fullmatch(r"[A-Z]{1,5}", symbol):
            return None
        if record.get("isEtf") is False or record.get("isActivelyTrading") is False:
            return None
        exchange = str(record.get("exchangeShortName") or record.get("exchange") or "").upper()
        if exchange and exchange not in US_EXCHANGES:
            return None
        price = _first_number(record, ("price",))
        volume = _first_number(record, ("volume", "avgVolume"))
        if not (math.isfinite(price) and math.isfinite(volume)) or price * volume < MIN_DOLLAR_VOLUME_USD:
            return None
        name = str(record.get("companyName") or record.get("name") or symbol)
        if EXCLUDE_LEVERAGED_INVERSE and self.LEVERAGE_PATTERN.search(name):
            return None
        return {"symbol": symbol, "name": name, "price": price, "dollar_volume": price * volume}

    def _enrich_and_deduplicate(self, ordered: List[Dict[str, Any]]) -> List[ETFDescriptor]:
        seen_keys: set = set()
        selected: List[ETFDescriptor] = []
        for row in ordered:
            if len(selected) >= DYNAMIC_CANDIDATE_POOL:
                break
            name_key = self._name_key(row["name"]) or row["symbol"]
            if name_key in seen_keys:
                self.logger.debug("Descartado %s por nombre redundante (%s)", row["symbol"], name_key)
                continue
            try:
                info = self.fmp.etf_info(row["symbol"])
            except APIError as exc:
                self.logger.debug("etf/info no disponible para %s: %s", row["symbol"], exc)
                info = {}
            avg_volume = _first_number(info, ("avgVolume", "averageVolume"))
            dollar_volume = avg_volume * row["price"] if math.isfinite(avg_volume) else row["dollar_volume"]
            if dollar_volume < MIN_DOLLAR_VOLUME_USD:
                continue
            asset_class = self._normalize_asset_class(str(info.get("assetClass") or ""), row["name"])
            seen_keys.add(name_key)
            selected.append(
                ETFDescriptor(row["symbol"], str(info.get("name") or row["name"]), f"Dinámico FMP · {asset_class}", asset_class, "FMP", dollar_volume, len(selected))
            )
        return selected

    @classmethod
    def _name_key(cls, name: str) -> str:
        text = name.lower()
        for issuer in cls.ISSUER_TOKENS:
            text = re.sub(rf"\b{re.escape(issuer)}\b", " ", text)
        tokens = re.findall(r"[a-z0-9&]+", text)
        return " ".join(token for token in tokens if token not in cls.STOPWORDS)

    @staticmethod
    def _normalize_asset_class(raw_class: str, name: str) -> str:
        raw = raw_class.lower()
        if any(token in raw for token in ("equity", "stock")):
            return "Equity"
        if any(token in raw for token in ("fixed", "bond")):
            return "Fixed Income"
        if "commodit" in raw:
            return "Commodity"
        if "real estate" in raw:
            return "Real Estate"
        text = name.lower()
        if any(token in text for token in ("bond", "treasury", "municipal", "fixed income", "aggregate", "t-bill", "credit")):
            return "Fixed Income"
        if any(token in text for token in ("gold", "silver", "oil", "commodity", "bitcoin", "ether", "copper", "natural gas")):
            return "Commodity"
        if any(token in text for token in ("reit", "real estate")):
            return "Real Estate"
        return "Equity"


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 0 · DESCARGA DE PRECIOS Y FILTRO DE RÉPLICAS POR CORRELACIÓN
# ══════════════════════════════════════════════════════════════════════════════════════════════

class MarketDataLoader:
    def __init__(self, fmp: FMPClient, years: int, min_observations: int) -> None:
        self.fmp = fmp
        self.years = years
        self.min_observations = min_observations
        self.logger = logging.getLogger("Precios")

    def load(self, tickers: Sequence[str]) -> pd.DataFrame:
        end = date.today()
        start = end - timedelta(days=int(365.25 * self.years) + 10)
        collected: List[pd.Series] = []
        for index, ticker in enumerate(tickers, start=1):
            try:
                series = self.fmp.historical_adjusted_close(ticker, start, end)
            except APIAuthorizationError:
                raise
            except APIError as exc:
                self.logger.warning("Sin precios para %s: %s", ticker, exc)
                continue
            if len(series) < self.min_observations:
                self.logger.warning("%s descartado: %d observaciones (< %d)", ticker, len(series), self.min_observations)
                continue
            collected.append(series)
            if index % 20 == 0:
                self.logger.info("Precios descargados: %d/%d", index, len(tickers))
        if not collected:
            raise RuntimeError("No fue posible descargar series de precios para ningún ETF.")
        return pd.concat(collected, axis=1).sort_index().ffill(limit=3)


class RedundancyFilter:
    def __init__(self, threshold: float, lookback: int, max_dynamic: int) -> None:
        self.threshold = threshold
        self.lookback = lookback
        self.max_dynamic = max_dynamic
        self.logger = logging.getLogger("Desduplicación")

    def apply(self, candidates: Sequence[ETFDescriptor], returns: pd.DataFrame) -> Tuple[List[ETFDescriptor], pd.DataFrame]:
        available = [etf for etf in candidates if etf.ticker in returns.columns]
        missing_master = [etf.ticker for etf in candidates if etf.source == "Maestra" and etf.ticker not in returns.columns]
        if missing_master:
            self.logger.warning("ETFs maestros sin datos suficientes: %s", ", ".join(missing_master))
        recent = returns[[etf.ticker for etf in available]].tail(self.lookback)
        correlation = recent.corr(min_periods=int(self.lookback * 0.8))
        kept = sorted([etf for etf in available if etf.source == "Maestra"], key=lambda etf: etf.priority)
        dynamic = sorted(
            [etf for etf in available if etf.source != "Maestra"],
            key=lambda etf: etf.dollar_volume if math.isfinite(etf.dollar_volume) else 0.0,
            reverse=True,
        )
        dropped: List[Dict[str, Any]] = []
        dynamic_count = 0
        for etf in dynamic:
            if dynamic_count >= self.max_dynamic:
                dropped.append({"Ticker": etf.ticker, "Motivo": "Cupo dinámico alcanzado", "Gemelo": "", "Correlación": np.nan})
                continue
            row = correlation.loc[etf.ticker, [k.ticker for k in kept]].dropna()
            if row.empty:
                dropped.append({"Ticker": etf.ticker, "Motivo": "Historial insuficiente", "Gemelo": "", "Correlación": np.nan})
                continue
            twin, rho = str(row.idxmax()), float(row.max())
            if rho >= self.threshold:
                dropped.append({"Ticker": etf.ticker, "Motivo": "Réplica redundante", "Gemelo": twin, "Correlación": rho})
                continue
            kept.append(etf)
            dynamic_count += 1
        self.logger.info("Universo definitivo: %d ETFs (%d dinámicos) | Descartados: %d", len(kept), dynamic_count, len(dropped))
        return kept, pd.DataFrame(dropped, columns=["Ticker", "Motivo", "Gemelo", "Correlación"])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 1 · MATRIZ DE CARGAS FACTORIALES B
# ══════════════════════════════════════════════════════════════════════════════════════════════

class FactorModelBuilder:
    FUNDAMENTAL_COLUMNS: Tuple[str, ...] = ("EarningsYield", "BookYield", "ROE", "ROIC", "RevenueGrowth", "EPSGrowth")
    TECHNICAL_COLUMNS: Tuple[str, ...] = ("Momentum_12_1", "Volatilidad_252d")

    def __init__(self, fmp: FMPClient, prices: pd.DataFrame) -> None:
        self.fmp = fmp
        self.prices = prices
        self.logger = logging.getLogger("Factores")
        self._holding_cache: Dict[str, Dict[str, float]] = {}
        self._disabled_endpoints: set = set()

    def build(self, universe: Sequence[ETFDescriptor]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        tickers = [etf.ticker for etf in universe]
        raw = pd.DataFrame(np.nan, index=tickers, columns=list(self.FUNDAMENTAL_COLUMNS + self.TECHNICAL_COLUMNS), dtype=float)
        for index, etf in enumerate(universe, start=1):
            if etf.asset_class in ("Equity", "Real Estate"):
                for column, value in self._aggregate_fundamentals(etf.ticker).items():
                    raw.loc[etf.ticker, column] = value
            raw.loc[etf.ticker, "Momentum_12_1"] = self._momentum(etf.ticker)
            raw.loc[etf.ticker, "Volatilidad_252d"] = self._volatility(etf.ticker)
            if index % 10 == 0:
                self.logger.info("Factores procesados: %d/%d", index, len(universe))
        raw = raw.replace([np.inf, -np.inf], np.nan)
        return self._assemble_matrix(raw), raw

    def _assemble_matrix(self, raw: pd.DataFrame) -> pd.DataFrame:
        value = _combine_scores([_percentile_score(raw["EarningsYield"]), _percentile_score(raw["BookYield"])])
        quality = _combine_scores([_percentile_score(raw["ROE"]), _percentile_score(raw["ROIC"])])
        if raw[["RevenueGrowth", "EPSGrowth"]].notna().any().any():
            growth = _combine_scores([_percentile_score(raw["RevenueGrowth"]), _percentile_score(raw["EPSGrowth"])])
        else:
            self.logger.warning("Sin datos de crecimiento: Growth se aproxima como 1 - Value.")
            growth = 1.0 - value
        matrix = pd.DataFrame(
            {
                "Value": value,
                "Growth": growth,
                "Momentum": _percentile_score(raw["Momentum_12_1"]),
                "Quality": quality,
                "LowVol": _percentile_score(-raw["Volatilidad_252d"]),
            },
            index=raw.index,
        )
        return matrix[list(FACTORS)].fillna(NEUTRAL_FACTOR_SCORE).clip(0.0, 1.0)

    def _aggregate_fundamentals(self, ticker: str) -> Dict[str, float]:
        if "etf_holdings" in self._disabled_endpoints:
            return {}
        try:
            holdings = self.fmp.etf_holdings(ticker)
        except APIAuthorizationError as exc:
            self._disabled_endpoints.add("etf_holdings")
            self.logger.warning("Holdings de ETFs no disponibles en el plan FMP (Value/Quality/Growth neutrales): %s", exc)
            return {}
        except APIError as exc:
            self.logger.debug("Holdings no disponibles para %s: %s", ticker, exc)
            return {}
        parsed: List[Tuple[str, float]] = []
        for holding in holdings:
            symbol = str(holding.get("asset") or holding.get("symbol") or "").upper().strip()
            weight = _first_number(holding, ("weightPercentage", "weight"))
            if re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", symbol) and math.isfinite(weight) and weight > 0:
                parsed.append((symbol, weight))
        parsed.sort(key=lambda item: item[1], reverse=True)
        rows: List[Dict[str, float]] = []
        weights: List[float] = []
        for symbol, weight in parsed[:TOP_HOLDINGS_PER_ETF]:
            metrics = self._holding_metrics(symbol)
            if metrics:
                rows.append(metrics)
                weights.append(weight)
        if not rows:
            return {}
        frame = pd.DataFrame(rows)
        weight_array = np.asarray(weights, dtype=float)
        aggregated: Dict[str, float] = {}
        for column in frame.columns:
            values = frame[column].to_numpy(dtype=float)
            mask = np.isfinite(values)
            aggregated[column] = float(np.average(values[mask], weights=weight_array[mask])) if mask.any() else float("nan")
        return aggregated

    def _safe_fetch(self, fetcher: Callable[[str], Dict[str, Any]], symbol: str) -> Dict[str, Any]:
        endpoint = fetcher.__name__
        if endpoint in self._disabled_endpoints:
            return {}
        try:
            return fetcher(symbol)
        except APIAuthorizationError as exc:
            self._disabled_endpoints.add(endpoint)
            self.logger.warning("Endpoint %s deshabilitado (plan/credenciales): %s", endpoint, exc)
        except APIError as exc:
            self.logger.debug("%s falló para %s: %s", endpoint, symbol, exc)
        return {}

    def _holding_metrics(self, symbol: str) -> Dict[str, float]:
        if symbol in self._holding_cache:
            return self._holding_cache[symbol]
        ratios = self._safe_fetch(self.fmp.ratios_ttm, symbol)
        key_metrics = self._safe_fetch(self.fmp.key_metrics_ttm, symbol)
        pe = _first_number(ratios, ("priceToEarningsRatioTTM", "peRatioTTM", "priceEarningsRatioTTM"))
        pb = _first_number(ratios, ("priceToBookRatioTTM", "pbRatioTTM", "priceBookValueRatioTTM"))
        earnings_yield = _first_number(key_metrics, ("earningsYieldTTM",))
        if not math.isfinite(earnings_yield) and math.isfinite(pe) and pe != 0:
            earnings_yield = 1.0 / pe
        roe = _first_number(key_metrics, ("returnOnEquityTTM", "roeTTM"))
        if not math.isfinite(roe):
            roe = _first_number(ratios, ("returnOnEquityTTM",))
        metrics = {
            "EarningsYield": _clip(earnings_yield, -1.0, 1.0),
            "BookYield": _clip(1.0 / pb, 0.0, 5.0) if math.isfinite(pb) and pb > 0 else float("nan"),
            "ROE": _clip(roe, -2.0, 2.0),
            "ROIC": _clip(_first_number(key_metrics, ("returnOnInvestedCapitalTTM", "roicTTM")), -2.0, 2.0),
            "RevenueGrowth": float("nan"),
            "EPSGrowth": float("nan"),
        }
        if FETCH_GROWTH_FUNDAMENTALS:
            growth = self._safe_fetch(self.fmp.financial_growth, symbol)
            metrics["RevenueGrowth"] = _clip(_first_number(growth, ("revenueGrowth",)), -1.0, 3.0)
            metrics["EPSGrowth"] = _clip(_first_number(growth, ("epsgrowth", "epsGrowth", "epsdilutedGrowth")), -3.0, 3.0)
        if all(not math.isfinite(value) for value in metrics.values()):
            metrics = {}
        self._holding_cache[symbol] = metrics
        return metrics

    def _momentum(self, ticker: str) -> float:
        series = self.prices[ticker].dropna()
        if len(series) <= MOMENTUM_LOOKBACK_DAYS:
            return float("nan")
        return float(series.iloc[-1 - MOMENTUM_SKIP_DAYS] / series.iloc[-1 - MOMENTUM_LOOKBACK_DAYS] - 1.0)

    def _volatility(self, ticker: str) -> float:
        daily = self.prices[ticker].dropna().pct_change().dropna().tail(VOLATILITY_LOOKBACK_DAYS)
        return float(daily.std(ddof=1) * math.sqrt(252)) if len(daily) > 60 else float("nan")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 2 · ESTIMADOR BKM (BAKSHI, KAPADIA & MADAN, 2003)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class BKMEstimator:
    @staticmethod
    def _trapezoid(y: np.ndarray, x: np.ndarray) -> float:
        if len(x) < 2:
            return 0.0
        return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))

    @staticmethod
    def _bs_price(spot: float, strike: float, rate: float, maturity: float, vol: float, side: str) -> float:
        if vol <= 0.0 or maturity <= 0.0:
            return max(0.0, (spot - strike) if side == "call" else (strike - spot))
        d1 = (math.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * math.sqrt(maturity))
        d2 = d1 - vol * math.sqrt(maturity)
        if side == "call":
            return spot * stats.norm.cdf(d1) - strike * math.exp(-rate * maturity) * stats.norm.cdf(d2)
        return strike * math.exp(-rate * maturity) * stats.norm.cdf(-d2) - spot * stats.norm.cdf(-d1)

    @classmethod
    def _implied_vol(cls, price: float, spot: float, strike: float, rate: float, maturity: float, side: str) -> float:
        intrinsic = max(0.0, (spot - strike) if side == "call" else (strike - spot))
        if not math.isfinite(price) or price <= intrinsic + 1e-8:
            return float("nan")
        try:
            return brentq(lambda v: cls._bs_price(spot, strike, rate, maturity, v, side) - price, 1e-4, 5.0, xtol=1e-6)
        except ValueError:
            return float("nan")

    @classmethod
    def _resample_via_iv_spline(
        cls, spot: float, maturity: float, rate: float, strikes: np.ndarray, prices: np.ndarray, side: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        order = np.argsort(strikes)
        strikes, prices = strikes[order], prices[order]
        ivs = np.array([cls._implied_vol(p, spot, k, rate, maturity, side) for k, p in zip(strikes, prices)])
        valid = np.isfinite(ivs) & (ivs > 1e-4)
        if valid.sum() < 4:
            return strikes, prices
        log_moneyness, unique_idx = np.unique(np.log(strikes[valid] / spot), return_index=True)
        ivs_valid = ivs[valid][unique_idx]
        if len(log_moneyness) < 4:
            return strikes, prices
        spline = CubicSpline(log_moneyness, ivs_valid, bc_type="natural")
        fine_x = np.linspace(log_moneyness[0], log_moneyness[-1], BKM_SPLINE_POINTS)
        fine_iv = np.clip(spline(fine_x), 1e-4, 5.0)
        fine_strikes = spot * np.exp(fine_x)
        fine_prices = np.array([cls._bs_price(spot, k, rate, maturity, v, side) for k, v in zip(fine_strikes, fine_iv)])
        return fine_strikes, fine_prices

    @staticmethod
    def _anchor_at_spot(strikes: np.ndarray, prices: np.ndarray, spot: float, side: str) -> Tuple[np.ndarray, np.ndarray]:
        order = np.argsort(strikes)
        strikes, prices = strikes[order], prices[order]
        if len(strikes) < 2:
            return strikes, prices
        near, far = (0, 1) if side == "call" else (-1, -2)
        slope = (prices[near] - prices[far]) / (strikes[near] - strikes[far])
        atm_price = max(float(prices[near] + slope * (spot - strikes[near])), float(prices[near]))
        if side == "call":
            return np.concatenate([[spot], strikes]), np.concatenate([[atm_price], prices])
        return np.concatenate([strikes, [spot]]), np.concatenate([prices, [atm_price]])

    @classmethod
    def moments(
        cls,
        spot: float,
        maturity_years: float,
        rate: float,
        call_strikes: np.ndarray,
        call_prices: np.ndarray,
        put_strikes: np.ndarray,
        put_prices: np.ndarray,
    ) -> Optional[Dict[str, float]]:
        if spot <= 0 or maturity_years <= 0:
            return None
        kc_fine, c_fine = cls._resample_via_iv_spline(
            spot, maturity_years, rate, np.asarray(call_strikes, dtype=float), np.asarray(call_prices, dtype=float), "call"
        )
        kp_fine, p_fine = cls._resample_via_iv_spline(
            spot, maturity_years, rate, np.asarray(put_strikes, dtype=float), np.asarray(put_prices, dtype=float), "put"
        )
        kc, c = cls._anchor_at_spot(kc_fine, c_fine, spot, side="call")
        kp, p = cls._anchor_at_spot(kp_fine, p_fine, spot, side="put")
        log_c = np.log(kc / spot)
        log_p = np.log(spot / kp)
        v = cls._trapezoid(2.0 * (1.0 - log_c) / kc**2 * c, kc) + cls._trapezoid(2.0 * (1.0 + log_p) / kp**2 * p, kp)
        w = cls._trapezoid((6.0 * log_c - 3.0 * log_c**2) / kc**2 * c, kc) - cls._trapezoid((6.0 * log_p + 3.0 * log_p**2) / kp**2 * p, kp)
        x = cls._trapezoid((12.0 * log_c**2 - 4.0 * log_c**3) / kc**2 * c, kc) + cls._trapezoid((12.0 * log_p**2 + 4.0 * log_p**3) / kp**2 * p, kp)
        growth = math.exp(rate * maturity_years)
        mu = growth - 1.0 - growth * v / 2.0 - growth * w / 6.0 - growth * x / 24.0
        variance = growth * v - mu**2
        if not math.isfinite(variance) or variance <= 0:
            return None
        skewness = (growth * w - 3.0 * mu * growth * v + 2.0 * mu**3) / variance**1.5
        kurtosis = (growth * x - 4.0 * mu * growth * w + 6.0 * growth * mu**2 * v - 3.0 * mu**4) / variance**2
        if not (math.isfinite(skewness) and math.isfinite(kurtosis)):
            return None
        return {"annualized_variance": variance / maturity_years, "skewness": skewness, "kurtosis": kurtosis}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 2 · MOMENTOS IMPLÍCITOS POR ETF (POLYGON + FALLBACK HISTÓRICO)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class ImpliedMomentsEngine:
    def __init__(self, polygon: Optional[PolygonClient], prices: pd.DataFrame, rate: float) -> None:
        self.polygon = polygon
        self.prices = prices
        self.rate = rate
        self.logger = logging.getLogger("BKM")
        self._polygon_enabled = polygon is not None
        if polygon is None:
            self.logger.warning("POLYGON_API_KEY no configurada: se usarán momentos históricos como fallback.")

    def compute(self, tickers: Sequence[str]) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        for index, ticker in enumerate(tickers, start=1):
            estimate: Optional[Dict[str, Any]] = None
            if self._polygon_enabled:
                try:
                    estimate = self._implied_from_options(ticker)
                except APIAuthorizationError as exc:
                    self._polygon_enabled = False
                    self.logger.error("Snapshot de opciones no autorizado; fallback histórico para el resto: %s", exc)
                except APIError as exc:
                    self.logger.warning("Opciones no disponibles para %s: %s", ticker, exc)
            if estimate is None:
                estimate = self._historical_fallback(ticker)
            rows.append({"Ticker": ticker, **estimate})
            if index % 10 == 0:
                self.logger.info("Momentos implícitos: %d/%d", index, len(tickers))
        return pd.DataFrame(rows).set_index("Ticker")

    def _implied_from_options(self, ticker: str) -> Optional[Dict[str, Any]]:
        today = date.today()
        contracts = self.polygon.options_chain_snapshot(
            ticker, today + timedelta(days=OPTIONS_MIN_DAYS), today + timedelta(days=OPTIONS_MAX_DAYS), MAX_OPTION_PAGES
        )
        chain, spot = self._parse_chain(contracts, ticker)
        if chain.empty or not math.isfinite(spot):
            return None
        estimates: List[Dict[str, float]] = []
        for expiry, group in chain.groupby("expiry"):
            days = (datetime.strptime(str(expiry), "%Y-%m-%d").date() - today).days
            if days < OPTIONS_MIN_DAYS or days > OPTIONS_MAX_DAYS:
                continue
            calls = group[(group["type"] == "call") & (group["strike"] > spot)].groupby("strike")["price"].mean().sort_index()
            puts = group[(group["type"] == "put") & (group["strike"] < spot)].groupby("strike")["price"].mean().sort_index()
            if len(calls) < MIN_OTM_STRIKES_PER_SIDE or len(puts) < MIN_OTM_STRIKES_PER_SIDE:
                continue
            result = BKMEstimator.moments(
                spot, days / 365.0, self.rate, calls.index.to_numpy(), calls.to_numpy(), puts.index.to_numpy(), puts.to_numpy()
            )
            if result:
                estimates.append({"days": float(days), **result})
        if not estimates:
            return None
        blended = self._interpolate_to_target(estimates)
        mfiv = math.sqrt(blended["annualized_variance"])
        if not 0.005 < mfiv < 3.0:
            return None
        return {
            "MFIV": mfiv,
            "MFIS": _clip(blended["skewness"], -10.0, 10.0),
            "MFIK": _clip(blended["kurtosis"], 1.0, 50.0),
            "Fuente": "BKM (Polygon)",
            "Vencimientos": len(estimates),
        }

    def _parse_chain(self, contracts: Sequence[Mapping[str, Any]], ticker: str) -> Tuple[pd.DataFrame, float]:
        records: List[Dict[str, Any]] = []
        spots: List[float] = []
        for contract in contracts:
            details = contract.get("details") or {}
            quote = contract.get("last_quote") or {}
            contract_type = str(details.get("contract_type", "")).lower()
            strike = _to_float(details.get("strike_price"))
            expiry = details.get("expiration_date")
            if contract_type not in ("call", "put") or not math.isfinite(strike) or not expiry:
                continue
            bid, ask, mid = _to_float(quote.get("bid")), _to_float(quote.get("ask")), _to_float(quote.get("midpoint"))
            if not (math.isfinite(mid) and mid > 0):
                mid = 0.5 * (bid + ask) if math.isfinite(bid) and math.isfinite(ask) and 0 < bid <= ask else _to_float((contract.get("day") or {}).get("close"))
            if not (math.isfinite(mid) and mid > 0):
                continue
            spots.append(_to_float((contract.get("underlying_asset") or {}).get("price")))
            records.append({"type": contract_type, "strike": strike, "expiry": str(expiry), "price": mid})
        finite_spots = [value for value in spots if math.isfinite(value) and value > 0]
        spot = float(np.median(finite_spots)) if finite_spots else float(self.prices[ticker].dropna().iloc[-1])
        return pd.DataFrame(records), spot

    @staticmethod
    def _interpolate_to_target(estimates: List[Dict[str, float]]) -> Dict[str, float]:
        ordered = sorted(estimates, key=lambda item: item["days"])
        below = [item for item in ordered if item["days"] <= OPTIONS_TARGET_DAYS]
        above = [item for item in ordered if item["days"] >= OPTIONS_TARGET_DAYS]
        if below and above and below[-1]["days"] != above[0]["days"]:
            low, high = below[-1], above[0]
            alpha = (OPTIONS_TARGET_DAYS - low["days"]) / (high["days"] - low["days"])
            return {key: (1 - alpha) * low[key] + alpha * high[key] for key in ("annualized_variance", "skewness", "kurtosis")}
        return min(ordered, key=lambda item: abs(item["days"] - OPTIONS_TARGET_DAYS))

    def _historical_fallback(self, ticker: str) -> Dict[str, Any]:
        daily = self.prices[ticker].dropna().pct_change().dropna().tail(VOLATILITY_LOOKBACK_DAYS)
        return {
            "MFIV": float(daily.std(ddof=1) * math.sqrt(252)),
            "MFIS": float(stats.skew(daily)),
            "MFIK": float(stats.kurtosis(daily, fisher=False)),
            "Fuente": "Histórico (fallback)",
            "Vencimientos": 0,
        }


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 2 · MATRIZ DE COVARIANZA IMPLÍCITA
# ══════════════════════════════════════════════════════════════════════════════════════════════

class ImpliedCovarianceBuilder:
    def __init__(self, mode: str, lookback: int, shrinkage: float, benchmark: str) -> None:
        self.mode = mode
        self.lookback = lookback
        self.shrinkage = shrinkage
        self.benchmark = benchmark

    def build(self, moments: pd.DataFrame, returns: pd.DataFrame) -> pd.DataFrame:
        tickers = list(moments.index)
        sigma = moments["MFIV"].to_numpy(dtype=float)
        recent = returns[tickers].tail(self.lookback)
        if self.mode == "beta":
            if self.benchmark not in tickers:
                raise ValueError(f"El modo 'beta' requiere que {self.benchmark} esté en el universo.")
            betas = _historical_betas(recent, recent[self.benchmark]).to_numpy(dtype=float)
            market_vol = float(moments.loc[self.benchmark, "MFIV"])
            covariance = np.outer(betas, betas) * market_vol**2
            np.fill_diagonal(covariance, sigma**2)
        else:
            correlation = recent.corr(min_periods=int(self.lookback * 0.6)).to_numpy(dtype=float)
            correlation = np.nan_to_num(correlation, nan=0.0)
            np.fill_diagonal(correlation, 1.0)
            correlation = (1.0 - self.shrinkage) * correlation + self.shrinkage * np.eye(len(tickers))
            covariance = np.outer(sigma, sigma) * correlation
        return pd.DataFrame(_nearest_psd(covariance), index=tickers, columns=tickers)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 2 · VECTOR DE RETORNOS ESPERADOS CON TILT POR RIESGO DE COLA
# ══════════════════════════════════════════════════════════════════════════════════════════════

class ExpectedReturnModel:
    def __init__(self, benchmark: str) -> None:
        self.benchmark = benchmark

    def build(self, returns: pd.DataFrame, moments: pd.DataFrame) -> pd.DataFrame:
        if self.benchmark not in returns.columns:
            raise ValueError(f"El benchmark {self.benchmark} no tiene serie de retornos.")
        tickers = list(moments.index)
        recent = returns.tail(CORRELATION_LOOKBACK_DAYS)
        betas = _historical_betas(recent[tickers], recent[self.benchmark])
        mu_capm = RISK_FREE_RATE + betas * EQUITY_RISK_PREMIUM
        mu_hist = returns[tickers].mean() * 252.0
        mu_base = (1.0 - HISTORICAL_MU_BLEND) * mu_capm + HISTORICAL_MU_BLEND * mu_hist
        skew_penalty = SKEW_PENALTY * (SKEW_THRESHOLD - moments["MFIS"]).clip(lower=0.0)
        kurt_penalty = KURTOSIS_PENALTY * (moments["MFIK"] - KURTOSIS_THRESHOLD).clip(lower=0.0)
        return pd.DataFrame(
            {
                "Beta": betas,
                "Mu_CAPM": mu_capm,
                "Mu_Histórico": mu_hist,
                "Mu_Base": mu_base,
                "Penalización_Skew": skew_penalty,
                "Penalización_Kurt": kurt_penalty,
                "Mu_Ajustado": mu_base - skew_penalty - kurt_penalty,
            },
            index=tickers,
        )


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 3 · OPTIMIZADOR CUADRÁTICO CON RESTRICCIONES FACTORIALES (OPCIÓN B)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PortfolioOptimizer:
    CONSTRAINT_TOLERANCE: float = 1e-7

    def __init__(self, mu: pd.Series, covariance: pd.DataFrame, factor_matrix: pd.DataFrame, profile: ProfileConfig) -> None:
        self.logger = logging.getLogger("Optimizador")
        self.tickers: List[str] = list(mu.index)
        self.mu = mu.to_numpy(dtype=float)
        self.sigma = covariance.loc[self.tickers, self.tickers].to_numpy(dtype=float)
        self.B = factor_matrix.loc[self.tickers, list(FACTORS)].to_numpy(dtype=float)
        self.risk_aversion = profile.risk_aversion
        self.max_weight = max(profile.max_weight, 1.0 / len(self.tickers) + 1e-9)
        if self.max_weight > profile.max_weight:
            self.logger.warning("max_weight ajustado a %.4f para garantizar plena inversión.", self.max_weight)
        self.requested_targets = profile.target_vector()
        self.targets, self.target_relaxation, self.warm_start = self._feasible_targets()

    def _feasible_targets(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        n_assets, n_factors = self.B.shape
        result = linprog(
            c=np.concatenate([np.zeros(n_assets), np.ones(n_factors)]),
            A_ub=np.hstack([-self.B.T, -np.eye(n_factors)]),
            b_ub=-self.requested_targets,
            A_eq=np.concatenate([np.ones(n_assets), np.zeros(n_factors)])[None, :],
            b_eq=[1.0],
            bounds=[(0.0, self.max_weight)] * n_assets + [(0.0, None)] * n_factors,
            method="highs",
        )
        if not result.success:
            raise OptimizationError(f"Chequeo de factibilidad (LP) fallido: {result.message}")
        slack = np.where(result.x[n_assets:] > 1e-9, result.x[n_assets:], 0.0)
        if slack.sum() > 0:
            relaxed = ", ".join(f"{f}: -{s:.4f}" for f, s in zip(FACTORS, slack) if s > 0)
            self.logger.warning("Targets factoriales infactibles; relajación mínima L1 aplicada → %s", relaxed)
        effective = np.where(slack > 0, self.requested_targets - slack - 1e-5, self.requested_targets)
        return np.clip(effective, 0.0, None), slack, result.x[:n_assets]

    def utility(self, weights: np.ndarray) -> float:
        return float(self.mu @ weights - 0.5 * self.risk_aversion * weights @ self.sigma @ weights)

    def solve(self, method: str) -> OptimizationResult:
        solvers: Dict[str, Callable[[], Tuple[np.ndarray, str]]] = {
            "cvxpy": self._solve_cvxpy,
            "scipy": self._solve_scipy,
            "qubo_sa": self._solve_qubo_sa,
        }
        if method not in solvers:
            raise ValueError(f"Solver '{method}' no soportado. Opciones: {list(solvers)}")
        if method == "cvxpy" and not CVXPY_AVAILABLE:
            self.logger.warning("CVXPY no instalado; se usa SciPy SLSQP.")
            method = "scipy"
        start = time.perf_counter()
        try:
            weights, status = solvers[method]()
        except OptimizationError as exc:
            if method != "cvxpy":
                raise
            self.logger.warning("CVXPY falló (%s); reintento con SciPy SLSQP.", exc)
            method = "scipy"
            weights, status = solvers[method]()
        return self._build_result(method, weights, status, time.perf_counter() - start)

    def _solve_cvxpy(self) -> Tuple[np.ndarray, str]:
        w = cp.Variable(len(self.tickers))
        sigma = cp.psd_wrap(self.sigma) if hasattr(cp, "psd_wrap") else self.sigma
        problem = cp.Problem(
            cp.Maximize(self.mu @ w - 0.5 * self.risk_aversion * cp.quad_form(w, sigma)),
            [cp.sum(w) == 1, w >= 0, w <= self.max_weight, self.B.T @ w >= self.targets - self.CONSTRAINT_TOLERANCE],
        )
        try:
            problem.solve()
        except cp.error.SolverError as exc:
            raise OptimizationError(f"CVXPY SolverError: {exc}") from exc
        if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE) or w.value is None:
            raise OptimizationError(f"CVXPY terminó con estado '{problem.status}'")
        return np.asarray(w.value, dtype=float), str(problem.status)

    def _solve_scipy(self) -> Tuple[np.ndarray, str]:
        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1.0, "jac": lambda x: np.ones_like(x)},
            {"type": "ineq", "fun": lambda x: self.B.T @ x - (self.targets - self.CONSTRAINT_TOLERANCE), "jac": lambda x: self.B.T},
        ]
        result = minimize(
            fun=lambda x: -self.utility(x),
            x0=self.warm_start,
            jac=lambda x: -(self.mu - self.risk_aversion * self.sigma @ x),
            bounds=[(0.0, self.max_weight)] * len(self.tickers),
            constraints=constraints,
            method="SLSQP",
            options={"maxiter": 2000, "ftol": 1e-12},
        )
        if not result.success and self._max_violation(result.x) > 1e-5:
            raise OptimizationError(f"SLSQP no convergió: {result.message}")
        return np.asarray(result.x, dtype=float), "optimal" if result.success else f"aceptable ({result.message})"

    def _solve_qubo_sa(self) -> Tuple[np.ndarray, str]:
        n_assets, bits = len(self.tickers), QUBO_BITS_PER_ASSET
        n_vars = n_assets * bits
        levels = 2**bits - 1
        scale = self.max_weight / levels
        encoder = np.zeros((n_assets, n_vars))
        for asset in range(n_assets):
            encoder[asset, asset * bits: (asset + 1) * bits] = scale * 2.0 ** np.arange(bits)
        ones = np.ones(n_assets)
        quadratic = 0.5 * self.risk_aversion * self.sigma + SA_BUDGET_PENALTY * np.outer(ones, ones)
        linear = -self.mu - 2.0 * SA_BUDGET_PENALTY * ones
        qubo = encoder.T @ quadratic @ encoder
        qubo[np.diag_indices_from(qubo)] += encoder.T @ linear
        qubo = 0.5 * (qubo + qubo.T)
        diagonal = np.diag(qubo).copy()
        asset_of_var = np.repeat(np.arange(n_assets), bits)
        weight_of_var = np.tile(scale * 2.0 ** np.arange(bits), n_assets)

        def violation(exposure: np.ndarray) -> float:
            return float(np.sum(np.maximum(0.0, self.targets - exposure) ** 2))

        strict_coefficient = SA_FACTOR_PENALTY * SA_FACTOR_PENALTY_MAX_MULT

        start_levels = np.clip(np.rint(self.warm_start / scale), 0, levels).astype(int)
        state = ((start_levels[:, None] >> np.arange(bits)) & 1).reshape(-1).astype(float)
        field = qubo @ state
        exposure = self.B.T @ (encoder @ state)
        quadratic_energy = float(state @ qubo @ state)
        current_violation = violation(exposure)
        best_state = state.copy()
        best_strict_energy = quadratic_energy + strict_coefficient * current_violation
        rng = np.random.default_rng(SA_RANDOM_SEED)

        def flip_delta(j: int) -> Tuple[float, np.ndarray, float]:
            dx = 1.0 - 2.0 * state[j]
            delta_q = dx * (diagonal[j] + 2.0 * (field[j] - diagonal[j] * state[j]))
            new_exposure = exposure + self.B[asset_of_var[j]] * weight_of_var[j] * dx
            new_violation = violation(new_exposure)
            return delta_q, new_exposure, new_violation

        sample = [abs(flip_delta(int(j))[0]) for j in rng.integers(n_vars, size=min(500, 2 * n_vars))]
        t_start = max(float(np.mean(sample)), 1e-8)
        t_end = t_start * 1e-4
        flips = rng.integers(n_vars, size=SA_ITERATIONS)
        uniforms = rng.random(SA_ITERATIONS)
        accepted = 0
        for step in range(SA_ITERATIONS):
            temperature = t_start * (t_end / t_start) ** (step / max(SA_ITERATIONS - 1, 1))
            # La penalización de factibilidad se endurece junto con el enfriamiento (de SA_FACTOR_PENALTY
            # hasta el tope strict_coefficient), en vez de quedar fija: así la SA explora libremente al
            # inicio y termina forzando casi estrictamente B^T w >= target al final del recocido.
            penalty_coefficient = min(SA_FACTOR_PENALTY * (t_start / temperature), strict_coefficient)
            j = int(flips[step])
            delta_q, new_exposure, new_violation = flip_delta(j)
            delta = delta_q + penalty_coefficient * (new_violation - current_violation)
            if delta <= 0.0 or uniforms[step] < math.exp(-delta / temperature):
                dx = 1.0 - 2.0 * state[j]
                state[j] += dx
                field += qubo[:, j] * dx
                exposure, current_violation = new_exposure, new_violation
                quadratic_energy += delta_q
                accepted += 1
                strict_energy = quadratic_energy + strict_coefficient * current_violation
                if strict_energy < best_strict_energy:
                    best_strict_energy, best_state = strict_energy, state.copy()
        weights = _project_capped_simplex(encoder @ best_state, self.max_weight)
        return weights, f"SA {SA_ITERATIONS} iter · aceptación {accepted / SA_ITERATIONS:.1%} · {n_vars} qubits"

    def _max_violation(self, weights: np.ndarray) -> float:
        factor_gap = float(np.max(np.maximum(0.0, self.targets - self.B.T @ weights)))
        return max(abs(float(np.sum(weights)) - 1.0), factor_gap)

    def _build_result(self, method: str, weights: np.ndarray, status: str, runtime: float) -> OptimizationResult:
        clean = np.clip(weights, 0.0, None)
        clean[clean < 1e-6] = 0.0
        clean = clean / clean.sum()
        exposure = self.B.T @ clean
        return OptimizationResult(
            method=method,
            weights=pd.Series(clean, index=self.tickers, name="Peso"),
            expected_return=float(self.mu @ clean),
            volatility=float(math.sqrt(max(clean @ self.sigma @ clean, 0.0))),
            utility=self.utility(clean),
            factor_exposure=pd.Series(exposure, index=list(FACTORS)),
            max_factor_violation=float(np.max(np.maximum(0.0, self.targets - exposure))),
            status=status,
            runtime_seconds=runtime,
        )


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 4 · REPORTE EN CONSOLA (SIN CSV)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class ConsoleReporter:
    WIDTH: int = 110

    def table(self, title: str, frame: pd.DataFrame, floatfmt: str = ".4f", show_index: bool = True) -> None:
        print("\n" + "═" * self.WIDTH)
        print(f"  {title}")
        print("═" * self.WIDTH)
        if frame.empty:
            print("  (sin registros)")
            return
        if TABULATE_AVAILABLE:
            print(tabulate(frame, headers="keys", tablefmt="fancy_grid", floatfmt=floatfmt, showindex=show_index))
        else:
            with pd.option_context("display.max_rows", None, "display.max_columns", None, "display.width", 220, "display.float_format", "{:,.4f}".format):
                print(frame.to_string(index=show_index))

    @staticmethod
    def risk_contributions(weights: pd.Series, covariance: pd.DataFrame) -> pd.Series:
        w = weights.to_numpy(dtype=float)
        sigma = covariance.loc[weights.index, weights.index].to_numpy(dtype=float)
        total = float(w @ sigma @ w)
        return pd.Series(w * (sigma @ w) / total if total > 0 else np.zeros_like(w), index=weights.index)

    def allocation_table(self, result: OptimizationResult, universe: pd.DataFrame, moments: pd.DataFrame, mu_table: pd.DataFrame, risk: pd.Series) -> pd.DataFrame:
        active = result.weights[result.weights > 1e-4].sort_values(ascending=False).index
        return pd.DataFrame(
            {
                "Categoría": universe.loc[active, "Categoría"],
                "Peso w*": result.weights[active],
                "μ ajustado": mu_table.loc[active, "Mu_Ajustado"],
                "MFIV": moments.loc[active, "MFIV"],
                "MFIS": moments.loc[active, "MFIS"],
                "MFIK": moments.loc[active, "MFIK"],
                "Contrib. Riesgo": risk[active],
                "Fuente Momentos": moments.loc[active, "Fuente"],
            }
        )

    @staticmethod
    def factor_table(result: OptimizationResult, requested: np.ndarray, effective: np.ndarray) -> pd.DataFrame:
        achieved = result.factor_exposure.to_numpy(dtype=float)
        return pd.DataFrame(
            {
                "Target Solicitado": requested,
                "Target Efectivo": effective,
                "Real (Bᵀw*)": achieved,
                "Holgura": achieved - effective,
                "Cumple": np.where(achieved >= effective - 1e-5, "✔", "✘"),
            },
            index=list(FACTORS),
        )

    @staticmethod
    def metrics_table(result: OptimizationResult, profile: ProfileConfig) -> pd.DataFrame:
        weights = result.weights.to_numpy(dtype=float)
        sharpe = (result.expected_return - RISK_FREE_RATE) / result.volatility if result.volatility > 0 else float("nan")
        rows = {
            "Perfil": profile.name,
            "Solver": result.method,
            "Aversión al riesgo (λ)": f"{profile.risk_aversion:.2f}",
            "Retorno esperado (μᵀw)": f"{result.expected_return:.2%}",
            "Volatilidad implícita": f"{result.volatility:.2%}",
            "Sharpe implícito": f"{sharpe:.3f}",
            "Utilidad U(w)": f"{result.utility:.6f}",
            "ETFs activos": str(int((weights > 1e-4).sum())),
            "N efectivo (1/Σw²)": f"{1.0 / float(np.sum(weights**2)):.2f}",
            "Máx. violación factorial": f"{result.max_factor_violation:.2e}",
            "Estado": result.status,
            "Tiempo (s)": f"{result.runtime_seconds:.2f}",
        }
        return pd.DataFrame({"Valor": rows})


# ══════════════════════════════════════════════════════════════════════════════════════════════
# FASE 5 · DASHBOARD INTERACTIVO HTML (PLOTLY)
# ══════════════════════════════════════════════════════════════════════════════════════════════

class DashboardBuilder:
    def build(
        self,
        path: str,
        profile: ProfileConfig,
        result: OptimizationResult,
        effective_targets: np.ndarray,
        moments: pd.DataFrame,
        mu_table: pd.DataFrame,
        risk: pd.Series,
    ) -> str:
        figure = make_subplots(
            rows=2,
            cols=2,
            specs=[[{"type": "domain"}, {"type": "polar"}], [{"type": "xy"}, {"type": "xy"}]],
            subplot_titles=(
                "Asset Allocation (w*)",
                "Exposición Factorial: Target vs. Real (Bᵀw*)",
                "Riesgo vs. Retorno · MFIV (BKM) vs. μ ajustado",
                "Peso vs. Contribución al Riesgo",
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.10,
        )
        active = result.weights[result.weights > 1e-4].sort_values(ascending=False)
        self._allocation_pie(figure, active)
        self._factor_radar(figure, profile, result, effective_targets)
        self._risk_return_scatter(figure, result, moments, mu_table)
        self._risk_budget_bars(figure, active, risk)
        sharpe = (result.expected_return - RISK_FREE_RATE) / result.volatility if result.volatility > 0 else float("nan")
        figure.update_layout(
            title=dict(
                text=(
                    f"<b>Passive ETF Allocation · Perfil {profile.name}</b><br><sup>Solver: {result.method} · "
                    f"E[R] {result.expected_return:.2%} · σ implícita {result.volatility:.2%} · Sharpe {sharpe:.2f} · "
                    f"Generado {datetime.now():%Y-%m-%d %H:%M}</sup>"
                ),
                x=0.5,
            ),
            template="plotly_white",
            height=1080,
            legend=dict(orientation="h", yanchor="bottom", y=-0.08, xanchor="center", x=0.5),
            polar=dict(radialaxis=dict(range=[0, 1], tickformat=".1f")),
            barmode="group",
            margin=dict(t=120, b=90, l=60, r=40),
        )
        figure.write_html(path, include_plotlyjs=True, full_html=True, config={"displaylogo": False, "responsive": True})
        return os.path.abspath(path)

    @staticmethod
    def _allocation_pie(figure: go.Figure, active: pd.Series) -> None:
        figure.add_trace(
            go.Pie(
                labels=active.index.tolist(),
                values=active.to_numpy(),
                hole=0.45,
                sort=False,
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Peso: %{percent}<extra></extra>",
                name="Asignación",
                showlegend=False,
            ),
            row=1,
            col=1,
        )

    @staticmethod
    def _factor_radar(figure: go.Figure, profile: ProfileConfig, result: OptimizationResult, effective_targets: np.ndarray) -> None:
        theta = list(FACTORS) + [FACTORS[0]]
        series = {
            "Target solicitado": profile.target_vector(),
            "Target efectivo": effective_targets,
            "Real Bᵀw*": result.factor_exposure.to_numpy(dtype=float),
        }
        for name, values in series.items():
            figure.add_trace(
                go.Scatterpolar(
                    r=list(values) + [values[0]],
                    theta=theta,
                    fill="toself",
                    opacity=0.55 if name == "Real Bᵀw*" else 0.30,
                    name=name,
                    hovertemplate="%{theta}: %{r:.3f}<extra>" + name + "</extra>",
                ),
                row=1,
                col=2,
            )

    @staticmethod
    def _risk_return_scatter(figure: go.Figure, result: OptimizationResult, moments: pd.DataFrame, mu_table: pd.DataFrame) -> None:
        weights = result.weights.reindex(moments.index).fillna(0.0)
        sizes = 9.0 + 45.0 * weights / max(float(weights.max()), 1e-9)
        custom = [[float(weights[t]), float(moments.loc[t, "MFIK"]), str(moments.loc[t, "Fuente"])] for t in moments.index]
        figure.add_trace(
            go.Scatter(
                x=moments["MFIV"],
                y=mu_table.loc[moments.index, "Mu_Ajustado"],
                mode="markers+text",
                text=moments.index.tolist(),
                textposition="top center",
                textfont=dict(size=9),
                customdata=custom,
                marker=dict(
                    size=sizes,
                    color=moments["MFIS"],
                    colorscale="RdYlGn",
                    showscale=True,
                    colorbar=dict(title="MFIS", x=0.44, y=0.22, len=0.42, thickness=12),
                    line=dict(width=0.6, color="#333333"),
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>MFIV: %{x:.2%}<br>μ ajustado: %{y:.2%}<br>MFIS: %{marker.color:.2f}"
                    "<br>MFIK: %{customdata[1]:.2f}<br>Peso: %{customdata[0]:.2%}<br>Fuente: %{customdata[2]}<extra></extra>"
                ),
                name="ETFs del universo",
            ),
            row=2,
            col=1,
        )
        figure.add_trace(
            go.Scatter(
                x=[result.volatility],
                y=[result.expected_return],
                mode="markers",
                marker=dict(symbol="star", size=22, color="#1f2a44", line=dict(width=1, color="white")),
                name="Portafolio óptimo",
                hovertemplate="<b>Portafolio</b><br>σ: %{x:.2%}<br>E[R]: %{y:.2%}<extra></extra>",
            ),
            row=2,
            col=1,
        )
        figure.update_xaxes(title_text="Volatilidad implícita anualizada (MFIV)", tickformat=".0%", row=2, col=1)
        figure.update_yaxes(title_text="Retorno esperado ajustado (μ)", tickformat=".1%", row=2, col=1)

    @staticmethod
    def _risk_budget_bars(figure: go.Figure, active: pd.Series, risk: pd.Series) -> None:
        figure.add_trace(
            go.Bar(x=active.index.tolist(), y=active.to_numpy(), name="Peso w*", hovertemplate="%{x}: %{y:.2%}<extra>Peso</extra>"),
            row=2,
            col=2,
        )
        figure.add_trace(
            go.Bar(x=active.index.tolist(), y=risk[active.index].to_numpy(), name="Contribución al riesgo", hovertemplate="%{x}: %{y:.2%}<extra>Riesgo</extra>"),
            row=2,
            col=2,
        )
        figure.update_yaxes(tickformat=".0%", row=2, col=2)


# ══════════════════════════════════════════════════════════════════════════════════════════════
# ORQUESTADOR DEL PIPELINE
# ══════════════════════════════════════════════════════════════════════════════════════════════

class PassiveETFAllocationPipeline:
    def __init__(self) -> None:
        self.logger = logging.getLogger("Pipeline")
        self.profile = ProfileConfig.from_registry(INVESTMENT_PROFILE, PROFILES)
        self.fmp = FMPClient(FMP_API_KEY, FMP_BASE_URL, FMP_MIN_INTERVAL_SECONDS, HTTP_TIMEOUT_SECONDS, HTTP_MAX_RETRIES)
        self.polygon = (
            PolygonClient(POLYGON_API_KEY, POLYGON_BASE_URL, POLYGON_MIN_INTERVAL_SECONDS, HTTP_TIMEOUT_SECONDS, HTTP_MAX_RETRIES)
            if _is_configured_key(POLYGON_API_KEY)
            else None
        )
        self.reporter = ConsoleReporter()

    def run(self) -> OptimizationResult:
        self.logger.info("FASE 0 · Construcción del universo híbrido")
        candidates = UniverseBuilder(self.fmp, MASTER_ETF_LIST).build_candidates()
        load_list = list(dict.fromkeys([BENCHMARK_TICKER] + [etf.ticker for etf in candidates]))
        prices = MarketDataLoader(self.fmp, PRICE_HISTORY_YEARS, MIN_PRICE_OBSERVATIONS).load(load_list)
        if BENCHMARK_TICKER not in prices.columns:
            raise RuntimeError(f"No se obtuvo historial para el benchmark {BENCHMARK_TICKER}.")
        returns = prices.pct_change(fill_method=None)
        universe, dropped = RedundancyFilter(REDUNDANCY_CORRELATION_THRESHOLD, CORRELATION_LOOKBACK_DAYS, MAX_DYNAMIC_ETFS).apply(candidates, returns)
        tickers = [etf.ticker for etf in universe]
        universe_frame = pd.DataFrame(
            {
                "Nombre": [etf.name for etf in universe],
                "Categoría": [etf.category for etf in universe],
                "Clase": [etf.asset_class for etf in universe],
                "Fuente": [etf.source for etf in universe],
                "Volumen USD": [etf.dollar_volume for etf in universe],
            },
            index=tickers,
        )

        self.logger.info("FASE 1 · Matriz factorial B (FMP + técnicos)")
        factor_matrix, raw_factors = FactorModelBuilder(self.fmp, prices[tickers]).build(universe)

        self.logger.info("FASE 2 · Momentos BKM, covarianza implícita y tilt de μ")
        moments = ImpliedMomentsEngine(self.polygon, prices[tickers], RISK_FREE_RATE).compute(tickers)
        covariance = ImpliedCovarianceBuilder(COVARIANCE_MODE, CORRELATION_LOOKBACK_DAYS, CORRELATION_SHRINKAGE, BENCHMARK_TICKER).build(moments, returns)
        mu_table = ExpectedReturnModel(BENCHMARK_TICKER).build(returns, moments)

        self.logger.info("FASE 3 · Optimización cuadrática con restricciones factoriales")
        optimizer = PortfolioOptimizer(mu_table["Mu_Ajustado"], covariance, factor_matrix, self.profile)
        result = optimizer.solve(SOLVER)
        comparison = self._compare_solvers(optimizer, result) if RUN_SOLVER_COMPARISON else pd.DataFrame()

        self.logger.info("FASE 4 · Reporte en consola")
        risk = self.reporter.risk_contributions(result.weights, covariance)
        self._print_reports(universe_frame, dropped, raw_factors, factor_matrix, moments, mu_table, result, optimizer, risk, comparison)

        self.logger.info("FASE 5 · Dashboard interactivo HTML")
        output = DashboardBuilder().build(DASHBOARD_FILE, self.profile, result, optimizer.targets, moments, mu_table, risk)
        self.logger.info("Dashboard generado: %s", output)
        return result

    def _compare_solvers(self, optimizer: PortfolioOptimizer, primary: OptimizationResult) -> pd.DataFrame:
        results = [primary]
        for method in ("cvxpy", "scipy", "qubo_sa"):
            if method == primary.method or (method == "cvxpy" and not CVXPY_AVAILABLE):
                continue
            try:
                results.append(optimizer.solve(method))
            except OptimizationError as exc:
                self.logger.warning("Solver %s falló en la comparación: %s", method, exc)
        return pd.DataFrame(
            {
                "E[R]": [r.expected_return for r in results],
                "σ implícita": [r.volatility for r in results],
                "Utilidad": [r.utility for r in results],
                "Máx. violación": [r.max_factor_violation for r in results],
                "ETFs activos": [int((r.weights > 1e-4).sum()) for r in results],
                "Tiempo (s)": [r.runtime_seconds for r in results],
                "Estado": [r.status for r in results],
            },
            index=[r.method for r in results],
        )

    def _print_reports(
        self,
        universe_frame: pd.DataFrame,
        dropped: pd.DataFrame,
        raw_factors: pd.DataFrame,
        factor_matrix: pd.DataFrame,
        moments: pd.DataFrame,
        mu_table: pd.DataFrame,
        result: OptimizationResult,
        optimizer: PortfolioOptimizer,
        risk: pd.Series,
        comparison: pd.DataFrame,
    ) -> None:
        composition = universe_frame.groupby(["Fuente", "Categoría"]).size().rename("N° ETFs").to_frame()
        self.reporter.table("UNIVERSO HÍBRIDO · COMPOSICIÓN", composition)
        self.reporter.table("UNIVERSO HÍBRIDO · ETFs DESCARTADOS (réplicas / cupo)", dropped, show_index=False)
        self.reporter.table("FASE 1 · MÉTRICAS CRUDAS (fundamentales agregados y técnicos)", raw_factors)
        self.reporter.table("FASE 1 · MATRIZ DE CARGAS FACTORIALES B (0-1)", factor_matrix, floatfmt=".3f")
        self.reporter.table("FASE 2 · MOMENTOS IMPLÍCITOS BKM (MFIV / MFIS / MFIK)", moments)
        self.reporter.table("FASE 2 · VECTOR μ Y TILT POR RIESGO DE COLA", mu_table)
        self.reporter.table("FASE 3 · PESOS ÓPTIMOS w* (activos)", self.reporter.allocation_table(result, universe_frame, moments, mu_table, risk))
        self.reporter.table("FASE 3 · EXPOSICIÓN FACTORIAL: DESEADA vs. LOGRADA", self.reporter.factor_table(result, optimizer.requested_targets, optimizer.targets))
        self.reporter.table("FASE 3 · MÉTRICAS DEL PORTAFOLIO", self.reporter.metrics_table(result, self.profile))
        if not comparison.empty:
            self.reporter.table("FASE 3 · COMPARACIÓN DE SOLVERS (QP vs. QUBO/SA)", comparison, floatfmt=".5f")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════════════════════

def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)-14s | %(message)s",
        datefmt="%H:%M:%S",
    )


def validate_configuration() -> None:
    if not _is_configured_key(FMP_API_KEY):
        raise ValueError("Configura FMP_API_KEY (variable de entorno o bloque de parámetros editables).")
    if INVESTMENT_PROFILE not in PROFILES:
        raise ValueError(f"INVESTMENT_PROFILE inválido: {INVESTMENT_PROFILE}")
    if not 0 < OPTIONS_MIN_DAYS <= OPTIONS_TARGET_DAYS <= OPTIONS_MAX_DAYS:
        raise ValueError("Se requiere OPTIONS_MIN_DAYS <= OPTIONS_TARGET_DAYS <= OPTIONS_MAX_DAYS.")
    if not 0.0 <= CORRELATION_SHRINKAGE <= 1.0 or not 0.0 <= HISTORICAL_MU_BLEND <= 1.0:
        raise ValueError("CORRELATION_SHRINKAGE y HISTORICAL_MU_BLEND deben estar en [0, 1].")


def main() -> int:
    configure_logging(LOG_LEVEL)
    logger = logging.getLogger("Main")
    try:
        validate_configuration()
        PassiveETFAllocationPipeline().run()
    except APIAuthorizationError as exc:
        logger.critical("Error de autorización con el proveedor de datos: %s", exc)
        return 2
    except (APIError, OptimizationError, ValueError, RuntimeError) as exc:
        logger.critical("Ejecución abortada: %s", exc)
        return 1
    except KeyboardInterrupt:
        logger.warning("Ejecución interrumpida por el usuario.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())

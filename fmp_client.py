"""Cliente HTTP compartido para la API 'stable' de Financial Modeling Prep.

Lo usan 'US Asset Manager.py' y 'Corp_FR_Optimization.py'. Aquí vive solo el transporte (throttling,
reintentos con backoff, caché, detección de errores de plan); los métodos de dominio de cada pipeline
(screener de ETFs, estados financieros, etc.) viven en cada script como subclase.

Los errores se señalan con excepciones (APIError / APIAuthorizationError). Quien prefiera un resultado
tolerante (None ante fallo) lo envuelve, como hace Corp_FR_Optimization.py.
"""
from __future__ import annotations

import logging
import math
import time
from typing import Any, Dict, List, Optional, Tuple

import requests


class APIError(Exception):
    """Error genérico de comunicación con un proveedor de datos."""


class APIAuthorizationError(APIError):
    """Clave inválida o endpoint no incluido en el plan contratado."""


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


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
        self.n_calls: int = 0  # intentos HTTP, incluidos los reintentos

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request_ts = time.monotonic()
        self.n_calls += 1

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
                self.logger.warning("%s %s: HTTP %s, reintento %d/%d", self.provider, endpoint, status, attempt, self.max_retries)
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

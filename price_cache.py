"""Caché por ticker de cierres ajustados (dividendos + splits) y fuente Yahoo Finance.

Por qué existe: ``MarketDataLoader.load`` bajaba 3 años de precios de FMP por candidato en cada corrida. Aquí cada
ticker se guarda en ``<dir>/<SIMBOLO_YAHOO>.csv`` y, en las corridas siguientes, solo se descarga el tramo que falta.

Formato del archivo (CSV legible, sin dependencias extra como pyarrow)::

    # covered_from=2023-10-18        <- inicio de la ventana pedida que ya quedó cubierta (un ETF joven empieza después)
    # source=yahoo
    date,adj_close
    2023-10-18,412.31
    ...

Ubicación por defecto: ``/workspace/pipeline/state/prices`` (junto al resto del estado del pipeline; se cambia con
``USAA_PRICE_CACHE_DIR``; ``USAA_PRICE_CACHE=off`` la desactiva). El nombre del archivo usa el símbolo de Yahoo
(``BRK-B``), igual que ``Portfolio-Manager/tickers.to_yahoo``. No se reutiliza ``PM_SHARED_MARKET_CACHE`` de
Portfolio-Manager: ese caché es de un solo día, guarda DataFrames en pickle con claves por argumentos de
``Ticker.history`` y está pensado para el lote 12:00 (VIX/GEX), no para historiales de varios años con descarga incremental.

Cierre ajustado: ``adj_close`` está ajustado hacia atrás por dividendos y splits (retorno total), igual que
``adjClose`` del endpoint ``historical-price-eod/dividend-adjusted`` de FMP que usaba el código. Como cada dividendo
reescala TODO el historial anterior por un factor constante, anexar solo los días nuevos mezclaría dos bases. Por eso
cada actualización vuelve a bajar una ventana de solape (``OVERLAP_DAYS``), compara el primer día del solape con lo
guardado y, si difieren, reescala el tramo guardado anterior por ese cociente. Si el cociente es absurdo o el caché no
cubre la ventana pedida, se descarta y se baja todo de nuevo.
"""
from __future__ import annotations

import io
import logging
import os
import re
import tempfile
import time
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from typing import Callable, Optional

import pandas as pd
from zoneinfo import ZoneInfo

DEFAULT_CACHE_DIR = "/workspace/pipeline/state/prices"
CACHE_DIR_ENV = "USAA_PRICE_CACHE_DIR"
CACHE_SWITCH_ENV = "USAA_PRICE_CACHE"  # "off"/"0"/"false"/"no" la desactiva
OVERLAP_DAYS = 7  # calendario: cubre varios cierres ya guardados para detectar reajustes por dividendo/split
RESCALE_TOLERANCE = 1e-9  # cocientes dentro de 1±tol se consideran "sin cambio" (ruido de coma flotante)
RESCALE_LIMITS = (0.2, 5.0)  # un cociente fuera de este rango no es un dividendo: se baja todo de nuevo
COVERAGE_SLACK_DAYS = 5  # el caché "cubre" el inicio pedido si empieza a lo sumo esto después (fines de semana/festivos)
NEW_YORK = ZoneInfo("America/New_York")
MARKET_CLOSE_SETTLED = dtime(16, 30)  # tras el cierre de NYSE (16:00 ET) Yahoo ya publica el ajustado definitivo
MAX_STALE_DAYS = 5  # si la descarga falla, se usa el caché solo si su último cierre es tan reciente

Fetcher = Callable[[str, date, date], pd.Series]  # (ticker, desde, hasta inclusive) -> cierre ajustado

log = logging.getLogger("PrecioCache")


def to_yahoo_symbol(ticker: str) -> str:
    """Símbolo de Yahoo: ``BRK.B`` -> ``BRK-B``. Los sufijos de bolsa (``RY.TO``) se conservan."""
    text = str(ticker).strip().upper()
    match = re.fullmatch(r"([A-Z0-9]+)\.([A-Z])", text)  # clase de acciones: una sola letra tras el punto
    return f"{match.group(1)}-{match.group(2)}" if match else text


def cache_dir_from_env(env: Optional[dict] = None) -> Optional[Path]:
    """Directorio del caché según el entorno; ``None`` si está desactivado."""
    environment = os.environ if env is None else env
    if str(environment.get(CACHE_SWITCH_ENV, "")).strip().lower() in {"off", "0", "false", "no"}:
        return None
    return Path(str(environment.get(CACHE_DIR_ENV) or DEFAULT_CACHE_DIR)).expanduser()


PRICE_SOURCE_ENV = "USAA_PRICE_SOURCE"
KNOWN_SOURCES = ("yahoo", "fmp")


def resolve_price_sources(env: Optional[dict] = None) -> tuple[str, ...]:
    """Orden de fuentes de precio: ``USAA_PRICE_SOURCE`` (p. ej. ``yahoo,fmp`` o ``fmp``); por defecto Yahoo y FMP de respaldo."""
    raw = str((os.environ if env is None else env).get(PRICE_SOURCE_ENV, "") or "yahoo,fmp")
    names = tuple(dict.fromkeys(part.strip().lower() for part in raw.split(",") if part.strip()))
    unknown = [name for name in names if name not in KNOWN_SOURCES]
    if unknown or not names:
        raise ValueError(f"{PRICE_SOURCE_ENV}={raw!r} inválido; use una lista de {', '.join(KNOWN_SOURCES)}.")
    return names


def _normalize(series: pd.Series, name: str) -> pd.Series:
    """Serie float con índice de fechas naive, ordenado, sin duplicados ni NaN ni precios <= 0."""
    if series is None or len(series) == 0:
        return pd.Series(dtype=float, name=name)
    index = pd.DatetimeIndex(pd.to_datetime(series.index))
    if index.tz is not None:
        index = index.tz_localize(None)
    clean = pd.Series(pd.to_numeric(series.to_numpy(), errors="coerce"), index=index.normalize(), name=name)
    clean = clean[clean.notna() & (clean > 0)].sort_index()
    return clean[~clean.index.duplicated(keep="last")]


def _drop_open_session(series: pd.Series, now: Optional[datetime] = None) -> pd.Series:
    """Quita la barra de hoy si la bolsa de NY aún no cerró: Yahoo la devuelve con el precio en vivo y FMP solo
    entregaba cierres completos. La siguiente corrida la repone (la ventana de solape la vuelve a bajar)."""
    if series.empty:
        return series
    moment = (now or datetime.now(NEW_YORK)).astimezone(NEW_YORK)
    if moment.time() < MARKET_CLOSE_SETTLED:
        return series[series.index < pd.Timestamp(moment.date())]
    return series


def fetch_yahoo_adjusted_close(
    symbol: str, start: date, end: date, *, retries: int = 3, sleep: Callable[[float], None] = time.sleep,
) -> pd.Series:
    """Cierre ajustado (dividendos + splits) de Yahoo entre ``start`` y ``end`` inclusive. Vacío si no hay datos.

    Usa ``auto_adjust=False`` y la columna ``Adj Close`` (misma base que el ``adjClose`` de FMP). Levanta la última
    excepción si todos los intentos fallan; una respuesta vacía NO es una excepción (ticker sin historial).
    """
    import yfinance as yf  # import perezoso: el módulo se puede importar sin yfinance (p. ej. en tests)

    yahoo_symbol = to_yahoo_symbol(symbol)
    last_error: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            # 'end' de yfinance es exclusivo: se suma un día para incluir el cierre de hoy.
            frame = yf.Ticker(yahoo_symbol).history(
                start=start.isoformat(), end=(end + timedelta(days=1)).isoformat(),
                interval="1d", auto_adjust=False, actions=False, raise_errors=False,
            )
            if frame is None or frame.empty or "Adj Close" not in frame.columns:
                return pd.Series(dtype=float, name=symbol)
            return _drop_open_session(_normalize(frame["Adj Close"], symbol))
        except Exception as exc:  # noqa: BLE001 - yfinance lanza tipos muy variados (red, JSON, rate limit)
            last_error = exc
            if attempt < retries:
                sleep(min(2.0 ** attempt, 10.0))
    assert last_error is not None
    raise last_error


class PriceCache:
    """Caché CSV por ticker con descarga incremental. ``directory=None`` desactiva lectura y escritura."""

    def __init__(self, directory: Optional[os.PathLike | str]) -> None:
        self.directory = Path(directory) if directory else None
        self.stats = {"incremental": 0, "full": 0, "stale": 0, "rescaled": 0}

    # ── archivo ──────────────────────────────────────────────────────────────────
    def path(self, ticker: str) -> Optional[Path]:
        if self.directory is None:
            return None
        return self.directory / f"{re.sub(r'[^A-Za-z0-9_.-]+', '_', to_yahoo_symbol(ticker))}.csv"

    def read(self, ticker: str) -> tuple[pd.Series, Optional[date]]:
        """(serie guardada, covered_from). Un archivo ilegible cuenta como caché vacío."""
        path = self.path(ticker)
        if path is None or not path.is_file():
            return pd.Series(dtype=float, name=ticker), None
        try:
            text = path.read_text(encoding="utf-8")
            covered: Optional[date] = None
            match = re.search(r"^# covered_from=(\d{4}-\d{2}-\d{2})\s*$", text, flags=re.M)
            if match:
                covered = date.fromisoformat(match.group(1))
            frame = pd.read_csv(io.StringIO(text), comment="#", parse_dates=["date"])
            return _normalize(pd.Series(frame["adj_close"].to_numpy(), index=frame["date"]), ticker), covered
        except Exception as exc:  # noqa: BLE001 - archivo corrupto: se ignora y se vuelve a bajar
            log.warning("Caché ilegible para %s (%s); se descarga de nuevo.", ticker, exc)
            return pd.Series(dtype=float, name=ticker), None

    def write(self, ticker: str, series: pd.Series, covered_from: date, source: str) -> None:
        path = self.path(ticker)
        if path is None or series.empty:
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            body = pd.DataFrame({"date": series.index.strftime("%Y-%m-%d"), "adj_close": series.to_numpy()})
            text = f"# covered_from={covered_from.isoformat()}\n# source={source}\n" + body.to_csv(index=False)
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_", suffix=".csv")
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            os.replace(tmp, path)
        except OSError as exc:  # un caché que no puede escribir nunca rompe la corrida
            log.warning("No se pudo escribir el caché de %s: %s", ticker, exc)

    # ── lógica incremental ───────────────────────────────────────────────────────
    @staticmethod
    def _first_with_data(
        ticker: str, start: date, end: date, fetchers: list[tuple[str, Fetcher]], errors: list[str],
    ) -> tuple[pd.Series, str]:
        """Primera fuente de la lista que devuelve datos para [start, end]; ``(vacía, "")`` si ninguna."""
        for name, fetch in fetchers:
            try:
                series = _normalize(fetch(ticker, start, end), ticker)
            except Exception as exc:  # noqa: BLE001 - se prueba la siguiente fuente
                errors.append(f"{name}: {exc}")
                continue
            if not series.empty:
                return series, name
            errors.append(f"{name}: sin datos")
        return pd.Series(dtype=float, name=ticker), ""

    def get(self, ticker: str, start: date, end: date, fetchers: list[tuple[str, Fetcher]]) -> tuple[pd.Series, str]:
        """Cierre ajustado de ``ticker`` en [start, end] y la fuente usada (``yahoo``/``fmp``/... o ``cache``).

        ``fetchers`` es una lista ordenada ``(nombre, fn(ticker, desde, hasta) -> Serie)``: se prueba cada una hasta
        que una devuelva datos. Si todas fallan o vienen vacías, se devuelve el caché solo si cubre la ventana y su
        último cierre es reciente (``MAX_STALE_DAYS``); si no, una serie vacía.
        """
        cached, covered = self.read(ticker)
        covers_start = covered is not None and not cached.empty and covered <= start + timedelta(days=COVERAGE_SLACK_DAYS)
        fetch_from = max(start, cached.index[-1].date() - timedelta(days=OVERLAP_DAYS)) if covers_start else start

        errors: list[str] = []
        new, used = self._first_with_data(ticker, fetch_from, end, fetchers, errors)
        if new.empty:
            if covers_start and (end - cached.index[-1].date()).days <= MAX_STALE_DAYS:
                self.stats["stale"] += 1
                log.warning("%s: sin descarga nueva (%s); se usa el caché hasta %s.", ticker, "; ".join(errors), cached.index[-1].date())
                return cached.loc[cached.index >= pd.Timestamp(start)], "cache"
            return pd.Series(dtype=float, name=ticker), ""

        merged = self._merge(ticker, cached, new) if covers_start else new
        if merged is None:  # solape incoherente: descartar el caché y bajar la ventana completa
            merged, used = self._first_with_data(ticker, start, end, fetchers, errors)
            covers_start = False
            if merged.empty:
                return pd.Series(dtype=float, name=ticker), ""
        self.stats["incremental" if covers_start else "full"] += 1
        self.write(ticker, merged, min(start, covered) if (covers_start and covered) else start, used)
        return merged.loc[merged.index >= pd.Timestamp(start)], used

    def _merge(self, ticker: str, cached: pd.Series, new: pd.Series) -> Optional[pd.Series]:
        """Une lo guardado con la descarga de solape. ``None`` si no se puede verificar/convertir la base de ajuste."""
        anchor = new.index[0]
        if anchor <= cached.index[0]:
            return new  # la descarga ya cubre todo lo guardado
        shared = cached.index.intersection(new.index)
        if len(shared) == 0:
            return None  # sin solape: no hay forma de comprobar que ambos tramos usan la misma base
        reference = shared[0]
        ratio = float(new.loc[reference] / cached.loc[reference])
        if not (RESCALE_LIMITS[0] <= ratio <= RESCALE_LIMITS[1]):
            log.warning("%s: cociente de reajuste %.4f fuera de rango; se vuelve a bajar todo.", ticker, ratio)
            return None
        old_part = cached[cached.index < anchor]
        if abs(ratio - 1.0) > RESCALE_TOLERANCE:
            old_part = old_part * ratio  # un dividendo/split reescala todo el pasado por un factor constante
            self.stats["rescaled"] += 1
            log.info("%s: historial reescalado x%.8f (dividendo/split en la ventana de solape).", ticker, ratio)
        return pd.concat([old_part, new]).sort_index()

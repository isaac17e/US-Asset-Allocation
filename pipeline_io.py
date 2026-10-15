"""Atomic JSON export for the shared pipeline contract (v1).

UTF-8, indent=2. Each file is written to ``<path>.tmp`` and then ``os.replace``.
Timestamps are ISO 8601 with a numeric offset in America/Bogota.
If the output directory cannot be created or written, print a warning and
return; these functions do not raise.
"""

from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from typing import Any, Mapping, Sequence
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo("America/Bogota")
RISK_PROFILE_NAMES = ("conservador", "moderado", "agresivo")
_WEIGHT_FLOOR = Decimal("1e-6")


def now_bogota(moment: datetime | None = None) -> datetime:
    """Current time in America/Bogota, or ``moment`` converted to that zone.

    A naive ``moment`` is read as a Bogotá wall time (not as the host local time).
    """
    if moment is None:
        return datetime.now(BOGOTA)
    if moment.tzinfo is None:
        return moment.replace(tzinfo=BOGOTA)
    return moment.astimezone(BOGOTA)


def iso_bogota(moment: datetime | None = None) -> str:
    """ISO 8601 with seconds and offset, e.g. ``2026-10-05T16:40:12-05:00``."""
    return now_bogota(moment).isoformat(timespec="seconds")


def stamp_bogota(moment: datetime | None = None) -> str:
    """``YYYYMMDDTHHMMSS`` in America/Bogota, for timestamped filenames."""
    return now_bogota(moment).strftime("%Y%m%dT%H%M%S")


def resolve_risk_free_rate(default: float, env: Mapping[str, str] | None = None) -> float:
    """Annual risk-free rate (decimal): ``RISK_FREE_RATE`` when set, else ``default``.

    Read once at startup. A non-number or a value outside ``0 <= rf < 0.5``
    raises ``ValueError`` (``0.052`` is 5.2%; ``5.2`` is rejected).
    """
    raw = (os.environ if env is None else env).get("RISK_FREE_RATE")
    if raw is None or not str(raw).strip():
        return float(default)
    try:
        rate = float(str(raw).strip())
    except ValueError:
        raise ValueError(
            f"RISK_FREE_RATE is not a number: {raw!r}. Use an annual decimal, e.g. 0.052."
        ) from None
    if not math.isfinite(rate) or not 0.0 <= rate < 0.5:
        raise ValueError(
            f"RISK_FREE_RATE out of range: {raw!r}. Expected 0 <= rf < 0.5 "
            "(annual decimal: 0.052 is 5.2%)."
        )
    return rate


HORIZON_MIN_DAYS = 7
HORIZON_MAX_DAYS = 400
# Same conventions as risk_estimators.to_years: dte is calendar days over 365,
# months over 12, so 1 month = 365 / 12 calendar days.
_CALENDAR_DAYS_PER_YEAR = 365.0
_MONTHS_PER_YEAR = 12.0


def months_to_days(months: float) -> int:
    """Calendar days (nearest integer) of ``months``: ``months / 12 * 365``."""
    return int(math.floor(float(months) / _MONTHS_PER_YEAR * _CALENDAR_DAYS_PER_YEAR + 0.5))


def _horizon_number(raw: Any, name: str, source: str) -> float:
    if isinstance(raw, bool):
        raise ValueError(f"{name} ({source}) is not a number: {raw!r}.")
    try:
        value = float(str(raw).strip()) if isinstance(raw, str) else float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{name} ({source}) is not a number: {raw!r}.") from None
    if not math.isfinite(value):
        raise ValueError(f"{name} ({source}) is not a finite number: {raw!r}.")
    return value


def _horizon_from_source(
    days_raw: Any, months_raw: Any, days_name: str, months_name: str, source: str,
) -> int | None:
    days_set = days_raw is not None and str(days_raw).strip() != ""
    months_set = months_raw is not None and str(months_raw).strip() != ""
    days = months = None
    if days_set:
        value = _horizon_number(days_raw, days_name, source)
        if value != int(value):
            raise ValueError(f"{days_name} ({source}) must be a whole number of days: {days_raw!r}.")
        days = int(value)
    if months_set:
        months = months_to_days(_horizon_number(months_raw, months_name, source))
    if days is not None and months is not None and days != months:
        raise ValueError(
            f"{days_name}={days_raw!r} and {months_name}={months_raw!r} disagree in {source} "
            f"({months_raw!r} months = {months} days). Set only one."
        )
    return days if days is not None else months


def resolve_horizon_days(
    default: int,
    env: Mapping[str, str] | None = None,
    inputs: Mapping[str, Any] | None = None,
) -> int:
    """Portfolio horizon in calendar days.

    Precedence: ``inputs`` (``horizon_days`` / ``horizon_months`` of an input
    file, when the caller has one) beats env (``USAA_HORIZON_DAYS`` /
    ``USAA_HORIZON_MONTHS``), and both beat ``default``. Months convert as
    ``months / 12 * 365`` calendar days (the ``to_years`` convention), rounded
    to the nearest day. Within one source, days and months must agree if both
    are given. The result must be a whole number in 7..400 days; anything else
    raises ``ValueError``. ``default`` is returned unchanged when nothing is set.
    """
    environment = os.environ if env is None else env
    chosen: int | None = None
    if inputs:
        chosen = _horizon_from_source(
            inputs.get("horizon_days"), inputs.get("horizon_months"),
            "horizon_days", "horizon_months", "input file",
        )
    if chosen is None:
        chosen = _horizon_from_source(
            environment.get("USAA_HORIZON_DAYS"), environment.get("USAA_HORIZON_MONTHS"),
            "USAA_HORIZON_DAYS", "USAA_HORIZON_MONTHS", "environment",
        )
    if chosen is None:
        chosen = int(default)
    if not HORIZON_MIN_DAYS <= chosen <= HORIZON_MAX_DAYS:
        raise ValueError(
            f"Portfolio horizon out of range: {chosen} days. "
            f"Expected {HORIZON_MIN_DAYS}..{HORIZON_MAX_DAYS} calendar days "
            "(USAA_HORIZON_DAYS or USAA_HORIZON_MONTHS)."
        )
    return chosen


def horizon_option_window(
    horizon_days: int, default_horizon: int, default_min: int, default_max: int,
) -> tuple[int, int]:
    """Expiry window (min, max DTE) scaled with the horizon.

    The window keeps the proportions of the defaults around their horizon
    (30/90 around 60 = 0.5x/1.5x). At ``default_horizon`` it returns the
    defaults untouched.
    """
    if horizon_days == default_horizon:
        return int(default_min), int(default_max)
    scale = horizon_days / float(default_horizon)
    low = max(1, int(math.floor(default_min * scale + 0.5)))
    high = max(low, int(math.floor(default_max * scale + 0.5)))
    return min(low, horizon_days), max(high, horizon_days)


def _cli_risk_profile(argv: Sequence[str]) -> str | None:
    for i, arg in enumerate(argv):
        if arg == "--risk-profile":
            if i + 1 >= len(argv) or str(argv[i + 1]).startswith("-"):
                raise ValueError("--risk-profile needs a value: conservador, moderado or agresivo")
            return argv[i + 1]
        if arg.startswith("--risk-profile="):
            return arg.split("=", 1)[1]
    return None


def resolve_risk_profile(
    default: str,
    allowed: Sequence[str] = RISK_PROFILE_NAMES,
    argv: Sequence[str] | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    """Profile name: ``--risk-profile`` beats ``RISK_PROFILE``, and both beat ``default``.

    Same convention as AM-PM-Architecture. Case and surrounding spaces are ignored.
    Only ``--risk-profile`` is looked for, so unrelated argv (unittest, pytest) is safe.
    A name outside ``allowed`` raises ``ValueError``.
    """
    chosen = _cli_risk_profile(sys.argv[1:] if argv is None else argv)
    if chosen is None:
        chosen = (os.environ if env is None else env).get("RISK_PROFILE")
    if chosen is None or not str(chosen).strip():
        chosen = default
    name = str(chosen).strip().lower()
    allowed = tuple(allowed)
    if name not in allowed:
        raise ValueError(
            f"invalid risk profile: {chosen!r}. Use one of: {', '.join(allowed)} "
            "(--risk-profile or RISK_PROFILE)."
        )
    return name


def normalize_weights(
    weights: Mapping[str, float],
    decimals: int = 6,
) -> tuple[list[str], dict[str, float]]:
    """Drop weights ``< 1e-6``, renormalize, and round so they sum to 1.

    Tickers are ordered by weight descending, then by ticker. Rounded weights
    sum to 1 at ``decimals`` decimal places. Returns ``([], {})`` when nothing
    remains.
    """
    scale = Decimal(10) ** decimals
    kept: list[tuple[str, Decimal]] = []
    for ticker, raw in weights.items():
        try:
            value = Decimal(str(float(raw)))
        except (TypeError, ValueError, ArithmeticError):
            continue
        if not value.is_finite() or value < _WEIGHT_FLOOR:
            continue
        kept.append((str(ticker), value))
    if not kept:
        return [], {}
    total = sum((value for _, value in kept), start=Decimal(0))
    if total <= 0:
        return [], {}

    pieces: list[list[Any]] = []
    for ticker, value in kept:
        exact = (value / total) * scale
        base = int(exact.to_integral_value(rounding=ROUND_FLOOR))
        pieces.append([ticker, base, exact - Decimal(base)])
    leftover = int(scale) - sum(item[1] for item in pieces)
    pieces.sort(key=lambda item: (-item[2], item[0]))
    count = len(pieces)
    cursor = 0
    while leftover > 0 and count and cursor <= int(scale) + count:
        pieces[cursor % count][1] += 1
        leftover -= 1
        cursor += 1
    while leftover < 0 and count:
        donor = max(range(count), key=lambda i: (pieces[i][1], pieces[i][0]))
        if pieces[donor][1] <= 0:
            break
        pieces[donor][1] -= 1
        leftover += 1

    units = {ticker: units_i for ticker, units_i, _ in pieces if units_i > 0}
    if not units:
        return [], {}
    drift = int(scale) - sum(units.values())
    if drift:
        top = max(units, key=lambda ticker: (units[ticker], ticker))
        if units[top] + drift <= 0:
            return [], {}
        units[top] += drift
    ordered = sorted(units, key=lambda ticker: (-units[ticker], ticker))
    return ordered, {ticker: float(Decimal(units[ticker]) / scale) for ticker in ordered}


def _warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr)


def _dumps(payload: Any) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def atomic_write_json(path: str | os.PathLike[str], payload: Any) -> bool:
    """Write one JSON file atomically. Return False (and warn) on failure."""
    try:
        text = _dumps(payload)
    except (TypeError, ValueError) as exc:
        _warn(f"no se pudo serializar el JSON del pipeline ({path}): {exc}")
        return False
    destination = Path(path)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        _warn(f"no se pudo crear el directorio de salida {destination.parent}: {exc}")
        return False
    return _atomic_write_text(destination, text)


def write_json_files(
    directory: str | os.PathLike[str],
    filenames: list[str],
    payload: Any,
) -> list[str]:
    """Write the same JSON to each filename. Return the paths that were written.

    Never raises. A failure to create ``directory`` warns once and writes nothing.
    """
    try:
        text = _dumps(payload)
    except (TypeError, ValueError) as exc:
        _warn(f"no se pudo serializar el JSON del pipeline ({directory}): {exc}")
        return []
    folder = Path(directory)
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        _warn(f"no se pudo crear el directorio de salida {folder}: {exc}")
        return []
    written: list[str] = []
    for name in filenames:
        path = folder / name
        if _atomic_write_text(path, text):
            written.append(str(path))
    return written


def _atomic_write_text(path: Path, text: str) -> bool:
    temporary = Path(str(path) + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        return True
    except OSError as exc:
        _warn(f"no se pudo escribir {path}: {exc}")
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        return False

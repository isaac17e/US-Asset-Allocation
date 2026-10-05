"""Atomic JSON export for the shared pipeline contract (v1).

UTF-8, indent=2. Each file is written to ``<path>.tmp`` and then ``os.replace``.
Timestamps are ISO 8601 with a numeric offset in America/Bogota.
If the output directory cannot be created or written, print a warning and
return; these functions do not raise.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from typing import Any, Mapping
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo("America/Bogota")
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

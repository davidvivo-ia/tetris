"""Puntuación BPS (escala Nintendo) que usaba el original."""

from __future__ import annotations

from typing import Final

_LINE_POINTS: Final[dict[int, int]] = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
_LINES_PER_LEVEL: Final[int] = 10
_MAX_LEVEL: Final[int] = 20


def score_for_lines(lines_cleared: int, level: int) -> int:
    """Puntos por limpiar `lines_cleared` líneas en `level`.

    Args:
        lines_cleared: 0..4.
        level: nivel actual, mínimo 1.

    Returns:
        Puntos otorgados según tabla BPS × nivel.

    Raises:
        ValueError: si los argumentos quedan fuera de rango.
    """
    if lines_cleared < 0 or lines_cleared > 4:
        raise ValueError(f"lines_cleared fuera de rango: {lines_cleared}")
    if level < 1:
        raise ValueError(f"level debe ser >= 1: {level}")
    return _LINE_POINTS[lines_cleared] * level


def level_for_total_lines(total_lines: int) -> int:
    """Nivel correspondiente a haber completado `total_lines` en total."""
    if total_lines < 0:
        raise ValueError(f"total_lines no puede ser negativo: {total_lines}")
    return min(_MAX_LEVEL, 1 + total_lines // _LINES_PER_LEVEL)

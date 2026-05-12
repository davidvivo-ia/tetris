"""Las siete piezas canónicas del Tetris."""

from __future__ import annotations

from enum import StrEnum


class TetrominoKind(StrEnum):
    """Las siete piezas estándar.

    Los nombres coinciden con la convención universal del juego (I, O, T,
    S, Z, J, L) — la misma que el original BASIC numeraba `K = 1..7`.
    """

    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


ALL_KINDS: tuple[TetrominoKind, ...] = tuple(TetrominoKind)
"""Tupla determinista con todas las piezas en orden canónico."""

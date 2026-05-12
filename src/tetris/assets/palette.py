"""Paleta y glifos del sistema visual Phosphor 2026."""

from __future__ import annotations

from typing import Final

from tetris.domain.tetromino import TetrominoKind

BACKGROUND: Final[str] = "#0B0F0A"
SURFACE: Final[str] = "#11160F"
SURFACE_ALT: Final[str] = "#1A2018"
PRIMARY: Final[str] = "#7FFFB2"
ACCENT: Final[str] = "#E5C100"
MUTED: Final[str] = "#4A5A4A"
DANGER: Final[str] = "#FF5C7A"

PIECE_COLOR: Final[dict[TetrominoKind, str]] = {
    TetrominoKind.I: "#5BE7F2",
    TetrominoKind.O: "#F5D44A",
    TetrominoKind.T: "#B271E3",
    TetrominoKind.S: "#6BE07F",
    TetrominoKind.Z: "#F26060",
    TetrominoKind.J: "#5C7BFF",
    TetrominoKind.L: "#F08A3A",
}

PIECE_GLYPH: Final[dict[TetrominoKind, str]] = {
    TetrominoKind.I: "I",
    TetrominoKind.O: "O",
    TetrominoKind.T: "T",
    TetrominoKind.S: "S",
    TetrominoKind.Z: "Z",
    TetrominoKind.J: "J",
    TetrominoKind.L: "L",
}

CELL_FULL: Final[str] = "██"
CELL_EMPTY: Final[str] = "  "
CELL_GHOST: Final[str] = "▒▒"

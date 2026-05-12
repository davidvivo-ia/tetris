"""Tabla de formas y rotaciones de las siete piezas.

Cada pieza tiene cuatro orientaciones, almacenadas como tuplas de
celdas `(x, y)` con origen en la esquina superior-izquierda del
bounding-box 4×4. Igual que el original BASIC, pero centradas para
evitar el offset visual de S/Z (B9 en el análisis arqueológico).
"""

from __future__ import annotations

from typing import Final

from tetris.domain.tetromino import TetrominoKind

Cell = tuple[int, int]
RotationShapes = tuple[
    tuple[Cell, ...],
    tuple[Cell, ...],
    tuple[Cell, ...],
    tuple[Cell, ...],
]


_SHAPES: Final[dict[TetrominoKind, RotationShapes]] = {
    TetrominoKind.I: (
        ((0, 1), (1, 1), (2, 1), (3, 1)),
        ((2, 0), (2, 1), (2, 2), (2, 3)),
        ((0, 2), (1, 2), (2, 2), (3, 2)),
        ((1, 0), (1, 1), (1, 2), (1, 3)),
    ),
    TetrominoKind.O: (
        ((1, 0), (2, 0), (1, 1), (2, 1)),
        ((1, 0), (2, 0), (1, 1), (2, 1)),
        ((1, 0), (2, 0), (1, 1), (2, 1)),
        ((1, 0), (2, 0), (1, 1), (2, 1)),
    ),
    TetrominoKind.T: (
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (1, 2)),
        ((1, 0), (0, 1), (1, 1), (1, 2)),
    ),
    TetrominoKind.S: (
        ((1, 0), (2, 0), (0, 1), (1, 1)),
        ((1, 0), (1, 1), (2, 1), (2, 2)),
        ((1, 1), (2, 1), (0, 2), (1, 2)),
        ((0, 0), (0, 1), (1, 1), (1, 2)),
    ),
    TetrominoKind.Z: (
        ((0, 0), (1, 0), (1, 1), (2, 1)),
        ((2, 0), (1, 1), (2, 1), (1, 2)),
        ((0, 1), (1, 1), (1, 2), (2, 2)),
        ((1, 0), (0, 1), (1, 1), (0, 2)),
    ),
    TetrominoKind.J: (
        ((0, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (2, 0), (1, 1), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (2, 2)),
        ((1, 0), (1, 1), (0, 2), (1, 2)),
    ),
    TetrominoKind.L: (
        ((2, 0), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (1, 2), (2, 2)),
        ((0, 1), (1, 1), (2, 1), (0, 2)),
        ((0, 0), (1, 0), (1, 1), (1, 2)),
    ),
}


def shape_cells(kind: TetrominoKind, rotation: int) -> tuple[Cell, ...]:
    """Devuelve las celdas locales `(x, y)` de la pieza en esa rotación.

    Args:
        kind: tipo de pieza.
        rotation: orientación entera; se normaliza módulo 4.

    Returns:
        Tupla inmutable de 4 celdas con coordenadas en el bounding-box
        4×4 local.
    """
    return _SHAPES[kind][rotation % 4]

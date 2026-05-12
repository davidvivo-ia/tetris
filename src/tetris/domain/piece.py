"""Pieza activa: tipo, rotación y posición en el tablero."""

from __future__ import annotations

from dataclasses import dataclass, replace

from tetris.domain.shapes import Cell, shape_cells
from tetris.domain.tetromino import TetrominoKind


@dataclass(frozen=True, slots=True)
class Piece:
    """Pieza en juego.

    Las coordenadas `(x, y)` apuntan a la esquina superior-izquierda
    del bounding-box 4×4 de la forma local. `y` puede ser negativo
    durante el spawn (parte superior del tablero).
    """

    kind: TetrominoKind
    rotation: int
    x: int
    y: int

    def cells(self) -> tuple[Cell, ...]:
        """Coordenadas absolutas en el tablero de las 4 celdas activas."""
        return tuple(
            (self.x + cx, self.y + cy)
            for cx, cy in shape_cells(self.kind, self.rotation)
        )

    def moved(self, dx: int, dy: int) -> Piece:
        """Devuelve una pieza desplazada `(dx, dy)`."""
        return replace(self, x=self.x + dx, y=self.y + dy)

    def rotated(self, direction: int) -> Piece:
        """Devuelve una pieza rotada `direction` cuartos de vuelta.

        Args:
            direction: +1 horario, -1 antihorario.
        """
        return replace(self, rotation=(self.rotation + direction) % 4)

    def with_position(self, x: int, y: int) -> Piece:
        """Devuelve una pieza con posición absoluta nueva."""
        return replace(self, x=x, y=y)

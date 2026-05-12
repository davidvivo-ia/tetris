"""Tablero inmutable de 10×20 celdas."""

from __future__ import annotations

from dataclasses import dataclass

from tetris.domain.piece import Piece
from tetris.domain.tetromino import TetrominoKind

ROWS = 20
COLS = 10

Row = tuple[TetrominoKind | None, ...]
Grid = tuple[Row, ...]


@dataclass(frozen=True, slots=True)
class Board:
    """Estado de las celdas fijadas. Inmutable.

    `grid[y][x]` con `y` creciendo hacia abajo, `x` hacia la derecha.
    `None` representa celda vacía; `TetrominoKind` el color/tipo de la
    pieza que la ocupó.
    """

    grid: Grid

    @classmethod
    def empty(cls, rows: int = ROWS, cols: int = COLS) -> Board:
        """Construye un tablero vacío de las dimensiones indicadas."""
        empty_row: Row = tuple(None for _ in range(cols))
        return cls(grid=tuple(empty_row for _ in range(rows)))

    @property
    def rows(self) -> int:
        """Número de filas."""
        return len(self.grid)

    @property
    def cols(self) -> int:
        """Número de columnas."""
        return len(self.grid[0]) if self.grid else 0

    def is_inside(self, x: int, y: int) -> bool:
        """Verdadero si `(x, y)` cae dentro del tablero."""
        return 0 <= x < self.cols and 0 <= y < self.rows

    def is_blocked(self, x: int, y: int) -> bool:
        """Verdadero si `(x, y)` está fuera, o lleno.

        Filas por encima del tablero (`y < 0`) cuentan como libres para
        permitir el spawn alto.
        """
        if y < 0 and 0 <= x < self.cols:
            return False
        if not self.is_inside(x, y):
            return True
        return self.grid[y][x] is not None

    def fits(self, piece: Piece) -> bool:
        """Verdadero si la pieza puede colocarse sin colisión."""
        return all(not self.is_blocked(x, y) for x, y in piece.cells())

    def with_locked(self, piece: Piece) -> Board:
        """Devuelve un tablero nuevo con la pieza fijada.

        Las celdas de la pieza fuera del tablero (`y < 0`) se ignoran
        silenciosamente; la detección de game-over la hace el reducer
        comparando si la pieza recién generada cabe.
        """
        new_grid: list[list[TetrominoKind | None]] = [list(row) for row in self.grid]
        for x, y in piece.cells():
            if 0 <= y < self.rows and 0 <= x < self.cols:
                new_grid[y][x] = piece.kind
        return Board(grid=tuple(tuple(row) for row in new_grid))

    def cleared(self) -> tuple[Board, int]:
        """Devuelve `(tablero_compactado, líneas_borradas)`.

        Filas completas se eliminan y se rellena por arriba con vacías.
        """
        kept = [row for row in self.grid if any(c is None for c in row)]
        cleared_count = self.rows - len(kept)
        empty_row: Row = tuple(None for _ in range(self.cols))
        new_grid: Grid = tuple([empty_row] * cleared_count + kept)
        return Board(grid=new_grid), cleared_count

    def is_empty(self) -> bool:
        """Verdadero si el tablero no tiene ninguna celda fijada."""
        return all(cell is None for row in self.grid for cell in row)

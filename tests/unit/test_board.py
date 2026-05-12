"""Comportamiento del tablero inmutable."""

from __future__ import annotations

from tetris.domain.board import COLS, ROWS, Board
from tetris.domain.piece import Piece
from tetris.domain.tetromino import TetrominoKind


def test_empty_board_has_expected_dimensions():
    b = Board.empty()
    assert b.rows == ROWS
    assert b.cols == COLS
    assert b.is_empty()


def test_is_inside_boundaries():
    b = Board.empty()
    assert b.is_inside(0, 0)
    assert b.is_inside(COLS - 1, ROWS - 1)
    assert not b.is_inside(-1, 0)
    assert not b.is_inside(COLS, 0)
    assert not b.is_inside(0, ROWS)


def test_is_blocked_negative_y_is_free_inside_x():
    b = Board.empty()
    assert not b.is_blocked(0, -1)
    assert not b.is_blocked(5, -3)
    # but out of x bounds even with negative y blocks
    assert b.is_blocked(-1, -1)


def test_with_locked_is_immutable_and_paints_cells():
    b = Board.empty()
    piece = Piece(kind=TetrominoKind.O, rotation=0, x=0, y=ROWS - 2)
    b2 = b.with_locked(piece)
    assert b is not b2
    assert b.is_empty()
    occupied = {(x, y) for x, y in piece.cells()}
    for y in range(ROWS):
        for x in range(COLS):
            expected = TetrominoKind.O if (x, y) in occupied else None
            assert b2.grid[y][x] == expected


def test_cleared_removes_full_rows_and_returns_count():
    full_row = tuple(TetrominoKind.I for _ in range(COLS))
    half_row = tuple(TetrominoKind.I if i < COLS - 1 else None for i in range(COLS))
    rows = [tuple(None for _ in range(COLS))] * (ROWS - 3) + [
        half_row,
        full_row,
        full_row,
    ]
    b = Board(grid=tuple(rows))
    cleared, n = b.cleared()
    assert n == 2
    assert cleared.rows == ROWS
    assert cleared.cols == COLS
    # last row is the surviving half row
    assert cleared.grid[-1] == half_row
    # rows above the half row are empty
    for r in cleared.grid[:-1]:
        assert all(c is None for c in r)


def test_fits_detects_collision_with_walls():
    b = Board.empty()
    piece = Piece(kind=TetrominoKind.I, rotation=0, x=-2, y=0)
    assert not b.fits(piece)
    piece = Piece(kind=TetrominoKind.I, rotation=0, x=COLS - 2, y=0)
    assert not b.fits(piece)

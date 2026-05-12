"""Pieza inmutable: movimientos y rotaciones."""

from __future__ import annotations

from tetris.domain.piece import Piece
from tetris.domain.tetromino import TetrominoKind


def test_moved_returns_new_instance():
    p = Piece(kind=TetrominoKind.T, rotation=0, x=4, y=0)
    p2 = p.moved(1, 2)
    assert p2 is not p
    assert (p2.x, p2.y) == (5, 2)
    assert (p.x, p.y) == (4, 0)


def test_rotated_normalizes_mod_4():
    p = Piece(kind=TetrominoKind.T, rotation=0, x=0, y=0)
    assert p.rotated(1).rotation == 1
    assert p.rotated(-1).rotation == 3
    assert p.rotated(5).rotation == 1


def test_cells_are_translated_correctly():
    p = Piece(kind=TetrominoKind.O, rotation=0, x=3, y=5)
    cells = set(p.cells())
    assert cells == {(4, 5), (5, 5), (4, 6), (5, 6)}

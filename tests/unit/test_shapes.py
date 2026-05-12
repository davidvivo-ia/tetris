"""Cada pieza tiene 4 celdas válidas en cada rotación."""

from __future__ import annotations

import pytest

from tetris.domain.shapes import shape_cells
from tetris.domain.tetromino import ALL_KINDS, TetrominoKind


@pytest.mark.parametrize("kind", ALL_KINDS)
def test_each_rotation_has_four_cells(kind):
    for rotation in range(4):
        cells = shape_cells(kind, rotation)
        assert len(cells) == 4
        assert len(set(cells)) == 4


@pytest.mark.parametrize("kind", ALL_KINDS)
def test_cells_fit_in_4x4_bbox(kind):
    for rotation in range(4):
        for x, y in shape_cells(kind, rotation):
            assert 0 <= x < 4, f"{kind} rot {rotation}"
            assert 0 <= y < 4


def test_o_piece_is_invariant_to_rotation():
    sets = [set(shape_cells(TetrominoKind.O, r)) for r in range(4)]
    assert all(s == sets[0] for s in sets)


def test_rotation_normalizes_modulo_four():
    assert shape_cells(TetrominoKind.T, 0) == shape_cells(TetrominoKind.T, 4)
    assert shape_cells(TetrominoKind.T, 1) == shape_cells(TetrominoKind.T, 5)

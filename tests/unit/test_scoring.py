"""Tabla BPS escala Nintendo."""

from __future__ import annotations

import pytest

from tetris.domain.scoring import level_for_total_lines, score_for_lines


def test_zero_lines_gives_zero():
    assert score_for_lines(0, 1) == 0
    assert score_for_lines(0, 9) == 0


@pytest.mark.parametrize(
    ("lines", "level", "expected"),
    [
        (1, 1, 40),
        (2, 1, 100),
        (3, 1, 300),
        (4, 1, 1200),
        (1, 5, 200),
        (4, 10, 12000),
    ],
)
def test_bps_table(lines, level, expected):
    assert score_for_lines(lines, level) == expected


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        score_for_lines(-1, 1)
    with pytest.raises(ValueError):
        score_for_lines(5, 1)
    with pytest.raises(ValueError):
        score_for_lines(1, 0)


def test_level_progression():
    assert level_for_total_lines(0) == 1
    assert level_for_total_lines(9) == 1
    assert level_for_total_lines(10) == 2
    assert level_for_total_lines(19) == 2
    assert level_for_total_lines(20) == 3
    assert level_for_total_lines(500) == 20  # capped


def test_level_rejects_negative():
    with pytest.raises(ValueError):
        level_for_total_lines(-1)

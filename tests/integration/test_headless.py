"""Pruebas del runner headless."""

from __future__ import annotations

from tetris.application.demo import DEMO_SEED
from tetris.presentation.headless import HeadlessResult, run_headless_demo


def test_headless_returns_result():
    result = run_headless_demo(seed=DEMO_SEED, max_ticks=30)
    assert isinstance(result, HeadlessResult)
    assert result.seed == DEMO_SEED
    assert result.actions_applied <= 30


def test_headless_is_deterministic():
    a = run_headless_demo(seed=12345, max_ticks=50)
    b = run_headless_demo(seed=12345, max_ticks=50)
    assert a == b


def test_headless_eventually_reaches_game_over():
    result = run_headless_demo(seed=DEMO_SEED, max_ticks=5000)
    assert result.game_over

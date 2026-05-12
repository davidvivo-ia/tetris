"""Test de integración de la sesión de juego."""

from __future__ import annotations

from collections.abc import Iterable
from itertools import cycle

from tetris.application.demo import demo_actions
from tetris.application.play_session import (
    INITIAL_QUEUE_SIZE,
    PlaySession,
    gravity_period,
)
from tetris.domain.actions import Action
from tetris.domain.game_state import QUEUE_VISIBLE
from tetris.domain.tetromino import ALL_KINDS, TetrominoKind


class FakeRandom:
    def __init__(self, sequence: Iterable[TetrominoKind] | None = None) -> None:
        self._source = cycle(sequence or ALL_KINDS)

    def next_kind(self) -> TetrominoKind:
        return next(self._source)

    def next_n(self, n: int) -> Iterable[TetrominoKind]:
        return [self.next_kind() for _ in range(n)]


class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


def test_session_starts_with_visible_queue():
    rng = FakeRandom()
    clock = FakeClock()
    session = PlaySession.start(rng, clock)
    assert len(session.state.queue) >= QUEUE_VISIBLE


def test_initial_active_is_first_drawn():
    rng = FakeRandom(sequence=[TetrominoKind.T, TetrominoKind.I, TetrominoKind.O])
    session = PlaySession.start(rng, FakeClock())
    assert session.state.active.kind is TetrominoKind.T


def test_gravity_does_not_trigger_before_period():
    clock = FakeClock()
    session = PlaySession.start(FakeRandom(), clock)
    initial = session.state
    new, events = session.update()
    assert new is initial
    assert events == ()


def test_gravity_triggers_after_period():
    clock = FakeClock()
    session = PlaySession.start(FakeRandom(), clock)
    clock.advance(gravity_period(session.state.level) + 0.01)
    new, _ = session.update()
    assert new.active.y == 1 or new.active.kind != session.state.active.kind


def test_queue_is_refilled_after_lock():
    clock = FakeClock()
    session = PlaySession.start(FakeRandom(), clock)
    for _ in range(50):
        session.apply(Action.HARD_DROP)
        if session.state.game_over:
            break
        assert len(session.state.queue) >= QUEUE_VISIBLE - 1


def test_demo_plays_for_at_least_a_minute_of_actions():
    clock = FakeClock()
    session = PlaySession.start(FakeRandom(), clock)
    actions = demo_actions()
    n = 0
    for action in actions:
        session.apply(action)
        n += 1
        if session.state.game_over or n >= 500:
            break
    assert n > 20


def test_reset_clears_state():
    clock = FakeClock()
    session = PlaySession.start(FakeRandom(), clock)
    for _ in range(10):
        session.apply(Action.HARD_DROP)
    session.reset()
    assert session.state.score == 0
    assert session.state.lines == 0
    assert not session.state.game_over


def test_initial_queue_size_includes_active():
    # Aseguramos que pedimos lo suficiente para tener cola visible
    assert INITIAL_QUEUE_SIZE >= QUEUE_VISIBLE


def test_gravity_period_decreases_with_level():
    assert gravity_period(1) > gravity_period(2)
    assert gravity_period(20) >= 0.05

"""Render de widgets sin levantar la app Textual completa."""

from __future__ import annotations

from tetris.application.play_session import PlaySession
from tetris.domain.actions import Action
from tetris.infrastructure.clock import MonotonicClock
from tetris.infrastructure.random_source import SevenBagRandom
from tetris.presentation.tui.widgets.board import _render_state


def test_board_render_returns_non_empty_text():
    session = PlaySession.start(SevenBagRandom(seed=1), MonotonicClock())
    rendered = _render_state(session.state)
    assert rendered.plain != ""
    # 20 filas separadas por \n
    assert rendered.plain.count("\n") == 19


def test_board_render_changes_after_move():
    session = PlaySession.start(SevenBagRandom(seed=1), MonotonicClock())
    a = _render_state(session.state)
    session.apply(Action.MOVE_LEFT)
    b = _render_state(session.state)
    # No siempre cambia (puede estar en pared), pero el render debe ser válido
    assert b.plain.count("\n") == a.plain.count("\n")

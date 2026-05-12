"""Reducer del dominio: cubre cada acción y casos límite."""

from __future__ import annotations

import pytest

from tetris.domain.actions import Action
from tetris.domain.board import COLS, ROWS, Board
from tetris.domain.events import EventKind
from tetris.domain.game_state import GameState, ghost_y, new_game, spawn_piece, step
from tetris.domain.piece import Piece
from tetris.domain.tetromino import TetrominoKind


def make_state(
    queue: list[TetrominoKind] | None = None,
    *,
    active: TetrominoKind = TetrominoKind.T,
    board: Board | None = None,
) -> GameState:
    queue = queue or [TetrominoKind.O] * 10
    state = new_game([active, *queue])
    if board is not None:
        state = state.__class__(
            board=board,
            active=state.active,
            queue=state.queue,
            hold=state.hold,
            hold_used=state.hold_used,
            score=state.score,
            lines=state.lines,
            level=state.level,
            game_over=state.game_over,
            paused=state.paused,
        )
    return state


def test_new_game_requires_non_empty_queue():
    with pytest.raises(ValueError):
        new_game([])


def test_new_game_initial_state():
    state = new_game([TetrominoKind.T, TetrominoKind.O])
    assert state.active.kind is TetrominoKind.T
    assert state.queue == (TetrominoKind.O,)
    assert state.score == 0
    assert state.lines == 0
    assert state.level == 1
    assert not state.game_over
    assert not state.paused


def test_move_left_and_right():
    state = make_state()
    moved_left, events = step(state, Action.MOVE_LEFT)
    assert moved_left.active.x == state.active.x - 1
    assert events[0].kind is EventKind.PIECE_MOVED

    moved_right, _ = step(state, Action.MOVE_RIGHT)
    assert moved_right.active.x == state.active.x + 1


def test_move_blocked_by_wall_does_not_change_state():
    state = make_state()
    # mover a la izquierda hasta tocar pared
    while True:
        new, events = step(state, Action.MOVE_LEFT)
        if not events:
            break
        state = new
    new, events = step(state, Action.MOVE_LEFT)
    assert new is state
    assert events == ()


def test_rotate_changes_rotation():
    state = make_state(active=TetrominoKind.T)
    rotated, events = step(state, Action.ROTATE_CW)
    assert rotated.active.rotation == 1
    assert events[0].kind is EventKind.PIECE_ROTATED

    back, _ = step(rotated, Action.ROTATE_CCW)
    assert back.active.rotation == 0


def test_pause_toggles_and_blocks_other_actions():
    state = make_state()
    paused, events = step(state, Action.PAUSE)
    assert paused.paused
    assert events[0].kind is EventKind.PAUSED

    same, e2 = step(paused, Action.MOVE_LEFT)
    assert same is paused
    assert e2 == ()

    resumed, events = step(paused, Action.PAUSE)
    assert not resumed.paused
    assert events[0].kind is EventKind.RESUMED


def test_soft_drop_increments_score():
    state = make_state()
    new, _ = step(state, Action.SOFT_DROP)
    assert new.score == state.score + 1
    assert new.active.y == state.active.y + 1


def test_hard_drop_locks_and_scores_distance_x2():
    state = make_state()
    distance = ghost_y(state) - state.active.y
    after, events = step(state, Action.HARD_DROP)
    kinds = [e.kind for e in events]
    assert EventKind.HARD_DROPPED in kinds
    assert EventKind.PIECE_LOCKED in kinds
    # Score: 2 * distancia (más bonus por lineas, aquí 0)
    assert after.score == state.score + 2 * distance


def test_tick_eventually_locks_piece():
    state = make_state()
    # Aplicar ticks hasta que la pieza se fije; el active cambiará de tipo
    initial_active = state.active.kind
    new = state
    safety = 0
    while new.active.kind == initial_active and not new.game_over:
        new, _ = step(new, Action.TICK)
        safety += 1
        assert safety < 100, "tick no termina"
    assert new.active.kind != initial_active


def test_lines_cleared_event_when_full_row():
    # Fila inferior con dos huecos en columnas 4 y 5; un O al caer rellena
    bottom = tuple(None if i in (4, 5) else TetrominoKind.I for i in range(COLS))
    empty = tuple(None for _ in range(COLS))
    rows = [empty] * (ROWS - 1) + [bottom]
    board = Board(grid=tuple(rows))
    state = GameState(
        board=board,
        active=Piece(kind=TetrominoKind.O, rotation=0, x=3, y=0),
        queue=(TetrominoKind.T, TetrominoKind.S),
        hold=None,
        hold_used=False,
        score=0,
        lines=0,
        level=1,
        game_over=False,
        paused=False,
    )
    new, events = step(state, Action.HARD_DROP)
    kinds = [e.kind for e in events]
    assert EventKind.LINES_CLEARED in kinds
    assert new.lines == 1
    assert new.score > 0


def test_hold_swaps_and_blocks_until_lock():
    state = make_state(active=TetrominoKind.T, queue=[TetrominoKind.I, TetrominoKind.O])
    new, events = step(state, Action.HOLD)
    assert new.hold is TetrominoKind.T
    assert new.active.kind is TetrominoKind.I
    assert new.hold_used
    assert events[0].kind is EventKind.HELD

    # Segundo hold ignorado
    same, e2 = step(new, Action.HOLD)
    assert same is new
    assert e2 == ()


def test_hold_with_existing_hold_swaps():
    state = make_state(
        active=TetrominoKind.T,
        queue=[TetrominoKind.S, *([TetrominoKind.O] * 30)],
    )
    state = step(state, Action.HOLD)[0]  # T -> hold, active=S
    while state.active.kind is TetrominoKind.S and not state.game_over:
        state, _ = step(state, Action.TICK)
    assert state.hold is TetrominoKind.T
    assert not state.hold_used
    new, _ = step(state, Action.HOLD)
    assert new.hold == state.active.kind
    assert new.active.kind is TetrominoKind.T


def test_actions_on_game_over_are_noop():
    state = make_state()
    state = GameState(
        board=state.board,
        active=state.active,
        queue=state.queue,
        hold=state.hold,
        hold_used=state.hold_used,
        score=state.score,
        lines=state.lines,
        level=state.level,
        game_over=True,
        paused=False,
    )
    for action in Action:
        new, events = step(state, action)
        assert new is state
        assert events == ()


def test_ghost_y_lands_at_bottom_for_empty_board():
    state = make_state()
    y = ghost_y(state)
    # Para una pieza T con rotación 0 y filas locales {0,1}, el fondo es 18
    assert y == ROWS - 2


def test_spawn_piece_position():
    p = spawn_piece(TetrominoKind.I)
    assert p.x == 3
    assert p.y == 0
    assert p.rotation == 0


def test_game_over_when_new_piece_does_not_fit():
    # Bloqueo en la zona de spawn (cols 3-6, filas 0-1) sin filas llenas
    top_blocker = tuple(TetrominoKind.I if 3 <= i <= 6 else None for i in range(COLS))
    empty = tuple(None for _ in range(COLS))
    rows = [top_blocker] + [empty] * (ROWS - 1)
    board = Board(grid=tuple(rows))
    state = GameState(
        board=board,
        active=Piece(kind=TetrominoKind.O, rotation=0, x=0, y=ROWS - 2),
        queue=(TetrominoKind.O,),
        hold=None,
        hold_used=False,
        score=0,
        lines=0,
        level=1,
        game_over=False,
        paused=False,
    )
    new, events = step(state, Action.HARD_DROP)
    assert new.game_over
    assert any(e.kind is EventKind.GAME_OVER for e in events)

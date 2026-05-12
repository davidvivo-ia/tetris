"""Tests basados en propiedades (Hypothesis)."""

from __future__ import annotations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from tetris.domain.actions import Action
from tetris.domain.board import COLS, ROWS, Board
from tetris.domain.game_state import new_game, step
from tetris.domain.piece import Piece
from tetris.domain.shapes import shape_cells
from tetris.domain.tetromino import ALL_KINDS, TetrominoKind

action_st = st.sampled_from(
    [
        Action.MOVE_LEFT,
        Action.MOVE_RIGHT,
        Action.SOFT_DROP,
        Action.HARD_DROP,
        Action.ROTATE_CW,
        Action.ROTATE_CCW,
        Action.HOLD,
        Action.TICK,
    ]
)
kind_st = st.sampled_from(ALL_KINDS)


@given(
    actions=st.lists(action_st, min_size=0, max_size=200),
    seed_queue=st.lists(kind_st, min_size=20, max_size=80),
)
@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_score_is_monotonic(actions, seed_queue):
    state = new_game(seed_queue)
    last_score = 0
    last_lines = 0
    for action in actions:
        state, _ = step(state, action)
        assert state.score >= last_score
        assert state.lines >= last_lines
        last_score = state.score
        last_lines = state.lines
        if state.game_over:
            break


@given(
    seed_queue=st.lists(kind_st, min_size=20, max_size=80),
    actions=st.lists(action_st, min_size=0, max_size=200),
)
@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_active_piece_always_fits(seed_queue, actions):
    state = new_game(seed_queue)
    if state.game_over:
        return
    assert state.board.fits(state.active)
    for action in actions:
        state, _ = step(state, action)
        if state.game_over:
            break
        assert state.board.fits(state.active), f"Pieza fuera tras {action}"


@given(
    seed_queue=st.lists(kind_st, min_size=20, max_size=40),
    actions=st.lists(action_st, min_size=0, max_size=80),
)
@settings(max_examples=50, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_board_dimensions_are_invariant(seed_queue, actions):
    state = new_game(seed_queue)
    for action in actions:
        state, _ = step(state, action)
        assert state.board.rows == ROWS
        assert state.board.cols == COLS
        if state.game_over:
            break


@given(kind=kind_st, rotation=st.integers(min_value=-100, max_value=100))
def test_rotation_modulo_4_is_canonical(kind, rotation):
    assert shape_cells(kind, rotation) == shape_cells(kind, rotation % 4)


@given(
    kind=kind_st,
    x=st.integers(min_value=-5, max_value=15),
    y=st.integers(min_value=-5, max_value=25),
)
def test_piece_cells_translate_consistently(kind, x, y):
    piece = Piece(kind=kind, rotation=0, x=x, y=y)
    local = shape_cells(kind, 0)
    expected = {(x + lx, y + ly) for lx, ly in local}
    assert set(piece.cells()) == expected


@given(
    cells=st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=COLS - 1),
            st.integers(min_value=0, max_value=ROWS - 1),
        ),
        max_size=40,
    )
)
def test_clearing_an_empty_board_is_noop(cells):
    if cells:
        return
    board = Board.empty()
    cleared, n = board.cleared()
    assert n == 0
    assert cleared.grid == board.grid


@given(kind=kind_st)
def test_all_kinds_have_valid_first_rotation(kind: TetrominoKind):
    cells = shape_cells(kind, 0)
    assert len(cells) == 4

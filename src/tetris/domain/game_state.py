"""Estado agregado del juego y reducer puro `step`."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace

from tetris.domain.actions import Action
from tetris.domain.board import COLS, Board
from tetris.domain.events import EventKind, GameEvent
from tetris.domain.piece import Piece
from tetris.domain.rotation import try_rotate
from tetris.domain.scoring import level_for_total_lines, score_for_lines
from tetris.domain.tetromino import TetrominoKind

SPAWN_X = 3
SPAWN_Y = 0
QUEUE_VISIBLE = 5


@dataclass(frozen=True, slots=True)
class GameState:
    """Estado agregado del juego, inmutable.

    `queue` contiene las próximas piezas en orden. La aplicación es
    responsable de mantenerla con un mínimo de elementos (≥1, idealmente
    ≥ `QUEUE_VISIBLE`).
    """

    board: Board
    active: Piece
    queue: tuple[TetrominoKind, ...]
    hold: TetrominoKind | None
    hold_used: bool
    score: int
    lines: int
    level: int
    game_over: bool
    paused: bool


def spawn_piece(kind: TetrominoKind) -> Piece:
    """Crea una pieza nueva con la posición canónica de spawn."""
    return Piece(kind=kind, rotation=0, x=SPAWN_X, y=SPAWN_Y)


def new_game(queue: Iterable[TetrominoKind]) -> GameState:
    """Construye un estado inicial.

    Args:
        queue: iterable de al menos un elemento; el primero se usa como
            pieza activa y el resto queda en cola.

    Raises:
        ValueError: si la cola viene vacía.
    """
    pieces = tuple(queue)
    if not pieces:
        raise ValueError("La cola inicial debe contener al menos una pieza.")
    active = spawn_piece(pieces[0])
    return GameState(
        board=Board.empty(),
        active=active,
        queue=pieces[1:],
        hold=None,
        hold_used=False,
        score=0,
        lines=0,
        level=1,
        game_over=False,
        paused=False,
    )


def ghost_y(state: GameState) -> int:
    """Calcula `y` final si la pieza activa cayera ahora mismo."""
    piece = state.active
    while state.board.fits(piece.moved(0, 1)):
        piece = piece.moved(0, 1)
    return piece.y


def step(state: GameState, action: Action) -> tuple[GameState, tuple[GameEvent, ...]]:
    """Transición pura: estado + acción -> nuevo estado + eventos.

    Reducer determinista. No emplea aleatoriedad ni IO: la cola de
    piezas siguiente debe estar contenida en `state.queue`.
    """
    if state.game_over:
        return state, ()

    if state.paused and action is not Action.PAUSE:
        return state, ()

    match action:
        case Action.PAUSE:
            return _toggle_pause(state)
        case Action.MOVE_LEFT:
            return _move(state, dx=-1, dy=0)
        case Action.MOVE_RIGHT:
            return _move(state, dx=1, dy=0)
        case Action.SOFT_DROP:
            return _soft_drop(state)
        case Action.HARD_DROP:
            return _hard_drop(state)
        case Action.ROTATE_CW:
            return _rotate(state, direction=1)
        case Action.ROTATE_CCW:
            return _rotate(state, direction=-1)
        case Action.HOLD:
            return _hold(state)
        case Action.TICK:
            return _tick(state)


def _toggle_pause(state: GameState) -> tuple[GameState, tuple[GameEvent, ...]]:
    new = replace(state, paused=not state.paused)
    event = GameEvent(kind=EventKind.PAUSED if new.paused else EventKind.RESUMED)
    return new, (event,)


def _move(
    state: GameState, *, dx: int, dy: int
) -> tuple[GameState, tuple[GameEvent, ...]]:
    candidate = state.active.moved(dx, dy)
    if state.board.fits(candidate):
        new = replace(state, active=candidate)
        return new, (GameEvent(kind=EventKind.PIECE_MOVED),)
    return state, ()


def _rotate(
    state: GameState, *, direction: int
) -> tuple[GameState, tuple[GameEvent, ...]]:
    rotated = try_rotate(state.board, state.active, direction)
    if rotated is None:
        return state, ()
    new = replace(state, active=rotated)
    return new, (GameEvent(kind=EventKind.PIECE_ROTATED),)


def _soft_drop(state: GameState) -> tuple[GameState, tuple[GameEvent, ...]]:
    candidate = state.active.moved(0, 1)
    if state.board.fits(candidate):
        new = replace(state, active=candidate, score=state.score + 1)
        return new, (GameEvent(kind=EventKind.PIECE_MOVED),)
    return _lock(state, drop_distance=0)


def _hard_drop(state: GameState) -> tuple[GameState, tuple[GameEvent, ...]]:
    target_y = ghost_y(state)
    distance = target_y - state.active.y
    dropped = state.active.with_position(state.active.x, target_y)
    state = replace(state, active=dropped, score=state.score + 2 * distance)
    locked_state, events = _lock(state, drop_distance=distance)
    return locked_state, (
        GameEvent(kind=EventKind.HARD_DROPPED, drop_distance=distance),
        *events,
    )


def _tick(state: GameState) -> tuple[GameState, tuple[GameEvent, ...]]:
    candidate = state.active.moved(0, 1)
    if state.board.fits(candidate):
        return replace(state, active=candidate), (
            GameEvent(kind=EventKind.PIECE_MOVED),
        )
    return _lock(state, drop_distance=0)


def _hold(state: GameState) -> tuple[GameState, tuple[GameEvent, ...]]:
    if state.hold_used:
        return state, ()
    current_kind = state.active.kind
    if state.hold is None:
        if not state.queue:
            return state, ()
        next_kind = state.queue[0]
        new_active = spawn_piece(next_kind)
        new_queue = state.queue[1:]
        new = replace(
            state, hold=current_kind, active=new_active, queue=new_queue, hold_used=True
        )
    else:
        new_active = spawn_piece(state.hold)
        new = replace(state, hold=current_kind, active=new_active, hold_used=True)
    return new, (GameEvent(kind=EventKind.HELD, piece_kind=current_kind),)


def _lock(
    state: GameState, *, drop_distance: int
) -> tuple[GameState, tuple[GameEvent, ...]]:
    locked_board = state.board.with_locked(state.active)
    cleared_board, n_cleared = locked_board.cleared()

    new_total_lines = state.lines + n_cleared
    old_level = state.level
    new_level = level_for_total_lines(new_total_lines)
    new_score = state.score + score_for_lines(n_cleared, new_level)

    events: list[GameEvent] = [
        GameEvent(
            kind=EventKind.PIECE_LOCKED,
            piece_kind=state.active.kind,
            drop_distance=drop_distance,
        )
    ]
    if n_cleared > 0:
        events.append(GameEvent(kind=EventKind.LINES_CLEARED, lines=n_cleared))
    if new_level > old_level:
        events.append(GameEvent(kind=EventKind.LEVEL_UP))

    if not state.queue:
        new = replace(
            state,
            board=cleared_board,
            score=new_score,
            lines=new_total_lines,
            level=new_level,
            game_over=True,
        )
        events.append(GameEvent(kind=EventKind.GAME_OVER))
        return new, tuple(events)

    next_kind = state.queue[0]
    next_queue = state.queue[1:]
    next_piece = spawn_piece(next_kind)

    if not cleared_board.fits(next_piece):
        new = replace(
            state,
            board=cleared_board,
            active=next_piece,
            queue=next_queue,
            hold_used=False,
            score=new_score,
            lines=new_total_lines,
            level=new_level,
            game_over=True,
        )
        events.append(GameEvent(kind=EventKind.GAME_OVER))
        return new, tuple(events)

    new = replace(
        state,
        board=cleared_board,
        active=next_piece,
        queue=next_queue,
        hold_used=False,
        score=new_score,
        lines=new_total_lines,
        level=new_level,
    )
    return new, tuple(events)


__all__ = [
    "COLS",
    "QUEUE_VISIBLE",
    "SPAWN_X",
    "SPAWN_Y",
    "GameState",
    "ghost_y",
    "new_game",
    "spawn_piece",
    "step",
]

"""Eventos emitidos por el reducer para que la presentación reaccione."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from tetris.domain.tetromino import TetrominoKind


class EventKind(Enum):
    """Categoría de evento."""

    PIECE_MOVED = auto()
    PIECE_ROTATED = auto()
    PIECE_LOCKED = auto()
    LINES_CLEARED = auto()
    HARD_DROPPED = auto()
    HELD = auto()
    LEVEL_UP = auto()
    GAME_OVER = auto()
    PAUSED = auto()
    RESUMED = auto()


@dataclass(frozen=True, slots=True)
class GameEvent:
    """Evento de dominio.

    Lleva información mínima útil para que la capa de presentación
    pueda decorar con animaciones o sonidos sin volver a inspeccionar
    el estado completo.
    """

    kind: EventKind
    lines: int = 0
    drop_distance: int = 0
    piece_kind: TetrominoKind | None = None

"""Acciones que la presentación puede inyectar al reducer."""

from __future__ import annotations

from enum import Enum, auto


class Action(Enum):
    """Acción atómica del juego."""

    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SOFT_DROP = auto()
    HARD_DROP = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    HOLD = auto()
    PAUSE = auto()
    TICK = auto()

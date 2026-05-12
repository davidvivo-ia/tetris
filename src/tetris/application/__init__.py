"""Capa de aplicación: orquesta el dominio con dependencias externas."""

from tetris.application.demo import DEMO_SEED, demo_actions
from tetris.application.play_session import PlaySession, gravity_period
from tetris.application.protocols import (
    Clock,
    RandomSource,
    ScoreEntry,
    ScoreRepository,
)

__all__ = [
    "DEMO_SEED",
    "Clock",
    "PlaySession",
    "RandomSource",
    "ScoreEntry",
    "ScoreRepository",
    "demo_actions",
    "gravity_period",
]

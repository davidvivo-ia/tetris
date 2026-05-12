"""Núcleo de dominio puro: sin IO, sin tiempo, sin RNG."""

from tetris.domain.actions import Action
from tetris.domain.board import Board
from tetris.domain.events import EventKind, GameEvent
from tetris.domain.game_state import GameState, new_game, step
from tetris.domain.piece import Piece
from tetris.domain.scoring import score_for_lines
from tetris.domain.tetromino import TetrominoKind

__all__ = [
    "Action",
    "Board",
    "EventKind",
    "GameEvent",
    "GameState",
    "Piece",
    "TetrominoKind",
    "new_game",
    "score_for_lines",
    "step",
]

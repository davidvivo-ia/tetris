"""Aplicación Textual raíz."""

from __future__ import annotations

from pathlib import Path

from textual.app import App

from tetris.application.play_session import PlaySession
from tetris.infrastructure.clock import MonotonicClock
from tetris.infrastructure.random_source import SevenBagRandom
from tetris.presentation.tui.screens.game import GameScreen

CSS_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "tetris.tcss"


class TetrisApp(App[None]):
    """App raíz del juego."""

    CSS_PATH = CSS_PATH
    TITLE = "Tetris — Phosphor 2026"

    def __init__(self, seed: int | None = None) -> None:
        super().__init__()
        self.session = PlaySession.start(SevenBagRandom(seed=seed), MonotonicClock())

    def on_mount(self) -> None:
        """Abre la pantalla de juego."""
        self.push_screen(GameScreen(self.session))

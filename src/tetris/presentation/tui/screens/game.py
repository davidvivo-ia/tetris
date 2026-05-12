"""Pantalla principal del juego."""

from __future__ import annotations

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Static

from tetris.application.play_session import PlaySession, gravity_period
from tetris.domain.actions import Action
from tetris.presentation.tui.widgets.board import BoardWidget
from tetris.presentation.tui.widgets.hud import HudContainer

UPDATE_INTERVAL = 1.0 / 30.0  # 30 Hz


class GameScreen(Screen[None]):
    """Pantalla con tablero + HUD."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("left", "act('MOVE_LEFT')", "izq"),
        Binding("right", "act('MOVE_RIGHT')", "der"),
        Binding("down", "act('SOFT_DROP')", "soft"),
        Binding("up", "act('ROTATE_CW')", "rotar"),
        Binding("x", "act('ROTATE_CW')", "rotar"),
        Binding("z", "act('ROTATE_CCW')", "rotar izq"),
        Binding("space", "act('HARD_DROP')", "drop"),
        Binding("c", "act('HOLD')", "hold"),
        Binding("p", "act('PAUSE')", "pausa"),
        Binding("r", "restart", "reinic."),
        Binding("q", "quit", "salir"),
    ]

    def __init__(self, session: PlaySession) -> None:
        super().__init__()
        self.session = session
        self.board = BoardWidget(id="board-panel")
        self.hud = HudContainer()
        self.overlay = Static("", id="overlay")
        self.overlay.display = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="layout"):
            yield self.board
            yield self.hud
        yield self.overlay

    def on_mount(self) -> None:
        """Configura timers y pinta el primer frame."""
        self.refresh_view()
        self.set_interval(UPDATE_INTERVAL, self._tick)

    def _tick(self) -> None:
        if self.session.state.game_over:
            self._show_game_over()
            return
        previous = self.session.state
        new, _ = self.session.update()
        if new is not previous or self.session.state.paused:
            self.refresh_view()

    def refresh_view(self) -> None:
        """Repinta tablero, HUD y overlays."""
        state = self.session.state
        self.board.update_state(state)
        self.hud.update_state(state)
        if state.game_over:
            self._show_game_over()
        elif state.paused:
            self._show_pause()
        else:
            self.overlay.display = False
            self.overlay.remove_class("danger")

    def _show_pause(self) -> None:
        self.overlay.update("▌  PAUSA  ▐")
        self.overlay.remove_class("danger")
        self.overlay.display = True

    def _show_game_over(self) -> None:
        self.overlay.update(
            f"GAME OVER\nscore {self.session.state.score}\npulsa R para reiniciar"
        )
        self.overlay.add_class("danger")
        self.overlay.display = True

    def action_act(self, name: str) -> None:
        """Despacha una acción nombrada al reducer."""
        action = Action[name]
        previous_period = gravity_period(self.session.state.level)
        self.session.apply(action)
        self.refresh_view()
        # Pequeña ayuda: si la pieza llega abajo, la próxima caída se nota
        _ = previous_period

    def action_restart(self) -> None:
        """Reinicia la partida."""
        self.session.reset()
        self.refresh_view()

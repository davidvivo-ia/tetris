"""Widgets de HUD: score, next, hold, help."""

from __future__ import annotations

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from tetris.assets.palette import CELL_FULL, MUTED, PIECE_COLOR, PRIMARY
from tetris.domain.game_state import GameState
from tetris.domain.shapes import shape_cells
from tetris.domain.tetromino import TetrominoKind


class StatsPanel(Widget):
    """Bloque con puntuación, líneas y nivel."""

    DEFAULT_CSS = "StatsPanel { height: 5; }"

    state: GameState | None = None

    def update_state(self, state: GameState) -> None:
        """Refresca cifras."""
        self.state = state
        self.refresh()

    def render(self) -> Text:
        if self.state is None:
            return Text("")
        s = self.state
        body = Text()
        body.append("SCORE\n", style=f"bold {MUTED}")
        body.append(f"{s.score:>10}\n", style=f"bold {PRIMARY}")
        body.append("LINES   ", style=MUTED)
        body.append(f"{s.lines:>3}\n", style=PRIMARY)
        body.append("LEVEL   ", style=MUTED)
        body.append(f"{s.level:>3}", style=PRIMARY)
        return body


def _mini_piece(kind: TetrominoKind | None) -> Text:
    if kind is None:
        return Text("   \n   \n   ", style=MUTED)
    cells = set(shape_cells(kind, 0))
    color = PIECE_COLOR[kind]
    text = Text()
    for y in range(3):
        for x in range(4):
            if (x, y) in cells:
                text.append(CELL_FULL[0], style=f"bold {color}")
            else:
                text.append(" ")
        if y < 2:
            text.append("\n")
    return text


class NextPanel(Widget):
    """Cola de próximas piezas (3 primeras)."""

    DEFAULT_CSS = "NextPanel { height: 11; }"

    state: GameState | None = None

    def update_state(self, state: GameState) -> None:
        """Refresca cola."""
        self.state = state
        self.refresh()

    def render(self) -> Text:
        body = Text()
        body.append("NEXT\n", style=f"bold {MUTED}")
        if self.state is None:
            return body
        for kind in self.state.queue[:3]:
            body.append(_mini_piece(kind))
            body.append("\n")
        return body


class HoldPanel(Widget):
    """Pieza en hold."""

    DEFAULT_CSS = "HoldPanel { height: 5; }"

    state: GameState | None = None

    def update_state(self, state: GameState) -> None:
        """Refresca hold."""
        self.state = state
        self.refresh()

    def render(self) -> Text:
        body = Text()
        body.append("HOLD\n", style=f"bold {MUTED}")
        if self.state is None or self.state.hold is None:
            body.append("  --", style=MUTED)
            return body
        body.append(_mini_piece(self.state.hold))
        return body


class HelpPanel(Static):
    """Listado estático de bindings."""

    def __init__(self, *, classes: str | None = None) -> None:
        super().__init__(self._build(), classes=classes)

    def _build(self) -> Text:
        text = Text()
        text.append("CONTROLES\n", style=f"bold {MUTED}")
        rows = [
            ("←/→", "mover"),
            ("↓", "soft drop"),
            ("espacio", "hard drop"),
            ("↑ / x", "rotar"),
            ("z", "rotar izq."),
            ("c", "hold"),
            ("p", "pausa"),
            ("r", "reiniciar"),
            ("q", "salir"),
        ]
        for key, label in rows:
            text.append(f"{key:<8}", style=PRIMARY)
            text.append(f"{label}\n", style=MUTED)
        return text


class HudContainer(Vertical):
    """Contenedor con los 4 paneles laterales."""

    def __init__(self) -> None:
        super().__init__(id="side-panel")
        self.stats = StatsPanel(classes="hud-block")
        self.next_panel = NextPanel(classes="hud-block")
        self.hold = HoldPanel(classes="hud-block")
        self.help = HelpPanel(classes="hud-block")

    def compose(self) -> ComposeResult:
        yield self.stats
        yield self.next_panel
        yield self.hold
        yield self.help

    def update_state(self, state: GameState) -> None:
        """Propaga el estado a los paneles dependientes."""
        self.stats.update_state(state)
        self.next_panel.update_state(state)
        self.hold.update_state(state)

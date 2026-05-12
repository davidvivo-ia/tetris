"""Widget de tablero: renderiza grid + activa + ghost con bloques de color."""

from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from tetris.assets.palette import CELL_EMPTY, CELL_FULL, CELL_GHOST, PIECE_COLOR
from tetris.domain.game_state import GameState, ghost_y


class BoardWidget(Widget):
    """Renderiza el `GameState` actual usando rich.Text."""

    DEFAULT_CSS = "BoardWidget { width: 22; height: 20; }"

    state: GameState | None = None

    def update_state(self, state: GameState) -> None:
        """Actualiza el estado a pintar y solicita repintado."""
        self.state = state
        self.refresh()

    def render(self) -> Text:
        if self.state is None:
            return Text("")
        return _render_state(self.state)


def _render_state(state: GameState) -> Text:
    board = state.board
    overlay: dict[tuple[int, int], str] = {}

    if not state.game_over:
        target_y = ghost_y(state)
        ghost_piece = state.active.with_position(state.active.x, target_y)
        for x, y in ghost_piece.cells():
            if 0 <= y < board.rows and 0 <= x < board.cols:
                overlay[(x, y)] = "ghost"
        for x, y in state.active.cells():
            if 0 <= y < board.rows and 0 <= x < board.cols:
                overlay[(x, y)] = "active"

    text = Text()
    for y in range(board.rows):
        for x in range(board.cols):
            overlay_kind = overlay.get((x, y))
            if overlay_kind == "active":
                color = PIECE_COLOR[state.active.kind]
                text.append(CELL_FULL, style=f"bold {color}")
            elif overlay_kind == "ghost":
                color = PIECE_COLOR[state.active.kind]
                text.append(CELL_GHOST, style=color)
            else:
                cell = board.grid[y][x]
                if cell is None:
                    text.append(CELL_EMPTY)
                else:
                    text.append(CELL_FULL, style=f"bold {PIECE_COLOR[cell]}")
        if y < board.rows - 1:
            text.append("\n")
    return text

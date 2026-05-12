"""Modo headless: ejecuta una partida sin TUI. Útil para CI y smoke tests."""

from __future__ import annotations

from dataclasses import dataclass

from rich.console import Console

from tetris.application.demo import demo_actions
from tetris.application.play_session import PlaySession
from tetris.infrastructure.clock import MonotonicClock
from tetris.infrastructure.random_source import SevenBagRandom


@dataclass(frozen=True, slots=True)
class HeadlessResult:
    """Resumen de una corrida headless."""

    score: int
    lines: int
    level: int
    actions_applied: int
    game_over: bool
    seed: int


def run_headless_demo(
    *,
    seed: int,
    max_ticks: int = 500,
    console: Console | None = None,
) -> HeadlessResult:
    """Aplica la secuencia demo de forma determinista hasta game over o tope.

    Args:
        seed: semilla del 7-bag.
        max_ticks: número máximo de acciones a aplicar.
        console: rich console opcional para emitir progreso.

    Returns:
        Resumen final de la partida.
    """
    rng = SevenBagRandom(seed=seed)
    session = PlaySession.start(rng, MonotonicClock())
    out = console or Console(quiet=True)

    applied = 0
    for action in demo_actions():
        if applied >= max_ticks or session.state.game_over:
            break
        session.apply(action)
        applied += 1

    out.print(
        f"[bold #7FFFB2]demo terminada[/]: score={session.state.score} "
        f"lines={session.state.lines} level={session.state.level} "
        f"game_over={session.state.game_over} seed={rng.seed_used}"
    )

    return HeadlessResult(
        score=session.state.score,
        lines=session.state.lines,
        level=session.state.level,
        actions_applied=applied,
        game_over=session.state.game_over,
        seed=rng.seed_used,
    )

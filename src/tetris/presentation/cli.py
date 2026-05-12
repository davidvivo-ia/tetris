"""CLI Typer para Tetris."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from tetris.application.demo import DEMO_SEED
from tetris.presentation.headless import run_headless_demo

app = typer.Typer(
    name="tetris",
    help="Tetris 2026 — un listado BASIC de 1986 reimaginado.",
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
)

console = Console()


def _launch_tui(seed: int | None) -> None:
    """Importa Textual perezosamente para que `--headless` no lo necesite."""
    from tetris.presentation.tui.app import TetrisApp  # noqa: PLC0415

    TetrisApp(seed=seed).run()


@app.callback(invoke_without_command=True)
def main(
    seed: Annotated[
        int | None,
        typer.Option("--seed", help="Semilla del 7-bag (reproducible)."),
    ] = None,
    demo: Annotated[
        bool,
        typer.Option("--demo", help="Ejecuta una partida demo determinista."),
    ] = False,
    headless: Annotated[
        bool,
        typer.Option(
            "--headless",
            help="No abre la TUI; útil para CI o smoke tests.",
        ),
    ] = False,
    max_ticks: Annotated[
        int,
        typer.Option(
            "--max-ticks",
            min=1,
            max=10000,
            help="Acciones máximas en modo demo headless.",
        ),
    ] = 500,
) -> None:
    """Lanza el juego. Sin opciones, abre la TUI Textual."""
    if demo:
        effective_seed = seed if seed is not None else DEMO_SEED
        if headless:
            result = run_headless_demo(
                seed=effective_seed,
                max_ticks=max_ticks,
                console=console,
            )
            raise typer.Exit(code=0 if result.actions_applied > 0 else 1)
        _launch_tui(seed=effective_seed)
        return

    if headless:
        result = run_headless_demo(
            seed=seed if seed is not None else DEMO_SEED,
            max_ticks=max_ticks,
            console=console,
        )
        raise typer.Exit(code=0 if result.actions_applied > 0 else 1)

    _launch_tui(seed=seed)

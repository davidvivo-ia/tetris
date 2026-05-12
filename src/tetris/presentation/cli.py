"""CLI Typer (placeholder; se completa en Fase 7)."""

from __future__ import annotations

import typer

app = typer.Typer(no_args_is_help=False, add_completion=False)


@app.callback(invoke_without_command=True)
def main() -> None:
    """Stub que será reemplazado en la fase de presentación."""
    typer.echo("tetris — CLI en construcción")

"""Entrada `python -m tetris`."""

from tetris.presentation.cli import app


def main() -> None:
    """Despacha al CLI Typer."""
    app()


if __name__ == "__main__":
    main()

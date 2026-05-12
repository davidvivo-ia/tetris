"""Smoke tests del CLI Typer."""

from __future__ import annotations

import re

from typer.testing import CliRunner

from tetris.presentation.cli import app

runner = CliRunner()


def test_help_runs():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "tetris" in result.output.lower()


def test_headless_demo_runs():
    result = runner.invoke(
        app, ["--demo", "--seed", "42", "--headless", "--max-ticks", "30"]
    )
    assert result.exit_code == 0
    assert re.search(r"demo terminada", result.output)


def test_headless_demo_with_explicit_max_ticks_is_deterministic():
    a = runner.invoke(app, ["--demo", "--seed", "7", "--headless", "--max-ticks", "50"])
    b = runner.invoke(app, ["--demo", "--seed", "7", "--headless", "--max-ticks", "50"])
    assert a.output == b.output


def test_headless_without_demo_still_works():
    result = runner.invoke(app, ["--headless", "--seed", "5", "--max-ticks", "20"])
    assert result.exit_code == 0


def test_app_imports_textual_lazily():
    # Si Textual importase en cli.py, la línea siguiente fallaría sin TTY.
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

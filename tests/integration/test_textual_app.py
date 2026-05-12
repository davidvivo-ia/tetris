"""Pilot test del TetrisApp con Textual run_test (async)."""

from __future__ import annotations

import pytest

from tetris.presentation.tui.app import TetrisApp


@pytest.mark.asyncio
async def test_app_mounts_and_renders_game_screen():
    app = TetrisApp(seed=42)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.session is not None
        assert app.session.state.score == 0
        assert not app.session.state.game_over


@pytest.mark.asyncio
async def test_app_responds_to_movement_keys():
    app = TetrisApp(seed=42)
    async with app.run_test() as pilot:
        await pilot.pause()
        initial_x = app.session.state.active.x
        await pilot.press("left")
        await pilot.pause()
        assert app.session.state.active.x == initial_x - 1


@pytest.mark.asyncio
async def test_app_pause_toggle():
    app = TetrisApp(seed=42)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("p")
        await pilot.pause()
        assert app.session.state.paused
        await pilot.press("p")
        await pilot.pause()
        assert not app.session.state.paused


@pytest.mark.asyncio
async def test_app_restart():
    app = TetrisApp(seed=42)
    async with app.run_test() as pilot:
        await pilot.pause()
        for _ in range(5):
            await pilot.press("space")
            await pilot.pause()
        await pilot.press("r")
        await pilot.pause()
        assert app.session.state.score == 0
        assert app.session.state.lines == 0


@pytest.mark.asyncio
async def test_app_hard_drop_advances_state():
    app = TetrisApp(seed=42)
    async with app.run_test() as pilot:
        await pilot.pause()
        initial_kind = app.session.state.active.kind
        await pilot.press("space")
        await pilot.pause()
        # Tras un hard drop, debe haber spawn de la siguiente pieza
        assert (
            app.session.state.active.kind != initial_kind
            or app.session.state.game_over
        )

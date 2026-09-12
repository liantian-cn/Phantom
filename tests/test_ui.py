from __future__ import annotations

import asyncio
import re
from pathlib import Path
from threading import Event
from threading import enumerate as enumerate_threads

import numpy as np
import pytest
from textual.color import Color
from textual.widgets import Button, DataTable, Log, TabbedContent

from phantom.captures.contracts import CaptureResult, CaptureStatus, RGBImage
from phantom.core.configuration import AppConfig
from phantom.core.game import GameStatus
from phantom.ui.app import GameUpdated, PhantomApp
from phantom.ui.business_log import BusinessLog
from phantom.ui.capture import decode_general


class FakeCapture:
    def __init__(self) -> None:
        self.running: bool = False
        self.result: CaptureResult = CaptureResult()
        self.starts: int = 0
        self.stop_entered: Event = Event()
        self.stop_release: Event = Event()
        self.stop_release.set()

    @property
    def is_running(self) -> bool:
        return self.running

    def start(self) -> None:
        if not self.running:
            self.starts += 1
        self.running = True
        self.result = CaptureResult()

    def stop(self) -> None:
        self.stop_entered.set()
        assert self.stop_release.wait(5)
        self.running = False

    def set_fps(self, fps: float = 15) -> None:
        pass

    def get_latest_result(self) -> CaptureResult:
        return self.result


def general_image(values: tuple[int, ...] = (6, 1, 255, 0, 0)) -> RGBImage:
    image = np.zeros((20, 32, 3), dtype=np.uint8)
    for index, value in enumerate(values, start=1):
        image[0:4, index * 4 : index * 4 + 4] = value
    return image


def make_app(tmp_path: Path, capture: FakeCapture, game: bool = True) -> PhantomApp:
    return PhantomApp(
        AppConfig(tmp_path / "phantom.toml", log_max_lines=6),
        capture=capture,
        game_detector=lambda: GameStatus(game),
    )


def test_decode_five_cells_purity_and_invalid_input() -> None:
    image = general_image()
    data = decode_general(CaptureResult(image))
    assert (data.width, data.height) == (32, 20)
    assert data.cells == (
        ("6,6,6", "6"),
        ("1,1,1", "1"),
        ("255,255,255", "255"),
        ("0,0,0", "0"),
        ("0,0,0", "0"),
    )
    image[1, 5] = (255, 0, 0)
    mixed = decode_general(CaptureResult(image))
    assert mixed.cells[0] == ("255,0,0", "—")
    assert data.cells[0] == ("6,6,6", "6")
    with pytest.raises(ValueError):
        decode_general(CaptureResult(image, CaptureStatus(True, "坏帧")))
    with pytest.raises(ValueError):
        decode_general(CaptureResult())
    with pytest.raises(ValueError):
        decode_general(CaptureResult(image[:, :24]))


def test_business_log_deduplicates_body_before_timestamp() -> None:
    lines: list[str] = []
    business_log = BusinessLog(lines.append)
    for message in ("A", "A", "B", "A", "first\nsecond"):
        business_log.log(message)
    assert len(lines) == 4
    assert all(re.match(r"^\[\d{2}:\d{2}:\d{2}\] ", line) for line in lines)
    assert lines[0][11:] == "A"
    assert lines[2][11:] == "A"
    assert len(lines[3].splitlines()) == 2


def test_dark_mocha_theme_is_applied(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = make_app(tmp_path, FakeCapture())
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            theme = app.current_theme
            assert theme.name == "phantom-mocha"
            assert theme.dark
            assert theme.primary == "#89b4fa"
            assert app.screen.styles.background == Color.parse("#1e1e2e")
            assert app.query_one("#footer").styles.background == Color.parse("#181825")

    asyncio.run(scenario())


def test_tabs_keyboard_and_resizing_preserve_state(tmp_path: Path) -> None:
    async def scenario() -> None:
        capture = FakeCapture()
        app = make_app(tmp_path, capture)
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            assert not capture.running
            assert not app.query_one("#start", Button).disabled
            assert app.query_one("#generate", Button).disabled
            assert app.query_one("#footer").region.y == 45
            assert app.query_one("#footer").region.height == 1
            assert len(app.query_one("#footer").children) == 1
            pages = app.query_one("#pages", TabbedContent)
            for expected in ("general", "logs", "macros", "conditions", "overview"):
                await pilot.press("tab")
                assert pages.active == expected
            await pilot.press("shift+tab")
            assert pages.active == "conditions"
            await pilot.press("tab", "down", "space")
            assert app.collecting
            capture.result = CaptureResult(general_image())
            app.refresh_capture()
            await pilot.press("tab")
            await pilot.resize_terminal(119, 46)
            assert app.query_one("#size_notice").display
            assert not pages.display
            assert app.collecting
            await pilot.resize_terminal(140, 55)
            assert pages.display
            assert pages.active == "general"
            assert app.query_one("#footer").region.y == 54
            await pilot.press("shift+tab", "up", "enter")
            await pilot.pause()
            assert not app.collecting
            assert not capture.running
            await pilot.press("ctrl+q")
        assert not capture.running
        assert not any(thread.name == "phantom-game" for thread in enumerate_threads())

    asyncio.run(scenario())


def test_valid_failed_and_paused_data_never_reuse_old_frame(tmp_path: Path) -> None:
    async def scenario() -> None:
        capture = FakeCapture()
        app = make_app(tmp_path, capture)
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            await pilot.click("#start")
            table = app.query_one("#general_table", DataTable)
            capture.result = CaptureResult(general_image())
            app.refresh_capture()
            assert table.get_cell("0", "rgb") == "6,6,6"
            assert table.get_cell("2", "mean") == "255"
            assert all(table.get_cell(str(index), "display") == "" for index in range(5))
            capture.result = CaptureResult(general_image(), CaptureStatus(True, "校验失败"))
            app.refresh_capture()
            assert table.get_cell("0", "rgb") == "—"
            assert app.general_data is None
            capture.result = CaptureResult(general_image((3, 2, 0, 255, 255)))
            app.refresh_capture()
            assert table.get_cell("0", "mean") == "3"
            assert table.get_cell("3", "mean") == "255"
            await pilot.pause()
            assert any("采集已恢复" in line for line in app.query_one(Log).lines)
            await pilot.click("#stop")
            await pilot.pause()
            app.refresh_capture()
            assert table.get_cell("0", "rgb") == "—"
            assert all(table.get_cell(str(index), "display") == "" for index in range(5))
            await pilot.click("#start")
            app.refresh_capture()
            assert table.get_cell("0", "rgb") == "—"

    asyncio.run(scenario())


def test_game_loss_pauses_and_return_requires_manual_start(tmp_path: Path) -> None:
    async def scenario() -> None:
        capture = FakeCapture()
        app = make_app(tmp_path, capture, game=False)
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            assert app.query_one("#start", Button).disabled
            app.start_collection()
            assert capture.starts == 0
            app.post_message(GameUpdated(GameStatus(True)))
            await pilot.pause()
            await pilot.click("#start")
            capture.result = CaptureResult(general_image())
            app.refresh_capture()
            app.post_message(GameUpdated(GameStatus(False)))
            await pilot.pause()
            assert not app.collecting
            assert app.general_data is None
            assert app.query_one("#start", Button).disabled
            app.post_message(GameUpdated(GameStatus(True)))
            await pilot.pause()
            assert not app.collecting
            assert capture.starts == 1

    asyncio.run(scenario())


def test_slow_stop_keeps_ui_responsive_and_blocks_restart(tmp_path: Path) -> None:
    async def scenario() -> None:
        capture = FakeCapture()
        app = make_app(tmp_path, capture)
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            await pilot.click("#start")
            capture.stop_release.clear()
            try:
                await pilot.click("#stop")
                assert capture.stop_entered.is_set()
                assert app.stopping
                assert app.query_one("#start", Button).disabled
                await pilot.press("tab")
                assert app.query_one("#pages", TabbedContent).active == "general"
                app.start_collection()
                assert capture.starts == 1
            finally:
                capture.stop_release.set()
            await pilot.pause()
            assert not app.stopping
            assert not capture.running

    asyncio.run(scenario())


def test_capture_termination_pauses_and_explicit_restart_works(tmp_path: Path) -> None:
    async def scenario() -> None:
        capture = FakeCapture()
        app = make_app(tmp_path, capture)
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            await pilot.click("#start")
            capture.result = CaptureResult(status=CaptureStatus(True, "GDI 失败"))
            capture.running = False
            app.refresh_capture()
            await pilot.pause()
            assert not app.collecting
            assert app.capture_error == "GDI 失败"
            assert not app.query_one("#start", Button).disabled
            await pilot.click("#start")
            assert capture.starts == 2
            assert app.collecting

    asyncio.run(scenario())


def test_logs_bound_history_even_when_tab_hidden(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = make_app(tmp_path, FakeCapture())
        async with app.run_test(size=(120, 46)) as pilot:
            await pilot.pause()
            for index in range(12):
                app.business_log.log(f"事件 {index}")
                app.business_log.log(f"事件 {index}")
            await pilot.pause()
            log = app.query_one("#business_log", Log)
            assert len(log.lines) == 6
            assert log.lines[0].endswith("事件 6")
            assert log.lines[-1].endswith("事件 11")
            await pilot.press("tab", "tab")
            assert log.region.height > 20
            assert log.max_lines == 6

    asyncio.run(scenario())

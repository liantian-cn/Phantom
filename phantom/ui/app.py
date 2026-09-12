"""
Summary:
    承载 Phantom 采集启停、游戏状态与通用原始数据的 Textual 界面。
Description:
    content 展示五个标签页，底部 footer 只包含一行状态。
    游戏检测通过消息交付，采集读取最新快照；停止和退出等待后台资源释放。
Key Variables:
    PhantomApp.collecting: 程序采集开关，独立于 Lua ENABLE。
    PhantomApp.stopping: 后台正在释放截图资源，期间禁止再次启动。
    PhantomApp.business_log: 主动业务日志入口，与 Textual 诊断日志分离。
Change Log:
    2026-09-12: Added 第 5、6 步 Textual 界面与采集展示生命周期。
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import ClassVar

from rich.text import Text
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.geometry import Size
from textual.message import Message
from textual.widgets import Button, DataTable, Label, Log, Static, TabbedContent, TabPane

from phantom.captures.contracts import CaptureWorker
from phantom.core.configuration import AppConfig
from phantom.core.game import GameMonitor, GameStatus, detect_game
from phantom.ui.business_log import BusinessLog
from phantom.ui.capture import GENERAL_FIELDS, GeneralData, create_capture, decode_general
from phantom.ui.theme import FLEXOKI, PHANTOM_THEME


class GameUpdated(Message):
    def __init__(self, status: GameStatus) -> None:
        super().__init__()
        self.status: GameStatus = status


class BusinessLogLine(Message):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text: str = text


class CaptureStopped(Message):
    def __init__(self, error: str = "") -> None:
        super().__init__()
        self.error: str = error


class PageTabs(TabbedContent):
    def on_tab_pane_focused(self, event: TabPane.Focused) -> None:
        # 切页由 Tab/鼠标明确控制；延迟到达的旧页面焦点事件不能把新页面切回去。
        event.prevent_default()
        event.stop()


class PhantomApp(App[None]):
    CSS_PATH = "app.tcss"
    TITLE = "Phantom"
    AUTO_FOCUS = None
    ENABLE_COMMAND_PALETTE = False
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("tab", "switch_tab(1)", "下一页", show=False, priority=True),
        Binding("shift+tab", "switch_tab(-1)", "上一页", show=False, priority=True),
        Binding("up", "move_button(-1)", "上一个按钮", show=False, priority=True),
        Binding("down", "move_button(1)", "下一个按钮", show=False, priority=True),
        Binding("space", "press_button", "执行", show=False),
        Binding("ctrl+q", "quit", "退出", show=False, priority=True),
    ]
    TAB_IDS: ClassVar[tuple[str, ...]] = ("overview", "general", "logs", "macros", "conditions")

    def __init__(
        self,
        config: AppConfig,
        capture: CaptureWorker | None = None,
        game_detector: Callable[[], GameStatus] = detect_game,
    ) -> None:
        super().__init__()
        self.config: AppConfig = config
        self.capture: CaptureWorker = capture if capture is not None else create_capture(config.fps)
        self.game_status: GameStatus = GameStatus(description="正在检测游戏")
        self.collecting: bool = False
        self.stopping: bool = False
        self.closing: bool = False
        self.capture_state: str = "已暂停"
        self.capture_error: str = ""
        self.general_data: GeneralData | None = None
        self._mounted_ui: bool = False
        self._small: bool = False
        self.business_log: BusinessLog = BusinessLog(self._publish_log)
        self.game_monitor: GameMonitor = GameMonitor(self._publish_game, game_detector)
        self.register_theme(PHANTOM_THEME)
        self.theme = PHANTOM_THEME.name
        self.animation_level = "none"

    def _publish_game(self, status: GameStatus) -> None:
        self.post_message(GameUpdated(status))

    def _publish_log(self, text: str) -> None:
        self.post_message(BusinessLogLine(text))

    def compose(self) -> ComposeResult:
        with Vertical(id="content"):
            yield Static("", id="size_notice", markup=False)
            with PageTabs(initial="overview", id="pages"):
                with TabPane("综合", id="overview"):
                    with Horizontal(id="overview_columns"):
                        with VerticalScroll(id="controls"):
                            yield Label("操作", classes="section_title")
                            yield Button("启动", id="start", disabled=True)
                            yield Button("关闭", id="stop", disabled=True)
                            yield Button("生成插件", id="generate", disabled=True)
                            yield Static("插件生成尚未实现", classes="muted")
                            yield Static(
                                "Tab / Shift+Tab  切换页面\n"
                                "↑ / ↓  选择按钮\nEnter / Space  执行\nCtrl+Q  退出",
                                id="keyboard_help",
                            )
                        with VerticalScroll(id="work_status"):
                            yield Label("当前工作状态", classes="section_title")
                            for name, title in (
                                ("program_state", "程序"),
                                ("game_state", "游戏"),
                                ("capture_state", "采集"),
                                ("board_size", "画布尺寸"),
                                ("capture_fps", "配置 FPS"),
                                ("current_error", "当前问题"),
                            ):
                                yield Label(title, classes="state_label")
                                yield Static("—", id=name, classes="state_value", markup=False)
                with TabPane("通用条件", id="general"):
                    yield Static("第一行通用 Cell · 原始采集值", classes="section_title")
                    yield DataTable[str](id="general_table", cursor_type="row", zebra_stripes=True)
                with TabPane("日志", id="logs"):
                    yield Log(id="business_log", max_lines=self.config.log_max_lines)
                with TabPane("宏绑定", id="macros"):
                    yield Static("宏绑定展示尚未实现", classes="placeholder")
                with TabPane("循环条件", id="conditions"):
                    yield Static("循环条件展示尚未实现", classes="placeholder")
        with Container(id="footer"):
            yield Static("", id="status_line")

    def on_mount(self) -> None:
        for button in self.query(Button):
            button.active_effect_duration = 0
        table = self.query_one("#general_table", DataTable)
        for title, key, width in (
            ("项目", "name", 22),
            ("RGB", "rgb", 22),
            ("亮度值", "mean", 16),
            ("显示值", "display", 26),
        ):
            table.add_column(title, key=key, width=width)
        for index, name in enumerate(GENERAL_FIELDS):
            table.add_row(name, "—", "—", "", key=str(index))
        self._mounted_ui = True
        self._resize_content()
        self._refresh_status()
        self.game_monitor.start()
        self.set_interval(1 / self.config.fps, self.refresh_capture)
        self.business_log.log("程序已暂停")

    def on_resize(self, event: events.Resize) -> None:
        if self._mounted_ui:
            self._resize_content(event.size)

    def _resize_content(self, size: Size | None = None) -> None:
        viewport = self.size if size is None else size
        was_small = self._small
        self._small = (
            viewport.width < self.config.min_width or viewport.height < self.config.min_height
        )
        self.query_one("#size_notice", Static).update(
            f"终端尺寸不足：当前 {viewport.width}×{viewport.height}\n"
            f"请调整至至少 {self.config.min_width}×{self.config.min_height}\n"
            "Ctrl+Q 退出"
        )
        self.query_one("#size_notice").display = self._small
        self.query_one("#pages").display = not self._small
        if not self._small and (was_small or self.focused is None):
            self.call_after_refresh(self._focus_page)

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action in ("move_button", "press_button"):
            return (
                self._mounted_ui
                and not self._small
                and self.query_one("#pages", TabbedContent).active == "overview"
            )
        if action == "switch_tab":
            return self._mounted_ui and not self._small
        return True

    def action_switch_tab(self, direction: int) -> None:
        pages = self.query_one("#pages", TabbedContent)
        index = self.TAB_IDS.index(pages.active)
        pages.active = self.TAB_IDS[(index + direction) % len(self.TAB_IDS)]

    @on(TabbedContent.TabActivated)
    def tab_activated(self) -> None:
        if self._mounted_ui and not self._small:
            self.call_after_refresh(self._focus_page)

    def _focus_page(self) -> None:
        if self._small or self.closing:
            return
        active = self.query_one("#pages", TabbedContent).active
        if active == "overview":
            self.action_move_button(1)
        elif active == "general":
            self.query_one("#general_table", DataTable).focus()
        elif active == "logs":
            self.query_one("#business_log", Log).focus()

    def action_move_button(self, direction: int) -> None:
        buttons = [button for button in self.query("#controls Button") if not button.disabled]
        if not buttons:
            return
        if self.focused in buttons:
            index = buttons.index(self.focused)
            buttons[(index + direction) % len(buttons)].focus()
        else:
            buttons[0 if direction > 0 else -1].focus()

    def action_press_button(self) -> None:
        if isinstance(self.focused, Button):
            self.focused.press()

    @on(Button.Pressed, "#start")
    def start_collection(self) -> None:
        if self.collecting or self.stopping or self.closing or not self.game_status.running:
            return
        self.capture.start()
        self.collecting = True
        self._set_capture_state("等待截图")
        self.business_log.log("程序已启动")
        self._refresh_status()
        if not self._small:
            self.query_one("#stop", Button).focus()

    @on(Button.Pressed, "#stop")
    def stop_collection(self) -> None:
        self._request_stop()

    def _request_stop(self, error: str = "") -> None:
        if not self.collecting:
            return
        self.collecting = False
        self.stopping = True
        self._show_data(None)
        self._set_capture_state("采集失败" if error else "已暂停", error)
        self.business_log.log("程序已暂停")
        self._refresh_status()
        self._stop_capture()

    @work(thread=True, group="capture-stop")
    def _stop_capture(self) -> None:
        error = ""
        try:
            self.capture.stop()
        except Exception as exception:
            error = f"停止采集失败：{exception}"
        self.post_message(CaptureStopped(error))

    def on_capture_stopped(self, message: CaptureStopped) -> None:
        if self.closing:
            return
        self.stopping = False
        if message.error:
            self._set_capture_state("采集失败", message.error)
        self._refresh_status()
        if not self._small and self.query_one("#pages", TabbedContent).active == "overview":
            self._focus_page()

    def on_game_updated(self, message: GameUpdated) -> None:
        if self.closing or message.status == self.game_status:
            return
        self.game_status = message.status
        state = "已启动" if message.status.running else "未启动"
        self.business_log.log(
            f"游戏{state}"
            + (f"：{message.status.description}" if message.status.description else "")
        )
        if not message.status.running:
            self._request_stop()
        self._refresh_status()
        if self.focused is None and not self._small:
            self.call_after_refresh(self._focus_page)

    def on_business_log_line(self, message: BusinessLogLine) -> None:
        if not self.closing:
            self.query_one("#business_log", Log).write_lines(message.text.splitlines())

    def refresh_capture(self) -> None:
        if not self.collecting or self.closing:
            return
        # 先检查存活，再取结果，保证线程结束时能读取它发布的最后错误。
        running = self.capture.is_running
        result = self.capture.get_latest_result()
        if not running:
            self._request_stop(result.status.description or "截图线程已结束")
            return
        if result.status.has_error:
            self._show_data(None)
            self._set_capture_state("采集失败", result.status.description)
        elif result.image is None:
            self._show_data(None)
            self._set_capture_state("等待截图")
        else:
            try:
                data = decode_general(result)
            except (ValueError, TypeError, IndexError) as error:
                self._show_data(None)
                self._set_capture_state("解析失败", f"通用数据解析失败：{error}")
            else:
                self._show_data(data)
                self._set_capture_state("采集正常")
        self._refresh_status()

    def _set_capture_state(self, state: str, error: str = "") -> None:
        previous_error = self.capture_error
        if error and error != previous_error:
            self.business_log.log(error)
        elif state == "采集正常" and previous_error:
            self.business_log.log("采集已恢复")
        self.capture_state = state
        self.capture_error = error

    def _show_data(self, data: GeneralData | None) -> None:
        if data == self.general_data:
            return
        self.general_data = data
        table = self.query_one("#general_table", DataTable)
        for index in range(5):
            rgb, mean = data.cells[index] if data is not None else ("—", "—")
            table.update_cell(str(index), "rgb", rgb)
            table.update_cell(str(index), "mean", mean)

    def _refresh_status(self) -> None:
        program = "已启动" if self.collecting else "已暂停"
        game = "已启动" if self.game_status.running else "未启动"
        status = Text()
        status.append(
            f"程序：{program}", style=FLEXOKI["green" if self.collecting else "subtext_1"]
        )
        status.append(" · ", style=FLEXOKI["text"])
        status.append(
            f"游戏：{game}", style=FLEXOKI["green" if self.game_status.running else "subtext_1"]
        )
        self.query_one("#status_line", Static).update(status)
        values = {
            "program_state": "正在停止" if self.stopping else program,
            "game_state": game,
            "capture_state": self.capture_state,
            "board_size": (
                f"{self.general_data.width} × {self.general_data.height} px"
                if self.general_data is not None
                else "—"
            ),
            "capture_fps": f"{self.config.fps:g}",
            "current_error": self.capture_error or self.game_status.description or "无",
        }
        for identifier, value in values.items():
            self.query_one(f"#{identifier}", Static).update(value)
        self.query_one("#start", Button).disabled = (
            self.collecting or self.stopping or self.closing or not self.game_status.running
        )
        self.query_one("#stop", Button).disabled = not self.collecting or self.closing

    def close_resources(self) -> None:
        try:
            self.game_monitor.stop()
        finally:
            self.capture.stop()

    async def action_quit(self) -> None:
        if self.closing:
            return
        self.closing = True
        self.collecting = False
        self._show_data(None)
        self._refresh_status()
        self._finish_exit()

    @work
    async def _finish_exit(self) -> None:
        await asyncio.to_thread(self.close_resources)
        self.exit()

    async def on_unmount(self) -> None:
        self.closing = True
        self.collecting = False
        await asyncio.to_thread(self.close_resources)

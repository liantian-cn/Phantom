"""
Summary:
    将明确的按键组合发送到标题恰好为魔兽世界的唯一窗口。
Description:
    沿用用户提供的 keyboard.py：PostMessageW 普通按键消息、零 lParam、10 ms 按住。
    目标发现和 Windows 虚拟键映射属于本插件；核心不传入 HWND 或宏文本。
    API 成功表示消息已入队，不保证游戏已经执行。中途失败仍尝试释放已按下的键。
Key Variables:
    VIRTUAL_KEYS: 中立按键标识到 Windows 虚拟键的映射。
Change Log:
    2026-09-14: Added 第一个版本化键盘后端，参考 EZWowX2 Terminal/terminal/keyboard.py。
"""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from time import sleep

from phantom.core.keyboard.contracts import Key, KeyCombination

VIRTUAL_KEYS: dict[Key, int] = {
    Key.CTRL: 0x11,
    Key.ALT: 0x12,
    Key.SHIFT: 0x10,
    Key.UP: 0x26,
    Key.DOWN: 0x28,
    Key.LEFT: 0x25,
    Key.RIGHT: 0x27,
    Key.HOME: 0x24,
    Key.END: 0x23,
    Key.PAGEUP: 0x21,
    Key.PAGEDOWN: 0x22,
    Key.INSERT: 0x2D,
    Key.DELETE: 0x2E,
    Key.SPACE: 0x20,
    Key.TAB: 0x09,
    Key.ENTER: 0x0D,
    Key.ESCAPE: 0x1B,
    Key.BACKSPACE: 0x08,
    Key.NUMPADPLUS: 0x6B,
    Key.NUMPADMINUS: 0x6D,
    Key.NUMPADMULTIPLY: 0x6A,
    Key.NUMPADDIVIDE: 0x6F,
    Key.NUMPADDECIMAL: 0x6E,
    Key.COMMA: 0xBC,
    Key.PERIOD: 0xBE,
    Key.SLASH: 0xBF,
    Key.SEMICOLON: 0xBA,
    Key.QUOTE: 0xDE,
    Key.LEFTBRACKET: 0xDB,
    Key.RIGHTBRACKET: 0xDD,
    Key.BACKSLASH: 0xDC,
    Key.EQUALS: 0xBB,
    Key.MINUS: 0xBD,
    Key.GRAVE: 0xC0,
}
VIRTUAL_KEYS.update(
    {Key(character): ord(character) for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"}
)
VIRTUAL_KEYS.update({Key(f"F{number}"): 0x6F + number for number in range(1, 25)})
VIRTUAL_KEYS.update({Key(f"NUMPAD{number}"): 0x60 + number for number in range(10)})


class WindowsMessages:
    def __init__(self) -> None:
        if sys.platform != "win32":
            raise OSError("PostMessageW 需要 Windows")
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        self.user32.EnumWindows.argtypes = [self.callback_type, wintypes.LPARAM]
        self.user32.EnumWindows.restype = wintypes.BOOL
        self.user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        self.user32.GetWindowTextLengthW.restype = ctypes.c_int
        self.user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        self.user32.GetWindowTextW.restype = ctypes.c_int
        self.user32.PostMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.PostMessageW.restype = wintypes.BOOL

    def target(self) -> int:
        matches: list[int] = []

        def visit(hwnd: int, parameter: int) -> bool:
            length = self.user32.GetWindowTextLengthW(hwnd)
            buffer = ctypes.create_unicode_buffer(length + 1)
            self.user32.GetWindowTextW(hwnd, buffer, len(buffer))
            if buffer.value == "魔兽世界":
                matches.append(hwnd)
            return True

        if not self.user32.EnumWindows(self.callback_type(visit), 0):
            raise ctypes.WinError(ctypes.get_last_error())
        if len(matches) != 1:
            raise OSError(f"标题为“魔兽世界”的窗口必须唯一，实际找到 {len(matches)} 个")
        return matches[0]

    def post(self, hwnd: int, message: int, key: int) -> None:
        if not self.user32.PostMessageW(hwnd, message, key, 0):
            raise ctypes.WinError(ctypes.get_last_error())


class Plugin:
    def __init__(self) -> None:
        self._messages: WindowsMessages | None = None

    def send(self, keys: KeyCombination) -> None:
        if self._messages is None:
            self._messages = WindowsMessages()
        target = self._messages.target()
        pressed: list[int] = []
        failure: Exception | None = None
        try:
            for key in keys.keys:
                virtual_key = VIRTUAL_KEYS[key]
                self._messages.post(target, 0x0100, virtual_key)
                pressed.append(virtual_key)
            sleep(0.01)
        except Exception as error:
            failure = error
        finally:
            for virtual_key in reversed(pressed):
                try:
                    self._messages.post(target, 0x0101, virtual_key)
                except Exception as error:
                    if failure is None:
                        failure = error
                    else:
                        failure.add_note(f"释放键 {virtual_key} 失败：{error}")
        if failure is not None:
            raise failure

    def close(self) -> None:
        # send 始终完成释放尝试；本后端不拥有目标窗口或持续按键状态。
        self._messages = None

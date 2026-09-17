from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes
from pathlib import Path
from types import ModuleType
from typing import Any
from uuid import uuid4

import pytest

from phantom.core.configuration import load_config
from phantom.core.keyboard.contracts import Key, parse_key
from phantom.core.keyboard.registry import KeyboardPluginError, Registry


def backend_module() -> ModuleType:
    plugin = Registry().create()
    return sys.modules[type(plugin).__module__]


@pytest.mark.parametrize(
    ("source", "keys"),
    [
        ("CTRL-1", (Key.CTRL, Key.DIGIT1)),
        ("ALT-F4", (Key.ALT, Key.F4)),
        ("SHIFT-CTRL-NUMPAD1", (Key.SHIFT, Key.CTRL, Key.NUMPAD1)),
        ("CTRL--", (Key.CTRL, Key.MINUS)),
        ("-", (Key.MINUS,)),
        ("F24", (Key.F24,)),
        ("CTRL-;", (Key.CTRL, Key.SEMICOLON)),
        ("NUMPADPLUS", (Key.NUMPADPLUS,)),
    ],
)
def test_key_combinations(source: str, keys: tuple[Key, ...]) -> None:
    assert parse_key(source).keys == keys


@pytest.mark.parametrize("source", ["", "ctrl-1", "CTRL-CTRL-A", "CTRL", "A-B", "F25", "CTRL+1", "CTRL-", "ALT--A", " M", "BUTTON1"])
def test_invalid_keys(source: str) -> None:
    with pytest.raises(ValueError):
        parse_key(source)


def test_windows_mapping_covers_every_key() -> None:
    mapping = backend_module().VIRTUAL_KEYS
    assert set(mapping) == set(Key)
    assert [mapping[key] for key in parse_key("CTRL-1").keys] == [0x11, 0x31]
    assert mapping[Key.F24] == 0x87
    assert mapping[Key.NUMPAD9] == 0x69
    assert mapping[Key.SEMICOLON] == 0xBA


class RecordingMessages:
    def __init__(self, fail_at: int = 0) -> None:
        self.calls: list[tuple[int, int, int]] = []
        self.fail_at: int = fail_at

    def target(self) -> int:
        return 123

    def post(self, hwnd: int, message: int, key: int) -> None:
        self.calls.append((hwnd, message, key))
        if len(self.calls) == self.fail_at:
            raise OSError("post failed")


@pytest.mark.parametrize("fail_at", [0, 2, 4])
def test_send_order_and_failure_release(monkeypatch: pytest.MonkeyPatch, fail_at: int) -> None:
    plugin = Registry().create()
    module = sys.modules[type(plugin).__module__]
    messages = RecordingMessages(fail_at)
    sleeps: list[float] = []
    monkeypatch.setattr(module, "WindowsMessages", lambda: messages)
    monkeypatch.setattr(module, "sleep", sleeps.append)
    if fail_at:
        with pytest.raises(OSError, match="post failed"):
            plugin.send(parse_key("CTRL-ALT-F4"))
    else:
        plugin.send(parse_key("CTRL-ALT-F4"))
    expected = [(123, 0x100, 0x11), (123, 0x100, 0x12)]
    if fail_at == 2:
        expected += [(123, 0x101, 0x11)]
        assert sleeps == []
    else:
        expected += [(123, 0x100, 0x73), (123, 0x101, 0x73), (123, 0x101, 0x12), (123, 0x101, 0x11)]
        assert sleeps == [0.01]
    assert messages.calls == expected
    plugin.close()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows API callback type")
@pytest.mark.parametrize("titles, expected", [(["魔兽世界"], 1), (["魔兽世界测试"], None), (["魔兽世界", "魔兽世界"], None)])
def test_target_requires_unique_exact_title(titles: list[str], expected: int | None) -> None:
    messages: Any = backend_module().WindowsMessages()

    class FakeUser32:
        def EnumWindows(self, callback: Any, parameter: int) -> bool:
            for index in range(len(titles)):
                callback(index + 1, parameter)
            return True

        def GetWindowTextLengthW(self, hwnd: int) -> int:
            return len(titles[hwnd - 1])

        def GetWindowTextW(self, hwnd: int, buffer: Any, length: int) -> int:
            buffer.value = titles[hwnd - 1]
            return len(buffer.value)

    messages.user32 = FakeUser32()
    if expected is None:
        with pytest.raises(OSError, match="必须唯一"):
            messages.target()
    else:
        assert messages.target() == expected


def test_registry_and_configuration(tmp_path: Path) -> None:
    registry = Registry()
    first, second = registry.create(), registry.create()
    assert first is not second and type(first) is type(second)
    for identifier in ("../bad", "x/y", "x\\y", "x:stream", "x.", "x ", "post_message@1", ""):
        with pytest.raises(KeyboardPluginError):
            registry.create(identifier)
    config = load_config(tmp_path)
    assert config.keyboard_plugin == "post_message@dev"
    config.path.write_text('[keyboard]\nplugin="other@dev"', encoding="utf-8")
    assert load_config(tmp_path).keyboard_plugin == "other@dev"
    with pytest.raises(KeyboardPluginError):
        registry.create(load_config(tmp_path).keyboard_plugin)


@pytest.mark.parametrize("source", ["Plugin = 0", "raise RuntimeError('broken')", "class Plugin:\n    pass", "class Plugin:\n    def send(self): pass\n    def close(self): pass"])
def test_invalid_plugin_interface(tmp_path: Path, source: str) -> None:
    directory = tmp_path / "broken@dev"
    directory.mkdir()
    (directory / "keyboard.py").write_text(source, encoding="utf-8")
    with pytest.raises(KeyboardPluginError, match="broken@dev"):
        Registry(tmp_path).create("broken@dev")


@pytest.mark.skipif(sys.platform != "win32", reason="real Windows message queue")
def test_real_post_message_to_owned_hidden_window(monkeypatch: pytest.MonkeyPatch) -> None:
    module = backend_module()
    messages: Any = module.WindowsMessages()
    user32 = messages.user32
    user32.CreateWindowExW.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID]
    user32.CreateWindowExW.restype = wintypes.HWND
    user32.DestroyWindow.argtypes = [wintypes.HWND]
    user32.DestroyWindow.restype = wintypes.BOOL
    user32.PeekMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.UINT]
    user32.PeekMessageW.restype = wintypes.BOOL
    hwnd = user32.CreateWindowExW(0, "STATIC", "Phantom-test-" + uuid4().hex, 0, 0, 0, 1, 1, None, None, None, None)
    assert hwnd, ctypes.WinError(ctypes.get_last_error())
    try:
        # Only the test-owned HWND can receive these messages; no game enumeration.
        monkeypatch.setattr(messages, "target", lambda: hwnd)
        monkeypatch.setattr(module, "WindowsMessages", lambda: messages)
        plugin: Any = module.Plugin()
        plugin.send(parse_key("CTRL-1"))
        plugin.send(parse_key("ALT-F4"))
        received: list[tuple[int, int, int]] = []
        message = wintypes.MSG()
        while user32.PeekMessageW(ctypes.byref(message), hwnd, 0x100, 0x101, 1):
            received.append((message.message, message.wParam, message.lParam))
        assert received == [(0x100, 0x11, 0), (0x100, 0x31, 0), (0x101, 0x31, 0), (0x101, 0x11, 0), (0x100, 0x12, 0), (0x100, 0x73, 0), (0x101, 0x73, 0), (0x101, 0x12, 0)]
        plugin.close()
    finally:
        assert user32.DestroyWindow(hwnd)

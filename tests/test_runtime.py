from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from threading import Event, Thread
from time import monotonic, sleep

import numpy as np
import pytest

from phantom.core.capture.contracts import CaptureResult, CaptureStatus
from phantom.core.capture.registry import Registry as CaptureRegistry
from phantom.core.keyboard.contracts import KeyCombination
from phantom.core.keyboard.registry import Registry as KeyboardRegistry
from phantom.core.pixels import PixelDecoder
from phantom.core.rotation import Rotation, load_rotation
from phantom.core.runtime import RotationRuntime


def wait_for(predicate: Callable[[], bool]) -> None:
    deadline = monotonic() + 3
    while not predicate():
        assert monotonic() < deadline, "runtime did not publish expected result"
        sleep(0.005)


def rotation_copy(tmp_path: Path) -> Rotation:
    path = tmp_path / "blood.toml"
    path.write_bytes(Path("rotations/blood-dk.toml").read_bytes())
    return load_rotation(path)


def frame(sequence: int, enabled: int = 255, delaying: int = 0) -> CaptureResult:
    image = np.zeros((20, 36, 3), dtype=np.uint8)
    for index, value in enumerate((6, 1, enabled, 0, delaying), 1):
        image[:4, index * 4 : index * 4 + 4] = value
    image[4:8, 20:24] = 255  # 死神的抚摩 ready; other rules do not match.
    return CaptureResult(image, sequence=sequence)


class Capture:
    def __init__(self) -> None:
        self.result: CaptureResult = CaptureResult()
        self.is_running: bool = True

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def set_fps(self, fps: float = 15) -> None:
        pass

    def get_latest_result(self) -> CaptureResult:
        return self.result


class Keyboard:
    def __init__(self) -> None:
        self.sent: list[KeyCombination] = []
        self.closed: bool = False
        self.entered: Event = Event()
        self.release: Event = Event()
        self.release.set()
        self.fail: bool = False

    def send(self, keys: KeyCombination) -> None:
        self.sent.append(keys)
        self.entered.set()
        assert self.release.wait(3)
        if self.fail:
            raise OSError("keyboard failed")

    def close(self) -> None:
        self.closed = True


def test_new_frames_idle_recovery_and_same_decision(tmp_path: Path) -> None:
    capture, keyboard = Capture(), Keyboard()
    runtime = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    runtime.start()
    try:
        capture.result = frame(1)
        wait_for(lambda: runtime.get_latest_result().decision is not None)
        decision = runtime.get_latest_result().decision
        assert decision is not None and decision.macro is not None
        assert keyboard.sent == [decision.macro.keys]
        sleep(0.05)
        assert len(keyboard.sent) == 1
        capture.result = frame(2)  # identical pixels, distinct capture
        wait_for(lambda: len(keyboard.sent) == 2)
        capture.result = frame(3, enabled=0)
        wait_for(lambda: runtime.get_latest_result().capture.sequence == 3)
        decision = runtime.get_latest_result().decision
        assert decision is not None and decision.macro is None
        assert decision.rule_index == 1
        capture.result = CaptureResult(status=CaptureStatus(True, "bad frame"), sequence=4)
        wait_for(lambda: runtime.get_latest_result().capture.sequence == 4)
        assert runtime.get_latest_result().decision is None
        capture.result = frame(5, delaying=255)
        wait_for(lambda: runtime.get_latest_result().capture.sequence == 5)
        assert len(keyboard.sent) == 2
        capture.result = frame(6)
        wait_for(lambda: len(keyboard.sent) == 3)
    finally:
        runtime.stop()
    assert keyboard.closed


def test_stop_waits_for_release_and_drops_backlog(tmp_path: Path) -> None:
    capture, keyboard = Capture(), Keyboard()
    keyboard.release.clear()
    capture.result = frame(1)
    runtime = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    runtime.start()
    stopped = Event()

    def stop_runtime() -> None:
        runtime.stop()
        stopped.set()

    stopper = Thread(target=stop_runtime)
    try:
        assert keyboard.entered.wait(3)
        capture.result = frame(2)
        runtime.request_stop()
        stopper.start()
        assert not stopped.wait(0.05)
    finally:
        keyboard.release.set()
        runtime.stop()
        if stopper.ident is not None:
            stopper.join()
    assert len(keyboard.sent) == 1 and keyboard.closed
    # Restart is a new run, so the latest frame may be considered again.
    restarted = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    restarted.start()
    try:
        wait_for(lambda: len(keyboard.sent) == 2)
    finally:
        restarted.stop()


def test_send_failure_stops_without_retry(tmp_path: Path) -> None:
    capture, keyboard = Capture(), Keyboard()
    keyboard.fail = True
    capture.result = frame(1)
    runtime = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    runtime.start()
    try:
        wait_for(lambda: runtime.get_latest_result().fatal)
        assert "keyboard failed" in runtime.get_latest_result().error
        capture.result = frame(2)
        sleep(0.04)
        assert len(keyboard.sent) == 1
    finally:
        runtime.stop()


def test_builtin_values_and_unreferenced_invalid_fields(tmp_path: Path) -> None:
    rotation = rotation_copy(tmp_path)
    result = frame(1)
    assert result.image is not None
    result.image[:4, 16:20] = 123  # burst is not referenced by the example
    assert rotation.trial(PixelDecoder(result.image)).macro is not None
    result.image[1, 13] = 254
    with pytest.raises(ValueError, match="插件启用"):
        rotation.trial(PixelDecoder(result.image))
    ungated = replace(rotation, rules=rotation.rules[1:])
    assert ungated.trial(PixelDecoder(result.image)).macro is not None


def test_reserved_builtin_name_rejected_before_write(tmp_path: Path) -> None:
    path = tmp_path / "blood.toml"
    source = Path("rotations/blood-dk.toml").read_text(encoding="utf-8")
    source = source.replace('title = "符文能量"', 'title = "插件启用"')
    path.write_text(source, encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(ValueError, match="条件标题"):
        load_rotation(path)
    assert path.read_bytes() == before


@pytest.mark.parametrize("sequence", [None, 0, -1, True])
def test_runtime_rejects_unusable_frame_identity(tmp_path: Path, sequence: int | None) -> None:
    capture, keyboard = Capture(), Keyboard()
    capture.result = replace(frame(1), sequence=sequence)
    runtime = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    runtime.start()
    try:
        wait_for(lambda: runtime.get_latest_result().fatal)
        assert not keyboard.sent
    finally:
        runtime.stop()


def test_exact_capture_and_keyboard_plugins_in_continuous_loop(tmp_path: Path) -> None:
    capture_directory = tmp_path / "captures/test.capture@dev"
    keyboard_directory = tmp_path / "keyboards/test.keyboard@dev"
    capture_directory.mkdir(parents=True)
    keyboard_directory.mkdir(parents=True)
    # Exact-loaded synthetic producer uses the real shared capture worker and pixel protocol.
    (capture_directory / "capture.py").write_text(
        """
import numpy as np
from phantom.core.capture.contracts import Bounds
from phantom.core.capture.worker import ThreadCaptureWorker
class Backend:
    def desktop_bounds(self): return Bounds(0,0,36,20)
    def capture(self, bounds):
        image = np.zeros((20,36,3), dtype=np.uint8)
        for y in range(4):
            for x in range(4):
                color = (15,25,20) if (x//2+y//2)%2==0 else (25,15,20)
                image[y,x] = color
                image[16+y,32+x] = color
        for y,color in enumerate(((0,255,255),(255,0,255),(255,255,0),(0,0,0))):
            image[(y+1)*4:(y+2)*4,:4] = color
        for y,color in enumerate(((127,127,127),(0,0,255),(0,255,0),(255,0,0))):
            image[y*4:(y+1)*4,-4:] = color
        for x,value in enumerate((6,1,255,0,0),1): image[:4,x*4:x*4+4] = value
        image[4:8,20:24] = 255
        return image
    def close(self): pass
class Plugin(ThreadCaptureWorker):
    def __init__(self, fps=15): super().__init__(Backend, fps)
""",
        encoding="utf-8",
    )
    (keyboard_directory / "keyboard.py").write_text(
        """
class Plugin:
    def __init__(self): self.sent = []; self.closed = False
    def send(self, keys): self.sent.append(keys)
    def close(self): self.closed = True
""",
        encoding="utf-8",
    )
    capture = CaptureRegistry(tmp_path / "captures").create("test.capture@dev", fps=40)
    keyboard = KeyboardRegistry(tmp_path / "keyboards").create("test.keyboard@dev")
    runtime = RotationRuntime(capture, keyboard, rotation_copy(tmp_path), 100)
    capture.start()
    runtime.start()
    try:
        wait_for(lambda: len(getattr(keyboard, "sent")) >= 3)
        snapshot = runtime.get_latest_result()
        assert snapshot.decision is not None and snapshot.decision.macro is not None
        assert snapshot.decision.macro.name == "死神的抚摩"
        assert not snapshot.capture.status.has_error
        assert snapshot.capture.sequence is not None
    finally:
        runtime.stop()
        capture.stop()
    assert getattr(keyboard, "closed")

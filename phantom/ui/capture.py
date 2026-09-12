"""
Summary:
    将现有 GDI worker 与同帧通用 Cell 数据接入 TUI。
Description:
    明确加载已实现的 gdi@1.0，不提前引入通用插件发现。
    仅接收有效截图，将五个 Cell 原始值一次性转换为表格展示数据。
Key Variables:
    GENERAL_FIELDS: 第一行五个已有通用 Cell 的固定展示顺序。
Change Log:
    2026-09-12: Added 第 6 步采集展示适配。
"""

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from phantom.captures.contracts import CaptureResult, CaptureWorker
from phantom.core.pixels import PixelDecoder

GENERAL_FIELDS = ("玩家职业", "玩家专精", "Lua 启动状态", "爆发开关", "延迟开关")


@dataclass(frozen=True)
class GeneralData:
    width: int
    height: int
    cells: tuple[tuple[str, str], ...]


def create_capture(fps: float) -> CaptureWorker:
    source = Path(__file__).resolve().parents[1] / "captures/gdi@1.0/capture.py"
    spec = importlib.util.spec_from_file_location("phantom_gdi_capture", source)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载截图后端：{source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(CaptureWorker, module.GDIWorker(fps=fps))


def decode_general(result: CaptureResult) -> GeneralData:
    if result.status.has_error:
        raise ValueError(result.status.description)
    if result.image is None:
        raise ValueError("尚无有效截图")
    decoder = PixelDecoder(result.image)
    cells = [decoder.getCell(index, 1) for index in range(1, 6)]
    return GeneralData(
        width=result.image.shape[1],
        height=result.image.shape[0],
        cells=tuple(
            (cell.color_string, f"{cell.mean:g}" if cell.is_pure else "—") for cell in cells
        ),
    )

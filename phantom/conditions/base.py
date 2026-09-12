"""
Summary:
    校验条件输出、冻结布局并将同一截图的区域转换为业务值。
Description:
    插件声明区域数量和业务类型；布局器独立排列三类输出。
    基类提取区域并保护解码边界，插件作者定义参数、Lua 与兜底语义。
Key Variables:
    Output: 不可变的输出数量、数值类型及数值条宽度。
    Region: 与 Lua 构造器一致的区域坐标。
Change Log:
    2026-09-12: Added 第 8 步条件生命周期与多区域布局。
"""

from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from phantom.core.pixels import Cell, IconTile, PixelDecoder, ValueBar

type Scalar = bool | int | float | str
type Value = Scalar | list[Scalar]
type Raw = tuple[list[Cell], list[ValueBar], list[IconTile]]
type OutputType = Literal["cell", "value_bar", "icon_tile"]


@dataclass(frozen=True)
class Output:
    output_type: OutputType
    output_count: int = 1
    value_type: type[bool] | type[int] | type[float] | type[str] = float
    value_shape: Literal["scalar", "list"] = "scalar"
    widths: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if self.output_type not in ("cell", "value_bar", "icon_tile"):
            raise ValueError("未知输出类型")
        if type(self.output_count) is not int or self.output_count < 1:
            raise ValueError("输出数量必须为正整数")
        if self.value_type not in (bool, int, float, str):
            raise ValueError("未知业务值类型")
        if self.value_shape not in ("scalar", "list"):
            raise ValueError("未知业务值形状")
        if self.output_type == "value_bar":
            if len(self.widths) != self.output_count or any(
                type(width) is not int or width < 1 for width in self.widths
            ):
                raise ValueError("每条 ValueBar 必须声明正整数内容宽度")
        elif self.widths:
            raise ValueError("只有 ValueBar 可以声明宽度")

    def accepts(self, value: Value) -> bool:
        if self.value_shape == "list":
            return isinstance(value, list) and all(type(item) is self.value_type for item in value)
        return type(value) is self.value_type


@dataclass(frozen=True)
class Region:
    x: int
    y: int | None = None
    width: int | None = None

    def metadata(self) -> dict[str, int]:
        result = {"x": self.x}
        if self.y is not None:
            result["y"] = self.y
        if self.width is not None:
            result["width"] = self.width
        return result


class Condition(ABC):
    def __init__(self, output: Output) -> None:
        self._output: Output = output
        self._regions: tuple[Region, ...] = ()
        self._template: Path | None = None

    @property
    def output(self) -> Output:
        return self._output

    @property
    def regions(self) -> tuple[Region, ...]:
        return self._regions

    def freeze(self, regions: tuple[Region, ...]) -> None:
        if self._regions:
            raise ValueError("条件布局已冻结")
        if len(regions) != self.output.output_count:
            raise ValueError("布局数量与输出声明不符")
        if not self.output.accepts(self.fallback_value()):
            raise ValueError("插件兜底与业务类型声明不符")
        self._regions = regions

    def set_template(self, path: Path) -> None:
        self._template = path

    def layout(self) -> dict[str, object]:
        return {
            "output_type": self.output.output_type,
            "regions": [region.metadata() for region in self.regions],
        }

    def raw_value(self, decoder: PixelDecoder) -> Raw:
        if not self.regions:
            raise ValueError("条件尚未分配布局")
        cells: list[Cell] = []
        bars: list[ValueBar] = []
        icons: list[IconTile] = []
        for region in self.regions:
            if self.output.output_type == "cell":
                assert region.y is not None
                cells.append(decoder.getCell(region.x, region.y))
            elif self.output.output_type == "value_bar":
                assert region.width is not None
                bars.append(decoder.getValueBar(region.x, region.width))
            else:
                icons.append(decoder.getIconTile(region.x))
        return cells, bars, icons

    def value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> Value:
        try:
            lengths = {
                "cell": len(cells),
                "value_bar": len(value_bars),
                "icon_tile": len(icon_tiles),
            }
            if any(
                length != (self.output.output_count if kind == self.output.output_type else 0)
                for kind, length in lengths.items()
            ):
                raise ValueError("输入区域数量与输出声明不符")
            result = self.decode_value(cells, value_bars, icon_tiles)
            if not self.output.accepts(result):
                raise ValueError("解码返回值与声明不符")
            return result
        except Exception:
            return self.fallback_value()

    def generate_lua(self, instance_id: str) -> str:
        if self._template is None or not self.regions:
            raise ValueError("模板或布局尚未就绪")
        parameters = self.template_parameters()
        parameters["uuid"] = instance_id
        for index, region in enumerate(self.regions, 1):
            parameters[f"x{index}"] = str(region.x)
            if region.width is not None:
                parameters[f"width{index}"] = str(region.width)
        source = self._template.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            name = match.group(1)
            if name not in parameters:
                raise ValueError(f"模板缺少参数：{name}")
            return parameters[name]

        return re.sub(r"\{\{([a-zA-Z0-9_]+)\}\}", replace, source)

    def template_parameters(self) -> dict[str, str]:
        return {}

    @abstractmethod
    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> Value:
        raise NotImplementedError

    @abstractmethod
    def fallback_value(self) -> Value:
        raise NotImplementedError


def allocate(conditions: list[Condition]) -> int:
    """按同类出现顺序独立排列，返回包含检测列的基板物理宽度。"""
    next_x: dict[OutputType, int] = {"cell": 1, "value_bar": 1, "icon_tile": 1}
    for condition in conditions:
        kind = condition.output.output_type
        regions: list[Region] = []
        for index in range(condition.output.output_count):
            width = condition.output.widths[index] if kind == "value_bar" else None
            regions.append(Region(next_x[kind], 2 if kind == "cell" else None, width))
            next_x[kind] += width + 1 if width is not None else 1
        condition.freeze(tuple(regions))
    content = max(5, next_x["cell"] - 1, next_x["value_bar"] - 1, 2 * (next_x["icon_tile"] - 1))
    return (content + 2) * 4


def check_args(args: dict[str, object], expected: set[str]) -> None:
    if set(args) != expected:
        raise ValueError(f"参数必须恰好为 {sorted(expected)}，实际为 {sorted(args)}")


def positive_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{name} 必须为有限正数")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} 必须为有限正数")
    return result


def positive_int(value: object, name: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} 必须为正整数")
    return value


def spell_ids(value: object) -> tuple[int, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("spell_ids 必须为非空技能 ID 数组")
    return tuple(positive_int(item, "spell_ids") for item in value)


def gray(cell: Cell) -> float:
    if not cell.is_pure or not bool((cell.inner[0, 0] == cell.inner[0, 0, 0]).all()):
        raise ValueError("需要纯灰色 Cell")
    return cell.mean


def boolean(cell: Cell) -> bool:
    if not cell.is_black and not cell.is_white:
        raise ValueError("需要纯黑或纯白 Cell")
    return cell.is_white


def cooldown(cell: Cell) -> float:
    brightness = gray(cell)
    points = ((255, 0.0), (155, 5.0), (105, 30.0), (55, 155.0), (0, 375.0))
    for (high, start), (low, end) in zip(points, points[1:]):
        if brightness >= low:
            return start + (high - brightness) * (end - start) / (high - low)
    return 375.0

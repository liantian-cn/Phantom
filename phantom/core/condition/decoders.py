"""
Summary:
    将通用像素或数值转换为可组合的解码结果。
Description:
    严格灰度、黑白、比例和线性插值只描述数学含义。
    插件负责传入业务上限和节点，并在自己的版本内定义业务公式和兜底。
Key Variables:
    Decoder: 解码输入与输出的泛型抽象接口。
    PiecewiseLinear.points: 按输入值严格递增的插值节点。
Change Log:
    2026-09-13: Added 与技能含义无关的对象化解码工具。
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from phantom.core.pixels import Cell, ValueBar


class Decoder[Input, Output](ABC):
    @abstractmethod
    def decode(self, value: Input) -> Output:
        """转换合法输入，无法解释时抛出异常交由条件处理兜底。"""
        raise NotImplementedError


class Gray(Decoder[Cell, float]):
    def decode(self, value: Cell) -> float:
        if not value.is_pure or not bool((value.inner[0, 0] == value.inner[0, 0, 0]).all()):
            raise ValueError("需要纯灰色 Cell")
        return value.mean


class BlackWhite(Decoder[Cell, bool]):
    def decode(self, value: Cell) -> bool:
        if not value.is_black and not value.is_white:
            raise ValueError("需要纯黑或纯白 Cell")
        return value.is_white


@dataclass(frozen=True)
class CellRatio(Decoder[Cell, float]):
    scale: float = 1.0

    def decode(self, value: Cell) -> float:
        Gray().decode(value)
        return value.ratio * self.scale


class BarRatio(Decoder[ValueBar, float]):
    def decode(self, value: ValueBar) -> float:
        return value.ratio


@dataclass(frozen=True)
class PiecewiseLinear(Decoder[float, float]):
    points: tuple[tuple[float, float], ...]

    def __post_init__(self) -> None:
        if len(self.points) < 2 or any(
            not math.isfinite(x) or not math.isfinite(y) for x, y in self.points
        ):
            raise ValueError("插值至少需要两个有限节点")
        if any(left[0] >= right[0] for left, right in zip(self.points, self.points[1:])):
            raise ValueError("插值节点必须按输入严格递增")

    def decode(self, value: float) -> float:
        if not math.isfinite(value) or not self.points[0][0] <= value <= self.points[-1][0]:
            raise ValueError("输入超出插值范围")
        for (low, end), (high, start) in zip(self.points, self.points[1:]):
            if value <= high:
                return start + (high - value) * (end - start) / (high - low)
        raise ValueError("无法定位插值区间")

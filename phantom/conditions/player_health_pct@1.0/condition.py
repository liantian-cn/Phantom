"""
Summary:
    玩家预测生命值百分比。
Description:
    参数：无参数，沿用示例 usePredicted=true。
    输出：cell，1 个区域，float scalar；4×4 像素。
    API：UnitHealthPercent；UnitDocumentation.lua。秘密生命值经颜色曲线直接渲染。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：Cell.percent。
    不可用或解码异常兜底 0.0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    None
Change Log:
    2026-09-12: Added player_health_pct@1.0 配对编解码。
"""

from phantom.conditions.base import Condition, Output, check_args, gray
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, set())
        super().__init__(Output("cell", value_type=float))

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> float:
        gray(cells[0])
        return cells[0].percent

    def fallback_value(self) -> float:
        return 0.0

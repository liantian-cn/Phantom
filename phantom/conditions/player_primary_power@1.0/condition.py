"""
Summary:
    玩家首要能量。
Description:
    参数：max_power 为有限正数。
    输出：cell，1 个区域，float scalar；4×4 像素。
    API：UnitPowerPercent、UnitPowerType；UnitDocumentation.lua。秘密能量经颜色曲线直接渲染。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：ratio*max_power。
    不可用或解码异常兜底 0.0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    max_power: 本专精约定的能量上限。
Change Log:
    2026-09-12: Added player_primary_power@1.0 配对编解码。
"""

from phantom.conditions.base import Condition, Output, check_args, gray, positive_number
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, {"max_power"})
        self.max_power: float = positive_number(args["max_power"], "max_power")
        super().__init__(Output("cell", value_type=float))

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> float:
        gray(cells[0])
        return cells[0].ratio * self.max_power

    def fallback_value(self) -> float:
        return 0.0

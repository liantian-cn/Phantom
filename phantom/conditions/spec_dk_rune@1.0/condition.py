"""
Summary:
    死亡骑士可用符文数量。
Description:
    参数：无参数。
    输出：cell，1 个区域，int scalar；4×4 像素。
    API：GetRuneCooldown；PlayerScriptDocumentation.lua。runeReady 无秘密返回标记；忽略秘密事件参数。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：mean 四舍五入为0–6整数。
    不可用或解码异常兜底 0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    None
Change Log:
    2026-09-12: Added spec_dk_rune@1.0 配对编解码。
"""

import math

from phantom.conditions.base import Condition, Output, check_args, gray
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, set())
        super().__init__(Output("cell", value_type=int))

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> int:
        count = math.floor(gray(cells[0]) + 0.5)
        if not 0 <= count <= 6:
            raise ValueError("符文数量超出 0–6")
        return count

    def fallback_value(self) -> int:
        return 0

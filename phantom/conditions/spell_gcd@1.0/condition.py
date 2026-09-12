"""
Summary:
    全职业公共冷却剩余秒数。
Description:
    参数：无参数，固定 61304 和 ignoreGCD=false，跳过法术书。
    输出：cell，1 个区域，float scalar；4×4 像素。
    API：GetSpellCooldownDuration；SpellDocumentation.lua。直接查询固定 GCD，秘密 duration 经颜色曲线渲染。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：亮度255/155/105/55/0对应0/5/30/155/375秒，分段线性反算。
    不可用或解码异常兜底 375.0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    None
Change Log:
    2026-09-12: Added spell_gcd@1.0 配对编解码。
"""

from phantom.conditions.base import Condition, Output, check_args, cooldown
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, set())
        super().__init__(Output("cell", value_type=float))

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> float:
        return cooldown(cells[0])

    def fallback_value(self) -> float:
        return 375.0

"""
Summary:
    首个匹配技能的充能层数。
Description:
    参数：spell_ids 为非空正整数列表；max_charges 为正整数。
    输出：value_bar，1 个区域，int scalar；内容 4*max_charges×4，含分隔 4*(max_charges+1)×4 像素。
    API：GetSpellCharges；SpellDocumentation.lua、SpellSharedDocumentation.lua。秘密 currentCharges 直接传给 StatusBar。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：ratio*max_charges 四舍五入。
    不可用或解码异常兜底 0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    spells: 按配置优先顺序的候选技能。
Change Log:
    2026-09-12: Added spell_charges@1.0 配对编解码。
"""

import math

from phantom.conditions.base import Condition, Output, check_args, positive_int, spell_ids
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, {"spell_ids", "max_charges"})
        self.spells: tuple[int, ...] = spell_ids(args["spell_ids"])
        self.max_charges: int = positive_int(args["max_charges"], "max_charges")
        super().__init__(Output("value_bar", value_type=int, widths=(self.max_charges,)))

    def template_parameters(self) -> dict[str, str]:
        return {"spell_ids": ", ".join(str(spell) for spell in self.spells)}

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> int:
        return math.floor(value_bars[0].ratio * self.max_charges + 0.5)

    def fallback_value(self) -> int:
        return 0

"""
Summary:
    首个匹配技能的高亮状态。
Description:
    参数：spell_ids 为非空正整数列表。
    输出：cell，1 个区域，bool scalar；4×4 像素。
    API：IsSpellOverlayed；SpellActivationOverlayDocumentation.lua。秘密布尔经 EvaluateColorFromBoolean 渲染。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：严格黑白布尔。
    不可用或解码异常兜底 False；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    spells: 按配置优先顺序的候选技能。
Change Log:
    2026-09-12: Added spell_overlay@1.0 配对编解码。
"""

from phantom.conditions.base import Condition, Output, boolean, check_args, spell_ids
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, {"spell_ids"})
        self.spells: tuple[int, ...] = spell_ids(args["spell_ids"])
        super().__init__(Output("cell", value_type=bool))

    def template_parameters(self) -> dict[str, str]:
        return {"spell_ids": ", ".join(str(spell) for spell in self.spells)}

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> bool:
        return boolean(cells[0])

    def fallback_value(self) -> bool:
        return False

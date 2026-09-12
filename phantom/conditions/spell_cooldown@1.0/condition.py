"""
Summary:
    首个匹配技能的剩余冷却秒数。
Description:
    参数：spell_ids 为非空正整数列表；ignore_gcd 为布尔。
    输出：cell，1 个区域，float scalar；4×4 像素。
    API：GetSpellCooldownDuration；SpellDocumentation.lua。秘密 duration 经颜色曲线渲染；法术书选择首个匹配。
    核验：2026-09-12，E:/Documents/GitHub/wow-ui-source，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58，12.1.0.69587。
    解码：亮度255/155/105/55/0对应0/5/30/155/375秒，分段线性反算。
    不可用或解码异常兜底 375.0；冷却黑色兼容饱和与不可用，无额外状态位。
Key Variables:
    spells: 按配置优先顺序的候选技能。
Change Log:
    2026-09-12: Added spell_cooldown@1.0 配对编解码。
"""

from phantom.conditions.base import Condition, Output, check_args, cooldown, spell_ids
from phantom.core.pixels import Cell, IconTile, ValueBar


class Plugin(Condition):
    def __init__(self, args: dict[str, object]) -> None:
        check_args(args, {"spell_ids", "ignore_gcd"})
        self.spells: tuple[int, ...] = spell_ids(args["spell_ids"])
        flag = args["ignore_gcd"]
        if type(flag) is not bool:
            raise ValueError("ignore_gcd 必须为布尔值")
        self.ignore_gcd: bool = flag
        super().__init__(Output("cell", value_type=float))

    def template_parameters(self) -> dict[str, str]:
        return {
            "spell_ids": ", ".join(str(spell) for spell in self.spells),
            "ignore_gcd": str(self.ignore_gcd).lower(),
        }

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> float:
        return cooldown(cells[0])

    def fallback_value(self) -> float:
        return 375.0

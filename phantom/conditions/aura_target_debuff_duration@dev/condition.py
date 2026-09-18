"""
Summary:
    估计不可辅助目标首个匹配减益的剩余秒数。
Description:
    固定 PLAYER|HARMFUL；官方 PLAYER 包含玩家宠物和载具，不增加 player_only 参数。
    aura_ids 为非空正整数列表，duration 为正整数秒，同时决定 ValueBar 内容宽度。
    官方 AuraSlot.SetDurationBar 使用 Immediate / RemainingTime 显示原生时长比例。
    Python 返回 ratio * 配置 duration 的 float；实际光环时长不同会有误差，0.25 秒仅为名义步长。
    永久光环交官方处理；无光环或解码异常返回 0.0，不读取秘密光环数据。
Key Variables:
    duration: 配置时长与条宽，非官方固定绝对量程。
Change Log:
    2026-09-18: Added 冻结迁移计划中的目标减益时长。
"""

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Output
from phantom.core.pixels import Cell, IconTile, PixelDecoder, ValueBar
from phantom.core.validation import Fields, Items, PositiveInteger


class Plugin(Condition):
    """将官方时长条的像素比例换算为配置秒数估计。"""

    def __init__(self, args: dict[str, object]) -> None:
        Fields(frozenset({"aura_ids", "duration"})).validate(args, "plugin_args")
        self.aura_ids: tuple[int, ...] = tuple(Items(PositiveInteger(), nonempty=True).validate(args["aura_ids"], "aura_ids"))
        self.duration: int = PositiveInteger().validate(args["duration"], "duration")
        super().__init__(Output("value_bar", value_type=float, widths=(self.duration,)))

    def template_parameters(self) -> dict[str, str]:
        return {"aura_ids": ", ".join(str(value) for value in self.aura_ids)}

    def decode_value(self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile], *, decoder: PixelDecoder) -> float:
        return value_bars[0].ratio * self.duration

    def fallback_value(self) -> float:
        return 0.0

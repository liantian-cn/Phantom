"""
Summary:
    玩家是否有任一指定增益。
Description:
    参数：非空正整数增益技能 ID 列表，任一存在即为真。
    输出：cell，1 个区域，bool scalar；4×4 像素，采样内部 2×2。
    API：AuraContainer:AddAuraSlot(key, "HELPFUL", options)；options.candidateFilters.includeSpellIDs 为技能 ID 布尔映射；玩家 HELPFUL 身份过滤允许。UpdateAllAuras() 请求刷新。
    参考 04_player_buff.lua，单 slot 匹配任一 ID，白色贴图覆盖黑底；不读取 aura 数据或显示状态。
    核验：2026-09-15，@wow-ui-source，12.1.0.69587，
    revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58；具体来源和限制见 template.lua。
    解码：严格全黑/全白；不可用或异常兜底 False。
Key Variables:
    buff_ids: 非空正整数增益技能 ID 列表，任一存在即为真。
Change Log:
    2026-09-15: Added 按已确认的玩家条件迁移计划新增 player_has_buff@dev。
"""

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Output
from phantom.core.pixels import Cell, IconTile, PixelDecoder, ValueBar
from phantom.core.validation import Fields, Items, PositiveInteger


class Plugin(Condition):
    """玩家是否有任一指定增益；参数、像素解码及异常兜底均属于本插件。"""

    def __init__(self, args: dict[str, object]) -> None:
        Fields(frozenset({"buff_ids"})).validate(args, "plugin_args")
        self.buff_ids: tuple[int, ...] = tuple(Items(PositiveInteger(), nonempty=True).validate(args["buff_ids"], "buff_ids"))
        super().__init__(Output("cell", value_type=bool))

    def template_parameters(self) -> dict[str, str]:
        """序列化已验证的配置；坐标由冻结布局注入。"""
        return {"buff_ids": ", ".join(str(value) for value in self.buff_ids)}

    def decode_value(self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile], *, decoder: PixelDecoder) -> bool:
        cell = cells[0]
        if not cell.is_black and not cell.is_white:
            raise ValueError("需要纯黑或纯白 Cell")
        return cell.is_white

    def fallback_value(self) -> bool:
        """无法识别时表示未确认条件成立。"""
        return False

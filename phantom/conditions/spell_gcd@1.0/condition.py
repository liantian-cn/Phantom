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
    COOLDOWN_POINTS: 本版本亮度与剩余秒数节点，两端共用。
Change Log:
    2026-09-13: Changed 组合校验器与解码器，保持 @1.0 配对语义。
    2026-09-12: Added spell_gcd@1.0 配对编解码。
"""

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Output
from phantom.core.condition.decoders import (
    Decoder,
    Gray,
    PiecewiseLinear,
)
from phantom.core.pixels import Cell, IconTile, ValueBar
from phantom.core.validation import (
    Fields,
)

# @1.0 的亮度到剩余秒数配对节点；黑色兼有饱和与不可用含义。
COOLDOWN_POINTS: tuple[tuple[float, float], ...] = (
    (0.0, 375.0),
    (55.0, 155.0),
    (105.0, 30.0),
    (155.0, 5.0),
    (255.0, 0.0),
)


class CooldownDecoder(Decoder[Cell, float]):
    def __init__(self) -> None:
        self.gray: Gray = Gray()
        self.curve: PiecewiseLinear = PiecewiseLinear(COOLDOWN_POINTS)

    def decode(self, value: Cell) -> float:
        """先拒绝污染颜色，再反算本插件版本的分段剩余秒数。"""
        return self.curve.decode(self.gray.decode(value))


class Plugin(Condition):
    """校验实例参数，声明输出，再将像素解释为本条件业务值。"""

    def __init__(self, args: dict[str, object]) -> None:
        Fields(frozenset(set())).validate(args, "plugin_args")
        self.decoder: CooldownDecoder = CooldownDecoder()
        # 输出声明只依赖已验证参数，随后由核心分配并冻结区域。
        super().__init__(Output("cell", value_type=float))

    def template_parameters(self) -> dict[str, str]:
        """Lua 曲线与 Python 反算共用本版本节点，避免两端漂移。"""
        return {
            "cooldown_points": ", ".join(
                f"{{{seconds}, {brightness}}}" for brightness, seconds in reversed(COOLDOWN_POINTS)
            )
        }

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> float:
        return self.decoder.decode(cells[0])

    def fallback_value(self) -> float:
        """保留 @1.0 的不可用业务值，亦用于核心捕获的解码异常。"""
        return 375.0

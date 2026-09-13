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
    不可用或解码异常兜底 0。
Key Variables:
    None
Change Log:
    2026-09-13: Changed 组合校验器与解码器，保持 @1.0 配对语义。
    2026-09-12: Added spec_dk_rune@1.0 配对编解码。
"""

import math

from phantom.core.condition.base import Condition
from phantom.core.condition.contracts import Output
from phantom.core.condition.decoders import (
    Decoder,
    Gray,
)
from phantom.core.pixels import Cell, IconTile, ValueBar
from phantom.core.validation import (
    Fields,
)


class RuneDecoder(Decoder[Cell, int]):
    def decode(self, value: Cell) -> int:
        """符文以整数亮度编码；非负四舍五入后仍须在 0–6 内。"""
        count = math.floor(Gray().decode(value) + 0.5)
        if not 0 <= count <= 6:
            raise ValueError("符文数量超出 0–6")
        return count


class Plugin(Condition):
    """校验实例参数，声明输出，再将像素解释为本条件业务值。"""

    def __init__(self, args: dict[str, object]) -> None:
        Fields(frozenset(set())).validate(args, "plugin_args")
        self.decoder: RuneDecoder = RuneDecoder()
        # 输出声明只依赖已验证参数，随后由核心分配并冻结区域。
        super().__init__(Output("cell", value_type=int))

    def decode_value(
        self, cells: list[Cell], value_bars: list[ValueBar], icon_tiles: list[IconTile]
    ) -> int:
        return self.decoder.decode(cells[0])

    def fallback_value(self) -> int:
        """保留 @1.0 的不可用业务值，亦用于核心捕获的解码异常。"""
        return 0

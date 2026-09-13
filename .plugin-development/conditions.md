# 条件插件开发

## Python 实现流程

每个版本的 `condition.py` 导出 `Condition` 子类 `Plugin`，构造参数为 `args: dict[str, object]`。
依次验证参数、创建业务解码器、声明 `Output`；布局、模板路径和异常兜底调用由核心负责。

| 内容 | 使用方式 |
| --- | --- |
| 生命周期 | `phantom.core.condition.base.Condition` |
| 输出与类型 | `phantom.core.condition.contracts.Output`、`Value`、`Region` |
| 参数字段 | `Fields(required, optional).validate(args, "plugin_args")`，字段集合用 `frozenset` |
| 基础输入 | `PositiveInteger`、`PositiveNumber`、`Boolean`、`String`、`Table`、`Items` |
| 通用解码 | `Gray`、`BlackWhite`、`CellRatio`、`BarRatio`、`PiecewiseLinear` |

`Validator.validate` 返回强类型合法值，失败抛出包含字段上下文的 `ValueError`。
`Decoder.decode` 返回解码结果，失败交由 Condition 的既有异常边界调用插件兜底。
例如 `SpellIDs` 在本插件内组合 `Items(PositiveInteger(), nonempty=True)`，保留技能候选顺序；冷却解码器在本版本内组合 `Gray` 和带本地节点的 `PiecewiseLinear`。

`decode_value(cells, value_bars, icon_tiles)` 将所需区域交给实例的解码对象；未使用的列表为空。
每个插件独立实现 `fallback_value()`，解释为何选择该值。兜底须符合输出声明；不要把布局越界伪装成可用业务值。

## 模板参数与常量

模板沿用项目 Lua 分区。在 `logical code` 开头、创建曲线或事件框架等逻辑之前，集中声明：

- 实例坐标、宽度和所有配置参数。
- 刷新间隔、固定技能 ID、数量上限、编码节点及其他业务常量。

`uuid` 是文件头元数据占位符；其余模板占位符只用于头部参数声明。`template_parameters()` 只返回已校验的插件参数，不接收任意 Lua 代码。
`uuid`、`xN`、适用的 `yN` 与 `widthN` 由核心从冻结布局注入，插件不得覆盖；不要把固定第二行重新写成另一份布局来源。

```lua
--[[  logical code  ]]
local POSITION_Y = {{y1}} -- 冻结布局的行
local POSITION_X = {{x1}} -- 冻结布局的横向位置

local runeCell -- 在 UIInitFuncs 回调中创建
local function InitializeRunes()
    runeCell = Cell:New({ x = POSITION_X, y = POSITION_Y })
end
```

多区域使用编号对应的声明。函数临时变量保留在局部；运行期状态不能为了“集中声明”变成加载期快照，必须保留原初始化时机。
头部常量不意味着新增用户可配置字段。例如 GCD 的固定技能 ID 仍不接受 `plugin_args`。

## 配对与说明

Lua 编码和 Python 解码属于同一版本契约。缩放、精度节点、饱和、不可用表示、区域合并与列表过滤必须配对；有共同静态节点时由插件参数生成 Lua，避免手写两份数据。

除通用 Python 文件头外，每个条件插件必须说明：

- 用途、业务语义及 `plugin_args` 的字段、类型与约束。
- 输出类型、数量、业务类型、形状和物理尺寸。
- WoW API、核验来源与 Secret Value 的处理边界。
- 解码算法、业务不可用状态及异常兜底含义。
- 已知的插件版本变化，不编造历史。

在参数到输出的映射、解码舍入/区间、模板序列化等关键步骤解释原因。冷却的黑色含义不能复制到血量、能量或布尔插件。

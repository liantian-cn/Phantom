# 条件插件开发

## Python 实现流程

每个版本的 `condition.py` 导出 `Condition` 子类 `Plugin`，构造参数为 `args: dict[str, object]`。
依次验证参数、保存业务参数、声明 `Output`；布局、模板路径和异常兜底调用由核心负责。

| 内容 | 使用方式 |
| --- | --- |
| 生命周期 | `phantom.core.condition.base.Condition` |
| 输出与类型 | `phantom.core.condition.contracts.Output`、`Value`、`Region` |
| 参数字段 | `Fields(required, optional).validate(args, "plugin_args")`，字段集合用 `frozenset` |
| 基础输入 | `PositiveInteger`、`PositiveNumber`、`Boolean`、`String`、`Table`、`Items` |
| 像素读取 | `Cell.mean`、`Cell.ratio`、`Cell.percent`、`Cell.is_white`、`ValueBar.ratio`、`IconTile.hash` 等区域属性 |

`Validator.validate` 返回强类型合法值，失败抛出包含字段上下文的 `ValueError`。
例如 `SpellIDs` 在本插件内组合 `Items(PositiveInteger(), nonempty=True)`，保留技能候选顺序。业务解码直接写在 `decode_value()` 中，失败交由 Condition 的既有异常边界调用插件兜底。
当前灰度条件先检查 `Cell.is_pure` 及内部像素的 RGB 分量相等，再读取亮度或比例；布尔条件先检查严格全黑或全白，再读取 `Cell.is_white`。冷却条件直接使用本版本固定节点进行分段插值，业务范围、舍入与兜底保留在插件内。

`decode_value(cells, value_bars, icon_tiles, *, decoder: PixelDecoder)` 直接读取所需区域对象；未使用的列表为空。`value` 也要求传入同一个 decoder，签名不兼容旧 `@dev` 接口。
插件可调用 `decoder.getCell(x, y)`、`decoder.getValueBar(x, width)`、`decoder.getIconTile(x)` 读取任意有效区域；坐标与宽度沿用像素协议。不得修改帧数据或缓存 decoder 供后续帧使用。
每个插件独立实现 `fallback_value()`，解释为何选择该值。兜底须符合输出声明。框架分配区域越界在调用层失败；插件额外读取异常与业务解码异常使用插件兜底。

## 无 Lua 与零区域插件

`template.lua` 可省略，生成器保留空的实例 `do/end` 块。存在模板时仍正常渲染并检查路径与占位符错误，不将损坏模板当成缺失模板。
不新增像素区域时使用 `Output("none", output_count=0, value_type=...)`，不声明 widths；框架冻结空 regions，向解码方法传三个空列表。仍必须声明业务值类型、形状和兜底。
模板与区域分配相互独立：零区域插件可以提供 Lua；有分配区域的插件也可以省略模板，但插件作者须确保该区域有实际有效的数据来源。
三个状态读取插件示例见系统的[通用状态读取插件](../.spec/plugin-system.md#通用状态读取插件)。它们依赖保留的第一行 Cell，不调用 WoW API、不重复生成 Cell。

## 模板参数与常量

模板沿用项目 Lua 分区。在 `logical code` 开头、创建曲线或事件框架等逻辑之前，集中声明：

- 实例坐标、宽度和所有配置参数。
- 刷新间隔、固定技能 ID、数量上限、编码节点及其他业务常量。

`uuid` 是文件头元数据占位符。业务模板只动态生成坐标、宽度及循环中必要的可配置变量（如 `spell_ids`、`ignore_gcd`）；这些占位符只用于头部参数声明。`template_parameters()` 只返回已校验的必要配置参数，不接收任意 Lua 代码。
固定曲线、节点、算法和固定业务常量直接写在源码中，不通过 Python 序列化或模板占位符生成。集中声明不等于动态生成。
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

Lua 编码和 Python 解码属于同一版本契约。缩放、精度节点、饱和、不可用表示、区域合并与列表过滤必须配对；固定的 Lua 编码曲线和 Python 解码节点分别写在各自源码中，通过配对测试确保一致；不得为了共用静态数据而动态生成固定曲线或算法。

除通用 Python 文件头外，每个条件插件必须说明：

- 用途、业务语义及 `plugin_args` 的字段、类型与约束。
- 输出类型、数量、业务类型、形状和物理尺寸。
- WoW API、核验来源与 Secret Value 的处理边界。
- 解码算法、业务不可用状态及异常兜底含义。
- 已知的插件版本变化，不编造历史。

在参数到输出的映射、解码舍入/区间、模板序列化等关键步骤解释原因。冷却的黑色含义不能复制到血量、能量或布尔插件。

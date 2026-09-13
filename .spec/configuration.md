# Rotation 配置规范

## 应用配置与 rotation 配置的边界

启动工作目录下的 `phantom.toml` 是应用配置文件，保存截图插件选择、FPS 与界面参数，与 rotation TOML 无关，其字段、默认值和错误规则见 [tui.md](tui.md)。本文件只规定旋转（rotation）配置的 schema 与语义。

## 文件边界

一份 TOML 文件（`.toml`）表示一份 rotation。schema v1 的顶层字段固定为：

- `schema_version`
- `uuid`
- `profile`
- `conditions`
- `macros`
- `rotation`

字段名统一使用 `snake_case`。草案中的 `unitTalnet`、`bing_key` 等拼写不是兼容契约，不得作为别名保留。列表必须使用真正的 TOML 数组，不得用逗号拼接伪装列表。配置对象不使用数字 `id`。

`profile` 使用表；`conditions`、`macros` 和 `rotation` 使用表数组。每个 `[conditions.plugin_args]` 归属于最近声明的 `[[conditions]]` 条目。

## 完整示例

此处 `example_author.health_pct@dev` 是说明 `unit_token` 参数的假设插件，不是内置插件；当前可运行示例见 `rotations/blood-dk.toml`。

```toml
schema_version = 1
uuid = "550e8400-e29b-41d4-a716-446655440000"

[profile]
title = "神圣骑士基础循环"
description = "优先治疗玩家，否则对有效目标使用审判。"
unit_class = "PALADIN"
unit_spec = 1

[[conditions]]
title = "玩家血量"
plugin = "example_author.health_pct@dev"
[conditions.plugin_args]
unit_token = "player"

[[conditions]]
title = "圣光术冷却时间"
plugin = "liantian_cn.spell_cooldown@dev"
[conditions.plugin_args]
spell_ids = [82326, 82325]
ignore_gcd = true

[[conditions]]
title = "目标血量"
plugin = "example_author.health_pct@dev"
[conditions.plugin_args]
unit_token = "target"

[[conditions]]
title = "审判冷却时间"
plugin = "liantian_cn.spell_cooldown@dev"
[conditions.plugin_args]
spell_ids = [12345]
ignore_gcd = true

[[macros]]
name = "对玩家释放圣光术"
macro_text = "/cast [@player] 圣光术"
key = "ALT-NUMPAD1"
bind_key = true

[[macros]]
name = "审判"
key = "E"
bind_key = false

[[rotation]]
condition = "玩家血量 < 70 and 圣光术冷却时间 == 0"
macro = "对玩家释放圣光术"

[[rotation]]
condition = "目标血量 > 0 and 审判冷却时间 == 0"
macro = "审判"
```

## 标识和引用

- `schema_version` 当前必须为整数 `1`。未来结构升级通过显式迁移完成，不得猜测字段形状。
- `uuid` 必须是带连字符的标准 RFC 4122 UUID 文本，并用于生成 `<uuid>.lua`。
- `profile.unit_class` 使用 Blizzard 的大写职业 token。
- `profile.unit_spec` 使用 `GetSpecialization()` 的顺序索引 1–4。
- schema v1 不包含 `unit_talents`。
- 每个 `conditions[].title` 在文件内唯一；表达式直接引用该标题。
- 每个 `macros[].name` 在文件内唯一；循环项的 `macro` 直接引用该名称。
- `plugin_args` 的具体字段由精确版本插件定义，但字段名仍使用 `snake_case`。

条件标题必须符合 Python 标识符兼容规则：以中文字符或英文字母开头，后续只含中文字符、英文字母、数字或下划线；不得包含空白、运算符、括号或引号，也不得使用 Python 保留词，包括 `and`、`or` 和 `not`。标题可以是中文或英文，只要引用完全一致。

## 条件表达式

加载配置时，执行器必须只解析和验证一次表达式 AST；运行期复用已验证结构，并读取 `conditions[title].value()`。不得使用 `eval`。

schema v1 支持：

- 字面量：整数、浮点数、`True`、`False`、带引号字符串和简单列表。
- 比较：`<`、`<=`、`>`、`>=`、`==`、`!=`。
- 布尔：`not`、`and`、`or`。
- 成员：`in`、`not in`。
- 用于改变结合顺序的括号。

优先级沿用 Python：比较与成员判断，然后 `not`，然后 `and`，最后 `or`。禁止属性访问、下标、函数调用、算术运算和其他 AST 节点。

列表字面量不得嵌套，元素必须为同一类型。成员判断的右侧也可以是另一个条件返回的列表；验证阶段必须确认右侧声明为列表、左侧声明为标量，且元素类型与左侧类型一致。字符串和数字之间不做隐式转换。

## 宏与键位

- `key` 必填，使用大写 WoW 连字符格式，例如 `ALT-NUMPAD1`、`SHIFT-F8`；Python 端解析同一个字符串并映射到 Windows 输入。
- `bind_key = true` 时，`macro_text` 必填。生成的 Lua 使用不可见 `SecureActionButtonTemplate` 设置 `type = "macro"` 与 `macrotext`，再通过 `SetOverrideBindingClick` 建立优先覆盖绑定。
- 上述绑定不创建 WoW 已保存宏槽位，也不改写玩家的持久键位设置。
- `bind_key = true` 会直接覆盖该键在当前运行期的已有动作，不检查也不提示；用户已经接受该风险。
- `bind_key = false` 时，`macro_text` 可省略；即使填写也不生效，生成器不得为该项输出安全按钮或覆盖绑定 Lua。Python 直接发送玩家已有游戏键位。

启用绑定时，生成代码必须保持以下调用语义；变量命名可以由生成器调整：

```lua
local buttonName = addonName .. "Button" .. macro.title
local frame = CreateFrame("Button", buttonName, UIParent, "SecureActionButtonTemplate")
frame:SetAttribute("type", "macro")
frame:SetAttribute("macrotext", macro.text)
frame:RegisterForClicks("AnyDown", "AnyUp")
SetOverrideBindingClick(frame, true, macro.key, buttonName)
```

## 执行顺序

`rotation` 从上到下求值，第一个为真的条目胜出。每轮最多发送一个键；全部为假时本轮不执行动作。

## 待定事项

- schema v1 之外的升级与迁移格式。
- 键位语法的完整合法键名表和错误提示。
- 循环频率、节流与相关配置字段。
- 未来是否增加天赋路由字段。


## 单份生成阶段扩展（schema v1）

- profile.unit_class_id 可省略，按职业 token 推导；显式值必须一致。annotate 是 rotation 条目的可选字符串说明。
- Idle 是保留动作名，不得声明同名宏，不需要键位。空 condition 仅允许在末尾显式 Idle；省略时在内存追加隐含 Idle，不写回该条目。
- 条件 layout 是可重建的排错表：output_type 加 regions 数组，每个区域有 x、适用的 y/width；单位与 Lua 构造器一致。
- 每次启动加载和点击生成重新分配，分类后按条件原始顺序排列，ValueBar 包含分隔。仅 layout 不同时保存，保留注释和其他内容，校验失败不回写。
- 本阶段校验所有结构、基本类型、UUID、职业专精、名称/引用与插件参数，加载时一次性完成表达式白名单、引用与类型校验，运行时复用 AST。
- 条件实例、宏和规则保持配置顺序；重复规则允许，条件标题与宏名称必须唯一。
- 当前键位仅校验大写格式及 CTRL/ALT/SHIFT 修饰符，无重复修饰符；完整合法键名表留待绑定阶段。
- 示例为 rotations/blood-dk.toml；每次生成所有声明的条件，包括尚未被规则引用的条件。

## 第 11–13 步求值边界

- 表达式最终结果、`not` 和 `and/or` 操作数必须为布尔，不使用数字或列表的隐式真假值。
- 数值比较允许 int 与 float；bool 不作为数值。字符串只与字符串比较。
- 列表字面量仅含同类型标量常量；空列表可用于成员判断。成员判断不混用 int/float。
- 支持链式比较及短路；列表仅允许同类型相等／不等判断，不支持排序比较。
- 负号属于未开放的一元算术节点；非有限浮点字面量被拒绝。
- 首条命中为 Idle 时本轮无宏；显式或内存追加的末尾 Idle 承接全部未命中。
- 本阶段只报告拟执行宏和键位，不实现 action、宏绑定生成或真实按键发送。

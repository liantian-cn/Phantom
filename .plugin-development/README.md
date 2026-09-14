# 插件开发手册

本目录维护插件作者的开发要求。开始开发前，先阅读本页，再进入对应专题：

| 插件类型 | 专题 | 当前入口 |
| --- | --- | --- |
| 条件 | [条件插件](conditions.md) | `phantom/conditions/<author>.<name>@<version>/condition.py` 与可选 `template.lua` |
| 截图 | [截图插件](captures.md) | `phantom/captures/<author>.<name>@<version>/capture.py` |
| 键盘 | [键盘插件](keyboards.md) | `phantom/keyboards/<author>.<name>@<version>/keyboard.py` |

系统加载、生命周期及输出契约以 [插件系统](../.spec/plugin-system.md) 为准；像素单位以 [像素协议](../.spec/pixel-protocol.md) 为准。
本手册与 `.spec` 分别维护作者要求与系统契约，具有相同的项目规范地位；同一规则只在一个位置维护，其他文档链接引用。

## 职责与依赖

- 版本目录放插件实现、配套模板与供 Agent 阅读的 `plugin.toml`。公共条件设施位于 `phantom/core/condition/`，截图设施位于 `phantom/core/capture/`，键盘设施位于 `phantom/core/keyboard/`。
- 插件依赖核心的公开契约；核心不依赖具体技能、职业或专精规则，不按某个插件名称写分支。
- 不导入另一个插件版本目录。通用数学与基础输入检查通过组合复用；业务字段、算法参数、业务范围和兜底留在本插件版本。
- 不在 UI 中加载具体后端文件或引用其具体实现类；使用核心注册器。
- 通用参数校验使用 `phantom.core.validation.Validator[T]`，通用解码使用 `phantom.core.condition.decoders.Decoder[Input, Output]`。选择适用的实现组合，不把所有职责塞进 Condition 基类。

## 版本与变更

以下是 Agent 开发规则，不由运行时代码或 CI 强制校验：

- 插件标识使用 `repo作者名.包名@版本号`，包名沿用英文 `snake_case`。作者名应为可用的 Python 包名（合法标识符且不是保留词）；本仓库作者 `liantian-cn` 使用 `liantian_cn`。
- 数字或点分数字版本（如 `1`、`1.0`、`1.2.3`）是正式版本，接口参数和逻辑不得原地修改；需要修改时创建另一版本。
- 其余非数字版本是测试版本，例如 `dev`、`beta`、`1.0-beta`，允许修改接口参数和逻辑；仍需同步受影响配置、说明并验证业务行为。
- 条件插件和 GDI 截图插件统一使用 `liantian_cn.<名称>@dev`，不保留旧标识别名。2026-09-14 条件接口增加必填同帧 decoder，并新增三个无 Lua 状态读取插件；原有八个条件保持业务解码语义。

运行时只按完整目录名精确加载，不做版本回退、作者名自动转换或跨版本隐式复用，保留路径安全及接口检查。

2026-09-13 的职责重构保留现有八个 `@1.0` 的业务契约，这次决定不构成未来修改已发布语义的通用授权。

## AI Agent 自述

建议每个插件提供 `plugin.toml`，新增或修改插件时由 Agent 同步维护。这是软性作者要求：Python 运行代码不读取它，缺失或内容错误不作为插件加载失败条件，也不增加强制 CI 校验。

自述使用英文 TOML 字段与中文业务说明，推荐结构如下：

| 字段 | 内容 |
| --- | --- |
| `name` | 完整插件标识，与目录名一致 |
| `display_name` | 简明中文插件名 |
| `description` | 中等详细用途：主要 API 名称、输入到输出转换、适用边界；无需 API 调用教程 |
| `recommended_condition_name` | 建议的条件标题；如 `{技能名称}的冷却时间`，占位符需替换，实际标题遵守 rotation 命名规则；截图填写“不适用” |
| `[parameters]` | 无参数时用 `description` 明确说明；有参数时使用下级表逐项描述 |
| `[parameters.<参数名>]` | `type`、`required`、`description`，仅有默认值时填写 `default`；说明含义与约束，不罗列内部临时变量 |
| `[returns]` | `type`、`description`，按业务需要填写 `unit`、`fallback`、输出形状与状态字段说明 |

内容必须与实际插件一致，不凭 API 名称推断更强的业务保证。WoW API 核验来源可用注释记录日期、版本、revision 和对应定义文件。完整源码说明要求仍见各插件专题。

## 文档、类型与验证

- 标识符使用英文，业务说明使用中文。解释业务步骤、边界和原因，不以注释数量为目标。
- 项目通用文件头、Type Hint、Lua 分区、API 文档与事实核验规则统一见 [开发规则](../.spec/development-rules.md)；插件专属说明见各专题。
- 注释必须与本实例和参数化行为一致，不能保留示例的固定坐标、固定宽度，或复制其他插件的兜底含义。
- 新增与修改插件时验证正常输入、边界、不可用输入及失败路径。条件须验证 Lua/Python 配对，截图须验证图像与生命周期，键盘须验证发送顺序和失败释放；检查方法见 [测试规则](../.spec/testing.md)。
- 完整类型检查使用 `.venv/Scripts/python scripts/check_types.py`，包括每个精确版本入口；新增插件不得依靠目录特殊字符避开检查。
- 离线测试、Windows 截图和游戏内验收分别记录，不把 API doubles 的结果写成游戏验证结论。

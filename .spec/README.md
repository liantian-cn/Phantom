# Phantom 项目规范

本目录保存 Phantom 的规范性文档。未来任务先阅读本文件，再按任务类型读取对应专题；不要把尚未确认的设想补写成规则。

## 权威顺序

发生冲突时，按以下顺序处理：

1. 用户当前明确指令与已冻结任务计划。
2. 本目录中的项目规范。
3. `.context/` 中的技术背景与核验记录。
4. 外部第三方源码和历史项目实现。

`.context/` 只提供事实背景，不自动成为项目要求。第三方旧项目只证明某种实现曾经存在，不代表 Phantom 必须照搬。

## 阅读路由

| 任务 | 必读文档 |
| --- | --- |
| 理解目标、范围和产品边界 | [project-overview.md](project-overview.md) |
| 修改模块职责、运行流程或生成模型 | [architecture.md](architecture.md) |
| 修改屏幕布局、采样或像素解码 | [pixel-protocol.md](pixel-protocol.md) |
| 创建或修改条件、行为、截图插件 | [plugin-system.md](plugin-system.md) |
| 修改 rotation TOML 或表达式语言 | [configuration.md](configuration.md) |
| 修改 TUI 页面、应用配置、游戏检测或业务日志 | [tui.md](tui.md) |
| 编写代码、查询 API、使用外部源码 | [development-rules.md](development-rules.md) |
| 设计或执行测试 | [testing.md](testing.md) |

涉及多个领域时，读取所有相关专题。WoW API、Secret Values、Aura、渲染、事件和安全限制的事实入口见 [`.context/README.md`](../.context/README.md)。

## 规范状态

- 正文中使用“必须”“禁止”“固定”等措辞的内容是已确认规则。
- 每份文档的“待定事项”不是规则，也不是实现授权；Agent 不得自行选择答案。
- 易随 WoW 版本变化的事实必须回到 `.context/` 和指定本地源码重新核验。
- 新决定应写入最小相关专题，不在多个文件重复维护同一套细节。

## 文档语言

- `.spec/` 与根 `AGENTS.md` 使用中文。
- `.context/` 保持英文，避免技术翻译误差。
- 文件名、配置字段、代码标识符和 API 名称保持英文。

## 待定事项

无。本文件只定义规范入口、权威关系与阅读方法；专题中的待定事项由各自未来任务处理。

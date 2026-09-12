# 系统架构

## 运行边界

Phantom 分为游戏外 Python 端和游戏内 Lua 端。Lua 端只负责采集游戏状态、编码与渲染数据以及建立已配置的安全按钮绑定；Python 端负责生成、截图、解码、求值和发送按键。

```text
rotation YAML
    ↓
Python 生成器 ──→ WoW 插件（共享基础模块 + UUID Lua）
                       ↓
                 画面角落像素协议
                       ↓
Windows 截图插件 → 条件实例解码 → rotation 白名单求值 → 行为插件发送按键
                                      │
                                      └─ 无命中：本轮无动作
```

## 组件职责

- 生成器：校验配置与插件参数，实例化条件，冻结布局，生成一个插件包。
- 条件插件：生成本实例 Lua、声明输出契约、读取原始区域并转换为业务值。
- 截图插件：在 Windows 上捕获约定屏幕区域，向条件层提供 NumPy 数组。
- 像素解析：`phantom/core/pixels/` 提供 `PixelDecoder`、`Cell`、`ValueBar`、`IconTile`，将完整基板按 Lua 坐标切分为独立区域，读取通用原始值，不包含条件业务公式。
- rotation 执行器：读取条件值，按配置顺序求值，返回首个命中的宏名称。
- 行为插件：把宏条目的 WoW 格式键位映射为 Windows 消息并发送到游戏窗口。
- Textual TUI：选择 rotation、输入生成包名并承载未来配置操作；当前只冻结技术选型。

## Textual 交互能力

Textual 提供以下能力，供后续 TUI 设计使用：

- 消息与事件：通过自定义 `Message`、`post_message` 和消息处理方法协调组件交互，参见[官方消息与事件文档](https://textual.textualize.io/guide/events/)。
- 信号通知：`Signal` 提供发布／订阅机制，可以在发布数据时调用订阅者的回调，参见[官方 Signal API](https://textual.textualize.io/api/signal/)。它可以实现类似信号槽的通知效果，但不代表与 Qt 信号槽具有完全相同的语义。
- 响应式状态：`reactive` 属性与 `watch_*` 方法支持状态变化后的界面刷新和联动，参见[官方响应式状态文档](https://textual.textualize.io/guide/reactivity/)。
- 后台任务：Worker 支持异步任务和线程任务；线程 Worker 可通过线程安全的 `post_message` 传递结果，或通过 `call_from_thread` 在界面线程执行更新，参见[官方 Worker 文档](https://textual.textualize.io/guide/workers/)。

上述内容说明框架能力；项目具体采用哪些通信机制、如何组织后台任务及调度运行循环，仍留待后续设计。

## 生成插件模型

一次生成操作可以选择多份 rotation，并产生一个 WoW 插件包：

- 包名由用户输入，必须匹配 `[A-Za-z][A-Za-z0-9_]*`。
- 插件目录和 `.toc` 文件使用完全相同的包名。
- 通用能力写入共享基础模块。
- 每份 rotation 生成一个 `<uuid>.lua`，其中 UUID 使用带连字符的标准 RFC 4122 文本。
- 每个 UUID Lua 在加载开头检查 `unit_class` 和 `unit_spec`；不匹配时立即 `return`，不加载其余逻辑。
- `unit_spec` 是 `GetSpecialization()` 返回的专精顺序索引，取值为 1、2、3 或 4。
- 切换专精后需要执行 `/reload`。当前不支持运行期热切换。

生成 UI 以表格展示 rotation，第一列是复选框。选中一份 rotation 时，UI 必须取消其他已选且具有相同 `(unit_class, unit_spec)` 的 rotation；不同职业或专精的选择可以共存。

## 循环语义

每一轮执行以下业务步骤：

1. 截取像素画布。
2. 更新所需条件实例的原始数据与业务值。
3. 从上到下求值 `rotation` 列表。
4. 第一个条件为真的条目胜出，并发送其宏键位。
5. 全部未命中时不发送按键。

每轮最多执行一个动作。“暂停”表示某一轮没有动作，不是一个需要额外恢复的持久状态。

## 预定源码结构

以下目录是未来代码工程的职责规划，不要求在当前文档阶段创建空目录：

```text
phantom/
  ui/
  core/
  lua/
    runtime/
    general/
  conditions/
  actions/
  captures/
scripts/
rotations/
  main.py
```

`phantom/lua/runtime/` 保存生成器使用的共享 Lua 运行时源码。这些源码会进入生成后的 WoW 插件，为条件插件生成的实例 Lua 提供公共运行能力；条件专属模板仍保存在对应的 `phantom/conditions/<name>@<version>/template.lua` 中。该目录不保存生成后的插件产物。

`phantom/lua/general/` 保存第一行通用字段的 Lua 实现，在 TOC 中于 runtime 文件之后加载。通用 Cell 仍使用 runtime 提供的普通 `Cell`，通过 `UIInitFuncs` 延迟创建以沿用共享尺寸换算和背景初始化；不另设 GeneralCell 类型。首个实现为 `01_player_class.lua`，文件头 `index: 1` 表示通用文件顺序元数据。

## 截图基础运行边界

`python -m rotations.main` 是未来 Textual 主程序入口，当前仅运行最小入口说明，不启动截图。
截图通过 `phantom/captures/gdi@1.0/demo.py` 独立验证，暂不连接 TUI 或 rotation 执行器。

共享图像算法与线程调度位于 `phantom/captures/`。后端只负责截图，线程负责全屏定位、局部截图、校验和交付最新结果。
截图使用独立后台线程，不使用子进程。主线程通过快照接口取得最新图像与状态，不排队保留历史帧。
截图 FPS 仅限制采集，不定义未来 rotation 求值或动作发送的循环频率。

## 待定事项

- 循环频率、节流策略和运行期调度模型。
- Textual TUI 除已确认的 rotation 表格、首列复选框及互斥选择规则之外的完整界面行为，以及具体通信方案。
- 天赋感知的 rotation 路由和对应重载规则。
- `phantom/lua/runtime/` 内共享基础模块的文件拆分，以及它们与各 UUID Lua 的最终生成文件关系。

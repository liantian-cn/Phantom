# 系统架构

## 运行边界

Phantom 分为游戏外 Python 端和游戏内 Lua 端。Lua 端只负责采集游戏状态、编码与渲染数据以及建立已配置的安全按钮绑定；Python 端负责生成、截图、解码、求值和发送按键。

```text
rotation TOML
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
- Textual TUI：承载采集启停、游戏与采集状态、第一行通用数据展示和业务日志；支持配置指定的单份 rotation 生成和条件值；多份选择和决策展示留到后续步骤（见 [tui.md](tui.md)）。

## Textual 通信与任务

界面通过 Textual 的消息机制与后台任务协作，项目当前采用以下方式：

- 消息与事件：游戏检测结果、业务日志和停止完成通过自定义 `Message` 与 `post_message` 从后台线程投递到界面线程，再由消息处理方法更新控件，参见[官方消息与事件文档](https://textual.textualize.io/guide/events/)。
- 后台任务：阻塞的截图停止与资源释放通过线程 Worker 执行，不在界面线程调用阻塞接口，参见[官方 Worker 文档](https://textual.textualize.io/guide/workers/)。
- 主题：用 `register_theme` 注册固定纯黑深色的 `phantom-monochrome` 主题，颜色角色集中定义在 `phantom/ui/theme.py`。
- 测试：用 `run_test` 驱动真实控件、按键和尺寸变化，验证标签页、按钮状态与数据刷新。

当前不使用 `Signal` 与响应式属性 `reactive`；状态更新由显式消息和刷新方法完成。

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

以下目录是代码工程的职责划分；`phantom/ui`、`phantom/core`、`phantom/captures`、`phantom/lua` 和 `rotations` 已在使用，`phantom/conditions` 已实现版本化条件，`phantom/actions` 仍是后续占位：

```text
phantom/
  ui/
  core/
    condition/
    capture/
    pixels/
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

`python -m rotations.main` 是 Textual 主程序入口：读取启动工作目录的应用配置、运行界面，并在退出时等待后台线程释放。
截图与像素解析仍由 `demo/demo.py` 和 `demo/demo01.py` 独立验证，demo 不经过 TUI，也不读取应用配置。

共享图像算法与线程调度位于 `phantom/core/capture/`，`phantom/captures/` 只存放版本插件。后端只负责截图，线程负责全屏定位、局部截图、校验和交付最新结果。
UI 通过截图核心注册器按 capture.plugin 创建后端，默认 gdi@1.0；不直接导入版本实现。
截图使用独立后台线程，不使用子进程。主线程通过快照接口取得最新图像与状态，不排队保留历史帧。
截图 FPS 仅限制采集，不定义未来 rotation 求值或动作发送的循环频率。

## 待定事项

- 循环频率、节流策略和运行期调度模型。
- 天赋感知的 rotation 路由和对应重载规则。


## 单份生成器落地

phantom/core/rotation.py 负责配置和布局回写，core/condition/registry.py 负责精确加载，core/generator.py 负责生成。
当前单份入口输出 runtime/ 与 general/ 源码副本、完整 media/ 二进制资源、一个 UUID Lua 和同名 TOC；不复制 examples。字体与纹理由 Lua 路径访问，不加入 TOC。
UUID Lua 开头检查玩家职业和专精，随后每个模板置于独立 do/end 作用域并注册 UIInitFuncs。
生成所有声明的条件；模板只插入经过校验的参数与固定位置，不插入表达式或宏文本作为 Lua。
同名文件覆盖、旧文件保留，TOC 最后写入且仅列本次产物。每个目标文件使用同目录临时文件替换，避免单文件截断；不提供整个目录的事务或备份。
当前不生成安全按钮和覆盖键位；多 rotation 选择及宏绑定仍留待后续阶段。

## 单帧决策报告

`core/expression.py` 负责加载期白名单／类型校验和运行期 AST 解释；`Rotation.trial` 依次进行同帧条件解码与首条命中求值。
返回结果包含该帧条件值、命中规则与可选宏；Idle 的宏为空。
TUI 启动后的采集流程与独立 `demo/demo02.py` 复用此入口，只输出决策，不接入 action。

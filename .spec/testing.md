# 测试规则

## 测试边界

Phantom 最终运行在 Windows，而日常开发环境是 WSL2 与 Docker。容器无法真实覆盖 GDI 截图、Windows 窗口消息和游戏内受保护 Lua 行为，因此不得为了形式完整而编造无效的跨平台集成测试。

这不代表跳过可验证逻辑。与平台无关、容易出错且影响协议一致性的算法必须测试。

## 优先测试内容

- TOML schema、唯一标题/宏名称、UUID、职业/专精和键位校验。
- 白名单 AST 的允许节点、拒绝节点、优先级、条件引用和类型检查。
- rotation 自上而下首个命中、每轮最多一个动作和无命中行为。
- Cell 中间 2×2 与 Icon Tile 中间 6×6 的裁剪。
- Value Bar 中间两行、严格纯白判断和 `0.0`–`100.0` 百分比。
- Icon Tile 全黑空值、连续数组 hash 和多槽位 `None` 占位。
- 插件参数校验、输出数量冻结、Lua/Python 成对编解码和兜底。
- 多行独立紧密布局、声明顺序和画布最大宽度。
- WoW 连字符键位到 Windows 输入的映射。
- 应用配置的工作目录定位、缺失字段默认值、已有文件不被改写和非法输入拒绝。
- 游戏检测的 `wow.exe` 名称与 `_retail_` 直接父目录判定、无法核验的候选路径、游戏退出自动暂停与返回后手动启动。
- TUI 的标签切换、按钮可用性、最小尺寸提示、慢速停止期间的响应性、业务日志时间戳与连续去重、暂停或失败后清空旧数据。
- 截图线程终止与可恢复错误的区分、显式重新启动、退出后后台线程结束。

## 测试质量

- 测试业务与算法结果，不写只比较大段固定字符串的脆弱测试。
- 生成代码测试应检查结构、契约和关键语义，不依赖无意义的空格或换行。
- 每个已知边界至少覆盖正常值、边界值和不可用输入。
- catch-all 解码兜底不能代替插件单元测试；确定性编程错误仍须被测试发现。
- 所有手写 Python 源码必须通过 mypy strict 静态类型检查。
- 截图测试输入完整合成图像或图像序列，验证定位、裁剪、中心颜色及 worker 的业务状态流转；不写简单字符串或算术测试。

## 分层验证

| 层级 | 执行环境 | 目标 |
| --- | --- | --- |
| 纯 Python 单元测试 | Windows、WSL2、容器 | 表达式、布局、schema、编解码、键位映射 |
| NumPy 图像算法测试 | Windows、WSL2、容器 | 裁剪、白色占比、空 Icon Tile、hash |
| 生成产物结构检查 | Windows、WSL2、容器 | TOC、共享模块、UUID Lua 和条件提前返回 |
| Windows GDI/PostMessage 集成 | Windows | 在 Windows 环境验证窗口定位、截图和按键发送 |
| WoW 游戏内验证 | 安装目标游戏的 Windows | 在目标 12.1 build 验证 API、渲染、安全按钮和保护状态 |

只有后两层才能证明完整端到端行为；容器测试结果不得被描述为已经验证 Windows 或游戏运行。

## 当前工程检查

在仓库根目录执行（已按开发规则安装依赖）：

```powershell
.venv/Scripts/python -m pytest
.venv/Scripts/python -m mypy
.venv/Scripts/python -m ruff check phantom rotations tests demo
.venv/Scripts/python -m ruff format --check phantom rotations tests demo
```

图像测试覆盖边界尺寸、精确角标、多基板歧义、DEBUG 拒绝、中心像素污染与边缘容忍、Flash 黑白、
负坐标桌面、色错保留区域与恢复、移动后重新定位、最新结果所有权、停止和重启、运行中更新 FPS 与底层错误交付。
数组保存测试应比较重新加载的 dtype、shape、RGB 内容及关联状态，不比较 JSON 排版。

Windows 可运行定时 demo 验证真实 GDI 调用、停止及文件输出。无非 DEBUG 基板时应得到 `has_error=true` 和未定位原因，不生成 NPY。
2026-09-12 用户确认第三步截图已测试成功；当日像素解析 demo 也成功读取当前游戏基板。
真实游戏验收使用非 DEBUG 画面；移动重定位等具体场景仍以各任务实际验证记录为准。
桌面 smoke test 与合成图像测试不能代替游戏验收。

像素解析测试见 `tests/test_pixels.py`，覆盖 Lua 坐标切分、边缘污染、严格黑白、无有效黑白像素、
空槽及非空 hash、非连续数组、独立只读快照和缓存、区域越界及 demo 错误结果拒绝。
运行 `python demo/demo01.py` 可验证同一游戏截图的十个 Cell、一个 ValueBar 和两个 IconTile。
2026-09-12 实测第一行亮度为 `6,1,255,0,0`，第二行为 `255,0,0,0,255`，
ValueBar ratio 为 `1.0`、percent 为 `100.0`，两个 IconTile 均为空槽 `None`。
非空 IconTile hash 已由合成图验证，本次游戏画面未覆盖非空图标。

TUI 与应用生命周期测试见 `tests/test_ui.py`、`tests/test_configuration.py` 和 `tests/test_game.py`。
它们使用 Textual 的 `run_test` 驱动真实控件、按键与尺寸变化，并用假截图 worker 覆盖标签切换、最小尺寸提示、
慢速停止、线程终止、游戏退出自动暂停和日志淘汰；游戏与路径判定使用伪造进程，不依赖游戏运行。
2026-09-12 在 Windows 执行 `python -m pytest` 得到 82 passed，`python -m mypy`（strict）与
`ruff check`／`ruff format --check` 均通过。

同日完成 Windows 桌面 smoke 验证：真实入口在启动工作目录创建默认 `phantom.toml`，界面以暂停状态打开，
未检测到游戏时“启动”保持禁用，标签顺序为综合→通用条件→日志→宏绑定→循环条件，Ctrl+Q 正常退出且不残留 `phantom-` 线程；
该次验证记录的浅色解析样式（Base `#eff1f5`、Text `#4c4f69`、Mantle `#e6e9ef`、Blue `#1e66f5`）随同日主题改为 Catppuccin Mocha 深色而失效。
深色主题通过 Textual 真实控件运行（`run_test`，120×46）重新解析：活动主题为 `phantom-mocha`（dark），Screen 背景为 Base `#1e1e2e`、
正文为 Text `#cdd6f4`、容器为 Mantle `#181825`、选中与强调为 Blue `#89b4fa`，
状态行“程序”使用 Peach `rgb(250,179,135)`、“游戏”使用 Green `rgb(166,227,161)`，CSS 变量中不再存在 `latte-*`。
本次环境无法分配交互式终端（ConPTY 创建失败），未重复桌面终端 smoke；以上深色证据来自真实控件的解析样式，不是终端截图。
同一环境直接启动 GDI 线程时，无基板会得到 `has_error=true`、原因“未找到非 DEBUG 基板定位标记”，线程保持运行并可正常停止。
以上 smoke 验证不带游戏画面，不能代替游戏内验收：第 6 步要求的“游戏内改变状态、TUI 随之变化”尚未执行。

## 待定事项

- 覆盖率工具。
- Windows 手工验证清单与可重复测试环境。
- WoW 12.1 build 的兼容矩阵和回归频率。

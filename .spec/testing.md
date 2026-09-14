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
该次验证记录的浅色解析样式（Base `#eff1f5`、Text `#4c4f69`、Mantle `#e6e9ef`、Blue `#1e66f5`）在同日主题先后改为 Catppuccin Mocha 与 Flexoki 后失效。
纯黑主题通过 Textual 真实控件运行（`run_test`，120×46）重新解析：活动主题为 `phantom-monochrome`（dark，primary `#FFFFFF`，background `#000000`），
Screen 背景为 `#000000`、正文为 `#EDEDED`、容器为 `#111111`，状态行正常使用 `#4ADE80`，暂停和未运行使用 `#A1A1AA`。
本次环境无法分配交互式终端（ConPTY 创建失败），未重复桌面终端 smoke；以上深色证据来自真实控件的解析样式，不是终端截图。
同一环境直接启动 GDI 线程时，无基板会得到 `has_error=true`、原因“未找到非 DEBUG 基板定位标记”，线程保持运行并可正常停止。
以上 smoke 验证不带游戏画面，不能代替游戏内验收：第 6 步要求的“游戏内改变状态、TUI 随之变化”尚未执行。

## 待定事项

- 覆盖率工具。
- Windows 手工验证清单与可重复测试环境。
- WoW 12.1 build 的兼容矩阵和回归频率。


## 第 7–10 步离线验收（2026-09-12）

新增配置、布局、多区域、插件参数、灰度/充能/冷却解码、Lua 生成及 TUI 集成测试。
160 项 pytest 通过；mypy strict、Ruff check 与 format --check 通过。
`condition.py` 在含 @ 的精确版本目录下不能作为普通包被 mypy 合并扫描（会冲突为同名模块）。
统一类型检查入口为 `.venv/Scripts/python scripts/check_types.py`：先检查核心/tests/scripts，
再逐个检查八个精确版本 condition.py，任何失败都返回非零；不跳过插件检查。
Ruff 命令增加 scripts 目录。运行依赖新增 tomlkit==0.15.1，开发依赖新增 lupa==2.8。
测试使用 lupa.lua51 编译全部生成 Lua，执行真实生成条件模板与 API doubles，再把输出构造成完整 NumPy 基板验证 Python 业务值。
特别覆盖 GCD 不查询法术书、固定 61304/false、无 duration 输出黑色、普通技能筛选和职业专精不匹配不注册条件。
TUI run_test 覆盖无游戏生成、错误后修复重试、同帧条件值、暂停/专精不匹配清空、慢速生成期间响应与退出等待。
实际 `E:\World of Warcraft\_retail_\Interface\AddOns\Phantom` 已生成 23 个文件（含 6 个 media 资源），TOC 引用 16 个存在的 Lua，全部通过 Lua 5.1 解析，未引用 examples。
没有启动游戏、安装宏绑定或发送按键；该记录仅证明离线生成与算法，不证明游戏端 API/渲染。

## 插件职责重构验收（2026-09-13）

核心与版本目录分离后，228 项 pytest 通过，scripts/check_types.py 严格检查核心及八个条件、一个截图入口通过；Ruff check 与 format --check 均通过。
新增校验器/解码器边界、临时截图插件精确加载与错误上下文、默认与显式配置、UI 前失败、非默认 Lua 坐标/宽度、冷却全区间配对测试。
Windows 使用核心截图注册器创建默认 GDI，以 5 FPS 完成两次启动和停止；均报告未找到非 DEBUG 基板，停止后没有 phantom- 线程。
该 smoke 验证真实 GDI 调用、错误交付与资源释放，未取得游戏基板，不代表游戏内验收。

## 第 11–13 步验收（2026-09-13）

275 项 pytest、`scripts/check_types.py`（核心及各精确版本入口）、Ruff check 与 format --check 通过。
表达式回归覆盖白名单、比较／成员／布尔组合、类型不匹配、禁止隐式真假值、加载失败不回写、短路与 AST 复用；rotation 回归验证首条命中与 Idle。
TUI 回归覆盖同帧条件及决策、宏名称日志去重、单次报告、无命中替换旧动作、截图失败／职业专精不匹配／暂停清空。

独立单次试运行：`.venv/Scripts/python demo/demo02.py [rotation.toml]`。
遵循 demo 的等待 3 秒、采集 5 秒流程，用最后结果解码求值一次，报告所有条件、命中规则、宏名称及键位，不发送按键。
真实游戏基板为 `(20,36,3)`，八项值为 `0.0, 6, 2, False, 0.0, 0.0, 100.0, False`，命中第 3 条“死神的抚摩冷却==0”，报告“死神的抚摩 / CTRL-NUMPAD3”。
Textual `run_test` 连接真实游戏检测与 GDI 得到相同结果，日志窗口存在宏名称及单次试运行详情，停止清空决策，退出后无 phantom 线程。
这是当前静态游戏帧与真实控件验证，不代表已覆盖新的游戏内动态场景或真实动作执行；未重生成／安装 Lua，也未发送游戏按键。

2026-09-13 后续调整：按用户要求移除 TUI 单次试运行按钮，决策与宏名称日志统一随启动后的采集刷新；独立 demo 保留。TUI 回归直接验证自动决策和日志。

2026-09-13 提交前复核：原 275 项测试中有两项在 Textual 卸载控件期间刷新失败。
刷新入口增加应用消息循环运行状态检查；新增两种截图线程状态下的真实界面卸载回归，修复前均复现 `#decision` 缺失，修复后完整 pytest 为 277 passed。
完整严格类型检查、Ruff check 与 format --check 通过；退出回归同时确认采集停止及无残留 phantom 线程。本次未重复真实游戏验证。


## 第 14–17 步离线与 Windows 消息验收（2026-09-14）

本次实现键盘插件、宏绑定生成、通用布尔表达式及新帧驱动运行。368 项 pytest 通过，5 项既有符号链接路径逃逸测试因 Windows 缺少创建链接权限跳过；不将跳过描述为已验证。完整 scripts/check_types.py 严格类型检查通过，包含八个条件、一个截图及一个键盘版本入口。

- 键位：合法/非法组合、全部声明键的 Windows 映射、精确插件加载、窗口标题精确唯一匹配、发送顺序和部分失败释放。
- Windows：真实 PostMessageW 仅发送至测试创建的隐藏窗口，验证 CTRL-1 / ALT-F4 的消息队列及逆序释放；未向实际游戏发键。
- 生成：Lua 5.1 解析、标准安全按钮/覆盖绑定 API doubles、多行/引号/反斜杠/控制字符文本保真、bind_key=false 不生成绑定、职业专精守卫。
- 运行：新帧去重、相同内容的新帧、Idle/恢复、无效截图、引用布尔变量的黑白校验、未引用字段不门控、停止等待释放、失败后手动重启、界面响应与清空。
- 双插件：精确加载的合成截图后端复用真实 ThreadCaptureWorker 定位裁剪与帧发布，再由实际 RotationRuntime 决策，交给精确加载的记录型键盘后端。无第二种真实截图或键盘设备实现。

完整检查使用 pytest、scripts/check_types.py、ruff check 和 ruff format --check（phantom rotations tests demo scripts）。独立 demo/demo02.py 继续只报告，不发送按键。

待有游戏环境后，使用普通键和组合键核对游戏动作、重载生成绑定并检查 bind_key 两种模式；验证启用/延迟表达式、Idle 后恢复、持续运行与停止。当前没有安装生成产物，也未验证真实游戏动作或持续闭环。

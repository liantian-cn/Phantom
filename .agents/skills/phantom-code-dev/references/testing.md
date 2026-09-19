# 测试规则

## 测试边界

Phantom 最终运行在 Windows，而日常开发环境是 WSL2 与 Docker。容器无法真实覆盖 GDI 截图、Windows 窗口消息和游戏内受保护 Lua 行为，因此不得为了形式完整而编造无效的跨平台集成测试。

这不代表跳过可验证逻辑。与平台无关、容易出错且影响协议一致性的算法必须测试。

## 优先测试内容

- TOML schema、唯一标题/宏名称、UUID、职业/专精和键位校验。
- rotation 默认参数补写：全部校验及布局成功后才写、所有 load_rotation 入口一致、构造与回写共享 config_defaults、递归补充已有嵌套字典、保留 false/0/合法空值、拒绝非法显式值及缺失必填字段；dispel_types 整体必填且只补七个缺失子键为 false。
- rotation 写入边界：无默认不创建空 plugin_args、无变更不写、保留注释和其他内容、原子替换、并发源检查、写入失败导致加载失败、后续生成失败不回滚；旧 conditions[].layout 兼容忽略且不增改删，内存布局保持原规则，phantom.toml 不受影响。
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

## 工程检查

在仓库根目录执行，按改动选择相关检查；业务改动应完成相应测试：

```powershell
.venv/Scripts/python -m pytest
.venv/Scripts/python scripts/check_types.py
.venv/Scripts/python -m ruff check phantom rotations tests demo scripts
.venv/Scripts/python -m ruff format --check phantom rotations tests demo scripts
```

`scripts/check_types.py` 先检查核心、测试与脚本，再逐个检查精确版本插件入口。单独运行 mypy 会遗漏含 `@` 的版本目录；不能因模块同名冲突而跳过插件。

## 按改动选择验证

| 改动 | 现有验证入口和重点 |
| --- | --- |
| 像素和截图 | `tests/test_pixels.py`、截图相关测试；合成图像、定位、裁剪、所有权、启动停止和错误结果 |
| TUI 和应用配置 | `tests/test_ui.py`、`tests/test_configuration.py`、`tests/test_game.py`；真实控件、消息、清空过期数据和退出 |
| 条件插件 | `tests/test_conditions.py`、`tests/test_player_conditions.py`、`tests/test_condition_frame.py`；同帧 decoder、参数、兜底、Lua/Python 配对 |
| 生成和循环 | `tests/test_generator.py`、表达式与 rotation 测试；Lua 5.1、类型白名单、首条命中、Idle、新帧去重 |
| 键盘 | 键盘与 runtime 测试；按下/逆序释放、部分失败、停止等待和窗口唯一性 |

生成 Lua 使用 `lupa.lua51` 解析，现有 API doubles 配合真实 Cell/IconTile 等消费者验证；doubles 不能证明 WoW 的全部秘密值和访问限制。
rotation 离线检查使用临时副本：`load_rotation()` 可能补写缺失的条件插件默认参数，不能把正式配置当成只读验证输入；旧 layout 字段只兼容接收并忽略，不回写布局。
Windows 消息测试仅对测试创建的隐藏窗口发送。真实游戏按键、宏绑定、渲染和闭环验收单独报告。

独立 demo 统一先说明演示内容、等待 3 秒、采集 5 秒：`demo/demo.py` 验证截图，`demo/demo01.py` 验证像素，`demo/demo02.py [rotation.toml]` 用最后结果解码求值并只报告，不发送按键。
数组保存验证重新加载后的 dtype、shape、RGB 内容及状态，不比较 JSON 排版。桌面 smoke 和合成图像不能代替游戏验收。

## 待定事项

- 覆盖率工具。
- Windows 手工验证清单与可重复测试环境。
- WoW 12.1 build 的兼容矩阵和回归频率。

## 历史证据

仅追溯过去验收时读取 [历史验收记录](history/verification-history.md)；旧数量和游戏结果不是当前保证。

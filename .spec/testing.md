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

## 待定事项

- 覆盖率工具。
- Windows 手工验证清单与可重复测试环境。
- WoW 12.1 build 的兼容矩阵和回归频率。

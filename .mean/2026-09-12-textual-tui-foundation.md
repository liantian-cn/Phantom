---
plan: .plan/2026-09-12-textual-tui-foundation.md
related_paths:
  - phantom/ui/
  - phantom/core/configuration.py
  - phantom/core/game.py
  - phantom/captures/contracts.py
  - phantom/captures/worker.py
  - rotations/main.py
  - tests/test_configuration.py
  - tests/test_game.py
  - tests/test_ui.py
  - tests/test_capture.py
  - requirements.txt
  - requirements-dev.txt
  - .spec/README.md
  - .spec/tui.md
  - .spec/configuration.md
  - .spec/architecture.md
  - .spec/development-rules.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .context/README.md
  - .context/catppuccin-latte.md
  - todo_list.md
  - .prompt/2026-09-12-textual-tui-foundation.md
---

## 意图 (Intent)

按 todo_list.md 实施第 5、6 步 Textual TUI 基础和基础采集数据展示。工作目录就是系统传入的启动目录，与程序路径无关。配置名 phantom.toml，截图 FPS 默认 15。采用给定 Catppuccin Latte 配色；content 顶部 tabs，footer 底部单行 status_line。综合页由 Agent 设计左右布局和当前工作状态面板；通用条件显示五个 Cell 的 RGB 与纯色 mean，显示值留空。Implement the plan.

## 约束 (Constraints)

Windows 下以用户提供的参考为准，不依赖不可见的根目录外部参考。默认暂停，关闭停止采集并保留 TUI。无 _retail_/wow.exe 时禁止启动，游戏退出自动暂停，回来后手动启动。缺配置自动创建，仅启动读取。小于 120×46 显示尺寸提示。日志独立 log 方法、生成时间戳、连续相同正文去重、最多 1000 行并记录状态变化。暂停或无效帧清空旧数据。Tab/Shift+Tab 切页，方向键选择按钮。生成插件、宏绑定、循环条件仅保留占位。配色写入 spec 与 context。完成检查后原子本地提交。

## 被拒绝的替代方案 (Rejected Alternatives)

本次不额外实现插件生成，也不隐藏未来入口；不自动开始或在暂停时继续采集。配置缺失不报缺失错误，也不只使用内存默认值。小窗口不保留超大可滚动布局。日志不只限制视口、不限制为 20 行。失效不保留过期原始数据。页内按钮不用 Ctrl+Tab 移动焦点。游戏检测不只用于显示。日志不保持空白。

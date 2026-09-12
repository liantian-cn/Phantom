---
plan: .plan/2026-09-12-tui-monochrome-theme.md
related_paths:
  - phantom/ui/theme.py
  - phantom/ui/app.py
  - phantom/ui/app.tcss
  - tests/test_ui.py
  - .spec/tui.md
  - .spec/architecture.md
  - .spec/testing.md
---

## 意图 (Intent)

将 Phantom TUI 改为纯黑画布、深灰面板、灰白强调和明亮状态色，参考 Codex 默认配色观感。

## 约束 (Constraints)

保持现有布局、交互、采集逻辑和第六项 TODO 验收边界；不增加主题切换。

## 被拒绝的替代方案 (Rejected Alternatives)

继续使用 Flexoki 当前暖黑底和偏暗的绿红配色；用户选择了新的纯黑与明亮状态色方案。

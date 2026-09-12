## Goal

将第六项 TUI 的视觉配色改为纯黑底、深灰面板和明亮状态色，改善绿色与红色过暗的问题。

## Scope

涉及 `phantom/ui/theme.py`、`phantom/ui/app.py`、`phantom/ui/app.tcss`、`tests/test_ui.py` 及相关规范记录；不改变布局、交互或第六项验收状态。

## Decisions

- 主背景使用 `#000000`，面板使用 `#111111`，悬停使用 `#222222`，边框使用 `#333333`。
- 正文使用 `#EDEDED`，次要文字使用 `#A1A1AA`，焦点和选中强调使用 `#FFFFFF`。
- 正常使用亮绿，暂停/未运行使用灰色，警告使用黄色，错误使用亮红。
- 主题名称为 `phantom-monochrome`，不提供主题切换或配置项。

## Implementation Steps

- 更新主题颜色角色与 Textual 主题注册。
- 更新状态行映射及控件样式，保留现有布局和行为。
- 更新主题测试与规范中的当前主题描述。

## Acceptance Criteria

- TUI 主背景为纯黑，面板与正文层次清晰。
- 状态颜色符合正常、暂停、警告和错误语义。
- 现有测试、类型检查、Ruff 检查和格式检查通过。

## Verification

2026-09-12: Full `pytest` passed 83 tests on rerun of the previously timing-sensitive UI case; `mypy`, `ruff check`, and `ruff format --check` passed.

## Review Notes

2026-09-12: 用户确认继续实施已确认的配色方案。

## Completion

Implemented; full repository verification recorded after final checks.

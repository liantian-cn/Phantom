---
plan: .plan/2026-09-11-fix-icon-tile-background-layer.md
related_paths:
  - phantom/lua/runtime/09_icon_tile.lua
  - .prompt/2026-09-11-fix-icon-tile-background-layer.md
---

## 意图 (Intent)

修复没有施法时 IconTile 显示 DEBUG 蓝底而不是自身黑底的问题。Implement the plan.

## 约束 (Constraints)

如有必要可调整 phantom\lua\runtime\04_baseline_definition.lua 定义的层级或新增层级。确认方案采用已有 FrameLevel.Cell = 9600，高于背景 9500，无需改动层级定义。保持当前坐标、Clear 行为和施法颜色；只提交本次修复与档案，保留此前未提交的坐标修正及其他改动。

## 被拒绝的替代方案 (Rejected Alternatives)

None

---
plan: .plan/2026-09-11-add-lua-cell-examples.md
related_paths:
  - phantom/lua/examples/01_spell_cooldown.lua
  - phantom/lua/examples/02_spell_overlay.lua
  - phantom/lua/examples/03_spell_usable.lua
  - phantom/lua/examples/04_player_buff.lua
  - phantom/lua/examples/05_player_health.lua
  - phantom/lua/addonTemplateName.toc
  - .prompt/2026-09-11-add-lua-cell-examples.md
---

## 意图 (Intent)

在第三步解码开始之前，在 phantom/lua/examples 下新增五个示例，方便填充 Lua 区域和后续开发：技能冷却、技能高亮、技能可用、玩家存在指定增益、玩家血量。加入 TOC，直接显示在第二行第 1–5 列。

Implement the plan.

## 约束 (Constraints)

沿用 general 的代码风格，uuid 使用 {{uuid}}，技能名称和 RotationsCell 只作为注释，局部大写参数放在前面。保留用户指定的技能 ID 顺序。前三块选首个已学会 ID，SPELLS_CHANGED 时重选，全部未命中黑色。冷却采用给定灰度曲线，ignoreGCD 默认 true，无 duration 对象时黑色。冷却与可用采用独立随机错峰的 0.1 秒 OnUpdate；高亮按指定事件刷新。增益完全交由 AuraContainer 管理；血量 usePredicted 默认 true，通过玩家血量事件刷新。复用已有 Cell:setCell。只提交本任务内容。

## 被拒绝的替代方案 (Rejected Alternatives)

多技能 ID 不采用“任意技能满足”或“最后一个已学会 ID”；冷却不采用只有黑白两态；示例不采用仅保存源码而不加入 TOC；无 duration 对象时不显示白色。

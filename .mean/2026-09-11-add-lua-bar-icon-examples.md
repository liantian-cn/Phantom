---
plan: .plan/2026-09-11-add-lua-bar-icon-examples.md
related_paths:
  - phantom/lua/examples/06_spell_charges.lua
  - phantom/lua/examples/07_player_cast.lua
  - phantom/lua/examples/08_target_cast.lua
  - phantom/lua/addonTemplateName.toc
  - .prompt/2026-09-11-add-lua-bar-icon-examples.md
---

## 意图 (Intent)

在第三步解码开始之前，增加一个技能充能 ValueBar 和玩家、目标施法的两个 IconTile，填充 Lua 区域并方便后续开发。代码风格参考已有 Cell 示例，本地大写参数供未来 plugin 替换。Implement the plan.

## 约束 (Constraints)

血液沸腾候选 ID 为 50841、50842，按技能书顺序选首个；宽度及最大值为 2，最小值为 0，反向填充 false，不存在或无充能信息时为 0。两个 IconTile 直接传入 1、2，接受现有左侧空隙。无施法或无目标时 Clear；玩家使用 PLAYER_SPELL；目标普通 nil 的可打断信息按不可打断着色。保留指定事件，包括 PLAYER_ENTERING_WORLD。只提交本任务文件，保留已有改动。

## 被拒绝的替代方案 (Rejected Alternatives)

IconTile 不采用修正 runtime 为紧密排列或仅在示例换算坐标的方案。目标 notInterruptible 为普通 nil 时，不采用隐藏角标或按可打断着色。

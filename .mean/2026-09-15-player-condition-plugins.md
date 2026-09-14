---
plan: .plan/2026-09-15-player-condition-plugins.md
related_paths:
  - .prompt/2026-09-15-player-condition-plugins.md
  - .spec/plugin-system.md
  - .spec/testing.md
  - phantom/conditions/liantian_cn.player_cast_icon@dev/condition.py
  - phantom/conditions/liantian_cn.player_cast_icon@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_cast_icon@dev/template.lua
  - phantom/conditions/liantian_cn.player_cast_progress@dev/condition.py
  - phantom/conditions/liantian_cn.player_cast_progress@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_cast_progress@dev/template.lua
  - phantom/conditions/liantian_cn.player_cast_target@dev/condition.py
  - phantom/conditions/liantian_cn.player_cast_target@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_cast_target@dev/template.lua
  - phantom/conditions/liantian_cn.player_damage_absorb@dev/condition.py
  - phantom/conditions/liantian_cn.player_damage_absorb@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_damage_absorb@dev/template.lua
  - phantom/conditions/liantian_cn.player_has_big_defensive@dev/condition.py
  - phantom/conditions/liantian_cn.player_has_big_defensive@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_has_big_defensive@dev/template.lua
  - phantom/conditions/liantian_cn.player_has_buff@dev/condition.py
  - phantom/conditions/liantian_cn.player_has_buff@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_has_buff@dev/template.lua
  - phantom/conditions/liantian_cn.player_has_dispellable_debuff@dev/condition.py
  - phantom/conditions/liantian_cn.player_has_dispellable_debuff@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_has_dispellable_debuff@dev/template.lua
  - phantom/conditions/liantian_cn.player_has_spell@dev/condition.py
  - phantom/conditions/liantian_cn.player_has_spell@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_has_spell@dev/template.lua
  - phantom/conditions/liantian_cn.player_has_talent@dev/condition.py
  - phantom/conditions/liantian_cn.player_has_talent@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_has_talent@dev/template.lua
  - phantom/conditions/liantian_cn.player_heal_absorb@dev/condition.py
  - phantom/conditions/liantian_cn.player_heal_absorb@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_heal_absorb@dev/template.lua
  - phantom/conditions/liantian_cn.player_heal_potion_ready@dev/condition.py
  - phantom/conditions/liantian_cn.player_heal_potion_ready@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_heal_potion_ready@dev/template.lua
  - phantom/conditions/liantian_cn.player_healthstone_ready@dev/condition.py
  - phantom/conditions/liantian_cn.player_healthstone_ready@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_healthstone_ready@dev/template.lua
  - phantom/conditions/liantian_cn.player_in_combat@dev/condition.py
  - phantom/conditions/liantian_cn.player_in_combat@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_in_combat@dev/template.lua
  - phantom/conditions/liantian_cn.player_in_group@dev/condition.py
  - phantom/conditions/liantian_cn.player_in_group@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_in_group@dev/template.lua
  - phantom/conditions/liantian_cn.player_in_vehicle@dev/condition.py
  - phantom/conditions/liantian_cn.player_in_vehicle@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_in_vehicle@dev/template.lua
  - phantom/conditions/liantian_cn.player_is_chatting@dev/condition.py
  - phantom/conditions/liantian_cn.player_is_chatting@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_is_chatting@dev/template.lua
  - phantom/conditions/liantian_cn.player_is_empowering@dev/condition.py
  - phantom/conditions/liantian_cn.player_is_empowering@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_is_empowering@dev/template.lua
  - phantom/conditions/liantian_cn.player_is_moving@dev/condition.py
  - phantom/conditions/liantian_cn.player_is_moving@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_is_moving@dev/template.lua
  - phantom/conditions/liantian_cn.player_is_player_target@dev/condition.py
  - phantom/conditions/liantian_cn.player_is_player_target@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_is_player_target@dev/template.lua
  - phantom/conditions/liantian_cn.player_is_targeting_spell@dev/condition.py
  - phantom/conditions/liantian_cn.player_is_targeting_spell@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_is_targeting_spell@dev/template.lua
  - phantom/conditions/liantian_cn.player_melee_enemies_count@dev/condition.py
  - phantom/conditions/liantian_cn.player_melee_enemies_count@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_melee_enemies_count@dev/template.lua
  - phantom/conditions/liantian_cn.player_role@dev/condition.py
  - phantom/conditions/liantian_cn.player_role@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_role@dev/template.lua
  - phantom/conditions/liantian_cn.player_trinket_ready@dev/condition.py
  - phantom/conditions/liantian_cn.player_trinket_ready@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_trinket_ready@dev/template.lua
  - tests/lua/player_conditions_harness.lua
  - tests/test_player_conditions.py
---

## 意图 (Intent)
根据过去项目制作 23 个玩家条件插件，统一放在 phantom/conditions 且全部为 dev；按已确认计划实施。完整要求见同名 prompt 的 R1–R14。

## 约束 (Constraints)
只读旧项目 Lua，借鉴秘密值、API、事件，着色和命名遵循本项目。保留坐骑、任意输入焦点、固定消耗品、旧轮询间隔和施法目标清理行为。所有插件添加 PLAYER_ENTERING_WORLD，移动延到下一帧，OnUpdate 使用 -random()。参数 snake_case；阈值非负整数；驱散允许空表。返回值及空值按已确认约定。只在 develop 修改并作原子本地提交。

## 被拒绝的替代方案 (Rejected Alternatives)
不借鉴 PhantomProject 的着色逻辑和命名规则；不保留原英雄天赋分类，改为技能/天赋两个等价插件。

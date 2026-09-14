---
plan: .plan/2026-09-14-remove-condition-decoders.md
related_paths:
  - phantom/core/condition/decoders.py
  - tests/test_decoders.py
  - tests/test_conditions.py
  - tests/test_condition_frame.py
  - .spec/plugin-system.md
  - .plugin-development/README.md
  - .plugin-development/conditions.md
  - phantom/conditions/liantian_cn.delaying@dev/condition.py
  - phantom/conditions/liantian_cn.enable@dev/condition.py
  - phantom/conditions/liantian_cn.in_burst@dev/condition.py
  - phantom/conditions/liantian_cn.player_health_pct@dev/condition.py
  - phantom/conditions/liantian_cn.player_primary_power@dev/condition.py
  - phantom/conditions/liantian_cn.spec_dk_rune@dev/condition.py
  - phantom/conditions/liantian_cn.spell_charges@dev/condition.py
  - phantom/conditions/liantian_cn.spell_cooldown@dev/condition.py
  - phantom/conditions/liantian_cn.spell_gcd@dev/condition.py
  - phantom/conditions/liantian_cn.spell_overlay@dev/condition.py
  - phantom/conditions/liantian_cn.spell_usable@dev/condition.py
  - .prompt/2026-09-14-remove-condition-decoders.md
---

## 意图 (Intent)

去掉 phantom/core/condition/decoders.py，所有插件直接访问 cell、value_bar、icontile 的各种方法，使代码更直观、更容易理解。Implement the plan.

## 约束 (Constraints)

插件内保留校验：在 decode_value 中直接使用像素属性并执行必要校验，保持当前业务结果及兜底行为。按确认计划迁移全部 11 个条件插件，保留 PixelDecoder 和现有接口；完成验证后在 develop 做一次原子本地提交，不推送。

## 被拒绝的替代方案 (Rejected Alternatives)

直接采用像素属性结果并删除额外颜色校验，接受混色均值和非白即 False 等行为变化。

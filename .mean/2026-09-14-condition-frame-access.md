---
plan: .plan/2026-09-14-condition-frame-access.md
related_paths:
  - .plugin-development/README.md
  - .plugin-development/conditions.md
  - .prompt/2026-09-14-condition-frame-access.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/pixel-protocol.md
  - .spec/plugin-system.md
  - .spec/testing.md
  - .spec/tui.md
  - phantom/conditions/liantian_cn.delaying@dev/condition.py
  - phantom/conditions/liantian_cn.delaying@dev/plugin.toml
  - phantom/conditions/liantian_cn.enable@dev/condition.py
  - phantom/conditions/liantian_cn.enable@dev/plugin.toml
  - phantom/conditions/liantian_cn.in_burst@dev/condition.py
  - phantom/conditions/liantian_cn.in_burst@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_health_pct@dev/condition.py
  - phantom/conditions/liantian_cn.player_primary_power@dev/condition.py
  - phantom/conditions/liantian_cn.spec_dk_rune@dev/condition.py
  - phantom/conditions/liantian_cn.spell_charges@dev/condition.py
  - phantom/conditions/liantian_cn.spell_cooldown@dev/condition.py
  - phantom/conditions/liantian_cn.spell_gcd@dev/condition.py
  - phantom/conditions/liantian_cn.spell_overlay@dev/condition.py
  - phantom/conditions/liantian_cn.spell_usable@dev/condition.py
  - phantom/core/condition/base.py
  - phantom/core/condition/contracts.py
  - phantom/core/condition/registry.py
  - phantom/core/rotation.py
  - phantom/ui/app.py
  - phantom/ui/capture.py
  - rotations/blood-dk.toml
  - tests/test_condition_frame.py
  - tests/test_conditions.py
  - tests/test_expression.py
  - tests/test_generator.py
  - tests/test_plugin_paths.py
  - tests/test_rotation.py
  - tests/test_runtime.py
  - tests/test_ui.py
---

## 意图 (Intent)

插件的 python 代码部分可以访问当前帧的 PixelDecoder 实例，按坐标读取任意 cell、valuebar、icontile。插件允许没有 lua 代码，生成空代码块。delay、爆发、enable 做成按配置加载的插件，条件名字以配置为准。

保留区域列表，增加 decoder。通用条件页只展示职业和专精。

## 约束 (Constraints)

保留 Lua，读取插件化：现有状态、控制面板和固定 Cell 保留。旧配置要求显式声明条件。兜底，但是 enable=True burst=False delay=False。

Implement the plan.

## 被拒绝的替代方案 (Rejected Alternatives)

完整按需生成 Lua 状态及 Cell；解码接口统一只接收 decoder；自动补齐旧条件；非法状态保留该帧失败行为；enable=False、delay=True 的兜底；通用条件页保留五项原始展示。

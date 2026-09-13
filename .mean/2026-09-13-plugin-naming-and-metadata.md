---
plan: .plan/2026-09-13-plugin-naming-and-metadata.md
related_paths:
  - .gitignore
  - .plugin-development/README.md
  - .plugin-development/captures.md
  - .prompt/2026-09-13-plugin-naming-and-metadata.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/plugin-system.md
  - .spec/project-overview.md
  - .spec/tui.md
  - demo/demo.py
  - demo/demo01.py
  - demo/demo02.py
  - phantom.toml
  - phantom/captures/gdi@1.0/capture.py
  - phantom/captures/liantian_cn.gdi@dev/capture.py
  - phantom/captures/liantian_cn.gdi@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_health_pct@dev/condition.py
  - phantom/conditions/liantian_cn.player_health_pct@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_health_pct@dev/template.lua
  - phantom/conditions/liantian_cn.player_primary_power@dev/condition.py
  - phantom/conditions/liantian_cn.player_primary_power@dev/plugin.toml
  - phantom/conditions/liantian_cn.player_primary_power@dev/template.lua
  - phantom/conditions/liantian_cn.spec_dk_rune@dev/condition.py
  - phantom/conditions/liantian_cn.spec_dk_rune@dev/plugin.toml
  - phantom/conditions/liantian_cn.spec_dk_rune@dev/template.lua
  - phantom/conditions/liantian_cn.spell_charges@dev/condition.py
  - phantom/conditions/liantian_cn.spell_charges@dev/plugin.toml
  - phantom/conditions/liantian_cn.spell_charges@dev/template.lua
  - phantom/conditions/liantian_cn.spell_cooldown@dev/condition.py
  - phantom/conditions/liantian_cn.spell_cooldown@dev/plugin.toml
  - phantom/conditions/liantian_cn.spell_cooldown@dev/template.lua
  - phantom/conditions/liantian_cn.spell_gcd@dev/condition.py
  - phantom/conditions/liantian_cn.spell_gcd@dev/plugin.toml
  - phantom/conditions/liantian_cn.spell_gcd@dev/template.lua
  - phantom/conditions/liantian_cn.spell_overlay@dev/condition.py
  - phantom/conditions/liantian_cn.spell_overlay@dev/plugin.toml
  - phantom/conditions/liantian_cn.spell_overlay@dev/template.lua
  - phantom/conditions/liantian_cn.spell_usable@dev/condition.py
  - phantom/conditions/liantian_cn.spell_usable@dev/plugin.toml
  - phantom/conditions/liantian_cn.spell_usable@dev/template.lua
  - phantom/conditions/player_health_pct@1.0/condition.py
  - phantom/conditions/player_health_pct@1.0/template.lua
  - phantom/conditions/player_primary_power@1.0/condition.py
  - phantom/conditions/player_primary_power@1.0/template.lua
  - phantom/conditions/spec_dk_rune@1.0/condition.py
  - phantom/conditions/spec_dk_rune@1.0/template.lua
  - phantom/conditions/spell_charges@1.0/condition.py
  - phantom/conditions/spell_charges@1.0/template.lua
  - phantom/conditions/spell_cooldown@1.0/condition.py
  - phantom/conditions/spell_cooldown@1.0/template.lua
  - phantom/conditions/spell_gcd@1.0/condition.py
  - phantom/conditions/spell_gcd@1.0/template.lua
  - phantom/conditions/spell_overlay@1.0/condition.py
  - phantom/conditions/spell_overlay@1.0/template.lua
  - phantom/conditions/spell_usable@1.0/condition.py
  - phantom/conditions/spell_usable@1.0/template.lua
  - phantom/core/capture/registry.py
  - phantom/core/condition/registry.py
  - phantom/core/configuration.py
  - phantom/main.py
  - rotations/blood-dk.toml
  - rotations/main.py
  - tests/test_capture_registry.py
  - tests/test_conditions.py
  - tests/test_configuration.py
  - tests/test_generator.py
  - tests/test_plugin_paths.py
  - tests/test_rotation.py
  - tests/test_ui.py
  - todo_list.md
---

## 意图 (Intent)
统一全部 9 个插件为 liantian_cn.插件名@dev；rotations.main 改成 phantom.main；给每个插件添加 AI Agent 阅读的 plugin.toml。自述覆盖配置参数、返回值、主要 API 名称、转换关系和中文简介。Agent 按业务含义生成中文名和推荐条件名；冷却使用“{技能名称}的冷却时间”，GDI 推荐条件名为“不适用”。

## 约束 (Constraints)
命名、数字正式版本接口参数与逻辑不可修改、自述编写均为软规则。dev、beta、1.0-beta 等测试版本可修改。加载器仅保留路径安全、精确查找和接口检查；Python 不读取自述。直接迁移并同步 blood-dk.toml、截图配置默认值和当前引用；历史档案保留原文。
Implement the plan.

## 被拒绝的替代方案 (Rejected Alternatives)
仅迁移条件插件；继续运行时强制命名格式；罗列内部全部变量；旧标识与旧入口过渡兼容；“冷却事件”用词；仅纯字母测试版本可变；GDI 省略推荐条件名字段。

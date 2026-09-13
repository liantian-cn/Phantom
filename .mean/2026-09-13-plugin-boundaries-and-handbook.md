---
plan: .plan/2026-09-13-plugin-boundaries-and-handbook.md
related_paths:
  - .plugin-development/README.md
  - .plugin-development/captures.md
  - .plugin-development/conditions.md
  - .prompt/2026-09-13-plugin-boundaries-and-handbook.md
  - .spec/README.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/plugin-system.md
  - .spec/testing.md
  - .spec/tui.md
  - AGENTS.md
  - demo/demo.py
  - demo/demo01.py
  - phantom/captures/__init__.py
  - phantom/captures/contracts.py
  - phantom/captures/gdi@1.0/capture.py
  - phantom/captures/imaging.py
  - phantom/captures/worker.py
  - phantom/conditions/__init__.py
  - phantom/conditions/base.py
  - phantom/conditions/player_health_pct@1.0/condition.py
  - phantom/conditions/player_health_pct@1.0/template.lua
  - phantom/conditions/player_primary_power@1.0/condition.py
  - phantom/conditions/player_primary_power@1.0/template.lua
  - phantom/conditions/registry.py
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
  - phantom/core/capture/__init__.py
  - phantom/core/capture/contracts.py
  - phantom/core/capture/imaging.py
  - phantom/core/capture/registry.py
  - phantom/core/capture/worker.py
  - phantom/core/condition/__init__.py
  - phantom/core/condition/base.py
  - phantom/core/condition/contracts.py
  - phantom/core/condition/decoders.py
  - phantom/core/condition/layout.py
  - phantom/core/condition/registry.py
  - phantom/core/condition/template.py
  - phantom/core/configuration.py
  - phantom/core/rotation.py
  - phantom/core/validation.py
  - phantom/ui/app.py
  - phantom/ui/capture.py
  - pyproject.toml
  - rotations/main.py
  - scripts/check_types.py
  - tests/test_capture.py
  - tests/test_capture_demo.py
  - tests/test_capture_registry.py
  - tests/test_conditions.py
  - tests/test_configuration.py
  - tests/test_decoders.py
  - tests/test_generator.py
  - tests/test_pixels.py
  - tests/test_ui.py
  - tests/test_validation.py
  - todo_list.md
---

## 意图 (Intent)

修正七项问题及同类问题：条件与截图核心归入 core，插件目录只保留插件；校验器与解码器各自基类、由插件组合；中文插件开发手册统一作者规则；补全准确业务注释；Lua 参数与业务常量集中声明；截图精确版本可配置且默认 GDI。Implement the plan.

## 约束 (Constraints)

保留八个 @1.0、参数、编解码与兜底语义；旧配置缺少后端字段时默认 GDI，不改写文件；不增加新后端或热切换；旧模块不保留。仅在 develop 修改，完成验证后一个原子本地提交，不推送。

## 被拒绝的替代方案 (Rejected Alternatives)

None

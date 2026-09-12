---
plan: .plan/2026-09-12-blood-dk-condition-generator.md
related_paths:
  - .context/README.md
  - .context/secret-values.md
  - .prompt/2026-09-12-blood-dk-condition-generator.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/pixel-protocol.md
  - .spec/plugin-system.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .spec/tui.md
  - AGENTS.md
  - phantom.toml
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
  - phantom/core/configuration.py
  - phantom/core/generator.py
  - phantom/core/pixels/cell.py
  - phantom/core/rotation.py
  - phantom/lua/addonTemplateName.toc
  - phantom/ui/app.py
  - phantom/ui/app.tcss
  - pyproject.toml
  - requirements-dev.txt
  - requirements.txt
  - rotations/blood-dk.toml
  - scripts/check_types.py
  - tests/lua/conditions_harness.lua
  - tests/test_conditions.py
  - tests/test_generator.py
  - tests/test_pixels.py
  - tests/test_rotation.py
  - tests/test_ui.py
  - todo_list.md
---

## 意图 (Intent)

完成第7–9步，初步实现第10步，不进游戏，通过实际生成目录验证。血DK职业/专精6/1；八个条件插件、可回写布局、TUI三列表格与生成按钮。修复实际生成包漏带字体的报错，携带共享运行时资源。Implement the plan.

## 约束 (Constraints)

公共冷却独立为spell_gcd@1.0，无参数，固定61304/false，不检查学会。宏名是“死神的抚摩”，重复规则为笔误。Idle为隐含保留动作。生成直接覆盖同名产物，旧文件保留且TOC不引用。每次加载/生成重新分配并仅在不同回写，保留注释。八插件采用已确认公式和兜底。纳入Cell.ratio已有改动，历史归档保持独立。Windows参考使用E:\Documents\GitHub\wow-ui-source并更新说明。

## 被拒绝的替代方案 (Rejected Alternatives)

用户选择直接覆盖，不采用产物清单清理或备份替换整个目录。公共冷却不作为spell_cooldown的特例，改为专用无参插件。

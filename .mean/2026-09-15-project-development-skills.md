---
plan: .plan/2026-09-15-project-development-skills.md
related_paths:
  - .agents/skills/phantom-code-dev/SKILL.md
  - .agents/skills/phantom-code-dev/agents/openai.yaml
  - .agents/skills/phantom-code-dev/references/architecture.md
  - .agents/skills/phantom-code-dev/references/development-rules.md
  - .agents/skills/phantom-code-dev/references/history/flexoki.md
  - .agents/skills/phantom-code-dev/references/history/performance-notes.md
  - .agents/skills/phantom-code-dev/references/history/verification-history.md
  - .agents/skills/phantom-code-dev/references/lua-development.md
  - .agents/skills/phantom-code-dev/references/pixel-protocol.md
  - .agents/skills/phantom-code-dev/references/project-overview.md
  - .agents/skills/phantom-code-dev/references/runtime-performance.md
  - .agents/skills/phantom-code-dev/references/testing.md
  - .agents/skills/phantom-code-dev/references/tui.md
  - .agents/skills/phantom-plugin-dev/SKILL.md
  - .agents/skills/phantom-plugin-dev/agents/openai.yaml
  - .agents/skills/phantom-plugin-dev/references/built-in-conditions.md
  - .agents/skills/phantom-plugin-dev/references/captures.md
  - .agents/skills/phantom-plugin-dev/references/common.md
  - .agents/skills/phantom-plugin-dev/references/conditions.md
  - .agents/skills/phantom-plugin-dev/references/history/version-migrations.md
  - .agents/skills/phantom-plugin-dev/references/keyboards.md
  - .agents/skills/phantom-rotation-dev/SKILL.md
  - .agents/skills/phantom-rotation-dev/agents/openai.yaml
  - .agents/skills/phantom-rotation-dev/references/configuration.md
  - .agents/skills/phantom-rotation-dev/references/key-syntax.md
  - .agents/skills/phantom-wow-api/SKILL.md
  - .agents/skills/phantom-wow-api/agents/openai.yaml
  - .agents/skills/phantom-wow-api/references/aura.md
  - .agents/skills/phantom-wow-api/references/events-performance.md
  - .agents/skills/phantom-wow-api/references/history/source-snapshots.md
  - .agents/skills/phantom-wow-api/references/rendering.md
  - .agents/skills/phantom-wow-api/references/secret-values.md
  - .agents/skills/phantom-wow-api/references/security-api.md
  - .agents/skills/phantom-wow-api/references/source-verification.md
  - .agents/skills/phantom-wow-api/references/wow-12.1-changes.md
  - .context/README.md
  - .context/aura.md
  - .context/events-performance.md
  - .context/flexoki.md
  - .context/rendering.md
  - .context/secret-values.md
  - .context/security-api.md
  - .context/wow-12.1-changes.md
  - .plugin-development/README.md
  - .plugin-development/captures.md
  - .plugin-development/conditions.md
  - .plugin-development/keyboards.md
  - .prompt/2026-09-15-project-development-skills.md
  - .spec/README.md
  - .spec/architecture.md
  - .spec/configuration.md
  - .spec/development-rules.md
  - .spec/pixel-protocol.md
  - .spec/plugin-system.md
  - .spec/project-overview.md
  - .spec/testing.md
  - .spec/tui.md
  - AGENTS.md
  - todo_list.md
---

## 意图 (Intent)

把项目的 agents.md 和相关文档整理成 skills：phantom-code-dev（项目代码开发）、phantom-plugin-dev（插件开发）、phantom-rotation-dev（循环开发）；额外需要由 Agent 判断补充。相关文件成为 references，根 AGENTS.md 大幅简化，减少未来提示词占用。Agent 补充 phantom-wow-api，集中共享 WoW 核验资料。

## 约束 (Constraints)

选择项目内 .agents/skills/；迁移并精简、合并重复规则、分离历史记录、保留有效约束及来源、移除旧入口并修复当前引用。循环开发负责配置和战斗优先级，新插件和引擎改动归对应 skill。Implement the plan.

## 被拒绝的替代方案 (Rejected Alternatives)

None

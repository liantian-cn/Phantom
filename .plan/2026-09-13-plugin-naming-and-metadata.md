# Plugin naming, metadata, and entry point migration

## Goal
Unify nine plugin identifiers, document plugins for AI agents, and move the application entry point to phantom.main without changing plugin business behavior.

## Scope
Eight condition plugins and one GDI capture plugin; registries, configuration, demos, tests, current documentation and author rules. Preserve historical task archives and verification records. No action plugin, game installation, push or publication.

## Decisions
- Identifiers use author.package@version; author components follow Python package naming. This repository uses liantian_cn.
- Rename all nine existing plugins to liantian_cn.<existing_name>@dev.
- Numeric and dot-separated numeric versions are immutable in interface parameters and logic; changes require another version. Test labels including dev, beta and 1.0-beta permit changes.
- Naming, version immutability and plugin.toml authoring are agent rules only. Remove registry naming regexes; retain exact lookup, path containment and interface validation.
- Do not preserve old identifier aliases or rotations.main forwarding.
- Add nine plugin.toml files for agents; runtime Python never reads them.
- Document parameters and business returns, not all internal variables. Use Chinese explanations and English TOML keys.
- Agent generates Chinese display names and suggested condition names. Cooldown suggestion is {技能名称}的冷却时间. GDI suggestion is 不适用.
- Metadata uses name, display_name, description, recommended_condition_name, parameters and returns. Include API names, conversion, types, units and fallback without API tutorials.
- Preserve blood DK condition titles, expressions, layout and plugin business contracts.

## Implementation Steps
1. Rename plugin directories and active references; update defaults, blood-dk.toml, demos and author/system documentation without rewriting historical records.
2. Remove registry format restrictions while rejecting absolute paths, traversal and source/template escape.
3. Move rotations/main.py to phantom/main.py and update imports and current startup instructions.
4. Read implementation and pinned reference APIs; write all nine metadata documents and record reference version/revision.
5. Run behavioral regressions and required checks, review the diff and commit task files atomically with archives.

## Acceptance Criteria
All nine new identifiers load, default GDI is liantian_cn.gdi@dev, blood DK generation/evaluation remains equivalent, phantom.main preserves startup and cleanup. No old aliases. Missing metadata does not prevent loading. Path containment and plugin interfaces remain enforced.

## Verification
- Final full pytest: 322 passed, 5 skipped in 13.42 seconds on Windows / Python 3.13.15.
- Five real symlink tests skipped because Windows returned WinError 1314 (no symlink creation privilege). Five independent resolved-path tests passed without link privileges; these validate containment branches, not actual symlink creation.
- scripts/check_types.py: strict checks passed for 51 ordinary source files and all nine version plugin entry points.
- Ruff check and format --check passed for all 60 Python files. git diff --check passed.
- All nine plugin.toml files parsed successfully and names match directories; contents reviewed against implementation, parameters, return contracts and source references. No runtime reader or persistent metadata validation added.
- AST comparison, ignoring docstrings, confirmed unchanged Python business implementation in all nine plugins. All eight Lua bodies after namespace initialization are identical to their previous versions.
- Configuration/generator/Lua pairing/TUI regressions passed. Active references migrated; old directories and entry absent. Remaining old identifiers occur only in history or deliberate test fixtures.
- WoW read-only evidence checked on 2026-09-13: E:/Documents/GitHub/wow-ui-source, version.txt 12.1.0.69587, revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58; generated API definitions for unit, spell, spellbook, rune, overlay, curve and duration APIs. No game installation or game/API behavioral claims from this offline check.

## Review Notes
- Frozen: 2026-09-13 12:18:42 UTC. Confirmation source: user "Implement the plan." through the native Plan-to-implementation flow; environment is Default mode.
- Confirmed decisions: all nine plugins, safety-only identifier checks, parameters/returns documentation, no compatibility aliases, 冷却时间 wording, numeric releases versus test labels, GDI recommendation 不适用.
- Agent-delegated naming: Chinese display and recommended condition names are selected from existing business semantics.
- Archive collision check passed before creation; working tree clean on develop. Frozen sections are Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria.

- Final review: requirements R1-R8 mapped to implementation and verification. The example-only health plugin in the schema documentation is explicitly labeled hypothetical; no target-health plugin was added. Chinese plugin display names and recommendations describe existing business outputs.

## Completion
Implementation and verification complete. All task implementation and three archives are prepared for one atomic local commit on develop, titled "Unify plugin names and metadata and move Phantom entry point". No unrelated pre-existing changes, push, publication, game installation or reference-repository mutation.

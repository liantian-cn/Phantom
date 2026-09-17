# Project Development Skills

## Goal

Replace Phantom's mandatory documentation entrypoints with four focused, progressively disclosed project skills and substantially shorten the root AGENTS.md.

## Scope

Create repository skills under .agents/skills; migrate and simplify .spec, .plugin-development and .context into skill references. Repair current document links including todo_list.md. Preserve historical task archives. Do not change business code, plugin interfaces, rotations, personal skills or global instructions.

## Decisions

- User selected repository-local skills, migration with simplification and separated history, and rotation authoring rather than engine development.
- phantom-code-dev owns core Python/Lua, TUI, pixels, generators, evaluators and runtime implementation; its references own shared development and testing rules.
- phantom-plugin-dev owns condition, capture and keyboard plugin authoring and contracts. Merge per-type contracts with author requirements, keep common rules and the built-in condition catalog separate.
- phantom-rotation-dev owns TOML, condition composition, macros, key syntax, combat priorities and offline validation. New plugin or engine work routes to the appropriate skill without implicit scope expansion.
- The user delegated additional skill selection. Add phantom-wow-api for shared WoW API, Secret Values, Aura, rendering, events and source verification; this avoids repeating technical references in multiple development skills.
- Keep implicit invocation enabled and provide concise Chinese descriptions and agents/openai.yaml. Project normative references remain Chinese; WoW technical references remain English.
- Keep shared rules in one reference and link directly to relevant sections across the co-located skills; do not require loading entire other skills for shared rules.
- Move Flexoki, historical test results and source snapshots to references/history, outside normal task reading paths. Preserve dates, sources, unresolved items and effective constraints.
- Remove old documentation entrypoints after migration. Existing historical archives retain their contents and original paths; record the migration map here for traceability.
- Root AGENTS.md retains branch limits, external-source read-only boundaries, authority order, unresolved-item handling and four skill routes, approximately 15 lines and at least 50 percent fewer characters.

## Implementation Steps

1. Record a complete source-to-reference migration map, including merges and historical destinations.
2. Create four concise SKILL.md entrypoints and UI metadata with task-specific source and reference routes.
3. Migrate, merge duplicates and separate history; resolve stale descriptions only where current explicit specifications and source establish the answer, otherwise preserve the uncertainty.
4. Shorten root AGENTS.md and repair maintained links and anchors, including todo_list.md.
5. Validate skill metadata, links, migration coverage, routing scenarios, root size reduction and absence of business changes.
6. Commit all migration files and the three workflow archives in one atomic local commit; do not push.

## Acceptance Criteria

- All four skills have exact names, discoverable locations and no scaffold placeholders.
- Every source document has an explicit destination; effective contracts and safety boundaries are preserved.
- TUI, plugin and rotation tasks load only relevant references; WoW references are conditional.
- Root AGENTS.md is at least 50 percent shorter by Unicode character count; report character counts rather than claimed token savings.
- Maintained documents have no stale migration links or duplicate normative copies.

## Verification

Run skill-creator quick_validate.py for all four skills. Validate YAML, relative links, anchors and old path references. Audit source-to-reference coverage. Walk through TUI, condition plugin, blood-DK rotation and secret aura API scenarios. Rotation offline validation must use a temporary copy because load_rotation may rewrite layout. Run git diff --check and verify no business implementation changes. No game startup, key sending or business regression suite is required for this documentation-only change.

### Results

- All four skills passed the bundled quick_validate.py; all four openai.yaml files parsed and retained default implicit invocation.
- Checked 33 maintained Markdown files: local targets, heading anchors, reference reachability and 22 original-file mappings passed. All 27 reference files are reachable; old entrypoints were removed only after verifying unchanged source contents and migration destinations.
- Root AGENTS.md: 850 to 387 Unicode characters (54.5 percent reduction), 10 lines. This is a character comparison, not an estimate of model tokens or total conversation context.
- Walked the TUI case (pure-black theme adjustment): code skill routes to TUI, development and testing references; no WoW or historical palette is required.
- Walked the condition case (change refresh cadence): plugin skill routes to common, conditions, Lua and pixel rules as applicable; 1-second fallback / 0.1-second continuous polling, next-frame callbacks, same-frame decoder and exact versions remain documented. Capture and keyboard references are not required.
- Walked the blood-DK priority case: rotation skill routes to configuration, key syntax and only relevant built-in condition metadata. Actually loaded a temporary copy of rotations/blood-dk.toml, rendered in memory and compiled all 16 generated Lua files using lupa.lua51. The original TOML SHA-256 was unchanged; no runtime was started, output installed or game keys sent.
- Walked the secret-aura case: WoW skill routes to source verification, Secret Values and Aura, with rendering/security only as needed. The skill preserves source revision requirements and the unverified boundary when the historical checkout is absent.
- Compared original substantive paragraphs with the migrated references and reviewed changed passages. Consolidated repeated method/zero-region rules and preserved current GDI ctypes.WinDLL and user-designated macro-example requirements. Dates and source evidence were not represented as fresh checks.
- The skill validator required PyYAML, unavailable in the project venv. Installed it only into ignored .cache/skill-migration/deps and used PYTHONPATH for the tooling; project dependencies and implementation files were not modified.
- git diff --check and git diff --cached --check passed. The staged scope exactly matches 61 affected documentation, metadata and task-archive paths (counting both sides of moves); no implementation, project dependency, rotation or pre-existing archive changed.

## Review Notes

- Confirmed at 2026-09-15T10:25:48.570625+08:00; source: user message "Implement the plan." following the proposed plan and transition to Default mode. Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
- Archive collision checks passed. Working tree was clean on develop; baseline commit c816caf contains the prior condition refresh task.
- Plan-mode restrictions prevented draft filesystem writes; all three archives are created after explicit implementation authorization.

### Documentation migration map

| Original | Destination(s) |
| --- | --- |
| `.spec/architecture.md` | `.agents/skills/phantom-code-dev/references/architecture.md` |
| `.spec/configuration.md` | `.agents/skills/phantom-rotation-dev/references/configuration.md` |
| `.spec/development-rules.md` | `.agents/skills/phantom-code-dev/references/development-rules.md`; `.agents/skills/phantom-code-dev/references/lua-development.md`; `.agents/skills/phantom-wow-api/references/source-verification.md`; `.agents/skills/phantom-wow-api/references/history/source-snapshots.md` |
| `.spec/pixel-protocol.md` | `.agents/skills/phantom-code-dev/references/pixel-protocol.md` |
| `.spec/plugin-system.md` | `.agents/skills/phantom-plugin-dev/references/history/version-migrations.md`; `.agents/skills/phantom-plugin-dev/references/common.md`; `.agents/skills/phantom-plugin-dev/references/conditions.md`; `.agents/skills/phantom-plugin-dev/references/built-in-conditions.md`; `.agents/skills/phantom-plugin-dev/references/captures.md`; `.agents/skills/phantom-plugin-dev/references/keyboards.md` |
| `.spec/project-overview.md` | `.agents/skills/phantom-code-dev/references/project-overview.md` |
| `.spec/README.md` | `AGENTS.md` |
| `.spec/testing.md` | `.agents/skills/phantom-code-dev/references/history/verification-history.md`; `.agents/skills/phantom-code-dev/references/testing.md` |
| `.spec/tui.md` | `.agents/skills/phantom-code-dev/references/tui.md` |
| `.plugin-development/captures.md` | `.agents/skills/phantom-plugin-dev/references/captures.md` |
| `.plugin-development/conditions.md` | `.agents/skills/phantom-plugin-dev/references/conditions.md` |
| `.plugin-development/keyboards.md` | `.agents/skills/phantom-rotation-dev/references/key-syntax.md`; `.agents/skills/phantom-plugin-dev/references/keyboards.md` |
| `.plugin-development/README.md` | `.agents/skills/phantom-plugin-dev/references/history/version-migrations.md`; `.agents/skills/phantom-plugin-dev/references/common.md`; `AGENTS.md` |
| `.context/aura.md` | `.agents/skills/phantom-wow-api/references/aura.md` |
| `.context/events-performance.md` | `.agents/skills/phantom-wow-api/references/events-performance.md`; `.agents/skills/phantom-code-dev/references/runtime-performance.md`; `.agents/skills/phantom-code-dev/references/history/performance-notes.md` |
| `.context/flexoki.md` | `.agents/skills/phantom-code-dev/references/history/flexoki.md` |
| `.context/README.md` | `.agents/skills/phantom-wow-api/references/source-verification.md`; `.agents/skills/phantom-wow-api/references/history/source-snapshots.md`; `AGENTS.md` |
| `.context/rendering.md` | `.agents/skills/phantom-wow-api/references/rendering.md` |
| `.context/secret-values.md` | `.agents/skills/phantom-wow-api/references/history/source-snapshots.md`; `.agents/skills/phantom-wow-api/references/secret-values.md` |
| `.context/security-api.md` | `.agents/skills/phantom-wow-api/references/source-verification.md`; `.agents/skills/phantom-wow-api/references/history/source-snapshots.md`; `.agents/skills/phantom-wow-api/references/security-api.md` |
| `.context/wow-12.1-changes.md` | `.agents/skills/phantom-wow-api/references/wow-12.1-changes.md` |
| `AGENTS.md` | `AGENTS.md` |

- Navigation-only README tables were folded into skill entrypoints. Repeated authority/language rules moved to root routing and shared development rules. No unresolved product decisions were implemented.
- Stale overview theme and trial-button statements now follow the existing TUI specification and source. Pixel OutputType now lists the already implemented none variant. Macro example field names now follow the existing schema; no runtime code changed.
- Earlier performance frequency uncertainty is retained in history; current architecture already establishes new-frame processing. Historical test and source records retain their original dates and limitations.

## Completion

Four repository skills, 27 references, simplified root routing and repaired current links are implemented and verified. This documentation-only migration does not constitute business-code or game validation. This archive is included with all changes in the atomic completion commit, together with the intent and requirements records. No push is authorized or performed.

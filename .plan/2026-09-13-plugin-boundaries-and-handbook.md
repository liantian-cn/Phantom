# Plugin boundaries and development handbook

## Goal

Correct the seven requested issues and analogous existing issues, separating plugin business rules from core facilities while preserving current behavior.

## Scope

Eight condition plugins, condition and capture core, GDI loading, configuration, generator, UI, demos, tests and documentation. No new business plugins, capture backends, runtime backend switching, actions, external repository edits or game installation writes.

## Decisions

- Move condition infrastructure to phantom/core/condition; separate lifecycle, contracts, layout and template rendering. Version directories contain plugins only.
- Separate generic Validator[T].validate(value, name) and Decoder[Input, Output].decode(value) abstract bases; use composition. Generic validation is independent of condition base.py. Spell argument rules, cooldown nodes, rune ranges, charge formulas and fallbacks belong to their plugins. No cross-version plugin imports.
- Reuse validators for equivalent application and rotation primitive checks; keep AST, references and security rules in their owning modules.
- Move capture contracts, worker, imaging and registry to phantom/core/capture. capture.plugin defaults to gdi@1.0 and is loaded exactly at startup. Plugins export Plugin accepting fps and satisfying the worker contract. Fail clearly before UI on invalid selection/import/interface; no fallback except absent configuration defaults. Existing config files are not rewritten. Demos explicitly select GDI via the registry without reading application config.
- Keep eight @1.0 identifiers, parameters, output, decoding and fallbacks. Update all internal imports without old-module forwarding.
- Centralize Lua instance parameters and business constants at the beginning of logical code; inject xN/yN/widthN from frozen regions. Preserve event, polling, random staggering and initialization timing. Local temporary variables remain local.
- Add accurate Chinese business comments, correct copied cooldown and fixed example descriptions, preserve known API verification history.
- Chinese .plugin-development/README.md owns author rules with condition/capture topics; .spec retains system contracts and links; AGENTS.md routes. Update roadmap step 16 partial completion without claiming continuous-loop validation.

## Implementation Steps

1. Split and relocate core facilities; update consumers and complete plugin type checks.
2. Introduce validator/decoder objects and compose them in eight plugins, preserving errors and fallback behavior.
3. Add configurable exact capture loading and startup errors; migrate demos.
4. Normalize Lua constants and layout injection; explain Python business flow and correct stale comments.
5. Establish handbook and synchronize routing, architecture, configuration and roadmap.

## Acceptance Criteria

New plugins require no core changes. Core contains no spell_ids/cooldown business rule. No old imports or UI-specific GDI loader remains. Existing values/layout/fallbacks are unchanged. Lua uses frozen layout through header declarations. Default/explicit capture selection and invalid paths work. Documentation has one source for each rule.

## Verification

Run full pytest, scripts/check_types.py, Ruff check and format check. Cover primitive validation, plugin boundaries, layout/multiple regions, gray/boolean/charges/cooldown/fallback, Lua 5.1 execution and Python roundtrips, capture loading/errors/config preservation, worker lifecycle and TUI regressions. Run bounded Windows GDI smoke separately from game acceptance. Record actual outcomes below.

- 2026-09-13: Full pytest completed with 228 passed; original 160 regressions also passed before adding task-specific coverage.
- scripts/check_types.py passed core (47 source files), eight condition entries and one capture entry under mypy strict. Ruff check and format --check passed (56 files).
- New tests verify validators, generic interpolation, exact capture selection, missing/broken plugins, UI factory wiring and startup rejection without config rewrite, nondefault Lua x/y/width and cooldown curve roundtrips across all segments.
- Windows smoke: default Registry created GDIWorker at 5 FPS; two start/stop cycles reported no non-DEBUG board found, with no phantom- threads left afterward. No game board image or game acceptance was obtained.
- Markdown relative targets, plugin-only top-level directories, old-import absence and git diff --check passed.

## Review Notes

- 2026-09-13 02:23:13 UTC: Frozen after native Plan-to-implementation confirmation; source: user "Implement the plan." and environment transition to Default mode. All six interview choices incorporated; no unresolved decisions.
- Archive paths checked before creation: no collisions. Working tree is now clean on develop (ahead 2); the previously observed unrelated archive edits have already been committed outside this task.

- Implementation follows the frozen decisions. Cooldown plugin nodes are serialized into Lua by that same version to keep the encoding pair aligned.
- The previously archived WoW API evidence was retained. Read-only reference HEAD remains a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58; this task makes no new API availability or game-rendering claims.
- All initial requirements and six selected answers map to prompt R1–R10; implementation authorization maps to R11. Mean related_paths was resolved to exact changed/new/deleted paths before staging.

## Completion

After successful verification, make one atomic local commit containing implementation and matching archives; exclude unrelated changes. No push or publication. Record verification limitations and actual completion below.

2026-09-13: Implementation and verification complete. Implementation and matching archives are delivered together in this single atomic local commit. No external repository, game installation, push or publication was modified/performed. Game acceptance and continuous-loop validation remain outside this task.

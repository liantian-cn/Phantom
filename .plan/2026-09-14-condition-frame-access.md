# Condition Frame Access and Optional Lua

## Goal

Expose the current frame’s `PixelDecoder` to condition plugins and replace the three built-in rotation variables with explicitly configured plugins.

## Scope

- Retain existing Lua state, commands, panel, and all five first-row Cells.
- Change Python condition contracts, loading, layout, rotation evaluation, configuration, tests, and relevant documentation.
- Reduce the TUI general-condition page to class and specialization.

## Decisions

- Extend `value` and `decode_value` with a required keyword-only `decoder: PixelDecoder`, retaining the three region lists. Migrate all existing `@dev` plugins and callers without an old-signature compatibility layer.
- Pass the same decoder used for that frame’s rotation evaluation. Plugins may read any valid Cell, ValueBar, or IconTile by existing decoder coordinates; they must not mutate the frame or retain it for later evaluation.
- Add `output_type="none"` with `output_count=0`, no widths, and empty regions. Preserve existing positive-count rules for pixel-producing output types. Track layout freezing explicitly so empty layouts remain valid and cannot be frozen twice.
- Make `template.lua` optional. Absence produces an empty instance `do/end` block. Lua presence and pixel allocation are independent capabilities; existing path-boundary checks remain.
- Add three parameterless plugins:
  - `liantian_cn.enable@dev`: Cell `(3,1)`, fallback `True`.
  - `liantian_cn.in_burst@dev`: Cell `(4,1)`, fallback `False`.
  - `liantian_cn.delaying@dev`: Cell `(5,1)`, fallback `False`.
- These plugins allocate no regions and contain no Lua. They use strict black/white decoding; invalid input returns the specified fallback.
- Explicitly allocated region bounds errors still fail the frame. Additional reads inside plugin decoding use the normal plugin exception/fallback boundary.
- Configuration `title` supplies the expression name, subject to existing identifier and uniqueness rules. Remove built-in names, reserved-name restrictions, and implicit general-value injection.
- Retain schema version 1. Old implicit references require explicit condition declarations; no automatic migration.

## Implementation Steps

1. Update system and plugin-author specifications to document the confirmed contracts.
2. Implement decoder forwarding, empty-output lifecycle, optional templates, and corresponding layout metadata.
3. Add the three plugins and their `plugin.toml` descriptions, including fallback semantics.
4. Simplify rotation decisions to configured condition values; preserve class/specification validation and new-frame execution behavior.
5. Add explicit enable and delay conditions to the repository rotation, retaining its expression text and existing pixel positions. Load burst only when declared.
6. Reduce general-condition UI decoding and presentation to two rows. Configured state plugins appear in the normal condition table under their titles.
7. Update affected demos, tests, and documentation.

## Acceptance Criteria

- A plugin can combine allocated inputs with arbitrary same-frame decoder reads.
- A Python-only condition loads, evaluates, and generates without allocating pixels.
- All three state plugins can be renamed, omitted, or instantiated under distinct titles.
- Invalid state pixels return exactly the confirmed fallbacks and evaluation continues.
- Unknown undeclared expression names fail configuration loading.
- Existing eight plugins preserve their business outputs.
- Lua controls and first-row pixel layout retain their current behavior.

## Verification

- Test decoder identity across instances and frames, all three region access methods, additional-read failures, and allocated-region bounds errors.
- Test optional/empty templates, zero-region freezing, mixed layouts, and plugin path protections.
- Test renamed and omitted state conditions, fallback-driven decisions, explicit configuration migration, and class/specification rejection.
- Verify the two-row TUI and configured condition values.
- Run pytest, strict type checks, Ruff checks, formatting checks, and generated Lua syntax checks. Use temporary outputs and mocked keyboard sending.

## Review Notes

Implementation starts only after native Plan confirmation and departure from Plan mode. Then create and freeze the English plan, record confirmation, and create matching mean and prompt archives named `2026-09-14-condition-frame-access.md`.

The user explicitly selected permissive enable/delay fallbacks; invalid state reads can therefore allow actions according to configured rules.

- 2026-09-14T15:55:02+08:00: Frozen after the user's native-flow confirmation, “Implement the plan.” Environment is in Default mode. Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria are frozen. Archive collision check passed; none of the three archive paths is Git-ignored. No files were written during Plan mode.
- Implementation review: the existing allocator already handles zero iterations without shifting pixel positions, and the generator already wraps every instance in do/end. No changes to those files were necessary. Demo callers use Rotation and inherit its migrated interface; the standalone raw-pixel demo retains its existing diagnostic output.
- Verification found the TUI refresh loop still hard-coded five rows; it now follows GENERAL_FIELDS, matching table creation. Initial UI regression failures and a test-only column-key mistake were corrected before the complete passing run. A final formatter check corrected mixed line endings in the localized UI edit.

## Completion

Record verification results and limitations, then create one atomic local commit on `develop` containing task changes and required archives under the repository workflow. Do not push or install generated game files.

- Implementation and documentation complete on develop. Required atomic local commit includes these archives and only task changes; initial working tree was clean.
- Final verification: 386 pytest tests passed, 5 skipped because Windows cannot create symlinks (WinError 1314). Strict typing passed for 58 common source files and all 13 version entrypoints (11 conditions, capture, keyboard). Ruff check passed; all 71 Python files passed format --check. Generated Lua 5.1 syntax/execution and original plugin roundtrips passed within pytest.
- No generated game installation, external-source modification, push, or game-key delivery occurred. Real game acceptance remains unperformed; full-suite Windows message checks used a test-owned hidden window.

# Goal

Complete roadmap steps 7–9 and the offline portion of step 10 with the supplied Blood DK rotation, eight condition plugins, layout persistence, Lua generation and TUI condition values.

# Scope

Implement configuration validation, exact plugin loading, frozen multi-output layouts, eight Python/Lua plugin pairs, a single-rotation generator and TUI integration. Include the existing Cell decimal-to-ratio change and its tests/specification. Preserve examples but remove TOC references. No expression execution, scheduler, macro binding, key sending, multi-rotation management or in-game testing.

# Decisions

- Example: rotations/blood-dk.toml, UUID 550e8400-e29b-41d4-a716-446655440000, title 血DK循环, description 测试使用。, DEATHKNIGHT/6/1. Class ID is optional but must agree when supplied. Correct the macro reference to 死神的抚摩 and remove the accidental duplicate overflow rule. Preserve the four macros and remaining rule order/parameters. TOML comments use #.
- Idle is reserved, requires no macro, and cannot be a user macro name. Empty conditions are allowed only for a final explicit Idle. Missing fallback is appended in memory only. Validate schema, types, UUID, names/references, plugins and arguments, expression syntax and referenced condition names; full expression whitelist/type checking and execution remain step 11.
- Each exact-version directory has condition.py and template.lua. Independently validate arguments and declare output_type/count, value_type/shape and per-bar widths. Freeze immutable positions/counts before generation. raw_value(decoder) extracts three lists; value(cells, value_bars, icon_tiles) invokes decode_value with the same lists and falls back on exceptions or wrong result types. Unused lists are empty; multiple outputs of one type are supported.
- Independently pack each output row in configuration order, including ValueBar separators. Persist each condition's layout table with output type and regions (x, applicable y/width). Recompute on startup and generation; save only when different and preserve comments/other content. Example: seven Cells at x=1..7, y=2, one ValueBar x=1,width=2, no IconTiles; board 36x20.
- Plugins @1.0: player_primary_power (Cell ratio*max_power, positive max_power, float fallback 0); spec_dk_rune (Cell mean rounded half up, 0..6, no args, fallback 0); spell_charges (ValueBar width=max_charges, spell_ids and positive integer max_charges, ratio*max_charges rounded half up, fallback 0); spell_overlay and spell_usable (Cell bool, spell_ids, fallback False); player_health_pct (Cell percent, predicted health as example, no args, fallback 0); spell_cooldown (Cell seconds, spell_ids and ignore_gcd, fallback 375); spell_gcd (Cell seconds, no args, fixed GetSpellCooldownDuration(61304,false), no spellbook filtering, fallback 375).
- Both cooldowns invert brightness 255/155/105/55/0 at 0/5/30/155/375 seconds, linearly within segments. Missing duration is black. Black also represents saturation/unavailability. Regular spells choose first spellbook candidate; spell_cooldown has no GCD special case. Grayscale inputs must be pure gray; booleans strict black/white. Rune callbacks ignore secret payloads. Other API/update behavior follows examples; cooldowns use independent randomized 0.1-second polling. Naming prefixes are suggestions only.
- App config: rotation.path, wow.executable, addon.name (default Phantom). Relative rotation paths resolve against config directory; absent rotation retains basic capture; absent executable disables generation. Repository config uses the supplied retail Wow.exe path and example.
- TUI generation reloads rotation, validates, allocates and renders in a background worker. Disable during capture/stop/generation. Derive output from executable parent/Interface/AddOns/name without requiring a running game. Generate runtime, general, UUID Lua and matching TOC. UUID Lua guards class/spec first, each instance uses local scope. Generate all declared conditions. Render before writing; overwrite same-name output, retain stale files, TOC lists only current files.
- Conditions page columns: condition name, plugin name, value; use the same valid frame, require matching class/spec. Clear on pause/capture failure/layout error/mismatch; show plugin fallback for decoding errors. Log generation outcomes/errors, not per-frame values.
- Windows reference is E:/Documents/GitHub/wow-ui-source, read-only. Update instructions while retaining historical evidence. Include existing Cell ratio change; exclude existing historical numpy plan/prompt edits.

# Implementation Steps

1. Freeze archives after authorization; update minimal relevant specifications and Windows reference routing.
2. Implement rotation schema, plugin contracts/discovery, layout persistence and corrected example.
3. Implement eight documented Python/Lua pairs with verified API and secret-value boundaries.
4. Implement generator, TOC changes, application settings and TUI integration.
5. Verify configuration, layouts, decoding, generated Lua and TUI; generate and inspect actual AddOns output; update roadmap.
6. Commit task implementation, mean and unignored plan/prompt atomically on develop, excluding unrelated historical edits.

# Acceptance Criteria

- Valid example loads, persists positions and generates; invalid schema/references/parameters/versions fail clearly.
- Frozen multi-output independent layouts include separators. Eight plugins meet normal/boundary/fallback contracts.
- GCD always queries 61304,false without spellbook filtering and accepts no arguments.
- Actual TOC references existing current files only, excludes examples/stale UUID Lua, and templates contain no unresolved tokens.
- TUI generates without game running and displays eight conditions using matching valid frames.
- Steps 7–9 pass offline checks; step 10 remains partial pending game loading and real round-trip verification.

# Verification

Planned: pytest (schema/UUID/duplicates/references/class consistency/Idle/arguments/versions; multi-region and separator layouts; comment-preserving idempotent writeback; complete synthetic frames, half-up rounding, cooldown segments, invalid inputs; GCD query behavior and Lua syntax; TUI generation/errors/lifecycle/same-frame/mismatch), mypy strict, Ruff check and format check, actual AddOns directory inspection. No game launch or keys.

- 2026-09-12: pytest: 160 passed; scripts/check_types.py: strict checks passed for 39 ordinary files and all eight condition.py versions; Ruff check and format --check passed (47 Python files).
- Lua 5.1 compiled every generated file. Real generated condition code ran against API doubles, produced a synthetic 36x20 frame, and decoded to [40.0,3,1,True,2.5,0.0,40.0,True]. GCD skips spellbook and queries 61304,false; missing duration black; normal spells retain filtering. Multi-output layouts, separators, half-up rounding, idempotent comment-preserving TOML, invalid inputs, TUI errors/retry/exit verified.
- Actual output verified: E:/World of Warcraft/_retail_/Interface/AddOns/Phantom, 17 files, 16 TOC Lua references, no examples or unresolved template tokens. Game was not launched.

# Review Notes

- Frozen: 2026-09-12T21:03:17+08:00. Confirmation source: user “Implement the plan.” after the revised proposed plan; environment switched to Default mode. Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
- User revision before confirmation: replaced the planned cooldown 61304 exception with the independent parameterless spell_gcd@1.0. User explicitly rejected cleanup/backup of old generated files: overwrite current outputs and keep stale files unreferenced.
- Reference checked: a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58, version 12.1.0.69587. Plan/mean/prompt filename collision checks passed. Mean is not ignored.
- Existing unrelated changes: .plan/2026-09-12-numpy-pixel-decoder.md and matching .prompt file. Existing phantom/core/pixels/cell.py ratio change is explicitly included.

- User interruption during final verification: reported FontString:SetFont missing media/UiFont.ttf in generated runtime/06_panel.lua. This exposed an implementation defect in packaging existing runtime dependencies, not a new behavior decision. Generator now includes all six existing media assets; required UiFont.ttf and aura_border_32_4px.tga must exist before writes. No frozen requirement changed.
- Corrected actual output: 23 files (17 text + 6 media), 16 Lua TOC references. UI font (10,753,020 bytes) and border texture match source bytes. Font SHA-256 acf1201a690012d58c4085cbae17bf1d5245c7a064b78ec40a88f58e0dc81d25. Re-generated actual AddOns directory. Targeted regression: 43 passed; all strict typing/Ruff checks passed again. Agent did not launch the game; user-reported loading failure is recorded, no successful game load claimed.

# Completion

Completed the authorized offline implementation and verification. Roadmap steps 7–9 marked complete; step 10 remains partial pending in-game loading/rendering, and step 13 records condition-table progress only. The workflow commit contains the task implementation and all three archives; unrelated historical plan/prompt changes remain unstaged. Final post-fix suite: 160 passed, strict typing and Ruff passed. No push or game verification.

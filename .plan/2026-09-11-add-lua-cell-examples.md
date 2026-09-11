# Add five Lua Cell examples

## Goal

Populate row 2, columns 1–5 with five independent Lua examples for subsequent plugin and decoding development.

## Scope

Create phantom/lua/examples/01_spell_cooldown.lua, 02_spell_overlay.lua, 03_spell_usable.lua, 04_player_buff.lua, and 05_player_health.lua. Append them to phantom/lua/addonTemplateName.toc after general files. Reuse existing Cell:setCell, colors, sizes, frame levels, and aura texture. Do not implement Python decoding or plugins or include unrelated existing changes.

## Decisions

- Use normal Cell instances, UIInitFuncs initialization, shared scaling, counters, and background resizing. RotationsCell and spell names are comments only. Put uppercase local parameters first in the logical-code section. Use the existing general file structure, Chinese business comments, original path, index, and literal {{uuid}} metadata.
- Cooldown: Dark Command / 黑暗命令, SPELL_IDS={56221,56222}, position (1,2), IGNORE_GCD=true. Use a Linear color curve with seconds 0/5/30/155/375 mapped to gray 255/155/105/55/0, divided by 255. Missing duration or no selected spell renders black.
- Overlay: Death and Decay / 枯萎凋零, SPELL_IDS={43264,43265}, position (2,2). White when overlayed, otherwise black.
- Usability: Death Strike / 灵界打击, SPELL_IDS={50000,49998}, position (3,2). White for isUsable, otherwise black; insufficientPower does not change the mapping.
- The first three examples select the first ID for which IsSpellInSpellBook returns true; reselect on SPELLS_CHANGED. No matches means black. Document that spellbook membership may include talent override spells rather than claiming strict learned-state equivalence.
- Cooldown and usability each use their own eventFrame and fastTimeElapsed=-random(). Keep initial black, add elapsed, and only when strictly greater than 0.1 subtract one interval and refresh once per frame, retaining the remainder. SPELLS_CHANGED reselects only; the next poll refreshes color.
- Overlay refreshes immediately after construction and on SPELLS_CHANGED and both SPELL_ACTIVATION_OVERLAY_GLOW_SHOW/HIDE events. Ignore event payloads and query the selected ID directly.
- Buff: Death and Decay / 枯萎凋零, SPELL_IDS={188298,188290}, position (4,2). Black Cell under a player HELPFUL AuraContainer slot with includeSpellIDs map and key {{uuid}}. Any matching buff displays a full white overlay. The container fills cell.Frame using SetAllPoints; initializeFrame statically sets button size, anchor, layer, and existing aura_border_full.tga texture. No custom refresh frame, aura enumeration, or visibility inspection.
- Health: position (5,2), USE_PREDICTED=true (使用预测生命值). Local Linear curve maps 0 to black and 1 to white; UnitHealthPercent("player", USE_PREDICTED, healthCurve) feeds Cell:setCell directly. Refresh immediately after construction and on player-only UNIT_HEALTH/UNIT_MAXHEALTH.
- Guard unconstructed Cells. Pass potentially secret booleans to EvaluateColorFromBoolean and duration/health results directly to color consumers; do not branch on combat values.
- API comments include purpose, signature, parameters, returns, restrictions, source links, verification date and pinned source revision. Wiki fetches returned 403; use user-supplied excerpts and local source without claiming a successful latest-page fetch.

## Implementation Steps

1. Freeze this plan after user authorization and create matching mean and prompt archives.
2. Create five independent examples following the decisions above; keep reusable future inputs local and uppercase.
3. Append the five files in order to the TOC. Do not alter runtime helpers or other existing work.
4. Run Lua syntax checks and a temporary behavior harness; inspect source contracts, texture coverage, and TOC order.
5. Record validation and game-only limitations, review the task-only diff, and make one atomic local commit with the five examples, TOC, and all three archives.

## Acceptance Criteria

- Five Cells occupy row 2 columns 1–5 without changing general row behavior.
- Candidate selection, reselection, black/white output, cooldown interpolation and missing-duration behavior follow confirmed decisions.
- Aura fills the whole Cell and leaves the black base when absent; health endpoints are black and white.
- Parameters are easy to replace and UUID placeholders are literal. No unsupported secret-value inspection or custom aura refresh is introduced.

## Verification

- Planned: luac -p for all five examples; verify TOC paths and order.
- Planned: temporary Lua harness for first-match selection/reselection, missing duration, direct color handoff, initialization guards, random staggering, residual elapsed time and at-most-once-per-frame polling.
- Planned: static Aura setup/filter/size review and player health event checks.
- Game-only validation: actual cooldown/GCD, overlay, resource shortage, aura gain/loss, health changes and combat restrictions. Container checks cannot prove in-game rendering.
- Evidence: /wow-ui-source 12.1.0.69587, revision 288f40d5cee5089223758d5810cb906ad34d4018, checked 2026-09-11.

- Completed: Lua 5.1.5 luac -p passed individually for all five new files.
- Completed: /tmp/phantom-cell-examples-check.lua passed 334 assertions using the real Cell runtime and five example modules with simulated WoW APIs. Covered all four candidate-presence combinations, first-match priority, SPELLS_CHANGED reselection/removal, initial guards, nil duration/recovery, gray nodes and midpoints, independent random delays, strict interval threshold, residual elapsed time, one refresh per long frame, opaque-token boolean handoff, health unit filtering/endpoints, and static Aura setup.
- Completed: Luacheck passed with 0 warnings/errors using explicit WoW globals, no maximum line length, and 211 ignored for the required unused addonName namespace binding. No existing declarations were cleaned up.
- Completed: verified all TOC entries resolve, new entries follow general in order, UUID placeholders and section metadata are present, and the existing 32x32 RGBA aura texture is uniformly (255,255,255,255).
- Completed: checked CustomAuraButtonPrivateMixin:UpdateAuraDisplay calls SetShown(secretwrap(auraData ~= nil)); managed slot assignment/clearing owns Show/Hide. The example only supplies static appearance.
- Limitations: API and rendering consumers are mocked in the harness; actual cooldown/GCD, proc, resource, aura, health rendering and combat/secret restrictions remain game-only checks and were not run.

## Review Notes

- 2026-09-11 14:58:54 UTC: shared understanding confirmed by user message “Implement the plan.” through the native implementation flow; environment is now Default mode. Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria are frozen.
- Archive collision check passed for this basename in .plan, .mean, and .prompt; all three are unignored.
- Pre-existing unrelated changes include Python capture work, specs, prior archives, and runtime/01_addon.lua and runtime/04_baseline_definition.lua. Preserve and exclude all of them from this task commit.
- No implementation writes occurred during Plan mode. Archives are created after explicit implementation authorization.

- Validation preserves existing TOC CRLF line endings and verbatim trailing whitespace in the archived primary prompt. Whitespace checks use cr-at-eol and exclude blank-at-eol only for that evidence archive.

## Completion

Implemented the five examples and TOC integration. Available container validation passed; game-only validation remains explicitly unverified. The success commit contains exactly the five examples, TOC, and these three archives. Unrelated pre-existing changes are preserved and excluded. No external actions or pushes are authorized or performed.

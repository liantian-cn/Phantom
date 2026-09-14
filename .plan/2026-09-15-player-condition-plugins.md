# Add 23 Player Condition Plugins

## Goal
Implement 23 player conditions from the user-designated PhantomProject Lua, using Phantom naming, rendering and Python contracts.

## Scope
Add condition.py, template.lua and plugin.toml under phantom/conditions/liantian_cn.<name>@dev for:
player_role, player_in_combat, player_is_player_target, player_is_moving, player_in_vehicle,
player_melee_enemies_count, player_is_targeting_spell, player_is_chatting, player_in_group,
player_trinket_ready, player_healthstone_ready, player_heal_potion_ready, player_cast_progress,
player_is_empowering, player_cast_icon, player_cast_target, player_has_big_defensive,
player_has_dispellable_debuff, player_has_spell, player_has_talent, player_damage_absorb,
player_heal_absorb, player_has_buff.
Include necessary tests, condition contract documentation and workflow archives. Do not change existing rotations or core public interfaces.

## Decisions
- Only inspect Lua in PhantomProject. Borrow its API, event and secret handling, not its naming or coloring.
- Required snake_case parameters: spell_id for melee; slot_id for trinkets; spell_ids for spell/talent; buff_ids for buffs; dispel_types for dispels; threshold for absorbs. Others accept no arguments.
- IDs are positive integers; ID lists nonempty. slot_id is 13 or 14. threshold is a nonnegative integer with distinct N and N+1 in Lua. Reject unknown fields and booleans used as numbers.
- dispel_types is a required boolean map over Magic, Poison, Disease, Curse, Stealth, Special, Enrage. Omitted keys are false; empty/all-false maps match nothing.
- Vehicle includes mounts; chatting means any keyboard focus; grouping includes raids.
- Melee scans nameplate1..40, requiring existence, attackability and configured spell range. Secret or nil range is excluded.
- Trinkets use the chosen slot. Healthstone/potion use 224464/258138 without added inventory count checks. Keep cooldown/usability semantics.
- Spell and talent have identical any-candidate IsSpellKnown or IsSpellInSpellBook behavior and cancellable 0.25-second refresh.
- Roles return TANK/HEALER/DAMAGER/NONE. Cast targets return player, party1..4, raid1..40 or empty string. Empty icons return empty string; others IconTile.hash.
- Booleans fallback False; counts 0; progress 0.0; roles NONE; target/icon empty string. Cast progress is float 0..100; idle 0.0. Empower is a channel subtype.
- Cast-target matching, secret-target retention, terminal-event clearing and two-second periodic clearing follow old Lua, including early clearing of long casts.
- Dispel uses HARMFUL|RAID_PLAYER_DISPELLABLE plus configured types. Buff uses HELPFUL plus configured spell IDs. Big defensive uses HELPFUL|BIG_DEFENSIVE and the reference sorting.
- Every plugin registers PLAYER_ENTERING_WORLD and appropriate player unit filters; each owns an event frame and initializes via UIInitFuncs.
- Existing two-second polls remain; progress poll is 0.1 seconds. Start each at -random(), subtract one interval, preserve remainder and refresh at most once per frame. Moving events refresh through C_Timer.After(0, function() update() end).
- Ordinary booleans use strict black/white Cells. Roles encode NONE/TANK/HEALER/DAMAGER as grayscale bytes 0/85/170/255; inaccessible roles yield NONE. Melee grayscale count/40 decodes with nonnegative rounding.
- Target grayscale uses five-byte steps: 0 unknown, 1 player, 2..5 party, 6..45 raid. Invalid codes fall back empty string.
- Progress uses CreateColorCurve black at 0 and white at 1, passed to DurationObject:EvaluateElapsedPercent. Cast textures use IconTile and Phantom's player spell border.
- Aura uses one Cell region with black backing and one fixed white Aura slot, existing buff example frame levels; entering-world calls UpdateAllAuras. No Lua aura data/visibility inspection.
- Absorbs use one Cell region with a white StatusBar over black, bounds N/N+1, directly receiving secret SetValue input.

## Implementation Steps
1. Recheck develop/worktree/collisions, freeze this plan and create matching mean and prompt records after authorization.
2. Implement all 23 triplets using existing validators, frozen layout and same-frame decoder. No cross-plugin imports.
3. Preserve confirmed reference behavior; use safe cast sentinels and direct secret display consumers.
4. Add required headers and Chinese business documentation, API/parameter/output/fallback descriptions and pinned local provenance. Update condition inventory.
5. Add focused Python/Lua execution tests, run checks, review changes and make one atomic local commit.

## Acceptance Criteria
All 23 exact identifiers load/generate independently, including multiple parameterized instances. Output types and confirmed semantics match. Encoders/decoders agree at normal/boundary/empty/invalid values. Official aura/secret consumers are respected. Events, deferred movement and staggered polls work. Documentation and strict typing pass. Offline simulation is distinguished from actual game validation.

## Verification
Plan investigation: develop clean; local WoW source 12.1.0.69587 revision a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58. Wiki requests failed; do not claim live Wiki verification.
Planned: invalid/missing/unknown arguments; ID/slot/threshold/dispel boundaries; four roles/counts 0..40/all target tokens/progress/icon/boolean/fallback pixel round trips; generated Lua initialization/events/delays/polling/isolation/cast transitions/target clearing/item readiness; aura configuration and opaque secret display doubles; all-plugin mixed layout and Lua 5.1 syntax; full pytest, scripts/check_types.py, Ruff check and format check. Actual game validation remains outstanding unless exercised.

Implemented verification: full pytest 562 passed, 5 skipped (existing Windows symlink privilege cases); all 159 new player-condition tests passed. scripts/check_types.py passed for the 57 ordinary source files and each exact-version entry (34 conditions plus capture/keyboard). Ruff check and format --check passed across phantom, rotations, tests, demo and scripts (93 formatted Python files). All 23 plugin.toml files parsed and matched their exact identifiers. New templates executed under Lua 5.1 with actual Cell/IconTile code and display/API doubles; mixed all-plugin generation compiled. No game installation, game key input or actual in-game validation.

## Review Notes
Frozen: 2026-09-15T00:45:50.791489+08:00; source: user “Implement the plan.” after native Plan-to-implementation transition. Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
No files were written during Plan mode. The user accepted Q1..Q11 and then authorized implementation through the native flow with “Implement the plan.”
No user decisions were delegated. Archive collision check passed for all three paths; none are ignored.

Implementation audit 2026-09-15T01:02:45.418717+08:00: confirmed requirements unchanged. The first focused test run had four bridge-fixture failures because Lua table field items collided with Lupa's Python items method; bracket access fixed the fixture, then the complete suite passed. Per-plugin provenance was narrowed to actual source files. Final diff contains only this task's additions plus plugin-system/testing records. Mean related_paths now lists every affected implementation/test/documentation file. Prompt R1–R14 covers initial requirements, all eleven answers and implementation authorization.

## Completion
Implementation and offline acceptance completed. Delivery consists of all 23 plugins, paired tests, documentation and the three workflow archives together in one authorized atomic local commit on develop. Actual game validation remains outstanding; no push or game installation was performed.

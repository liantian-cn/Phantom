# Goal

Add the third and fourth general Cells reflecting shared enable and burst states.

# Scope

Create phantom/lua/general/03_enable.lua and 04_in_burst.lua, append both TOC entries, and document their pixel contracts. Preserve all runtime code and existing general Cells, including the uncommitted specialization comment edit.

# Decisions

- Third field: index: 3, x=3, y=1, uuid: c845da87-d22c-462b-9696-0678101df51b; read addonTable.ENABLE on each refresh.
- Fourth field: index: 4, x=4, y=1, uuid: 0db46515-244d-4755-9a77-65b3581d85ef; call addonTable.InBurst() on each refresh. This function returns a boolean; do not encode BurstRemaining().
- Both use ordinary Cell:setCellBoolean: true is white, false is black, alpha 1. Enable state does not gate burst output.
- Construct through UIInitFuncs with existing scale, row count and background resizing. Keep default black until the first staggered update; do not refresh on construction.
- Each file has an independent local eventFrame = CreateFrame("Frame") and local fastTimeElapsed = -random(), with local random = math.random. Do not seed the random generator.
- HookScript("OnUpdate") accumulates elapsed. If strictly greater than 0.1, subtract exactly 0.1 and refresh once. Preserve remaining elapsed; no loop, timer reset or additional event registrations. Refresh before construction safely returns.
- Follow existing Lua sections and concise Chinese business comments. No new public interfaces.

# Implementation Steps

1. Check archive collisions and ignore rules; create and freeze the confirmed archives.
2. Add both independent general modules with required metadata and staggered update callbacks.
3. Append TOC entries in third/fourth order and update the first-row field specification.
4. Run syntax, TOC and temporary Lua mock verification of timing, shared state and combined layout.
5. Review and create one atomic local commit on develop containing task files and archives only.

# Acceptance Criteria

- Third and fourth Cells occupy (3,1) and (4,1), initially black, then accurately reflect live enable and burst booleans.
- Independent random initial delays, strict threshold, remainder preservation and at most one refresh per frame match the supplied code.
- Early callbacks are safe, repeated updates never create additional Cells, and ENABLE=false does not suppress burst state.
- Four general Cells share existing scale and background geometry, with general row length 4.
- TOC, metadata and specification match the approved plan.

# Verification

- Repository sources checked: runtime/03_rotation_variable.lua defines ENABLE and callable InBurst using BurstTime > GetTime(); runtime/07_cell.lua provides black/white boolean rendering and row counting; runtime/06_panel.lua demonstrates OnUpdate HookScript usage.
- Planned: Lua syntax and TOC checks; deterministic random/elapsed mocks for initial delay, exact threshold, long frame, retained remainder, pre-init callback safety, live ENABLE changes and burst expiry, independent state updates, four-Cell normal/debug geometry and no duplicate creation.
- Manual game display verification is outside container capabilities.

- Passed: luac -p for both new Lua modules.
- Passed: /tmp/phantom-enable-burst-check.lua ran 6 combinations of ordinary/debug screen scale and pre-init callbacks, loading actual runtime 01/03/04/05/07 and all four general modules. Deterministic random values 0.25/0.75 verified distinct first refresh timing, black after construction, exact 0.1 threshold, one update on a long frame with retained remainder, and no duplicate Cells. Live ENABLE toggles and actual InBurst deadline/extension were checked independently; class and specialization textures were untouched by these updates. Verified four positions, row length 4 and background width 6 * SIZE.CELL.
- Passed: all TOC paths exist, no duplicate entries, four general files load in index order.

# Review Notes

- Frozen at 2026-09-08 16:18:57 UTC. Confirmation: user "Implement the plan." through the native plan flow; environment has left Plan mode.
- All three archive paths were absent and not Git-ignored. Archive writes were deferred during Plan mode to comply with its restrictions.
- Exclude pre-existing changes in phantom/lua/general/02_player_specialization.lua and .prompt/2026-09-05-add-lua-foundation-directory.md, .prompt/2026-09-05-create-directory-skeleton.md, .prompt/2026-09-06-runtime-documentation.md.

# Completion

Implementation and container verification completed on 2026-09-08. All task files and three archives are included in the single local implementation commit on develop. Pre-existing specialization comments and old prompt edits remain outside this commit. No external mutation was performed. Manual game verification remains unperformed; no physical display result is claimed.

# Goal
Add Delay state, addon-name-derived slash commands, and the fifth general status Cell.

# Scope
Modify runtime/03_rotation_variable.lua, add general/05_delaying.lua, update the addon TOC and pixel protocol. Paths are relative to phantom/lua unless noted. Do not alter unrelated existing prompt edits.

# Decisions
- DelayTime starts at GetTime(); Delaying() compares the latest deadline strictly against GetTime(). DelayRemaining() returns max(0, DelayTime - GetTime()) without an upper bound.
- Preserve ENABLE and Burst initialization and existing Burst queries. All three states remain independent.
- Register / followed by the first two lowercase characters of addonName, using the full addon name for the internal registry key.
- disable/enable/toggle update ENABLE. delay [NN] sets DelayTime to GetTime() + NN (default 0.4); burst [NN] sets BurstTime similarly (default 15).
- Parse NN with tonumber, imposing no sign, digit-count, or duration cap. 99999 means 99999 seconds; -1 immediately deactivates the timer. Each invocation replaces the deadline.
- Ignore command-word case and surrounding/separating whitespace. Valid commands are silent. Empty input, help, unknown commands, invalid numbers, and extra arguments print Chinese help without changing state.
- Help lists actual prefix, all five commands, defaults, and signed duration examples.
- Fifth Cell: general/05_delaying.lua, index 5, UUID db99c08a-9f97-4ae8-b076-dd2981bf99cc, x=5/y=1. Read Delaying(), true white and false black, independently of ENABLE.
- Follow existing Burst Cell initialization, random staggering, and strictly greater than 0.1-second refresh behavior.

# Implementation Steps
1. Archive confirmed intent and interview; freeze this plan after implementation authorization.
2. Add runtime state queries, command registration, parsing, and help with project-style comments.
3. Add the fifth Cell, register it in the TOC, and document its pixel contract.
4. Run syntax and mocked behavioral checks; inspect task-only diffs.
5. Commit implementation and workflow archives atomically on develop, excluding pre-existing changes.

# Acceptance Criteria
Apple registers /ap and Bear registers /be. Commands implement the confirmed table and preserve unrelated state. Delay starts inactive, expires at its deadline, exposes unclamped positive remaining time, and renders through the fifth Cell. Invalid input only prints help. Existing Burst behavior is preserved.

# Verification
- Validate Lua syntax and mocked timer, parser, state, and UI behavior, including boundary times, signed/long durations, invalid input, initialization safety, and refresh pacing.
- Check UUID uniqueness and TOC order.
- Chat routing and physical pixel rendering require in-game verification; container checks do not establish these.
- API source verified on 2026-09-09 at /wow-ui-source revision 288f40d5cee5089223758d5810cb906ad34d4018: SystemTimeDocumentation.lua and Blizzard_ChatFrameBase/Shared/SlashCommandsRegistry.lua. Wiki references: https://warcraft.wiki.gg/wiki/API_GetTime and https://warcraft.wiki.gg/wiki/Creating_a_slash_command.

- Passed Lua 5.1.5 syntax check: luac -p on both changed Lua files.
- Passed /tmp/phantom-delay-verification.lua using mocked GetTime, SlashCmdList, CreateFrame and Cell: Apple/Bear prefixes; independent enable/delay/burst updates; defaults, decimals, zero, negatives, long values and exponent notation; deadline equality and overwrite; invalid-input help with unchanged state; initialization guard, initial black, strict refresh threshold and one refresh per frame with retained backlog.
- Passed unique UUID scan and TOC file existence/order checks.
- Preserved existing CRLF in runtime and TOC; task diff whitespace check uses core.whitespace=cr-at-eol.

# Review Notes
- Frozen at 2026-09-09T12:46:29.221627+00:00; confirmation source: user native Plan-to-implementation authorization, “Implement the plan.” Environment is now Default mode. No files were written in Plan mode.
- Initial archive collision check passed. Existing edits in three older .prompt files are excluded.

- A concurrent .vscode/settings.json change appeared during implementation; it is not part of this task and remains unstaged.

# Completion
Implemented all confirmed behavior and completed container verification. In-game chat routing and physical rendering remain manual verification items. The task implementation, mean, plan and prompt are included in one atomic local commit on develop; unrelated prompt and editor-setting changes are excluded.

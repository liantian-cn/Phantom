# Keyboard Plugins and Continuous Rotation Execution

## Goal

Implement roadmap steps 14–16 and bring forward step 17's keyboard plugin architecture. Complete automated and feasible local Windows verification; retain real-game acceptance as pending.

## Scope

Replace the planned actions category with keyboards. Implement PostMessageW, macro-binding generation, continuous execution, frame identification, built-in expression variables, and the blood DK example. Sleep and Pass remain future aliases of Idle.

## Decisions

- Kernel selects macros and parses platform-neutral typed key combinations; plugins receive no macros, rules, or window parameters.
- Public facilities: phantom/core/keyboard/. First implementation: phantom/keyboards/liantian_cn.post_message@dev/keyboard.py.
- keyboard.plugin defaults to liantian_cn.post_message@dev, exact loading, independent instances, no fallback.
- Plugin resolves exactly one window titled 魔兽世界 for each send. Follow the supplied keyboard reference: WM_KEYDOWN/WM_KEYUP, zero lParam, ordered presses, 10 ms hold, reversed releases.
- Process the latest new screenshot once, including identical-content new frames; no backlog. Existing Start runs collection and execution with a valid rotation, collection only without one.
- Reserved boolean expression names: 插件启用, 爆发开启, 正在延迟. No implicit gates. Blood DK starts with not 插件启用 or 正在延迟 -> Idle.
- Idle skips this round. Ordinary macros still require keys. Sleep/Pass aliases deferred.
- Target, send, and unexpected execution errors pause until manual restart. Temporarily invalid screenshots skip the round.
- Common keyboard keys: A–Z, 0–9, F1–F24, numeric keypad including arithmetic/decimal, arrows, navigation/editing, SPACE/TAB/ENTER/ESCAPE/BACKSPACE, common punctuation, unique CTRL/ALT/SHIFT prefixes.

## Implementation Steps

1. Add immutable key identifiers/combinations, synchronous send(keys), close(), exact loading, load-time key validation, and backend-owned Windows conversion.
2. Declare Windows API signatures, validate unique exact-title target, retain it for the combination, check posting results, and attempt reverse release of successfully pressed keys on failure. No elevation or automatic retries.
3. Generate bind_key=true secure buttons following the user-supplied Macro.lua (macro type/text, AnyDown/AnyUp, priority override binding) inside the existing class/spec guard. Deterministic unique names, safely encoded Lua strings; no saved macro slots or persistent binding edits.
4. Extend CaptureResult with optional sequence metadata, copied unchanged in snapshots and advanced on publication. Add one background runtime reading latest frames, decoding, deciding and sending; UI displays that decision. Referenced built-in booleans decode strict black/white from that frame; unreferenced fields do not block execution. Reject reserved-name collisions. Stop prevents new dispatch and waits for current releases; discard stale UI updates and join resources.
5. Synchronize specifications, plugin author documentation/metadata, defaults, type-check discovery, and roadmap. Record implementation/offline evidence separately from outstanding real-game acceptance.

## Acceptance Criteria

Kernel owns key decisions; plugin only delivers keys. Each new valid frame sends at most once; rereads never resend. Idle sends nothing and does not persistently pause. Enable/delay affect the example only through its explicit rule. Target/send failures pause visibly until manual restart. Stop prevents subsequent combinations and waits for releases. Generated bindings follow the supplied example and bind_key distinction.

## Verification

Test key parsing/mapping, exact plugin loading/path rejection/missing versions, new-frame deduplication and identical-content new frames, Idle, built-ins, invalid frames, failures and stop/restart races. Test Lua 5.1 generation and API doubles including escaped/multiline text and both binding modes. Test responsive TUI/same decisions/errors/shutdown. Use an isolated owned Windows receiver for actual posted messages, never real-game sending. Run pytest, complete strict mypy including keyboard entry, Ruff check and format check. Real-game ordinary/modifier keys, bindings and sustained-loop acceptance remain pending.

- 2026-09-14: Final verification: 368 passed, 5 skipped in 22.39 s. Skipped cases are existing symlink escape tests requiring unavailable Windows symlink privilege. Full scripts/check_types.py passed for core and all ten version entries. Ruff check and format --check passed (67 Python files); git diff --check passed.
- Real PostMessageW messages were received only by a test-owned hidden window, including CTRL-1 and ALT-F4; no messages were sent to a game. Lua 5.1 and API doubles verified bindings/text preservation. Exact-loaded synthetic capture and recording keyboard completed continuous-loop regression.
- Initial local virtual environment lacked pinned dependencies; requirements-dev.txt was installed without changing dependency files.

## Review Notes

- 2026-09-14T09:28:32+08:00: Frozen. Confirmation source: user "Implement the plan." after the native proposed plan; environment is Default mode. Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
- Three archive paths checked absent before creation; develop worktree initially clean.
- Referenced E:/Documents/GitHub/wow-ui-source is unavailable here. Online source at pinned a89e9d0ceb7f6cd31e8fc5ca7df1a338ac0b1b58 was inspected; SecureTemplates.lua retains macrotext branch. User's Macro.lua is the specified generation example.
- User corrected target ownership to plugins and enable/delay handling to explicit expressions. Both corrections are reflected above.

## Completion

Implementation and authorized offline acceptance completed on 2026-09-14. Task files and all three archives are included in one atomic local commit on develop. No push, game-directory installation, or real-game sending occurred. Real-game acceptance remains explicitly pending in roadmap steps 14–17.

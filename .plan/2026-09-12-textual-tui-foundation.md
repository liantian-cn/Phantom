# Goal

Implement roadmap steps 5 and 6: a Textual TUI controlling capture and displaying the five existing general Cells.

# Scope

Add working-directory application configuration, a Latte TUI, game-process detection, capture lifecycle integration, business logs, tests and relevant documentation. Retain disabled addon generation and placeholder macro/rotation-condition tabs. Exclude rotation loading, addon generation, analysis, actions and changes to Lua or external references.

# Decisions

- Run through python -m rotations.main. Default to paused; Start begins capture/decode/display and Close stops collection without exiting the TUI.
- Read phantom.toml from the process startup working directory, never from the program directory; do not chdir. Create defaults only when absent, read once at startup and never rewrite an existing file. Missing fields use defaults. Syntax/type/read/write errors fail explicitly.
- Configuration defaults: [capture] fps=15; [ui] min_width=120, min_height=46, log_max_lines=1000. FPS is finite and positive; UI numbers are positive integers.
- Use the exact user-supplied Catppuccin Latte palette. Base background, Mantle containers, Text foreground, Blue selection; state on is Green and off is Peach.
- content fills remaining space; footer docks to bottom with content-driven height and contains only one single-line status_line. Status items are left aligned and separated by " · ".
- Tab order: 综合, 通用条件, 日志, 宏绑定, 循环条件; default 综合. Tab/Shift+Tab wrap between tabs; Up/Down select enabled overview buttons, Enter/Space activate, Ctrl+Q exits; mouse supported.
- Below configured minimum size, content shows actual/required size while footer remains visible. Resizing preserves active tab and execution state.
- Overview uses approximately 1:3 left/right columns. Left: 启动, 关闭, disabled 生成插件 with pending explanation. Right: program state, game state, capture state, board width/height, configured FPS, current error.
- General table has five named rows mapped to getCell(1..5,1) from the same valid frame. Columns: 项目, RGB, 亮度值, 显示值. RGB is color_string; mean only when is_pure; display value always empty. Non-pure mean and unavailable raw data use an em dash. Pause/capture/decode failure clears old values.
- Business log component exposes log(message: str), separate from Python/Textual diagnostic logging. Add local [HH:MM:SS] timestamp at insertion, suppress consecutive identical bodies before timestamping, retain at most configured 1000 physical lines, evict oldest, fill tab space and scroll. Record program transitions, game transitions, capture failure/recovery; never log every frame.
- Detect game independently once per second with psutil. Require case-insensitive wow.exe filename and direct parent _retail_ in executable path; no hardcoded drive. No confirmed matching process disables Start. Game exit stops collection and clears data. Game return requires manual Start. Unverifiable candidate paths cannot count as running and expose a reason.
- Reuse the existing GDI worker and latest-result snapshot, sample/decode for UI at configured FPS without queuing frames. Process queries and blocking stop run off the UI thread; update widgets through Textual messages on the UI thread.
- Extend capture worker with a read-only running property to distinguish recoverable locating/validation errors from terminated capture. Fatal termination pauses the program, reports failure and permits explicit restart.
- Share cleanup for Close/game exit/application exit; disable Start during stop, wait for resources, reject stale results after pause.
- Preserve the exact supplied palette values in English .context; write Chinese TUI requirements and synchronize routing, configuration, architecture, development, testing and roadmap documentation.
- Pin Textual, psutil and needed dependencies; keep Python 3.13, pytest, mypy strict and Ruff.
- User delegated overview design; the chosen current-state panel and proportional layout expose actual capture status without anticipating rotation behavior.

# Implementation Steps

1. Create and freeze matching workflow archives after native authorization.
2. Implement typed configuration, game detection, capture lifecycle integration and TUI; pin dependencies.
3. Add behavior-focused tests and update minimum related specifications and roadmap.
4. Run automated checks, Windows capture/TUI smoke verification and record exact limits of live game verification.
5. Commit implementation and archives atomically on develop without pushing.

# Acceptance Criteria

- UI starts paused, stays responsive during capture/stop, uses all specified tabs/keys/colors/layout and releases threads when exiting.
- Configuration is independent of program path, created only when missing, validated explicitly and never silently overwritten.
- Only a verified retail WoW process permits starting; losing the game pauses, returning does not restart.
- Five raw fields come from one valid frame; purity controls mean and failures/pause remove old raw data.
- Logs have insertion timestamps, consecutive deduplication and bounded history with explicit business events only.
- Automated checks pass, including lifecycle, CWD, process matching, raw data, logging, resize and input scenarios.
- Windows and live game evidence is recorded honestly; do not mark roadmap step 6 complete before manual live state-change verification.

# Verification

- Initial repository: develop, clean working tree.
- All three target archive paths checked absent on 2026-09-12 before creation; git check-ignore confirmed none ignored.
- 2026-09-12, Windows with the project `.venv` on Python 3.13.15: `pytest` 82 passed; `mypy` strict clean for 30 source files; `ruff check` and `ruff format --check` clean after normalizing three files with mixed line endings.
- 2026-09-12 Windows desktop smoke through the real entry point: the app created the default `phantom.toml` in the launch directory (matching the default template), opened paused, kept Start disabled because no verified retail process existed, switched tabs in the order 综合→通用条件→日志→宏绑定→循环条件, exited on Ctrl+Q, and left no `phantom-` threads. Resolved styles were Base `#eff1f5`, Text `#4c4f69`, Mantle `#e6e9ef`, and Blue `#1e66f5`.
- 2026-09-12 Windows GDI worker probe: `is_running` was true after start with `has_error=true` and the reason “未找到非 DEBUG 基板定位标记”, the image stayed `None`, and stop returned it to not running.
- Not verified: in-game state change reflected in the TUI. No retail `wow.exe` process was running during verification, so roadmap step 6 stays unchecked and the limitation is recorded in `.spec/testing.md` and `todo_list.md`.

# Review Notes

- Frozen at 2026-09-12T11:36:04+08:00 (Asia/Shanghai).
- Confirmation source: native Plan-to-implementation flow and user message "Implement the plan." Environment entered Default mode before all writes.
- Plan-mode restrictions prohibited draft file writes during the interview; confirmed archives are created together now.
- User selected no-game auto-pause instead of informational-only detection; this is included in frozen behavior.
- Continuation on 2026-09-12 after the user reported the plan unfinished: completed the specification and roadmap synchronization, added the Windows smoke evidence, and made the single workflow commit. No frozen requirement changed.

# Completion

Implementation, automated verification, documentation synchronization and Windows desktop smoke verification completed on 2026-09-12. Roadmap step 5 is marked complete with evidence; step 6 remains unchecked until in-game state changes are verified. Implementation, tests, specifications, roadmap and workflow archives are included in one local commit on develop; nothing was pushed and no external reference was modified.

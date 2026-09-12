# Goal

Replace the TUI's Catppuccin Latte light palette with a fixed Catppuccin Mocha dark palette and synchronize the specifications, context palette and verification evidence.

# Scope

Change the Textual theme module, stylesheet color variables, status-line colors, theme regression tests, `.spec/tui.md`, `.spec/architecture.md`, `.spec/project-overview.md`, `.spec/testing.md`, `.context/README.md`, and replace `.context/catppuccin-latte.md` with `.context/catppuccin-mocha.md`. Exclude layout, interaction, application configuration schema, WoW Lua rendering, dependency versions and existing history archives.

# Decisions

- Use the exact official Catppuccin Mocha palette from catppuccin/palette 1.8.0, transcribed without rewriting, approximating or substituting values.
- The theme is fixed dark: no system or terminal detection, no `phantom.toml` theme field and no switching shortcut. Textual 8.2.8 has no terminal background detection and Windows Terminal provides no reliable signal.
- Keep the existing semantic mapping: Base background, Mantle containers, Text foreground, Blue selection and accent, Mauve secondary, Peach warning, Red error, Green success; state on uses Green and state off uses Peach.
- Rename the theme to `phantom-mocha`, the palette constant to `MOCHA` and the CSS variables to `mocha-*`; active code and documentation no longer define Latte.
- Replace the Latte context palette file with a Mocha file that preserves the same Color/Hex/RGB/HSL/OKLCH table structure, sourced from the official palette with its retrieval date.
- Update `.spec/testing.md` smoke evidence to the re-verified Mocha resolved colors instead of keeping the superseded Latte observation.

# Implementation Steps

1. Create and freeze matching `.plan`, `.mean` and `.prompt` archives after authorization.
2. Rewrite `phantom/ui/theme.py` with the Mocha palette and `phantom-mocha` theme; update the stylesheet variables and the status-line colors.
3. Add a theme regression assertion to `tests/test_ui.py`.
4. Replace the context palette file and update the routing, TUI, architecture, overview and testing documents.
5. Run the automated checks, record the resolved-color evidence and commit implementation, tests, documentation and archives atomically on develop.

# Acceptance Criteria

- The application starts in a dark Catppuccin Mocha theme, and no Latte color remains in active code or documentation.
- Palette values match the official Catppuccin Mocha values exactly, and the specification points at the Mocha context file.
- Layout, interaction, configuration and capture behavior are unchanged; tests, mypy strict and Ruff pass.
- Resolved TUI styles use Mocha Base `#1e1e2e`, Mantle `#181825`, Text `#cdd6f4` and Blue `#89b4fa`.
- Archives record the decisions, and one local commit on develop contains implementation, tests, specifications, context and archives; nothing is pushed.

# Verification

- Initial repository: develop; the only untracked file was the user's `phantom.toml`, outside this task.
- 2026-09-12: all three target archive paths were absent and not git-ignored before creation.
- 2026-09-12, Windows with the project `.venv` on Python 3.13.15: `pytest` 83 passed; `mypy` strict clean for 30 source files; `ruff check` and `ruff format --check` clean.
- 2026-09-12 theme evidence through real Textual widgets (`run_test`, 120x46): active theme `phantom-mocha` with `dark=true`, Screen background Base `#1e1e2e`, Text foreground `#cdd6f4`, footer and panel containers Mantle `#181825`, TabPane Base `#1e1e2e`, and status-line spans Peach `rgb(250,179,135)` for 程序 and Green `rgb(166,227,161)` for 游戏. Resolved CSS variables contain `mocha-*` values and no `latte-*` key.
- Not verified: an interactive desktop terminal run. Allocating a PTY failed in this environment (ConPTY process creation error), so the dark theme was verified through resolved widget styles and CSS variables instead of a terminal screenshot. No in-game verification was performed or claimed.

# Review Notes

- Frozen at 2026-09-12T12:38:00+08:00 (Asia/Shanghai).
- Confirmation source: native Plan-to-implementation flow and user message "Implement the plan." Environment entered Default mode before all writes.
- Plan-mode restrictions prohibited draft file writes during the interview; confirmed archives are created together now.
- Interview decisions: Catppuccin Mocha; fixed dark theme without system following; replace the Latte context file with Mocha instead of keeping both.

# Completion

Implementation, test, documentation and verification work completed on 2026-09-12. The TUI now uses a fixed dark Catppuccin Mocha theme with no Latte color left in active code or documentation. Implementation, tests, specifications, the replaced context palette and the three workflow archives are included in one local commit on develop; nothing was pushed and no external reference was modified.

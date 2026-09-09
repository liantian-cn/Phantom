# Phantom development roadmap

## Goal

Create a Chinese root-level `todo_list.md` with 20 ordered milestones leading to a complete personally usable Phantom version.

## Scope

Documentation only: `todo_list.md` and the matching plan, mean, and prompt archives. No application implementation, specification changes, dependency changes, or external operations.

## Decisions

- Mark Lua foundation as complete based on the user's explicit statement; mark all remaining milestones incomplete.
- Give each milestone its goal, main tasks, prerequisites, completion criteria, and relevant deferred design questions.
- Interpret multiple rotations as managing, generating, selecting, and matching multiple rotation configurations, with one active at a time.
- Target a personally usable complete version, without adding distribution packaging or release engineering.
- Establish screenshot and action functionality before extracting their versioned plugins.
- Separate a single evaluation without input dispatch from continuous execution with real actions.
- Keep unresolved plugin lists, interfaces, TUI pages, and scheduling policies as design tasks for their respective future stages; this roadmap does not freeze those choices.
- Retain current specifications as authority and link them rather than duplicating their full contents.

## Implementation Steps

1. Record confirmation and freeze this plan; create matching intent and prompt archives.
2. Create the roadmap with these ordered milestones: Lua foundation; Python foundation; screenshot module; NumPy parsing; Textual foundation; basic capture data display; rotation configuration; condition plugin foundation and layout; small test plugin set; single-rotation Lua generation; expression evaluation; single dry evaluation; condition and decision display; action foundation; continuous single-rotation execution; screenshot plugin extraction; action plugin extraction; multiple rotation management; business plugin expansion; complete acceptance and personal usage instructions.
3. Add prerequisites, tasks, and measurable completion criteria to each milestone, with design questions only where relevant.
4. Review coverage, dependency ordering, current-spec consistency, Markdown links, and whitespace. Distinguish container checks from Windows and in-game verification.
5. Commit exactly the roadmap and three archives atomically on develop, excluding unrelated existing changes; do not push.

## Acceptance Criteria

- Root `todo_list.md` is Chinese and contains exactly 20 ordered milestone checkboxes, with only the first checked.
- All user-listed subjects and the missing engineering, configuration, layout, generation, evaluation, and end-to-end stages are covered.
- Every milestone has a goal, tasks, prerequisites, and completion criteria.
- The roadmap preserves the confirmed single-active-rotation interpretation and functional-module-before-plugin-extraction sequence.
- Future unresolved decisions are not represented as established requirements or completed work.
- Only the four task documents enter the local commit.

## Verification

- Inspected `.spec/README.md` and all seven routed specification documents during planning, plus repository structure and the current Lua TOC.
- Repository is on develop; Python module and rotations directories contain placeholders.
- Rechecked before writing: all four target paths are absent. Planning ignore checks found no matching ignore rules for them.
- Business tests are unnecessary for this documentation-only task; document checks will be recorded below.
- Document validation passed: exactly 20 sequential milestones, one checked and 19 unchecked; all milestones contain goals, tasks, prerequisites, and completion criteria; all numbered dependencies point backward; every local Markdown link resolves.
- Archive validation passed: required section names match all three protocols and no Pending markers remain. Reviewed coverage and deferred decisions against the agreed roadmap and existing specifications.
- All four task paths are unignored. The roadmap whitespace check reported no errors.

## Review Notes

- Confirmed at 2026-09-09 15:46:32 UTC; source: user message `Implement the plan.` following the native Plan flow, with the environment now in Default mode.
- Frozen: Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria.
- Plan-mode restrictions prevented writing the draft during the interview; this archive is created after confirmation and before the roadmap.
- Existing changes in three historical prompt archives, `.vscode/settings.json`, and `phantom/lua/runtime/06_panel.lua` are outside this task.

## Completion

The roadmap and all three archives are complete. Document validation passed; no business code or project specifications were changed. The atomic local commit containing these four files is the completion record. No push is authorized; pre-existing modifications remain outside this task.

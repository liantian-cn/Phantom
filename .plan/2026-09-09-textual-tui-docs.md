# Textual TUI documentation

## Goal

Replace the planned PySide6 UI with a Textual TUI in the current project specifications.

## Scope

Update `.spec/project-overview.md` and `.spec/architecture.md`, plus this task's plan, intent, and prompt archives. Documentation only; no dependencies, UI implementation, public API, configuration format, or source directory changes.

## Decisions

- Use Textual for the terminal user interface.
- Include a brief capability description covering messages/events, Signal pub-sub, reactive state, and Workers, with official documentation links.
- Keep rotation selection, generated package name entry, and future configuration responsibilities.
- Preserve the rotation table with checkboxes in the first column, mutual exclusion for identical `(unit_class, unit_spec)`, and coexistence across different classes or specializations.
- Preserve the rule that the old Terminal project is not a visual or interaction reference.
- Leave complete page design, interactions, concrete communication mechanisms, and runtime scheduling to future tasks.

## Implementation Steps

1. Record confirmation and freeze this plan; create matching intent and prompt archives.
2. Replace the PySide6 selection and related future-design wording in both specifications.
3. Add a concise Textual capability subsection to architecture, with official references and the distinction between framework capabilities and undecided project design.
4. Review the document diff, check current specifications for obsolete selection wording, and run whitespace checks.
5. Commit only the two specifications and three task archives in one local commit on develop; do not push.

## Acceptance Criteria

- Current specifications consistently select Textual TUI and no longer select PySide6.
- The confirmed rotation interaction rules and old Terminal reference restriction remain intact.
- Capability descriptions match the official references and do not freeze a communication or scheduling implementation.
- No unrelated existing changes or historical archive rewrites enter the task commit.

## Verification

- Planning inspection found four PySide6 mentions across the two target specifications.
- Official Textual events, signal, reactivity, and worker documentation was checked during planning on 2026-09-09.
- Before implementation, confirmed develop, no archive filename collisions, and no ignore rules affecting the three archive paths.

- Reviewed both specification diffs: all four PySide6 mentions are replaced, rotation selection rules and the Terminal restriction are preserved, and linked capabilities match the references checked during planning.
- `git diff --check -- .spec/project-overview.md .spec/architecture.md` passed. The unrestricted check reported whitespace in pre-existing changes outside this task; those files are left untouched.
- No business tests are required for this documentation-only change. `git diff --cached --check` passed for all five task files; the staged file list contains exactly the authorized documents and archives.

## Review Notes

- Confirmation recorded at 2026-09-09 13:28:44 UTC; source: user message `Implement the plan.` following the native plan flow, with the environment now in Default mode.
- Frozen: Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria.
- Plan-mode restrictions prevented writing a draft during the interview; this archive is created after explicit confirmation and before specification edits.
- Existing changes in three historical prompt archives, `.vscode/settings.json`, and `phantom/lua/runtime/06_panel.lua` are outside this task.

## Completion

Documentation updates and task archives are complete. The atomic local commit containing these five files is the completion record; no push is authorized. Unrelated working-tree changes remain outside the commit.

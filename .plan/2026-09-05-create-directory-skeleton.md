# Goal

Create the documented Phantom application directory skeleton without adding application code.

# Scope

- Create `phantom/ui/`, `phantom/core/`, `phantom/conditions/`, `phantom/actions/`, `phantom/captures/`, `scripts/`, and `rotations/`.
- Add one empty `.gitkeep` file to each leaf directory so Git tracks the empty structure.
- Do not create `main.py`, Python package files, concrete versioned plugin directories, tests, configuration, or business documentation.
- Preserve all unrelated pre-existing user changes.

# Decisions

- The directory list follows the frozen `预定源码结构` in `.spec/architecture.md`.
- Concrete plugin directories are excluded because `.spec/plugin-system.md` leaves the first condition-plugin list unresolved and presents named versions only as examples or first-version plans.
- `.gitkeep` is a tracking placeholder only and contains no content.

# Implementation Steps

1. Create the seven documented leaf directories.
2. Add an empty `.gitkeep` file to every leaf directory.
3. Verify the exact structure, placeholder emptiness, Git visibility, and absence of out-of-scope files.
4. Commit the directory skeleton and all task workflow archives atomically without including unrelated changes.

# Acceptance Criteria

- All seven documented leaf directories exist.
- Each leaf directory contains only an empty `.gitkeep` file.
- No application code or concrete versioned plugin directory is created.
- Unrelated pre-existing changes to `.gitignore`, `LICENSE`, and `README.md` remain untouched and are excluded from the task commit.
- The successful task is recorded in one local Git commit on `develop`.

# Verification

- 2026-09-05: Verified that all seven documented leaf directories exist.
- 2026-09-05: Verified that each leaf directory contains exactly one zero-byte `.gitkeep` and no other file.
- 2026-09-05: Verified that no `Pending` marker remains in the task archives.
- 2026-09-05: Verified that unrelated modifications to `.gitignore`, `LICENSE`, and `README.md` remain outside the task staging scope.

# Review Notes

- 2026-09-05: Draft created from the user's request and the repository's documented future source structure.
- 2026-09-05T15:45:29Z: The user answered `1`, confirming the shared-understanding summary and authorizing implementation. `Goal`, `Scope`, `Decisions`, `Implementation Steps`, and `Acceptance Criteria` are frozen.

# Completion

- 2026-09-05: Created the documented directory skeleton without application code or concrete plugin versions.
- 2026-09-05: Prepared the directory placeholders and workflow archives for one atomic local commit on `develop`.

# Goal

Design and create a repository directory for shared Lua runtime foundations required by generated condition plugins.

# Scope

- Add one shared Lua foundation directory under `phantom/` and track it with an empty `.gitkeep`.
- Clarify the directory's responsibility and its boundary from versioned condition-plugin `template.lua` files in the smallest relevant specification.
- Do not add Lua implementation files, Python code, generated addon output, or concrete plugin versions.
- Preserve unrelated pre-existing user changes.

# Decisions

- Use `phantom/lua/runtime/` so `lua` identifies game-side source assets and `runtime` identifies shared runtime support included in generated addons.
- Update `.spec/architecture.md` to make the new source-directory responsibility normative.
- Shared Lua foundations are source assets consumed by the generator, not generated addon output and not condition-specific templates.
- Keep the final shared-Lua file split unresolved; this directory-only task does not invent module filenames or contents.

# Implementation Steps

1. Create the confirmed shared Lua foundation directory with an empty `.gitkeep`.
2. Update the architecture source tree and responsibility description without deciding the still-unresolved final Lua file split.
3. Verify the directory, placeholder, documentation consistency, and task-only Git scope.
4. Commit the implementation and workflow archives atomically without unrelated changes.

# Acceptance Criteria

- `phantom/lua/runtime/` exists and is tracked by an empty `.gitkeep`.
- No Lua or Python implementation code is added.
- The boundary between shared Lua runtime foundations and condition-specific `template.lua` is unambiguous.
- Unrelated modifications to `.gitignore`, `LICENSE`, and `README.md` remain untouched and excluded from the task commit.
- The successful task is recorded in one local Git commit on `develop`.

# Verification

- 2026-09-05: Verified that `phantom/lua/runtime/.gitkeep` exists, is zero bytes, and is the directory's only file.
- 2026-09-05: Verified that `.spec/architecture.md` records the source-tree location, generated-addon role, condition-template boundary, and exclusion of generated output.
- 2026-09-05: Verified that the final shared-Lua file split remains explicitly unresolved.
- 2026-09-05: Verified that no `Pending` marker remains in the task archives.
- 2026-09-05: Verified that unrelated modifications to `.gitignore`, `LICENSE`, and `README.md` remain outside the task staging scope.

# Review Notes

- 2026-09-05: Draft created after reviewing `.spec/architecture.md`, `.spec/plugin-system.md`, and the current repository tree.
- 2026-09-05: The user accepted both recommended choices: `phantom/lua/runtime/` and an accompanying `.spec/architecture.md` update.
- 2026-09-05T15:54:34Z: The user answered `1`, confirming the final shared-understanding summary and authorizing implementation. `Goal`, `Scope`, `Decisions`, `Implementation Steps`, and `Acceptance Criteria` are frozen.

# Completion

- 2026-09-05: Added the shared Lua runtime source directory placeholder and documented its architectural responsibility.
- 2026-09-05: Prepared the implementation and workflow archives for one atomic local commit on `develop`.

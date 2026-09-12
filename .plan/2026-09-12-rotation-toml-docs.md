# Goal
Replace the planned rotation YAML format with TOML in current documentation.

# Scope
Update six current documents: .spec/README.md, .spec/architecture.md, .spec/project-overview.md, .spec/testing.md, .spec/configuration.md, todo_list.md. Preserve historical archives and unrelated working-tree changes. No implementation or dependency changes.

# Decisions
Use TOML only, retain schema v1, field names, values, ordering, expressions and business semantics. No YAML compatibility or migration. Use tables, arrays of tables, and condition-owned plugin argument tables in the example.

# Implementation Steps
1. Freeze and create the workflow archives after confirmation.
2. Update the six documents and convert the full configuration example.
3. Parse the TOML example and verify its data against the prior example; check current-document references and whitespace.
4. Stage only task changes and archives, then make one atomic local commit on develop.

# Acceptance Criteria
All current format requirements use TOML. The complete example parses and preserves the prior data and behavior. Existing unrelated changes remain outside the commit.

# Verification
- PASS: Python tomllib parsed the complete documented example; all nested values and list ordering equal the original example data, with integer schema_version and Boolean bind_key values.
- PASS: All six current documents contain no YAML format references.
- PASS: git diff --cached --check; reviewed the six-document staged diff.
- PASS: Existing demo-path and other user changes remain unstaged. All three archive paths are not ignored.
- No application tests required for this documentation-only change.

# Review Notes
- 2026-09-12T10:04:47+08:00: Frozen. Confirmation source: user message `Implement the plan.` following the native Plan-to-implementation flow; environment is now in Default mode.
- User confirmed the six-document scope and rejected YAML compatibility or migration.
- Archive collision check passed. Existing changes in architecture, testing and roadmap concern demo paths and can be isolated by staging only this task's changes.

# Completion
All six documentation updates and example verification are complete. Workflow archives accompany the documentation in the atomic local commit for this task; no code or dependencies changed. Commit scope was reviewed before committing.

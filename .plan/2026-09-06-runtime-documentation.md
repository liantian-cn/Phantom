# Goal

Maintain project rules and complete documentation for the six user-authored Lua runtime files.

# Scope

- phantom/lua/runtime/01_addon.lua through phantom/lua/runtime/06_panel.lua.
- .spec/development-rules.md for the Lua documentation and section conventions.
- Complete missing API localization declarations while preserving business behavior.

# Decisions

- Use an independent subagent for each Lua file, scheduling within available concurrency.
- Do not add modification history entries in this task.
- Required header fields: original, uuid, 摘要, 描述, 修改记录.
- Required sections: namespace initialization, api cache, variable reference, logical code.
- Namespace initialization contains only `local addonName, addonTable = ...`.
- Preserve original paths relative to phantom/lua, using the existing runtime\01_addon.lua format.
- Complete trailing comments for API caches, cross-file references, and business-meaningful code; structural lines such as end do not require comments.
- Archive paths are not ignored; include plan, mean, and prompt in the atomic local workflow commit.

# Implementation Steps

- Obtain final shared-understanding confirmation; then freeze the plan and create mean and prompt archives.
- Update the minimal project rules topic and dispatch each Lua file to its own subagent.
- Verify documentation accuracy and the agreed code-change boundary.
- Isolate task changes from pre-existing user edits and complete the authorized local commit.

# Acceptance Criteria

- All six files have accurate summaries and descriptions and agreed trailing comments.
- Preserve existing UUIDs if unique and preserve existing modification history.
- Project rules reflect confirmed Lua conventions.
- Missing API localization is completed without changing business behavior; original paths retain their existing base and format.

# Verification

- Initial branch: develop.
- All six target Lua files already have uncommitted user modifications.
- Other pre-existing changes: .gitignore, .vscode/settings.json, LICENSE, README.md, runtime TOC.
- Verified with git check-ignore -v: the three archive paths are not ignored. The initial report incorrectly interpreted the directory-list output appended after cat .gitignore as ignore-file content.

- Pre-existing tracked changes were verified to be CRLF-only relative to HEAD. Preserve working-tree line endings and stage normalized LF task content to exclude those pre-existing changes.

- Six independent agents completed one Lua file each, scheduled in two batches within the concurrency limit.
- Verified all six files with the installed liblua5.4 syntax loader; this is a syntax check, not WoW runtime validation.
- Token comparison against the saved pre-task baseline allows only 12 new API/global-object cache declarations and the two panel call substitutions (math.max to max, string method gsub to cached gsub). All other executable tokens match.
- Checked required section order, exact namespace initialization, nonempty summaries/descriptions, trailing comments on every API/reference declaration, six unique preserved UUIDs, unchanged original/runtime_index/history, and preserved CRLF working-tree bytes.
- Reviewed descriptions against initialization order and shared-state access; mutable enable/burst state and delayed size initialization remain unchanged.
- API comments were checked on 2026-09-06 against /wow-ui-source revision 288f40d5cee5089223758d5810cb906ad34d4018. Evidence: Interface/AddOns/Blizzard_APIDocumentationGenerated/{SystemTimeDocumentation,ScreenDocumentation,UITimerDocumentation,CVarDocumentation,SpellDocumentation,CurveUtilDocumentation,LuaCurveObjectConstantsDocumentation,SimpleTextureBaseAPIDocumentation}.lua; Interface/AddOns/Blizzard_SharedXMLBase/Color.lua; Interface/AddOns/Blizzard_SharedXML/PixelUtil.lua.
- Special CVar writes retain their values; comments describe the write without claiming undocumented client support. No game-client execution was performed.

# Review Notes

- Frozen at 2026-09-06 06:58:56 UTC after the user explicitly replied “实施” to the final shared-understanding summary. Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria are frozen.
- User confirmed recommended choices for Q1–Q3: “Q1-Q3 按推荐来 . Q4我检查了.gitignore 没看到啊，在第几行”. Q4 was based on an incorrect interpretation of tool output and is withdrawn after verification; no ignore-rule change or force-add is needed.
- Interpret the repeated namespace initialization heading before API localization as api cache, consistent with the user's section list and files.

# Completion

Completed the six Lua documentation updates and the project Lua documentation convention. Existing modification-history entries are preserved; none were added.

The atomic local workflow commit contains the six Lua files, .spec/development-rules.md, and this task's plan, mean, and prompt archives. Original CRLF-only working-tree changes are retained and excluded from the commit; no external publication is included.

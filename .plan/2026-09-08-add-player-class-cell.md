# Goal

Add a first-row player-class Cell using the existing Lua architecture.

# Scope

Create phantom/lua/general/01_player_class.lua, add its TOC entry, and update the architecture and pixel protocol specifications. Preserve unrelated existing prompt edits.

# Decisions

- The user delegated directory naming; use general because it contains first-row general field implementations. Use 01_player_class.lua for the first field.
- GeneralCell means an ordinary Cell in row one, not a new type or registry. Use a local instance and the existing Cell API.
- File metadata: index: 1; uuid: 0536bd34-e377-4274-a7ae-b80455dd359a; original: general\01_player_class.lua.
- Coordinates are x=1, y=1. Encode select(3, UnitClass("player")) in all RGB channels divided by 255, with alpha 1. Missing classID means black (0).
- Create an independent local eventFrame using CreateFrame("Frame"); refresh on PLAYER_LOGIN and PLAYER_ENTERING_WORLD. Register construction in UIInitFuncs and refresh immediately after construction. Ignore refreshes before construction.
- Reuse runtime scaling, row counting, and background resizing. Load the new file after runtime files.
- Document the API signature, arguments, returns, restriction annotations, all 13 classes and supplied introduction versions; omit webpage navigation and image noise. Distinguish the supplied 12.1.5.69594 page from the locally checked 12.1.0.69587 source.
- No public API changes or other general fields. No runtime refactoring.

# Implementation Steps

1. Create confirmed workflow archives, following the required formats.
2. Add the Lua module with existing Chinese documentation and section conventions, API caches, local Cell, initializer, and event handler.
3. Append the module to the TOC; document general directory ownership and the first general field contract in the relevant specifications.
4. Run Lua syntax and temporary mocked lifecycle/geometry checks; review the diff.
5. Commit implementation and archives atomically on develop, excluding unrelated pre-existing changes.

# Acceptance Criteria

- Exactly one ordinary Cell at (1,1) is created through UIInitFuncs.
- Initialization and both events set RGB to classID/255, or zero when absent; alpha remains 1.
- Events before initialization are safe, and repeated events do not create more Cells.
- Existing size conversion, debug scaling, row count, and background width apply.
- Metadata, API comments, TOC entry and specifications match the confirmed decisions.

# Verification

- Local reference: /wow-ui-source revision 288f40d5cee5089223758d5810cb906ad34d4018, version 12.1.0.69587; checked 2026-09-08. UnitDocumentation.lua documents UnitClass; SystemDocumentation.lua documents both events. Blizzard FrameXML also uses select(3, UnitClass("player")).
- Planned checks: luac -p; temporary Lua mock for IDs 1–13, missing result, both events before/after initialization, no duplicate creation, row count and scaled geometry; TOC ordering and diff review.
- Game login, reload, world transitions and physical pixel rendering require manual WoW verification; container checks cannot establish these.

- Passed: luac -p phantom/lua/general/01_player_class.lua.
- Passed: temporary /tmp/phantom-player-class-check.lua executed 6 combinations of initial class/nil and screen/UI/debug scale, loading actual runtime 01, 04, 05 and 07 plus the new module. Both events covered all IDs 1–13 and nil; verified pre-init events, immediate initialization refresh, alpha, coordinates, size, background width, row count and no duplicate creation.
- The first mock run lacked WoW's global max alias used by existing runtime; adding max = math.max to the mock resolved the harness error without changing repository runtime code.
- Passed: every TOC path exists; the general module occurs once, after all runtime entries.
- Passed: targeted diff whitespace review with cr-at-eol, preserving the existing TOC CRLF convention. Unrelated prompt whitespace is excluded; the new prompt archive intentionally preserves source table trailing tabs.

# Review Notes

- Frozen: 2026-09-08 13:09:49 UTC. Confirmation source: native plan-to-implementation flow followed by user message "Implement the plan." Environment is now in Default mode.
- No archive writes were performed in Plan mode because its file-write restrictions took precedence. Archive collision check passed after confirmation; none of the three paths is Git-ignored.
- Existing unrelated edits: .prompt/2026-09-05-add-lua-foundation-directory.md, .prompt/2026-09-05-create-directory-skeleton.md, .prompt/2026-09-06-runtime-documentation.md. Exclude these from the commit.

# Completion

Implementation and container verification completed on 2026-09-08. All task files and workflow archives are included in the single local implementation commit on develop. No external actions were performed. Manual WoW validation remains unperformed; no game-runtime result is claimed.

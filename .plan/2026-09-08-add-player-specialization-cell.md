# Goal

Add the second general Cell displaying the player's specialization index using the established class Cell structure.

# Scope

Add phantom/lua/general/02_player_specialization.lua, its TOC entry, and the specialization field contract in .spec/pixel-protocol.md. Keep existing class output and rotation reload requirements unchanged. No new public interfaces.

# Decisions

- Use ordinary Cell at x=2, y=1; file header index: 2 and uuid: 154ab0be-9c33-4935-8e57-531eb6bde99e.
- Cache C_SpecializationInfo.GetSpecialization as local GetSpecialization, preserving local specializationIndex = GetSpecialization() in business logic without relying on deprecated global fallbacks.
- All RGB channels equal (specializationIndex or 0)/255; alpha is 1. Preserve numeric results including 5; nil renders black.
- Construct through UIInitFuncs after class initialization, immediately refresh, and use existing scaling, row counting, and background resizing.
- Independent local eventFrame listens to PLAYER_LOGIN, PLAYER_ENTERING_WORLD and ACTIVE_PLAYER_SPECIALIZATION_CHANGED, plus RegisterUnitEvent("PLAYER_SPECIALIZATION_CHANGED", "player"). Skip events before construction; subsequent events update the same instance.
- Follow existing Lua Chinese headers and sections. Paraphrase the requested Wiki API description with optional arguments, index/nil semantics, historical new-character value 5 note, and old/new API relationship. Include source link, date and pinned source revision; distinguish historical Wiki statements from generated API metadata.

# Implementation Steps

1. Create and freeze confirmed workflow archives after checking collisions and ignore status.
2. Add the specialization Lua module and load it immediately after the class module in the TOC.
3. Document the second general field and remove specialization from the undecided field candidates.
4. Run syntax, TOC and temporary mock checks using the real Cell, sizing and background runtime alongside both general fields.
5. Review and atomically commit all task files and archives on develop, excluding unrelated pre-existing prompt edits.

# Acceptance Criteria

- One Cell at (2,1) displays the returned specialization index as grayscale, including 5; nil yields black.
- All four events refresh after initialization; only player specialization unit events are registered. Pre-init events are safe and construction refreshes immediately.
- Class and specialization cells update independently; general row length is 2 and scaling/background geometry remain correct without duplicate creation.
- Metadata, comments, TOC and specification match the confirmed plan. No runtime refactoring or rotation hot switching.

# Verification

- Reference checked 2026-09-08: /wow-ui-source revision 288f40d5cee5089223758d5810cb906ad34d4018, version 12.1.0.69587. SpecializationInfoDocumentation.lua defines the namespaced API; UnitDocumentation.lua defines the specialization events. Deprecated_Specialization_Standard.lua defines the old alias only when loadDeprecationFallbacks is enabled; Blizzard_ClassSpecializationsFrame.lua uses player-filtered event registration.
- Requested Wiki page: https://warcraft.wiki.gg/wiki/API:GetSpecialization (retrieved through search after direct access returned 403). The historical nil/5 notes are not claimed as target-build game verification.
- Planned: luac -p, TOC ordering, mock indices 1–5/nil and all four events, player filtering, early events, independent Cell updates, normal/debug scale, row count and background width.
- Manual WoW login/reload/spec-switch/physical pixel validation cannot be performed in this container.

- Passed: luac -p phantom/lua/general/02_player_specialization.lua.
- Passed: /tmp/phantom-specialization-check.lua, 6 combinations of initial specialization/nil and physical-height/UI/debug scale. Actual runtime 01/04/05/07 and both general modules were loaded; tested 1–5/nil on all four events, pre-init events, immediate refresh, player-filtered registration and simulated dispatch, independent updates, both Cell positions, general length 2, background width and no duplicate creation. Deprecated global GetSpecialization was explicitly nil.
- Passed: TOC paths all exist, no duplicates, specialization follows class. Targeted diff whitespace check passed with cr-at-eol for existing TOC line endings.

# Review Notes

- Frozen at 2026-09-08 16:02:36 UTC. Confirmation source: user "Implement the plan." following the native plan flow; environment is in Default mode.
- Archive collision and ignore checks passed. Plan-mode write restrictions postponed archive creation until implementation authorization.
- Pre-existing unrelated changes in .prompt/2026-09-05-add-lua-foundation-directory.md, .prompt/2026-09-05-create-directory-skeleton.md and .prompt/2026-09-06-runtime-documentation.md are excluded.

# Completion

Implementation and container verification completed on 2026-09-08. This task is included in a single atomic local implementation commit on develop, with its specification and all three archives. Existing unrelated edits are excluded. No push or other external mutation. Manual WoW validation remains unperformed and no game-runtime result is claimed.

# Fix IconTile Background Layering

## Goal

Ensure idle casting IconTiles display opaque black instead of the DEBUG blue background.

## Scope

Fix the frame level in phantom/lua/runtime/09_icon_tile.lua and its explanatory comments. Preserve the existing coordinate correction and other working-tree changes.

## Decisions

- Use existing FrameLevel.Cell = 9600, above FrameLevel.Background = 9500, following Cell implementation.
- No new layer or change to 04_baseline_definition.lua is needed.
- Keep texture layers BACKGROUND, ARTWORK, and OVERLAY for black background, icon, and corner marker.
- Clear() continues hiding only icon and marker. No public API changes.

## Implementation Steps

1. After confirmation and leaving Plan mode, create matching workflow archives, record confirmation, and freeze this plan.
2. Change IconTile frame level from FrameLevel.Background to FrameLevel.Cell and update relevant comments.
3. Verify and make one atomic local commit containing only this fix and its archives. Stage task-specific hunks; exclude the earlier uncommitted coordinate correction and unrelated changes.

## Acceptance Criteria

- IconTile frame is explicitly above the shared background.
- Initialization and clearing retain an opaque black background.
- Casting and channeling retain existing icons and corner colors.
- Current positions and spacing remain unchanged.

## Verification

- Run Lua syntax validation.
- Extend temporary mock harness to capture actual frame levels and verify IconTile is above its parent, with opaque black texture retained after Clear(). Run existing casting-example regression checks.
- Game validation requires inspecting DEBUG idle state, cast/channel termination, and target removal. Mocks do not prove actual rendering; report game validation as unverified without an available game session.
- Completed: luac -p passed for the modified runtime; CRLF-aware whitespace check passed.
- Completed: /tmp/phantom-bar-icon-check.ZgrI9H/check.lua passed 699 assertions with actual baseline layer definitions and real ValueBar/IconTile implementations. Added checks for frame strata, IconTile above its parent, opaque black background retained at initialization and after Clear(), and unchanged texture layers. Existing casting, channeling, target loss, charge, and TOC checks passed.
- Actual game rendering remains unverified because no game session is available.

## Review Notes

- 2026-09-11 16:56:51 UTC: User confirmed shared understanding via "Implement the plan." after the native transition out of Plan mode. Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria are frozen.
- User authorized shared-layer changes if necessary; existing Cell layer provides the required ordering.
- Rechecked archive paths: no collisions. Index initially empty; earlier coordinate fix and unrelated working-tree changes will remain unstaged.

## Completion

Implemented and verified the IconTile frame-level fix. The atomic local commit contains only the single runtime layer/comment replacement and three matching workflow archives. Earlier coordinate changes and all unrelated working-tree changes are preserved outside the commit. No external actions or pushes were performed.

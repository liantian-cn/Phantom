## Goal

Remove phantom/core/condition/decoders.py so condition plugins read pixel objects directly in decode_value.

## Scope

Migrate all eleven existing @dev condition plugins, associated tests and current plugin documentation. Preserve parameters, output types, Lua encoding, pixel layouts and business results.

## Decisions

- Preserve strict grayscale and black/white validation inside each plugin, including existing fallback behavior (user selected the recommended option).
- Remove plugin decoder classes, self.decoder and generic decoder dependencies without introducing replacement wrappers.
- Keep PixelDecoder, Cell, ValueBar, IconTile and decode_value(..., *, decoder) interfaces.
- Keep each cooldown plugin's existing fixed points and interpolation formula locally.

## Implementation Steps

1. Read Cell.percent for health, Cell.ratio times maximum for power and Cell.mean with existing half-up rounding/range checks for runes.
2. Validate boolean cells then read is_white; state plugins retain same-frame coordinate reads.
3. Read ValueBar.ratio directly and retain charge scaling and half-up rounding.
4. Inline segment interpolation into both cooldown plugins using existing COOLDOWN_POINTS.
5. Delete the generic decoder module and its dedicated tests; cover business behavior through plugin tests.
6. Update system/plugin documentation and affected comments; preserve historical archives.
7. Run required checks and make one atomic local commit with implementation and workflow archives on develop.

## Acceptance Criteria

- Active code, tests and current normative documentation do not depend on the removed module.
- Eleven plugins directly express pixel reading, validation and business conversion.
- Valid values, damaged colors, boundaries, return types and fallbacks remain equivalent.

## Verification

Planned: full pytest, scripts/check_types.py, Ruff check and format --check. Cover grayscale, uniform colored cells, center pollution, black/white, rune bounds, charge rounding, cooldown nodes and intervals, same-frame reads and existing Lua/Python pairing. Record failures/skips honestly; offline verification is not game verification.

- Completed: pytest 403 passed, 5 skipped in 16.31s. Skips are existing symlink escape tests blocked by Windows privilege error 1314.
- Completed: scripts/check_types.py passed for ordinary modules and all versioned plugin entrypoints; Ruff check and format --check passed (phantom rotations tests demo scripts).
- Regressions cover strict rejection (including direct decode_value exceptions), uniform colored and mixed cells, state fallbacks, every cooldown brightness from 0 through 255, existing charge/rune boundaries, Lua/Python pairing and same-frame access.
- Active-source/current-documentation search found no removed decoder dependencies. Reviewed diff; no Lua, pixel implementation, configuration or unrelated file changes. Plugin metadata still describes unchanged business behavior and needs no edits.
- No game installation or game-input verification performed.

## Review Notes

- Frozen at 2026-09-14 08:20:51 UTC. Confirmation source: user message "Implement the plan." through the native Plan-to-implementation flow; environment is now Default mode.
- Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
- Archive collision check passed for all three paths. Initial working tree clean; branch develop.
- During interview the assistant incorrectly said delaying falls back to True, then corrected this from source to False before presenting the plan. Preserve actual existing fallbacks.

## Completion

Implementation and required verification completed successfully. All task implementation files, mean, plan and prompt archives are included in the single local commit for this task. No push. The commit containing this archive is the completion commit.

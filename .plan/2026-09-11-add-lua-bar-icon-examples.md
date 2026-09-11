# Add Lua ValueBar and IconTile Examples

## Goal

Add one spell-charge ValueBar and two casting IconTiles for subsequent decoding and plugin development.

## Scope

Create examples/06_spell_charges.lua, examples/07_player_cast.lua, and examples/08_target_cast.lua under phantom/lua/. Append them to phantom/lua/addonTemplateName.toc after example 05. Preserve runtime APIs, supplied spell IDs, and unrelated working-tree changes. Python decoding and plugin implementation are excluded.

## Decisions

- Follow Cell examples: existing Lua sections, Chinese business comments, original, literal {{uuid}}, sequential index, and uppercase local parameters first in logical code.
- Use independent event frames and UIInitFuncs; guard refreshes before construction and refresh immediately after construction. Use events without polling.
- Charges: comment name 血液沸腾 and type ValueBar; SPELL_IDS = {50841, 50842}, POSITION_X = 1, WIDTH = 2, REVERSE = false. Select the first spellbook match during initialization, PLAYER_ENTERING_WORLD, and SPELLS_CHANGED. Fix the range to 0..WIDTH; forward currentCharges directly to setValue. Missing selection or charge information means zero.
- Icons: comment type IconTile. Pass positions 1 and 2 directly to the existing constructor, accepting its current offset and left-side gap.
- Prioritize casting over channeling. Detect casting using return 11, delayTimeMs ~= nil; detect channeling using return 9, isEmpowered ~= nil, including false.
- Player casts use COLOR.SPELL_TYPE.PLAYER_SPELL; idle means Clear().
- Target absence or idle means Clear(). Ordinary nil interruptibility uses NOT_INTERRUPTIBLE; distinguish ordinary nil using issecretvalue. Otherwise pass the flag directly to EvaluateColorFromBoolean, mapping true to NOT_INTERRUPTIBLE and false to INTERRUPTIBLE.

## Implementation Steps

1. After authorization and leaving Plan mode, recheck collisions and create matching plan, mean, and prompt archives. Record confirmation and freeze agreed sections.
2. Implement charges using ValueBar:New, setMinMaxValues, and setValue. Register PLAYER_ENTERING_WORLD, SPELL_UPDATE_CHARGES, SPELL_UPDATE_USES, and SPELLS_CHANGED.
3. Implement both icons with RegisterUnitEvent for player or target. Register UNIT_SPELLCAST_ events with suffixes START, STOP, INTERRUPTED, FAILED, FAILED_QUIET, DELAYED, SUCCEEDED, CHANNEL_START, CHANNEL_STOP, CHANNEL_UPDATE, EMPOWER_START, EMPOWER_STOP, INTERRUPTIBLE, and NOT_INTERRUPTIBLE.
4. Register PLAYER_ENTERING_WORLD for both icons; additionally register PLAYER_TARGET_CHANGED and UNIT_TARGETABLE_CHANGED for target.
5. Document core API signatures, arguments, returns, secrecy restrictions, Wiki links, verification date, and local revision near caches. Describe SpellChargeInfo fields and casting/channeling return positions; record Wiki access failure honestly.
6. Append TOC entries, verify behavior, complete archives, and make one atomic task-only local commit on develop.

## Acceptance Criteria

- Charge counts 0, 1, and 2 produce empty, half-full, and full content with existing red separators.
- Spellbook changes replace or clear the selected spell immediately.
- Casting, channeling, and empowered channels display appropriate icons; ending or losing casts clears stale content.
- Target changes refresh immediately; ordinary nil interruptibility displays the non-interruptible color.
- Potentially secret charges, textures, and booleans reach supported rendering consumers without ordinary Lua inspection.

## Verification

- Run luac -p on the three examples; check TOC paths and order.
- Use a temporary Lua mock harness for candidate priority/removal, missing charge information, initialization guards, event registration, cast/channel precedence, false channel sentinel, target loss, true/false/nil interruptibility, and opaque-value forwarding.
- Mocks do not establish real WoW Secret Value compatibility. Actual rendering, combat restrictions, and event timing require game validation.
- Completed: individual luac -p checks passed for all three examples.
- Completed: /tmp/phantom-bar-icon-check.ZgrI9H/check.lua passed 325 assertions using the real ValueBar and IconTile runtimes with simulated WoW APIs. Covered candidate combinations and priority, reselection/removal, nil information, 0/1/2 charges, fixed maximum, initialization guards, required events and unit filters, no polling, casting precedence, false/true channel sentinels, target loss/replacement, true/false/nil interruptibility, and opaque-value forwarding. TOC paths and load order passed.
- Completed: existing TOC CRLF format preserved; whitespace check with core.whitespace=cr-at-eol passed. Game validation remains unperformed.

## Review Notes

- 2026-09-11 16:40:22 UTC: Shared understanding confirmed by user message "Implement the plan." after the native Plan-to-implementation transition. Goal, Scope, Decisions, Implementation Steps, and Acceptance Criteria are frozen.
- User selected direct IconTile positions 1 and 2; ordinary nil interruptibility is non-interruptible. This example positioning intentionally retains the existing gap rather than changing the general pixel-layout specification.
- Local API evidence checked on 2026-09-11: WoW 12.1.0.69587, revision 288f40d5cee5089223758d5810cb906ad34d4018. Wiki pages returned 403.
- Collision checks found no matching archives. No files were written during Plan mode.
- Existing unrelated working-tree changes must remain outside the task commit; the TOC had no pre-existing changes.

## Completion

Implemented the three examples and TOC integration. Available container validation passed; rendering, combat restrictions, and real event timing remain for game validation. The atomic success commit includes only the three new examples, TOC, and three matching archives. Unrelated pre-existing changes are preserved and excluded; no push or other external action is included.

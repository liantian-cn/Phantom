# Events and Performance

## Event-first rule

Prefer events to unrestricted `OnUpdate` work. Events identify when a condition may have changed; the plugin can then update only its assigned output. Use `RegisterUnitEvent` when the event supports unit filtering.

An `OnUpdate` handler is appropriate only when a display consumer or animation genuinely needs time progression. Throttle it to the required resolution and keep its body allocation-free.

## Generated-code implications

Phantom generates only the conditions referenced by selected rotations. Generated Lua should:

1. load shared primitives first;
2. return early from each UUID rotation file when class or specialization does not match;
3. register only events required by the active rotation;
4. update only affected regions;
5. avoid rebuilding tables, closures, curves, formatters, or frames on frequent events.

Static layout and plugin arguments are frozen during generation. Runtime code must not change output count or shift later regions.

## Useful lifecycle events

Choose the exact event from current source, but keep these lifecycle categories separate:

- addon initialization and saved state;
- player login or entering world;
- specialization or talent changes;
- combat lockdown transitions;
- unit-specific state changes;
- aura-container managed updates;
- post-combat work that was prohibited during combat.

Do not use event payloads as ordinary values when the current build marks them secret.

## Python loop

Each Python cycle captures the matrix, updates condition instances, evaluates the pre-parsed whitelist AST in rotation order, and sends at most one key. A cycle with no match sends nothing.

The loop frequency is intentionally undecided. Measure capture, decode, UI, and input costs before selecting it. A local microbenchmark showed that evaluating 30 small pre-parsed AST expressions at 10 Hz is negligible compared with image capture, so do not optimize the expression evaluator at the cost of clarity.

## Allocation and caching

- Reuse NumPy views when possible; make a contiguous copy only where byte-stable hashing requires it.
- Cache static layout, parsed ASTs, plugin descriptors, and Lua templates.
- Do not cache combat values beyond the plugin's explicit freshness contract.
- Avoid per-frame table creation in Lua and repeated parsing in Python.
- Keep diagnostics off the hot path or rate-limit them.

## Testing focus

Test mapping and boundary behavior: trusted crops, white-bar percentage, hash input, nonlinear encodings, fallback rules, AST validation, first-match rotation order, and key parsing. Do not spend tests on literal generated strings unless text itself is the contract.

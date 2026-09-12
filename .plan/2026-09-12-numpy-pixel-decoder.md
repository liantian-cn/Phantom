# Goal

Implement roadmap step 4: NumPy pixel decoding aligned with the existing Lua layout.

# Scope

Add PixelDecoder, Cell, ValueBar, IconTile, a timed Windows demo, algorithm tests, and relevant specification updates. Mark step 3 complete based on the user's successful test confirmation. Exclude Lua changes, condition formulas, TUI, and actions.

# Decisions

- Export the four classes from phantom.core.pixels; use decoder.py, cell.py, value_bar.py, and icon_tile.py.
- Decoder accepts the complete RGB uint8 board. getCell(x,y), getValueBar(x,width), getIconTile(x) use Lua arguments unchanged.
- Cell starts at (4*x,4*(y-1)), size 4x4; ValueBar starts at (4*x,8), size 4*(width+1) by 4; IconTile starts at (4+8*(x-1),12), size 8x8.
- Region constructors receive logical coordinates and already cropped arrays. Coordinates affect only location metadata.
- All computed and location interfaces are read-only properties. pos/region use board-relative pixels and exclusive bottom/right edges; strings are comma-separated without spaces or parentheses.
- Cell inner is [1:3,1:3]; mean averages RGB components, decimal divides by 255, percent multiplies decimal by 100. color_string uses the first inner RGB pixel. Purity requires equal RGB pixels; black/white are exact.
- ValueBar inner is [1:3,:]. ratio counts white/(white+black); percent is ratio*100. Other colors are excluded; empty denominator returns 0.0. No value or reverse interface.
- IconTile inner is [1:7,1:7]. Whole-inner black returns None; otherwise hash uses contiguous RGB bytes and xxh3_64_hexdigest seed 0, with instance _hash_cache. Purity compares all inner pixels.
- Regions own independent read-only snapshots. Decoder validates board shape and dtype, positive integer indices/width, Cell rows 1/2, and content bounds. Invalid requests fail explicitly.
- demo01.py waits 3 seconds, captures for 5 seconds, stops in finally, and reports the final result only. Errors never fall back to old frames. Report ten Cell means, one bar ratio/percent, and two tile hashes.

# Implementation Steps

1. Create confirmed workflow archives and add the typed pixel package and pinned xxhash dependency.
2. Add algorithm tests and the GDI demo; update minimum relevant Chinese specifications and roadmap.
3. Run pytest, mypy strict, Ruff lint/format checks, and the actual Windows game demo.
4. Record evidence and make one atomic local commit of task files and archives without pushing.

# Acceptance Criteria

- Identical Lua/Python inputs select identical regions, including red separators and adjacent icon slots.
- Requested properties return documented values from inner pixels only; cache remains stable if source arrays change.
- Tests cover edge contamination, exact colors, no valid bar pixels, black icons, non-contiguous arrays, multiple slots, invalid inputs, and location strings.
- All Python checks pass. Actual game output is recorded honestly; step 4 is complete only after game verification succeeds.

# Verification

Initial repository: develop, clean working tree, one existing commit ahead of origin/develop. All three target archive paths were absent and are not ignored. Windows reference files matrix.py and cell.py were inspected read-only.

- Windows Python 3.13.15, NumPy 2.5.3, xxhash 4.0.1: dependency installation succeeded.
- pytest: 49 passed, including 16 pixel tests and the existing 33 capture tests.
- mypy strict: success for all 19 Python source files.
- Ruff check and format --check: passed after sorting three new import blocks. git diff --check: passed.
- Actual GDI demo exited successfully: Cell row 1 means [6,1,255,0,0]; row 2 [255,0,0,0,255]; ValueBar(1,2) ratio=1.0, percent=100.0; IconTile(1) and IconTile(2) hash=None.
- Both live icon slots were black; non-empty hashes, whole-inner black detection, non-contiguous input, and hash-cache reuse were verified with synthetic images. No non-empty live icon claim is made.
- The command transport displayed garbled Chinese labels under its default Windows encoding; numeric output was intact. This did not affect image decoding.

# Review Notes

- Frozen on 2026-09-12 (Asia/Shanghai), confirmation source: native Plan-to-implementation flow followed by user message "Implement the plan." Environment entered Default mode before writes.
- User replaced proposed ValueBar.value with explicit percent and ratio properties; no value alias will be added.
- Confirmation timestamp recorded locally: 2026-09-12T09:50:03+08:00. The helper _region.py centralizes array ownership and location formatting; this follows the frozen snapshot and coordinate contract.

# Completion

Implementation, automated verification, and live game demo completed successfully on 2026-09-12. Roadmap steps 3 and 4 are marked complete with evidence and the live non-empty-icon limitation recorded. All task implementation, tests, specifications, and workflow archives are included in one local commit; no push or external-source changes.

# Goal

Establish Python 3.13 engineering and a standalone GDI capture worker.

# Scope

Implement roadmap steps 2 and 3 foundations, a placeholder rotations.main, shared capture contracts and image algorithms, gdi@1.0 and its demo. No Textual integration, other backends, plugin discovery, or Lua behavior changes. Keep DEBUG=true. Live game acceptance is deferred.

# Decisions

- pip requirements files with verified pinned versions; pytest, mypy and Ruff configured in pyproject.toml.
- Background thread, entire virtual desktop including negative coordinates, physical pixel coordinates.
- Constructor and set_fps default to 15; finite positive FPS, runtime updates. Future backends may ignore the requested limit.
- start/stop are idempotent; stop joins and preserves the last result; restart clears results and localization.
- Latest result only: independent contiguous uint8 RGB image or None, and has_error/description status. No frame backlog.
- Exact 4x4 checkerboard localization, colors (15,25,20)/(25,15,20); bounds include markers, height 20, width >=8 and divisible by 4. Ambiguous candidates are errors.
- Validate all four center pixels of eight calibration cells. Flash is uniformly black or white; no temporal alternation check.
- Lost geometry/markers triggers full search; calibration errors retain bounds and invalid image. Missing/ambiguous target yields None. GDI errors publish failure and end the run.
- Valid results have false/empty status. Missing target and validation failures are errors; idle/stop itself is not an error.
- FPS caps both search and regional capture, includes processing time, uses interruptible waits without catch-up.
- Demo waits 3 seconds, starts, waits 5 seconds, stops and saves latest result.npy without pickle when available plus UTF-8 result.txt, in a fresh ignored directory.
- Only meaningful image/business tests. Desktop smoke tests do not imply game acceptance.

# Implementation Steps

1. Create confirmed archives and Python package/tool foundation.
2. Implement shared typed contracts, NumPy localization/validation and latest-result thread worker.
3. Implement typed Windows GDI resource lifecycle and timed standalone demo.
4. Add full-image and image-sequence business tests, run checks and Windows demo.
5. Update relevant Chinese specifications and roadmap, record verification and atomically commit task files and archives on develop.

# Acceptance Criteria

- pip installation and python -m rotations.main work under Python 3.13.
- Standalone demo follows the confirmed timeline and saves final status/image accurately.
- Localization, validation, transitions and frame ownership satisfy Decisions; GDI resources and worker thread terminate cleanly.
- pytest, mypy and Ruff pass. Windows smoke results and unavailable live-game verification are distinguished.
- Lua remains unchanged and unrelated files are excluded from the commit.

# Verification

- Before implementation: develop, clean working tree; Python 3.13 and pip available; no archive collisions or ignore matches.
- Python 3.13.15: pip install -r requirements-dev.txt and pip check succeeded with the recorded dependency pins.
- pytest: 33 full-image, image-sequence and saved-array cases passed. Includes negative-origin coordinate translation, ambiguous/missing/DEBUG images, exact center calibration, Flash, relocation, error propagation, latest-result ownership, runtime FPS updates, stop/restart, and NPY round trips.
- mypy strict passed for all 11 Python source files under Windows and Linux target platforms. Linux target checking is static verification, not a Linux runtime test.
- Ruff lint and format checks passed for all handwritten Python files.
- python -m rotations.main ran successfully.
- Windows timed demo completed: three-second delay, five-second capture run, stop, then a fresh result directory with has_error=true and the missing non-DEBUG marker description. No NPY was written because no target was present.
- Direct Windows GDI smoke check passed: (1080,1920,3) desktop -> (20,32,3) region -> repeated region, uint8 contiguous arrays with independent storage, then resource release.
- No real game or physical multi-monitor acceptance was performed. Negative coordinates were exercised through image-driven tests. Lua DEBUG remains unchanged.

# Review Notes

- Frozen 2026-09-11 04:28:12 UTC. Confirmation source: user “Implement the plan.” after native Plan-to-implementation mode transition. Goal, Scope, Decisions, Implementation Steps and Acceptance Criteria are frozen.
- User confirmed keeping DEBUG=true and cannot run the game now; use proportionate available verification.
- The user interrupted and then requested “继续”; resumed the same authorized task with no frozen decision changes.
- Initial verification found a Python 3.13 forward annotation issue and Linux-target Windows ctypes annotations; both were corrected before final checks.
- Related-path metadata was finalized before the first commit. Desktop demo artifacts remain ignored and are excluded from the commit.

# Completion

Implementation and available verification completed. The task files and all three archives are included in one atomic local commit on develop. Roadmap step 2 is complete; step 3 implementation and desktop checks are complete, with live-game acceptance explicitly deferred by user instruction. No external repository, Lua behavior, push or publication changes.

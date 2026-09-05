# Goal

Initialize Phantom's documentation foundation and local third-party reference sources for a Chinese-first, AI-friendly World of Warcraft 12.1 combat automation project.

# Scope

- Refine the supplied project draft into a coherent set of Chinese project documents and structural guidance without creating application code or an application directory skeleton.
- Reorganize, condense, and clarify the existing `.context/` World of Warcraft addon knowledge base in English to avoid translation-induced technical errors.
- Reorganize, condense, and clarify the existing `.spec/` project rules.
- Create a Chinese `AGENTS.md` that routes future agents to the relevant context and specification files.
- Initialize the four specified third-party source repositories at their required absolute paths and branches, without disturbing existing local work.
- Preserve unrelated pre-existing user changes in `.gitignore`, `LICENSE`, and `README.md`.
- Keep the root `README.md` unchanged; place the complete project description in `.spec/project-overview.md` because the README is reserved for future end-user documentation.
- Shallow-clone each missing third-party repository at its specified branch; treat all four external repositories as read-only references after initialization and do not include them in the Phantom Git repository.
- Back up the 42 current `.context/` Markdown files outside the project tree, then replace them with approximately seven curated English topic documents.
- Use the confirmed eight-file Chinese `.spec/` structure and an `AGENTS.md` whose sole responsibility is routing and authority ordering.
- Commit only the task-owned documentation and workflow archives; exclude the pre-existing `.gitignore`, `LICENSE`, and root `README.md` changes, and never include external source checkouts.

# Decisions

- Project specifications, project structural guidance, and `AGENTS.md` created or rewritten by this task will be Chinese. `.context/` will remain English to avoid translation errors. This plan remains English because the governing Plan Protocol requires English.
- Development work is restricted to the `develop` branch; the repository is currently on `develop`.
- Existing uncommitted user changes must not be overwritten or included accidentally.
- The root `README.md` remains unchanged; the supplied draft becomes a layered specification set led by `.spec/project-overview.md`.
- The specification set separates project overview, architecture, pixel protocol, plugin protocol, configuration format, and development/testing rules so agents can read only relevant documents.
- `.context/` is curated around Phantom's needs: WoW 12.1 APIs, Secret Values, Aura, pixel-capable UI primitives, events and performance, and security restrictions. Unrelated general UI customization material is reduced to necessary summaries.
- Retained technical claims are cross-checked against the specified local source revision and version-change records. Unconfirmed claims are marked as requiring verification rather than made normative.
- Document bodies use Chinese except `.context/`; filenames and technical identifiers remain stable English ASCII.
- Missing third-party repositories are cloned through SSH with `--branch`, `--single-branch`, and `--depth 1`. The existing `/wow-ui-source` checkout and its local archival commit remain untouched.
- Third-party repositories are external read-only references after initialization and are not part of the Phantom repository.
- Before replacing `.context/`, archive its original contents outside the Phantom project directory. Consolidate it into an English entry index and approximately six topic documents covering WoW 12.1 changes, Secret Values, Aura, rendering primitives, events/performance, and security/API lookup.
- `.spec/` contains exactly `README.md`, `project-overview.md`, `architecture.md`, `pixel-protocol.md`, `plugin-system.md`, `configuration.md`, `development-rules.md`, and `testing.md`.
- Confirmed rules and unresolved design questions are separated. Each unresolved question appears explicitly under a Chinese `待定事项` section and is not normative; agents must not invent or enforce an answer.
- The supported knowledge and specification target is the WoW 12.1 release family. Volatile technical claims include their verification date and local source revision and must be rechecked for later 12.1 builds.
- Third-party reference repositories remain writable at the filesystem level but are governed as read-only: agents must not modify files, commit, change branches, fetch, pull, or reset unless the user explicitly requests an update.
- `AGENTS.md` is a concise router containing authority order, mandatory entry points, task-specific links, and only the few global rules necessary to route correctly. It does not duplicate specification bodies.
- Protocol-level decisions required for this documentation foundation are settled; intentionally unspecified implementation details are assigned to explicit future tasks.
- Configuration schema version 1 uses corrected `snake_case` field names and proper YAML arrays. Misspellings in the initial draft are not compatibility aliases.
- Macro definitions preserve a key-to-macro-text relationship. When binding is enabled, generated Lua creates an invisible `SecureActionButtonTemplate`, assigns its `macrotext`, and uses `SetOverrideBindingClick` to route the key to that button; it does not create a saved WoW macro-slot entry. When binding is disabled, the player selects an existing in-game key and the automation side sends that key without emitting secure-button or override-binding Lua for the entry.
- Pixel protocol documentation freezes the logical geometry, output modes, and purpose while isolating unspecified low-level color, sampling, validation, and hash details as non-normative pending items.
- Each of the four display rows is independently packed from left to right in declaration order; canvas width is the maximum occupied width of any row.
- A generated WoW addon package contains shared base modules and one Lua file per selected rotation, named from that rotation's UUID. Each rotation file checks its confirmed activation criteria before loading its remaining logic and returns early on mismatch. The generation UI permits selecting multiple rotations for one package.
- Plugin identifiers resolve exact versioned directories. Versions coexist without automatic fallback or upgrade; a shared configuration is expected to reference the tested exact version. Identifiers are case-sensitive lower-case snake_case plus the version, such as `health_pct@1.0`, `post_message@1.0`, and `gdi@1.0`.
- PySide6 is the only UI decision frozen in this task. The UI does not use the prior Terminal as its design reference; screens, interactions, and visual design remain pending for a later task.
- One YAML file represents one rotation and contains `schema_version`, `uuid`, `profile`, `conditions`, `macros`, and `rotation`. Numeric sequence IDs are removed.
- `conditions[].title` is a user-authored unique string and is the dictionary key referenced directly by `rotation[].condition`; it may be Chinese or English. `macros[].name` is the user-authored unique string referenced by `rotation[].macro`. These human-authored reference strings are distinct from `macros[].key`, which denotes a physical keyboard combination. The top-level macro collection is named `macros`.
- A condition title must be non-empty and unique within its rotation, may contain Chinese characters, English letters, and digits, and may not contain whitespace, comparison operators, parentheses, quotes, or equal the reserved words `and`, `or`, or `not`. The parser resolves exact registered titles.
- Condition values may be booleans, floating-point numbers, integers, strings, or lists. Expressions support `<`, `<=`, `>`, `>=`, `==`, `!=`, `and`, `or`, `not`, parentheses, `in`, and `not in`. The right operand of membership may be a compatible list returned by another condition, not only a list literal. Conditions are Python class instances stored as `conditions[title]`; the expression evaluator consumes each instance's decoded business value.
- Rotation entries are evaluated from top to bottom and the first true entry wins. Each cycle sends at most one key; if no entry matches, that cycle performs no action. “Pause” in the initial draft means this per-cycle no-action result, not a persistent runtime state.
- Schema version 1 removes `unit_talents`. Rotation activation and GUI exclusivity use only `unit_class` plus `unit_spec`; talent routing is a future pending feature.
- The generation UI presents rotations in a table whose first column contains selection checkboxes. Selecting a rotation automatically deselects any other selected rotation with the same `unit_class` and `unit_spec`; other class/spec combinations remain selected.
- Each UUID-named rotation Lua file checks class and specialization at addon load and returns early on mismatch. Changing specialization requires `/reload`; runtime hot-switching and future talent-aware routing are not part of this task.
- When `bind_key` is false, `key` is required, `macro_text` is optional and has no effect, and generated Lua emits no macro creation or key-binding code for that entry.
- When `bind_key` is true, `SetOverrideBindingClick` directly places a priority override on any existing action for the configured key without checking or warning. The persistent player binding is not rewritten. The user explicitly accepts the runtime override because configuration authors are expected to choose uncommon keys.
- Future business code uses English identifiers and Chinese business comments. Condition plugins receive a standardized header that records purpose, parameters, output type and dimensions, WoW API provenance, Secret Value risk, and version changes, in addition to the repository-wide required file documentation. Type hints are mandatory in every handwritten Python file for function and method parameters and returns, class and instance attributes, containers, and non-obvious local values. Obvious simple locals and loop variables need not be annotated; third-party and generated code are exempt.
- Loop frequency, throttling, and configuration remain pending; 10 Hz was only an example.
- Configuration key combinations use uppercase WoW-style hyphenated strings such as `ALT-NUMPAD1` and `SHIFT-F8`; the Python action plugin parses the same representation into Windows input.
- The generated addon package name is supplied by the user for each generation operation; name validation constraints remain pending.
- Each condition instance uses exactly one output mode (`cell`, `status_bar`, or `icon`) but may reserve multiple consecutive regions of that same mode. Its output contract separately declares `output_type`, `output_count`, `value_type`, and `value_shape`; the output count is computed after argument validation and remains fixed after layout. Multiple regions may combine into one scalar or decode into a list. For example, one cast icon returns one lowercase 16-character `xxh3_64_hexdigest`, while a ten-icon blacklist condition may return a list of zero to ten such hashes.
- The condition base class publicly exposes `raw_value()` and `value()`. `raw_value()` reads the instance's declared capture regions. `value()` calls the plugin's `decode_value(raw)` and returns the plugin's mandatory `fallback_value()` whenever decoding raises any exception. Plugins may also return their fallback proactively from `decode_value`. A plugin missing decoding or fallback implementations cannot be instantiated.
- `raw_value()` preserves capture facts: Cell RGB channels, Status Bar white-fill percentage, or Icon hash. Cell reading trusts only `array[1:3, 1:3]` from the 4×4 region. A Status Bar trusts only `bar_pix_array[1:3, :]`, counts pixels exactly equal to `(255, 255, 255)`, and returns `100.0 * white_count / total_count` or `0.0` for an empty inner region. Icon reading trusts only `array[1:7, 1:7]` from the 8×8 region; an all-black inner region yields `None`, otherwise it yields the lowercase 16-character `xxh3_64_hexdigest` of the contiguous inner array with seed zero. Multi-Icon raw results always have `output_count` entries and preserve absent slots as `None`.
- `value()` performs plugin-specific calculation, scaling, filtering, and fallback and must always return a value matching the declared type and shape. A plugin may remove empty icon slots or define a different business order; the core does not prescribe list ordering.
- Every condition plugin must define an explicit fallback rule; the base-class contract rejects a plugin that does not provide one. Examples confirmed by the user include treating an unreadable cooldown as ready and an unreadable target-existence state as nonexistent. Encoding and decoding transformations are versioned paired contracts between generated Lua and Python, including nonlinear ranges such as different Cell precision bands.
- Membership validation uses plugin declarations before execution: the right operand must be list-shaped, the left must be scalar-shaped, and element types must match without implicit string/number coercion.
- General-row candidate values currently include script enabled state, delay state, class, specialization, and combat state. The list and semantics remain pending rather than normative.
- The generated addon package name must match `[A-Za-z][A-Za-z0-9_]*`; its directory and `.toc` file use the same name.
- Condition titles follow Python-identifier-compatible rules: start with a Chinese character or English letter; continue with Chinese characters, English letters, digits, or underscores; contain no whitespace or operators; and avoid language-reserved words.
- Expression literals use Python spellings such as `True`, `False`, numbers, quoted strings, and lists.
- Rotation expressions use a whitelist AST evaluator. Configuration loading parses and validates expressions once; runtime evaluation reads `conditions[title].value()` and permits only the confirmed literal, comparison, membership, and Boolean nodes. Attribute access, subscription, calls, arithmetic, and all other nodes are rejected.
- Deferred to later protocol or implementation tasks: capture channel-order normalization, concrete general-cell fields, exact Cell and Status Bar encodings, loop frequency, full UI behavior, generated addon display metadata, and talent-aware rotation routing.

# Implementation Steps

1. Complete a repository and third-party-source inventory, then interview the user across the full decision frontier.
2. Freeze this plan after explicit user confirmation; create the matching mean and prompt archives.
3. Create the agreed Chinese project overview and structural guidance documents without changing the root `README.md`.
4. Consolidate `.context/` into the agreed English knowledge structure while preserving required facts and provenance.
5. Consolidate `.spec/` into the agreed Chinese rule structure with clear authority and routing.
6. Create the root Chinese `AGENTS.md` and link it to the appropriate specifications and context.
7. Initialize or verify third-party source repositories using the agreed non-destructive policy.
8. Validate document links, language, structure, Git scope, repository branches, and source availability.
9. Record verification and completion evidence, then create one isolated atomic local commit for repository files.

# Acceptance Criteria

- `.spec/` contains the eight confirmed files and `.context/` contains the confirmed English entry index plus approximately six curated topic files.
- All agreed specification and agent-guidance documentation is written in Chinese; `.context/` remains English and workflow archives follow their governing language rules.
- `.context/` provides concise, navigable, project-relevant World of Warcraft 12.1 addon knowledge with explicit source precedence.
- `.spec/` provides concise, unambiguous, navigable project rules.
- Root `AGENTS.md` tells agents which documents to read for each kind of task and establishes their authority order.
- Each required third-party source exists at its specified absolute path and is checked out to the agreed branch without loss of local work.
- Existing unrelated user changes are preserved and excluded from the task commit unless explicitly authorized.
- Documentation links and repository-state checks pass.

# Verification

- Initial inventory on 2026-09-05: project branch is `develop`; `.gitignore`, `LICENSE`, and `README.md` have pre-existing modifications; `.context/` and `.spec/` are untracked.
- Initial inventory on 2026-09-05: `.context/` contains 42 Markdown files totaling approximately 15,302 lines; `.spec/` contains 3 Markdown files totaling 187 lines.
- Initial inventory on 2026-09-05: `/wow-ui-source` exists on `ptr` and is one commit ahead of `origin/ptr`; `/PhantomProject`, `/Shigure`, and `/midnight` are absent.
- Initial inventory on 2026-09-05: all four requested remote branches are reachable with the configured SSH credentials.
- Initial inventory on 2026-09-05: `/wow-ui-source` has no uncommitted changes; its additional local commit archives that checkout's own plan, mean, and prompt workflow files and must not be discarded.
- Initial inventory on 2026-09-05: the root `README.md` and `LICENSE` diffs are line-ending-only; `.gitignore` also removes the generic `*.spec` ignore rule and adds `提示词`.
- 2026-09-05 local source check at `/wow-ui-source` revision `a89e9d0c` confirmed current secure override-binding pathways, while exact protected-state timing remains an implementation-time verification item.
- 2026-09-05 source check of the user-referenced M.I.D.N.I.G.H.T `12.0` `DejaVu/DejaVu_DeathKnight/Blood/Macro.lua` confirmed the intended `SecureActionButtonTemplate` plus `SetOverrideBindingClick` implementation and hyphenated key examples such as `ALT-NUMPAD1`.
- 2026-09-05 source check of the user-referenced M.I.D.N.I.G.H.T `12.0` `Terminal/terminal/pixelcalc/cell.py` confirmed 4×4 Cell inner cropping with `[1:3, 1:3]`, 8×8 icon inner cropping with `[1:7, 1:7]`, and seeded `xxh3_64_hexdigest` over a contiguous NumPy array.
- 2026-09-05 source check of the user-referenced M.I.D.N.I.G.H.T `12.0` `Terminal/terminal/pixelcalc/matrix.py` confirmed Status Bar cropping with `[1:3, :]`, exact white-pixel counting, and a `0.0`–`100.0` percentage result.
- 2026-09-05 local microbenchmark: a simple whitelist AST walker evaluated 30 representative pre-parsed expressions in approximately 29.9 microseconds per cycle; at 10 Hz this is about 0.30 milliseconds of CPU time per wall-clock second on the current container. The result supports AST evaluation as negligible relative to capture and image processing, but is not a production performance guarantee.
- Final verification will be recorded during implementation.
- 2026-09-05 final structure check: `.context/` contains exactly the seven confirmed Markdown files (365 lines), `.spec/` contains exactly the eight confirmed Markdown files (589 lines), and the root router is `AGENTS.md`.
- 2026-09-05 archive check: the external backup contains all 42 original Markdown files and matches SHA-256 `cd9137d4c6922c37e7fdf1b528c9113944b42c7bd8905567fe384bb57f7eeb54`.
- 2026-09-05 documentation check: all local links in `AGENTS.md`, `.spec/`, and `.context/` resolve; every specification contains an explicit `待定事项` section; all `.context/` documents contain no Han characters.
- 2026-09-05 configuration check: PyYAML 6.0.3 parsed the embedded schema v1 example successfully; the expected top-level fields, RFC 4122 UUID, arrays, Boolean values, macros, and rotation-entry shape were verified. The parser was installed only in a temporary `/tmp` directory, which was removed after validation.
- 2026-09-05 source check: `/PhantomProject`, `/Shigure`, and `/midnight` are clean shallow single-branch checkouts at the confirmed revisions; `/wow-ui-source` remains clean on `ptr`, one unchanged local archival commit ahead of `origin/ptr`.
- 2026-09-05 source-path check: all local files cited for AuraContainer, Secret Values, restricted execution, pixel crops, Status Bar decoding, hashing, and macro binding exist; the cited historical implementations contain the documented operations.
- 2026-09-05 archive-format check: the prompt archive has exactly the required `Primary` and `Question` top-level sections and balanced evidence fences. Original trailing whitespace is intentionally preserved inside quoted user messages; `git diff --check` passes for every task file outside that evidence archive.
- 2026-09-05 commit-scope check: the staged set contains only `AGENTS.md`, the seven `.context/` files, the eight `.spec/` files, and the matching plan, mean, and prompt archives. Pre-existing `.gitignore`, `LICENSE`, and root `README.md` modifications remain unstaged.

# Review Notes

- 2026-09-05: Draft created from the user's `/init` request; shared-understanding interview is not yet complete and the plan is not frozen.
- 2026-09-05 08:20:53 UTC: Interview round 1 settled the delivery boundary, layered specification approach, English `.context/` exception, Phantom-focused context scope, fact-checking policy, ASCII filenames, unchanged root README, and shallow-clone policy. The user emphasized that small translation errors can accumulate into major errors.
- 2026-09-05: Interview round 2 settled context backup and consolidation, the eight-file specification map, explicit non-normative pending sections, WoW 12.1-series targeting, policy-only read-only treatment of third-party sources, and a routing-only `AGENTS.md`.
- 2026-09-05: Interview round 3 settled schema naming/versioning, macro-to-key intent, logical pixel protocol scope, independent deterministic row packing, a shared generated addon containing UUID-named rotation files, exact plugin versions, and PySide6 as the sole current UI constraint. The user explicitly rejected using Terminal as a UI reference.
- 2026-09-05: Interview round 4 settled one-YAML-per-rotation, unique Chinese condition-title lookup, ordered first-match execution, per-cycle no-action semantics, class/spec UI exclusivity, optional inactive macro text when binding is disabled, direct overwrite behavior when binding is enabled, and Chinese standardized plugin documentation. During this round the user withdrew talent-based rotation differentiation, superseding the earlier class/spec/talent activation design; affected talent and reload branches remain open.
- 2026-09-05: Interview round 5 removed `unit_talents` from schema version 1, clarified title/name/key roles, constrained condition titles, added list membership to the expression language, settled load-time class/spec activation and GUI checkbox exclusivity, left loop frequency pending, and replaced the earlier persistent-binding assumption with invisible secure action buttons and runtime override bindings. The user's earlier requirement for plus-separated uppercase keys conflicts with the later selection of hyphenated WoW-style keys and remains open.
- 2026-09-05: Interview round 6 resolved the key format as uppercase hyphenated WoW syntax, confirmed plural `macros`, UUID filenames, specialization indexes, lower-case snake_case plugin identifiers, a user-supplied generated package name, multi-region same-mode condition outputs, scalar-or-list condition results, and candidate general cells. The condition-list model superseded the proposed literal-only membership rule.
- 2026-09-05: Interview round 7 settled the condition instance's end-to-end Lua/capture/value responsibility, four-part output descriptors, instance-time fixed output counts, declared membership typing, mandatory plugin-specific non-null fallbacks, plugin-defined business list ordering, safe generated package names, and continued deferral of general Cell fields. This superseded the proposed universal `None` business value.
- 2026-09-05: Interview round 8 settled the base-class template flow, normalized Status Bar raw values, trusted inner Cell/Icon crops, fixed-length raw Icon lists, catch-all decode fallback behavior, Python-compatible condition titles, and Python-style literals. Expression execution remains open pending the requested performance explanation.
- 2026-09-05: After reviewing a local microbenchmark, the user selected pre-parsed whitelist AST evaluation. The design-tree frontier is empty; intentionally unspecified implementation details are explicitly deferred rather than treated as open decisions.
- 2026-09-05: The user selected `Revise` at the final shared-understanding confirmation. The plan remains a draft and no implementation is authorized; the revision target has not yet been identified.
- 2026-09-05: The user revised Status Bar decoding to use the middle two rows and exact white-pixel percentage, superseding the prior normalized `0.0`–`1.0` decision, and added mandatory Python type hints. Type-hint enforcement depth remains the only open affected branch.
- 2026-09-05: The user selected mandatory type hints across all handwritten Python files, with the recommended coverage for signatures, attributes, containers, and non-obvious locals. The revision frontier is now empty; the plan remains a draft awaiting renewed final confirmation.
- 2026-09-05 10:04:35 UTC: The user confirmed the revised shared-understanding summary with the message `Confirm`. `Goal`, `Scope`, `Decisions`, `Implementation Steps`, and `Acceptance Criteria` are frozen and implementation is authorized.
- 2026-09-05 10:29:13 UTC: Implementation completed without creating application code or changing the root `README.md`. The original prompt whitespace remains verbatim by protocol, so the prompt-only whitespace warnings are documented rather than normalized.

# Completion

Implementation authorized; completion evidence will be appended after verification.

- Documentation foundation completed: Chinese specifications and routing, English curated WoW context, and workflow evidence archives are ready.
- External reference initialization completed without modifying the existing `/wow-ui-source` worktree.
- The original 42-file context set is recoverable from `/workspaces/phantom-5796e240-context-original-20260905.tar.gz` using the recorded checksum.
- No business code or empty application skeleton was created in this task.
- One isolated local success commit will record the verified repository-owned files; no push or other publication is authorized.

# Phantom WoW Addon Context

This directory is a compact, English-language knowledge base for Phantom's World of Warcraft 12.1 addon work. It is informative, not normative. Project requirements live in [`.spec/README.md`](../.spec/README.md).

## Snapshot

The material was consolidated on 2026-09-05 and checked against these local references:

| Reference | Branch | Revision | Primary area |
| --- | --- | --- | --- |
| `/wow-ui-source` | `ptr` | upstream `a89e9d0c` (Build 69587); local archival commit `288f40d5` | Current FrameXML and generated API documentation |
| `/PhantomProject` | `develop` | `f6935113` | Earlier experimental Lua and Secret Value patterns |
| `/Shigure` | `main` | `b73d242f` | Alternative addon structure and Lua patterns |
| `/midnight` | `12.0` | `12c7fba9` | Windows capture, matrix decoding, rotations, and secure-button macros |

These repositories are read-only references. Do not modify, fetch, pull, reset, switch branches, or commit in them unless the user explicitly requests an update.

The 42 pre-consolidation Markdown files are preserved outside the project at `/workspaces/phantom-5796e240-context-original-20260905.tar.gz` with SHA-256 `cd9137d4c6922c37e7fdf1b528c9113944b42c7bd8905567fe384bb57f7eeb54`.

## Reading map

| Task | Read |
| --- | --- |
| Check a 12.1 change or volatile API | [`wow-12.1-changes.md`](wow-12.1-changes.md) |
| Handle combat-derived or Secret Values | [`secret-values.md`](secret-values.md) |
| Display or filter auras | [`aura.md`](aura.md) |
| Build frames, textures, bars, icons, or secure buttons | [`rendering.md`](rendering.md) |
| Choose events or optimize update work | [`events-performance.md`](events-performance.md) |
| Check taint, combat restrictions, or an API signature | [`security-api.md`](security-api.md) |
| Look up the Flexoki color values used by the TUI | [`flexoki.md`](flexoki.md) |

## Evidence order

For project behavior, `.spec/` is authoritative. For WoW technical facts, use this order:

1. The generated API documentation and implementation at the pinned `/wow-ui-source` revision.
2. The archived version-change records for chronology and removed or renamed contracts.
3. Third-party reference projects for tested patterns, never as proof of the current API.
4. Primary online sources only when local evidence is insufficient or the task explicitly requests an update.

If sources disagree, do not silently choose one. Record the build and revision, mark the claim as unverified, and keep it out of normative project rules until resolved.

## Update discipline

- Treat all combat, unit, aura, spell, cooldown, target, threat, and nameplate values as potentially secret until the current build proves otherwise.
- Recheck volatile claims whenever the 12.1 build or `/wow-ui-source` revision changes.
- Keep examples small and project-relevant. Do not rebuild a general WoW addon tutorial here.
- Preserve API names, enum names, paths, and code in English; accuracy is more important than translation.

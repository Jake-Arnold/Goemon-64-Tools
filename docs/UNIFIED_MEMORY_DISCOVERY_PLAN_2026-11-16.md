# Unified Memory Discovery and Toolkit Redesign

**Date:** 2026-11-16  
**Status:** Approved for an isolated, reviewable test prototype; full release and tracing scope not yet accepted  
**Base:** Toolkit v0.11.31 on `main`  
**Branch:** `toolkit/unified-memory-discovery`  
**Platforms:** Native Linux and Windows  
**Regions:** USA and Japanese retail revision 0  
**Preferred runtime:** native Goemon recomp; emulator adapters retained

## 1. Objectives and hard constraints

Build one cohesive toolkit with a persistent USA/Japan selector, coherent game connection and region-specific guest-memory validation, readable discovery workflows, real original-instruction read/write tracing *when a capable runtime is available*, and first-class saved reports.

- Preserve scene browsing, warps, practice controls, checkpoints, unlocks, Live Memory, freezes, autosplitter interfaces and user data until independently tested.
- Linux must not depend on Wine; Windows must use the same workflows and report schema.
- Read-only experiments must not silently enable writes. No candidate address becomes a writable confirmed field without independently validated meaning and permissions.
- A memory snapshot can establish a changed value; it cannot establish the instruction that read or wrote the value. Clearly distinguish this throughout the UI/reports.
- Do not merge decompilation branch histories or commit ROM files, proprietary tools, savestates, full raw memory dumps or private machine diagnostics.

## 2. Proposed interface

Keep a globally visible game version (USA/Japan), backend, connection and PID status. Aim for unclipped core actions at 1220×790 and a functional 960×640 minimum.

Target primary navigation:

1. **Dashboard** — connection, health, selected ROM/version and quick actions.
2. **Game Controls** — scene browser, checkpoints, unlocks, progress and practical controls.
3. **Live Memory** — unified field/watch table, custom watch, editing and freezing; region-specific addresses remain distinct.
4. **Memory Discovery** — guided A/B/C experiments, value search, automatic damage/events, access tracing and trial history.
5. **Reports** — indexed investigations, recent results, open folder, open summary, copy path, portable export.
6. **Settings** — advanced connections, reports location, tracing and tools.

The prototype may retain existing Game Controls/Live Memory tabs and migrate one section at a time. It must not add another permanently redundant front page.

UX: clean hierarchy, consistent button labels, scrollable body, responsive controls, advanced settings collapsed, no confirmation for read-only operations, understandable disabled controls, no dead-end actions, errors with actionable diagnostics. Preserve keyboard navigation and GNOME/Windows launcher identity.

## 3. Shared application model

Introduce common, testable components:

- `GameSession`: version, PID/start token, executable/backend, verified ROM, guest-memory layout, connection lifecycle.
- `MemoryReader`: canonical big-endian guest reads at N64 addresses regardless of host layout.
- `DiscoveryEngine`: scanning, A/B/C capture, repetitions, control trials, candidate ranking, cancellation.
- `AccessTracer`: optional bounded guest-instruction access events, capability reported at runtime, not assumed.
- `FieldRegistry`: per-region candidates, known fields, provenance, validation level.
- `ReportManager`: consistent directory, manifest, data formats, versioning and legacy report discovery.

Disconnection, PID reuse, region switch, ROM change and savestate load invalidate session-bound capture/trace state. Do not treat USA and Japan memory layouts as interchangeable.

## 4. Memory Discovery workflows

### Guided discovery

Choose a template (movement/position; character change; HP/damage; inventory/currency; unlock/story flag; dialogue; scene transition; custom). The app explains each capture: A baseline; B perform action; optional C reverted/settled; optional idle/control and repeated trials. Capture region/character/scene context and timestamp; avoid requiring gameplay pointers in menus and cutscenes.

### Value search

Retain exact/unknown and increased/decreased/changed/unchanged filtering; support signed/unsigned integers, f32, bit masks, greater/less than, aligned/unaligned modes. Provide candidate count, last values, add watch, rename, explain evidence, trace reads/writes (only when available), save report. Background scans remain cancellable and do not block Tk. Rows hidden by a display limit must be disclosed in reports.

### Automatic events

Unify damage-triggered recording and persistent event-flag sessions into experiment templates, retaining their distinct algorithms and presets. Read-only by default; repeat events and control trials to rank false positives.

### Address tracing

Select guest address/range and read/write/both. Record (where supported) original MIPS PC, decoded instruction, guest address, width, access type, value, scene/character context, timestamp, register context when available, source function/overlay if resolved, hit counts and drops. Include pause/resume/stop, filter, grouping, buffer bounds, session identity, error and completeness indicators.

Never label external process RAM polling as original-instruction access tracing.

## 5. Native recomp tracing feasibility — separate gate

First validate on **known** guest addresses that an instrumented native recomp reports actual reads and writes with the original MIPS instruction PC, rather than a generic native helper site.

1. Audit N64Recomp codegen and runtime guest load/store paths for USA and Japan; identify incomplete/bypassing paths.
2. Add an opt-in instrumented research build separate from production performance builds.
3. Make watchpoint filters narrow and overhead bounded; preserve correct guest RAM byte order and CPU address provenance.
4. Expose events through a local, versioned, authenticated-by-session communication channel, portable to Linux and Windows.
5. Distinguish access events initiated by original game code from external toolkit writes.
6. Prove original guest PC, access direction, width, values and context on known fields in both regional builds.
7. Benchmark overhead, count dropped events and fail closed on incompatible versions.

Only after evidence succeeds should live original-MIPS read/write tracing be offered as a working feature. Emulator debugger integration may serve as an independent validation backend, not a Linux dependency.

## 6. Candidate evidence and cross-region mapping

Rank support using expected value change, unaffected control trials, reversal to baseline, repetitions and plausible groups (XYZ vectors, bitfields, pointers). A verified MIPS access is a separate type of evidence. Resolve function/section/overlay and, when independently established, correlate USA and Japanese functions. Never apply a universal constant USA-to-Japan offset.

Evidence statuses: **hypothesis**, **repeated-support**, **instruction-traced**, **function-linked**, **gameplay-verified**. Each report records raw values/context and explains why the status applies. No automatic promotion into memory editors, freezes or warps.

## 7. Reports and files

Default root, with configurable override:

- Linux: `~/Documents/Goemon Practice Toolkit/Reports/` (honour XDG Documents where configured).
- Windows: `Documents\Goemon Practice Toolkit\Reports\` (honour resolved Windows Documents location).
- Do **not** write new reports into `practice/` or the source checkout.

Directory naming: `Reports/<USA|JP>/YYYY-MM-DD_HHMMSSZ__<safe-experiment-slug>__<short-id>/`.

Files: `summary.md` (human-readable); `candidates.csv`; `accesses.csv` (only when applicable); `session.json` (machine-readable); `manifest.json` (schema/version, region, identity and completeness without sensitive host details). Index only completed reports; never overwrite existing sessions.

Provide Open Reports Folder, Open Latest/Selected Summary, Copy Path and Export ZIP. Allow browsing existing legacy `diagnostics/*.json` without deleting or rewriting them, then offer explicit import/migration if useful.

Use consistent UTC timestamps, no unsafe path characters and safe uniqueness. Report truncation/sample coverage; avoid claiming that limited rows contain all candidates.

## 8. Redundancy audit (initial findings, not deletion approvals)

| Component | Evidence | Intended disposition |
|---|---|---|
| Value Search tab | Existing `practice/value_search_ui.py` | Retain algorithm; consolidate under Discovery |
| Event Sessions + nested A/B/C | `practice/event_sessions_ui.py`, `practice/state_discovery_ui.py` | Retain distinct algorithms; unify entry point |
| Automatic Events | `practice/damage_event_capture_ui.py` | Retain damage recorder; integrate as Discovery template |
| Japan Live diagnostic tab | `practice/japanese_fields_ui.py` | Eventually fold region-specific read-only watches into Live Memory |
| Separate USA/JP custom watches | `ui_extension.py`, `japanese_fields_ui.py` | Shared controls; preserve region-isolated saved data |
| Native debug calibration / character cursor | Functions defined in `ui_extension.py` | Inspect direct callers/tests; Advanced discovery or retire only if provably unused |
| Logical checkpoint card | Constructed and `pack_forget()` in `toolkit.py` | Audit compatibility and saved data first |
| Japanese room XYZ capture button | Hidden by `configure_scene_browser_region()` | Candidate for UI retirement only after call-site audit |
| Scene descriptions | Older initial labels conflict with current 0x0C Japan behavior | Correct obsolete text |
| Exporters and storage | Multiple independent `diagnostics_dir()` writers | Centralize via ReportManager incrementally |
| `practice/paths.py` | Source checkout is default report location for non-frozen toolkit | Migrate new reports out of checkout |

Classification: keep, consolidate, advanced, retire, preserve for compatibility. No deletion before reachability, tests, command-line options and saved-data consumers are reviewed.

## 9. Phases and acceptance gates

| Phase | Deliverable | Gate |
|---|---|---|
| 0 | Baseline audit and data compatibility inventory | Review before destructive cleanup |
| 1 | Native recomp trace feasibility prototype | Proven original instruction read/write events on known addresses |
| 2 | ReportManager, paths/names, Report Library | Linux/Windows tests, no repo output by default |
| 3 | Unified Discovery navigation / reuse existing engines | Existing user flows remain functional, GUI regression |
| 4 | Guided A/B/C templates and multi-trial evidence | Reproducible USA and JP capture/report scenarios |
| 5 | Instrumented native tracing integration | Real traces from both regional recomp builds |
| 6 | Correlation, function/overlay linking, USA↔JP mapping | Evidence survives exports and repeated trials |
| 7 | Approved redundancy cleanup, packaging and release | Linux + Windows CI and live gameplay acceptance |

The **first test build** is deliberately narrower: implement Phase 2 and a low-risk Phase 3 prototype; upload this plan and the detailed audit, reorganize existing value/event research under one Discovery navigation tab, add a usable cross-platform report browser, and create a report from Value Search. No claim of native instruction tracing until Phase 1 passes.

## 10. Tests and release controls

Run synthetic unit and Linux Tk tests; add Windows-compatible headless file/path tests. Test both regions, byte order, 4/8MiB layout, process restart/PID reuse, session changes, exporter data hygiene, collision-safe filenames, legacy diagnostics, GUI resizing/scrolling, selection navigation and optional file-manager invocation.

Live acceptance covers USA + JP native recomp attachment, known and unknown value scans, real read/write MIPS-PC traces, repeat/control trials, opening reports, export/re-import, reconnect and four characters where relevant. Distinguish live results from mock tests. Do not break game input, 0x0C scene reload, checkpoints, unlocks, pauses or freezes.

Every user-facing toolkit commit bumps `practice/version.py`, the README heading and `PROGRESS.md`. Use `main` only after review; no ROMs or user data in commits. Test/prototype scope and unsupported capabilities must be prominently labelled.

# Toolkit redundancy and usability audit — 16 November 2026

**Baseline:** main v0.11.31. **Status:** Initial source audit; no feature deletion authorised.  
**Plan:** UNIFIED_MEMORY_DISCOVERY_PLAN_2026-11-16.md

## Source-backed findings

| Component | Evidence | Disposition |
|---|---|---|
| Value Search | practice/value_search_ui.py, value_search.py | Keep scanner, consolidate under Memory discovery |
| Automatic Events | damage_event_capture_ui.py | Keep read-only damage recorder, consolidate |
| Event Sessions | event_sessions_ui.py | Keep persistent event trials, consolidate |
| Advanced A/B/C RAM comparison | state_discovery_ui.py already nested in Event Sessions | Preserve algorithms, later unify capture/session model |
| Japan Live diagnostics | japanese_fields_ui.py | Preserve for now; eventual region-aware Live Memory integration |
| Separate USA/JP watch storage | ui_extension.py and japanese_fields_ui.py | Preserve saved data; unify controls only after migration strategy |
| Native menu calibration | ui_extension.py defines build_debug_calibration_tab; not called in toolkit.__init__ | Audit callers/tests, then advanced or retire |
| Character cursor scan | ui_extension.py defines build_character_cursor_tab; not called in toolkit.__init__ | Audit callers/tests, then advanced or retire |
| Hidden logical checkpoints | toolkit.py constructs card then calls pack_forget | Preserve persisted states and restore APIs pending full audit |
| Hidden Japanese room XYZ capture button | configure_scene_browser_region calls pack_forget for both regions | Candidate for UI retirement, not writer removal |
| Obsolete scene text | Initial scene/browser labels still mention old JP debug menu; region refresh corrects them | Correct old initial strings later without changing actual warp mechanism |
| Non-frozen report location | practice/paths.py diagnostics_dir uses source practice_data_dir | New reports must use Documents, legacy files remain discoverable |
| Distributed report exporters | inspector, transition, native watch, cursor, damage, events write separate JSON | Migrate incrementally and maintain historical formats |

## Prototype scope

- One Memory discovery top-level tab nests Value search, Automatic events, and Event sessions. Existing Advanced RAM comparison remains inside Event sessions.
- One Reports tab indexes both the new report manifest format and old diagnostic JSON.
- New Value Search report export: Markdown summary, CSV, JSON, manifest; UTC region-specific names; honest truncation/evidence warning.
- Open Reports Folder, Open report, Open containing folder, Copy path, Export ZIP.
- OS-appropriate openers for Linux and Windows; no Wine.
- No changes to scene warp writers, freezes, unlocks or game regions.

## Cleanup gates

1. Inventory callers/tests/saved profiles for uncalled calibration and cursor builders.
2. Establish backwards compatibility for old saved sessions, bookmarks and reports.
3. Unify capture models, evidence metadata and region-correct watch persistence.
4. Remove only code demonstrated unreachable with no external consumer.
5. Confirm Linux and Windows GUI regressions, including window resizing.
6. Prove native recomp original-MIPS-PC read/write tracing separately before exposing live tracing controls.

**Outside this first prototype:** native recomp tracing, function/overlay mapping, full guided experiments, complete Japan Live consolidation, bulk old-exporter migration, real-game verification.

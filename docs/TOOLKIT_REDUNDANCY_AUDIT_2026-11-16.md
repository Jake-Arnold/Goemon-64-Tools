# Toolkit redundancy audit — 16 November 2026

**Current scope:** `toolkit/unified-memory-discovery` v0.11.36 test build.
**Baseline:** the previous v0.11.35 prototype. This is a source-level UI and data-flow audit, not a claim of completed live native-recomp acceptance.

## Disposition matrix

| UI or code area | Source evidence | Decision |
|---|---|---|
| Separate **Japan Live (diagnostics)** top-level tab | `practice/japanese_fields_ui.py` repeats region-aware `Live memory` watches, scene/debug actions and memory baselines. | **Hide the extra top-level page** for both USA and JP. Keep the backing field and watch-model objects for compatibility. Remove periodic hidden table polling. |
| **Japan custom watches** on old diagnostics page | `JapaneseFieldsUi.add_japan_custom_watch` persists `japan_0_custom_watches.json`. The shared inspector already reads and edits the same stored entries. | **One user-facing Live Memory tab.** Keep the existing persisted JP file and the backing data model; do not migrate/delete user watches. |
| **Goemon XYZ manual position editor** | The sole bounded, confirmed-scene manual position controls were constructed on the old Japanese research subtab. | **Move controls to Scene Browser**, connected to the same X/Y/Z variables and guarded write/read callbacks, not a new writer. Keep the strict Goemon, scene 0x161 and ROM/PID/RAM verification gates. |
| **Original Japanese debug menu / scene warp** | Scene Browser already has a region-specific native debug/warp action, overlapping the old separate JP menu. | **Use Scene Browser**. Hidden legacy control remains a guarded compatibility object; no extra destination list or new debug writer. |
| **Verify ROM** dashboard button | `practice/game_versions.py`, `practice/remembered_rom.py`, `practice/toolkit.py`, `practice/japan_native_recomp.py`: exact 16 MiB ROM hash plus three independent 64-byte guest-code probes protect the JP RAM attachment from wrong-game/wrong-region mapping. | **Remove the separate button, retain verification as a required safety prerequisite.** Connect opens the retail-ROM picker only when a previously verified JP file is unavailable. Remember its path and revalidate bytes on future runs. Failed/cancelled selection never attaches. USA process connection is unchanged. |
| **Compare memory changes "Test" dropdown** | `practice/state_discovery_ui.py` used static `PROBE_ACTIONS`/`JAPAN_PROBE_ACTIONS` guidance. Capture scope was actually controlled by `focused`/`wide` only. `compare_captures` assigned 5 extra travel points and 30 extra storyline/item points based solely on the selected text label. | **Remove presets and label-based ranking bias.** Use any freeform report name in the common Results toolbar; expose Focused vs Wide as the real capture-policy control. Keep dedicated Japanese XYZ analysis separate. |
| **Capture C confusing semantics** | USA `compare_captures` and Japanese `compare_japan_memory` discard candidates that fail to return to A whenever a third capture is supplied; Japanese XYZ requires C stable at B instead. | **Explicitly explain the difference.** Standard A/B comparison only needs A and B. C is optional and restrictive for normal reversible changes; **skip it for persistent or irreversible flags**. For Japanese XYZ: wide A still, B moved, C still at B, then Find XYZ triples. |
| **Two investigation names in one panel** | Flag and A/B pages each added their own title field alongside the common Save report name. | **Remove duplicate fields.** All four research pages use the same shared Results/report action bar, placed before the individual method's controls. |
| **Value Search / Compare memory / Investigate flags / Record damage** | Their actual algorithms differ: live exact/unknown scan, broad snapshot A/B, repeated 100-byte bit trials, and automatically triggered HP-loss windows. | **Keep four distinct capture engines.** Shared results table, live polling, watch selection and reporting remain unified; no nested extra sessions. |
| **Value freezes tab vs Live Memory freeze context menu** | `value_freezes_ui.py` adds automatic HP resources, god mode and native per-frame guard logic, while Live Memory exposes raw-value freeze. | **Keep the specialised freeze functions for now.** Raw freeze form may be folded into Live Memory later, after proving write/update parity. |
| **Unlocks vs Story progress** | The former edits verified mapped item and unlock bytes; the latter groups story progress and event-type flags. | **Keep** because they are not provably functionally identical. Audit duplicated address mappings separately before deleting any action. |
| **Dashboard Japanese raw RAM read vs Live Memory** | Dashboard's Address/Bytes/Read supports temporary arbitrary guest byte inspection without a persistent watch; Live Memory offers typed persisted values. | **Keep temporarily**: similar appearance but not functionally equivalent. Candidate for an advanced Live Memory reader after replacement testing. |
| **Per-tool raw JSON exporters vs Reports** | `ui_extension.py` provides old inspector, transition and native watch exports. This research branch uses four-file reports for the main discovery tools. | **Retain legacy actions/data for now**; migrate only after confirming all trace fields are represented and old report import works. |
| **Unused calibration/cursor builders** | `practice/ui_extension.py` defines native calibration and character-cursor pages that the Toolkit constructor does not presently call. | **Mark unmounted/dead-UI candidates**, but do not delete without a caller/search/import audit and test coverage. |
| **Hidden logical checkpoint panel** | Toolkit instantiates legacy bookmark/checkpoint handling and later hides part of the layout. | **Preserve persistent saved states and APIs** until all uses and fallbacks have been mapped. |

## Comparison controls: exact current behaviour

1. **Investigation name:** freeform, labels captures/report. It does not change memory range, matching rules or ranking.
2. **Focused:** USA reads system (0x800C7800 + 0x1000), game globals (0x8015C500 + 0x900), plus accessible player task/object regions. JP focused reads two 4 KiB research windows; they are not verified JP saved-event banks.
3. **Wide:** USA reads 0x80000000–0x803FFFFF (4 MiB); Japan reads the verified available 4 or 8 MiB RDRAM. Wider scans can take longer.
4. **A / B:** snapshot before and after a chosen action. A/B comparisons rank changed bytes, potential one-bit or boolean transitions and (where supported) plausible floats. No addresses are excluded by a question preset.
5. **C (optional):** for ordinary compare, retain only A→B changes that returned to A in C, filtering away permanent changes. **Do not use C** to find an irreversible story/item event.
6. **Japanese Find XYZ triples:** separate read-only heuristic requires three WIDE captures with C stationary at B; it searches float triples and does not establish the player pointer. Its exhaustive advanced export remains available.

## Safeguards and limits

- Original RAM snapshot evidence, region-specific saved custom watches, report formats and guarded writers remain intact.
- Japan connection still requires verified ROM bytes and region-correct guest RAM probes; clicking Connect no longer requires a separate Verify ROM action.
- The duplicate Japanese diagnostics table may still exist as an internal compatibility widget, but it is not a user-visible tab and no longer polls continuously. A future cleanup can remove its internal widget creation after all call sites have migrated.
- No changes to ROM bytes, source recomp binaries or original guest-MIPS instruction tracing. Real Linux/Windows native-game behaviour is still an acceptance gate, not proof from synthetic GUI tests.
- The implementation does not automatically discard or rewrite saved research files.

## Next cleanup gates

1. Live-test JP Connect (fresh ROM picker, remembered ROM, wrong ROM, recomp restart) and both regions' shared Live Memory and Scene Browser.
2. Screenshot review at minimum window size and a wide desktop window, especially the newly relocated Japanese XYZ controls.
3. Move genuinely unique old inspector exporters into the common Reports flow before deleting their code.
4. Audit fixed-address aliases across Unlocks, Story progress and the Live Memory field registry before consolidating those tabs.
5. Delete hidden compatibility widgets only after import/caller/test migration, not simply because they are no longer displayed.

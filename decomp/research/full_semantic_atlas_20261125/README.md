# Whole accepted-C semantic atlas — 25 November 2026

Research-only, canonical snapshot stable/decomp@ad5c02dbba2a82ac37e94184c5aa82d53bb5561f (merged PR #249). Authenticated source archive 15020042724 against COMMIT.txt and SHA256SUMS, plus both expanded original SHA-1 pins. This is a whole accepted-C census, NOT a census of all remaining assembly functions. Previous PR #255 is independent pending research; this pass does not supersede or duplicate its address-record changes. PR #250 is unmerged and excluded. No new matching C, source renames, compiler attempt, gameplay run or toolkit change.

## Reconciliation

| Metric | USA | Japan rev-0 |
|---|---:|---:|
| Accepted regional C entries (including 13 existing USA upstream) | 2952 | 2842 |
| Reconstructed extents independently reconciled | 2939 | 2842 |
| Original instruction bytes | 192312 | 178040 |
| Individual stored code hashes corroborated against original ROM | 2939 | 2517 |
| Complete accepted-body exact unique pairs (per region) | 216 | 216 |
| Calls to identified helpers (unique callers) | 1054 | 1018 |

The 325 remaining JP extents have original-ROM hashes computed but no corroborating digest found in the scanned stored metadata; these are not claimed as fresh digest replays. USA's 13 upstream C names/addresses are included with extent unresolved (separate from canonical 2939 reconstruction proof). No ambiguous competing extents survived reconciliation. Regional inventory membership is canonical USA combined/inventory and JP2842 inventory, not inferred from source filenames.

## Mutually exclusive primary evidence categories

| Category | USA | JP |
|---|---:|---:|
| Documented static role | 87 | 38 |
| Resource-list registration family | 374 | 374 |
| Verified bounded low-level behavior | 115 | 119 |
| Existing symbol name | 40 | 31 |
| Known callee lead only | 641 | 625 |
| Overlay context only | 666 | 644 |
| Unresolved | 1029 | 1011 |

125 function-specific static roles integrate previous research and newly corroborated findings. 748 registration wrappers are repetitive, not unique actor implementations; 234 bounded low-level patterns include empty returns, single field reads/writes, argument-home spills and offset returns. 71 existing symbol names are not new gameplay identifications. 1,266 additional entries have a known helper call but not a complete caller meaning; 1,310 have context only; 2,040 remain unresolved. 2,072 total callers have at least one recognized helper call (overlaps primary categories); 114 call saved bank C operations (59 USA/55 JP). 216 unique nontrivial exact-code pairs (>=32 bytes) within the same original owner among accepted C are candidate relationships, not proof of equivalent data, relocations or gameplay. Do not transfer a semantic label merely because instruction hashes match.

## Meaningful findings and earlier accepted code

- Dialogue window opening USA 8000D4E0 / ROM E0E0, JP 8000D230 / DE30, 396 B; closing USA 8000D79C / E39C, JP 8000D4EC / E0EC, 380 B. The existing VM_ARCHITECTURE_RESEARCH.md documents opening phase 1–3, ready phase 4, closing phases 5–6, and the original poll/close paths. These are dialogue presentation transitions, NOT room transitions. The paired newly accepted C confirms dimensions and scale progression.
- All 374 36-byte wrappers per region in file 12 independently exhibit the same complete instruction shape and call USA 80013AC4 / JP 80013654. Pinned upstream src/wave_uty.c and accepted JP func_80013654_14254.c walk a zero-terminated list of unsigned halfword resource identifiers and invoke the per-resource loader. Resource-list registration is more precise than a generic actor-spawning label.
- Scheduler: 16 accepted USA/JP paired routines verified across the entire original extents; every changed instruction is either the same JAL with a 0x390 code displacement or the corresponding cursor-load immediate. This is not a global code-translation rule. Insertion, activation, removal and all six callback-slot setters are independently paired. USA current-task setters 80035204/8003521C/80035234 correspond to JP 80034E74/80034E8C/80034EA4 (slots +8/+C/+10); explicit-task setters 80035214/8003522C/80035244 correspond to JP 80034E84/80034E9C/80034EB4 and their bodies are byte-identical. Source trace: decomp/docs/USA_TASK_SCHEDULER_LIFECYCLE_20261121.md; accepted regional code.
- USA 8000B824 (64 B, save_resources.c) turns four Fortune Doll quarters into +2 max health native units and refills current health, once per invocation, leaving excess quarters. USA 8000B640 initializes a new game: lives 3, health/max health 10, Ryo 100; 8000B718 restores spawn record and enforces minimum lives 3/health 10. See DOLL_REWARD_TRACE.md and save_resources.c. These are older accepted C, not new matches.
- Older paired file 26 code: Mr Arrow update USA 080000CC / ROM 6AE8AC, JP 080000CC / 6B342C (168/152 B); tests actor interaction bit 0x200, starts event 0x6C and sets actor-supplied saved flag. Existing USA runtime capture in PHASE1_MR_ARROW_NATIVE_SETTER_RUNTIME_USA_JP_20261117.md. Map pickup event 0x6B USA 080002D0 / 6AEAB0, JP 080002B0 / 6B3610 (168/152 B); per-instance identity provisional. Silver Doll USA 080005F8 / 6AEDD8, JP 080005B8 / 6B3918 (232/212 B); starts event 0x66 or 0x312 based on saved flag 0xE2. Follow-up USA 080006E0 / 6AEEC0, JP 0800068C / 6B39EC waits for script completion. USA gold update 0800083C / 6AF01C starts event 0x6A. Exact script semantics from DOLL_REWARD_TRACE.md and SILVER_FORTUNE_DOLLS.md. No JP gameplay replay.
- New paired file 61 semantic lead USA 0800098C / ROM 72125C, JP same VMA / ROM 72566C, 100 B each. Both accepted C bodies test saved bank C bit 0x199; if clear, set it and start numbered VM event 0x137; retire task regardless. Original call sites +0x9A4,+0x9B8,+0x9C8,+0x9D8 in both overlays. USA candidate in promo367_20261125, JP candidate in jp1686_promotion/pass509. Existing Ghost Toys research records 0x199 in a nearby flag-clearing sequence; do not identify this callback as a torch or assign exact in-game trigger yet. Flag 0x199 and event 0x137 are different namespaces.
- Previously promoted gameplay Start gates USA 8001F940 / JP 8001F610; three-callback dispatch USA 8001F8B0 / JP 8001F580; VM busy test USA 8003F1D8 / JP 8003EE44. These are accepted, unlike the unresolved complete pause/skip causality. Character switch sync USA 801DD5C0 / JP 801E2970; alternate USA 801DD654 / JP 801E2A04; actual state clearing and callback installation checked against paired reconstructed bodies. USA Mini selector 801E1C90 uses movement speed 1.12f versus 2.8f, transition parameter 0.3f; preserved accepted native C. No new runtime claim.

## Reproducible evidence package

Source-only ZIP goemon_semantic_atlas_20261125.zip delivered in originating conversation; SHA256 7b10abe7999cfefd044d43cb292748245b6fea545b29b50366a8368be35ae5f9. Includes 5,794-row semantic_atlas.csv, complete regional summary JSON, two standard-library Python scripts and instructions/SHA256SUMS. It excludes private ROM bytes, generated ASM, assets, ELF/object files and proprietary toolchain. Direct shell GitHub DNS unavailable; authenticated local source archive and connector isolated tree used for documentation and compact summary publication. Full large CSV/scripts delivered in ZIP, not committed via connector.

Two clean outputs identical (CSV and summary cmp); 5,794 unique regional entries, 432 reciprocal exact-peer rows (216 pairs) validated; complete reconstructed byte totals reconcile; original input SHA-1s verified. Static direct call scanner resolves literal addresses only in uninterrupted basic blocks, clears facts across control flow and does not infer indirect runtime targets. This is not dynamic path coverage. Native IDO/G2 NOT_RUN; existing proof/source/inventory unchanged. Required hosted PR regression and routing remain mandatory; counts unchanged. Future work: review event-linked callbacks and assign precise object identities using registration and original placement data; identify remaining original ASM separately.

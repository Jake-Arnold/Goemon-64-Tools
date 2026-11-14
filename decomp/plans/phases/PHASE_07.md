# Phase 07 — State transitions

**Scope:** G64-061–G64-070; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/transition_state.c`
- `decomp/rotation_angles.c`
- `decomp/engine_state.c`
- `decomp/default_entrance.c`
- `decomp/MAP_TRANSITION_TRACE.md`
- `docs/KEY_LOCK_CODE_TRACE.md`

## Known phase risks and negative controls
A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

## Task work packages

### G64-061 — Draw native transition state graph

**Status:** RESEARCH_ONLY. **Dependencies:** G64-002.
**Focus files:** `decomp/transition_state.c`; `decomp/MAP_TRANSITION_TRACE.md`.

**Architectural intent:** Connect matching 80003728/80003628/80003528/80003428/80003380 helpers to dispatcher 8001F8B0 and pending 800030F0.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/transition_state.c, decomp/MAP_TRANSITION_TRACE.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Connect matching 80003728/80003628/80003528/80003428/80003380 helpers to dispatcher 8001F8B0 and pending 800030F0.
4. Create caller/callee graph of 800030F0, 8001F8B0, the nested reset chain and scene-init routines.
5. Distinguish requested scene state from actual resource teardown/loading and actor instantiation.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Graph labels observed function effects separately from unproven room loading/unloading semantics.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-14):** `RESEARCH_ONLY`; the original-address graph is
documented in `../MAP_TRANSITION_TRACE.md`. The pinned linked ELF confirms the
18-entry outer `stepw` table, the separate five-entry `800030F0` substate
dispatch and the three-entry `8001F8B0` nested dispatch. State 15/substate 1
requests file ID 15 at its pinned overlay VMA only when `D_800548D8` is zero;
the file maps to `file_15`, not generic room content. The flag's meaning and
the routines' complete teardown/activation effects remain unproven. No C was
promoted and no fresh G2 was run. `800030F0` and `8001F8B0` remain ASM-owned;
G64-064 completed as `RESEARCH_ONLY`; G64-065 is next.

### G64-062 — Trace file/resource loading boundary

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-061.
**Focus files:** `decomp/transition_state.c`; `decomp/file_table.c`; `decomp/MAP_TRANSITION_TRACE.md`.

**Architectural intent:** Follow 80001C00_2800 and table paths toward resource allocation, room scene activation and releases without changing runtime features.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/transition_state.c, decomp/file_table.c, decomp/MAP_TRANSITION_TRACE.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Follow 80001C00_2800 and table paths toward resource allocation, room scene activation and releases without changing runtime features.
4. Trace file ID 0x0F load to 0x801CB460 and relevant file table readers.
5. Record where decompression, allocation and freeing occur; do not assume scene transition from a state-byte write.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Call-edge table identifies which data are files, RAM pointers, overlays or object lists and what remains unknown.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome:** The retail table proves ID 15 is uncompressed at `[0x61D5DE,
0x626E5E)` and maps to Splat `file_15` at reference interval
`[0x65E310, 0x667B90)`. Its caller-supplied destination is the shared
`static_overlay_1` window at `0x801CB460`; the loader fills `0x14CA0` BSS bytes
and returns `0x801E9980`. Allocation/free are caller-owned. No activation,
prior-overlay release or room teardown edge was established. See the execution
record and loader call-edge table in `MAP_TRANSITION_TRACE.md`. G64-065 is next.

### G64-063 — Analyze middle transition dispatcher

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-061.
**Focus files:** `decomp/rotation_angles.c`; `decomp/MAP_TRANSITION_TRACE.md`.

**Architectural intent:** Recover func_8001F940_20540 between already matched 8001F914 and 8001FA3C; inspect all global changes/calls.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/rotation_angles.c, decomp/MAP_TRANSITION_TRACE.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover func_8001F940_20540 between already matched 8001F914 and 8001FA3C; inspect all global changes/calls.
4. Inspect unresolved middle dispatcher 8001F940 with its siblings 8001F914 and 8001FA3C.
5. Recover actual order of calls, system field writes and possible resource side effects.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** CFG and typed signature have original evidence; host test distinguishes state branches before G1/G2.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-14):** `RESEARCH_ONLY`; raw pinned-ROM instructions and the
caller establish the 252-byte CFG, guarded store order, and an inferred
`void func_8001F940(void)` signature. The cursor helper is a pure nonzero test
of VM program PC `0x80077858`; this dispatcher does not update it. The
ASan/UBSan host reference and its reload negative control passed. Two bounded
IDO variants linked at the original VMA but both first differed at `+0x10`,
so codegen stopped and `rotation_angles.c` retains `GLOBAL_ASM`. No fresh G2 was
run; manifest, proof, and inventory are unchanged. See
`../execution/2026-11-14-g64-063-middle-transition-dispatch.json`.
G64-065 is next.

### G64-064 — Analyze transition loop 8000394C

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-061, G64-062, G64-063.
**Focus files:** `decomp/transition_state.c`; `decomp/test_transition_state.c`.

**Architectural intent:** Map func_8000394C_454C original stack, step dispatch and state byte updates inside transition_state.c.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/transition_state.c, decomp/test_transition_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map func_8000394C_454C original stack, step dispatch and state byte updates inside transition_state.c.
4. Inspect 8000394C main-loop branch conditions and input/state changes.
5. Create an ordered state-transition table, then host-test self-transitions and exit conditions.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** All branches accounted for and sentinel state tests pass; no claim that this alone implements safe scene transition.

**Outcome (2026-11-14):** `RESEARCH_ONLY`; the pinned 116-byte routine has one
conditional gate, and its five callers ignore the return. Its zero-result path
writes byte `5` at `0x800C7CDD`, stores halfword `1` at `0x800C7A76` in the
`80003880` call delay slot, then reloads the current system pointer and
increments `SYS_W+0x3ADD6`. The ASan/UBSan host reference covers both branch
outcomes, store/call order, pointer reload, sentinels and byte wrap. The
function itself has no internal loop; scene teardown/activation remains
unproved. Production retains `GLOBAL_ASM`; no native candidate or fresh G2
was run. See `../execution/2026-11-14-g64-064-transition-loop-gate.json`.
G64-065 is next.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-065 — Revisit engine state 80039F84

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-061.
**Focus files:** `decomp/engine_state.c`; `decomp/test_engine_state.c`.

**Architectural intent:** Study earliest unresolved engine_state.c function and interactions with D_801C09CE/CF and nearby matched helpers.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/engine_state.c, decomp/test_engine_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Study earliest unresolved engine_state.c function and interactions with D_801C09CE/CF and nearby matched helpers.
4. Characterize engine_state 80039F84 from original assembly, fields and known adjacent matching writers.
5. Use typed read/write evidence, not names; derive corner-case behaviour before compiler variation.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Original C-call/field-width contract plus host state-table tests precedes native compiler matching.

The pinned 220-byte target is dispatched indirectly by low-halfword command
index 5 through `D_8006E5CC`. It consumes `D_801C09D0` as an unsigned-byte
one-shot gate, then writes the current entry pointer for each of 16 records
before checking each full word. Nonzero records have flag bit 0 set and call
`alSynSetPan` with `(lhu(+0x58) >> 8) & 0x7F`, the global audio-context word,
and a target at stride `0x1C`. The matching CE/CF helpers remain independent;
the target does not access them. Its pan sweep is established from the call
and argument data. `8003A060` is a static D0 writer and `8003889C` clears it;
the runtime event, semantic name and live purpose remain unknown.

The ASan/UBSan host reference passes the latch, empty/active-record, signedness,
pan-boundary, pointer-order and adjacent-byte sentinel cases. Negative controls
without the `0x7F` pan mask and with a signed object-word predicate both fail as
expected. No native compiler variant was justified by the trace; production
keeps `GLOBAL_ASM`, with no manifest/proof/inventory change and no fresh G2 or
in-game check. See
`../execution/2026-11-14-g64-065-engine-pan-sweep.json` and
`../../MAP_TRANSITION_TRACE.md`. G64-066 is next.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-066 — Revisit engine state 8003A060

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-065.
**Focus files:** `decomp/engine_state.c`; `decomp/test_engine_state.c`.

**Architectural intent:** Study next retained-ASM engine_state.c function; identify frame, globals, conditional writes and call effects.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/engine_state.c, decomp/test_engine_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Study next retained-ASM engine_state.c function; identify frame, globals, conditional writes and call effects.
4. Characterize 8003A060 preserving original shared global aliasing and conditional order.
5. Compare original ABI/register map in complete unit with neighboring C.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Static CFG is complete and exact G1 codegen achieved or bounded mismatch logged.

Original MIPS confirms this as the complementary fixed-pan sweep: nonzero D0
returns untouched; zero D0 is set to 1, then 16 records at stride `0xB0` are
checked and active entries receive flag bit 0 plus `alSynSetPan(..., 0x40)`
with target stride `0x1C`. The active-entry context is reloaded each call and
CE/CF are untouched. Sol Medium independently confirmed dispatch index 6 and
the shared state contract.

The ASan/UBSan host matrix passes both latch states, empty and mixed records,
high-bit-only words, flag and adjacent-byte sentinels, fixed-pan behavior,
pointer/call order, and synthetic D0/context mutation. A per-entry-pan mutant
fails as expected. One full native source-unit hypothesis linked the target at
its original VMA but emitted 212 bytes versus 216; first mismatch is `+0x0C`
where the candidate loads D0 before the original RA save. Under the v2 stop
rule retain `GLOBAL_ASM`; no G2 or live-game test was run. See
`../execution/2026-11-14-g64-066-fixed-pan-sweep.json` and
`../../MAP_TRANSITION_TRACE.md`. G64-067 is next.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-067 — Revisit engine state 8003A138

**Status:** RESEARCH_ONLY (2026-11-14). **Dependencies:** G64-066.
**Focus files:** `decomp/engine_state.c`; `decomp/test_engine_state.c`.

**Architectural intent:** Recover adjacent 8003A138_3AD38 and compare with existing 8003A1C4 / 8003A204 / 8003A228 semantics.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/engine_state.c, decomp/test_engine_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover adjacent 8003A138_3AD38 and compare with existing 8003A1C4 / 8003A204 / 8003A228 semantics.
4. Characterize 8003A138 including all callback and conditional side effects.
5. Verify unchanged 8003A1C4 and 8003A204/8003A228 code when staging.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** No accidental adjacent-global aliasing; signedness/byte-write regression and production-codegen proof when eligible.

The verified 140-byte leaf reads the full `D_801C0A20` word, branches on
equality with 10, uses that same word as a byte-table index, and conditionally
sets either `D3` or `D6` to `0xFF` before copying one unsigned table byte to
`D1/D2` or `D4/D5`. Dispatcher entries 7–10 all point here; the direct caller
also has a delay-slot store that selects mode 10. The biased table produces
`{1, 2, 8, 8}` for those indices. ASan/UBSan host cases cover each mode,
latch preservation, neighboring sentinels and a synthetic full-word index.
The low-byte-truncation mutant fails.

One full-unit IDO candidate had the correct 140-byte extent and kept every
neighboring function exact, but its first target mismatch is the branch at
`+0x10`; IDO scheduled the `D6` address into the delay slot instead of forming
the original `D3` fallthrough address. Stop under the one-hypothesis v2 rule,
retain `GLOBAL_ASM`, and do not run G2. Details: `../../ENGINE_STATE_TRACE.md`
and `../execution/2026-11-14-g64-067-engine-state-mode-map.json`. G64-068 is
next.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-068 — Review default entrance 80020F10

**Status:** RESEARCH_ONLY. **Dependencies:** G64-061, G64-062, G64-063, G64-064.
**Focus files:** `decomp/default_entrance.c`; `decomp/test_default_entrance.c`.

**Architectural intent:** Model func_80020F10_21B10 adjacent to matching 80021444/214E4; separate entrance record selection from load requests.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/default_entrance.c, decomp/test_default_entrance.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Model func_80020F10_21B10 adjacent to matching 80021444/214E4; separate entrance record selection from load requests.
4. Trace 80020F10 native entrance lookup against already matching 80021444/800214E4.
5. Test all-zero coordinates and original unchecked indexes without authoring new warp APIs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Test all-zero triplet semantics and room indices against original data accesses; do not expose a generic warp API.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-14):** The 1,332-byte target is the indirect-dispatch
stage/room selection display handler, not the entrance-record reader. It
indexes group base/count tables, updates SYS_W+0x3ADF4 and derives the intended
room ID at +0x3ADF2. Only the confirm path calls matched 0x80021444; matched
0x800214E4 performs the 10-byte record lookup and all-zero-coordinate
clearing. Existing host tests for those neighbors passed. No whole-function
native candidate was justified under the v2 budget, so retain GLOBAL_ASM; no
fresh G2 was run and the stored proof is unchanged. See
../../DEFAULT_ENTRANCE_TRACE.md and
../execution/2026-11-14-g64-068-default-entrance-review.json.

### G64-069 — Architect transition safety assertions

**Status:** RESEARCH_ONLY. **Dependencies:** G64-061, G64-062, G64-063, G64-064, G64-065, G64-066, G64-067, G64-068.
**Focus files:** `decomp/MAP_TRANSITION_TRACE.md`; `decomp/test_transition_state.c`.

**Architectural intent:** Add static/synthetic checks for correct state sequencing, resource pointer validity assumptions and absence of toolkit writes.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/MAP_TRANSITION_TRACE.md, decomp/test_transition_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Add static/synthetic checks for correct state sequencing, resource pointer validity assumptions and absence of toolkit writes.
4. Write explicit assertion that state request, room resource loading and safe gameplay transition are three distinct properties.
5. Host tests can check known state updates; they cannot claim in-game transition safety without observed runtime proof.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Tests fail on invalid inferred scene unload shortcuts; documented evidence clearly separates native behavior from controllable API.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-14):** Added a three-claim evidence matrix to MAP_TRANSITION_TRACE.md, distinguishing a state request, the gated file-15 load request, and a safe gameplay transition. Existing G64-062 original-ROM/table evidence supports only the static destination window; runtime activation remains unknown. The state host fixture now protects intended-room sentinels and the file-15 table window. Disabled direct-warp and scene-list tests now spy on write_guest, catching write-then-restore behavior. Focused C and Python tests and local decomp CI passed. No production control or matching-C ownership changed; no fresh G2 was run. See ../execution/2026-11-14-g64-069-transition-safety-assertions.json.

### G64-070 — Gate transition slice

**Status:** PLANNED. **Dependencies:** G64-063, G64-064, G64-065, G64-066, G64-067, G64-068, G64-069.
**Focus files:** `decomp/transition_state.c`; `decomp/rotation_angles.c`; `decomp/manifest.json`.

**Architectural intent:** Integrate only exact transition/engine/default-entrance C functions after original-unit and full-image verification.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/transition_state.c, decomp/rotation_angles.c, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Integrate only exact transition/engine/default-entrance C functions after original-unit and full-image verification.
4. Build the entire transitioned slice with original C+ASM adjacency, full-ROM verifier and inventory.
5. Promote independently exact native matches only; leave unsupported graph nodes in assembly.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Any promotion preserves the ROM and current host tests; speculative state-machine findings stay documentation-only.

**Required negative control:** A matching state setter is not proof of a safe room warp, unload, map reset or successful live game transition; never add companion game-memory writes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

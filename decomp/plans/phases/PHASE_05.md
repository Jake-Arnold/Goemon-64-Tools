# Phase 05 — VM graphics and formatting

**Scope:** G64-041–G64-050; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/script_vm.c`
- `decomp/NEXT_TEN_FUNCTIONS.md`
- `decomp/candidates/vm_display_e234.c`
- `decomp/candidates/vm_display_ebac.c`
- `decomp/candidates/vm_callback_setup_e6c0.c`
- `decomp/candidates/vm_digits_format_probe.c`

## Known phase risks and negative controls
Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

## Task work packages

### G64-041 — Recover first display-list emitter

**Status:** RESEARCH_ONLY. **Dependencies:** G64-002.
**Focus files:** `decomp/candidates/vm_display_e234.c`; `decomp/test_vm_display_emitters.c`.

**Architectural intent:** Inspect 8003E234_3EE34's 440 original bytes and 11 graphics-command emissions; type cursor, source arrays and ordered word stores.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_display_e234.c, decomp/test_vm_display_emitters.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Inspect 8003E234_3EE34's 440 original bytes and 11 graphics-command emissions; type cursor, source arrays and ordered word stores.
4. Inspect the first display emitter's eleven two-word graphics commands and each cursor increment.
5. Compare 440-byte native target to 516/480-byte historical variants; do not trust equivalent host output to schedule stores.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Original MIPS/ROM word map and write-by-write register contract established before generating new source variants.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome:** Pinned ROM and assembly agree on all 110 original words at ROM 0x3EE34 / VMA 0x8003E234; the 440-byte instruction SHA-256 is acd6d1ecf74790033a8438ba6aae9c7652497de18d5ad7c205deaf2650268336. The tracked report keeps provenance and SHA-256 evidence instead of raw opcodes, and records all eleven cursor reads and +8 updates, all 22 output word stores, exact w0/w1 expressions, and store order. In particular, the cursor global is advanced before each pair; the final w1 is stored before jr ra and the final w0 is written in its delay slot. The caller at 0x8003F004 invokes the no-argument function only when the effective D_801C77E0_1C83E0 value is 3. The trace establishes an 8-byte two-word cursor contract; a C-level Gfx type and volatile qualifier remain unproven.

Historical E234 candidates remain nonmatches: the ordinary layout compiled to 516 bytes and the volatile-cursor layout to 480 bytes versus 440 original bytes. Their host output is mock semantics and does not establish original MIPS scheduling or ownership. G41 made no candidate, production, or manifest changes. The stored proof remains 153 functions / 11,800 bytes and inventory remains 7,376 entries. See plans/execution/2026-11-13-g64-041-display-emitter-trace.json.

**Next:** G64-042 has since completed RESEARCH_ONLY. G64-043 remains PLANNED and dependency-ready; G64-044 waits for both tasks.

### G64-042 — Test first emitter memory model

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-041.
**Focus files:** `decomp/test_vm_display_emitters.c`; `decomp/script_vm.h`.

**Architectural intent:** Host-test mock destination capacity, first/last graphics words, cursor advancement, aliasing and unchanged guard regions.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_vm_display_emitters.c, decomp/script_vm.h. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Host-test mock destination capacity, first/last graphics words, cursor advancement, aliasing and unchanged guard regions.
4. Use sentinel-guarded host graphics buffer to assert exact write order, first/last words, valid zero-input behavior and unchanged padding. Treat null cursor and owner pointers as invalid preconditions because the original path dereferences them directly.
5. Keep all encoded command constants at supported widths and forbid accidental out-of-bounds behavior in tested valid inputs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** All modeled 11 command writes match static original expectations; sanitizer guards catch out-of-bounds or skipped writes.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Added valid zero-input and aliased-owner cases to the first-emitter host harness. All 22 modeled command words, cursor advancement, first/last words, and guard regions are checked. The aligned fixture places owner[0x5D] over the B400 w0 slot, seeds the byte to one, and verifies that emitting w0 clears it before w1 reads it. A temporary pre-read-order mutant failed at the expected B400 w1 assertion. The test restores stack-backed global pointers before each helper returns. Null cursor and owner are invalid preconditions because the modeled original path dereferences them directly; no null behavior is claimed. ASan/UBSan passed 1,000 seeded cases plus zero and alias cases. This is mock memory semantics, not original-MIPS identity. Production source, candidate, manifest, and proof reports remain unchanged; native comparison, G2, and inventory were not run. See plans/execution/2026-11-13-g64-042-display-memory-model.json.

**Next:** G64-043 has since completed RESEARCH_ONLY. G64-044 is now dependency-ready.

### G64-043 — Recover second display-list emitter

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-041.
**Focus files:** `decomp/candidates/vm_display_ebac.c`; `decomp/test_vm_display_emitters.c`.

**Architectural intent:** Independently reconstruct 8003EBAC_3F7AC (436 bytes), preserving distinct resource pointers, opcodes and store order.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_display_ebac.c, decomp/test_vm_display_emitters.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Independently reconstruct 8003EBAC_3F7AC (436 bytes), preserving distinct resource pointers, opcodes and store order.
4. Inspect second emitter's distinct opcodes and resource-pointer sources instead of copying the first's control flow.
5. Inspect preserved original-address reports or outputs for the historical 500/464-byte variants and record a first mismatch if retained evidence supports one. If those artifacts are absent, record the mismatch as unavailable and leave a fresh original-unit comparison to G64-044.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A second command-word trace demonstrates where emitters differ; no unsupported shared macro changes compiler scheduling.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Verified all 109 EBAC words against the pinned ROM slice and traced all eleven cursor updates and command pairs independently of E234. EBAC uses resource D_80076148, distinct F300/F200 constants, caller-supplied x/y with a y-2 rectangle adjustment, and owner byte +0x5C. Its final B300 pair stores w0 before w1, with w1 in the jr delay slot; E234 stores w1 before w0. The host harness now builds EBAC mode separately and passed 1,000 synthetic cases. Historical summaries show 500- and 464-byte nonmatching candidates, but their native outputs/disassembly and first mismatch were not retained; no fresh native comparison was run. G64-041's E400 y-load, B400 w0, and owner-pointer offsets were corrected against the pinned source. Production code, candidate C, manifest and proof remain unchanged; G2 and inventory were not run. See plans/execution/2026-11-13-g64-043-display-emitter-trace.json.

**Next:** G64-044 is dependency-ready for the fresh first/second emitter native-layout comparison.

### G64-044 — Compare first/second compiler layouts

**Status:** RESEARCH_ONLY. **Dependencies:** G64-042, G64-043.
**Focus files:** `decomp/candidates/vm_display_e234.c`; `decomp/candidates/vm_display_ebac.c`.

**Architectural intent:** Revisit previous 516/500-byte candidates and volatile cursor variants; isolate exact register/pointer declarations.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_display_e234.c, decomp/candidates/vm_display_ebac.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Revisit previous 516/500-byte candidates and volatile cursor variants; isolate exact register/pointer declarations.
4. Annotate register reuse, address formation, two-word store grouping and no-call constraints side-by-side.
5. Try only source changes supported by both functions' access patterns; compare full units, not a synthetic aggregate.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Each targeted native codegen probe reports first differing instruction/relocation and whether original size is met; no size-only acceptance.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Sol identified the production context as the manifest's full `script_vm.c` unit (10,112 text bytes at VMA `0x8003CFA0`), not isolated candidate files. The pinned source/ROM, compiler, and MIPS binutils matched their recorded inputs. Two historical variants per emitter were counted; a screening V1 was semantically invalid (all packet writes normalized to w0→w1, and EBAC read owner flags before the B400 w0 store). Corrected V2 encoded the traced per-packet ordering and passed the EBAC alias-order control. V2 E234 is 444/440 bytes; V2 EBAC is 428/436. Both retain the entry cursor-base register mismatch (`$v0` vs `$v1`), with first target relocation-symbol difference at `+0x0C`. After the approved assignment-table pack and original-VMA link, both full units first differ at `+0x118` / `0x8003D0B8`, where a forward-call relocation changes because `func_8003F0FC_3FCFC` moves. The E234 unit grows to 10,128 text bytes and shifts `func_8003E3EC_3EFEC` by +4; the EBAC unit remains 10,112 bytes after section rounding but shifts `func_8003ED60_3F960` by -8. The packed `.rodata` is 60 bytes with all 15 table relocations retained and payload unchanged. Four of five distinct variants per target are counted; V2 did not improve the first mismatch, so no V3 was run. Production C/manifest/proof are unchanged, `GLOBAL_ASM` remains, and G2/inventory were not run. See `plans/execution/2026-11-13-g64-044-compiler-layouts.json`.

**Next:** G64-045 is dependency-ready for the VM setup callback ABI investigation.

### G64-045 — Recover VM setup callback ABI

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-021.
**Focus files:** `decomp/candidates/vm_setup_f37c.c`; `decomp/test_vm_setup_f37c.c`.

**Architectural intent:** Analyze 8003F37C_3FF7C's 192 bytes, float argument staging, 0x50 stack frame, three calls and callback values.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_setup_f37c.c, decomp/test_vm_setup_f37c.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Analyze 8003F37C_3FF7C's 192 bytes, float argument staging, 0x50 stack frame, three calls and callback values.
4. Trace three callback calls, floating-point stores and the 0x50-byte native stack-frame in func_8003F37C.
5. Treat size-equal 192-byte candidate as nonmatch until float registers and call argument order are identical.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host test verifies call order, float storage bits and untouched memory; original FPU/register arrangement required for G1.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Confirmed F37C's 192-byte extent at VMA `0x8003F37C` / ROM `0x3FF7C`, verified all six allocator integer stack slots are halfword reads, and corrected the research prototype to use `u16` for those arguments. The original reads a 32-bit owner word at `+0x8C` and a byte at `+0xD8`; the known flags field at `+0xD4` is retained in the F37C-local test layout. The shared header remains unchanged. The baseline 10,112-byte `script_vm.c` unit matched the original slice. One Sol-approved full-unit candidate compiled and linked to the original VMA at 10,112 bytes, but it differed in 36 words (115 bytes), all inside F37C. The first mismatch is `+0x08`: IDO emits `mtc1 $zero,$f2` where the original loads the scale into `$f2`; at `+0x0C` those values are reversed. Candidate relocations are 23 versus 19 original; the scale LO16 and allocator call each move four bytes. The host test passed 300/300 ASan/UBSan scenarios and rejected a float-zero mutant; the existing VM host suite passed. No second variant, G2, inventory or in-game check was run. Production `script_vm.c` still owns F37C as `GLOBAL_ASM`; manifest and stored proof are unchanged. See `plans/execution/2026-11-13-g64-045-vm-setup-abi.json`.

**Next:** G64-046 is dependency-ready for the callback setup path investigation.

### G64-046 — Recover callback setup path

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-045.
**Focus files:** `decomp/candidates/vm_callback_setup_e6c0.c`; `decomp/test_vm_callback_setup_e6c0.c`.

**Architectural intent:** Analyze 8003E6C0_3F2C0 (348 bytes) against 400-byte research candidate, its branches and callback-modified globals.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_callback_setup_e6c0.c, decomp/test_vm_callback_setup_e6c0.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Analyze 8003E6C0_3F2C0 (348 bytes) against 400-byte research candidate, its branches and callback-modified globals.
4. Recover original func_8003E6C0 348-byte callback sequencing, branch conditions and caller-visible globals.
5. Reject 400-byte output; host-test callback mutation and return timing before native matching.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** All branches represented in tests; original layout and 348-byte native codegen proven before promotion.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Original MIPS confirms a 0x38-byte frame, conditional cleanup callback, callback-sensitive window-index reloads, 20-byte choice records, a 0x8012 stream sentinel, final-link clearing, state 2 publication, and return of the updated cursor. The explicit pointer-lifetime candidate passed 400/400 ASan/UBSan host cases but compiled to 356 bytes versus the original 348. Its target first differs at +0x0C / 0x8003E6CC (`sw $s2,0x1C($sp)` versus `sw $s5,0x28($sp)`); the extra eight bytes shift a later call target and the following function. Production `GLOBAL_ASM`, manifest, source, and stored proof remain unchanged. Full-ROM G2 and inventory were not run. See `plans/execution/2026-11-13-g64-046-callback-setup.json`.

**Next:** G64-047 is dependency-ready for the number formatter investigation.

### G64-047 — Resolve number formatter

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-021.
**Focus files:** `decomp/candidates/vm_digits_format_probe.c`; `decomp/test_vm_digits_format_probe.c`.

**Architectural intent:** Analyze func_8003F480_40080 (164 bytes), sprintf argument preparation, destination halfword stream and bnel delay slot.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_digits_format_probe.c, decomp/test_vm_digits_format_probe.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Analyze func_8003F480_40080 (164 bytes), sprintf argument preparation, destination halfword stream and bnel delay slot.
4. Recreate original 164-byte digit formatter with sprintf argument loading and bnel delay slot.
5. Include negative, zero, multi-digit and buffer boundary tests; retain 9/41 masked positions as research-only until exact.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Exact native branch/argument code shape, original 164 bytes and formatting edge-case host cases required; avoid host printf locale assumptions.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Rechecked the original 164-byte/41-word span against the pinned decompressed ROM; all words match, and the format string at ROM 0x7DB60 is `%d`. Original MIPS uses the `$a0` delay slot for the `sprintf` destination and a `bnel` delay slot to preload the next signed-halfword digit. The 1,000-case ASan/UBSan host harness passes. Historical isolated IDO evidence covers 15 variants; the best recorded shape has only 3/13 comparable direct positions and none reproduce the `bnel` schedule. Because those trials already cover argument-source, pointer, loop and preloaded-character variants, no new native hypothesis was justified under v2. The function remains `GLOBAL_ASM`; no new full-unit build, G2, or inventory was run. See `plans/execution/2026-11-13-g64-047-number-formatter.json`.

**Next:** G64-048 is dependency-ready for the VM graphics integration boundary.

### G64-048 — Test VM graphics integration boundary

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-041, G64-042, G64-043, G64-044, G64-045, G64-046, G64-047.
**Focus files:** `decomp/script_vm.c`; `decomp/script_vm.h`; `decomp/verify.py`.

**Architectural intent:** Compose sandbox tests confirming display-list emitters and setup code do not corrupt VM state or neighboring buffers.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/script_vm.h, decomp/verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Compose sandbox tests confirming display-list emitters and setup code do not corrupt VM state or neighboring buffers.
4. Identify which graphics/setup routines share actual translation-unit ordering and rodata ownership.
5. Check candidate symbols/sections for padding and rodata shifts before altering manifest boundaries.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Deterministic mock traces and guard regions pass with ASan/UBSan; static/host results identified as non-game evidence.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Ran the existing ASan/UBSan memory-boundary harnesses for E234 and EBAC (1,000 traces each; E234 also covered zero input and owner alias), F37C (300), E6C0 (400), F480 (1,000), and the broader VM regression. All passed. Their fixtures guard display-list words, owner/control fields, choice arrays, formatter sentinel slots, callbacks, and VM state. The fixtures are independent mocks, not combined MIPS or in-game execution. Reviewed the shared `script_vm.c`/header/manifest/proof unit: the five functions remain ASM-owned, and preceding candidate size/relocation evidence gives no safe boundary or rodata edit. No production source, header, verifier, manifest, proof, or inventory change; no new full-ROM build under the v2 stop rule. See `plans/execution/2026-11-13-g64-048-vm-graphics-boundaries.json`.

**Next:** G64-049 is dependency-ready for the qualifying VM graphics routines gate.

### G64-049 — Stage qualifying VM graphics routines

**Status:** RESEARCH_ONLY (completed 2026-11-13). **Dependencies:** G64-044, G64-045, G64-046, G64-047, G64-048.
**Focus files:** `decomp/script_vm.c`; `decomp/manifest.json`; `decomp/verify.py`.

**Architectural intent:** Replace only G1-exact functions in original script_vm.c order, retaining assembly for other large VM targets.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/manifest.json, decomp/verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Replace only G1-exact functions in original script_vm.c order, retaining assembly for other large VM targets.
4. Stage one proven contiguous unit at a time, retaining all unresolved asm pragmas and original order.
5. Build complete ROM with new proof report; never accept an isolated full-size symbol as an integrated promotion.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Production translation-unit and full-ROM G2 passes; no translator drift in previously promoted VM helpers.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** The live manifest confirms all five dependency candidates remain `GLOBAL_ASM`: E234 (440 bytes), EBAC (436), E6C0 (348), F37C (192), and F480 (164). None has source-unit exact evidence. The emitter candidates have size and sibling-relocation differences; F37C remains 36 words different despite matching size; E6C0 grows to 356 bytes and shifts a forward relocation; F480's best historical isolated result is 156 bytes and no full-unit proof exists. The production `script_vm.c` unit remains 10,112 bytes at VMA `0x8003CFA0`, ROM `0x3DBA0..0x40320`. No boundary, padding, rodata, manifest, or verifier change is justified. Retain all five ASM owners; matching-C delta is zero. See `plans/execution/2026-11-13-g64-049-vm-graphics-staging.json`.

**Next:** G64-050 closes the VM candidate inventory.

### G64-050 — Close VM candidate inventory

**Status:** PLANNED. **Dependencies:** G64-030, G64-040, G64-049.
**Focus files:** `decomp/MASTER_WORK_QUEUE.md`; `decomp/results/inventory.json`.

**Architectural intent:** Reconcile all 13 original unpromoted VM entries against current manifest and new proofs; label every blocked function.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/MASTER_WORK_QUEUE.md, decomp/results/inventory.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Reconcile all 13 original unpromoted VM entries against current manifest and new proofs; label every blocked function.
4. Cross-check every VM draft against current manifest and strongest published historical result.
5. Write an evidence-ranked table of blockers, source hashes, exactness and next supported hypothesis; no duplicate queues.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Machine-readable residual VM list has verified state, original extent, current source and concrete mismatch, not a guessed percent-complete metric.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

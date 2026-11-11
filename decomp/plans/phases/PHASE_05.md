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

**Status:** PLANNED. **Dependencies:** G64-002.
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

### G64-042 — Test first emitter memory model

**Status:** PLANNED. **Dependencies:** G64-041.
**Focus files:** `decomp/test_vm_display_emitters.c`; `decomp/script_vm.h`.

**Architectural intent:** Host-test mock destination capacity, first/last graphics words, cursor advancement, aliasing and unchanged guard regions.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_vm_display_emitters.c, decomp/script_vm.h. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Host-test mock destination capacity, first/last graphics words, cursor advancement, aliasing and unchanged guard regions.
4. Use sentinel-guarded host graphics buffer to assert exact write order, first/last words, null/zero paths and unchanged padding.
5. Keep all encoded command constants at supported widths and forbid accidental out-of-bounds behavior in tested valid inputs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** All modeled 11 command writes match static original expectations; sanitizer guards catch out-of-bounds or skipped writes.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-043 — Recover second display-list emitter

**Status:** PLANNED. **Dependencies:** G64-041.
**Focus files:** `decomp/candidates/vm_display_ebac.c`; `decomp/test_vm_display_emitters.c`.

**Architectural intent:** Independently reconstruct 8003EBAC_3F7AC (436 bytes), preserving distinct resource pointers, opcodes and store order.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_display_ebac.c, decomp/test_vm_display_emitters.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Independently reconstruct 8003EBAC_3F7AC (436 bytes), preserving distinct resource pointers, opcodes and store order.
4. Inspect second emitter's distinct opcodes and resource-pointer sources instead of copying the first's control flow.
5. Compare original 436 bytes to 500/464-byte variants, noting actual first mismatch.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A second command-word trace demonstrates where emitters differ; no unsupported shared macro changes compiler scheduling.

**Required negative control:** Do not equate host-compatible graphics output with original instruction order, float ABI, branch-likely delay semantics, relocation identity or whole-ROM matching.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-044 — Compare first/second compiler layouts

**Status:** PLANNED. **Dependencies:** G64-042, G64-043.
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

### G64-045 — Recover VM setup callback ABI

**Status:** PLANNED. **Dependencies:** G64-021.
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

### G64-046 — Recover callback setup path

**Status:** PLANNED. **Dependencies:** G64-045.
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

### G64-047 — Resolve number formatter

**Status:** PLANNED. **Dependencies:** G64-021.
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

### G64-048 — Test VM graphics integration boundary

**Status:** PLANNED. **Dependencies:** G64-041, G64-042, G64-043, G64-044, G64-045, G64-046, G64-047.
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

### G64-049 — Stage qualifying VM graphics routines

**Status:** PLANNED. **Dependencies:** G64-044, G64-045, G64-046, G64-047, G64-048.
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

# Phase 02 — Object scheduling and short routines

**Scope:** G64-011–G64-020; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/object_dispatch.c`
- `decomp/engine_state.c`
- `decomp/state_predicate.c`
- `decomp/file_table.c`
- `decomp/NEXT_TEN_MAIN_SEGMENT.md`
- `decomp/results/next_twenty_execution_20261110.json`

## Known phase risks and negative controls
Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

## Task work packages

### G64-011 — Classify object mismatch

**Status:** PASSED_G2. **Dependencies:** G64-001, G64-003.
**Focus files:** `decomp/object_dispatch.c`; `decomp/candidates/integrated_object_dispatch_probe.c`; `decomp/results/next_twenty_execution_20261110.json`.

**Architectural intent:** Compare original object_dispatch.c pair with integrated_object_dispatch_probe.c; annotate exact swapped instructions at 0x35C9C/0x35CA0.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_dispatch.c, decomp/candidates/integrated_object_dispatch_probe.c, decomp/results/next_twenty_execution_20261110.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Compare original object_dispatch.c pair with integrated_object_dispatch_probe.c; annotate exact swapped instructions at 0x35C9C/0x35CA0.
4. Record the original and compiled instruction order at ROM 0x35C9C and 0x35CA0, including surrounding frame setup.
5. Treat the two swapped 32-bit instructions as an eight-byte mismatch, not an alignment or comparator tolerance issue.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Mismatch worksheet identifies original $ra spill vs lui ordering and demonstrates existing func_80035064_35C64 is unaffected.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-012 — Recover object ABI and liveness

**Status:** PASSED_G2. **Dependencies:** G64-011.
**Focus files:** `decomp/object_dispatch.c`; `decomp/candidates/object_dispatch_c94.c`; `decomp/test_three_dispatch_wrappers.c`.

**Architectural intent:** Trace func_80035094_35C94 parameter retention across first call, global reload and call to func_800350C4_35CC4; review signed/pointer types.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_dispatch.c, decomp/candidates/object_dispatch_c94.c, decomp/test_three_dispatch_wrappers.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Trace func_80035094_35C94 parameter retention across first call, global reload and call to func_800350C4_35CC4; review signed/pointer types.
4. Trace first-call side effects, reloaded D_8016DAB4 and the retained actor argument passed to func_800350C4.
5. Write a live-register map over both calls and show why original function saves RA before LUI without changing the sibling.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A register/liveness table specifies callee preservation, spill sites, function order and symbol bindings; no speculative semantic renames.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-013 — Bound IDO variants for object dispatch

**Status:** PASSED_G2. **Dependencies:** G64-012.
**Focus files:** `decomp/candidates/integrated_object_dispatch_probe.c`; `decomp/prove_integrated_units.py`.

**Architectural intent:** Try one supported C-expression/alias/lifetime variation per native IDO build, not opcode patching; retain all failed candidates and diffs.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/integrated_object_dispatch_probe.c, decomp/prove_integrated_units.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Try one supported C-expression/alias/lifetime variation per native IDO build, not opcode patching; retain all failed candidates and diffs.
4. Test one isolated source hypothesis at a time, retaining every original/compiled disassembly and score.
5. Stop after a bounded set with no progress; eleven previous volatile/pointer/local/comma/block variants already failed.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** An exact 96-byte combined unit becomes a G1 candidate; otherwise stop after a stated non-improvement budget and keep ASM.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-014 — Gate object promotion

**Status:** PASSED_G2. **Dependencies:** G64-010, G64-013.
**Focus files:** `decomp/object_dispatch.c`; `decomp/manifest.json`; `decomp/verify.py`.

**Architectural intent:** Stage object C only if true combined-unit matching; then full verifier, relocations, symbol inventory and host callback cases.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_dispatch.c, decomp/manifest.json, decomp/verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Stage object C only if true combined-unit matching; then full verifier, relocations, symbol inventory and host callback cases.
4. Integrate object dispatcher into actual object_dispatch.c only after full-unit 96-byte source matching.
5. Run new complete-ROM verifier and compare old 48-byte sibling; otherwise keep the 48-byte original ASM function.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Conditional +48-byte promotion to 148/11,020 only with complete-ROM equality; known 8-byte discrepancy must never be waived.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-015 — Revisit engine reset

**Status:** FAILED_NATIVE. **Dependencies:** G64-002.
**Focus files:** `decomp/engine_state.c`; `decomp/test_engine_state.c`.

**Architectural intent:** Investigate func_8003A1E8_3ADE8 (28 bytes) and original u16/s8 adjacent globals, two stores, address construction and delay slot.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/engine_state.c, decomp/test_engine_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate func_8003A1E8_3ADE8 (28 bytes) and original u16/s8 adjacent globals, two stores, address construction and delay slot.
4. Reconstruct the two writes to D_801C09D8 and D_801C09DA with exact sh/sb width and address construction.
5. Compare prior 20/28-byte native variants to original 28-byte span and assert neighboring storage is unchanged.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host sentinels detect adjacent-field damage; native unit emits 28 exact bytes before G2 eligibility.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-016 — Revisit state writer

**Status:** FAILED_NATIVE. **Dependencies:** G64-002.
**Focus files:** `decomp/state_predicate.c`; `decomp/test_state_predicate.c`.

**Architectural intent:** Investigate func_80006274_6E74 (36 bytes), original halfword/word writes, base adjustment and stack/argument spill.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/state_predicate.c, decomp/test_state_predicate.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate func_80006274_6E74 (36 bytes), original halfword/word writes, base adjustment and stack/argument spill.
4. Preserve the three original sh, sh, sw stores, final store in jr delay slot and stackless ABI.
5. Compare 28-byte candidate against the original 36-byte function; adjust declarations only if supported by MIPS accesses.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Store widths/offsets and delay-slot word store match original; host checks guard bytes, then G2.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-017 — Revisit file-table second lookup

**Status:** FAILED_NATIVE. **Dependencies:** G64-002.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Investigate func_80001D94_2994 (44 bytes) adjacent to matching 80001D68, preserving different table base and 0x7FFFFFFF masks.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate func_80001D94_2994 (44 bytes) adjacent to matching 80001D68, preserving different table base and 0x7FFFFFFF masks.
4. Use the secondary table base D_800573D8 rather than the existing first table D_800573D4.
5. Check repeated 0x7FFFFFFF masking and original argument spill/register allocation in all 44 bytes.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Test low-16-bit indexing, high-bit masking and original register schedule; exact 44-byte unit codegen precedes G2.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-018 — Revisit file-size reader

**Status:** FAILED_NATIVE. **Dependencies:** G64-017.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Investigate func_80001DC0_29C0 (52 bytes), unsigned entry subtraction, zero-input branch, delayed return scheduling.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate func_80001DC0_29C0 (52 bytes), unsigned entry subtraction, zero-input branch, delayed return scheduling.
4. Model the zero-index branch separately and preserve unsigned difference between file-table fields.
5. Match original late-return schedule and exactly 52 bytes; do not accept equal size with different registers.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host cases cover zero index, boundary unsigned subtraction and original branch behavior; original 52 bytes then G2.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-019 — Integrate independently passing short functions

**Status:** RESEARCH_ONLY. **Dependencies:** G64-015, G64-016, G64-017, G64-018.
**Focus files:** `decomp/engine_state.c`; `decomp/state_predicate.c`; `decomp/file_table.c`; `decomp/manifest.json`.

**Architectural intent:** Batch compatible source neighbors without mixing unrelated ASM; allow partial integration if only a subset matches.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/engine_state.c, decomp/state_predicate.c, decomp/file_table.c, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Batch compatible source neighbors without mixing unrelated ASM; allow partial integration if only a subset matches.
4. Integrate each independently matching short function without bundling a failing neighbor into the same promotion claim.
5. Rebuild the whole ROM after each coherent translation-unit staging, retaining existing 142+ proofs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Every newly counted function passes exact current translation unit, original-address instructions, complete-ROM comparison and unchanged inventory.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-020 — Record hard-stop decisions

**Status:** DOC_ONLY. **Dependencies:** G64-014, G64-019.
**Focus files:** `decomp/results/next_twenty_execution_20261110.json`; `PROGRESS.md`.

**Architectural intent:** Publish per-target disposition: promoted, exact isolated but unpromoted, mismatch, or blocked by proof; retain comparison diffs privately.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/results/next_twenty_execution_20261110.json, PROGRESS.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Publish per-target disposition: promoted, exact isolated but unpromoted, mismatch, or blocked by proof; retain comparison diffs privately.
4. Document every nonmatch with first ROM offset, original/candidate opcodes, register/relocation category and strongest source hypothesis.
5. Mark blocked/research-only instead of cycling indefinitely through variants or inflating totals.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** No prospective total is reported as achieved; PROGRESS.md and CONTINUE.md reconcile actual manifest/proof counts.

**Required negative control:** Reject equal-size but different-register codegen, changed adjacent C functions, invented no-op padding and any fixed binary instruction bytes.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

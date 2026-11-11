# Phase 04 — VM parser and text loop

**Scope:** G64-031–G64-040; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/script_vm.c`
- `decomp/VM_STREAM_MATCHING.md`
- `decomp/NEXT_TEN_FUNCTIONS.md`
- `decomp/candidates/vm_text_loop_alias_probe.c`
- `decomp/candidates/vm_command_walker_goto_probe.c`

## Known phase risks and negative controls
Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

## Task work packages

### G64-031 — Construct text-loop control-flow graph

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-021.
**Focus files:** `decomp/candidates/vm_text_loop_alias_probe.c`; `decomp/test_vm_text_loop_addressing.py`.

**Architectural intent:** Decompose func_8003DBEC_3E7EC's outer/inner counters, six branch-likely delay slots, callbacks and script-pointer aliases.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_text_loop_alias_probe.c, decomp/test_vm_text_loop_addressing.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Decompose func_8003DBEC_3E7EC's outer/inner counters, six branch-likely delay slots, callbacks and script-pointer aliases.
4. Write a block graph for func_8003DBEC_3E7EC including six branch-likely delay slots, both loop counters and early exits.
5. Account for the global pointer storage at 0x801C77E8 and halfword at +0xA without conflating pointer and pointed-to data.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Annotated 472-byte original graph covers every branch and delay slot, with data-liveness trace tied to original instructions.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome:** `VM_TEXT_LOOP_TRACE.md` records all 26 original control transfers,
their delay instructions, the six branch-likely annul slots, block successors,
and global/register liveness for the ROM-verified 472-byte function. The
ROM-bound guard verifies all 118 words, ten addressing/controller anchors, and
the six exact likely slots. C promotion was not attempted; original assembly
ownership remains.

### G64-032 — Resolve text-loop 0x48 frame

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-031.
**Focus files:** `decomp/candidates/vm_text_loop_alias_probe.c`; `decomp/probe_vm_text_loop_codegen.py`.

**Architectural intent:** Investigate why research candidate has 0x50 frame despite 472-byte symbol; isolate saved-register, volatile global and script argument lifetimes.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_text_loop_alias_probe.c, decomp/probe_vm_text_loop_codegen.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate why research candidate has 0x50 frame despite 472-byte symbol; isolate saved-register, volatile global and script argument lifetimes.
4. Compare expected 0x48 stack frame with candidate 0x50 and annotate every saved register and spill slot.
5. Test whether source-level lifetime changes move frame allocation without altering callback order.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A native IDO variant matches original 0x48 frame and branch layout without changing behavior, or records exact remaining words.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome:** The candidate saves the same ten registers and uses the same
`sp+0x44` outer-counter slot as the original, but IDO emits a 0x50-byte frame
with an unused eight-byte tail. Five controlled source-lifetime variants did
not reduce the frame; none matched the complete branch layout. All six
variants passed 5,000 synthetic differential cases. See
[`../VM_TEXT_LOOP_FRAME.md`](../VM_TEXT_LOOP_FRAME.md).

### G64-033 — Strengthen text-loop differential model

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-031, G64-032.
**Focus files:** `decomp/test_vm_text_loop_differential.py`; `decomp/test_vm_text_loop_differential_stubs.c`.

**Architectural intent:** Retain original-MIPS versus host-C test harness for controller halfwords, +0xA work value, dynamic bounds and early return.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_vm_text_loop_differential.py, decomp/test_vm_text_loop_differential_stubs.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Retain original-MIPS versus host-C test harness for controller halfwords, +0xA work value, dynamic bounds and early return.
4. Run deterministic original-MIPS interpreter versus host-C differential cases over two seeds with mutable callbacks.
5. Explicitly test controller held/pressed unsigned halfwords, changing loop bound, null returns and state reset.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** At least existing 10,000 deterministic synthetic scenarios pass; targeted mutants for signedness, stale bounds and aliasing are killed.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** The MIPS/host differential runner now executes ten
named edge cases before each seeded batch and defaults to 10,000 deterministic
random cases. Both required seeds pass 10,000 cases each. Negative controls
kill signed held and pressed high-bit checks, a cached outer bound, and the
script-pointee/work-record alias. The ASan/UBSan host harness passes all 15
groups; focused text-loop Python tests pass 10, the decomp suite passes 135,
and verifier tests pass 17. This remains host/static research: candidate source,
manifest ownership and the stored 148-function proof are unchanged; no IDO
translation-unit build, new whole-ROM proof, inventory build or in-game run was
made. See [`../execution/2026-11-11-g64-033-text-loop-differential.json`](../execution/2026-11-11-g64-033-text-loop-differential.json).

### G64-034 — Recover command-walker CFG

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-028.
**Focus files:** `decomp/VM_STREAM_MATCHING.md`; `decomp/candidates/vm_command_walker_goto_probe.c`.

**Architectural intent:** For 8003DE80_3EA80 retain signed halfword behavior and post-callback reread, negative-token handling and repeat suppression.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/VM_STREAM_MATCHING.md, decomp/candidates/vm_command_walker_goto_probe.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: For 8003DE80_3EA80 retain signed halfword behavior and post-callback reread, negative-token handling and repeat suppression.
4. Build CFG from signed 16-bit input and all negative-token cases; preserve reread after output callback.
5. Represent suppression (-1), delegated negative commands and ordinary positive tokens as independent exit paths.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** CFG explicitly models -1, other negative words, nonnegative words and callback-mutated current word; host tests exercise all paths.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** Added the exact 232-byte ROM extent and 24 control /
callback word guards to the existing original-MIPS checker. The paced-reader
CFG now distinguishes signed `-1`, every other negative token, suppression,
ordinary nonnegative output, callback mutation of the current halfword, and
the repeat-setting reloads. Baseline and GOTO probe each passed 1,100
ASan/UBSan host cases across 11 explicit scenarios; a cached-token mutant was
rejected by the callback-reread case. A fresh pinned IDO compile emitted a
220-byte function symbol / 224-byte `.text`; linked at the original VMA, its
first difference is `0x8003DE84` and 36/56 available positional words differ.
The older 228-byte result was not reproduced. The target remains `GLOBAL_ASM`;
no full-unit integration or fresh whole-ROM/inventory run occurred. See
[`../execution/2026-11-11-g64-034-command-walker-cfg.json`](../execution/2026-11-11-g64-034-command-walker-cfg.json).

### G64-035 — Fix command-walker delay slots

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-034.
**Focus files:** `decomp/candidates/vm_command_walker_goto_probe.c`; `decomp/test_vm_command_walker_probe.c`.

**Architectural intent:** Use original 232-byte native codegen target, bltzl delay slot and $s0-$s3 allocation; compare bounded C control-flow shapes.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_command_walker_goto_probe.c, decomp/test_vm_command_walker_probe.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Use original 232-byte native codegen target, bltzl delay slot and $s0-$s3 allocation; compare bounded C control-flow shapes.
4. Target original bltzl and delay-slot placement; record saved-register s0-s3 lifetimes.
5. Reject source variants whose 232-byte symbol matches in size but differ in instruction order or 0x? frame.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Exact original branch placement and 232 bytes before promotion; never accept a mere size-only variant or comparator score.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** Applied the updated Architect v2 budget after pulling
`a68c44b`. Four local C shapes were tested against pinned IDO 5.3 after the
G64-034 baseline. The best first-mismatch movement was from `0x8003DE84` to
`0x8003DE88`; the best-positioned variant still differs at 38/56 available
words and its `bltzl` target is four bytes late. A 232-byte symbol was rejected
because it used a `0x30` stack frame; another shape regressed to a `0x20` frame
and mismatch at `DE80`. All four passed the existing 1,100-case ASan/UBSan mock
harness. No fifth trial was run after the first-mismatch experiment regressed.
The function remains `GLOBAL_ASM`; no source-unit or full-ROM gate was run.
Updated the compact task-context regression to reflect G64-035's research-only
status and G64-036's pending dependency; the full decomp and verifier suites
pass. See [`../execution/2026-11-11-g64-035-delay-slots.json`](../execution/2026-11-11-g64-035-delay-slots.json).

### G64-036 — Prove command-walker semantics

**Status:** RESEARCH_ONLY (completed 2026-11-11). **Dependencies:** G64-034, G64-035.
**Focus files:** `decomp/test_vm_command_walker_probe.c`; `decomp/VM_STREAM_MATCHING.md`.

**Architectural intent:** Run sentinels for state marker, output suppression, changed cursor/word after external calls and zero/nonzero repetition.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_vm_command_walker_probe.c, decomp/VM_STREAM_MATCHING.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Run sentinels for state marker, output suppression, changed cursor/word after external calls and zero/nonzero repetition.
4. Test callback rewriting current input word and dynamic repeat setting, including null delegated cursor.
5. Assert marker writes occur before exit-state reloads and the cursor advances by one halfword, not one word.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Original behavior differential passes for all modeled branches, including null delegate return; no unknown external effect is invented.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** Reused G64-034's eleven-scenario host matrix,
1,100 sanitizer cases per source and stale-token mutant. Mapped the sentinel,
delegated negatives (including null), suppression, output callback mutation,
repeat reloads and halfword cursor step to original ROM instructions and the
58-word / 24-anchor guard. The gate at `DF68` is known C: it decrements
`D_801C77A0` when applicable and does not mutate `D_801C7798`; no unsupported
gate-mutation case was added. Existing host stubs select wrapper branches and
do not claim full helper-state simulation. No new C scenarios or MIPS model
were needed; production ownership and proof are unchanged. See
[`../execution/2026-11-11-g64-036-command-walker-semantics.json`](../execution/2026-11-11-g64-036-command-walker-semantics.json).

### G64-037 — Characterize 8003ED60 handler

**Status:** PLANNED. **Dependencies:** G64-021.
**Focus files:** `decomp/script_vm.c`; `decomp/script_vm.h`.

**Architectural intent:** Map currently retained-ASM func_8003ED60_3F960, identifying interpreter inputs, memory writes, callees and genuine CFG boundaries.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/script_vm.h. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map currently retained-ASM func_8003ED60_3F960, identifying interpreter inputs, memory writes, callees and genuine CFG boundaries.
4. Inspect original 8003ED60 switch/handler callers, argument types and live global state before drafting C.
5. Build an opcode/exit matrix and avoid inventing unobserved handlers; keep unknown cases delegated to ASM.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Reviewable original instruction map and narrow C signature precede a bounded exact-IDO candidate; no role inferred from address alone.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-038 — Resolve 8003F6E8 extent

**Status:** PLANNED. **Dependencies:** G64-002.
**Focus files:** `decomp/test_vm_wrapper_extent.py`; `decomp/script_vm.c`.

**Architectural intent:** For func_8003F6E8_402E8 preserve original 48-byte extent, including trailing jr $ra/nop absent from 40-byte natural C prefix.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_vm_wrapper_extent.py, decomp/script_vm.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: For func_8003F6E8_402E8 preserve original 48-byte extent, including trailing jr $ra/nop absent from 40-byte natural C prefix.
4. Treat original func_8003F6E8_402E8 extent as 48 bytes and prior candidate annotation 56 as unreliable.
5. Require exact original trailing jr ra + nop; 40-byte matching prefix never qualifies.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Original-function extent tests reject 40/56-byte confusion; full 48-byte codegen is required before G2.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-039 — Build VM parser behavioral matrix

**Status:** PLANNED. **Dependencies:** G64-033, G64-036, G64-037, G64-038.
**Focus files:** `decomp/test_script_vm.c`; `decomp/test_vm_text_loop_differential.py`.

**Architectural intent:** Compose semantic tests for parser loop, decoder and wrapper interactions without claiming a playable VM emulator.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_script_vm.c, decomp/test_vm_text_loop_differential.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Compose semantic tests for parser loop, decoder and wrapper interactions without claiming a playable VM emulator.
4. Create a corpus with each VM parser branch, side effect, callback boundary, signed token and escape path.
5. Require differential behavior under mutation and sentinel guards before isolated codegen.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** All identified paths have expected state/cursor/callback traces; test mocks explicitly separate modeled from unknown effects.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-040 — VM parser production gate

**Status:** PLANNED. **Dependencies:** G64-032, G64-033, G64-034, G64-035, G64-036, G64-037, G64-038, G64-039.
**Focus files:** `decomp/script_vm.c`; `decomp/manifest.json`.

**Architectural intent:** Integrate only fully matching text/parser/wrapper units using current translation-unit source with separate verified checkpoints.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Integrate only fully matching text/parser/wrapper units using current translation-unit source with separate verified checkpoints.
4. Stage only independently native-exact parser routines into the original 69-function script_vm.c unit.
5. Require unchanged existing VM functions, all original-address bytes and full ROM; skip unrelated unresolved parser branches.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Preserve all 142+ prior exact functions; whole ROM, 7,376-entry inventory and updated source hashes pass for every promotion.

**Required negative control:** Do not accept a correct length with mismatched delay slots, wrong 0x48 frame, incorrect control-flow exits or fabricated unreachable return instructions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

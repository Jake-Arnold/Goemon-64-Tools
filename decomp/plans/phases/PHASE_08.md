# Phase 08 — File/object/scheduler

**Scope:** G64-071–G64-080; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/file_table.c`
- `decomp/object_flags.c`
- `decomp/object_flags.h`
- `decomp/scheduler_queue.c`
- `decomp/LOCAL_MNSG_REVIEW.md`

## Known phase risks and negative controls
Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

## Task work packages

### G64-071 — Inspect file-table reader 80001DF4

**Status:** PLANNED. **Dependencies:** G64-017, G64-018.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Map function's table base, index widths, mask and downstream callers without assuming identical semantics to adjacent 80001D68.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map function's table base, index widths, mask and downstream callers without assuming identical semantics to adjacent 80001D68.
4. Trace next file reader 80001DF4 index-width, table base and bit-31 behaviour; compare sibling 80001D68.
5. Record original word loads, branch structure and expected return type before writing candidate.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Document symbol references and test each table index/bit mask case before an exact candidate.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-072 — Inspect file-table reader 80001E50

**Status:** PLANNED. **Dependencies:** G64-071.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Recover segment record access, branch structure and return semantics for 80001E50_2A50.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover segment record access, branch structure and return semantics for 80001E50_2A50.
4. Recover 80001E50 file reader pointer/record widths and all caller assumptions.
5. Test signed/unsigned limits, first and final valid entry, adjacent sentinel isolation.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host fixture uses boundary indices and sentinel table entries; original-address codegen is required to stage C.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-073 — Inspect file-table reader 80001EB0

**Status:** PLANNED. **Dependencies:** G64-072.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Recover final retained-ASM function in file_table.c and any shared data declaration constraints.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover final retained-ASM function in file_table.c and any shared data declaration constraints.
4. Recover 80001EB0 file reader arithmetic and call edges; record any nontrivial error/sentinel values.
5. Test table bounds for characterized valid inputs without adding different safety behaviour to original C.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Complete function-level ABI ledger, exact isolated comparison and G2 if qualified; otherwise unresolved ASM remains.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-074 — Characterize object list 80036308

**Status:** PLANNED. **Dependencies:** G64-012.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Use matched 800362DC and object_flags.h to derive next function's pointer iteration and flag updates.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_flags.c, decomp/object_flags.h, decomp/test_object_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Use matched 800362DC and object_flags.h to derive next function's pointer iteration and flag updates.
4. Use existing ObjectFlagOwner/ObjectFlagNode layouts as evidence for 80036308.
5. Trace linked-list mutation order and byte flag widths with pointer-null/one/many nodes.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A host linked-list test exercises empty/single/multiple nodes and keeps byte flags outside selected field unchanged.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-075 — Characterize object list 80036388

**Status:** PLANNED. **Dependencies:** G64-074.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Recover subsequent object_flags.c function and compare call/loop structure without assuming it is a flag setter.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_flags.c, decomp/object_flags.h, decomp/test_object_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover subsequent object_flags.c function and compare call/loop structure without assuming it is a flag setter.
4. Trace 80036388 branch predicates, link traversal and target flags without assuming identical semantics to 80036308.
5. Host-test preservation of unrelated bitfields and no-loop termination.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Observed behavior and pointer traversal proven from original instructions; test invalid-pointer assumptions are excluded.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-076 — Characterize object list 800363F4

**Status:** PLANNED. **Dependencies:** G64-075.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Reconstruct next object lifecycle routine; identify callback writes, ownership and memory allocation/free behavior.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_flags.c, decomp/object_flags.h, decomp/test_object_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Reconstruct next object lifecycle routine; identify callback writes, ownership and memory allocation/free behavior.
4. Trace 800363F4 state-callback effects and write order against original assembly.
5. Use mocks for callbacks that mutate the list during traversal.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Test callbacks and list tail/head mutation in synthetic memory; no live-game safety inference.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-077 — Characterize object list 80036448

**Status:** PLANNED. **Dependencies:** G64-076.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Complete this known four-function assembly neighborhood and check shared header field aliasing.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_flags.c, decomp/object_flags.h, decomp/test_object_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Complete this known four-function assembly neighborhood and check shared header field aliasing.
4. Trace 80036448 and determine whether it frees, clears or marks list nodes; no inferred ownership without evidence.
5. Assert null/sentinel path and original external call sequence.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** If functions match, all four pass same-unit IDO and full-ROM gate; otherwise preserve each separately as ASM.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-078 — Analyze scheduler 8000702C

**Status:** PLANNED. **Dependencies:** G64-002.
**Focus files:** `decomp/scheduler_queue.c`; `decomp/test_scheduler_queue.c`.

**Architectural intent:** Inspect func_8000702C_7C2C adjacent to matching pointer-offset helper 80007024 and characterize queue layout.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/scheduler_queue.c, decomp/test_scheduler_queue.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Inspect func_8000702C_7C2C adjacent to matching pointer-offset helper 80007024 and characterize queue layout.
4. Trace 8000702C scheduler queue link and head/tail mutations; compare exact SYS offsets.
5. Test empty, one element, multiple elements and callback-mutation cases.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Test empty/single/multiple queue cases and exact pointer arithmetic in a 32-bit host model.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-079 — Analyze scheduler 80007160

**Status:** PLANNED. **Dependencies:** G64-078.
**Focus files:** `decomp/scheduler_queue.c`; `decomp/test_scheduler_queue.c`.

**Architectural intent:** Recover second scheduler_queue.c ASM function; assess ordering, interrupt/state assumptions and alias relationships.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/scheduler_queue.c, decomp/test_scheduler_queue.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover second scheduler_queue.c ASM function; assess ordering, interrupt/state assumptions and alias relationships.
4. Trace 80007160 queue operations and any interrupt/state assumptions from actual MIPS.
5. Test order, sentinels and unchanged queue pointers for early returns.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Static and mocked call-order checks cover actual branches; G1 then G2 needed before promotion.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-080 — Gate files/object/scheduler batch

**Status:** PLANNED. **Dependencies:** G64-071, G64-072, G64-073, G64-074, G64-075, G64-076, G64-077, G64-078, G64-079.
**Focus files:** `decomp/file_table.c`; `decomp/object_flags.c`; `decomp/scheduler_queue.c`; `decomp/manifest.json`.

**Architectural intent:** Avoid combining independent failures in one manifest commit; integrate verified subsets with separate proofs.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/object_flags.c, decomp/scheduler_queue.c, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Avoid combining independent failures in one manifest commit; integrate verified subsets with separate proofs.
4. Integrate file, object and scheduler units separately behind current full-ROM gate.
5. Recompute inventory only after staged unit exactness; stop per unit on first mismatch.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Full-ROM exactness, preserved names/sections and function-specific host tests; record remaining caller graph gaps.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

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

**Status:** RESEARCH_ONLY. **Dependencies:** G64-017, G64-018.
**Focus files:** `decomp/file_table.c`; `decomp/test_file_table.c`.

**Architectural intent:** Map function's table base, index widths, mask and downstream callers without assuming identical semantics to adjacent 80001D68.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/file_table.c, decomp/test_file_table.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map function's table base, index widths, mask and downstream callers without assuming identical semantics to adjacent 80001D68.
4. Trace `80001DF4`'s full-width index, 8-byte table stride and bit-30 (`0x40000000`) return mask; distinguish these from sibling `80001D68`'s low-16-bit index and bit-31 clearing.
5. Record original word loads, branch structure and expected return type before writing candidate.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Document symbol references and test each table index/bit mask case before an exact candidate.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** the 92-byte reader uses the full-width input in an 8-byte-stride lookup and returns only bit 30 (`0x40000000`); its 96-byte helper is called first and may provide the same flag for type `0x11`. Three caller sites show two low-16-bit inputs and one unchanged input. The adjacent matched reader instead truncates to 16 bits, uses a 4-byte stride, and clears bit 31. A 92-byte IDO candidate first differed at `+0x24`; the explicit-goto variant grew to 96 bytes and regressed to `+0x1C`. Retain `GLOBAL_ASM`; G2 was not run. Full trace and hashes: `plans/execution/2026-11-11-g64-071-file-table-reader.json`.

### G64-072 — Inspect file-table reader 80001E50

**Status:** RESEARCH_ONLY. **Dependencies:** G64-071.
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

**Outcome (2026-11-13):** the 96-byte helper uses an unsigned 32-bit input, returns zero for input zero, returns `0xFF` for an empty table or at the zero-boundary sentinel, and otherwise returns byte `+3` from the first four-byte record whose unsigned halfword boundary at `+0` exceeds the input. Equality advances to the next record; the routine has no independent count or bounds check. All ten direct callers were inspected. Three bounded IDO candidates linked at the original VMA were 112 bytes and first differed at `+0x04` in the zero-input branch delay slot. Retain `GLOBAL_ASM`; G2 was not run. Full evidence: `plans/execution/2026-11-13-g64-072-file-table-helper.json`.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-073 — Inspect file-table reader 80001EB0

**Status:** RESEARCH_ONLY. **Dependencies:** G64-072=RESEARCH_ONLY.
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

**Outcome (2026-11-13):** `func_80001EB0_2AB0` is 312 bytes / 78 words at VMA `0x80001EB0` and ROM offset `0x2AB0`; the full span matches the pinned USA ROM. It calls `80001DF4` as a zero/nonzero gate, then uses an eight-byte pair at `D_80054ACC_556CC` to derive an inclusive `0x2000` page range. Each mapping slot is checked and updated before the six-argument `osMapTLB` call. Both callers ignore the zero return. The direct caller's constant index 60 selects row 59; the dynamic caller supplies a halfword index. The table extent is undeclared in the pinned source, and no bound check appears in the target. Two IDO candidates linked at the original VMA but both first differed at `+0x04` in saved-register/argument-mask scheduling (304 and 320 bytes versus 312); calls and global relocations resolved. Keep `GLOBAL_ASM`; whole-unit G2 and inventory were not run. See `plans/execution/2026-11-13-g64-073-file-table-mapper.json`.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-074 — Characterize object dispatcher 80036308

**Status:** PASSED_G2. **Dependencies:** G64-012.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Use the matched 800362DC neighbor and pinned MIPS to distinguish this per-node dispatcher from list traversal.

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

**Explicit acceptance:** Test the dispatcher's original single-node flag selection, helper order, default paths and null behavior; document return-register behavior from MIPS, where all direct callers ignore it. The adjacent 800362DC separately covers empty/single/multiple-node traversal.

**Required negative control:** Preserve actual list termination, mutation order, signed/unsigned table arithmetic and atomicity; do not introduce a safety check that changes original native code.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Outcome (2026-11-13):** Pinned MIPS shows `func_80036308_36F08` is a 128-byte per-node dispatcher, not a list walker. It loads node byte `+4`, selects on `flags & 0x7F`, and dispatches kinds 1–3 to four helpers in the observed order; kind 4/default and null follow their original return paths. All nine direct callers ignore the result. Host tests cover the dispatch table and null/default behavior; the neighboring `func_800362DC_36EDC` keeps the empty/single/multiple linked-list coverage. One pinned IDO candidate matched all 128 bytes in the integrated source unit. Fresh full-ROM G2 matched 149/149 claims and all 33,554,432 bytes; inventory now records 149 matching C and 7,214 remaining ASM entries. See `plans/execution/2026-11-13-g64-074-object-flags.json`.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-075 — Characterize object list 80036388

**Status:** RESEARCH_ONLY. **Dependencies:** G64-074.
**Focus files:** `decomp/object_flags.c`; `decomp/object_flags.h`; `decomp/test_object_flags.c`.

**Architectural intent:** Recover the move-to-front operation and its caller-established non-head membership precondition from pinned MIPS.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/object_flags.c, decomp/object_flags.h, decomp/test_object_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Recover the existing-entry search and move-to-head operation without inferring a flag setter.
4. Trace the owner head at +0x78, entry link at +0x74, null guards, caller membership condition and relink order.
5. Host-test null arguments, empty/singleton caller gates, valid two/three-node moves and lookup-key preservation; do not call the function with an absent entry.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Prove observed pointer traversal and relink order; test only caller-valid list members, with empty/singleton caller paths terminating before this function and invalid membership excluded.

**Required negative control:** Reject a broken predecessor relink or changed move-to-front order; do not invent absent-entry safety or test pointers outside the caller-established membership contract.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Outcome (2026-11-13):** `func_80036388_36F88` is 108 bytes / 27 words at VMA `0x80036388`, ROM offset `0x36F88`; all words match the pinned USA ROM. It reads the list head at owner `+0x78` and link pointers at entry `+0x74`. Its sole caller (`func_80018F3C_19B3C`) checks the head separately, scans from `head->next` with a null terminator, and calls this function only after finding a matching non-head entry. The target removes that entry from its prior position, places it at the head and returns 1; null owner/entry return 0. It has no callback. Host reference cases cover empty/singleton caller gates, nulls, valid two/three-node moves, relink order and key preservation; absent-entry calls are excluded. Three IDO candidates linked at the original VMA at 112, 96 and 104 bytes; all first differed at `+0x00`, where guard polarity/scheduling remained different. Stop at the three-variant limit and retain `GLOBAL_ASM`. No source-unit exact build, full-ROM G2 or inventory was run; stored proof remains 149/149 functions / 11,148 bytes. See `plans/execution/2026-11-13-g64-075-object-list-move-to-front.json`.

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

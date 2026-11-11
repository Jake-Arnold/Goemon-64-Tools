# Phase 10 — Proof automation and camera

**Scope:** G64-091–G64-100; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/batch.py`
- `decomp/probe.py`
- `decomp/verify.py`
- `decomp/inventory.py`
- `decomp/compare_original.py`
- `decomp/LOCAL_MNSG_REVIEW.md`
- `decomp/MASTER_WORK_QUEUE.md`

## Known phase risks and negative controls
Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

## Task work packages

### G64-091 — Define candidate evidence ledger

**Status:** PLANNED. **Dependencies:** G64-003, G64-020.
**Focus files:** `decomp/manifest.json`; `decomp/results/combined.json`; `decomp/results/inventory.json`; `decomp/batch.py`.

**Architectural intent:** Standardize per-function entries: unit, original size/VMA/ROM, candidate hash, exactness tier, tests, failed words, blocker, proof run.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/manifest.json, decomp/results/combined.json, decomp/results/inventory.json, decomp/batch.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Standardize per-function entries: unit, original size/VMA/ROM, candidate hash, exactness tier, tests, failed words, blocker, proof run.
4. Extend the candidate ledger to record source hash, ROM identity, original size, VMA, exactness tier, test results and failure signature.
5. Do not rewrite historical evidence; emit a new entry per attempt with immutable IDs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Schema rejects missing original provenance and conflation of isolated/whole-ROM matches; prior reports can be imported without rewriting history.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-092 — Rank research by evidence not byte size

**Status:** PLANNED. **Dependencies:** G64-050, G64-080, G64-090.
**Focus files:** `decomp/batch.py`; `decomp/MASTER_WORK_QUEUE.md`.

**Architectural intent:** Extend batch queue selection beyond prior 762 scalar attempts using reviewed type context, callers, known exact siblings and bounded expected effort.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/batch.py, decomp/MASTER_WORK_QUEUE.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Extend batch queue selection beyond prior 762 scalar attempts using reviewed type context, callers, known exact siblings and bounded expected effort.
4. Score candidates using reviewed types, nearby matching C, known blockers and full-unit likelihood, not simply byte length.
5. Exclude 762 prior unchanged scalar trials and promoted manifest members.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Dry-run plan contains only unpromoted symbols and stable recipe hashes; rerun unchanged recipes excluded by default.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-093 — Reuse typed C context safely

**Status:** PLANNED. **Dependencies:** G64-022, G64-061, G64-074.
**Focus files:** `decomp/script_vm.h`; `decomp/object_flags.h`; `decomp/batch_context.h`.

**Architectural intent:** Create versioned, declaration-only context bundles for VM, object, scene and math families with source evidence references.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.h, decomp/object_flags.h, decomp/batch_context.h. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Create versioned, declaration-only context bundles for VM, object, scene and math families with source evidence references.
4. Version each typed context and record a source/assembly justification for every field width.
5. A context change invalidates downstream isolated proof cached under old type hashes.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Context changes invalidate old isolated proof identity; compilation tests flag conflicting types and unexpected symbol changes.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-094 — Classify native codegen failures

**Status:** PLANNED. **Dependencies:** G64-011, G64-023, G64-032, G64-044.
**Focus files:** `decomp/compare_original.py`; `decomp/probe.py`; `decomp/test_compare_original.py`.

**Architectural intent:** Provide mismatch categories (size, register, delay slot, relocation, padding, symbol, section, original-boundary), with first differing instruction.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/compare_original.py, decomp/probe.py, decomp/test_compare_original.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Provide mismatch categories (size, register, delay slot, relocation, padding, symbol, section, original-boundary), with first differing instruction.
4. Classify mismatches into size, register, branch likely, delay slot, relocation, VMA, rodata, alignment, symbol and stale reference.
5. Require a parser test that deliberately injects every class and fails without a false success.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Parser unit tests intentionally inject each failure and assert fail-closed classifications; no mask-based false positives.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-095 — Harden automated proof regression

**Status:** PLANNED. **Dependencies:** G64-003, G64-051, G64-052, G64-053, G64-054, G64-055.
**Focus files:** `decomp/verify.py`; `decomp/inventory.py`; `tests/test_decomp_verify.py`.

**Architectural intent:** Compose CI-capable structural/host checks plus an optional private local-ROM gate without uploading ROM or generated bytes.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/verify.py, decomp/inventory.py, tests/test_decomp_verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Compose CI-capable structural/host checks plus an optional private local-ROM gate without uploading ROM or generated bytes.
4. Run public pure-Python/host tests without proprietary ROM; gate private-ROM full verifier separately only on user environment.
5. No CI job may upload ROM, generated assembly, raw memory, or binary compiler archives.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Public jobs never need proprietary assets; private gate rejects modified ROM, shifted function bytes and stale proof hashes.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-096 — Inventory upstream camera research

**Status:** PLANNED. **Dependencies:** G64-055.
**Focus files:** `decomp/LOCAL_MNSG_REVIEW.md`; `decomp/overlay_file43.py`.

**Architectural intent:** Review pinned mnsg camera branch f1a86c3, compare original overlay source symbols with current main baseline; treat all camera C as unverified.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/LOCAL_MNSG_REVIEW.md, decomp/overlay_file43.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Review pinned mnsg camera branch f1a86c3, compare original overlay source symbols with current main baseline; treat all camera C as unverified.
4. Read pinned upstream camera branch f1a86c328be09d2d35a8d0817bd41e67783d343a as a research reference only.
5. Index its ~4,600 source lines and provisional structures by actual overlay function and original assembly ownership.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Separate evidence index lists already known structure hints, unresolved C functions and version-specific constraints; nothing merged.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-097 — Resolve camera initializer C mismatch

**Status:** PLANNED. **Dependencies:** G64-096.
**Focus files:** `decomp/LOCAL_MNSG_REVIEW.md`; `decomp/compare_original.py`.

**Architectural intent:** Investigate 8001D27A4_58E6B4 link failure from unexpected memset call against original inline clearing loop.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/LOCAL_MNSG_REVIEW.md, decomp/compare_original.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Investigate 8001D27A4_58E6B4 link failure from unexpected memset call against original inline clearing loop.
4. Trace camera initializer 080? / 8001D27A4_58E6B4 unexpected memset link failure to original inline clearing loop.
5. Correct source-level loop and compare IDO output; no linker alias or synthesized memset is an acceptable workaround.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Native codegen research eliminates unsupported memset without linker alias patches; no promotion until original overlay ROM proof.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-098 — Design camera subset promotion process

**Status:** PLANNED. **Dependencies:** G64-055, G64-096, G64-097.
**Focus files:** `decomp/overlay_file43.py`; `decomp/manifest.json`.

**Architectural intent:** Choose smallest independently bounded camera functions with known ROM/VMA, types and original assembly; isolate from mass 4,600-line import.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/overlay_file43.py, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Choose smallest independently bounded camera functions with known ROM/VMA, types and original assembly; isolate from mass 4,600-line import.
4. Choose a bounded camera subset with independently verified function extents and known overlay mapping.
5. Do not merge entire camera branch or claim a function by source volume; require complete overlay-ROM proof.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Candidates are individually original-address verified and full-ROM accepted; camera branch not merged wholesale or counted by source lines.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-099 — Re-baseline architecture after each phase

**Status:** PLANNED. **Dependencies:** G64-010, G64-020, G64-030, G64-040, G64-050, G64-060, G64-070, G64-080, G64-090.
**Focus files:** `decomp/manifest.json`; `decomp/results/combined.json`; `decomp/results/inventory.json`; `PROGRESS.md`.

**Architectural intent:** Compare live branch, manifest, proof and residual ASM with planned targets; drop already promoted or invalid targets and re-rank blockers.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/manifest.json, decomp/results/combined.json, decomp/results/inventory.json, PROGRESS.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Compare live branch, manifest, proof and residual ASM with planned targets; drop already promoted or invalid targets and re-rank blockers.
4. After each phase, re-read live branch and manifest; mark tasks already promoted or invalid without running them.
5. Recalculate total bytes/functions from proof rather than assumed milestone arithmetic.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** A dated delta report contains achieved promotions, failed/blocked steps, revised critical path and no duplicated work.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-100 — Publish executor-ready next-wave contract

**Status:** PLANNED. **Dependencies:** G64-091, G64-092, G64-093, G64-094, G64-095, G64-096, G64-097, G64-098, G64-099.
**Focus files:** `decomp/CONTINUE.md`; `decomp/MASTER_WORK_QUEUE.md`; `PROGRESS.md`.

**Architectural intent:** Create final architecture decision record, dependency DAG, prioritized new ten-target tranche and explicit tool/ROM proof contract; edit only decomp branch docs.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/CONTINUE.md, decomp/MASTER_WORK_QUEUE.md, PROGRESS.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Create final architecture decision record, dependency DAG, prioritized new ten-target tranche and explicit tool/ROM proof contract; edit only decomp branch docs.
4. Write final next-ten execution queue with exact source symbols, original hashes, confidence and required tests.
5. Update operational CONTINUE.md with current actionable queue, preserving prior provenance and failed attempt history.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest tests.test_decomp_verify tests.test_decomp_batch tests.test_decomp_probe_integration tests.test_decomp_inventory -q` plus affected test files. No real-ROM pass is implied without a separate invocation.

**Explicit acceptance:** Future executor can identify unambiguous target, required inputs, exact stop conditions and acceptance tests without relying on chat history.

**Required negative control:** Evidence automation may only surface claims, never automatically promote candidates without current source ownership and complete-ROM proof. Keep private assets outside Git.

**Stop/recovery:** Documentation, static analysis and tool work never change the matching-C count. Add negative tests before making validation policy changes. Record any unrun private-ROM test as NOT_RUN, never PASS.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

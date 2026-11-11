# Phase 03 — VM resource path

**Scope:** G64-021–G64-030; branch `chatgptweb/decomp`; phase execution began at `907e86bc04e3abccb902c742813eb2e5406b2cd9` (refresh before each task).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/script_vm.c`
- `decomp/script_vm.h`
- `decomp/VM_CHECKPOINT.md`
- `decomp/MASTER_WORK_QUEUE.md`
- `decomp/candidates/vm_resource_halfword_volatile_probe.c`
- `decomp/candidates/vm_loader_storage_probe.c`

## Known phase risks and negative controls
Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

## Task work packages

### G64-021 — Map resource call graph

**Status:** DOC_ONLY. **Dependencies:** G64-002.
**Focus files:** `decomp/script_vm.c`; `decomp/script_vm.h`; `decomp/VM_CHECKPOINT.md`.

**Architectural intent:** Trace script_vm.c unresolved 8003D468, 8003D68C, 8003F038 and matched 8003DDC4, plus resource table callees and callback side effects.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/script_vm.h, decomp/VM_CHECKPOINT.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Trace script_vm.c unresolved 8003D468, 8003D68C, 8003F038 and matched 8003DDC4, plus resource table callees and callback side effects.
4. Inventory VM resource call edges around func_8003D468, func_8003DDC4, func_8003F038, callback recovery, and current global IDs.
5. Separate resource lookup, validation, recovery and cursor relocation paths before declaring types.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A call graph labels verified vs inferred signatures, global reads, side effects, and private ROM evidence links.

**Outcome:** Accepted as `DOC_ONLY`; see [VM_RESOURCE_CALLGRAPH.md](../../VM_RESOURCE_CALLGRAPH.md) and `plans/execution/2026-11-11-g64-021-resource-callgraph.json`. The ROM-derived listing records five exact function extents and hashes, all checked against the private decompressed image. The unknown `13B14` callback effects remain explicitly unclaimed.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-022 — Define narrow VM resource types

**Status:** RESEARCH_ONLY. **Dependencies:** G64-021.
**Focus files:** `decomp/script_vm.h`; `decomp/candidates/vm_loader_storage_probe.c`.

**Outcome (2026-11-11):** Added `VmResourceId` and `VmResourceContext` with
only observed widths/offsets; the +4/+8 words remain offset-annotated because
their meanings are not established. Host endian/static assertions, both loader
harnesses, and all 114 decomp Python tests passed. Pinned IDO produced a
556-byte isolated candidate against the 548-byte original; comparison had
1/26 matching nonrelocation positions, 46/58 matching relocation shapes, 53
relocation-layout differences, and first mismatch at +0x8. Keep the production
function as `GLOBAL_ASM`. A fresh verifier still matched all 148 existing
claims and the complete ROM; no claim was promoted. See
`plans/execution/2026-11-11-g64-022-resource-types.json`.

**Architectural intent:** Propose confirmed-only structures and scalar widths in script_vm.h/support context; encode low-half big-endian resource-ID semantics.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.h, decomp/candidates/vm_loader_storage_probe.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Propose confirmed-only structures and scalar widths in script_vm.h/support context; encode low-half big-endian resource-ID semantics.
4. Type only byte/halfword/word widths justified by original loads and writes; annotate unknown fields with offsets.
5. Include distinct names for VM entry ID and live mutable global resource ID; reject a single aliased abstraction.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Offset/static assertions and host-width/endian tests pass; no invented field can silently propagate into matching functions.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-023 — Reproduce lookup candidate baseline

**Status:** PLANNED. **Dependencies:** G64-022.
**Focus files:** `decomp/candidates/vm_resource_halfword_volatile_probe.c`; `decomp/test_vm_resource_halfword_volatile_probe.py`.

**Architectural intent:** Replay volatile signed-half-index 8003F038_3FC38 (196 bytes, historically 25/42 comparable positions); identify register and relocation mismatches.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_resource_halfword_volatile_probe.c, decomp/test_vm_resource_halfword_volatile_probe.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Replay volatile signed-half-index 8003F038_3FC38 (196 bytes, historically 25/42 comparable positions); identify register and relocation mismatches.
4. Use the 196-byte volatile-half-index research candidate as the reference and reproduce 25/42 directly comparable positions.
5. Confirm native IDO -c output and the three relocation shapes from the SHA-verified original, without falsely calling it exact.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Native object is compared with original ROM, not reassembled text; every mismatch classified and baseline measurement reproducible.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-024 — Refine lookup code generation

**Status:** PLANNED. **Dependencies:** G64-023.
**Focus files:** `decomp/candidates/vm_resource_halfword_volatile_probe.c`; `decomp/compare_original.py`.

**Architectural intent:** Focus original $v1 index, stack slot, signed truncation, 0x100 bypass, callback recovery and shift/wrap effects; vary one factor per attempt.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_resource_halfword_volatile_probe.c, decomp/compare_original.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Focus original $v1 index, stack slot, signed truncation, 0x100 bypass, callback recovery and shift/wrap effects; vary one factor per attempt.
4. Focus on original v1 half-index register versus candidate t6, original spilled argument placement and four relocation-layout differences.
5. Change one declaration or lifetime at a time; run signed-half-index, recovery and overflow behavior tests after every promising source change.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Exact original 196 bytes or an explicit failed bounded result; 3,000 synthetic cases and relocation checks remain mandatory.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-025 — Model loader entry-versus-current ID

**Status:** PLANNED. **Dependencies:** G64-021, G64-022.
**Focus files:** `decomp/candidates/vm_loader_storage_probe.c`; `decomp/test_vm_loader_resource_mutation.c`.

**Architectural intent:** For 8003D468_3E068 preserve entry ID sent to 8003DDC4, while resource globals may mutate on two callbacks.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_loader_storage_probe.c, decomp/test_vm_loader_resource_mutation.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: For 8003D468_3E068 preserve entry ID sent to 8003DDC4, while resource globals may mutate on two callbacks.
4. Simulate callback 1 and callback 2 independently mutating the global resource ID between reads.
5. Preserve original entry ID for func_8003DDC4 while later global reloads use their current mutated values.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** 1,024-case mutation harness catches stale cached reads, and low-half accessor tests match N64 big-endian semantics.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-026 — Resolve loader ABI and frame

**Status:** PLANNED. **Dependencies:** G64-025.
**Focus files:** `decomp/candidates/vm_loader_storage_probe.c`; `decomp/test_vm_loader_original.py`.

**Architectural intent:** Recover original 548-byte 8003D468 stack layout ($s0/$s1) and 32-byte frame; test typed prefix and aliased global loads.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/vm_loader_storage_probe.c, decomp/test_vm_loader_original.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover original 548-byte 8003D468 stack layout ($s0/$s1) and 32-byte frame; test typed prefix and aliased global loads.
4. Recover exact MIPS stack frame and saved s0/s1 lifetimes from original loads and calls.
5. Do not accept previous 560-byte candidate against the 548-byte original; use a complete original-address comparison.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Pinned native output reproduces each identified load/call/order; a 548-byte length alone does not count as a match.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-027 — Trace VM main-step 8003D68C

**Status:** PLANNED. **Dependencies:** G64-021.
**Focus files:** `decomp/script_vm.c`; `decomp/VM_CHECKPOINT.md`.

**Architectural intent:** Recover CFG, live state and authoritative declarations for unresolved func_8003D68C_3E28C before writing C; identify callbacks and exit paths.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/VM_CHECKPOINT.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover CFG, live state and authoritative declarations for unresolved func_8003D68C_3E28C before writing C; identify callbacks and exit paths.
4. Trace 8003D68C entry, callback order, exit paths and VM work-state mutations using original assembly.
5. Do not invent script opcode semantics from a single call-site, and do not count research-only semantic models.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Document complete instruction/branch map, input/output contract, and a host-model test matrix; no speculative matching claim.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-028 — Trace VM control decoder 8003DF98

**Status:** PLANNED. **Dependencies:** G64-027.
**Focus files:** `decomp/script_vm.c`; `decomp/VM_STREAM_MATCHING.md`.

**Architectural intent:** Recover command delegation and cursor rules for func_8003DF98_3EB98, as called by existing stream walker.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/VM_STREAM_MATCHING.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover command delegation and cursor rules for func_8003DF98_3EB98, as called by existing stream walker.
4. Trace signed negative stream-token handling delegated to 8003DF98 and its caller obligations.
5. Record whether marker/repeat and current pointer values are read before or after callbacks.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** For every negative-token family, static evidence defines cursor movement, return value and external side effects; unsafe inputs remain undefined.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-029 — Guard already matching resource decoder

**Status:** PLANNED. **Dependencies:** G64-025, G64-028.
**Focus files:** `decomp/script_vm.c`; `decomp/test_vm_loader_resource_mutation.c`.

**Architectural intent:** Add regression coverage for 8003DDC4_3E9C4's retry behavior and resource-ID mutation before changing shared types.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/script_vm.c, decomp/test_vm_loader_resource_mutation.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Add regression coverage for 8003DDC4_3E9C4's retry behavior and resource-ID mutation before changing shared types.
4. Use the already matching resource decoder as a regression invariant when staging nearby VM C.
5. Test callback mutation and original resource-ID preservation; require no changes to previously accepted words.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Existing matching machine code/hash unchanged; mutation tests intentionally fail when global ID is incorrectly cached.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-030 — VM resource checkpoint

**Status:** PLANNED. **Dependencies:** G64-024, G64-026, G64-027, G64-028, G64-029.
**Focus files:** `decomp/MASTER_WORK_QUEUE.md`; `decomp/results/combined.json`.

**Architectural intent:** Stage only exact candidates in the original script_vm.c context; leave unresolved VM helpers as ASM.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/MASTER_WORK_QUEUE.md, decomp/results/combined.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Stage only exact candidates in the original script_vm.c context; leave unresolved VM helpers as ASM.
4. Produce a typed VM interface matrix with evidence levels for every field and address.
5. Publish only function-level G2-verified matches; unresolved lookup/loader code stays as ASM.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Each selected function passes original guest address, full-ROM identity and inventory; otherwise close as research-only with precise next blocker.

**Required negative control:** Callbacks may mutate the current global resource ID. Tests must distinguish it from the entry ID, reject signedness/halfword mistakes, and keep existing matching siblings byte-identical.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

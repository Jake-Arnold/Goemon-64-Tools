# Phase 06 — Overlays and file_43

**Scope:** G64-051–G64-060; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/overlay_file43.py`
- `decomp/test_overlay_file43.py`
- `decomp/NEXT_FIVE_ACTIONS.md`
- `decomp/GHOST_TOYS_CHECKPOINT.md`
- `decomp/candidates/key_spawn_gate.c`
- `decomp/candidates/ghost_probe.c`

## Known phase risks and negative controls
Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

## Task work packages

### G64-051 — Specify overlay manifest schema

**Status:** DOC_ONLY. **Dependencies:** G64-003.
**Focus files:** `decomp/manifest.json`; `decomp/verify.py`; `tests/test_decomp_verify.py`.

**Architectural intent:** Model segment ID, ROM ranges, VMA, text/rodata boundaries, relocation provenance and source ownership distinct from main-segment linear map.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/manifest.json, decomp/verify.py, tests/test_decomp_verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Model segment ID, ROM ranges, VMA, text/rodata boundaries, relocation provenance and source ownership distinct from main-segment linear map.
4. Model explicit overlay ID, ROM start/end, VMA start/end, text/rodata/data mapping and alignment in a new manifest contract.
5. Keep main-segment map unaffected and reject unrecognized overlay forms rather than inferring an offset formula.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Schema rejects main VMA formula on overlays, duplicate overlays/functions, negative ranges and cross-segment overlap.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-052 — Promote file_43 reference guard to input contract

**Status:** PLANNED. **Dependencies:** G64-051.
**Focus files:** `decomp/overlay_file43.py`; `decomp/test_overlay_file43.py`.

**Architectural intent:** Reuse overlay_file43.py's pinned 0x6F34E0..0x6FB200 layout and original section SHA-256 evidence.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/overlay_file43.py, decomp/test_overlay_file43.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Reuse overlay_file43.py's pinned 0x6F34E0..0x6FB200 layout and original section SHA-256 evidence.
4. Use existing file_43 guard: ROM 0x6F34E0, text end 0x6F9CE0, end 0x6FB200 and VMA 0x08000000.
5. Require SHA-verified original 32 MiB image and section fingerprints before any candidate ELF proof.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Tests reject changed Splat segment order, 0x08000000 VMA, section hashes, wrong ROM length or wrong source SHA-1.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-053 — Add overlay linked-ELF provenance

**Status:** PLANNED. **Dependencies:** G64-051, G64-052.
**Focus files:** `decomp/overlay_file43.py`; `decomp/verify.py`; `decomp/elf_layout.py`.

**Architectural intent:** Design section/symbol extraction from original and candidate overlay ELF, explicitly binding each function to ROM and original load address.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/overlay_file43.py, decomp/verify.py, decomp/elf_layout.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Design section/symbol extraction from original and candidate overlay ELF, explicitly binding each function to ROM and original load address.
4. Bind each overlay function claim to linked ELF symbol/section and original ROM offsets, checking relocation records.
5. Reject a candidate that matches bytes in the wrong overlay VMA or whose target section differs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** A shifted VMA, mismatched relocation target, missing symbol or wrong section size fails before any function claim.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-054 — Expand fail-closed overlay tests

**Status:** PLANNED. **Dependencies:** G64-052, G64-053.
**Focus files:** `decomp/test_overlay_file43.py`; `tests/test_decomp_elf_layout.py`.

**Architectural intent:** Create mutation fixtures for text/rodata padding, aliases, duplicate function bounds, symbol-size lies and altered undefined relocations.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_overlay_file43.py, tests/test_decomp_elf_layout.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Create mutation fixtures for text/rodata padding, aliases, duplicate function bounds, symbol-size lies and altered undefined relocations.
4. Add tests for wrong file_43 identifier, rodata shift, padding, overlap, duplicate functions and altered ROM SHA.
5. Use known valid overlay fixture as control; each deliberately corrupted fixture must fail.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Each intentionally corrupted fixture fails, while untouched main-segment verifier continues passing its existing regression suite.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-055 — Define overlay integration adapter

**Status:** PLANNED. **Dependencies:** G64-053, G64-054.
**Focus files:** `decomp/verify.py`; `decomp/manifest.json`; `decomp/overlay_file43.py`.

**Architectural intent:** Stage overlay Splat split and C replacement as a guarded capability in verify.py, leaving existing main-path behavior unchanged.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/verify.py, decomp/manifest.json, decomp/overlay_file43.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Stage overlay Splat split and C replacement as a guarded capability in verify.py, leaving existing main-path behavior unchanged.
4. Implement a staging adapter that replaces only exact overlay ASM ownership and restores verified section boundaries.
5. Full build must still link main segment and all overlay objects; do not special-case output bytes for a match.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Exact overlay object placement and generated assembly ownership established; complete ROM comparison cannot be bypassed.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-056 — Prepare key initializer replacement

**Status:** PLANNED. **Dependencies:** G64-055.
**Focus files:** `decomp/candidates/key_spawn_gate.c`; `decomp/test_key_spawn_gate.c`.

**Architectural intent:** Review func_080001BC_6F369C (96 bytes), task +0xD4, saved key flag, callback and unknown external symbols in the real overlay.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/key_spawn_gate.c, decomp/test_key_spawn_gate.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Review func_080001BC_6F369C (96 bytes), task +0xD4, saved key flag, callback and unknown external symbols in the real overlay.
4. Place 96-byte key initializer into file_43 only after linked overlay proofs exist.
5. Trace task +0xD4 field, engine callback addresses and original pointers; do not promote old isolated link.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Existing isolated 96-byte match reproduces in original overlay context; recovered signature/field widths have instruction evidence.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-057 — Prove key initializer semantics

**Status:** PLANNED. **Dependencies:** G64-056.
**Focus files:** `decomp/test_key_spawn_gate.c`; `decomp/overlay_file43.py`.

**Architectural intent:** Test key-collected and not-collected host callback flow, task-state update and unchanged sentinel fields.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_key_spawn_gate.c, decomp/overlay_file43.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Test key-collected and not-collected host callback flow, task-state update and unchanged sentinel fields.
4. Host-test both collected and uncollected key flag paths plus callback assignment and untouched task fields.
5. Check 96/96 target bytes and full image when production-staged.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Key cases and control-flow guards pass, and no key spawn or game-memory edit is introduced into toolkit features.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-058 — Resolve Ghost Toys entrance spill

**Status:** PLANNED. **Dependencies:** G64-055.
**Focus files:** `decomp/candidates/ghost_probe.c`; `decomp/GHOST_TOYS_CHECKPOINT.md`.

**Architectural intent:** For func_08006490_6F9970 (140 bytes), isolate sp+0x1C original vs sp+0x18 candidate store/reload; preserve pointer lifetime.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/candidates/ghost_probe.c, decomp/GHOST_TOYS_CHECKPOINT.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: For func_08006490_6F9970 (140 bytes), isolate sp+0x1C original vs sp+0x18 candidate store/reload; preserve pointer lifetime.
4. For 140-byte Ghost Toys entry, compare original sp+0x1C save/reload with candidate sp+0x18 at exactly two words.
5. Change pointer liveness or legitimate source ABI, never manually patch stack displacements or MIPS instructions.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Exact original 35 words and both spill operands arise from reviewed native IDO source, not manual opcode patching.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-059 — Prove Ghost event logic

**Status:** PLANNED. **Dependencies:** G64-058.
**Focus files:** `decomp/test_ghost_probe.c`; `decomp/GHOST_TOYS_CHECKPOINT.md`.

**Architectural intent:** Model flags 0x19A/0x19B gate, writing 0x19C, task +0x60 bit, helper argument 0x224 and callback replacement.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/test_ghost_probe.c, decomp/GHOST_TOYS_CHECKPOINT.md. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Model flags 0x19A/0x19B gate, writing 0x19C, task +0x60 bit, helper argument 0x224 and callback replacement.
4. Test flags 0x19A and 0x19B gating 0x19C, task +0x60 bit 0, argument 0x224 and callback 0800651C.
5. Assert no flags are written on failing preconditions and call order is exact.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest decomp.test_overlay_file43 -q`; for any section/ELF adapter changes run `python3 -m unittest tests.test_decomp_verify tests.test_decomp_elf_layout -q`. Both original section hashes and full-ROM equality must hold for promotion.

**Explicit acceptance:** Both precondition branches and callback sequence pass host tests; missing/unknown field assumptions recorded explicitly.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-060 — Gate overlay promotions

**Status:** PLANNED. **Dependencies:** G64-055, G64-056, G64-057, G64-058, G64-059.
**Focus files:** `decomp/manifest.json`; `decomp/verify.py`; `decomp/inventory.py`.

**Architectural intent:** Rebuild complete ROM with individual or combined overlay C candidates; compare original-address bytes, full image and total symbol inventory.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/manifest.json, decomp/verify.py, decomp/inventory.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Rebuild complete ROM with individual or combined overlay C candidates; compare original-address bytes, full image and total symbol inventory.
4. Only promote verified overlay symbols after complete Splat/IDO/ELF/ROM gate and inventory with no main regressions.
5. Retain incomplete overlay work as research and keep both original ASM functions if proof is unavailable.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Only functions with exact overlay provenance and whole-ROM identity gain matching counts; no claim if overlay adapter or linker fails.

**Required negative control:** Do not use the main-segment ROM/VMA formula for overlays; reject section aliasing, overlap, hash mismatch and isolated byte matches as promotions.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

## Optional read-only REA research lane for this phase

**Not mandatory.** Begin with [REA_PILOT.md](../REA_PILOT.md), which requires an actual Goemon ELF admission check and the 10-control benchmark before native provider output is treated as useful evidence. Goemon's pinned `-mips2` compilation is outside REA's listed standard MIPS ISA support unless the *actual* linked ELF and provider demonstrate otherwise. No original ELF was inspected here.

If REA refuses the Goemon binary, record `REA_UNSUPPORTED_GOEMON` and continue ordinary original MIPS / m2c / IDO / full-ROM steps. Do not forge ELF header flags, suppress provider refusal or treat direct Ghidra observations as a passing REA benchmark. Selected G64 tasks have optional per-task evidence fields in `TASKS_100.json`. **No REA output alone may promote C.**

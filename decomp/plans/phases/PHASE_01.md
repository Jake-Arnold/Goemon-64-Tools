# Phase 01 — Baseline and near-ready promotions

**Scope:** G64-001–G64-010; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `AGENTS.md`
- `decomp/CONTINUE.md`
- `decomp/NEXT_TWENTY_STEPS.md`
- `decomp/manifest.json`
- `decomp/resource_dispatch.c`
- `decomp/empty_menu_hook.c`
- `decomp/prove_integrated_units.py`
- `decomp/results/combined.json`
- `decomp/results/inventory.json`

## Known phase risks and negative controls
Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

## Task work packages

### G64-001 — Freeze live authority

**Status:** PASSED_G2. **Dependencies:** baseline live branch verification.
**Focus files:** `AGENTS.md`; `decomp/CONTINUE.md`; `decomp/manifest.json`; `decomp/results/combined.json`; `decomp/results/inventory.json`.

**Architectural intent:** Record chatgptweb/decomp HEAD, AGENTS.md, CONTINUE.md, manifest, combined/inventory hashes and six ASM placeholder identities; segregate dated historical notes.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: AGENTS.md, decomp/CONTINUE.md, decomp/manifest.json, decomp/results/combined.json, decomp/results/inventory.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Record chatgptweb/decomp HEAD, AGENTS.md, CONTINUE.md, manifest, combined/inventory hashes and six ASM placeholder identities; segregate dated historical notes.
4. Read each current result's format, status, source-hash and count fields rather than copying a historical checkpoint.
5. Query the remote branch immediately before work; save HEAD, upstream commit, and the six unpromoted function names in a sanitized scratch record.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A machine-readable checkpoint has 142 claimed functions, 10,652 matched bytes, 155 C entries, 7,221 ASM entries, and no promoted candidate among the six.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-002 — Validate claim ownership

**Status:** PASSED_G2. **Dependencies:** G64-001.
**Focus files:** `decomp/manifest.json`; `decomp/verify.py`; `tests/test_decomp_verify.py`.

**Architectural intent:** Define one-to-one mapping of ROM offset/VMA, function name, translation unit, C owner or retained ASM; guard existing-source patch and no-padding exceptions.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/manifest.json, decomp/verify.py, tests/test_decomp_verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Define one-to-one mapping of ROM offset/VMA, function name, translation unit, C owner or retained ASM; guard existing-source patch and no-padding exceptions.
4. Build a manifest ownership table keyed by ROM start, end, guest VMA, function name, and owner type.
5. Add negative tests for duplicated claims, missing retained assembly markers and any overlap; keep the reviewed 27FE0.c collision patch exceptional and hash-pinned.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Reject duplicates, missing ASM ownership, overlapping extents, changed patch hashes and false promotions in synthetic manifest fixtures.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-003 — Specify proof tiers

**Status:** SKIPPED_ALREADY_COMPLETE. **Dependencies:** G64-001, G64-002.
**Focus files:** `decomp/verify.py`; `decomp/inventory.py`; `decomp/compare_original.py`; `decomp/prove_integrated_units.py`.

**Architectural intent:** Document G0 source/ROM provenance, G1 semantic + isolated codegen, G2 full translation-unit and complete-ROM verification, G3 inventory/regression/publication.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/verify.py, decomp/inventory.py, decomp/compare_original.py, decomp/prove_integrated_units.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Document G0 source/ROM provenance, G1 semantic + isolated codegen, G2 full translation-unit and complete-ROM verification, G3 inventory/regression/publication.
4. Create distinct evidence states PROPOSED, HOST_TESTED, ISOLATED_EXACT, UNIT_EXACT, FULL_ROM_EXACT and PUBLISHED.
5. Confirm the verifier refuses missing source fingerprints and that an object proof cannot set FULL_ROM_EXACT or update official counts.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** A candidate with only G1 evidence cannot alter manifest counts; failed G2 leaves original assembly and prior published proof intact.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-004 — Review resource ABI

**Status:** PASSED_G2. **Dependencies:** G64-002.
**Focus files:** `decomp/resource_dispatch.c`; `decomp/candidates/resource_wrapper_ed4.c`; `decomp/candidates/resource_wrapper_f20.c`.

**Architectural intent:** Inspect resource_dispatch.c, two candidate wrappers, called symbols 80034EF8/80034F44/80035044 and actual original ABI; preserve function order.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/resource_dispatch.c, decomp/candidates/resource_wrapper_ed4.c, decomp/candidates/resource_wrapper_f20.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Inspect resource_dispatch.c, two candidate wrappers, called symbols 80034EF8/80034F44/80035044 and actual original ABI; preserve function order.
4. Read the original 112-byte resource region and sibling original source order: ED4, EF8, F20.
5. Capture each call target and late argument load; do not merge these functions or change the already matching 40-byte EF8.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Typed declarations, first-call argument, delay-slot loading and 0x18 stack-frame requirements are supported by original instructions rather than guesses.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-005 — Design resource ED4 replacement

**Status:** PASSED_G2. **Dependencies:** G64-004.
**Focus files:** `decomp/resource_dispatch.c`; `decomp/candidates/resource_wrapper_ed4.c`.

**Architectural intent:** Replace only func_80034ED4_35AD4 pragma in a staging checkout; preserve already matching func_80034EF8_35AF8 and C unit layout.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/resource_dispatch.c, decomp/candidates/resource_wrapper_ed4.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Replace only func_80034ED4_35AD4 pragma in a staging checkout; preserve already matching func_80034EF8_35AF8 and C unit layout.
4. Copy only the reviewed ED4 function body into the original translation unit and remove only its matching pragma.
5. Compare codegen at 0x80034ED4: expected 36 bytes, 0x18 stack frame and original jal delay-slot argument load.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Native IDO emits 36 exact bytes at 0x80034ED4 with correct relocation, and existing middle function remains exact.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-006 — Design resource F20 replacement

**Status:** PASSED_G2. **Dependencies:** G64-005.
**Focus files:** `decomp/resource_dispatch.c`; `decomp/candidates/resource_wrapper_f20.c`.

**Architectural intent:** Replace func_80034F20_35B20 pragma in the same translation unit; retain distinct callee and original source order.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/resource_dispatch.c, decomp/candidates/resource_wrapper_f20.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Replace func_80034F20_35B20 pragma in the same translation unit; retain distinct callee and original source order.
4. Integrate F20 after EF8 and retain its distinct func_80034F44_35B44 callee.
5. Compile all 112 bytes as one native IDO translation unit, including unchanged EF8, before changing production proof.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Both 36-byte wrappers plus existing 40-byte middle function reproduce 112/112 unit bytes; callback mock checks correct call targets.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-007 — Gate resource promotion

**Status:** PASSED_G2. **Dependencies:** G64-003, G64-006.
**Focus files:** `decomp/resource_dispatch.c`; `decomp/manifest.json`; `decomp/verify.py`; `decomp/inventory.py`.

**Architectural intent:** Update staging manifest ownership for ED4/F20 and run the standard 2,331-object full-ROM gate plus inventory and resource host tests.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/resource_dispatch.c, decomp/manifest.json, decomp/verify.py, decomp/inventory.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Update staging manifest ownership for ED4/F20 and run the standard 2,331-object full-ROM gate plus inventory and resource host tests.
4. Stage two manifest function claims with corresponding removed assembly placeholders; use a fresh verifier workspace and report.
5. Reject promotion unless 144/144 functions and all 33,554,432 ROM bytes match, with inventory and existing-source hashes unchanged.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Only 33,554,432-byte identity, previous 142 exact functions and inventory preservation permit the conditional 144/10,724 milestone.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-008 — Review menu ABI model

**Status:** PASSED_G2. **Dependencies:** G64-002.
**Focus files:** `decomp/empty_menu_hook.c`; `decomp/candidates/menu_enable_b60.c`; `decomp/candidates/menu_disable_bb4.c`; `decomp/candidates/menu_nested_c04.c`.

**Architectural intent:** Derive shared MenuPanel/MenuOptions/MenuBit layout from empty_menu_hook.c, menu candidates and original +0x22/+0x64/+4/+0x18 accesses.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/empty_menu_hook.c, decomp/candidates/menu_enable_b60.c, decomp/candidates/menu_disable_bb4.c, decomp/candidates/menu_nested_c04.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Derive shared MenuPanel/MenuOptions/MenuBit layout from empty_menu_hook.c, menu candidates and original +0x22/+0x64/+4/+0x18 accesses.
4. Cross-check MenuPanel flags at +0x22, MenuOptions byte at +4 and marker at +0x64, nested link at +0x18.
5. Preserve two independent pointer guards; verify host null handling and bit isolation.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Compile-time layout guards and host cases preserve null checks, bit widths, pointer nesting and unchanged 8-byte hook.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-009 — Design all three menu replacements

**Status:** PASSED_G2. **Dependencies:** G64-008.
**Focus files:** `decomp/empty_menu_hook.c`; `decomp/test_three_menu_flags.c`.

**Architectural intent:** In original unit order replace 80011B60, 80011BB4, 80011C04; retain explicit 0xFF7F AND mask and non-cached nested dereference shape.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/empty_menu_hook.c, decomp/test_three_menu_flags.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: In original unit order replace 80011B60, 80011BB4, 80011C04; retain explicit 0xFF7F AND mask and non-cached nested dereference shape.
4. Combine enable B60, disable BB4 and nested C04 in the exact original order after the 8-byte no-op.
5. Keep explicit 0xFF7F mask for original ANDI, remove the extra cached nested local, and compare complete 256-byte unit.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Start with `python3 -m unittest decomp.test_prove_integrated_units decomp.test_prove_three_wrappers -q`; run the listed C harness with verified compile flags. For native byte claims use the pinned compiler and original-reference proof scripts. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** IDO native combined source matches all 256/256 bytes (8-byte hook + 84/80/84 functions); 90,000-case synthetic harness remains valid.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-010 — Gate menu promotion

**Status:** PASSED_G2. **Dependencies:** G64-007, G64-009.
**Focus files:** `decomp/empty_menu_hook.c`; `decomp/manifest.json`; `decomp/verify.py`.

**Architectural intent:** Verify menu changes in an actual project link; capture source hashes and before/after inventory, then update evidence atomically.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/empty_menu_hook.c, decomp/manifest.json, decomp/verify.py. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Verify menu changes in an actual project link; capture source hashes and before/after inventory, then update evidence atomically.
4. Stage and gate only the three menu placeholders; do not overwrite a failed resource milestone.
5. Require 147 total matching functions only if the resource pair and all three menu functions are full-ROM exact.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes. Then run the complete `python3 -m decomp.verify` and `python3 -m decomp.inventory` gates using the new paths described in EXECUTOR_PROTOCOL.md.

**Explicit acceptance:** Only full-ROM and original-address proof of all five added functions permits the conditional 147/10,972 milestone; otherwise promote only independently passing units.

**Required negative control:** Do not treat a research fixture's exact byte span as a complete-ROM promotion. Failed full link leaves the original GLOBAL_ASM retained.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

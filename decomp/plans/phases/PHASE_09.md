# Phase 09 — Math and adjacent units

**Scope:** G64-081–G64-090; branch `chatgptweb/decomp`; G64-084 task-start checkpoint `5ac7d116f839f5305218b35380dca6c65d97cd32` (refresh after publication).

Read [EXECUTOR_PROTOCOL.md](../EXECUTOR_PROTOCOL.md) before starting. Follow individual dependency IDs, not simply numeric order. Tests listed are to be executed, not claimed as already passing. Never increase matching counts from research-only evidence.

## Mandatory phase inputs
- `decomp/math_helpers.c`
- `decomp/angle_variant.c`
- `decomp/rotation_angles.c`
- `decomp/float_state.c`
- `decomp/return_zero.c`

## Known phase risks and negative controls
No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

## Task work packages

### G64-081 — Analyze math helper 8000E2D4

**Status:** RESEARCH_ONLY. **Dependencies:** G64-002.
**Focus files:** `decomp/math_helpers.c`; `decomp/test_math_helpers.c`.

**Architectural intent:** Recover float parameters, trig/helper calls and 10-bit angle masking adjacent to matched 8000E28C.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/math_helpers.c, decomp/test_math_helpers.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover float parameters, trig/helper calls and 10-bit angle masking adjacent to matched 8000E28C.
4. Inspect 8000E2D4 argument order, float return conversions and existing 0x3FF angle mask idioms.
5. Preserve original float precision, register classes and runtime helper calls.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host input table covers zero axes, sign changes, wrap and confirmed float round-off; exact FPU instruction trace required.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** Pinned `func_8000E2D4_EED4` is 200 bytes / 50 words at VMA `0x8000E2D4`, ROM `0xEED4`; all 50 words match the SHA-verified USA ROM, with original span SHA-256 `7de0d22ff6b2f44d8c4b0e8955d2e59a2cb03410398f2b9fc2d65b0426902f30`. Its direct caller `func_80204C5C_63003C` at `0x80204CFC` passes scale 8.0, unsigned halfword angles from `+0x14/+0x16`, and output pointer `$s1`; return is unused. The target calls sine(angle A), writes `sin(A)*magnitude` at `+0x74`, calls cosine(angle A), then writes `sin(B)*(cos(A)*magnitude)` at `+0x70` and `cos(B)*(cos(A)*magnitude)` at `+0x78`, returning 1. The angle helpers own the 10-bit mask; this target passes the raw halfwords. The strict `< 0` path preserves negative zero and the multiplication order produces observable binary32 rounding.

Seven host-reference calls passed ASan/UBSan across cardinal axes, negative scale, negative zero, angle wrap and exact rounding bits. A reassociated-product mutant failed the expected `+0x70` bit pattern. Three correctly typed pinned-IDO target-only variants linked at the original VMA; best was 180 bytes versus 200 and first differed at `+0x08` (`sw $ra,0x1C($sp)` versus original `sw $a1,0x24($sp)`). The compiler kept the live scale in `$f20`, changed the frame/register schedule and generated 20 fewer bytes. The sign-after-call variant regressed to `+0x00`; the direct-expression variant also differed at `+0x00`. Stop with no first-mismatch improvement and retain `GLOBAL_ASM`. The complete source-unit comparison, full-ROM G2 and inventory were not run because no isolated exact candidate qualified.

**Next at that checkpoint:** G64-084, analyze `8000EA74` under the Architect v3 rank-1 candidate selection; G64-083 was dependency-eligible but lower priority. G64-084 has since passed G2; see its outcome below. Sol selected G64-085 next at 96/100.

### G64-082 — Analyze math helper 8000E39C

**Status:** PASSED_G2 (completed 2026-11-13). **Dependencies:** G64-081.
**Focus files:** `decomp/math_helpers.c`; `decomp/test_math_helpers.c`.

**Architectural intent:** Map 8000E39C_EF9C source operands and intermediate float conversion, preserving original call order.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/math_helpers.c, decomp/test_math_helpers.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map 8000E39C_EF9C source operands and intermediate float conversion, preserving original call order.
4. Inspect 8000E39C trigonometric callback table and FPU condition branches.
5. Test NaN, signed zero and boundary angles only where semantics can be justified; exact native bytes remain mandatory.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Reference trace and edge-case host tests cover observed rounding; mismatch report distinguishes semantics from codegen.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** `func_8000E39C_EF9C` is 328 bytes / 82 words at VMA `0x8000E39C`, ROM `0xEF9C`, original span SHA-256 `3538f84b01e28177cb1fe7e7727afc8382acd083fc114a95ae11d26d12d16765`. The ROM-backed trace established `$f12` scale, `$f14` X, `$a2/$a3` Y/Z bit patterns and a fifth object pointer from caller stack `+0x10`; the nested position pointer is object `+0x18`, coordinates are nested `+0x08/+0x0C/+0x10`, and outputs are object `+0x70/+0x74/+0x78`. It computes `(dx² + dy²) + dz²`, then passes each `(delta² * scale²) / length²` through `_nsqrtf`, negating only when the delta is strictly `< 0`, and returns 1. Negative scale is squared; negative-zero comparison is false; NaN and zero-length behavior follow the observed FPU path.

Seven host-reference calls passed GCC ASan/UBSan with `-ffp-contract=off`; coverage includes object/nested offsets, output order, negative scale, signed zero, NaN, zero length, and two fixed binary32 rounding cases. A target-only division-reassociation mutant was rejected by the exact sqrt-input bit comparison. Five bounded pinned-IDO variants used the 328-byte task budget. V1 first differed at `+0x00` with a `0x50` frame; v2 moved the mismatch to `+0x24` but used incorrect nested offsets; v3 had the right `0x48` frame but nine spill-home differences beginning at `+0x58`; v4 produced the same linked output as v3; v5 moved `scale_squared` assignment after `dz_squared` and exactly matched all 328 bytes. The final source SHA-256 is `fc9e4473a5be0754429ed8020a2b089e4a503a1d6419658c86edf428214d755c`; the three `_nsqrtf` relocations resolve at the original target.

The candidate was staged in a copied production source bundle and a fresh G2 build matched all 33,554,432 ROM bytes, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, 150/150 claimed functions and 11,476 bytes. The fresh inventory reports 150 matching C targets, 163 combined C, 7,213 ASM and 7,376 identified entries; the function-entry identity hash is unchanged. Both accepted math siblings remain exact. Updated `decomp/results/combined.json`, `decomp/results/inventory.json`, the production manifest and this evidence record from those verified artifacts. No in-game verification was performed.

See [`../execution/2026-11-13-g64-082-math-helper.json`](../execution/2026-11-13-g64-082-math-helper.json).

### G64-083 — Analyze math helper 8000E4E4

**Status:** PLANNED. **Dependencies:** G64-082.
**Focus files:** `decomp/math_helpers.c`; `decomp/test_math_helpers.c`.

**Architectural intent:** Map 8000E4E4_F0E4 and reuse only type declarations demonstrated by preceding original MIPS.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/math_helpers.c, decomp/test_math_helpers.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Map 8000E4E4_F0E4 and reuse only type declarations demonstrated by preceding original MIPS.
4. Inspect 8000E4E4 and compare shared helper signatures to earlier math matches.
5. Test sign, wrapping and output alias cases; do not replace original float path with reassociated formula.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Native original-address codegen/relocation and unchanged neighboring math C before G2.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-084 — Analyze angle variant 8000EA74

**Status:** PASSED_G2 (completed 2026-11-13). **Dependencies:** G64-081.
**Focus files:** `decomp/angle_variant.c`; `decomp/test_angle_variant.c`.

**Architectural intent:** Study 8000EA74_F674 near matching 8000EABC, including sign/order of helper arguments and mask width.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/angle_variant.c, decomp/test_angle_variant.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Study 8000EA74_F674 near matching 8000EABC, including sign/order of helper arguments and mask width.
4. Inspect 8000EA74 against matching sibling 8000EABC and its reversed-angle 0x400 logic.
5. Preserve wrap mask and float register order; do not infer identical argument order.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Angular quadrant/wrap host test passes, with exact IDO call and return scheduling.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** `func_8000EA74_F674` (72 bytes at VMA `0x8000EA74`, ROM `0xF674`, original span SHA-256 `7845fee09516aead2222a42d43c21fe4a39119052c9586ea60ee0cd1b346c5cf`) exactly matches after one new source variant. A deduplicated historical mismatch signature was counted once against the three-variant task ceiling; no equivalent recipe was rerun. The full 400-byte source unit linked at the original VMA with all six relocations matching; EABC remains matching C and EB08/EB50 remain `GLOBAL_ASM`. Fresh uncached G2 matched 151/151 functions, 11,548 bytes and the full 32 MiB ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Inventory passed with 7,376 entries, 151 matching C, 7,212 ASM, zero extra aliases and unchanged function-entry identity. See `../execution/2026-11-13-g64-084-angle-variant.json`. No in-game verification was performed.

**Next:** G64-085 passed G2 as pilot candidate 3 of 3. Sol later closed the pilot after outcome review; G64-086 passed under ordinary v2, and G64-083 is now the next selected Wave C task.

### G64-085 — Analyze angle variant 8000EB08

**Status:** PASSED_G2 (completed 2026-11-13). **Dependencies:** G64-084.
**Focus files:** `decomp/angle_variant.c`; `decomp/test_angle_variant.c`.

**Architectural intent:** Recover original register argument allocation and angle mask arithmetic for 8000EB08_F708.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/angle_variant.c, decomp/test_angle_variant.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover original register argument allocation and angle mask arithmetic for 8000EB08_F708.
4. Inspect 8000EB08 with same vetted trigonometric interfaces and ABI.
5. Test original XZ/XY axis ordering and 10-bit outputs.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Host cases include boundary 0/0x3FF and sign flips; exact native instructions required.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** func_8000EB08_F708 (72 bytes at VMA 0x8000EB08, ROM 0xF708, original SHA-256 c2489007d9a10c741e79de88d21869fc7e0f5996a1a984aeef4058dc73232e1c) exactly matches with the E74 scalar/mask shape and EB08's observed (arg0-arg2, arg1-arg3) helper order. The complete 400-byte angle_variant.c unit linked at 0x8000EA74 matched, all six relocations matched the fresh baseline, and E74/EABC remained exact while EB50 stayed GLOBAL_ASM. The one historical failure recipe was deduplicated across three rows and not replayed. Fresh uncached G2 matched 152/152 functions, 11,620 bytes and the full 32 MiB ROM; inventory passed with 7,376 entries, 152 matching C, 7,211 ASM, zero extra aliases and unchanged function-entry identity. See ../execution/2026-11-13-g64-085-angle-variant.json. No in-game verification was performed.

**Next:** G64-086 passed under ordinary v2 after two of five variants. Sol selected G64-083 at 87/100 as the only remaining dependency-ready Wave C candidate.

### G64-086 — Analyze angle variant 8000EB50

**Status:** PASSED_G2. **Dependencies:** G64-085.
**Focus files:** `decomp/angle_variant.c`; `decomp/test_angle_variant.c`.

**Architectural intent:** Recover last angle_variant.c retained-ASM helper, compare shared call signatures and downstream consumers.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/angle_variant.c, decomp/test_angle_variant.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Recover last angle_variant.c retained-ASM helper, compare shared call signatures and downstream consumers.
4. Inspect 8000EB50 and adjacent code ordering; retain original helper call placement.
5. Run relative angle boundary and alias tests before compiler probe.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Same-unit type consistency and original-address proof; unresolved function never promoted on functional resemblance alone.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-13):** `func_8000EB50_F750` (180 bytes at VMA `0x8000EB50`, ROM `0xF750`, original SHA-256 `ba59dad46351a30ab57dbafe9afc1d18869fc55e14a8ff2e10f8a06d3ab64760`) passed after two distinct bounded variants. V1 first differed at `+0x58` (`nop` vs `mov.s $f14,$f0`) from branch-delay scheduling; Sol approved an explicit two-way magnitude `if/else` based on G2-matched `func_8000EC04_F804`. V2 matched the complete 400-byte `angle_variant.c` unit at original VMA `0x8000EA74`, including all four functions and six relocations. Fresh uncached G2 matched 153/153 functions, 11,800 bytes and the complete 32 MiB ROM; inventory passed with 7,376 entries, 153 matching C, 7,210 ASM, zero extra aliases and unchanged function-entry identity. See [`../execution/2026-11-13-g64-086-angle-variant.json`](../execution/2026-11-13-g64-086-angle-variant.json). No in-game verification was performed.

**Next:** Sol selected G64-083 at 87/100 as the only remaining dependency-ready Wave C candidate. G64-089 remains gated on G64-083; G64-087 remains gated on G64-061/062/063.

### G64-087 — Analyze dispatcher 8001F8B0

**Status:** PLANNED. **Dependencies:** G64-061, G64-062, G64-063.
**Focus files:** `decomp/rotation_angles.c`; `decomp/test_rotation_angles.c`.

**Architectural intent:** Study three-entry state dispatcher and ROM 0x6C330 address table, preserving ordered pointer reads and indirect calls.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/rotation_angles.c, decomp/test_rotation_angles.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Study three-entry state dispatcher and ROM 0x6C330 address table, preserving ordered pointer reads and indirect calls.
4. Inspect dispatcher 8001F8B0's three-address dispatch table and system +0x3ADDE state.
5. Require precise table element offsets, original callback targets and branch order.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Mock dispatch covers all three state choices and default behavior; original codegen/linking validated.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-088 — Analyze 8001FA80 adjacent routine

**Status:** PLANNED. **Dependencies:** G64-087.
**Focus files:** `decomp/rotation_angles.c`; `decomp/test_rotation_angles.c`.

**Architectural intent:** Inspect remaining 8001FA80_20680 in rotation_angles.c and check relation to resource/global state calls.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/rotation_angles.c, decomp/test_rotation_angles.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Inspect remaining 8001FA80_20680 in rotation_angles.c and check relation to resource/global state calls.
4. Inspect 8001FA80 after matched 8001FA3C for shared resource state effects.
5. Test original external call order and no unintended adjacent source reordering.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Evidence-backed CFG and effects table; integration leaves existing two matched branches byte-identical.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-089 — Select first float-state batch

**Status:** PLANNED. **Dependencies:** G64-081, G64-082, G64-083, G64-084, G64-085, G64-086.
**Focus files:** `decomp/float_state.c`; `decomp/test_float_state.c`.

**Architectural intent:** Inspect float_state.c's five ASM functions, beginning with 8000643C_703C beside matched setter 80006430.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/float_state.c, decomp/test_float_state.c. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Inspect float_state.c's five ASM functions, beginning with 8000643C_703C beside matched setter 80006430.
4. Rank unresolved float_state functions 8000643C, 80006568, 8000693C, 80006B44, 80006BF8 using original address, size and callers.
5. Start smallest typed candidate only, preserve FPU flags and original single-precision semantics.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Prioritize by concrete layout and instruction complexity; compare float bit patterns, NaN and sign-zero only where original specifies behavior.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

### G64-090 — Audit misleading trivial-function names

**Status:** RESEARCH_ONLY. **Dependencies:** G64-002.
**Focus files:** `decomp/return_zero.c`; `decomp/manifest.json`.

**Architectural intent:** Review return_zero.c's 13 ASM entries individually; do not infer they all return zero from unit name.

**Numbered implementation recipe:**
1. Fetch `chatgptweb/decomp`; confirm `git branch --show-current`, HEAD and current `AGENTS.md`. Stop and replan if current manifest already owns this target as accepted C.
2. Read the exact focus files: decomp/return_zero.c, decomp/manifest.json. Determine real symbols, original function bounds, compile flags, callers and section ownership from the pinned original rather than guessing.
3. Implement the bounded design: Review return_zero.c's 13 ASM entries individually; do not infer they all return zero from unit name.
4. Inspect all 13 return_zero.c ASM placeholders instead of assuming they simply return zero.
5. Classify hidden stores, conditional branches, callback effects and real code extent before selecting any candidate.
6. Run focused host/static tests first and classify failures by wrong behaviour, ABI, codegen, relocation, symbol or section. Keep attempted variants in ignored/local research storage.
7. For any matching-C claim, compile the function in its real original translation unit, verify native IDO linked instructions at the actual VMA, and then run G2's entire ROM/inventory gate. If any gate fails, restore/reretain its ASM ownership.
8. Update only truthful evidence and `PROGRESS.md`; commit scoped work to `chatgptweb/decomp` and verify remote SHA. Never force-push, modify `main`, or commit ROMs/binaries.

**Focused tests:** Run the focused test files named in this task and the phase inventory; compile native candidate with pinned IDO and compare at original VMA. `python3 -m unittest discover -s decomp -p 'test_*.py' -q` and `python3 -m unittest tests.test_decomp_verify -q` for relevant Python changes.

**Explicit acceptance:** Per-function original size, side effect and CFG classification generated; only genuinely trivial, exact candidates proceed to G2.

**Required negative control:** No invented float tolerance for byte-identity, no compiler reassociation, no unproven trivial return/body matching from filename alone.

**Stop/recovery:** If only isolated/host tests pass, record RESEARCH_ONLY. If native full-unit codegen differs, retain the original GLOBAL_ASM. If full-ROM bytes, addresses or inventory differ, reject promotion and preserve a fresh failure report. Do not edit compiled instructions or comparison masks.

**Evidence packet:** record exact branch HEAD, target function/ROM extent/VMA (if applicable), tested source hash, commands and observed exit codes, native mismatch first word, full-ROM evidence or NOT_RUN, source/manifest/proof diff, and verified remote SHA if published.

**Outcome (2026-11-11):** all 13 placeholders are separately bounded Memory Pak/PFS routines (64–240 bytes; 1,672 bytes total), with device calls, status/output stores, CRC/cache work, or state-query control flow. The shortest is a 64-byte `osPfsIsPlug` query. The adjacent 8-byte C function is the actual constant-zero routine. No G2 candidate was eligible; retain all 13 as `GLOBAL_ASM`. ROM-bound spans and caller sites are recorded in `plans/execution/2026-11-11-g64-090-return-zero-audit.json`. Next v2 work is G64-071–080.

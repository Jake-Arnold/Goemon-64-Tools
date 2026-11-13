# Phase 09 — Math and adjacent units

**Scope:** G64-081–G64-090; branch `chatgptweb/decomp`; current source checkpoint `a68881da4b10e2553e7a89b7129d09d64b427435` (refresh before execution).

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

**Next:** G64-082, analyze `8000E39C` while preserving its observed float conversions and call order.

### G64-082 — Analyze math helper 8000E39C

**Status:** PLANNED. **Dependencies:** G64-081.
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

**Status:** PLANNED. **Dependencies:** G64-081.
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

### G64-085 — Analyze angle variant 8000EB08

**Status:** PLANNED. **Dependencies:** G64-084.
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

### G64-086 — Analyze angle variant 8000EB50

**Status:** PLANNED. **Dependencies:** G64-085.
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

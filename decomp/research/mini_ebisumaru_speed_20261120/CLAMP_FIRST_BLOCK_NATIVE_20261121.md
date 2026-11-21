# USA movement clamp first-block native IDO probe (21 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY.** No formal matching-C promotion, original game code patch or game-memory override.

## Source identity
Target `func_801CD310_589220`, USA original ROM `0x589220`, original VMA `0x801CD310`, 4,320 instruction bytes. Exact authentic original retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; expanded and existing clean upstream 32 MiB rebuild SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, 33,554,432/33,554,432 equal. Original upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

## Tested source improvements

1. Added authentic IDO 5.3 `#pragma intrinsic(sqrtf)` after the `sqrtf` prototype. Original has nine inline `sqrt.s`; previous C made nine extra external calls. With the pragma the compiler emits all **nine original inline sqrt.s**, no `sqrtf` call relocations. Original calls and compiled calls are **33/33, exact callee identities and order**. The intermediate native function becomes 4,112 B / 97 text relocations.
2. Restored the original switch's full 18-entry range `0x8E..0x9F` by adding explicit `case 0x9F:` falling into `default`. Compiler and original have five identical destination groupings for all 18 entries; current candidate's relative destinations are consistently **4 bytes later** than original. The first variant with table restored but without corrected motion source had an 8-byte consistent shift.
3. The first call to `func_801CE3F0_58A300` must pass selected input `var_f12` (initial argument `a2`, overridden from `D_8020CA2C + 0x0C` when context `+0x18 & 1`), not `arg1` (movement-cap value). Correcting this prevents dead-code elimination of the override's data read, restores its HI16/LO16 reference pair and shifts output from **4,112 to 4,124 bytes**.

## Verified native delta

- **Original 4,320 B; current ELF FUNC 4,124 B; 196 B short** (was 260 B short at the previous session checkpoint). The complete function still differs.
- **Original function-local file_11 relocations 101** = 33 R_MIPS_26 + 34 HI16 + 34 LO16. **Native C text relocations 99** = 33 + 33 + 33. One global-address HI16/LO16 pair remains missing; its owner is unresolved.
- Original 18 jump-table entries and candidate 18 entries have identical case-target grouping; relative target displacement is +4 B for every candidate entry.
- Original first-block frame **232 B**; IDO C frame **440 B**, with an extra saved `$f20`. The compiler hoists a repeated zero to `$f20` instead of original `$f0`, causing incorrect register lifetimes. Original stores incoming `a1` at `sp+0xEC`; native stores it at `sp+0x1BC`.
- Exact contiguous non-relocated instruction subsequences exist after alignment: original `+0x3A8` / candidate `+0x384` (24 B); `+0xBBC` / `+0xB50` (24 B); original `+0x54` / candidate `+0x5C` (20 B). These are structural evidence, **not original-address exact basic blocks**.
- Two-argument first helper and volatile-cap variants were also compiled. None repaired the oversized stack or yielded a complete exact match. Current C compiler still reports 16 incompatible-pointer warnings: no semantics or type correctness proof.

## Reproduction

Companion conversation artifact `GOEMON_CLAMP_FIRST_BLOCK_20261121.zip` contains **complete candidate C**, type header, original IDO compilation script and read-only ELF/ROM structural auditor. File `audit_result.json` contains the reproducible output (no original instruction bytes, ROM, original ASM, objects, or toolchains).

Actual tests: authentic IDO 5.3 C compilation **PASS**; 32 MiB already-built pristine USA ROM versus original expanded ROM **PASS**; original versus native function/relocation/callee/sqrt/jump-table audit **PASS for listed structural properties**, full function **FAIL**. Production combined `decomp.verify`, strict inventory, `decomp.local_ci` and emulator gameplay **NOT RUN**.

Canonical USA decomp remains **1,956 accepted C / 83,940 instruction bytes / 5,407 ASM** (branch inventory checked on 21 Nov 2026); this research is never added to that count without full original-ROM gates.

## Next bounded step

1. Recover the correct original 232-byte frame and register liveness; remove the erroneous saved `$f20` by improving expression and local-variable scoping rather than modifying compiler code or MIPS instructions.
2. Identify the remaining missing original `R_MIPS_HI16/LO16` data dependency and verify the corresponding C load.
3. Continue basic-block comparisons; only attempt combined 1,956-plus C verification after all 4,320 original function bytes are exact.

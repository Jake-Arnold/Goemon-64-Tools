# USA resource 26 adjacency sweep — 15 native-exact C functions, one remaining ASM

**17 November 2026** — research-only evidence for original USA NG5E. Pinned upstream: `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Original authenticated expanded 32 MiB USA ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. No proprietary ROM, ELF, toolchain, original disassembly, or gameplay save is committed.

## Context and outcome

The previous Project64 trace identified the resource-26 Mr. Arrow native saved-event callback. The prior task reconstructed three exact C functions (168+64+80=**312 original instruction bytes**), in `decomp/research/file26_mr_arrow_chain_20261117.c`. This task searched *adjacent original resource-26 function boundaries* and found **12 additional original-IDO-5.3 exact C functions covering 2,196 original instruction bytes**, with no duplication of those prior three.

The result is **15/16 original resource-26 functions matching C, 2,508 original instruction bytes**; only a single **236-byte** initializer retains assembly. **No production C count increased in this task.** The connected branch had already promoted three unrelated USA file11 functions and remains at **782 accepted USA C / 34,392 bytes**, plus separate **34 Japanese C**.

| Original USA resource-26 function | Original decompressed ROM offset | Original byte count | Status |
| --- | --- | ---: | --- |
| `func_08000000_6AE7E0` | `0x6AE7E0` | 204 | **NEW** IDO exact |
| `func_080000CC_6AE8AC` | `0x6AE8AC` | 168 | Prior IDO exact |
| `func_08000174_6AE954` | `0x6AE954` | 64 | Prior IDO exact |
| `func_080001B4_6AE994` | `0x6AE994` | 80 | Prior IDO exact |
| `func_08000204_6AE9E4` | `0x6AE9E4` | 204 | **NEW** IDO exact |
| `func_080002D0_6AEAB0` | `0x6AEAB0` | 168 | **NEW** IDO exact |
| `func_08000378_6AEB58` | `0x6AEB58` | 188 | **NEW** IDO exact |
| `func_08000434_6AEC14` | `0x6AEC14` | 120 | **NEW** IDO exact |
| `func_080004AC_6AEC8C` | `0x6AEC8C` | 104 | **NEW** IDO exact |
| `func_08000514_6AECF4` | `0x6AECF4` | 228 | **NEW** IDO exact |
| `func_080005F8_6AEDD8` | `0x6AEDD8` | 232 | **NEW** IDO exact |
| `func_080006E0_6AEEC0` | `0x6AEEC0` | 96 | **NEW** IDO exact |
| `func_08000740_6AEF20` | `0x6AEF20` | 252 | **NEW** IDO exact |
| `func_0800083C_6AF01C` | `0x6AF01C` | 204 | **NEW** IDO exact |
| `func_08000908_6AF0E8` | `0x6AF0E8` | 236 | **FAILED_NATIVE**; retain ASM |
| `func_080009F4_6AF1D4` | `0x6AF1D4` | 196 | **NEW** IDO exact |

The **14 contiguous exact functions** occupy original resource26 `+0x000..+0x908`, original decompressed ROM `0x6AE7E0..0x6AF0E8` (**2,312 instruction bytes**). All 14 match as an *actual linked C unit*. The **15th exact** callback is `+0x9F4..+0xAB8` (**196 bytes**), separated from the 14-function unit by the one retained 236-byte ASM function `+0x908..+0x9F4`. Original resource file26 ends with **eight zero/NOP padding bytes** after `+0xAB8`.

## Matching source and original-code coverage

- `decomp/research/file26_adjacent14_20261117.c`: exact 14-function C unit, Git blob SHA `46b09743516a006317c067d4147edd9b947e519a`. Includes the three previously proven callbacks; **do not count those three as newly discovered**. Verified original 2,312-byte SHA-256 `5c9745fe62c61885842a2996e8c7a883630fc350ea7d90e49bb2b77f47fa11e0`.
- `decomp/research/file26_adjacent_tail_20261117.c`: exact last 196-byte callback, Git blob SHA `bdd2612bb8da53956ed0918944e7f0304b474f3e`. Verified original 196-byte SHA-256 `e6efd31b7016e31330b89613edc0361dc767813e152b7a54fa02e16e6b30ced0`.
- `decomp/research/test_file26_adjacent15_20261117.c`: host regression run against the **actual** 14-function and final callback C source, exact Git blob SHA `4f6e1e95b140d5e585972a1c98a2506720927974`.
- `decomp/results/file26_adjacent15_upstream_scratch_20261117.json`: sanitized original-function table, exact hashes, original 32 MiB ROM proof, test flags and limits.

The original C deliberately retains function-address symbols and opaque helper prototypes where semantics remain uncertain, rather than inventing names. Actor flag IDs are parameterized by actor `+0xD0`; saved-event bank flag setting is performed by the original `func_80024038_24C38`. A separate child actor byte field at `+0xD0` is **not itself** a persistent saved-event ID.

## Verification actually run

1. **Native matching-C:** original pinned IDO 5.3 `-O2 -mips2`, MIPS cross-binutils, original-address linkage. All **15/15 original FUNC name/VMA/size and instruction bodies** matched. Contiguous first 14 functions **2,312/2,312 exact**; final callback **196/196 exact**.
2. **Fresh pinned-upstream scratch whole-ROM rebuild:** Independently rebuilt unmodified original game baseline, then replaced original assembly using the 14-function C unit and final callback C while **retaining** original assembly for `func_08000908_6AF0E8`. Trimmed **only proven-zero alignment padding** of C/ASM section boundaries (no original instruction or game data modifications). Two scratch stages passed, including the final 15-function stage. The resulting complete **33,554,432/33,554,432-byte original USA ROM matched exactly**, SHA1 `6ea0ed71032ce08fc2745f412d84936382197494`. Original positive-sized ELF function identities **7,376/7,376 equal** and original `.rel.file_26` semantic relocations **207/207 equal**.
3. **Host regression on actual source:** GCC `-std=gnu11 -O1 -g -Wall -Wextra -Wno-unused-parameter -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize=alignment -fno-pie -no-pie` **PASS**, including an independent recheck. Exercises actor `+0x68 & 0x200` gating; flag argument `0x104`; callback selection and handoff; event IDs `0x6C/0x6B/0x6A/0x66/0x312/0x64`; original temporary field `+0x5E` restoration; child object byte update; both completion paths; and angle/context `+0x16` wrapping.
4. **Sanitizer limitation:** Host alignment-only UBSan checking was disabled (`-fno-sanitize=alignment`) because the candidate retains original N64 32-bit-pointer field layout while the GCC host is 64-bit. Other ASan/UBSan instrumentation was active. This does **not** replace native code matching, which was independently performed using original MIPS sizes/addressing.

## Remaining one resource-26 ASM and failure evidence

`func_08000908_6AF0E8` is an **original 236-byte initializer** with float load scheduling that did not match the native IDO output after **six bounded variants**. Best candidate first mismatched at function-relative `+0x98`: original `lwc1` versus compiled `lw` ordering with the associated stack temporary. Do not promote, modify ASM or patch instruction bytes to conceal it. The adjacent callback `func_080009F4_6AF1D4` independently matches C despite its unpromoted initializer.

## Production acceptance boundary

The full original-ROM build here used a *disposable pinned upstream checkout*, **not** an authenticated materialization of the current connected `chatgptweb/decomp` branch with its **782 accepted USA C functions**. The local toolchain could not obtain a complete current GitHub branch checkout by shell `git` because GitHub DNS was unavailable; the GitHub connector returned file text but no complete verifiable native checkout archive. Therefore **NOT RUN** for this new batch: final canonical combined `python3 -m decomp.verify` of 782+12, strict `decomp.inventory`, all production overlay and complete ELF ownership rules, and full `decomp.local_ci`. These results are `RESEARCH_ONLY`, **production delta +0**, not `PASSED_G2` or an accepted USA C count of 794.

The locally generated reproducibility bundle `goemon_file26_adjacent15_native_20261117.zip` contains the exact source/test files, native verifier, disposable upstream stage runners and sanitized JSON proofs. It excludes all ROMs, assembled original code, saves, extracted assets and proprietary toolchains.

**Next actionable gate:** Reconstruct a **complete GitHub-head-authenticated current branch checkout**, stage only the 12 newly matched functions alongside all 782 accepted USA C, run the full combined ROM / original ELF / semantic relocation / strict inventory / full CI verification, and only then consider promotion to **794**. The unmatched `+0x908` ASM remains untouched.

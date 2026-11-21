# 21 November 2026 — Mini Ebisumaru movement area A–E (ROM-reproduced research)

**Status: RESEARCH_ONLY / FAILED_NATIVE for the clamp; NO PRODUCTION PROMOTION.** The 1,956 accepted USA original-address C functions and 5,407 ASM entries remain unchanged. Existing three pristine-USA speed-path matches in this draft PR are untouched.

## Original-USA input authenticity

Exact original USA Rev 00 retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. The pinned `mnsg` upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` rebuilt exactly 33,554,432/33,554,432 bytes, independently confirmed using `cmp`. Original IDO 5.3 was used for C probes. The user-supplied private ROM, generated ASM, ELF objects, and toolchain are not published.

## A. Clamp `func_801CD310_589220` — BLOCKED at native equality

Original ROM `0x589220`, original VMA `0x801CD310`, original **4,320 bytes**. Prior m2c 565-line C draft had 25 native-incompatible host C errors. Checking original MIPS call interfaces corrected the inferred arity of two three-vector helpers, a single-argument angle lookup, and invalid pointer/float forms. The resulting research C compiles with authentic original IDO 5.3 to a **4,060-byte ELF FUNC** — **260 bytes short** of original. Two bounded original-ID0 C source variants generated the same 4,060-byte extent; the first instructions already differ. The C draft still has numerous incompatible-pointer warnings and is not production-ready.

**Relocations:** original `file_11` function range has **101 semantic relocation sites**, split 33 `R_MIPS_26`, 34 `R_MIPS_HI16`, 34 `R_MIPS_LO16`. Candidate object has **106**, split 42, 32, 32. This comparison filters *only* original `.rel.file_11`; naive VMA-only filtering incorrectly includes other overlays occupying the same guest address range. No original-address native text exactness or complete-ROM integration of this candidate was claimed.

**New original MIPS facts:** the original function has both a 3D magnitude clamp (`sqrt.s` at PC `0x801CDCB8`, compare at `0x801CDCBC`) and an additional 2D clamp (`sqrt.s` at PC `0x801CE0EC`, compare at `0x801CE0F0`). The early branch at PCs `0x801CD368`–`0x801CD39C` checks bit 0 of context byte `+0x18`; set means **4.0f override cap** and alternate motion input at `D_8020CA2C +0x0C`. This is not a validated universal-speed hack.

## B. Speed profile table — expanded and ROM-confirmed

Float mode profile table `D_801FC91C_5B882C`, original ROM offset `0x5B882C`, VMA `0x801FC91C`: **17 records**, stride **40 bytes**, three mode floats in each. Task `+0x98` selects the profile, task `+0x70` selects the movement mode and task `+0x74` receives the selected float via `func_801D288C_58E79C`. Rows by ID: `0:40/70/100`, `1:50/80/120`, `2:40/50/70`, `3:40/50/60`, `4:40/50/70`, `5-8:80/160/260`, `9:40/0/0`, `10-11:50/95/140`, `12-13:100/230/350`, `14-15:100/160/250`, `16:100/0/0`. Exact profile-to-character/action ownership remains unproved.

## C. Missing transient 1.0f writer identified

`func_801DA84C_59675C` (ROM `0x59675C`): original MIPS constructs **1.0f** and writes it to context `+0x04` at PC `0x801DA87C`, task `+0xE8` at PC `0x801DA880`, and task `+0xE4` at PC `0x801DA884`; it also zeros the movement vector. The same path sets task `+0xA4 = 1.2f` for Mini mode or `3.0f` otherwise. The live gameplay event for this writer is **UNVERIFIED**; user-reported `1.0` hurt-speed correlation remains a hypothesis.

## D. Visual scale and collision still unknown

No original MIPS access establishes that context `+0xA4` is visual scale/collision, or that runtime-correlated `0x801C159A` is the renderer scale owner. Do not promote these interpretations or expose unverified writes.

## E. Transformation and action gates

`func_801DD3C4_5992D4` gates character switching on current task character index `1` and context `+0x86 == 0xFFFF`; attack is separate in `func_801DCFB0_598EC0`. `func_801E78DC_5A37EC` (ROM `0x5A37EC`, original **112 B**) decrements `+0x86` unless it is `0` or `0xFFFF`. IDO 5.3 compiles a research C candidate to the same **112-byte** function length, but **six non-relocation instructions differ**. No match or promotion.

## Actual gates and handoff

- Original complete clean ROM rebuild: **PASS**, original USA expanded SHA-1 verified, full 32 MiB byte comparison PASS.
- Research read-only verifier: **PASS**, **13 original MIPS opcode assertions** plus all **51 floats** in 17 profile records.
- Clamp original IDO native compilation: **PASS**, result 4,060 vs original 4,320, relocation mismatch 106 vs 101; **FAILED_NATIVE**.
- Countdown candidate IDO native compilation: **PASS**, 112-byte function but 6 instruction differences; **FAILED_NATIVE**.
- Host GCC C syntax check: only passes with pointer-compatibility warnings tolerated (**17 warnings**). No semantic correctness claim.
- Canonical combined `python3 -m decomp.verify`, strict inventory, full `decomp.local_ci`, gameplay/emulator tracing: **NOT RUN**. Canonical count unchanged **1,956 C / 83,940 bytes / 5,407 ASM**.

Reproducible detailed 10-file research package (read-only ROM assertions, complete clamp C draft, profiles CSV, original IDO script, countdown C and sanitized evidence): conversation artifact `GOEMON_MINI_SPEED_AREA_20261121.zip`. No ROM bytes, generated disassembly, compiled objects, or toolchain are committed.

**Next bounded priority:** concentrate on the first mismatching basic block and the 2D/3D dispatch inside `func_801CD310`, reconstruct the actual operand types from original MIPS and surrounding C callers, then retry an original-ID0 probe with measured gains. If no progress, use debugger watchpoints at `0x801DA884` to confirm hurt reset and at `0x801CDCB8` / `0x801CE0EC` to distinguish which clamp executes; map the profile index `task +0x98` to live character/action modes. Do not alter production original code until all original-ROM proof gates pass.

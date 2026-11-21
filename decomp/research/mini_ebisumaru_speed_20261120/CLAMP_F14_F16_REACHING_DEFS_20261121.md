# 21 November 2026 — original USA clamp f14 / f16 zero reaching-definition analysis

**FAILED_NATIVE / RESEARCH_ONLY; no production promotion.** Target func_801CD310_589220 at ROM 0x589220, VMA 0x801CD310, length 4320 bytes, frame 232 bytes, file_11.

## Actual original-MIPS dataflow

Authenticated original USA SHA-1: 6ea0ed71032ce08fc2745f412d84936382197494. A fail-closed control-flow analysis of function-relative +0x1B4 through +0x27F enumerated **65 reachable register-definition states**, validating **eight branch opcode/target signatures**, including branch-likely delay-slot execution. No original opcode bytes or ASM were published.

| Original definition | Observed uses |
| --- | --- |
| +0x1B4: zero to f14 | +0x218 stack store sp+0x8C and +0x234 comparison |
| +0x1F4: zero to f16, in branch-likely taken-only delay slot | +0x274, +0x278, +0x27C later motion stores |
| +0x1F8: zero to f16 | +0x200, +0x204, +0x208, +0x20C reset-only motion stores |
| +0x214: zero to f16 | +0x274, +0x278, +0x27C later motion stores on alternative paths |

**New constraint:** The later three stores have two possible f16 reaching definitions (+0x1F4 OR +0x214), and NOT the reset-only +0x1F8 definition. f14 is an independent shorter-lived zero. These are facts about original machine-code control flow, not established original C declarations.

## Native compiler findings

An isolated ordinary-C gate fixture compiled with authentic SGI IDO 5.3, -O2 -mips2 -G 0 -non_shared, naturally emitted **three zero definitions** at fixture-relative +0x74, +0x78 and +0x94, including the delayed conditional zero, but used f2 (not original full-function f16). This demonstrates the branch source shape can induce the original three-definition topology without inline ASM or patching machine code.

**Nine full-function authentic IDO C trials**, including the existing baseline and eight targeted alternatives, were compared at fixed original positions. Nesting/inverting the condition and using goto either produced identical code or slightly worsened it. Adding float gate-zero / compare-zero locals or explicit branch merging changed the stack frame **232 to 240 bytes** without reproducing a single f14 or f16 zero in the candidate gate. The best remains existing 4324-byte native FUNC versus original 4320, 232-byte frame, **24/902** same-position comparable nonrelocated MIPS instructions, **10/101** exact offset/type/symbol relocations, 33 calls, nine inline sqrt.s and 101 text relocs. First nonrelocated mismatch +0x04 (unwanted saved f20 zero). All whole-function C variants are FAILED_NATIVE.

## Executed verification

- Pinned original USA 32MiB ROM rebuilt/compared: **33,554,432/33,554,432 exact**, SHA-1 6ea0ed71032ce08fc2745f412d84936382197494. This is not a C replacement ROM.
- Original CFG analyzer: **65 states, 8 branch signatures, 9 asserted zero-use sites PASS**.
- **Eight** Python synthetic/original CFG unit tests PASS, including likely/nonlikely delay paths and corruption rejection.
- Isolated normal-C native IDO 5.3 fixture PASS for diagnostic three-definition topology, not original address.
- **Nine** complete C IDO builds and original-address instruction/ELF/relocation audits PASS for expected FAILED_NATIVE results.
- Existing original context-gate microexecutor: **3000/3000 PASS**.
- Source-only ZIP freshly extracted and independently replayed: PASS.
- Candidate complete-ROM replacement, all-accepted-C canonical decomp.verify, strict inventory, full local_ci and emulator gameplay: NOT RUN.

Source-only 23-file archive: **GOEMON_F14_F16_CFG_RECON_20261121.zip**, SHA-256 **883cf9708312e233624978fdb25d77df2f5c7db1a742f3f675b7a95037b26736**. It contains all nine complete C variants, executable read-only original-ROM CFG analyzer and unit tests, native fixture, comparators, gate micro-executor, and one-command replay. No original ASM/ROM/game assets/object/ELF/proprietary toolchain.

**Next technical action:** Stop lexical zero-local variants. Recover original source-level floating-point and vector backing-store lifetimes across the two trigonometric helper calls before this gate and later norm/transform helpers. The original assembly's localized zero definitions compile naturally in an isolated fixture; the full reconstructed C keeps a global zero live in f20 across calls. Recover the historically stronger 157/925-word source only if its complete C bytes become available, and do not claim a new match without complete original-address evidence.

USA production remains **1965 accepted C, 84648 instruction bytes, 5398 ASM entries**. The older combined and inventory snapshots still refer to 1956 C. Keep PR #144 draft.

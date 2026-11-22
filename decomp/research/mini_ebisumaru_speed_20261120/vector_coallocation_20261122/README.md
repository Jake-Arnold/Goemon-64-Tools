# USA Mini clamp — native vector coallocation research, 22 November 2026

**FAILED_NATIVE / RESEARCH_ONLY.** The original USA `func_801CD310_589220` remains assembly-owned. ROM `0x589220`, VMA `0x801CD310`, extent 4,320 bytes, frame 232 bytes.

## New result

Source-level relocation of an ordered vector aggregate into the local declarations immediately after `pool_fp_6` recovers both original native stack pointer operands in one complete SGI IDO 5.3-compiled C function:

| Measurement | Previous F14 complete C | New vector complete C | Original MIPS |
|---|---:|---:|---:|
| First vector | `sp+0x88` | **`sp+0xA4`** | `sp+0xA4` |
| Second vector | `sp+0x7C` | **`sp+0xB0`** | `sp+0xB0` |
| Native frame | 232 B | **232 B** | 232 B |
| FUNC size | 4,440 B | 4,440 B | 4,320 B |
| Exact word positions | 117/917 | **123/917** | complete |
| Exact relocation triples | 30/101 | 30/101 | 101/101 |
| Original `f14` at +0x1B4 | YES | YES | YES |
| Original 8-word F16 reset sequence | NO | NO | YES |

The native code gains six same-position instruction words, **without losing any previous matches**: `+0x43C,+0x450,+0x464,+0x468,+0x50C,+0x510`. The complete 101 native relocation entries remain identical to the earlier F14 candidate. Original helper-call order (33), square-root count (9), positive-zero operations and 232-byte frame remain intact.

The source-only change begins with the previously authenticated F14 candidate SHA-256 `43f54bc681c1f1faaa33544a9effbba6750b9bc4acf49c29c36d2d73fbefb6d5`. Remove its two separate `f32 vecA[5];` and `f32 vecB[3];` declarations, insert `struct { f32 vecA[3]; f32 vecB[5]; } scratch;` directly after the declaration of `pool_fp_6`, and access both vector variables using `scratch.vecA[i]` / `scratch.vecB[i]`. Only elements 0,1,2 are actually indexed, so the two additional B elements are unused layout space. Source SHA-256 `ee2b72bd25526ec54cebc3353ef1b4766f4d64a9b79a98caf0e1d6e21c055cca`. The fact that this declaration choice induces a matching stack layout does **not** prove the original source declarations.

The remaining stack mismatch is substantial: original `sp+0x8C` magnitude default +0x218 / square-root +0x4E4 / late read +0xFE8 is still not reproduced, and the candidate's FP vector access multiplicities are `8/8/8` for A4/A8/AC and `5/5/6` for B0/B4/B8, versus original `9/8/9` and `4/5/5`. The candidate first-mismatch is at +0x44; all 101 relocations still do not agree. Full native equality **fails**.

## Actual verification and next constraints

- Authentic user USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; private expanded USA and pristine rebuilt ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, **33,554,432/33,554,432 bytes identical**, PASS. This is an unchanged original baseline, not a candidate-linked ROM.
- **1,557 completed variants** across 11 local bounded groups, **1,549 IDO compiles PASS**, eight compile errors. Excludes incomplete timed-out sweep. The final 354 typed-zero variants did not exceed 123 matching words or recover combined F14/F16.
- Original-offset ROM/ELF/101-relocation/33-call/nine-sqrt/232-frame native measurements for both complete C candidates, source reconstruction SHA-256 verification, pristine ROM comparison, ZIP integrity, and fresh extraction/replay PASS for measured research invariants. Original matched machine-code function **FAIL**.
- User-facing source-only `GOEMON_CLAMP_VECTOR_STACK_20261122.zip` (SHA-256 `5977f4dd41ae7596fff3be39105a3739644f923c98e1cbb36f3b9f6fc8fb0500`) includes both complete C sources, deterministic source reconstructor, full native replay/strict comparator, report and safe 11-group evidence. The archive is provided in the same chat. No original ROM, assembly, proprietary compiler, object file, ELF or asset is distributed.
- Candidate ROM integration, combined `decomp.verify`, strict inventory, full local CI and emulator gameplay **NOT RUN**. Do not promote to accepted C. USA production stays **1,965 C, 84,648 original instruction bytes, 5,398 ASM**. Keep PR #144 draft.

**Next:** change stack *ownership and live ranges* to place the persistently defined magnitude in `sp+0x8C` and recover the original branch-local F16 resets, while retaining both new vector bases, 232-byte frame, 33 calls and 101 relocations. Keep original assembly and all canonical manifests untouched until full native equality and G2.

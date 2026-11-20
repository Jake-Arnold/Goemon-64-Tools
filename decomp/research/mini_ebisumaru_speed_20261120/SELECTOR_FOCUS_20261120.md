# USA Mini Ebisumaru selector — focused IDO replay (20 November 2026)

**Function:** `func_801E1C90_59DBA0`; original USA ROM `0x59DBA0`, guest VMA `0x801E1C90`, 384 original instruction bytes. **Status: FAILED_NATIVE / RESEARCH_ONLY**.

## Reproduced original-address comparison

The mounted original USA retail ROM SHA-1 remains `df8083a54296b8c151917c5333e1c85f014a2a66`. The saved pristine, pinned upstream rebuild was compared against its authentic expanded ROM (all 33,554,432 bytes identical, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`). This verifies the baseline used for research, not a new full-ROM candidate replacement.

The prior best C source was recompiled with original IDO 5.3, `-O2 -mips2 -G 0 -non_shared`. The original code has 96 words; the C candidate still has **12 different non-relocated instruction words**, first at original PC `0x801E1CEC` (original `0x45010044`; candidate `0x45010043`). The source-generated ELF **function symbol is 380 bytes**, while its `.text` section is **384 bytes because of alignment padding**. The 384-byte section alone is not a matching-function proof.

The main discrepancy is one absent unconditional branch in the switch-default return block (original region near `+0x168`); its absence shifts the earlier float-compare and subsequent case-exit branch targets. Both calls to the speed smoothing function encode the zero `a2` argument with a different instruction form. The candidate generates an eight-entry `.rodata` table; original `file_11` stores its 8-entry jump table at guest `0x8020B2E0`, so data-owner/linker and relocation proof will be necessary in addition to exact text.

## New bounded trials

Five additional source variants adjusting explicit goto, default return initialization, post-switch control flow, and local variable scope produced the **same 12 non-relocation mismatches**. A typed-`float` third-argument ABI variant instead generated **64 non-relocation mismatches**, moving floating-point and call register instructions. No variant was exact. All compiled and were compared locally with the authentic IDO toolchain; there was no new standalone original-address exactness claim.

Research reproduction package is in the conversation artifact `func_801E1C90_focus_2026-11-20.zip`, containing the near-match C, failed type variant, native comparison runner and machine-readable mismatch ledger. No ROM, original ASM, disassembly, object, compiler or game asset is included in this Git branch.

## Acceptance

No production manifest, original source staging, accepted C count or inventory changed. Combined `decomp.verify`, `decomp.inventory`, full `decomp.local_ci`, and emulator gameplay were **NOT RUN** on this research. USA accepted C remains **1,723**, 5,640 ASM entries. Prior `func_801E276C` and `func_801E3DE0` isolated exact proofs remain unpromoted in this draft PR.

**Next targeted work:** inspect compiler codegen and the surrounding original `file_11` translation-unit switch/return patterns to explain the extra original branch and differing immediate-zero encoding, before generating further variants. Do not promote a 380-byte function plus four bytes of padding as the 384-byte original.


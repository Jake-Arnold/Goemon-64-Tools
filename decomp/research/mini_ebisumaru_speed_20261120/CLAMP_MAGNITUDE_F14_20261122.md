# USA Mini clamp: f32 magnitude lifetime and original F14 definition (22 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY. No accepted-C promotion.**

Original USA function func_801CD310_589220: ROM 0x589220; guest VMA 0x801CD310; 4,320 original bytes; 232-byte stack frame; overlay file_11. User retail ROM SHA-1 df8083a54296b8c151917c5333e1c85f014a2a66. Decompressed original 32 MiB SHA-1 6ea0ed71032ce08fc2745f412d84936382197494. Original pin 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, original native SGI IDO 5.3 -O2 -mips2 -G 0 -non_shared.

## Verified change in C dataflow

The earlier reconstructed complete C tracked optional 3D magnitude using a u8 magnitude_valid flag, assigning the float zero at its later use when the flag was false. The original machine code instead has evidence for a floating-point local initialised to positive zero across the context gate. A source-equivalent rewrite removes the Boolean flag, defaults pool_fp_2 to 0.0f before the gate, overwrites it on the sqrt branch, and multiplies it through the same late helper path. This preserves zero times infinity/NaN behaviour rather than replacing the multiplication with a constant.

Placing that f32 initialisation immediately before the original context-gate condition leads native IDO to emit the **original mtc1 zero,$f14 at function relative +0x1B4**. The earlier version did not have this instruction at this position. The original mtc1 zero,$f0 at +0x04, original 232-byte frame, five case-local angle stores, original cosine calls +0x19C/+0x1A4, original early delay slots, original stack positions sp+0x64/+0x6C/+0x6E and exact jump-table destinations remain. The initial float/Boolean source rewrite alone reduces FUNC length by 56 B and improves fixed-original-position MIPS matches 85 to 94, exact relocation offsets/types/symbols 20 to 22.

## Native IDO measured Pareto points

| Native source | Function bytes | Frame | Matching nonrelocated instruction positions | Original-offset/type/symbol relocation triples | Original F14 at +0x1B4 |
| --- | ---: | ---: | ---: | ---: | --- |
| Prior source | 4480 | 232 | 85/910 | 20/101 | No |
| Float-magnitude early F14 | **4424** | **232** | **94** | **22/101** | **Yes** |
| Strongest comparable source | 4440 | 232 | **117/917** | **30/101** | **Yes** |
| Shortest selected source | **4396** | 232 | 93 | 22/101 | Yes |
| Alternative context source | 4400 | 232 | 107 | 26/101 | No; its early trigonometric calls differ |

Changing which 11 of 33 task f32 zero assignments are written (f32)0 instead of 0.0f produces a distinct native allocation without changing the source-level positive-zero values or field lvalue types. 29 group distributions and 143 controlled one-for-one swaps were compiled and measured at authentic original MIPS offsets, with the original F0/F14, 232-frame, cosine call sites and jump-table positions used as fail-closed selection constraints. The strongest candidate is SHA-256 43f54bc681c1f1faaa33544a9effbba6750b9bc4acf49c29c36d2d73fbefb6d5. Its first 15/15 original prologue words, context 13/13 original words at +0x50..+0x8F, and original switch 49/55 comparable words at +0x90..+0x1B3 are exact. Full function **still fails**; first differing nonrelocation word +0x44, overall extent 4,440 vs original 4,320, and only **30/101** exact relocation triples. Original type/symbol pairs in ordered relocations remain 99/101 (two compiler .rodata versus original named jump-table references). The companion shortest candidate is 76 bytes above original; it loses some word/relo agreement. Do not combine achievements from distinct sources.

## Tests actually executed

- Original USA retail SHA-1 and original expanded SHA-1 authenticated from user-supplied files.
- Fresh pinned upstream complete unmodified USA ROM rebuild compared **33,554,432/33,554,432 bytes exactly** and original expected SHA-1. This is the baseline, NOT a C-integrated ROM.
- Native original-ID0 compile, original-offset MIPS / ELF / 101 text relocation / 33 call / 9 native sqrt / original 18-entry jump grouping / stack / original F0-F14 instruction validation for five complete C sources. Each compiles, each explicitly FAILED_NATIVE.
- Clean unzip and SHA256SUMS source integrity PASS, and a fresh independent replay of all five C candidates PASS with expected FAILED_NATIVE.
- Source-only deterministic reconstruction tool generated early/strongest/shortest candidates with exact SHA256 matches.
- GCC ASan+UBSan and Clang ASan+UBSan each **131,072** bounded magnitude-state cases PASS, non-NaN bit identical and NaN class equivalent (4,633 NaN-class pairs per compiler). These do not prove complete game behaviour.
- Candidate integrated-ROM build, canonical current decomp.verify, strict inventory, full decomp.local_ci and emulator gameplay **NOT RUN**, as the isolated function is not original-address native-exact.

## Reproducibility and next instruction block

Complete source-only conversation attachment **GOEMON_CLAMP_MAGNITUDE_F14_20261122.zip**, SHA-256 **51b4f8c59bf533b265790affbde837234f3ca76772e81f7e9ea3f3b239831455**, includes five complete candidate C sources, fail-closed original-address native comparator and replay.py, GCC/Clang host test, base-to-best source patch, source-reconstruction utility, README, checksums and sanitized evidence. The script **RECONSTRUCT_MAGNITUDE_F14_20261122.py** is also committed on this research branch byte-for-byte (Git blob **76957b92a9bcc84e0a06c028fa1d7319379ca7d2**, standalone SHA-256 **8e63851c52a5e766d8e6479dda55924e9aef9274a19633e29f4c3bc292da609b**). It takes the already regenerable prior original C SHA b444006aa5bd9dddf64b3fd19d2d5a49d43a7ff962f2d65778e93f72c8ac6078 and reconstructs each new C byte-for-byte, rejecting any input/source drift. No ROM, original ASM, extracted asset, original MIPS words, native object/ELF or compiler committed.

**Next:** Original MIPS has the F14 value stored as swc1 f14,sp+0x8C at +0x218, whereas the new C stores a zero value prematurely at a different stack location. Reconstruct the delayed magnitude backing-store assignment and separate original F16 branch-likely zero definitions around +0x1F4/+0x1F8/+0x214 without regressing the recovered +0x1B4 F14 definition, early calls or 232-frame. Do not use type-incorrect integer stores to manipulate allocation.

USA formally verified unchanged: **1,965 accepted original C, 84,648 accepted machine-code bytes, 5,398 ASM**. Do not change C manifest or original ASM; keep PR #144 draft.

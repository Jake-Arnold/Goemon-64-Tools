# 22 November 2026 — Original whole-function magnitude SSA and stack ownership audit

**FAILED_NATIVE / RESEARCH_ONLY.** No production code or C ownership changes.

Original USA `func_801CD310_589220`, ROM `0x589220`, VMA `0x801CD310`, original 4320 bytes / 232-B frame, owner `file_11`. Retail ROM SHA1 `df8083a54296b8c151917c5333e1c85f014a2a66`, expanded 32MiB original SHA1 `6ea0ed71032ce08fc2745f412d84936382197494`; pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, genuine SGI IDO 5.3.

## New full-MIPS original CFG analysis — correct branch-likely semantics

Authenticated original ROM has 1080 instructions in this FUNC, 103 reached conditional branch sites including **43 branch-likely** sites, and one JR jump table of 18 entries / 5 targets. The new `original_cfg_ssa.py` computes a CFG over **(PC, pending-delay-slot-destination)** rather than PC alone, producing **1146 reachable control states** and 1969 forward-dataflow updates. This matters because original instructions **+0x610 and +0x8A4** can execute both as delay-slot instructions and as ordinary entry points; their successor paths differ. The analyzer models conditional-annulled BEQL/BNEL/BLEZL/BGTZL and floating-point likely branches. The corrected final branch count is **103 / 43** (the first incremental run omitted integer likely opcodes and reported 87 / 27, which has been superseded). Eleven independent synthetic original-independent unit tests pass.

Read-only original ROM stack opcode/register/displacement verification proves:

| Original instruction location | Operation at sp+0x8C | Semantic ownership |
| --- | --- | --- |
| +0x218 | `swc1 f14,sp+0x8C` | Magnitude default +0 |
| +0x4E4 | `swc1 f0,sp+0x8C` | Optional 3D sqrt result overwrites zero |
| +0xFE8 | `lwc1 f4,sp+0x8C` | BOTH +0x218 and +0x4E4 may reach this read |
| +0xFFC | `swc1 f8,sp+0x8C` | Update overrides either prior definition |
| +0x1000 | `lwc1 f10,sp+0x8C` | Only +0xFFC reaches this read |

Both possible +0xFE8 incoming definitions have independently generated abstract CFG witness paths. The path witnesses are **not actual emulator executions and cannot establish path-condition feasibility**. No raw original instruction words, original assembly, proprietary game contents or full PC traces exported.

## Crucial native C comparison: control flow already retains two-source magnitude topology

The two independently native-compiled research C functions have the *same* two-source default/sqrt shape, but their compiler-chosen magnitude storage and spills differ from the original.

| Source | Native bytes/frame | Same original-position MIPS | Exact text relocation triples | Magnitude slot and reaching definitions |
| --- | --- | --- | --- | --- |
| Original USA ASM | 4320/232 | Exact | 101/101 | `sp+0x8C`, defaults +0x218 OR sqrt +0x4E4 reach +0xFE8 |
| F14 research C | 4440/232 | 117/917 | 30/101 | `sp+0xD4`, defaults +0x1C4 OR sqrt **+0x4E4** reach +0x1060 |
| F16 research C | 4412/232 | 86/906 | 20/101 | `sp+0xD4`, defaults +0x220 OR sqrt +0x500 reach +0x1044 |

F14 source's sqrt-result store occurs at **the exact original instruction offset +0x4E4 and uses f0**, but its stack displacement is wrong. Its default zero spills much too early at +0x1C4. F16 source retains all eight original branch-local f16 reset words but loses F14 and spills its magnitude at +0xD4 as well.

**The original magnitude slot is demonstrably occupied by *different* FP scratch data in both current C outputs**:
- Native F14 accesses `sp+0x8C` at eight PCs, with writes +0x314,+0x458,+0x544,+0xF50,+0xF64, and reads +0x2C8,+0x538,+0x748. None are magnitude's initial default or late update.
- Native F16 also accesses `sp+0x8C` at eight PCs: its two writes are +0xF2C,+0xF78, and the other six are reads.
- Original has 9/8/9 FP component accesses at `sp+0xA4/+0xA8/+0xAC`, plus 4/5/5 at `sp+0xB0/+0xB4/+0xB8`. Native candidates show **zero direct FP stack accesses** at `A4,A8,AC,B0,B4`, and only 4 at `B8`. Thus declaration-order and vector scratch ownership differ substantially, not merely the magnitude-zero literal.

This is a stronger C reconstruction constraint: **reallocate the scratch vector buffers so `sp+0x8C` can own one persistent magnitude value while preserving separate short-lived F16 reset zeros and delayed long-lived F14 initialisation**. The original magnitude's two reaching sources are *already* present in compiled C; another unnecessary Boolean guard rewrite will not solve stack allocation.

## Bounded native experiments

**2442 authentic SGI IDO 5.3 native C compilation/audit trials** were performed in 8 source-variant groups:
- 140 type-correct zero / initializer / volatile trials.
- 792 local/scoped/array/struct/union magnitude lifetime and address-taking variants.
- 190 typed task-structure field access trials (typical normal typed structs compile identically to generic field casts).
- 160 task-context pointer/branch representation trials (similarly codegen-equivalent).
- 960 attempts to separate gate zeros and F14/F16 lifetime through local variables, arrays, declaration order and assignment timing.
- 200 stack aggregate/vector object grouping variants.

None produced **original F14 and any original-position F16 reset instruction simultaneously**, nor the required `+0x218` `swc1 f14,sp+0x8C`. Highest same-position score in these groups remained 117 words / 30 relocations. These variants are **diagnostic source experiments**; not all have established semantic equivalence and none meets the native matching gate.

Separately, corrected original full-m2c-derived C (private scratch, not committed or distributed) compiled using authentic IDO, but yielded a **456-byte frame and only 3 same-position words / 1 relocation**. It is **not** a source candidate and supports treating raw m2c output as an analysis rather than original C.

## Actually passed and blocked

- Original pinned USA 32MiB pristine ROM full byte comparison **33,554,432/33,554,432 PASS**; original SHA-1 matched. This is an unmodified original baseline, *not* a C-replaced ROM.
- Eleven synthetic CFG tests, real original-ROM stack-site signatures and 1146-state reaching-definition proof **PASS**.
- Native SGI IDO 5.3 source builds of the strict F14 and F16 full-function reconstructed C, original ELF 101 relocations, original ROM 33 calls/nine sqrt and original-position instruction comparator reproduced **117/917, 30/101** and **86/906, 20/101**. Both explicitly **FAILED_NATIVE**.
- Fresh extraction and SHA256SUMS full **12-file source-only ZIP replay** PASS, including complete native builds and original CFG/stack occupancy audits.
- Candidate integrated full-USA ROM, canonical `decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci` and emulator gameplay: **NOT RUN**; neither C candidate matches original-address native code.

## Scripts and package

Reusable, byte-for-byte verified source-only tools on this research PR under `decomp/research/mini_ebisumaru_speed_20261120/magnitude_ssa_20261122/`: `original_cfg_ssa.py` (contextual original MIPS CFG), `compare_magnitude_ssa.py` (candidate original-offset magnitude paths), `audit_stack_owner.py` (FP stack footprint), `audit_scaffold.py` (native ROM/ELF/reloc), `test_original_cfg_ssa.py` (11 tests), `replay.py` (full pinned native replay), plus sanitized report/proof and PROGRESS.

The **complete C sources** and all scripts are delivered together in user-facing source-only archive `GOEMON_CLAMP_MAGNITUDE_SSA_20261122.zip`, exact SHA-256 **`dc209fc6003cacb38a808e68b9570412c3828c9347b5d8feda5f09a7625726d9`** (12 files, 26,028 compressed bytes). No private ROM, original ASM, original m2c C, native object/ELF/assets or IDO compiler distributed.

**Next:** reconstruct C declaration/alias structure that frees `sp+0x8C` for the magnitude and correctly positions original vector scratch at `sp+0xA4` and `sp+0xB0`, preserving original F14+F16 definitions, 232-byte frame, and 33-call/101-relo order. Keep PR #144 draft; original ASM production owned. Published USA G2 remains **1,965 C / 84,648 original machine-code bytes / 5,398 ASM**.

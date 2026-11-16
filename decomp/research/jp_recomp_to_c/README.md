# Japan ↔ USA original-IDO matching-C sources

**Do not infer production promotion from source presence in this directory.**

This draft research branch now contains **47 distinct, newly unpromoted USA C function source files** from original overlay files `file_12`, `file_13`, `file_14`, `file_15`, `file_17`, `file_18`, and `file_19`. The directory also retains `func_800166AC_172AC` (52-byte main-code bit-array helper), which **is already formally promoted**. Do not count it again.

The additional research source archive `goemon_jp_recomp_to_c_52_verified_20261116.zip` contains all 52 original cross-region isolates, their exact source SHA-256s, original USA/JP ROM offsets, standalone verifier, discovery scan and test suite. The research inventory has **49 newly unpromoted USA original-address C candidates**, 2,284 bytes; the two outside this seven-overlay native pass are the independent `main` (`func_800133E0_13FE0`) and `file_11` (`func_801F3AD0_5AF9E0`) helpers. Those require separate canonical production adapters.

## Native 47-function scratch: pass

A fresh source-verified, original 100%-ASM USA Splat rebuild was reconstructed from the user's exact original ROM and pinned IDO 5.3/toolchain, then 47 C functions were inserted into the **original** seven overlay linker layouts. Compiler-only zero alignment was trimmed without changing source instructions: 212 zero bytes from the C objects and 316 zero bytes from split ASM objects. After the correction, the build:

- Reproduced the **entire original 33,554,432-byte USA image** byte-for-byte, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Preserved exactly **7,376/7,376** positive-sized ELF FUNC identities (name, VMA and size), with no new aliases.
- Matched all original relocation tuple multisets in each affected overlay: `file_12` 7,051; `file_13` 9,589; `file_14` 3,041; `file_15` 1,625; `file_17` 1,739; `file_18` 3,365; `file_19` 1,078.
- Rebuilt **47 original functions / 2,220 instruction bytes** as exact native C, with zero external per-function relocations.

Full evidence: [47-function native scratch report](../../../docs/JAPAN_47_C_NATIVE_SCRATCH_20261116.md) and `native_scratch_47_evidence.json`. The separate, independently tested `goemon_47_native_promotion_scratch_20261116.zip` provides four fail-closed scripts, build wrapper and the detailed original-ROM/ELF proof, without original ROM, assets, compiler binaries or compiled objects.

**Critical limitation:** the exact ROM/ELF scratch started from the original **all-ASM** game, not the canonical **315-C** `decomp.verify` stage. This is not a combined **362-C G2**, and no canonical result/count should be changed until a full native 315+47 G2, original inventory and `decomp.local_ci` all pass. Japanese region acceptance is independently required.

# USA Mini Ebisumaru 384-byte speed selector — original-native exact (21 November 2026)

**PASSED_NATIVE_PRISTINE / RESEARCH_ONLY (not production G2).**

Target: `func_801E1C90_59DBA0`, ROM `0x59DBA0`, guest `0x801E1C90`, 384 bytes. Source: `selector_exact.c` (SHA-256 `3dcbf3eac6764dcd36e4ec402d5b0cffe6ce181ef84f40a9736fa507a495541b`).

## Exact compiler result

The existing source had 12 non-relocation word mismatches and a 380-byte ELF function plus four bytes of padding. Two source changes resolve all differences:

1. Declare the easing function with the correct **float** third parameter but pass literal integer **0** to both calls. Original IDO 5.3 now emits the original `addiu a2,zero,0` at both sites, rather than `or a2,zero,zero`.
2. Use one outer `retval=0`, assign each switch case's return value, and `goto final` into one `return retval`. The compiler now generates the original three-instruction default epilogue and all original branch displacements.

Authentic IDO 5.3 `-O2 -mips2 -G 0 -non_shared`: **384-byte ELF FUNC**, **87/87 non-relocation instruction words exactly identical**, **9 native .text relocations**, and eight exact jump-table relative target offsets `0x14C/0x154/0x15C/0x164*5`. Complete compiled unrelocated .text SHA-256 `ea84f86d0591c7ad8ce9f9d8a9484c1b1097a9615167c2f28d8666b04461d95a`.

## Full authentic pristine USA build (run twice)

Private original USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Original clean baseline full rebuild **PASS**, 33,554,432 bytes identical to original expanded ROM. Scratch C integration built at original `file_11` address also **PASS**, 33,554,432/33,554,432 byte-identical USA ROM, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Independently repeated from a fresh scratch staging clone with the same exact result.

Pristine baseline/staged linked ELF comparison: **7,376/7,376 positive-sized original FUNC identities equal**, **82,216/82,216 complete semantic relocations equal**, including **8,825/8,825 file_11 semantic relocations**. Zero positive ELF aliases or unexpected relocation changes.

**Jump table source-ownership detail:** original numeric eight-entry table remains at `0x8020B2E0` in `file_11` data. The scratch linker adapter validates compiler table targets, restores the unchanged original numeric data values in the staged table, removes the eight *extra compiler-only* table relocations and retargets exactly two compiler text relocations to the original jump-table symbol. No IDO-generated instruction word was patched. The original source ASM and ROM are untouched. This adapter is a scratch research staging procedure, not a production verifier bypass.

## Promotion remains blocked

The live `chatgptweb/decomp` branch has advanced independently to **1,956 verified USA C / 83,940 bytes / 5,407 ASM**. The selector was not in that batch. The complete branch cannot be cloned locally (shell DNS failure), so the required *combined* `python3 -m decomp.verify` against all **1,956** functions, strict `decomp.inventory` and full `decomp.local_ci` were **NOT RUN**. The official count remains **1,956**. No emulator gameplay test performed. Do not promote until the existing canonical native gates pass.

The independently tested scratch-staging Python script, ELF comparison script, full repro instructions and sanitized proof are included in conversation artifact `func_801E1C90_native_exact_2026-11-21.zip`. Do not commit original ROMs, Splat ASM, toolchains, objects, binaries or private memories.

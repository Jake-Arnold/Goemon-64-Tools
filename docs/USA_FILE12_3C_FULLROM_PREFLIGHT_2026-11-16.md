# USA file_12 — exact three-C full-ROM preflight

Date: 16 November 2026. Research, not canonical 318-C promotion.

## Original-USA authentication and combined linkage

- Original retail SHA-1: df8083a54296b8c151917c5333e1c85f014a2a66.
- Original decompressed 32 MiB SHA-1: 6ea0ed71032ce08fc2745f412d84936382197494.
- Pinned upstream revision: 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee.
- Original linked upstream ELF SHA-256: 83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038.

Six original-location C/ASM linker inputs cover file_12 text, ROM range 0x5C8770 to 0x5E3C90:

| Kind | ROM start | End | Instructions / bytes |
|---|---|---|---:|
| Original ASM | 0x5C8770 | 0x5D434C | 48092 |
| C dispatcher | 0x5D434C | 0x5D4400 | 180 |
| C state-2 callback | 0x5D4400 | 0x5D44B8 | 184 |
| Original ASM | 0x5D44B8 | 0x5D5B14 | 5724 |
| C active gate | 0x5D5B14 | 0x5D5B4C | 56 |
| Original ASM | 0x5D5B4C | 0x5E3C90 | 57668 |

All six original MIPS ELF input .text extents were trimmed only where trailing bytes were zero, and their section input alignment changed from 16 to 4. The linked .file_12 section retains VMA 0x8020D2A0, extent 0x2E0D0 and output alignment 16.

Fixes identified during integration:

1. The four-byte text-end datum D_802287BC_5E3C8C must remain an assembly data alias, not be treated as a new function by Splat.
2. The original full ASM object was also referenced by output data/rodata/BSS linker sections; keeping those references after splitting the text caused duplicate symbols. All those references were changed to the new prefix ASM object, with original bytes preserved.

## Executed acceptance checks

- Full decompressed USA candidate: 33,554,432 of 33,554,432 bytes identical, SHA-1 6ea0ed71032ce08fc2745f412d84936382197494.
- .rel.file_12: 7,051/7,051 relocation entries, identical multiset by address, relocation type, symbol name and resolved symbol value. Raw ELF relocation ordering is different and **not** claimed identical.
- Positive-sized ELF FUNC identities: 7,376/7,376 identical (name, virtual address, size), no extra alias function.
- Three original-address exact matching-C isolates: 420/420 instruction bytes and 25 external C-object relocations, tested separately.
- Six synthetic fail-closed integration regression tests passed.

The complete source-only integration archive was generated in the project session (goemon_file12_3c_fullrom_integration_20261116.zip), including original code-independent verification script, synthetic tests, original source-only C, and sanitized proof JSON. It includes no game ROM, generated assembly, ELF or other copyrighted binary.

## Strict gate still outstanding

This proof is the pristine pinned upstream plus three C functions, not a simultaneous central **315+3** C rebuild. Do not amend the canonical matching-C count or rewrite decomp/results/combined.json or inventory. The central verifier's existing multi-file12 stage preparation needs a new versioned adapter that can preserve all six original input boundaries. Only after successful canonical decomp.verify, complete ELF inventory/relocations and decomp.local_ci can the project claim 318 USA matching-C functions.

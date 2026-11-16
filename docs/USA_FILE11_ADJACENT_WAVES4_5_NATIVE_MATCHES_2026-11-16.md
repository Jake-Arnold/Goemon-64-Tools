# USA file_11 Wave 4+5 verified C adjacency — 16 November 2026

## Findings

The original 32 MiB USA image and ELF from pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` were authenticated, with native original IDO 5.3 `-O2 -mips2 -G0` testing.

**Wave 4:** five newly matched original-address C functions, 280 bytes; three exact contiguous units, 20 functions / 800 bytes. Offsets: `0x599CCC` (48), `0x59E82C` (52), `0x5B1808` (60), `0x5B186C` (60), and `0x5B18A8` (60).

**Wave 5:** three additional original-address matches, 164 bytes:
- `0x59E32C` (48): fixed-argument float-ABI dispatcher
- `0x59F088` (48): analogous float-ABI dispatcher
- `0x59A4CC` (68): actor-state conditional selects one of two handlers

All **three individually exact** and all **three combined contiguous units exact**:

| ROM range | Functions | Bytes | Exactness |
|---|---:|---:|---|
| `0x59E32C–0x59E368` | 2 | 60 | 15/15 instructions |
| `0x59A38C–0x59A510` | 11 | 388 | 97/97 instructions |
| `0x59F044–0x59F0B8` | 3 | 116 | 29/29 instructions |

These units have 16 distinct members, including 13 previously researched functions. Only three names and 164 bytes are newly claimed in Wave 5. All new offsets are disjoint from the previous 199 research candidates and Wave 4.

## Complete clean-upstream Wave 4+5 ROM integration

A separate original upstream checkout staged six combined C units (three Wave 4 plus three Wave 5) and preserved all intervening original assembly. Their total footprint is **1,364 machine-code bytes**. File_11 was linked with `SUBALIGN(4)`; ELF `.text` section *size headers* were trimmed to original extents without discarding relocations. Generated machine code and exact ROM boundaries were verified.

- **Whole 33,554,432-byte USA ROM byte-for-byte exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Original .rel.file_11 has **8,825** entries; candidate also has **8,825**.
- `(site, type, resolved symbol value)` relocation multisets are **identical**, not just equal in size.
- Pinned assembly SHA-256: `e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b`.
- Original ELF SHA-256: `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038`.

**Scope limit:** This is NOT the full current project 210+207-function central G2 or inventory gate. The uploaded pinned checkout predates the 210-function promotion. The canonical baseline stays **210 matching-C functions / 13,336 bytes**. Research-only pending pool becomes **207 functions / 7,444 bytes**. The hypothetical combined number is **417 functions / 20,780 bytes** after a still-pending formal promotion.

## Reproducibility and restrictions

Machine-readable source, address, original SHA and group definitions: `decomp/research/file11_adjacent_wave5_sources.json`. Structured evidence: `decomp/results/file11_adjacent_wave45_proof_20261116.json`. The separate local evidence archive includes Wave 4 and Wave 5 native verification scripts and a comparison script for the complete 32 MiB ROM and file_11 relocation multisets.

No ROM, generated assembly, copyrighted asset, linked object, original raw instruction stream, save or memory dump is committed. The Japanese full-ROM rebuild is unrelated and remains independently blocked by upstream USA assembly references.

Next: integrate waves 1–5 into a fresh copy of the **current** 210-function production source, run central `decomp.verify`, `decomp.inventory`, whole-ROM comparison and relocation audits before incrementing production counts.

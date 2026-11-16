# Japanese/USA file_11 — 101-function independent scratch verification
Date: 2026-11-16. Research-only, not a canonical C promotion.

## Inputs and parent
From PR #20's formally promoted 50-function file_11 stage on `chatgptweb/decomp` (210 central C functions) plus draft PR #24's 23 unpromoted research functions (73 scratch functions total). New work adds 28 original unclaimed functions, all with verified Japanese counterparts.

## 28 new exact original-address native matches
- **16 short actor/event wrappers** in USA ROM offsets `0x5B2004–0x5B2654`. Corresponding Japanese offsets `0x5B70AC–0x5B75F8`. Each has matching region-specific IDO 5.3 original-VMA instruction bytes.
- **10 short state and data helpers**: USA offsets `0x58E2D0`, `0x59E35C`, `0x59EE48`, `0x59EEF0`, `0x59EF04`, `0x5A1630`, `0x5A4070`, `0x5AA30C`, `0x5AAC94`, `0x5AB77C`.
- **Two nearby scene-state helpers**: USA `0x5B7150` (48 bytes) sets bit 4 of a 16-bit actor field before calling a helper; USA `0x5B71B4` (44 bytes) clears four halfwords and three floats. Their verified Japan counterparts are `0x5BC120` and `0x5BC184`.

Together these 28 functions are **892 native-exact instruction bytes per region**. Separate regional matching is not Japanese whole-ROM matching.

## Original-ROM 101-function proof
- Scratch USA mixed-C file_11 contains all previously verified 73 functions + 28 additions: **101 C functions / 2,348 bytes**.
- **86 ordered original-offset C/ASM text sections**, each checked against the generated original-VMA linker map.
- Rebuilt USA ROM **33,554,432 / 33,554,432 bytes identical** to the authenticated original; SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Overlay original VMA `0x801CB460` and size `0x41400`.
- All **101 original FUNC symbol names, VMAs, sizes and instruction SHA-256 identities** verified.
- Both separately linked pristine and candidate ELFs have the exact same **7,376 positive-size FUNC identity tuples**; no added or lost entries.
- All **8,825 semantic relocation tuples** identical; raw relocation order has exactly two three-record rotations at indexes `2506–2508` and `6131–6133`. Do not label raw relocation order identical.
- Splat introduced an extra FUNC alias at original 4-byte NOP USA `0x801F619C` (ROM `0x5B20AC`). Removed **only** that newly generated FUNC label; the NOP and its assembly ownership remain byte-for-byte unchanged. Two older v2 and one previous v3 false labels were also normalized as previously documented.
- **14 ROM-free regression/claim guard tests passed**, and the 28-pair original-VMA native probe was rerun to completion in both regions.

## Reproduction/source and gate status
Source-only archive: `goemon-file11-more-101-research-20261116.zip` (SHA-256 `4bc815edf75fdb75c15bd3573f71d5275be747a26c383dcada5ad9d812743add`). It includes reviewed 28-body C sources, regional names/addresses/external symbols and original SHA-256 digests, dual-region compiler probe, 101-function Splat stage, 86-chunk linker/ELF audit and 14 regression tests. No ROMs, generated game assembly, MIPS objects, compiler binary, or game assets.

Official central manifest remains **210 matching-C functions / 13,336 bytes**. The 101 scratch set contains the existing 50 promoted file_11 functions plus **51 unpromoted** research candidates: total central target if all gates pass = **261 functions / 14,620 bytes / 7,102 remaining assembly**. **No 261 full central G2 or Japanese whole-ROM gate was run.** No change to `decomp/manifest.json` or production `decomp/results/combined.json`; this PR stays draft.

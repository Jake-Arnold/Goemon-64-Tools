# Original-address USA/Japan `file_11` transition helpers: 104-function scratch verification

Date: 16 November 2026. **Research-only**; no central 264-function G2 or Japanese full-ROM proof was run.

## Fresh repeat verification

The authenticated original USA/Japan 32 MiB ROMs and pinned IDO 5.3 were used to repeat the exact native original-VMA comparison of the preceding 28 USA/Japan research matches. The original 101-function USA scratch ROM was **re-audited from real pristine/candidate ELF files**, with exact 33,554,432-byte ROM identity, 86 original linker extents, 8,825 semantic relocation tuples, 7,376 original positive-size FUNC entries, and 101 original function identities. All 14 prior research tests passed.

## Three additional exact matching-C functions

| USA VMA | Japan VMA | Bytes per region | Behaviour |
|---|---|---:|---|
| `0x801FB270` (ROM `0x5B7180`) | `0x80200180` (ROM `0x5BC150`) | 52 | Set byte at region-specific system pointer + `0x3AE23` and call seven-field reset |
| `0x801FC590` (ROM `0x5B84A0`) | `0x802014A0` (ROM `0x5BD470`) | 48 | Resolve pointer at system pointer + `0xCF8F0`; clear `0x14` in actor halfword +`0x22` |
| `0x801FC5C0` (ROM `0x5B84D0`) | `0x802014D0` (ROM `0x5BD4A0`) | 48 | Resolve same pointer; set `0x14` in actor halfword +`0x22` |

**Six regional native original-VMA comparisons exact**, 148 bytes per region. The two actor-flag functions directly follow the previously proven 12-byte callbacks at USA `0x801FC578` and `0x801FC584`.

## Exact USA 104-function scratch build

Two existing assembly sections at ROM `0x5B7180` and `0x5B84A0` were replaced by C without moving sections. The full independent scratch rebuild is **33,554,432 / 33,554,432 bytes identical**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Its 86 C/ASM object extents, 104 exact original-VMA C function symbols/lengths, overlay size `0x41400`, complete 8,825 semantic relocations, and 7,376 original function identities all match.

An initial candidate reproduced ROM bytes but dropped six ELF relocations by encoding `0x3AE23` and `0xCF8F0` directly as numeric constants. **That candidate was rejected.** Using original external symbols `D_3AE23` and `D_CF8F0` preserved the six HI16/LO16 relocation records while retaining exact machine instructions. Three exact three-record relocation-order cycles occur at indices `2506–2508`, `6131–6133` and `6762–6764`. All relocation tuples are identical as a multiset; **raw order differs**, and the exact cycles are pinned in the auditor.

**Regressions:** 14/14 existing and 9/9 newly added scratch/source tests passed. No complete repository Local CI was performed.

## Nearby functions still in assembly

USA `0x801F8428` (52 bytes; JP `0x801FD330`) and USA `0x801F8644` (44 bytes) did not match the original compiler's instruction scheduling in bounded C trials and remain **unpromoted**. Do not infer that a matching implementation is available from a similar C source or a matching ROM prefix.

## Production gate

Formal central baseline: **210 C functions / 13,336 bytes** (the 50-function v2 `file_11` promotion). The isolated 104-function `file_11` scratch build has **54 additional research-only** functions beyond those 50. A future complete original-USA central verification would need to prove **264/264 functions, 14,768 bytes, 7,099 remaining ASM entries**, original ROM identity, all relocation/symbol ownership and inventory, plus full Local CI. Those figures are *targets, not completed gates*. The Japanese whole-ROM blocker remains separate.

Full repeatable source-only package: `goemon-file11-followup-104-research-20261116.zip`, SHA-256 `efd9daa63d176fe4b915363d7e1f9615ea0f6e704842c73fbbc00e8e43cb4cc6`. Contains staged C sources, exact pair/region compiler probe, source-only original 101-function registry, strict ELF/ROM auditor, metadata and 9 regression tests. **No ROM/ELF/object/game assets/IDO executable are committed.**

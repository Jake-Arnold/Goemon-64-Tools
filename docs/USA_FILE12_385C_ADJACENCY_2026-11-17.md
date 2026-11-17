# USA file_12: 385 C functions in one exact original-upstream build (17 November 2026)

**Research checkpoint, not a canonical matching-C promotion.** Built against original verified USA ROM, pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original IDO 5.3 and MIPS GNU binutils.

## Scope and exact code results

The adjacent function scan found **374 consecutive 36-byte functions** from VMA `0x8020DE40` through `0x802112D8` (exclusive; ROM `0x5C9310–0x5CC7A8`). Each loads a distinct static descriptor address and calls `func_80013AC4_146C4`. The 374 functions were compiled **as one C translation unit**, with the original symbol names extracted from authenticated local Splat assembly. This complete 13,464-byte C-generated span is byte-identical to the original USA ROM. No original ROM or game assembly is checked in.

Eight additional nearby C helpers are now individually original-VMA exact: `0x80218D7C` (20 B), `0x80218D90` (24 B), `0x80218DF8` (12 B), `0x80218E04` (120 B), `0x8021A308` (8 B), `0x8021A310` (24 B), `0x8021A4DC` (8 B) and `0x8021A7E8` (112 B). Their eight C sources are checked in under `decomp/research/file12_spatial/adjacent/`, each independently matched with IDO 5.3 at the original address.

Together with the existing three lifecycle functions from the stacked parent branch (420 B), this produces **385 functions / 14,212 matching code bytes** in 12 C source objects.

## Actual full-ROM integration verification

An independent pinned original-USA workspace was decompressed and extracted anew; its unmodified baseline rebuilt byte-exact. Two separate expanded-C candidate builds then passed, one using the generated 374-function source file and the second regenerating that source directly from the authenticated original Splat symbol declarations.

| Gate | Verified result |
| --- | --- |
| Original retail ROM SHA-1 | `df8083a54296b8c151917c5333e1c85f014a2a66` |
| Original, baseline, and candidate decompressed ROM SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Full candidate ROM bytes | **33,554,432 / 33,554,432 identical** |
| Original/candidate `.rel.file_12` semantic records | **7,051 / 7,051 identical multisets** of site, relocation type, symbol name, resolved value |
| Original/candidate positive-sized ELF FUNC identity | **7,376 / 7,376 identical** name/address/size entries |
| MIPS code contributed in C | **14,212 bytes** |
| Input layout | 12 C + 8 ASM input sections; original output `.file_12` VMA/size/alignment |
| Additional ROM-free tests | **6 / 6 passed** |

**Raw relocation ordering differs:** code and semantic-relocation multiset matches do not prove byte-identical `.rel.file_12` entries.

The integration uses original-address ASM/C ownership, trims only zero-only section padding, lowers input ELF `.text` alignment to 4, preserves the original zero-size trailing datum `D_802287BC_5E3C8C`, and correctly reassigns the original unsplit assembly object's data/rodata/BSS linker entries to the first replacement ASM input.

The full source-only reproduction bundle `goemon_file12_385c_research_20261117.zip` was generated in this research session. It includes the pinned wrapper C generator/expanded driver, original-upstream linker adapter, tested source, six synthetic regression tests and detailed sanitized per-object proof metadata. The bundle contains no original ROM, generated original assembly, linked ELF, copied asset data, saves or binaries.

## Strict boundary and next targets

**This proves original-upstream ASM + 385 file_12 C**, not the simultaneous canonical prior **315 USA C + 385 C**. Production remains 315, not 700; central `decomp.verify`, `decomp.inventory`, `decomp.local_ci` and coexistence must all pass before formal promotion.

The **actual general actor-manager functions** are still in ASM and remain higher-value semantic targets: spatial index `0x8020D2A0`, grid scan `0x8020D36C`, actor constructor `0x80218A54` and range-based release `0x8021A328`. Do not represent the 374 repetitive descriptor wrappers as the actor spawning algorithm itself.

# USA file_12 — 387-C canonical-overlay coexistence proof (17 November 2026)

**Status:** Exact original-ROM mixed-ASM/C build PASS for **385 research functions + 2 canonical file_12 C functions**. This is **not** a simultaneous 342+385 central G2 or an approved USA 727-C promotion.

## Original-USA native tests independently executed

The user-provided original USA retail ROM was independently hash-authenticated and decompressed. The pinned original upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` Splat extraction and MIPS/IDO toolchain reproduced all 33,554,432 bytes of the original ROM. Two distinct 387-function builds (including the reproducible `integrate_387.py` driver) replaced 14 translation units in `file_12` and passed the following comparisons:

| Gate | Result |
| --- | --- |
| Original retail USA SHA-1 | `df8083a54296b8c151917c5333e1c85f014a2a66` |
| Rebuilt 32 MiB USA SHA-1 | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Complete ROM equality | **33,554,432 / 33,554,432** bytes |
| 387 original `file_12` C functions | **14,268 bytes** compiled at original VMAs |
| Original vs candidate `.rel.file_12` | **7,051/7,051**, identical (site, relocation type, name, resolved value) multisets |
| Positive-sized ELF `FUNC` identities | **7,376/7,376** identical |
| Added 387 coexistence guard tests | **5/5 PASS** |
| Existing expanded 385 guard tests | **6/6 PASS** |

Original `.file_12` section VMA `0x8020D2A0`, size `0x2E0D0`, linked output alignment 16 retained. Source files for the two already-canonical `file_12` functions are read from `decomp/candidates/` and pinned by their exact SHA-256:

- `func_80222034_5DD504`: `bce7049e5438f50b9cb5bd7cea430fb2101067dcfdab760003ecaef3c2527fd2`
- `func_80222168_5DD638`: `2fff2f49dbeb427200ef469596a8a229c9763db6f70bee93e662a1b1016ef6d1`

Raw relocation *ordering* changes, although the full semantic relocation multiset matches. No proprietary ROM/ELF, original ASM extraction, or game asset is committed.

## Cross-branch canonical audit

As of pinned canonical commit `1961f1333e8a5007c3cf8df5dfa0d0ca5a0cea8b`, `decomp/results/combined.json` reports USA **342/342 C functions**, **17,568 original code bytes**, exact 32 MiB ROM identity; `decomp/results/inventory.json` independently reports 7,376 ELF function identities. The live canonical comparison file was checked for all 342 code intervals against the new 385 interval inventory: **zero overlaps**.

The **hypothetical 727-C target** is 342 + 385 functions / 31,780 original C code bytes. Its production status is **NOT VERIFIED**. The local 387-function build used original assembly for the other 340 canonical C functions. Therefore it cannot substitute for one full combined `decomp.verify`, `decomp.inventory`, and `decomp.local_ci` run. The current USA production matching-C count remains **342**.

## Reproduction and exact source

Run the reviewed `decomp/research/file12_spatial/integrate_387.py` against a pinned fresh original USA build, passing `--canonical-source-dir decomp/candidates`, a distinct new `--candidate` directory and a new `--report` path. It delegates all native object/linker/ROM checks to the earlier exact `integrate_385.py` driver. Optional `--canonical-comparison decomp/results/combined.json` enforces the exact 342-function prior proof and rejects overlapping ranges.

The committed integration-driver Python Git blob equals the original locally executed source, SHA-1 `c182c219d800307f7e3016fd1d56b7aed45c8fd2`; the adjusted five-test suite Git blob equals the locally passing test source, SHA-1 `a691b0b54dfcc97bd95b606da3e0d276eca71ead`.

### Uncompleted full production gate

The entire private `chatgptweb/decomp` source tree is accessible through GitHub connector reads but not mounted as a local Git checkout, and the execution container cannot network-clone GitHub. Consequently **no 727-C simultaneous compilation or complete central verifier/CI pass was executed**. This remains a research-only stacked draft. Do not change the manifest, combined proof, inventory, or official 342 function count.

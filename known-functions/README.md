# Verified matching-C game functions — source-only browser

This folder collects the known, original-address, native-G2-accepted reconstructed C functions for Mystical Ninja Starring Goemon (N64) and the Japanese game revision. This is a **browse-only snapshot** of the source accepted by the project's native original-ROM verification, as recorded on the original `chatgptweb/decomp` branch at commit `c699608fa79ba8058546a6b2d9caf9dc64768dec` (22 November 2026).

| Revision | Previously accepted C functions | Original code bytes | C source files here | Remaining original ASM functions |
|---|---:|---:|---:|---:|
| USA | 1,965 | 84,648 | 1,265 | 5,398 |
| Japan rev-0 | 2,369 | 126,612 | 2,050 | 5,007 |

## Layout

- `usa/core/`: reviewed matching-C translation units tracked in the USA manifest.
- `usa/candidates/`: individually accepted implementations originally staged via candidate source files.
- `usa/batches/`: verified promotion-batch C sources, including the 166 file11 originals recovered from the source-text fixture, and all 132 wide132 C files extracted from the original repository's archived source bundle.
- `japan_0/core/`: 35 base C translation units implementing the first 39 Japan routines.
- `japan_0/ported/`: the four accepted character-switch functions, 290 source-generated verified JP callbacks/no-ops, and the 99 verified USA-to-Japan source ports with Japanese function names.
- `japan_0/batches/`: native-G2-accepted Japanese source batches: 1,686 original-address functions from JP1686 (including grouped-source units), 3 glitch/start functions, 2 VM functions, 145 short-function ports, subsequent donor/tiny/retry/expand batches, and 55 more JP55 functions.

The two JP1686 functions that matched isolated instructions but failed semantic relocation preservation are **excluded**: `func_08001228_6B3168`, `func_080012AC_6B51AC`. The USA file `27FE0.c` belongs to the pinned original upstream checkout and is not duplicated as a newly reconstructed function here.

## Source and proof authority

These files are **reference copies**, not new independent promotions. The accepted-function counts and provenance are documented in `decomp/CONTINUE.md`, `decomp/README.md`, `decomp/results/usa_scheduler6_1965_g2_20261121.json`, `decomp/results/japan_0_2369_jp55_g2_20261122.json`, and the prior batch manifests/proofs. In the original pipeline, some JP functions are generated as separate translation units from a source template. The consolidated 290-noop C listing intentionally renders those functions together for reading. The JP ported files are reconstructed from the original stage adapters' source-selection and name-substitution rules for browsing. Source-file count is **not** function count.

Only `.c` function sources appear under the regional directories. They may reference the original project's headers, external symbols and original linker sections, which are not replicated here. **Do not use the collection as a standalone build target** or replace the production stage with these combined files.

The branch's snapshot does not modify `main`, accepted source ownership, ROMs, original assembly, G2 evidence, or toolchain. Its Git-tree/file membership was checked against the existing proof and manifest records; **no new full-ROM build, native G2 re-verification, local CI or emulator test was run** for this copy-only presentation.

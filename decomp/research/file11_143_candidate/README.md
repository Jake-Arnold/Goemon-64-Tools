# Goemon USA `file_11`: 143-function matching-C promotion candidate

**Status:** native verification and full-ROM clean-upstream integration passed; **not formally promoted** to the current `decomp.verify` manifest.

Date: 16 November 2026. Research branch: `chatgptweb/file11-expansion-20261116`, draft PR #23.

## Verified results

| Gate | Result |
|---|---|
| Original retail USA source and version | Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` |
| Original decompressed ROM | SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494` |
| Original generated file_11 assembly | SHA-256 `e936f86295b8d8795369fd6db6a42da5b13184b9856058878066b9448e4a5f8b` |
| Original ELF | SHA-256 `83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038` |
| Original-address linked C functions | **143** |
| Complete compiled C code coverage | **3,908 bytes**, 44 C groups |
| Prior production file_11 C functions | 50 functions, 1,064 bytes |
| Additional distinct functions with full-ROM research integration proof | **93 functions, 2,844 bytes** |
| File_11 C/ASM object extents and pinned hashes | **88/88 exact** |
| Original-linked symbols and function sizes | **143/143 exact** |
| Full USA ROM build | **33,554,432/33,554,432 bytes exact** |
| Semantic file_11 relocation multiset | **8,825/8,825 exact** |
| Local mutation/contract regression tests | **9/9 pass** |

The 143 consist of the previously published 50, all 77 candidates from the first callback/reset research pass, and 16 additional functions in the six Wave 4–5 contiguous groups that are not part of those 77. The contiguous groups also contain functions already found in Wave 2/3: these are **not counted twice**. The new 93 functions form a subset of the currently unpromoted pool of 207 candidate functions, not an addition to that pool.

**Critical gate still missing:** the independently exact USA build above uses the authentic *pristine upstream baseline* and its file_11 segment, not the source tree reconstructed by the project's current canonical **210-function** `decomp.verify` build. A combined 210+93 central verifier/whole-ROM/inventory acceptance gate has not run. The official baseline stays **210 functions / 13,336 bytes**. Prospective only after that gate is **303 / 16,180**. The remaining 114 of 207 research functions need their own integration stage. A complete 417-function promotion is also unproven.

## Source files

`file11_143_source_fixture.json` contains 44 independently pinned C translation units (with native source, original address, original instruction SHA-256, original symbol metadata and expected compiled-object SHA-256), plus all 44 intervening ASM slices represented only by address and SHA. It contains no original machine-code bytes or extracted assembly.

`verify_file11_143.py` does the following, fail-closed: checks original source/ELF/ROM identities; validates every original symbol boundary and disjoint C ownership; copies the pinned upstream build into a *new* scratch directory; stages all 44 C groups and original assembly slices; regenerates Splat; compiles with the original IDO 5.3/MIPS toolchain; validates and trims only trailing zero `.text` alignment padding, preserving relocations; links the complete ROM; verifies 143 original symbol ranges; and compares the 32 MiB ROM and all 8,825 semantic relocations.

`reproduction_proof.json` is the verified proof from an independent second clean checkout replay. `test_file11_143.py` contains nine negative/positive fixture regression checks.

## Run on native Ubuntu

The upstream pinned checkout must already have its original ROM decompressed, Splat extracted and original exact ROM built. Set the original toolchain environment from `GOEMON_BUILD_ENVIRONMENT.md` (including the standalone Python 3.12, MIPS binutils and shared-library path), then run:

```bash
"$PY" verify_file11_143.py \
  --upstream /path/to/clean/pinned/mnsg-japan \
  --workdir /tmp/goemon-file11-143-replay \
  --splat-script "$SPLAT_SCRIPT" \
  --report /tmp/goemon-file11-143-replay-proof.json
```

The runner does not reuse or overwrite a pre-existing workdir/report. Reproducing the full project 210+93 acceptance requires adapting the current verifier's `overlay_file11_stage` contract to the 143-function layout, followed by a fresh canonical `decomp.verify` and `decomp.inventory` acceptance run. **Do not change the production manifest/count without that separate success.**

The original copyrighted ROM, generated assembly, linked binaries, original ELF and extracted assets are not distributed or committed.

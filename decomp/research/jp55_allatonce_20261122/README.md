# Japan rev-0 JP55 full native matching-C promotion — 22 November 2026

**Status: `PASSED_G2_LOCAL` — 55 previously assembly-owned functions accepted by full native Japanese original-ROM verification.**

One incorrectly counted historical research function, `func_801E818C_5A415C`, was already accepted in JP1686 and is **not** in this source batch. The initial 56 research records were deduplicated against the actual JP2314 linker ownership. The remaining **55 genuine ASM-owned functions** spanned **33 original assembly objects** and preserved every prior accepted C function.

## Measured full build results

| Evidence | Measured result |
|---|---|
| SGI IDO 5.3 compilation, linked at original addresses | PASS for all 55 |
| Original expanded Japan 32 MiB image | **33,554,432 identical bytes**; SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |
| Original retail Japan 16 MiB image | **16,777,216 identical bytes**; SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Original ELF function identity multiset | **7,376**, unchanged |
| Original semantic relocation multiset | **80,747**, unchanged; SHA-256 `e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20` |
| Strict original C/ASM function ownership | **2,314 C → 2,369 C**, **5,062 ASM → 5,007 ASM** |
| Original matching C instruction bytes | **123,236 → 126,612**; new **3,376** |
| Full `python3 -m decomp.local_ci` after integration | **PASS** (exit code 0) |
| JP55-specific ROM-free regression tests | **4 PASSED** |
| Native gameplay/emulator | **NOT RUN** |

The original ROMs, IDO compiler and generated assembly are **not** in this repository or its research bundle. The user's original Japan ROM and pinned upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` were required.

## Reproduce the verified full gate

In an isolated clean pinned original upstream checkout, with the original Japanese ROM, extracted dependencies and runtime in separate locations:

```bash
bash decomp/build_japan_jp55_promotion.sh \
  /path/to/clean-pinned-mnsg \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
```

The script must start with an unbuilt upstream checkout. It authenticates the pinned commit, runs the full original Japanese JP2314 baseline build and local CI, stages only the 55 proven original ASM owners, compiles their C and adjacent ASM, links at the original VMAs, compares the entire expanded-ROM image, all function identities, all original semantic relocations, strict inventory, then compresses and compares the retail original 16 MiB cartridge and runs full local CI. Each stage fails closed on drift or mismatch. Generated files stay in that private local upstream checkout.

The staged sources and SHA-256s are in [manifest.json](manifest.json). [G2 proof](../../results/japan_0_2369_jp55_g2_20261122.json), [strict inventory](../../results/japan_0_2369_jp55_inventory_20261122.json) and [publication ledger](../../results/japan_0_2369_jp55_publication_20261122.json) are separate from the original USA-only canonical results. The original-USA matching-C counts were not changed or retested in this Japan-specific batch.

## Header installation for the original IDO build

The original upstream Makefile converts C into `build/japan_0/src/.../*.encoded.c` before running IDO, so quoted relative headers are not resolved from the source directory. The integration adapter therefore places identical pinned source headers both alongside `src/jp55/*.c` and under `src/` (already in IDO's `-Isrc` include search). This fixes source-directory lookup without changing original instructions or rewriting the toolchain.

## Limitations

This is verified original-ROM matching C, not an N64 gameplay smoke test. The source for `func_8021251C_67BC0C` uses a MIPS32 address-valued linker symbol and is intentionally not treated as portable 64-bit host pointer arithmetic. The previous host regression for `func_801D0B90_6630E0` contained an obsolete incompatible-pointer diagnostic; the current source compiled under host GCC sanitizers and matched in the full original MIPS build. No original Japanese ROM, generated assembly, proprietary compiler or executable is committed.

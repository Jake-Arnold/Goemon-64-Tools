# Japanese original-address matching-C: 1,686-function combined promotion

**Region:** Japan-0 only. **Initial full local native acceptance:** 20 November 2026. **Publication:** pending GitHub branch update. **Current source target:** `chatgptweb/decomp`. Never modify `main`.

This directory contains the 1,688 original isolated-exact research sources and the exact original-ROM source ledger, including two C sources that **must remain original ASM** in the production build:

- `func_08001228_6B3168` at Japanese expanded ROM offset `0x6B3168`
- `func_080012AC_6B51AC` at Japanese expanded ROM offset `0x6B51AC`

Those two standalone C bodies reproduced the machine instructions, but their combined replacement discarded five original `R_MIPS_PC16` branch-relocation records. They are **not accepted/promoted**. The staging module enforces this exclusion.

The other **1,686 functions / 101,448 code bytes**, across **1,663 grouped source units** and **298 active current ASM owners**, passed the original JP432 plus new source **complete native** gate in a fresh pinned environment. Expanded ROM SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; retail SHA-1: `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`; all 7,376 ELF functions, 73 code sections and 80,747 semantic relocations preserved, including the same original hashes. The reported accepted local total becomes **2,118 JP C / 111,856 original instruction bytes / 5,258 ASM remaining**. The USA decomp result is unchanged.

## Rebuild

Reconstruct the private Japanese ROM/tools using `GOEMON_BUILD_ENVIRONMENT.md`. Invoke:

```sh
GOEMON_JOBS=8 bash decomp/build_japan_1686_promotion.sh \
  /path/to/fresh-pinned-mnsg /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
```

The script rebuilds the prior JP432 in full, fail-closes on any original address, source hash or linker layout drift, generates 1,686 C placements and the retained ASM fragments, compiles the original IDO compiler, normalizes **zero-only** compiler section padding, compares the complete expanded and retail ROMs, validates original ELF positive function identity + original relocations, then runs complete `decomp.local_ci`. The main stager is `decomp/japan_1686_promotion.py`, and the immutable candidate ledger is `candidates.csv`. Its three `m2c_types.h` compatibility headers stay adjacent to their original source groups; the stager mirrors them to generated encoded C compilation paths. No copyrighted ROM, extracted ASM, compiled binary or proprietary toolchain is committed.

## Proof and limits

See `decomp/results/japan_0_2118_promotion_20261120.json` and `decomp/results/japan_0_2118_inventory_20261120.json`. Two fresh independent pinned upstream workspaces have reproduced the full original ROM, ELF function identity and relocation digests; complete post-test-fix local CI also passed. Full-ROM byte equality is the acceptance criterion, not isolated source exactness alone. The branch publication step must include all source, manifests, stager, proof, tests, `decomp/CONTINUE.md` and `PROGRESS.md` in one commit, re-fetch the resulting remote SHA, and only then record publication. A local passing verification is not a remote GitHub promotion. Emulator gameplay and C-Right glitch exploitation tests have not been run.

The Japanese C-Right stage initializer `func_80212514_5CDAA4` and main scheduler `func_800343A4_34FA4` remain assembly and are **not** counted in this promotion.

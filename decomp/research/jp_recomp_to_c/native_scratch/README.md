# USA native C promotion scratch: reproducibility

**Scratch-only original-ROM acceptance. Do not update canonical counts based on this check alone.**

1. Obtain the *user-owned* exact original USA expanded ROM (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`) and a pinned, freshly Splat-split original `mnsg` checkout with a complete original-USA all-ASM ROM and ELF baseline.
2. Unpack the independently hash-verified `goemon_jp_recomp_to_c_52_verified_20261116.zip` source archive with `manifest.json` and `src/*.c`.
3. Configure the original IDO 5.3 compiler and MIPS binutils using `GOEMON_BUILD_ENVIRONMENT.md`. Use the host `/usr/bin/python3` to execute the scripts.
4. Set three environment variables and run the wrapper from this directory:

```bash
export GOEMON_BASELINE=/path/to/pinned/original/mnsg
export GOEMON_C_SOURCE_ARCHIVE=/path/to/goemon_jp_recomp_to_c_52_verified_20261116
export GOEMON_CANDIDATE=/tmp/goemon-usa-47-fresh-scratch
bash build_and_verify.sh
```

This fail-closed wrapper refuses to overwrite an existing candidate checkout. It copies the pristine source, splits exactly seven original overlay assembly units around 47 original function extents, compiles all 47 C sources, trims **only independently verified zero padding** from C and split ASM, builds the complete original USA ROM, and verifies **all original 33,554,432 bytes, the full 7,376-positive-FUNC identity multiset and all seven complete relocation multisets**. Scripts abort rather than modify a nonmatching source, unexpected compiler output, nonzero padding or altered ELF.

The scripts are also preserved in the independently exported `goemon_47_native_promotion_scratch_20261116.zip`. The reference proof is `../native_scratch_47_evidence.json`.

**Not included in these checks:** the canonical 315-C source-stage composition, an integrated 362-C decomp G2, `decomp.inventory` on the production 315+47 layout, complete `decomp.local_ci`, and independent Japanese full-ROM acceptance. The 315-C canonical manifest and proof are unchanged.

# USA 506-function wide native IDO research — 18 November 2026

**RESEARCH_ONLY.** This pull request publishes a metadata-only handoff for a separately delivered ChatGPT source archive. It **does not include the 506 C source files**, the original ROM, any game code binaries, the private toolchain, a full canonical verification, or new accepted C entries.

The research archive is `goemon_usa_500_native_research.zip`, SHA-256 `471669dbefab4860978dd06a9f44340536205163236834567455c74df34be54e`, distributed to the project owner in the session that generated this report. This GitHub metadata alone **cannot replay 506 exact matches without that source archive**.

## Evidence actually run

- Original retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Original 32 MiB expanded SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Pinned upstream source commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Unchanged original upstream USA build reconstructed all 33,554,432 authentic ROM bytes.
- Exactly **506 new original-address C routines** from **25 original ASM source files** matched **21,652 original MIPS instruction bytes** under original IDO 5.3 `-O2 -mips2`. The independent replay compiled all 506 C sources from the delivered ZIP, resolved referenced external symbols to their original guest VMAs, and matched original instruction bytes and lengths at every address: **506/506 PASS**.
- GCC `-std=c11 -Wall -Wextra -Werror -O1 -fno-omit-frame-pointer -fsanitize=address,undefined` ran semantic host regression on nine representative reconstructed source functions: **PASS**. No claim that all 506 underwent semantic host tests, runtime gameplay tests or automatic interface validation.
- Prior research batches 202/109/53 and accepted canonical evidence were deduplicated by original ROM offset. Three extra crossregion47 previously accepted offsets were explicitly **excluded**: `0x5D52D8`, `0x5D5310`, `0x5D7AF8`.

## Production boundary

Official accepted remains **987 USA C / 42,640 bytes, 39 Japan-0 C**. Conditional `987+506=1493` is **not** an accepted count. Complete 506-C pristine-upstream scratch ROM integration and current **987+506 canonical `decomp.verify`**, `decomp.inventory`, complete original ELF function/relocation audit and full `decomp.local_ci` were **NOT RUN**. The isolated original-native compiler host cannot materialize the authenticated current entire canonical 987-C source tree because shell GitHub DNS fails.

Do not merge these matching-C functions into production until the original sources are made available in the build environment, deduplicated against the then-current HEAD and all acceptance gates pass. Keep existing ASM ownership intact. This branch changes only research metadata and runbooks.

See `decomp/results/usa_506_isolated_native_research_20261118.json`. Separate GitHub research PRs #73 and #74 contain the prior 53- and 109-function work; the previous 202-function batch was delivered separately without a PR.

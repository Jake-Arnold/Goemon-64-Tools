# C-Right file12 native matching-C research — 23 November 2026

Status RESEARCH_ONLY. Base stable/decomp 1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e verified by source archive COMMIT.txt and SHA256SUMS, all original ROM hashes, pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee and original IDO5.3. Existing open research PRs and canonical ASM ownership checked.

| Region | Function | Expanded ROM offset | Exact original native instructions | Named relocations |
| --- | --- | --- | ---: | ---: |
| USA | func_8020D6BC_5C8B8C | 0x5C8B8C | 26/26 | 6/6 |
| Japan-0 | func_802124AC_5CDA3C | 0x5CDA3C | 26/26 | 6/6 |
| USA | func_8020DD78_5C9248 | 0x5C9248 | 32/32 | 10/10 |

All three have original instruction bytes, object ELF FUNC extents and named relocation offset/type/symbol tuples verified at their true original VMA. Nine compiled negative-source controls all rejected; original USA 76-byte descriptor comparator FAILED_NATIVE, best 9/19 words, ASM preserved.

A named descriptor-pointer local gives 26/26 original words in both regions. Semantically equivalent inline-expression source gives 12/26 and different first LUI register allocation in both. This is a limited two-region source-shape compiler observation, not a universal rule.

In **two independent clean original-upstream USA checkouts**, simultaneously staging both USA functions (232 bytes) into original file12 reproduced the entire 33,554,432-byte original USA expanded ROM (SHA1 6ea0ed71032ce08fc2745f412d84936382197494), all 7,376 positive ELF FUNC identities, and 82,216/82,216 original-pristine semantic relocation identities. Exactly three independently guarded original ABS symbol-type NOTYPE-vs-OBJECT differences were corrected in ELF st_info metadata only, with no ROM/code/relocation change. Original pristine ASM baseline (82,216 relocations) is NOT the canonical USA 2,316-C combined build (82,103 relocations). This whole-ROM research is NOT canonical G2 promotion.

Canonically accepted remains USA 2,316 C and Japan 2,528 C. JP candidate complete-ROM G2, canonical original-ROM/ELF/strict inventory/promotion-integrity and full local CI NOT PASSED. Full CI was attempted but encountered unavailable compiler/dependency and verifier/ledger failures and was interrupted. No gameplay freeze proof.

Complete reproducible source-only artifact **Goemon_CRight_Native_Research_20261123.zip**, containing Python original-ROM replayer, source fingerprints, all nine compiled negative controls, full original-USA scratch integration script and detailed JSON, is downloadable in the originating conversation. This repository research checkpoint includes the three native C sources, inline negative controls and sanitized summary. No ROMs, raw game ASM, original assets, objects, savestates or toolchain in Git.

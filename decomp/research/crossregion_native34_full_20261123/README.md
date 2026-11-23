# 34 exact native original-region C reconstructions from USA/Japan cross-region donor audit

**23 November 2026 — RESEARCH ONLY; zero canonical matching-C promotions.**

## Source authority
- Live repository baseline `stable/decomp@838e9f87c3a860973e9d168b58fcf88bd456bfb4` at task start, open PRs inspected, `BRANCHES.md`, `AGENTS.md`, `decomp/CONTINUE.md`, the autonomous skill and executor protocol read. The current live branch must be re-fetched before any promotion.
- Original USA expanded 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; original Japan-0 expanded 32 MiB SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded` independently reproduced from the uploaded authenticated retail ROMs using pinned upstream `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Executed **actual native SGI IDO 5.3**, executable SHA-256 `76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0` with `-c -G 0 -non_shared -O2 -mips2` on all candidates and native C negative controls. Binary code compared at every target's original ROM offset, size and original-code SHA-256.
- Seven explicit-symbol candidates plus the USA callback case (8 total) were additionally linked at the original function VMA using read-only symbol addresses and a narrow `.text : SUBALIGN(4)` linker script, without patching any code bytes. **This is a single-function isolated link, not a full original translation-unit or regional ROM proof.**

## Proven results
- **34 distinct isolated original-function native matches; 1,364 original instruction bytes**. 33 Japanese and 1 USA.
- **34/34 independent source-mutated negative controls rejected**. The standalone replay in this archive **passed 34/34** again against both original 32 MiB ROMs in a fresh output workspace.
- 24 Tier A unique identical-code donor matches, 2 Tier B ambiguous identical-code donor matches, and 8 Tier C single-word-difference regional donor matches.
- **29 additional independently reconstructed exact C**; five Japanese overlay predicates (`func_801ECEC8_5A8E98`, `func_801ECEE8_5A8EB8`, `func_801ECF10_5A8EE0`, `func_801ECF40_5A8F10`, `func_801ED030_5A9000`) reproduce previous isolated source research in draft PR #183, and must not be counted as novel.
- The other 6 Tier A targets, 6 Tier B and 43 Tier C destinations do **not** have native verified C from this package. Attempted and failed C variants remain in attempt logs; no systematic unknown C/ASM equivalence is inferred for all 583 possible donor destinations.

## How to replay (private original inputs required)

```sh
python3 replay.py \
  --usa-rom /private/usa/baserom.decompressed.z64 \
  --jp-rom /private/japan/baserom.decompressed.z64 \
  --cc /private/mnsg/tools/ido-5.3/cc \
  --objcopy /private/bin/mips-linux-gnu-objcopy \
  --ld /private/bin/mips-linux-gnu-ld \
  --binutils-lib /private/runtime/lib \
  --out /tmp/new-goemon-native34-replay
python3 test_metadata.py
```

The replay fails closed on the original ROM SHA-1 and 32 MiB size, native IDO executable SHA-256, exact candidate and negative C source SHA-256, and all original target instruction-body fingerprints. It writes generated objects and binaries **only under the user's separate private `--out` directory**, never into this source archive. No original game instruction bytes or proprietary binaries are included.

## Acceptance and compiler boundaries

`ISOLATED_NATIVE_EXACT` and `ISOLATED_LINKED_EXACT` are research statuses. **NOT RUN:** staging on the full live source manifest, complete original-source translation-unit placement, full original 32 MiB ROM identity, full 7,376 ELF identity proof, complete original relocation graph, fresh region-specific strict inventory, `decomp.promotion_integrity --validate`, complete `python3 -m decomp.local_ci` and original gameplay. This task cannot claim any new officially accepted matching C. The live GitHub branch cannot be cloned in this shell (DNS unavailable), so no false source promotion was attempted. The historical sanctioned Japanese dual-original relocation reference is separate and must not be relaxed here.

Compiler attempt classification: all successful 34 report `NO_NEW_COMPILER_FINDING` after original IDO codegen. Failed exploratory variants do not establish a new compiler quirk; first differing instruction offsets and bounded variants are preserved in `attempts/` and should be classified `NO_NEW_COMPILER_FINDING` unless a verified quirk was specifically tested. The full live compiler ledger was consulted at task preflight; the local precheck is source-only guidance, not a substitute for the current ledger in future sessions.

**Canonical baseline remains USA 2,164 C / 5,199 ASM; Japan 2,398 C / 4,978 ASM.**

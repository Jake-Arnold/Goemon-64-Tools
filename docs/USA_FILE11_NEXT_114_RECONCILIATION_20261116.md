# USA file_11: 306 baseline, 114 deduplicated research candidates, 307 native trial

Date: 2026-11-16. This record is not an automatic production promotion.

The canonical USA baseline is **306 matching C** (16,292 bytes), with 143 `file_11` functions.
Comparing the PR #23 research pools by original ROM offset against the published
143-function source fixture yields **207 discovered** additional candidate offsets,
of which **93 are already promoted**, leaving **114 disjoint**. PR #24 additionally
contains four independent offsets outside the PR #23 pool; range-only overlaps in its
other functions are not independent source-identity proofs. The hypothetical further
USA target would be 306 + 114 + 4 = **424**, requiring a combined native G2, all
relocations and original ELF inventory. Japan's independently verified 24 C functions
belong to a separate region and cannot be added to the USA count.

## First opt-in experiment: original 52-byte actor state reset

`func_801E3008_59EF18` occupies exactly the pre-existing 52-byte ASM chunk at
ROM range `[0x59EF18,0x59EF4C)`; the original VMA is `0x801E3008`.
The previously independent Wave 3 original-address C source has no external
bindings. Original IDO 5.3 compiled the C to 52 matching instruction bytes,
followed by 12 **zero** bytes of compiler padding; ELF object trimming changes
only the `.text` extent. Original code SHA-256:
`01a2ee6edebc172353056fea6431c94c82500d681115481434ececce2f575cc8`.
The trimmed ELF object SHA-256 is
`89980da48f2448a3af0a06fd6346dd2c87c5def09266cf53055d245a91496e1b`.
The original 143-C fixture and canonical 306-C manifest are preserved unchanged.

The isolated 307-C candidate links a byte-identical 33,554,432-byte USA ROM
(`6ea0ed71032ce08fc2745f412d84936382197494`), reproduces all **307/307 C**
functions (16,344 bytes), preserves all **8,825** `file_11` relocations,
retains the complete original `file_13` section and all verified Impact stages,
and passes `decomp.inventory` with **7,376** original function identities,
**7,056** ASM entries and **zero** extra positive FUNC aliases.

The initial verifier command reached the asset-link phase but exceeded the
bounded execution session. Its candidate build was resumed via `make` and
completed. The exact existing verifier post-build comparisons and overlay
checks were then executed directly and the inventory was run with the standard
CLI. This does **not** constitute an uninterrupted standard `decomp.verify`
CLI report, so this work is review-only and **does not raise the canonical 306**.

### Follow-up gates

- Re-run the opt-in 307 candidate through the standard full verifier (with sufficient
  build time or a fail-closed resumable CLI checkpoint) and create its standard report.
- Local CI passed on the isolated opt-in source (222 decomp, 160 verifier/ledger tests, task evidence audit, and GCC ASan/UBSan host regression). Preserve historical 306/303 G2 proofs.
- Review and formally promote the 307 result only after all stages pass together.
- Expand the multi-island adapter to the additional 114 candidates after prioritizing
  contiguous no-gap units; retain ASM for any unresolved identity or relocation.

No ROM, generated assembly, compiled objects, savestates or game assets are committed.

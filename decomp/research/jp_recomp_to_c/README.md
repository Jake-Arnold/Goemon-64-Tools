# New isolated JP ↔ USA exact C functions — 2026-11-16

These twenty-three reconstruction sources are **research-only** original-ID0 matching-C proofs. Each has an independent exact code match in USA and Japanese decompressed retail ROMs; individual linked overlay relocations/full-ROM G2 have not been retested.

**Count:** 23 exact functions, 964 bytes per region. Twenty-two new USA candidates, 912 bytes; `func_800166AC_172AC` is already formally promoted, and must never be added a second time.

Source SHA-256 and original regional address pairs are in the complete 52-function `manifest.json` distributed in the local reproducible source bundle, alongside `verify_candidates.py`, `scan_cross_region_exact.py`, 303-code-lead discovery report and seven unit tests.

Original verified expanded ROM SHA-1: USA `6ea0ed71032ce08fc2745f412d84936382197494`, JP `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Pinned upstream IDO 5.3, `-O2 -mips2 -G 0 -non_shared`. Functions may include object alignment bytes **outside** the named symbol extent; only exact original function bytes count.

Do not treat these paths as production `decomp/src`, alter canonical `decomp/manifest.json`, or claim a full-ROM build until the fail-closed production G2/inventory/relocation acceptance succeeds.

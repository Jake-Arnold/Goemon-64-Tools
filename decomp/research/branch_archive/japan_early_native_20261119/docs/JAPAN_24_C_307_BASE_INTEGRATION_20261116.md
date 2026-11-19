# Japanese 24-C draft integration onto canonical USA 307

Date: 2026-11-16. PR #26 is reconciled with USA production commit
`cd1d650993b33b3910733abf7f5b058c8851dafb`.
The integration imports 122 previously absent Japan-region source, config,
tests, proof and documentation Git blobs from the older Japanese consolidation
branch. It retains the USA 307 manifest, verifier and native proof unchanged.

The pinned Japanese `decomp/regions/japan_0.json` manifest independently
describes 20 C translation units, 24 distinct functions / 1,604 bytes,
with no overlapping original ROM ranges. Historical Japanese native evidence
reports exact 32 MiB expanded ROM SHA-1
`6f8745fecc3a5e7d4918c7a73353eb0726116ded`
and exact 16 MiB retail ROM SHA-1
`9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`,
7,376 ELF function identities, 7,352 remaining ASM and 55 approved
C relocations.

**Not yet established in the combined checkout:** execution of the unchanged
`decomp/build_japan_twentyfour_c.sh` and
`decomp/japan_twentyfour_verify.py` against a fresh pinned Japanese native
build; full integrated ROM-free `decomp.local_ci`; repeat USA 307 native G2.
Those remain mandatory gates before an official Japanese production promotion.
Japanese C functions must not be added to the USA 307-function count.

No ROM, original generated assembly, object, ELF or compiler binary is part
of this integration.

## Additional overlays and symbol research from PRs #7–8

Eight further previously absent Japan/USA research-source, test and document
files are imported by original Git blob from Japanese symbol-reconciliation
head `a2f57bacbe67230af82b7767c1140878c422c8db`. They cover 69-overlay direct-JAL scanning, audio-patch
audit and reconciled original-symbol function extents. Their tests are
synthetic ROM-free tests; their research claims do **not** change Japanese
24-C native production acceptance or the USA 307 canonical count.

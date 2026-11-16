# Decomp consolidation checkpoint — 16 November 2026

## Intent

Stage the Japanese native matching-C pipeline beside the current verified USA baseline.
Do **not** merge research branches wholesale, close/freeze them, or change the canonical USA
manifest and proof. This is an integration snapshot; originating branches remain independent.

## Sources pinned

- Target branch: `chatgptweb/decomp` at `3aae4e55855697229622acc9c528e761e42602c1`.
- Japanese source: `chatgptweb/japanese-decomp-port` at `ed4c0e3ad2a96d6c2e033da0351ed43f58b9b203`.
- Source selection: 121 **new**, Japanese decomp/proof/documentation/test files copied by their original Git blob identities; no modified USA or shared toolkit files copied.
- No original ROMs, generated assembly, linked objects, assets or savestates imported.

## Verification claims (independent; not additive across regions)

- USA canonical production: **210 matching-C functions / 13,336 bytes**, full 32 MiB USA image and 8,825 file_11 relocation identities matching; authoritative `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json` retained bit-for-bit.
- Japanese source branch: **24 matching-C functions / 1,604 bytes / 20 units**. Its recorded 32 MiB expanded hash is `6f8745fecc3a5e7d4918c7a73353eb0726116ded`; 16 MiB normalized retail hash is `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`. Source-branch records report zero differing ROM bytes, 7,376 positive ELF function entries, and no unexplained unmarked functions.
- **Integration status: STAGED, NOT FRESHLY VERIFIED.** Neither a new combined-branch USA G2 run nor a new Japanese 24-C build has been executed after this snapshot. Existing Japanese proof remains source-branch evidence; do not label this consolidation branch as fully acceptance-tested.

## Next acceptance gates

1. Validate all imported Python module imports and ROM-free tests against the current `chatgptweb/decomp` code.
2. Rebuild/verify latest USA 210-C 32 MiB ROM against its reference hash; verify preserved relocations and inventory.
3. Rebuild/verify Japan 24-C 32 MiB and recompressed 16 MiB images, original ELF extents and relocations, and region inventory using the pinned toolchain.
4. Correct integration-specific failures in this branch only; never weaken the verification checks.
5. Advance the 54 unpromoted USA file_11 candidates from PR #24, then deduplicate and promote groups from PR #23 (199 independent native candidates as of this checkpoint) using original-USA ROM offset and full central G2 gates.
6. Review older Impact and VM research branches for remaining unpromoted functions, avoiding cherry-picked old manifests or stale result files.

## Concurrency policy

The source branches may continue committing. This checkpoint never force-updates them.
On future passes compare their current heads to this recorded source SHA; reconcile by
region, ROM offset, original symbol, source content and proof scope, rather than blindly
adding function counts. Never merge a research-only proof into the official function totals.

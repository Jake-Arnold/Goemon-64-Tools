# USA wide109: 106 deduplicated original-address matching C in canonical 1225-C stage

Date: 18 November 2026. `PASSED_G2_LOCAL` / **remote publication pending**.

The source branch `chatgptweb/usa-wide-109-native-research-20261118` documented 109 exact C functions / 1,228 bytes. Three original-ROM offsets in that research set are already accepted in the 1119-C production tree: `0x5D42C8`, `0x5D57D8`, `0x5D59AC` (28 bytes). This source package stages exactly the other 106 / 1200 bytes, preserving prior ownership.

`promotion_manifest.json` lists all original-ROM offsets, VMAs, exact extents, original ROM instruction SHA-256s, and source SHA-256s. The 68 `sources/*.c` are human-readable original IDO 5.3 sources, not ROM, binary objects, extracted game ASM, or assets.

`decomp.overlay_wide109` authenticates full 32 MiB original SHA-1, source hashes, ROM instruction anchors and ASM ownership before replacing the original assembly at its original positions. The stage preserves original layout, symbol extents, ASM and accepted relocation multisets; no compiler-produced instruction bytes are patched. It executes after all 1119 existing C stages.

Verified on the owner-supplied USA ROM and pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`:

- Native original IDO / full standard `python3 -m decomp.verify`: PASS 1225/1225, 52,028 bytes, 32 MiB ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- `python3 -m decomp.inventory`: PASS; 7,376 exact original ELF FUNC identities and 6,138 ASM entries, zero extra positive aliases.
- `python3 -m decomp.local_ci` **full**: PASS with 256 decomp tests, 245 verifier/ledger tests, evidence validation and GCC ASan/UBSan actual-source regressions for the 68 added C units (`test_actual109.c`).
- No emulator gameplay verification; Japanese decomp unchanged at 39 C / 2,092 bytes.

Authoritative native proof and source catalog: `decomp/results/usa_wide109_1225_promotion_20261118.json`, `decomp/results/combined.json` and `decomp/results/inventory.json`. Historical reports saved as `combined_1119_before_wide109_20261118.json` and `inventory_1119_before_wide109_20261118.json`.

**GitHub:** This package has not been pushed to `chatgptweb/decomp`. The native host cannot access GitHub to push and the connector cannot ingest the tested local source tree. Retain the research PR #74 as draft until the exact source, native proof and inventory are published and re-fetched.

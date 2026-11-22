# USA Mini Ebisumaru + Cross48: 49 original-address C functions (22 November 2026)

**Status:** `PASSED_G2_LOCAL`, with original USA Rev.00. Source branch base: `c738164ff1fed1c1258faf74f45cada8189f8f5e`. No `main` change.

The Mini Ebisumaru movement callback `func_801E20A0_59DFB0` (ROM `0x59DFB0`, VMA `0x801E20A0`, 224 original bytes, 12 relocations) and 48 Japan-to-USA donor functions (3,028 bytes, 130 original relocations) are now native exact at their USA addresses and combined exact in a fresh 32 MiB ROM. No duplicate accepted functions, including the already-accepted 100-byte `func_801E7F50_5A3E60`, are counted.

## Complete proof

The complete USA ROM remains 33,554,432 bytes and SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. ELF positive FUNC identities: 7,376; all original semantic relocations: 82,103. Strict inventory: 2,014 matching C, 5,349 ASM; C instruction bytes: 87,900. Standalone 48/48 native replay, G2 adapter's all-symbol/relocation audits, 5 new ROM-free regression tests, actual-source GCC ASan/UBSan and entire `decomp.local_ci` have passed.

## Requirements

- Full `chatgptweb/decomp` checkout at this publication (not only this source bundle).
- Pinned `mnsg` git checkout `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` and authenticated USA retail ROM; no ROM included in Git or this artifact.
- Original IDO 5.3 and N64 GNU binutils, plus pinned Python 3.12 Splat dependencies and portable runtime.
- Fresh canonical 1,956 stage, accepted historical `glitch`, `scheduler4`, `scheduler5`, `scheduler6` stages, then Mini1 and Cross48. Verify after each stage.

## Reproduce the final stages

From the toolkit repo root, where `$CHECKOUT` is the privately rebuilt pinned USA upstream containing the verified USA1965 stage and `$BASELINE` is the original upstream USA ELF+ROM checkout, run:

```bash
python3 -m decomp.mini_ebisumaru_1_g2_promotion stage --checkout "$CHECKOUT" --prior "$MINI_PRIOR"
python3 -m decomp.mini_ebisumaru_1_g2_promotion build --checkout "$CHECKOUT" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.mini_ebisumaru_1_g2_promotion verify --checkout "$CHECKOUT" --prior "$MINI_PRIOR" --original "$BASELINE"
python3 -m decomp.usa_crossregion48_g2_promotion stage --checkout "$CHECKOUT" --prior "$CROSS_PRIOR"
python3 -m decomp.usa_crossregion48_g2_promotion build --checkout "$CHECKOUT" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.usa_crossregion48_g2_promotion verify --checkout "$CHECKOUT" --prior "$CROSS_PRIOR" --original "$BASELINE"
python3 -m unittest decomp.test_usa49_followup_g2 -v
python3 -m decomp.local_ci
```

To reproduce the prerequisite historical stages, refer to `decomp/CONTINUE.md` and their respective promotion modules and reports. The scripts refuse stale source hashes, duplicate identities, non-original ROMs or an absent predecessor proof.

## Evidence and limitations

- `decomp/results/usa_mini_1966_g2_20261122.json`: complete Mini1 G2 and strict 1966-function inventory.
- `decomp/results/usa_cross48_2014_g2_20261122.json`: complete 49-function G2 and strict 2014-function inventory.
- `decomp/research/mini_ebisumaru_1_g2_20261122/manifest.json`: original Mini1 offsets, SHA-256 and relocations.
- `decomp/research/usa_crossregion48_g2_20261122/manifest.json`: original Cross48 offsets, SHA-256 and relocations.
- Existing `decomp/results/combined.json` and `inventory.json` are historical pre-scheduler canonical snapshots; the full staged inventory is included in the new G2 reports.
- Earlier 51-source cross-region research archive is unavailable in the supplied full repo ZIP. Metadata-only candidates were not falsely promoted.
- Verification is exact ROM/ELF/relocation, not a live emulator gameplay claim. No ROM/ASM bytes, tools or proprietary assets are distributed.

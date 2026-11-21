# USA scheduler wrapper four — original-address native C

Region: USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; decompressed SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Original upstream IDO 5.3, pinned `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

Four native IDO 5.3 C implementations at original USA offsets `0x359D8`, `0x35A08`, `0x35A38`, and `0x35A68`, 48 bytes each, previously demonstrated in a clean-upstream original-ROM proof. These four are novel relative to the 1,958 accepted C functions after the published 2026-11-21 Start-path stage; the previously researched traversal helper and callback setters were **already accepted** and were not counted again.

The four wrappers call the original task-creation/insertion helpers and then `func_80034D24_35924`, which initializes/activates the returned task pointer. The underlying insertion routines remain ASM; matching their wrappers does not prove their own bodies. Type/signature confirmation is limited to the observed call/return ABI.

## Verified local integration, 2026-11-21

1. Unmodified `python3 -m decomp.verify` on the advanced branch: **1956 accepted C, 32 MiB byte identical**. The supplied pinned offline Python and `uv` shim were used because package downloads are inaccessible; all original IDO and linker inputs were retained.
2. The separately published `decomp.glitch_g2_promotion` rebuilt and verified two USA Start-path functions against the correct 1956-C accepted ELF, bringing the accepted predecessor to **1958 C / 84,292 bytes**.
3. `decomp.scheduler4_g2_promotion stage`, `build`, `verify` ran on that predecessor: **1962 C / 84,484 bytes / 5,401 original ASM**, complete 33,554,432-byte USA original ROM equal, 7,376 exact positive ELF FUNC identities and **82,103 exact semantic relocation records**.
4. The same strict `decomp.inventory.summarize_inventory` algorithm validated all 1,956 canonical manifest C claims plus the two accepted Start-path claims plus four new wrapper claims. The default CLI inventory still reads the canonical 1956 stage manifest and therefore must not be presented as a 1962-stage CLI pass. Results are stored in `decomp/results/usa_scheduler4_1962_g2_20261121.json`.
5. Full `python3 -m decomp.local_ci` PASSED on the updated adapter/test suite: 319 decomp Python tests, 349 verifier/ledger tests and configured sanitizer/ledger checks. Original host C sanitizer test separately passed **1,024 wrapper call chains** and both callback setter checks. Emulator gameplay was not run.

## Reproduction

Using original pinned upstream, supplied toolchain and files, first run canonical `decomp.verify`, then accepted `decomp.glitch_g2_promotion stage/build/verify`, passing the accepted 1956 ELF as the glitch verification baseline. On the resulting accepted USA1958 candidate:

```sh
python3 -m decomp.scheduler4_g2_promotion stage --checkout "$CANDIDATE" --prior "$WORK/accepted1958-elf"
python3 -m decomp.scheduler4_g2_promotion build --checkout "$CANDIDATE" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.scheduler4_g2_promotion verify --checkout "$CANDIDATE" --prior "$WORK/accepted1958-elf" --original "$ORIGINAL_USA_BASELINE_CHECKOUT"
python3 -m unittest decomp.test_scheduler4_g2_promotion
python3 -m decomp.local_ci
```

`--prior` must be a path that does not exist before staging; the stage saves the exact prior ELF/ROM. The complete original ELF/ROM comparison is fail-closed. No ROM, executable, generated ASM or toolchain bytes are distributed by this research directory.

## Outstanding

The 120-byte dispatcher `func_80002040_2C40`, 344-byte task executor `func_80034734_35334`, and 52-/56-byte insertion wrappers are **not** accepted based on this work. Their C translations remain research-only until original instruction encoding and relocation proofs succeed.
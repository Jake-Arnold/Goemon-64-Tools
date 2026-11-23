# Japan cross-region30 native original-ROM promotion — 23 November 2026

**PUBLISHED_REMOTE_VERIFIED:** actual original-region native G2 PASS; GitHub reviewed PR #196 merged to `stable/decomp` as commit `360a9f6c3e381b0a9f5c7a939f36c16a338516a0` and remotely re-read at the exact 2,428-C count. The original native G2 source proof below remains unchanged. 

## Canonical baseline

- GitHub `stable/decomp@838e9f87c3a860973e9d168b58fcf88bd456bfb4` authenticated using successful SHA-pinned GitHub Actions source-archive workflow COMMIT.txt and SHA256SUMS.
- Pinned upstream `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` clean Japanese checkout. Authenticated original Japan retail and expanded ROM hashes, native SGI IDO 5.3 original compiler SHA-256.
- Original Japan **2,398 matching C / 128,988 bytes / 4,978 ASM**, full 32MiB/16MiB ROM, ELF and reloc verified before new staging; preexisting USA **2,164 C / 5,199 ASM** unchanged.

## Native accepted original source delta

- **30** original Japanese ASM-owned functions moved to independently original-ROM-exact native C at their exact original source-owner linker position, **1,280 original instruction bytes** across **26 original ASM source owners**, retaining every other original assembly span. New Japanese **2,428 matching C / 130,268 original bytes / 4,948 remaining ASM**. See `decomp/regions/japan_0_crossregion30_2428.json` for 30 original names, ROM offsets, original sha256, actual C source names and source SHA.
- **3 original 12-byte MMIO/OS stub functions remain ASM**: `osAiGetLength`, `__osSpGetStatus`, `__osSpSetStatus`. The isolated compiler output matches all three instruction bodies, but drops original symbolic ABS relocation pairs. Switching to correct extern references creates extra `addiu` instruction, so strict relocation and full-ROM proof fail. Deliberately excluded, never counted as accepted C.
- Four verified C symbol-reference variants compile the original native instructions and preserve the true canonical relocation *names*, with 4/4 newly source-mutated native negative controls rejected. Prior original donor research native replay and controls 34/34 PASS.
- Existing IDO 5.3 ELF-symbol provenance quirk reproduced for two uses of `D_CF8F0` and one of `D_CF8F8`: original canonical globals have NOTYPE, original C native objects mark undefined symbols OBJECT. Strictly original-name/ELF32/ABI guarded **single st_info byte** changes on three *compiler-generated objects* restore the original symbol metadata. Their compiled MIPS instruction bytes, all original relocations and all ROM bytes are unchanged; no byte-patching of the game ROM and no generalized quirk adapter. Original 26,393 stable global name/address/type identities exact.

## Independent combined original-ROM G2 proof actually executed

| Gate | Measured result |
|---|---|
| USA ROM untouched | USA canonical C 2,164 unchanged; USA original native G2 not rerun for this Japan-only promotion |
| Original Japan expanded ROM | **33,554,432/33,554,432 byte-identical**, SHA1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |
| Original Japan retail recompression | **16,777,216/16,777,216 byte-identical**, SHA1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Original positive ELF symbols (name, VMA, size, type) | **7,376/7,376** exact |
| Original stable global symbol identities | **26,393/26,393** name/address/type exact |
| Original Japan canonical semantic relocations | **80,745/80,745**, SHA256 `43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0` |
| C and ASM ownership | 2,398 predecessor C preserved + **30 C** / original 4,948 ASM remaining; all exact original function extents |
| Region-specific integrity | PASS, source SHA, no duplicate promotion and inventory pinned |
| Full *unmodified* `python3 -m decomp.local_ci` | **PASS exit 0**; 465 decomp Python tests (3 skipped), 350 verifier tests, GCC/Clang sanitizer suites and original USA strict-promotion checks; 2026-11-23 |
| Emulator gameplay | NOT RUN |
| GitHub remote publication | **PUBLISHED_REMOTE_VERIFIED** as `360a9f6c3e381b0a9f5c7a939f36c16a338516a0`, PR #196 |

## Replay from authenticated owned inputs

```sh
# Starting from exact canonical original JP2398 staged checkout in a clean workspace:
python3 -m decomp.japan_crossregion30_promotion stage --checkout /private/jp2398
python3 -m decomp.japan_crossregion30_promotion build --checkout /private/jp2398 --deps /private/dependencies --runtime /private/runtime-additions
python3 -m decomp.japan_crossregion30_promotion verify --checkout /private/jp2398 --base /private/pristine-jp2398-baseline
python3 -m decomp.japan_crossregion30_integrity --validate
python3 -m decomp.japan_short28_integrity --validate
python3 -m decomp.promotion_integrity --validate
python3 -m decomp.local_ci
```

The `--base` must be a **separately snapshotted** pre-staging canonical JP2398 original 32MiB ROM and original ELF, never the same mutated checkout. Existing JP2398 reproduction uses the pinned historical Japanese stage chain from `decomp/CONTINUE.md`. The stage and verify are fail-closed on original ROM and ELF/reloc identities. User-owned ROMs, native compiler, toolchain, original ASM and build objects are never committed or uploaded.

Compiler classifications: 30 positive native function compile attempts generally `NO_NEW_COMPILER_FINDING`; three absolute global metadata type corrections **EXISTING_QUIRK_REPRODUCED**. Failure of the three MMIO stubs retains ASM; no invented new compiler quirk. See `decomp/COMPILER_QUIRKS.md`, and prior research attempts and standalone negatives in the source-only research tree.

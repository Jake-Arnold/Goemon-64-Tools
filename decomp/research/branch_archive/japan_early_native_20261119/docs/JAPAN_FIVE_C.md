# Japanese five-function matching-C promotion

**Date:** 2026-11-15  
**Status:** native IDO 5.3 matching-C, full 32 MiB source-linked image, and 16 MiB retail recompression **PASS**. Separate Japanese N64 milestone; not native PC execution.

## Newly promoted function

| Property | Verified value |
| --- | --- |
| Function | `func_80012160_12D60` |
| Original Japan ROM offset | `0x12D60` |
| Original guest VMA | `0x80012160` |
| Code size | **32 bytes** |
| Behaviour | Store mode byte and three floating-point parameters in object fields |
| Source | `decomp/japan_matching/jp_motion_12D60.c` |
| Native compiler | pinned IDO 5.3, `-O2 -mips2` |
| Compiled `.text` SHA-256 | `7abe3e7fff0963bfcb4e6b333fa738d03ddb1d3147b3ca02f8573f4f34fbdf55` |
| Compiled text relocations | **0** |
| Link map | `build/japan_0/src/jp_motion_12D60.c.o` at `0x80012160`, length `0x20` |

The native IDO-generated text is **32/32 bytes identical** to the original Japanese instructions. Splat config `splat_five_c.local.yaml` retains the prior C units and inserts this unit between assembly sections `main_122F0` and `main_12D80`, leaving the pinned upstream Splat configuration untouched.

## Updated Japanese decompilation count

| Metric | Previous | Current |
| --- | ---: | ---: |
| Verified matching-C functions | 4 | **5** |
| Matching-C original function bytes | 136 | **168** |
| C translation units | 2 | **3** |
| Positive-sized Japanese ELF function entries | 7,376 | **7,376** |
| Remaining explicit assembly-marked entries | 7,372 | **7,371** |
| Unreviewed unmarked entries | 0 | **0** |

The five-C ELF inventory is saved separately at `decomp/results/japan_0_elf_inventory_five_c_2026-11-15.json`. It includes 73 executable sections and the updated function-symbol fingerprint `4b53a2d0dc5e21d3e2ac42c2a7772d4ebf87d8dbe146494e5ce040a7f525d9db`. As before, ELF entries include IPL3/entry markers and must not be mistaken for a complete collection of gameplay functions.

## Exact full-image gate

- Pinned `mnsg` source: `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`
- 32 MiB linked Japanese ROM: **PASS**, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, **0 differences**
- 16 MiB recompressed Japanese retail ROM: **PASS**, SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, **0 differences**
- Independent region verifier: **PASS** for all 5 functions / 168 bytes and all 3 compiled C objects; exact source bytes, section/code hashes, function extents, linker addresses and zero unexpected text relocations
- ROM-free regressions: **32/32 PASS**; Bash runner syntax check PASS
- The one-command five-C runner's complete Splat phase passed, but its bulk assembly phase exceeded the execution window. Resuming the generated native make completed with the exact linked ROM; subsequent recompression and region verification both passed. No assertion of an uninterrupted one-command run is made.

## Reproduction with private offline files

Keep the source checkout, game ROM, output binaries, assembly and toolchain archives out of Git.

```bash
python3 -m unittest \
  decomp.test_japan_asm_baseline \
  decomp.test_japan_first_c \
  decomp.test_japan_four_c \
  decomp.test_japan_five_c \
  decomp.test_region_verify \
  decomp.test_japan_five_region \
  decomp.test_japan_inventory -q

GOEMON_JOBS=12 bash decomp/build_japan_five_c.sh \
  /path/to/pinned-mnsg-japan \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
```

The script uses an original Japanese rev-0 ROM only inside the private pinned checkout; it checks SHA-1 before running Splat and writes the detailed proof to the ignored build directory.

**Backward compatibility:** `decomp/regions/japan_0_four_c.json` preserves the old manifest. `decomp/regions/japan_0.json` now describes the five-C stage. The region verifier supports both reviewed stage layouts, while USA remains delegated unchanged to its original verifier.

## Still unverified

A fresh USA original-address G2 build, Japanese emulator gameplay, and Japanese native Goemon64Recomp PC execution have **not** been run. A further C function is not claimed without original-IDO/linker/full-ROM proof.

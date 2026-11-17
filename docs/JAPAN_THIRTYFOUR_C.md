# Japanese Goemon 64 rev-0 — 34 native matching-C functions

**Verified 16 November 2026.** From a verified 31-function / 1,784-byte baseline, three adjacent audio/state routines were compiled from C with original IDO 5.3 and integrated into the pinned Japanese GNU MIPS build. Two independent clean upstream source checkouts reproduced the original **32 MiB expanded and 16 MiB retail** cartridges byte-for-byte.

| Check | Result |
|---|---|
| Matching-C functions | **34** (three newly promoted) |
| Original matching instruction bytes | **1,912** (+128) |
| C translation units | **30** |
| Expanded 32 MiB SHA-1 | `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, zero differences |
| Retail 16 MiB SHA-1 | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, zero differences |
| ELF positive-sized game functions | 7,376 (7,342 ASM-marked + 34 C) |
| ELF sections | 73 |
| Unreviewed unmarked symbols | 0 |
| Source, native machine code, relocations and linker map | PASS |
| ROM-free guardrail tests | 8/8 PASS |
| Independent pinned full native builds | 2 PASS |
| Japanese emulator gameplay / PC-native runtime | NOT RUN |

### Newly promoted functions
- `func_80038984_39584`: 40-byte audio wrapper with parameter 0xF0.
- `func_800389AC_395AC`: 40-byte audio wrapper with parameter 0xF1.
- `func_800389D4_395D4`: 48-byte state comparison and byte flag update.

Original code coordinates are in the Japanese ROM, not the USA. The first two wrappers each have one call relocation; the flag function has six HI16/LO16 data relocations. They match the original code at original guest addresses.

### Reproduction

Use the original, pinned `klorfmorf/mnsg` source at `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, the private Japanese rev-0 cartridge and supplied offline compiler/runtime archives:

```bash
bash decomp/build_japan_thirtyfour_c.sh /path/to/fresh-pinned-mnsg /path/to/goemon-dependencies /path/to/goemon-runtime-additions
python3 -m unittest decomp.test_japan_thirtyfour_c
```

The builder produces the Japanese Splat split, compiles C under original IDO 5.3, checks reviewed relocations, applies zero-only, relocation-safe ELF text alignment trims, and verifies whole-ROM equality. Additional reviewed ASM slices `main_38F50` (0x634 original bytes / 12 pad) and `main_39604` (0x15DC / 4 pad) are required. The project retains the older 31-function manifest for separate regression.

A self-contained, source-only tested build bundle is also attached in the conversation as `goemon-japan-thirtyfour-c-verified.zip` (SHA-256 `7d0c80741ee7fdb5c3c780601c536fcca9e8dde51363b3267a9e6b1585fdcf96`). Its seven earlier C sources reside in `decomp/japan_followup` whereas the branch copies them under `decomp/japan_matching` with identical source hashes.

### Next adjacent candidates

The 0x39408/0x39438/0x39468 wrappers currently differ from IDO's original register/prologue ordering, despite correct broad semantics. The 0x38C34/0x38DF8 candidates fail code-size matching. Larger 308-, 324- and 468-byte neighbouring warp routines remain owned by assembly. **None is counted**. Emulator gameplay and native PC recompilation were not tested.

No private ROM, original assembly, generated game objects, compiler binaries or game assets are committed.

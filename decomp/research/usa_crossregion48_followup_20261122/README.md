# USA rev-0 — 48 additional native-exact original C implementations (22 November 2026)

**Status: `PASSED_ISOLATED_NATIVE / RESEARCH_ONLY`. Not official USA C promotion.**

## Cross-region result and deduplication

This batch follows the earlier 51-USA-function research (`goemon_usa_51_native_crosswalk_research_20261122.zip`), which established 27 novel USA functions directly from the Japanese JP55 promotion and another 24 from separate Japanese donors. **None of those 51 functions is counted here.**

A further automated comparison of previously accepted Japanese C donors against authenticated original-USA MIPS disassembly generated 50 byte-identical USA candidates. Two were excluded because the candidate C object introduced six HI16/LO16 symbol pairs that were **not present as relocation annotations** in the corresponding original-USA disassembly. These two remain unresolved rather than being counted.

**48 distinct additional USA-original identities / 3,028 code bytes / 130 original symbol relocations** independently passed native compilation using SGI IDO 5.3 `-G 0 -non_shared -O2 -mips2`, symbol-aware linking at each actual USA guest VMA and byte-for-byte comparison of complete function extents against the USA 32 MiB original ROM. Every one of their 130 object relocations was compared by **offset, MIPS relocation type and target symbol** against the corresponding original USA disassembly. No unspecified instruction mismatches or code-byte substitutions were tolerated; trailing toolchain alignment bytes must be zero.

Combined with the **51 earlier unpromoted USA candidates / 3,864 bytes / 81 relocations**, there are now **99 unique isolated-USA exact C candidates / 6,892 original bytes / 211 original object relocations** pending integrated USA acceptance. The canonical USA baseline is still **1,965 accepted C, 84,648 original C instruction bytes, 5,398 original ASM functions**. These research-only findings do **not** modify that inventory.

Japanese C donor names and batches, USA targets and addresses, independent original code SHA-256 values, candidate source SHA-256 values and explicit original relocation records are all in `manifest.json`. Function symbols/addresses are region-specific: this is not a generic USA/Japan address arithmetic crosswalk.

## Original input and verification

- **USA retail ROM, 16 MiB SHA-1:** `df8083a54296b8c151917c5333e1c85f014a2a66`
- **USA expanded ROM, 32 MiB SHA-1:** `6ea0ed71032ce08fc2745f412d84936382197494`
- **USA unchanged full upstream ROM rebuild:** byte-identical to expanded original, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`
- **Native isolated proof:** `isolated_native_proof.json`, made by actual `verify_native.py` execution on the original 32 MiB ROM, all **48/48 functions, 3,028/3,028 bytes, 130/130 symbolic records**.
- **Host sanitizer proof:** `host_semantics_proof.json`, produced by executing `tests/test_host.py` with GCC ASan/UBSan: **48/48 authentic source C files compile**, **45/48 execute actual original-source semantic fixtures**, three architecture-dependent cases only compile. The three compile-only cases deliberately are *not* reported as executed tests.
- **Excluded two relocation conflicts:** `excluded_relocation_conflicts.json` captures the disputed source-to-original relocation differences, without containing any original ROM code bytes.

### Replay

Install pinned original SGI IDO 5.3, MIPS binutils and their shared libraries using `GOEMON_BUILD_ENVIRONMENT.md`. Supply your own authenticated 32 MiB original expanded USA ROM. From this archive's root run:

```bash
python3 verify_native.py \
  --rom /absolute/path/to/config/usa/baserom.decompressed.z64 \
  --cc /absolute/path/to/mnsg-japan/tools/ido-5.3/cc \
  --ld /absolute/path/to/mips-linux-gnu-ld \
  --objcopy /absolute/path/to/mips-linux-gnu-objcopy \
  --objdump /absolute/path/to/mips-linux-gnu-objdump \
  --report /tmp/usa48-native-replay.json

python3 tests/test_host.py --report /tmp/usa48-host-replay.json
```

Native verifier requires the exact original ROM SHA-1, per-function C and original code SHA-256 hashes, IDO instruction bytes including delay slots and extents, every original HI16/LO16/MIPS_26 symbolic relocation and linked symbol original VMA. Host tests compile the *actual reconstructed C*, not substitute implementations; callback stubs are provided only for host testing where the original code's external functions are not linked.

## Formal promotion status

**Full USA integrated G2 not run:** no combined 33,554,432-byte USA ROM rebuild with the 48 new sources inserted alongside 1,965 existing accepted USA C functions; no full original 7,376 ELF-function identity comparison, 82,103 semantic relocation multiset comparison, strict integrated inventory, post-integration full CI, or production ownership migration. Therefore the official USA accepted C function count remains unchanged and all 48 assembly owners must be preserved. Independent native matching demonstrates machine-code compatibility, not identical game-data/asset semantics across regional overlays.

**Source-only distribution.** The archive contains no original ROM bytes, extracted original assembly, compiled MIPS objects, proprietary toolchain, disassembly dumps, credentials, or game assets.

# Japanese revision-0: sixth exact matching-C function

**Date:** 2026-11-15. **Status:** native C code, source-linked 32 MiB N64 ROM and recompressed 16 MiB Japanese retail ROM **all exact**.

## New original-address function

| Evidence | Value |
| --- | --- |
| Function | `func_80012F70_13B70` |
| Original JP ROM offset | `0x13B70` |
| Original JP VMA | `0x80012F70` |
| Function length | **32 bytes** |
| Native C source | `decomp/japan_matching/jp_camera_13B70.c` |
| C behaviour | Store three floating point parameters in structure fields at offsets 0x60, 0x6C, 0x78 |
| Compiler | pinned original native IDO 5.3, `-O2 -mips2` |
| Text SHA-256 | `5ac8c04bfd5044d48649fa29217ef11385d853508fcff5445d9376620cec3ca5` |
| Relocations | **0** in compiled object `.text` |
| Linker | `.text 0x80012F70 0x20 build/japan_0/src/jp_camera_13B70.c.o` |

The name `jp_camera` follows the Splat module area, not a verified gameplay-level explanation. The observed operation is simply three float stores. A preliminary alternative, `__osPopThread`, did not generate exact bytes and was **not** promoted.

## Independent exact ROM proofs

From pinned `klorfmorf/mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, staged a separate Japanese Splat config `config/japan_0/splat_six_c.local.yaml`. It preserves the existing five matching-C functions, splits the original assembly region at `0x13B70` and `0x13B90`, links a real fourth C translation unit, and leaves all remaining original code as assembly.

- Native Splat extraction: **PASS**.
- Repaired the same 22 unique cross-object labels and two BSS label aliases: **PASS**.
- Whole decompressed 32 MiB Japanese N64 link: SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, **0 differing bytes**.
- Original upstream Rommy 16 MiB recompression: SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, **0 differing bytes**.
- Separate strict region verifier: **MATCH**, all six native C functions, 200 original function bytes, four original-address translation units, no unreviewed `.text` relocations.
- Actual linked ELF inventory: **7,376 positive-sized entries**, **7,370** assembly marked, **6** reviewed C; **0** unreviewed unmarked entries, 73 sections. As before, entries include ELF boot/IPL3 placeholders rather than only gameplay functions.
- Region-specific regression suite: **37/37 PASS**.
- Build runner Bash syntax: **PASS**. The full build was run through its individual native commands; the newly published one-command runner itself was not executed end-to-end as a single invocation.
- Fresh USA integrated matching-C G2, emulator gameplay and Japanese native PC runtime: **NOT RUN**.

## Files and reproduction

In `Goemon-64-Tools`, the following private inputs must exist: pinned `mnsg-japan` checkout, the original verified Japanese rev-0 cartridge in its config directory, and both already-supplied offline toolchain/runtime archives unpacked as directories.

```bash
python3 -m unittest discover -s decomp -p 'test_*.py' -q

GOEMON_JOBS=12 bash decomp/build_japan_six_c.sh \
  /path/to/mnsg-japan \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
```

The script preserves the original Japanese Splat file and USA verifier; it refuses wrong ROM and upstream source identities, stages only reviewed C, and never commits copyrighted ROMs or extracted assembly. The standalone runner writes local-only build outputs and a detailed strict region report.

The default Japanese manifest `decomp/regions/japan_0.json` now contains six verified functions, while reviewed four-C and five-C manifests remain as `japan_0_four_c.json` and `japan_0_five_c.json`. The region verifier recognizes all three staged Splat layouts. Its default USA path is unchanged.

The attached metadata-only proof is `decomp/results/japan_0_six_c_2026-11-15.json`, and the per-section inventory is `decomp/results/japan_0_elf_inventory_six_c_2026-11-15.json`.

**Next:** Choose the next 16/32/48-byte Japanese functional helper with clear source correspondence; repeat exact IDO object, linked ROM, retail ROM, source manifest and ELF inventory checks. Separately, a Japanese N64 emulator and full native PC recompilation toolchain remain required for gameplay testing.

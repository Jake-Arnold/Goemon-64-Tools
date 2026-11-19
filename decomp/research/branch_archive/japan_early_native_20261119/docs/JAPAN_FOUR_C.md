# Japanese four-function matching-C milestone (2026-11-15)

**Status:** Four Japanese IDO 5.3 matching-C functions verified in a complete 32 MiB N64 build and an exact 16 MiB recompressed retail ROM. The Japan and USA builds remain separately gated.

## Promoted functions

| Japanese function | Japanese ROM | VMA | Original code bytes | Effect |
| --- | --- | --- | ---: | --- |
| func_80037A20_38620 | 0x38620 | 0x80037A20 | 8 | Previously verified empty no-op |
| func_800161F0_16DF0 | 0x16DF0 | 0x800161F0 | 36 | Set a bit in a byte array |
| func_80016214_16E14 | 0x16E14 | 0x80016214 | 40 | Clear a bit in a byte array |
| func_8001623C_16E3C | 0x16E3C | 0x8001623C | 52 | Test a bit and return 0/1 |

The three new functions correspond to the semantics and exact C expressions already validated for the USA counterparts in decomp/bit_array.c. Japanese functions have their own original addresses. **Total: 4 Japanese matching-C functions, 136 original function bytes (up from 1 function / 8 bytes).**

## Original-address linked proof

- Pinned external source: klorfmorf/mnsg commit 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee.
- Original Japanese ROM: 16,777,216 bytes, SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b.
- Expected decompressed Japanese reference: 33,554,432 bytes, SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded.
- Native compiler: pinned IDO 5.3 with -O2 -mips2 and existing Makefile flags. New compiled jp_bit_array.c .text section is **128/128 bytes identical** to the source ROM at 0x16DF0..0x16E70. The three functions span that section continuously and have **0 .text relocations**.
- .text SHA-256 for the three functions: 585a234af53888f922034d8f0c4f7c9c157dc35c12d26b3d35b1a9ff7419cc70.
- Splat generates a real C translation unit at 0x16DF0; it remains linked alongside the prior matching-C unit at 0x38620 and the unconverted original Japanese assembly.
- **Complete linked 32 MiB ROM**: exact original SHA-1 6f8745fecc3a5e7d4918c7a73353eb0726116ded, 0 differing bytes.
- **Recompressed 16 MiB ROM**: exact original SHA-1 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b, 0 differing bytes.
- ROM-free regression tests: **10/10 PASS** (3 assembly-only, 3 first-C, 4 new four-C tests).
- Native emulator boot/gameplay: NOT RUN. Fresh USA original-address G2: NOT RUN. Japanese native Goemon64Recomp PC executable: NOT RUN.

## Reproduction

Use the private normalized Japanese ROM and the pinned mnsg checkout; do not commit any ROM, bin/asm output, object files or original extracted assets.

Run within the Goemon-64-Tools checkout, with the two dependency archive contents unpacked to separate directories:

~~~bash
python3 -m unittest \
    decomp.test_japan_asm_baseline \
    decomp.test_japan_first_c \
    decomp.test_japan_four_c -v

GOEMON_JOBS=8 bash decomp/build_japan_four_c.sh \
    /path/to/mnsg-japan \
    /path/to/goemon-dependencies \
    /path/to/goemon-runtime-additions
~~~

The runner validates hashes, prepares the Japanese Splat config from the original assembly baseline, keeps the previously verified C unit, inserts exactly one new C unit at 0x16DF0, runs native Splat, restores both verified C source files, fixes 22 known cross-object labels and two BSS name collisions, then builds, recompresses and proves all outputs. No changes to original config/japan_0/splat.yaml or the USA region.

The full pipeline was run manually and passed; an additional one-command runner attempt was interrupted by the execution limit during full reassembly, after Splat/source/link fixups had completed. Resuming the exact generated native Make build completed with a matching 32 MiB ROM, and the independent recompression+verification passed again. This interruption is **not** a game-code mismatch.

The private generated proof is written to build/japan_0/four-c-proof.json; the metadata-only publication record is decomp/results/japan_0_four_c_2026-11-15.json.

## Next

JPN-006 is still outstanding: a reusable opt-in region-aware version of decomp.verify and independently generated per-region matching inventory, preserving the original USA default. Next substantive work can extend the bit-array module into larger units, but every new C function must pass the same native original-address, relocation and whole-ROM checks.

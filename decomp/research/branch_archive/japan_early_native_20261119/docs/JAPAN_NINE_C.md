# Japanese nine-function matching C — 16 November 2026

**Native original-address Japanese build: PASS.** Five C translation units replace nine functions and 248 original function bytes, preserving the remaining Japanese assembly. Neither emulator gameplay nor native PC execution is claimed.

## Three new mode-setting helpers

| Original Japanese symbol | ROM offset | RAM address | Bytes | Mode |
| --- | --- | --- | ---: | ---: |
| func_80036CD0_378D0 | 0x378D0 | 0x80036CD0 | 16 | 2 |
| func_80036CE0_378E0 | 0x378E0 | 0x80036CE0 | 16 | 1 |
| func_80036CF0_378F0 | 0x378F0 | 0x80036CF0 | 16 | 3 |

The three functions write to g_system + 0x3ADD5. The native IDO 5.3 -O2 -mips2 object has 48 bytes of text (prelink SHA-256 952f9004206e8f3ab29fe84f8c8fcc536e5d237d742c76e4522234368f2c50c8). It has exactly six reviewed R_MIPS_HI16 / R_MIPS_LO16 relocations to g_system at offsets 0x04, 0x0C, 0x14, 0x1C, 0x24 and 0x2C. The original-address linked instruction bytes equal the original Japanese ROM for all three functions.

## Full-image acceptance

- Source: pinned klorfmorf/mnsg at 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee.
- Source-linked 32 MiB expanded Japanese ROM SHA-1: 6f8745fecc3a5e7d4918c7a73353eb0726116ded. Complete byte comparison: zero differences.
- Recompressed 16 MiB original Japanese retail ROM SHA-1: 9843ee979b5f6c80f5eda85df0baed9ae7c4e73b. Complete byte comparison: zero differences.
- ELF inventory: 7,376 positive-sized F entries over 73 executable sections; 7,367 explicitly assembly-marked, nine reviewed C functions and zero unreviewed unmarked.
- Full native linker map confirms five C objects at exact Japanese RAM addresses and original section sizes.
- Original USA code and hashes unchanged.

## Reproduction

Run in Goemon-64-Tools on x86-64 Linux with the two private dependency archives unpacked and canonical Japan rev-0 ROM staged in the exact pinned mnsg checkout:

    bash decomp/build_japan_nine_c.sh /path/to/mnsg-japan /path/to/goemon-dependencies /path/to/goemon-runtime-additions

The runner verifies ROM identity, stages a separate five-C-unit Splat config, restores all C sources, exports 22 cross-object labels, renames two BSS aliases, assembles/links, recompresses and runs the region-aware verifier. Preserve original game assets outside GitHub.

The individual native build and ROM/ELF verification stages passed in this session. The newly authored unattended wrapper and updated formal Python unit tests were **not** rerun in this session; treat these as pending integration gates.

The previous six-function default manifest had an outdated source SHA-256 for jp_bit_array.c; the nine-function manifest corrects it to the SHA-256 measured from the current checked-in source, acd4065aeb90b4015c19cc443e5d333e45aaedea94dee710dda4615b2bf0f650. Historical six-function manifest is archived unchanged.

Next: run the new strict unit suite and unattended build wrapper, then promote larger Japanese gameplay functions.

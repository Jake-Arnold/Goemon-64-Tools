# C-Right file12 second native matching-C batch (23 November 2026)

RESEARCH_ONLY. Base stable/decomp 1ddb1b0941b0f39d4db6b0a3534fc1f230b51e0e; verified SHA-pinned archive, original retail and expanded USA and Japan ROM hashes, clean tracked pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee, original SGI IDO5.3 compiler SHA256 76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0. Checked open PR list and targeted PR queries; both positive names absent from the USA manifest and Japanese accepted inventory.

| Region | Function | Original ROM | VMA | Size | Native words | Relocations |
|---|---|---|---|---:|---:|---:|
| USA | func_8020D2A0_5C8770 | 0x5C8770 | 0x8020D2A0 | 204 | 51/51 | 3/3 |
| Japan-0 | func_80212090_5CD620 | 0x5CD620 | 0x80212090 | 204 | 51/51 | 3/3 |

Original ELF FUNC extents and complete isolated linked ROM slices exact. Reassembled original symbolic ASM and verified its annotations against original ROM before each regional comparison. 34 distinct source variants independently replayed, 2 matches and 32 nonmatches. Actual-source GCC and Clang ASan+UBSan tests passed eight finite signed-dimension/coordinate cases per region per compiler (32 total). No gameplay validation.

Positive source SHA256 USA 17803dccf2a3119d21ab7ef0ccf7eb7f0bd3876a4eb286556bf09470d4c55697, JP 96ef2307beefed45ddd7bac30d2e6b57a448917686df667d152573856b2b03ad. Literal-only negative controls change float half=(float)2 to half=2.0f; both retain 204-byte extent and all three relocations but reproduce only 34/51 original words, first difference +0xC (original dimension load vs generated stack adjustment). USA positive NEW_REPRODUCIBLE_QUIRK; JP positive EXISTING_QUIRK_REPRODUCED. This is specific to the regional pair.

Other results: USA/JP descriptor comparators each 9/19 best, original 76-byte size and relocations exact; both stage helpers remain ASM, best 264B versus 256B, first 8 bytes equal. USA spatial-object loader 848B versus 772B, 5/193 aligned words; USA main loader 1200B versus 1072B with first 80 bytes equal and 22/268 aligned words after caching floats. These larger C hypotheses are not validated gameplay logic; JP larger counterparts not attempted. All failed variants retain ASM ownership.

Source-only downloadable artifact Goemon_CRight_Spatial_Native_Research_20261123.zip SHA256 38ec7fcca72d8d5add420cc81d8cb6444040daab54fcbaf28d620037c0abbc4e, verified 39 entries and all 34 source hashes, includes native replay, all variants, actual-source host test, per-attempt evidence/flags and private-input instructions. The two positives and literal-only controls are kept here. No ROM, assembly dumps, objects, savestates or toolchain committed. Full original ROM/combined-C G2, strict inventory, promotion integrity and full local CI NOT_RUN. Canonical counts unchanged: USA 2316 newly matching C (2329 total C entries), Japan 2528 C. Direct Git fetch blocked by DNS; source archive and connector live ref used for research. Next: stage two exact functions in current regional canonical builds, and retain ASM if any acceptance gate fails.

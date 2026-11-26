# Exit overlay adjacent functions — 26 November 2026

ISOLATED_EXACT / RESEARCH_ONLY. Base stable/decomp ee6328ab121bb59b27f03a54c3c80563a720fe77. Four distinct native-exact original functions, 592 bytes, 148 instructions, 12 named relocations. No canonical promotion. Original addresses, positive/negative source controls and original ELF/relocation comparisons were independently checked against the USA and JP ROMs. Canonical USA3056/JP2995 unchanged. Full owner, full G2, strict inventory and promotion integrity NOT_RUN.

| Function | Bytes | Named relocations | Source |
|---|---:|---:|---|
| func_8021617C_5D164C | 172 | 0 | bitpreone |
| func_8021AEF4_5D6484 | 172 | 0 | bitpreone |
| func_80216E54_5D2324 | 124 | 6 | double |
| func_8021BBC4_5D7154 | 124 | 6 | double |

56 distinct variants compiled without errors and were independently replayed, six positive variants (four distinct functions). Six selected negatives rejected. Bitfield assignment-order reversal 38/43 words with first mismatch +0x08; removing redundant null check 9/31 and 120 bytes, first mismatch +0x1C; changing Z to zero 10/31 and 128 bytes, first mismatch +0x1C. Positive C and negative controls in sources/. Eight actual-source GCC/Clang ASan/UBSan executions passed, 278528 total cases. Host fixtures test logical bitfield values, not portable equivalence of bitfield memory layout. Native IDO checked the actual MIPS encoding.

108-byte pair USA 802157C4 / JP 8021A554 remains 24/27, +0x28 float load versus stack reload. Adjacent USA 802150E4 / JP 80219E74 30/32 and USA 80215164 / JP 80219EF4 28/30, +0x30 float-load scheduling. Dispatcher USA 80215230 / JP 80219FC0 remains 17/64 after correcting the second argument pointer: original a1 passed to collision checker unchanged, which reads float fields from it. No gameplay confirmation. Preserve ASM. Pending-PR filename audit found no address-name overlap; not exhaustive manifest audit.

Full source-only replay kit with 56 variants, complete JSON evidence and host tests delivered separately in the task conversation, goemon-exit-adjacent-native-20261126.zip SHA256 601f491e7cf97b38a4220fff2d22f7b41bafaee3e149512c7c997e940f542e83. Selected ten source blobs in this directory byte-verified against locally tested source hashes. No ROM, extracted ASM or compiled code included. Next investigate original literal-pool provenance for the common float-load scheduling difference, then canonical G2 integration of the four candidates.

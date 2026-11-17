# USA file_12 registration wrappers — native object-code verification (2026-11-17)

Status: **374/374 native machine-code match; central integration and promotion pending**.

Environment: user-supplied original USA ROM and pinned upstream build, original IDO 5.3 MIPS compiler, -O2 -mips2 -G 0 -non_shared, MIPS relocatable ELF object. Source generated from original Splat assembly at `asm/usa/5C8770.s` by the pinned `integrate_385.py` algorithm.

- Wrapper first ROM offset: `0x5C9310`
- Wrapper first VMA: `0x8020DE40`
- Functions: **374**, each **0x24** bytes
- Final exclusive VMA: `0x802112D8`
- Original code bytes: **13,464**
- Generated source SHA-256: `046af7d8140efca107fd45b79ea7a08cd8562ad857b9dcbde9323754a6aa639a`
- IDO 5.3 object `.text`: 13,472 bytes, including **8 bytes trailing padding**
- ELF `.rel.text`: **1,122** relocations (three per wrapper: `R_MIPS_HI16`, `R_MIPS_LO16`, `R_MIPS_26`)
- Reconstructed resolved object-code bytes: **13,464/13,464 byte-identical** to the original decompressed USA ROM at `0x5C9310`.
- Byte mismatches: **0**.

Verification procedure: compile the exact generated C source with the upstream compiler flags, extract the object `.text`, parse `readelf -Wr`, resolve each relocation from the original encoded address in its `D_XXXXXXXX_...` or `func_XXXXXXXX_...` symbol, patch the HI16/LO16/26 instruction fields, and compare the first 374 × 36 bytes to the original decompressed ROM. This verifies the full original function machine code, not just structural shape or a source hash.

**Limitations:** The relocation resolutions here use the pinned original addresses; this is a standalone native object-code proof, not a linked coexistence build with the canonical 346 accepted C functions. The central `decomp.verify`, `decomp.inventory`, full `decomp.local_ci`, whole-ELF relocation audit and canonical manifest update are **not** established by this report. Do not count these 374 as accepted until those gates pass. No ROM bytes or proprietary build outputs are committed.

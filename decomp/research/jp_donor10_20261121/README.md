# Japanese additional donor-template native C — 10 original functions

Region `japan_0` only; fresh pinned original `mnsg` commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

This batch finds original Japanese assembly whose MIPS opcode/register structure matches previously accepted Japanese C functions, permitting the same *source algorithm* with the correct regional symbols, callback values and data addresses. It is independent of the earlier 145-function wave and deduplicated against its accepted ELF inventory.

- Ten original-address C bodies are in `sources/`, with SHA-256 source/original-function digests and ROM offsets in `manifest.json`.
- Nine donor variants compiled exact on the first corrected symbol map; the tenth requires the region-correct overlay data table. A separate 44-byte forwarding variant does **not** match IDO's delay-slot integer-zero encoding and remains original ASM.
- `decomp/japan_donor10_promotion.py` stages the C at original ELF addresses, retains genuine ASM including terminal padding, compiles with original IDO 5.3, compares the complete 32 MiB expanded Japanese ROM, all 7,376 ELF function identities and the 80,747 original semantic relocations. It rejects source-hash drift, incorrect owners, offsets, instruction extents and layout changes.
- `decomp/build_japan_donor10_promotion.sh` builds the entire earlier JP2268 baseline from a fresh original checkout before integrating this wave, comparing both the expanded and retail Japanese ROMs. Host tests include three actual-source wrappers under GCC ASan/UBSan with 1,000 deterministic cases each.

This research package contains no ROMs, original disassembly/assembly, proprietary compiler, extracted assets, object files or executable binaries. No emulator gameplay tests were run. Publication is a separate gate following local original-ROM and full CI acceptance.

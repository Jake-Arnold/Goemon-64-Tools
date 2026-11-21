# 21 November 2026 — 112-byte Mini transformation countdown: pristine original-ROM exact C

**PASSED_NATIVE_PRISTINE / RESEARCH_ONLY. NOT formal production promotion.**

Original USA target `func_801E78DC_5A37EC`, ROM `0x5A37EC`, VMA `0x801E78DC`, 112 original instruction bytes; original linked overlay `file_11`. Exact recovered C source in adjacent `countdown_exact.c`, source SHA-256 `770d9bd58004a5c06b011609f0567952cfddd32cda1d66ac113857fcf1ed8229` (verified by `git hash-object` SHA `228161a6e08a0f023226660118836b41842270d8`).

## C source-level change

The previous native compiler candidate had six instruction-word register-allocation differences, despite correct size. Retaining a saved context pointer for the countdown store while directly re-reading the task+0x5C pointer on the *first* context+0x86 halfword load makes genuine IDO 5.3 emit the original 112-byte machine code. The key expression is `M2C_FIELD(M2C_FIELD(arg0, void **, 0x5C), u16 *, 0x86)`. The source does not use inline MIPS, instruction patching or manually padded C symbol lengths.

Native IDO 5.3 `-O2 -mips2 -G 0 -non_shared` generated **27 of 27 non-relocation original MIPS words identical** at their original relative locations; the 28th original instruction is a relocated call `R_MIPS_26` at original `+0x4C` to `func_801DD498_5993A8`, identically represented in the candidate object's `.rel.text`.

## Native pristine original-USA full-ROM integration

Pinned `mnsg` upstream commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; private retail USA Rev 00 source SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Scratch C object substituted at exactly `0x801E78DC` inside original `file_11`. Original and staged complete expanded USA ROMs are byte-for-byte equal **33,554,432 / 33,554,432**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Linked ELF exactness: **7,376/7,376 positive-sized original function identities equal**, **82,216/82,216 semantic relocation records equal**, including **8,825/8,825 `file_11` relocation records**. No positive ELF aliases, extra/missing semantic relocations or ROM changes.

The original ASM translation unit is split into scratch-only pre/post pieces around the 112-byte function. Since the original function starts at a 4-byte but not 16-byte alignment, the assembler adds 4 and 12 **trailing zero padding** bytes to those pieces. The scratch replay validates zeros and proves no relocated symbol lies in either tail, then adjusts **only scratch ELF .text section header sizes** to exclude that assembler-only padding, along with a file_11-only `SUBALIGN(4)` override. All original source game ASM and all generated IDO C instruction words remain untouched. This does not bypass the byte-identical ROM/ELF proof.

**Independent replay:** From a second completely new scratch checkout, recompilation of source with authentic IDO 5.3 and the full 32MiB link reproduced the same original ROM and all original ELF identities/relocations. The conversation artifact `GOEMON_MINI_COUNTDOWN_NATIVE_EXACT_20261121.zip` contains exact C source, a fail-closed cross-platform Python scratch linker/replay and semantic ELF comparison, JSON proof and source hashes. It excludes original ROM, original ASM, object/ELF/binaries, compiler and game assets.

**Current canonical status:** the complete latest `chatgptweb/decomp` checkout containing **1,956 already-accepted USA C** could not be cloned in the isolated Linux container (DNS); no combined `python3 -m decomp.verify`, strict inventory, full `decomp.local_ci` or emulator gameplay was run with this countdown source and all earlier accepted functions. Therefore **do not add this 112-byte research match to accepted count** or update production decomp manifests. Checked count remains 1,956 USA C, 83,940 accepted original instruction bytes, 5,407 ASM. The earlier three 752-byte native-pristine Mini speed matches are also separately unpromoted in this draft PR.

**Next acceptance step:** obtain a complete verified local checkout of live `chatgptweb/decomp`, stage only truly new original-address functions (three earlier speed C + this countdown), run current combined G2, strict inventory and full CI, and only promote on PASS. Large 4,320-byte `func_801CD310_589220` remains nonmatching, with newly verified 292-byte blockwise region as a separate research result.

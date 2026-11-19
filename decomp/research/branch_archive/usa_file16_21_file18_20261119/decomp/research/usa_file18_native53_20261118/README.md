# USA file_18: 53 original-address native-exact C functions / 796 bytes (research-only)

18 November 2026. RESEARCH_ONLY. This work does not modify canonical accepted source ownership, manifest, results or inventory.

Starting live USA accepted inventory: 966 functions / 41,324 instruction bytes; Japan-0 independently 39 functions / 2,092 bytes. Potential 966+53 = 1,019 is not a production accepted count.

## Discovery

From the authenticated original-USA Splat file_18 overlay source spanning 0x676C80 through 0x693770, scanned 70 previously unpromoted short functions after excluding twelve already accepted file_18 native87 functions. Original IDO 5.3 -O2 -mips2 gave 53 exact function matches (796 original instruction bytes) in 50 distinct C source units. Fourteen attempted functions FAILED_NATIVE, three were not supported by a C draft. These are 36 one-float stores, six two-float zero setters, five three-float zero setters, four three-float stores to a pointer at owner +0x18, one 10-bit halfword masked setter and one no-op callback. No new fixed guest-RAM global or validated gameplay field label is claimed.

source_catalog.txt contains all 50 C units, separated by a unit label and pipe-delimited function definitions. The exact local catalog Git blob SHA-1 and uploaded Git blob are both 60cd01e4f3469f38807a042fd5c130866e973767. Catalog SHA-256: 2b2f5f49ad89935ba7312a49b2aee4af3e6ffb8b041167895382acf13cf9b57f. Recreate the original 50 C files using regenerate_sources.py, then verify original-address native instruction bytes using verify_native.py and the privately owned expanded USA ROM.

## Native scratch evidence ACTUALLY run

- Original USA 16 MiB retail ROM SHA-1 df8083a54296b8c151917c5333e1c85f014a2a66; original 32 MiB expanded ROM SHA-1 6ea0ed71032ce08fc2745f412d84936382197494; pinned upstream commit 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee.
- Pristine original upstream USA built exact 33,554,432-byte baseline before any candidate replacement.
- All 53 independently compiled with native IDO 5.3 -O2 -mips2 and matched original function extents and instruction sequences.
- Split Splat original file_18 at 50 C unit intervals while retaining intervening ASM; subalign 4 and assembler -no-pad-sections. Generated zero-only ELF32 .text section-header tail trimming totaled 292 bytes across 50 C objects; original instructions and relocations not modified.
- Single disposable scratch ROM including all 53 C functions plus original ASM elsewhere: 33,554,432 / 33,554,432 bytes equal; expanded ROM SHA-1 unchanged.
- Exact semantic ELF relocation audit: 72/72 sections, 82,216/82,216 records; original ELF positive-sized function identities 7,376/7,376, no new aliases. Candidate linked ELF SHA-256 3a91d8e9eba47a7f32051ee09ac8e76bca4fea00b139963e04869f9091f55018.
- All 53 actual original C source bodies compiled into GCC -Werror -fsanitize=address,undefined host test: PASS for scalar/paired/triple float writes, nested pointer, mask and unaffected adjacent fields.

## Production gate NOT RUN

The native host could not materialize a complete authenticated live 966-C canonical checkout because direct shell GitHub DNS failed. Canonical 1,019-C python3 -m decomp.verify, python3 -m decomp.inventory and full python3 -m decomp.local_ci were NOT RUN. Therefore 0 newly accepted production functions. Do not merge/promote before all canonical ROM/ELF/relocation/inventory/full local sanitizer CI gates pass.

Sources are C reconstruction text only. No original ROM, generated ASM, assets, object code, toolchain or private memory included.

# USA file_27: 21 original-address matching-C functions

Status: native whole-ROM `PASSED_G2` on 18 November 2026; all 21 functions and 1,316 original instruction bytes are accepted only together with all 966 preceding production USA C functions.

The 21 separately linked original-address IDO 5.3 probes in `isolated_native_results.json` were compiled using `-O2 -mips2`; each matches its original instruction range, after excluding only zero linker alignment padding. Their sources under `sources/` are pinned by SHA-256 in `promotion_manifest.json`.

The fail-closed canonical `overlay_file27.py` stage authenticates source digests and the 32 MiB original ROM, unique live assembly parent ownership, word-for-word address coverage and relocatable object instructions. It stages 21 C files and eight retained ASM fragments. It then enforces original ROM SHA-1, all 7,376 ELF function entries, original `file_27` relocations (876), unchanged main/entry and all overlay relocations, and no new symbol aliases. Existing historical symbol alias exceptions in file_11 were already present before this batch.

The canonical exact proof is `decomp/results/combined.json`; strict inventory is `decomp/results/inventory.json`; checkpoint report is `decomp/results/usa_file27_adjacent21_987_promotion_20261118.json`. The original ISA and overlays are USA-specific; no Japan ROM source was staged. The original assembly remains accessible in the pinned upstream checkout and is not checked into this repository.

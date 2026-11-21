# Japanese original native C — 29 previously failed candidates revisited

**Region:** Japan rev-0. **Previous accepted baseline:** JP2289 (122,280 original bytes; 5,087 ASM). **New local full G2:** JP2303 (122,792 bytes; 5,073 ASM).

The original `failed_native.json` contained **31 failed attempts covering 29 unique functions**. Five of those functions were already accepted in the JP2289 baseline; these were not counted twice. The other 24 were retried using original IDO 5.3, changed C pointer/value types, persistent temporaries and statement ordering.

**14 new original-address functions (512 instruction bytes)** compile exactly in isolation and in the full Japanese 32 MiB image. All 7,376 original ELF positive function identities and all 80,747 semantic relocations were verified unchanged. The source set includes seven relocation-bearing functions with 14 original HI16/LO16 symbolic relocations, preserved by the complete original-ELF gate. The 16 MiB Japanese retail image also compresses identically to the original. The 10 remaining names are recorded in `failed_native.json` and remain original ASM.

Sources under `sources/` are human-reviewable C, not original code dumps. Manifest SHA-256s bind all source and ROM-offset names. One compiler output may contain trailing linker alignment beyond the named function; only original source function instruction extents are accepted and original padding remains unchanged.

## Proof and reproducer

- `decomp/japan_retry29_promotion.py` — strict ASM owner, original ROM, source hash, MIPS ELF and complete semantic relocation gate
- `decomp/build_japan_retry29_promotion.sh` — clean pinned upstream replay, building through JP2289 then applying these 14 C implementations
- `decomp/test_japan_retry29_promotion.py` — ROM-free source integrity/negative and 1,000-case GCC ASan/UBSan actual-C host tests
- `decomp/results/japan_0_2303_retry29_g2_20261121.json` — original G2 evidence
- `decomp/results/japan_0_2303_retry29_inventory_20261121.json` — strict accepted-C/ASM partition

No ROMs, original assembly, toolchains, built objects or ELFs are included.

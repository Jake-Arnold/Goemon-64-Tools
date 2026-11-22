# USA 27 cross-region source recovery — full native G2 (2026-11-22)

Status: **PASSED_G2_LOCAL**, 27 original-USA C functions independently recovered from published Japanese JP55 donor C using original USA ASM and exact symbols. This is the first 27 of the remaining 51 research candidates; the other 24 are **NOT PROMOTED**. The original source-only 51 archive could not be materialized and was **not** treated as a source input.

- USA starting published state: **2,014 matching-C functions**, 87,900 original instruction bytes.
- This stage: **27 distinct original ASM-owned functions**, 1,904 original instructions bytes; **77/77** original `.text` symbolic relocations at original USA guest VMAs. Ten original functions are `#pragma GLOBAL_ASM` owners in `src/dialogue_window.c`; 17 live in separately linked assembly parents. Original ASM instructions and ROM input never modified.
- USA ending staged state: **2,041 matching-C functions**, 89,804 original instruction bytes, 5,322 ASM functions. 33,554,432-byte original ROM **exact**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. All **7,376** ELF FUNC identities present; complete semantic relocations multiset **82,103** unchanged; strict C/ASM inventory **PASS**.
- One original ELF annotation was corrected: canonical `func_8000D3B8_DFB8` size 72 versus original 64, and newly compiled source size 64. This is the only permitted identity change relative to immediate predecessor. It **restores** the original identity rather than weakening the check; the other pre-existing 48/56 size anomaly remains unchanged. Proof records the exact exception.
- Full ROM-free post-integration `python3 -m decomp.local_ci` **PASS**, including new provenance/adapter-scope tests. No in-game emulator execution claimed.

## Reproduce

Requires the exact original USA retail ROM, pinned SGI IDO 5.3, pinned mnsg checkout and a locally built, G2-verified **USA2014** candidate checkout, already provided by the prior staged promotion. Those private inputs must not be committed.

```sh
python3 -m decomp.usa_crossregion51_recovered27_g2_promotion stage --checkout "$CANDIDATE" --prior "$PREDECESSOR_BACKUP"
python3 -m decomp.usa_crossregion51_recovered27_g2_promotion build --checkout "$CANDIDATE" --deps "$DEPS" --runtime "$RUNTIME"
python3 -m decomp.usa_crossregion51_recovered27_g2_promotion verify --checkout "$CANDIDATE" --prior "$PREDECESSOR_BACKUP" --original "$ORIGINAL_BASELINE"
python3 -m unittest decomp.test_usa27_recovered_g2 -v
python3 -m decomp.local_ci
```

A stage requires an untouched exact predecessor and a fresh backup path. Do **not** run it twice on the same candidate. See `decomp/results/usa_recovered27_2041_g2_20261122.json`, immutable `manifest.json` and every exact C source in `sources/`. Source bytes and their original code range are hashed in the manifest. No file contains ROM binaries, disassembly listings or toolchain binaries.

**Remaining 24** original research candidates: 19 related float range/ratio setters (84 bytes each), four 80-byte callback wrappers with one relocation each and one 44-byte byte-to-float setter. No full-ROM promotion for those 24 was run.

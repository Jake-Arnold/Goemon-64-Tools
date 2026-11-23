# USA/Japan original-ROM short-function dedup research — 23 Nov 2026

**RESEARCH_ONLY. No accepted-C promotion or complete original-ROM G2 for the six new candidates.**

Base: `stable/decomp` 4b289a015a2ffd9f47ca3356d09a248836e8dee8. Original USA and JP 32MiB images independently authenticated; original pinned `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; original IDO 5.3 native MIPS compiler.

## Canonical deduplication
- USA: 2,092 accepted matching C, 94,760 original bytes, 5,271 ASM.
- JP: 2,370 accepted matching C, 127,008 original bytes, 5,006 ASM; all 24 independent cumulative canonical stages reconciled without overlap.
- Annotated, ASM-owned original functions with size **strictly <100B**: USA **961**, JP **824**.
- Original code byte-hash hints: 38 unaccepted short functions have exact-code accepted-C donors; 211 USA/JP byte-identical ASM short pairs; 45 within-region ASM duplicate groups; 335 cross-region accepted-C exact-code groups. Raw-code hash is not sufficient to prove cross-region C equivalence, original-global relocations or original source ownership. This is the scoped annotated-ASM inventory, not the entire positive ELF-symbol inventory.
- **6 new isolated native original-instruction matches, 264 bytes**, recorded in `evidence.json`. All six have source-only negative controls in `native_probe.py`. These exact isolated bodies retain original ASM canonically.

Full 1,785-function per-candidate inventory, independent deduplication script, complete native probe and all six source files delivered in the corresponding ChatGPT source-only ZIP `goemon-short-functions-audit-20261123.zip`, SHA256 `83b5b41ddc5726833bafaceeaafdca55cb8ca10903e25148cd36cbf4abd8637f`. The full archive contains no original code bytes or ROMs.

Reproduce six isolated candidates against user-owned **decompressed** regional original ROMs:

```sh
LD_LIBRARY_PATH=/private/goemon-runtime-additions/lib \
 python3 decomp/research/region_short_under100_20261123/native_probe.py \
 --ido /private/mnsg/tools/ido-5.3/cc \
 --objcopy /private/goemon-dependencies/bin/mips-linux-gnu-objcopy \
 --usa-rom /private/usa/baserom.decompressed.z64 \
 --jp-rom /private/jp/baserom.decompressed.z64 \
 --out /tmp/NEW-native-short-probe
```

The script checks full regional SHA1 and source-mutation negative controls, *but not* whole translation units, ELFs, linker relocations, full original-ROM equivalence or new inventory. **Full `decomp.local_ci` NOT COMPLETED** for this research candidate; canonical stored `decomp.promotion_integrity --validate` PASS on unchanged USA 2,092. No game execution and no changed published C counts.

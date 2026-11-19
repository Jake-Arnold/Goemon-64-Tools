# USA original-address actor-state field copy

- Function: `func_80035398_35F98`, USA expanded ROM `0x35F98`, VMA `0x80035398`, 12 instruction bytes, original `main` section, upstream ASM parent `35280.s`.
- Source: `sources/statecopy1_000.c`, native original IDO 5.3 flags (`-O2 -mips2`). Copies word 5 into word 3 of an opaque state array; no higher-level type semantics claimed.
- Original code SHA-256: `2bde60ad28d9c7e327e3543580b3692be866a2f37c5c387d66cc2b05064e4071`.
- Independent native object `readelf -Ws`: one `FUNC`, 12 bytes, offset 0. Object instruction bytes at original range match all 12/12 reference bytes. `readelf -Wr`: no relocations. Trailing zero alignment omitted from instruction comparison.
- Before staging, canonical `decomp/results/combined.json` claims exactly 1,500 functions; the new function is absent. The prior accepted `main` parent stage includes eight adjacent C funcs, so the original remaining ASM owner must be dynamically recovered from the *fully staged accepted* 1,500 checkout.
- Integration stage is fail-closed. **Native isolated match is not full original ROM or production acceptance.** Only fresh combined 1,501-C G2, strict ELF/relocation/inventory, full local CI and a verified GitHub publication can promote it.
- Original ROM/ASM/object bytes are intentionally not committed.

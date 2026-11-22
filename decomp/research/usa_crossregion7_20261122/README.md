# Seven JP↔USA matching-C transfers, 22 November 2026

**Scope:** source-only original-USA research and fail-closed production adapter. Original private ROMs, upstream ASM, native IDO, ELF, object files and other copyrighted/proprietary binary materials are **not** included.

The source fixture contains seven original-USA IDO5.3 matching-C functions in `sources/xreg7_000.c` … `xreg7_006.c`, with immutable hashes, USA guest VMAs, ROM offsets/sizes, JP donor locations when available and source relocations pinned in `manifest.json`. It is only valid against the specific, published **2,072 C / 92,492-byte** predecessor manifest and is not usable to re-promote the same functions at a later branch head.

The promotion adapter `decomp/usa_crossregion7.py` reuses the original-source ownership and linker-splitting logic in `decomp/overlay_isolated233.py`; six targets replace exact individual ASM extents, and the original object-list helper at USA `0x36FF4` replaces its own inline `GLOBAL_ASM` in `src/object_flags.c`. Previous mixed C and remaining ASM stay in their original translation units. The source archive is **not** a raw ROM patch and is not a standalone build: it needs the complete, pinned `mnsg` checkout, authenticated private retail USA ROM, exact SGI IDO5.3 and MIPS tools, and the current canonical decomp verifier.

Canonical source test:

```bash
python3 -m unittest decomp.test_usa_crossregion7 -v
```

Complete original native ROM G2, using *new paths* and the tools described in `GOEMON_BUILD_ENVIRONMENT.md`:

```bash
python3 -m decomp.verify --upstream "$GOEMON_UPSTREAM" \
    --retail-rom "$GOEMON_ROM" --workdir "$NEW_WORKDIR" \
    --report "$NEW_REPORT" --uv "$(command -v uv)" --jobs 4
python3 -m decomp.inventory --baseline "$NEW_WORKDIR/baseline" \
    --candidate "$NEW_WORKDIR/candidate" --report "$NEW_INVENTORY"
python3 -m decomp.promotion_integrity --validate
python3 -m decomp.local_ci
```

When a validated prior baseline cache is used, `decomp.inventory --baseline` must point at the actual certified cached baseline directory. For non-matching branch heads or corrupted sources, stop and rebase; never weaken source hashes or reuse a stale proof. The exact acceptance results and limitations are documented in the dated G2 report and `PROGRESS.md` once the complete transaction passes. This repository is exclusively the `chatgptweb/decomp` branch, not the live toolkit's `main`.

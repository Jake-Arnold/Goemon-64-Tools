# Promo367 — original native matching C

Base: `stable/decomp@67ff7d0cb4735e67db7a19229fe159dc14ccee65` (source archive 15015267782, verified COMMIT and SHA256SUMS; prior CI 45601372892). The two research checkpoints of 25 November 2026 supply 282 USA and 85 Japanese distinct original address ranges. Source/negative control hashes and exact original IDO flags are pinned in the regional candidate manifests. No original ROM, original assembly dump, compiler or object files are included. The 13 USA upstream C functions are excluded. Open decomp PRs 200, 202, 203, 205–214 (existing numbers only), 220, 225–234 (existing numbers only), 236, 240, 244 and 246 checked; PR200 index range comparison found no overlap; appearances of `func_80035690_36290` in other sources are callee references, not overlapping ownership.

## Reproduce

Use authenticated original USA and Japan ROMs and pinned upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee with the existing native toolchain. Read `AGENTS.md`, `CONTINUE.md` and `COMPILER_QUIRKS.md` first. Use the original pristine Splat extraction for original-function references. From the repository root, run the existing production verifier against the authenticated original USA baseline:

```
python3 -m decomp.verify --upstream "$USA_UPSTREAM" --workdir "$USA_WORK" --retail-rom "$USA_ROM" --report "$USA_REPORT" --jobs 8
```

The verifier runs all previous canonical stages and the new USA stage. For Japan rebuild all preceding stages to JP2757 per their retained replay instructions, then on that isolated native candidate checkout:

```
python3 -m decomp.promo367_promotion --region japan_0 --checkout "$JP_2757_CHECKOUT" --pristine "$JP_ORIGINAL_SPLAT_CHECKOUT" --work "$JP_367_WORK" --uv "$UV" --jobs 8
```

The checkout must contain the exact canonical predecessor ELF; the pristine checkout must contain the authenticated original ROM and original per-function Splat references. Both native stage runs require actual original IDO 5.3, every negative control rejected, exact expanded and recompressed retail ROMs, exact positive FUNC identity, semantic relocations, stable globals, strict readelf inventory and ASM-to-C ownership. No historical original translation-unit or live gameplay claim. The source layout uses artificial split owners and retains original padding. The Japan original-Splat recovery during this session was necessary because an earlier assembly-only checkout omitted historical per-function references. The original independent extracted assembly was used, not reconstructed C.

`python3 -m decomp.promotion_integrity --validate` and `python3 -m decomp.promo367_promotion` validate the stored canonical proof/manifest/inventory and immutable predecessors without original ROMs. Hosted full ROM-free CI remains mandatory before merge.

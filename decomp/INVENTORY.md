# Whole-build function inventory

This document explains the stored USA ELF inventory and the later 21 November 2026 full-G2 promotions, including the latest Japan-only **published** result at 2,123 matching C. **This is not a replacement for fresh native proof.** Read [CONTINUE.md](CONTINUE.md) and [the latest acceptance report](docs/GOEMON_START5_G2_PROMOTION_20261121.md) before using any figures.

## Versioned counts

| Measure | Stored USA inventory | Published USA G2 | Latest Japan-0 published G2 |
| --- | ---: | ---: | ---: |
| Newly matching original-address C | **1,956** | **1,958** | **2,123** |
| Original instruction bytes from reconstructed C | 83,940 | **84,292** | **112,336** |
| Remaining original assembly entries | 5,407 | **5,405** | **5,253** |
| Original positive-sized ELF function entries | 7,376 | 7,376 | 7,376 |
| Expanded ROM bytes matched | 33,554,432 | 33,554,432 | 33,554,432 |

**Stored canonical USA inventory:** [results/inventory.json](results/inventory.json) and [results/combined.json](results/combined.json), from the 20 November 1,956-function batch. The inventory also records **13 pre-existing upstream unmarked C functions**, meaning `1,956 + 13 = 1,969` total unmarked positive-size ELF entries and `1,969 + 5,407 = 7,376`.

**Later USA G2:** [five-function regional ledger](results/glitch_start5_2121jp_1958usa_g2_20261121.json) accepts **two new USA original-address C functions** (100 and 252 bytes), giving `1,958 + 13 = 1,971` unmarked entries and `1,971 + 5,405 = 7,376`. The five-function report also accepts **three additional Japan-0** functions. Its local proof was subsequently published and remotely re-verified, as recorded in [PROGRESS.md](../PROGRESS.md). A later [Japan script-VM two-function original-ROM G2 report](results/japan_0_2123_vm_g2_20261121.json) adds **two more** functions (92 bytes), resulting in **2,123** matching C and **5,253** ASM. **This last increment is `PASSED_G2`, remotely published and re-verified**; do not conflate its status with the previous 2,121 published stage. The old stored `inventory.json` is **not manually rewritten**, because it represents an earlier authentic native build.

**Region SHA-1:** expanded original USA `6ea0ed71032ce08fc2745f412d84936382197494`; expanded original Japan-0 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. The pinned upstream revision is `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.

## Inventory semantics and edge cases

`decomp.inventory` reads original/candidate ELF symbol tables using MIPS `readelf`. It counts defined positive-sized `STT_FUNC` entries, requires original entry identity, and checks C/ASM ownership against the matching manifest. It does not turn a research candidate, object file, undefined symbol or data-only marker into a decompiled function.

- The candidate linker exports **851 zero-sized switch labels** as function symbols for mixed C/ASM. They are excluded. Raw `FUNC` counts are misleading.
- The baseline function-entry map is authoritative when overlays reuse the same guest VMA; overlay functions must remain distinct by section/ROM ownership.
- Two historical size-annotation differences remain tracked: `func_8003F6E8_402E8` (48 original vs 56 candidate metadata bytes) and `func_8000D3B8_DFB8` (64 original vs 72 candidate). These are not additional recovered functions, and the original ROM still matches.
- Strict original ELF identities **and all semantic relocation records** must remain the same. An exact 32 MiB byte stream can still be rejected when original relocation symbols differ.
- Function count measures identified original ELF entries, not percentage of code bytes or total project completion. Some SDK/runtime assembly may legitimately remain ASM.

## Reproduce a new canonical inventory after an actual native G2 run

From a suitable Linux checkout with the verified original private ROM and pinned native toolchain:

```bash
python3 -m decomp.verify \
  --upstream "$GOEMON_UPSTREAM" \
  --workdir /tmp/goemon-fresh-verify \
  --retail-rom "$GOEMON_ROM" \
  --report practice/diagnostics/goemon-verify.json \
  --uv "$(command -v uv)" --jobs 2

# Only after decomp.verify succeeds:
python3 -m decomp.inventory \
  --baseline /tmp/goemon-fresh-verify/baseline \
  --candidate /tmp/goemon-fresh-verify/candidate \
  --report practice/diagnostics/goemon-inventory.json
```

Verify the region's latest staged sources, complete relocations and original ELF identities as well as the ROM hash. Run the full `python3 -m decomp.local_ci`. **Do not** overwrite authentic older result JSON with manually changed totals or infer a completed regional build from a document.

# USA canonical reconciliation of 108 missed C promotions — 22 November 2026

This is a **canonical native matching-C promotion**, not a detached research count. The previous staged 100-function report had 100 real native C identities but did not update canonical proof/inventory; meanwhile a six-function and two-function batch landed on the canonical branch. Research candidate `func_800108BC_114BC` was already accepted by the six-function stage, and the other old scheduler/Start C routines had been lost from the accepted canonical count. All were reconciled by **original ROM range**, not symbol nickname.

- Base: canonical 1,964 matching USA C functions / 84,708 original bytes / 5,399 ASM, branch `chatgptweb/decomp` at `56c54a88e4f70e44ed0d676dc552fa80bf9aa2c7`.
- New source: frozen `manifest.json` lists 108 individually SHA-256 checked original-address C sources, 7,784 bytes. Twelve original C/ASM mixed owners and 96 previously standalone ASM functions retained at their precise original positions. Source files remain in existing research directories; none duplicated.
- Final: canonical 2,072 original C functions / 92,492 instruction bytes / 5,291 ASM. 33,554,432 original USA ROM bytes and SHA1 `6ea0ed71032ce08fc2745f412d84936382197494` exact.
- Proof: full `python3 -m decomp.verify` and `python3 -m decomp.inventory` with 7,376 ELF positive function entries and unchanged 82,103 canonical semantic relocs; 14 pre-existing file11 alias-name relocations match original targets/types/addends and previous canonical symbol names exactly, with zero new alias drift. One original 64-byte `func_8000D3B8_DFB8` size annotation corrects an earlier 72-byte positive ELF entry.
- Fail-closed reconciliation stage `decomp/usa_canonical_reconcile108.py` is part of canonical `decomp/verify.py`; it demands original SHA/individual code hashes, predecessor manifest and original accepted function registry hashes, original-owner non-overlap, native code placement, complete ROM, ELF and relocation equality.
- Prevention: `python3 -m decomp.promotion_integrity --validate`, now run in full `decomp.local_ci`, requires canonical manifest, `results/combined.json`, `results/inventory.json`, source-proof, and function identity agreement. A detached G2 record cannot increment accepted counts.

## Reproduce

Use private authenticated 16 MiB USA retail ROM and the pinned, clean extracted `mnsg-japan` checkout and dependencies; no ROM or proprietary toolchain is distributed in this repository.

```sh
python3 -m decomp.verify --upstream /PRIVATE/mnsg-japan --workdir /PRIVATE/fresh-2072 --retail-rom /PRIVATE/Mystical_Ninja_USA.z64 --report /PRIVATE/fresh-2072-report.json --uv /PRIVATE/uv --jobs 4
python3 -m decomp.inventory --baseline /PRIVATE/fresh-2072/baseline --candidate /PRIVATE/fresh-2072/candidate --report /PRIVATE/fresh-2072-inventory.json
python3 -m decomp.promotion_integrity --validate
python3 -m decomp.local_ci
```

The inventory and local CI commands must be run **after the canonical proof and inventory have been updated and independently inspected**. The historical predecessor reports are preserved under dated filenames; the dated reconciliation G2 report is `decomp/results/usa_canonical_reconcile108_2072_g2_20261122.json`.

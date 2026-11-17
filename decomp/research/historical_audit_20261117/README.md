# Historical original-address research reconciliation — 17 November 2026

**Status: RESEARCH_ONLY / DOC_ONLY; no C promotion from this audit.**

This audit systematically rechecks the **recorded research evidence** against the live USA **864-C / 37,904-byte** and Japanese rev-0 **39-C / 2,092-byte** production manifests. It is not a claim to have native-recompiled every one of the remaining **6,499 USA assembly entries**, nor does it declare historical task statuses current evidence. The locally mounted 864/39 source was independently checked against the current GitHub manifest/combined/inventory/registry Git blob SHAs before analysis. The original ROM is never read by `audit.py`.

## Verified historical coverage

- `INDEX.json`: 100 architect task definitions, **77** structured historical execution evidence records, **85** noncanonical report metadata records and **45** historical branch references, with source paths and Git blob hashes.
- All **87** entries from the former 782-C pending candidate registry are present in the accepted USA/Japan canonical matching sets. The current production candidate registry has zero entries as of this snapshot. Historic status strings in older reports are *not* new pending candidates.
- The script-VM translation unit still explicitly owns **13 original ASM functions**, including `D468`, `D68C`, `DBEC`, `DE80`, `DF98`, `ED60`, `F038` and `F6E8`. Their semantic/regression reports are preserved; no whole-function native C match is established for them.
- Recorded legacy native retries for the 92-byte file table helper `func_80001DF4_29F4` and 48-byte VM wrapper `func_8003F6E8_402E8` already live in `decomp/research/legacy_revisit_20261117/`. Both remain assembly; source/trace evidence preserved.

## Outstanding native-exact research not yet promoted

The old **87-item** production candidate registry does *not* include newer scratch/isolated leads. These are separate, explicitly unpromoted groups:

| Group | Prior / refreshed evidence | Why it remains research |
| --- | --- | --- |
| Five USA main-code graphics helpers | Fresh IDO 5.3 original-address recheck: **5/5**, **284/284 bytes**, exact ELF FUNC name/VMA/size; original scratch whole ROM also previously passed | No new 864+5 canonical whole-ROM G2, main-code source/ASM layout adapter, full ELF relocation/inventory gate |
| USA file 27 callback islands | **21 original functions / 1,316 bytes** across seven source units, previously original-VMA and upstream scratch-ROM exact; research source is on canonical decomp | No simultaneous **864+21** accepted-C build or strict canonical inventory/CI gate |
| USA file 25 callback | One **72-byte** isolated-exact function | Original relocation equivalent link blocked by an artificial extra symbol; no G2 |
| USA file 26 adjacent callbacks | **15 total / 2,508 bytes** in upstream scratch; **12 new / 2,196 bytes** beyond the previously exact 312-byte trio | No full 864+12 canonical production gate; separate **236-byte initializer** still fails IDO at +0x98 |
| Three nearby graphics routines | 76 / 108 / 48-byte prior codegen near matches | Order of stores, LUI scheduling, and argument home scheduling remain mismatched |

**Fresh test here:** `recheck_graphics.py` runs compiler/source SHA checks, exact original guest VMA and linked ELF FUNC size comparisons, and a complete 284-byte original-ROM instruction comparison. Its results are in `decomp/results/graphics_five_native_recheck_20261117.json`. The three original C sources are byte-for-byte identical to their provenance at research PR #63. The PR's unchanged independent scratch-ROM proof is retained as `decomp/results/graphics_adjacent_scratch_proof_20261117.json`; its earlier 782-C baseline is historical and its canonical production gates explicitly remain **NOT RUN**.

**Precise proof boundary:** Fresh five-function `ISOLATED_OR_COHERENT_GROUP_EXACT`. Original source-unit scratch ROM checks from prior research are authentic as recorded but **not** a full 864-C combined production verifier. Original ELF relocation equality for the integrated canonical branch has **NOT RUN**. No in-game validation or Japanese C promotion is claimed.

## Reproduce on Linux

Run the metadata audit without a ROM:

```sh
python3 decomp/research/historical_audit_20261117/audit.py \
  . /tmp/goemon-historical-audit.json
```

For native recheck, use privately owned pinned expanded USA ROM, original IDO 5.3 and MIPS binutils; keep ROM/objects out of Git:

```sh
python3 decomp/research/historical_audit_20261117/recheck_graphics.py \
  --rom /path/to/usa/baserom.decompressed.z64 \
  --ido /path/to/pinned/mnsg/tools/ido-5.3/cc \
  --report /tmp/goemon-graphics-native-recheck.json
```

Run full ROM-free CI separately with `python3 -m decomp.local_ci`. A passing `local_ci` never replaces fresh original-ROM `decomp.verify` and `decomp.inventory` for matching-C promotions.

## Follow-up ordering without repeating failed hypotheses

1. Stage **five** native-exact graphics helpers in original main-code Splat translation units, preserving ASM siblings and main linker padding; verify all **869** simultaneously with accepted USA C using G2/inventory/local CI before promoting any.
2. Stage the **21** original file_27 exact native C and all **15** file_26 helpers (original three plus twelve newly exact) using separate, region/overlay-specific production adapters; do not treat their upstream scratch ROMs as combined proof.
3. Resolve the file_25 symbol-relocation discrepancy from genuine original symbols; no artificial source names.
4. Revisit the **13** VM ASM functions according to established F038/DE80/ED60 original ABI and control-flow evidence. Stop on source budget; preserve ASM when native words differ.
5. Address the recorded graphics near-matches and 236-byte file_26 initializer only with a falsifiable compiler-scheduling improvement.

Original research is **linked, not overwritten**. This index never deletes or modifies previously accepted C sources, manifests, canonical combined-ROM proofs, ELF inventory, or the Japanese build. There is no source evidence supporting a claim that every one of the 6,499 remaining ASM functions has previously been researched.

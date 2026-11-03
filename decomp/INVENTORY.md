# Whole-build function inventory

Date: 2026-11-02. Pinned upstream:
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Baseline and current candidate
both reproduce decompressed ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
The current [metadata report](results/inventory.json) records the measurement,
ELF hashes, tool hash and original entry-map identity.

| Inventory | Entries |
| --- | ---: |
| Identified function entries across the configured ROM | 7,376 |
| Matching C already in pinned upstream | 13 |
| Newly matching C in this toolkit's decomp track | 124 |
| Matching C combined | 137 |
| Still marked as assembly | **7,239** |

The VM unit is a smaller subset: 52 of its 69 functions are matching C, with
17 retained assembly functions. Its remaining count is not the whole-game count.
The toolkit's headline 124-function count deliberately excludes the 13 routines
already present as matching upstream C. The report lists those names explicitly;
existing source definitions were checked in the pinned upstream C units.

## What is counted

`inventory.py` reads the pinned baseline and candidate ELF symbol tables using
MIPS readelf. It counts defined, positive-sized `STT_FUNC` entries. Their original
names and entry addresses must agree between builds, and newly unmarked names
must agree exactly with the matching manifest. It checks both complete ROM
identities before producing a report. Objects, undefined/absolute symbols and
data-only `.NON_MATCHING` markers do not become functions.

The candidate exports **850 zero-sized switch labels** as function symbols for
mixed C/assembly linking. They are excluded; a raw `FUNC` count would incorrectly
report 8,226 entries. Overlay functions sharing a guest address remain separate
entries, and positive-sized aliases are reported rather than silently merged.
No positive-sized alias duplicates were found in this pinned inventory.

One retained routine, `func_8003F6E8_402E8`, has different ELF size metadata:
48 bytes in baseline and 56 in the mixed build. The extra extent covers its
existing alignment tail; entry addresses and all ROM bytes are unchanged. This
is recorded as a size-annotation difference, not a newly recovered function or
extra code. The baseline entry map remains the identity reference.

This is an inventory of **currently identified native function entries**, not
proof that every logical function boundary is known. It includes SDK/runtime
assembly; some low-level assembly may appropriately remain assembly. Script
commands, data formats, assets and runtime integration are separate work, so
function count is not an estimate of time remaining or a full-decomp percentage.

## Reproduce after a matching checkpoint

From the toolkit repository inside the build environment:

```bash
python -m decomp.inventory \
  --baseline /path/to/fresh-verifier-run/baseline \
  --candidate /path/to/fresh-verifier-run/candidate \
  --report practice/diagnostics/inventory-next.json
```

The command reads builds and writes only a new metadata report; it never
modifies a build/game or replaces an existing report. Review and refresh the
checked-in metadata after each matching checkpoint. Tests require it to agree
with the current manifest and inventory tool. Synthetic tests also cover zero
labels, data markers, overlapping guest addresses, unsupported promotions,
regressions, moved entries, ambiguous symbols and size annotations.

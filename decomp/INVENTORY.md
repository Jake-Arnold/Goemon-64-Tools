# Whole-build function inventory

**Current proof snapshot: 2026-11-16.** Pinned upstream revision:
`7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`. Baseline and candidate
reproduce the same decompressed 33,554,432-byte USA ROM, SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`. Full native verification
passed **210/210** exact C function claims and **13,336 instruction bytes**.
The [current metadata report](results/inventory.json) records ELF fingerprints,
source tool identity, and the immutable original function-entry map.

| Inventory | Entries |
| --- | ---: |
| Identified function entries across the configured USA ROM | 7,376 |
| Matching C already in pinned upstream | 13 |
| Newly matching C in this toolkit's decomp track | 210 |
| Matching C combined | **223** |
| Still marked as assembly | **7,153** |

The 50 newly promoted `file_11` functions comprise 13 native
character-switch routines and 37 empty actor callbacks. Two split-generated
four-byte `nop` labels were explicitly restored to their original
non-function symbol status before the inventory was accepted. The 180-byte
character selector is still owned by assembly.

## What is counted

`inventory.py` reads the pinned baseline and candidate ELF symbol tables using
MIPS readelf. It counts defined, positive-sized `STT_FUNC` entries. Their original
names and entry addresses must agree between builds, and newly unmarked names
must agree exactly with the matching manifest. It checks both complete ROM
identities before producing a report. Objects, undefined/absolute symbols and
data-only `.NON_MATCHING` markers do not become functions.

The candidate exports **851 zero-sized switch labels** as function symbols for
mixed C/assembly linking. They are excluded; a raw `FUNC` count would incorrectly
report 8,227 entries. Overlay functions sharing a guest address remain separate
entries, and positive-sized aliases are reported rather than silently merged.
No positive-sized alias duplicates were found in this pinned inventory.

Two retained routines have different ELF size metadata: `func_8003F6E8_402E8`
is 48 bytes in baseline and 56 in the mixed build, and `func_8000D3B8_DFB8`
is 64 bytes in baseline and 72 in the mixed build. The extra extent covers its
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

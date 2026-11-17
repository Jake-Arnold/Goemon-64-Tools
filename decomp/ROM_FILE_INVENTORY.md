# ROM file-size inventory (USA and Japanese rev-0)

`decomp/data/rom_file_inventory.csv` is a **read-only, non-copyrighted metadata index** of all **1,311 numbered file slots** in each retail ROM (including **227 empty slots** and **1,084 populated slots**). It records original cartridge offsets and stored sizes, expanded-ROM offsets and sizes, compression status and Japan-minus-USA differences. The index is for rapid lookup; it contains no extracted ROM payload, disassembly or game assets.

The file IDs come from the `Nisitenma-Ichigo` 32-bit file table parsed by pinned upstream `tools/rommy.py`. The first 31 bits are a ROM address and bit 31 is the LZKN64 indicator. A file's **stored size** is the difference between consecutive table offsets. An **expanded size** is the length of the file after LZKN64 decompression, or the original size for raw files. Expanded offsets are calculated cumulatively from the first file position, not by applying the USA-to-Japan RAM-address crosswalk. Both ROMs must match their pinned SHA-1 identities to generate the CSV.

The `Segment classification` field comes from the pinned Splat extraction layout: files 11–23 are static code overlays, files 24–80 are TLB code overlays and remaining populated files are **opaque binary/data** (not evidence that they are all graphics). A zero-byte slot is `Empty slot`. ROM positions differ from guest-RAM VMAs; overlay modules can share a load address and do not stay resident together.

## Lookup

```bash
# Lookup without ROMs, toolchains or Python:
grep '^file_12,' decomp/data/rom_file_inventory.csv

# Evidence-backed, manually updated known functions:
cat decomp/data/rom_file_semantics.json
```

## Regeneration / drift check

Use the Python environment from `GOEMON_BUILD_ENVIRONMENT.md` (the pinned `lzkn64` package is required). The supplied JP `.n64` is byte-swapped and is normalized in memory before checking its SHA-1.

```bash
python3 -m decomp.rom_file_inventory \
  --usa-rom '/path/to/Mystical Ninja Starring Goemon (USA).z64' \
  --japan-rom '/path/to/Ganbare Goemon - Neo Momoyama Bakufu no Odori (Japan).n64' \
  --check

# Deliberate regeneration when verified source data changes:
python3 -m decomp.rom_file_inventory \
  --usa-rom '/path/to/USA.z64' --japan-rom '/path/to/JP.n64' \
  --output decomp/data/rom_file_inventory.csv
```

Reference source hashes:

| Input | SHA-1 |
| --- | --- |
| USA retail z64 | `df8083a54296b8c151917c5333e1c85f014a2a66` |
| JP rev-0 normalized z64 | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` |
| Original 32 MiB USA expanded ROM | `6ea0ed71032ce08fc2745f412d84936382197494` |
| Original 32 MiB JP expanded ROM | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` |

`decomp/data/rom_file_inventory.schema.json` describes CSV columns and types; CSV integers are decimal strings. `decomp/data/rom_file_semantics.json` is a separate, manually maintained, evidence-linked partial catalogue. Missing entries have unknown function; speculative leads are distinguished from established interpretations. The numeric inventory changes only if verified extraction facts change. This catalogue can evolve independently of matching-C counts.

This index does not change the decomp manifest, matching-C ownership, saved-game fields, runtime toolkit or full-ROM verification result.

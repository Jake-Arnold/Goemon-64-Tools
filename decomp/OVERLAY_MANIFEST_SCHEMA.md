# Overlay manifest schema (research contract)

`overlay_manifest.py` validates explicit overlay mappings and provenance. It is
not wired into `decomp.verify`, does not validate the ROM bytes against hashes,
and does not authorize a function promotion. A future linked-ELF adapter must
independently verify the segment, section, symbol, relocation, and full-ROM data.

## Mapping rules

- `reference_rom_sha1` identifies the exact reference image. Each file-backed
  section and function carries SHA-256 evidence fields.
- Every overlay declares its own ROM and VMA half-open ranges, alignment, and
  exclusive RAM identifier. There is deliberately no main-segment
  `rom_to_vma_offset` formula.
- File-backed `text`, `rodata`, and `data` sections declare explicit ROM/VMA
  ranges of equal size, section alignment, and a SHA-256. A `bss` section has
  only a VMA range and alignment because it occupies no ROM bytes.
- Sections must fit inside their overlay. ROM ranges and VMA ranges are checked
  independently for overlap, including across overlays. Overlay VMA reuse is
  rejected by this schema even if overlays might be mutually exclusive; any
  future relaxation needs explicit loader/exclusivity evidence and tests.
- Functions must be aligned, nonempty, lie wholly inside a `text` section, and
  have a name whose encoded VMA and ROM offset agree with the explicit fields.
  Function ROM ranges and VMA ranges are independently checked for overlap.
- `source_owner` is a repository-relative path without traversal components.
  Source, object, relocation, and original-code SHA-256 values must be present.

## Validation

Run the schema checks with:

```sh
python3 -m unittest decomp.test_overlay_manifest -v
```

The fixtures cover independent ROM/VMA mappings, the forbidden main-segment
formula, unknown fields, duplicate IDs, negative and mismatched ranges,
section/function overlap in either address space, file-free BSS, and unsafe or
missing provenance. Passing these tests means only that the declared metadata
is internally consistent; it is not original-binary or whole-ROM proof.

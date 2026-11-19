# Japanese warp-adjacent matching-C research — 2026-11-16

**Status: isolated exact matches, research only. Not promoted to production.**

Six previously ASM-owned functions match the original Japanese rev-0 code at their original RAM addresses using the pinned upstream `mnsg` source, native IDO 5.3 (`-O2 -mips2 -G 0 -non_shared`), GNU MIPS linker and explicit original symbol addresses. Source/object/relocation checks were made against the SHA-1-pinned decompressed Japanese cartridge. No original ROM bytes are committed.

| ROM offset | Function | Bytes | IDO zero tail | Relocations | Behaviour |
|---|---|---:|---:|---:|---|
| `0x37958` | `func_80036D58_37958` | 204 | 4 | 7 | Capture three position coordinates and area index, then call scene effect |
| `0x37A24` | `func_80036E24_37A24` | 208 | 0 | 7 | Coordinate sibling with different call parameters |
| `0x37AF4` | `func_80036EF4_37AF4` | 100 | 12 | 2 | Accept state values 1/2; write warp flag and location |
| `0x37B8C` | `func_80036F8C_37B8C` | 192 | 0 | 5 | Copy six fields from 12-byte-stride warp records |
| `0x37D5C` | `func_8003715C_37D5C` | 92 | 4 | 5 | Conditional transition 14 or current-to-next location transfer and transition 12 |
| `0x37EEC` | `func_800372EC_37EEC` | 52 | 12 | 2 | Compare two system-location halfwords |

**New isolated exact matches:** six functions, 848 bytes, 28 relocations. Existing formal Japanese baseline stays at 18 C functions / 756 bytes. **24 / 1,604 is a potential total, not a production achievement.**

The reproducible Python IDO/GNU MIPS harness and six ROM-free negative-control tests were executed locally (6/6 native functions, 6/6 guard tests) and included in the source archive `goemon-japan-six-adjacent-probes.zip` delivered in the conversation. All source files are now also recorded under `decomp/japan_adjacent_probes/`. These C sources are intentionally not named `japan_matching` or linked into production.

For formal promotion: extend `decomp/japan_eighteen_c.py` to stage 24 functions; validate native source hashes, symbol placement, relocation records, 4/12/4/12 byte tail repairs, generated ASM tail handling and ELF ownership; then require exact 32 MiB linked and exact 16 MiB Rommy retail images. Keep ASM placeholders upon any mismatch.

Further neighbours remain assembly-owned: `func_800371B8_37DB8` (308 bytes), `func_80037320_37F20` (324), `func_80037464_38064` (468). No emulator, native PC-port or gameplay tests were performed.

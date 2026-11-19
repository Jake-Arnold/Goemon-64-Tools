# Japanese 24-C matching build — 16 November 2026

**Verified:** 24 original-address native matching-C functions, 1,604 original machine-code bytes, 20 C translation units. Six warp-neighbour functions promoted from isolated research after complete source-linked Japanese ROM proof.

| Proof | Result |
|---|---|
| Native compiler/linker | Pinned IDO 5.3, GNU MIPS, Japanese Splat |
| Expanded 32 MiB SHA-1 | `6f8745fecc3a5e7d4918c7a73353eb0726116ded` / 0 different bytes |
| Retail 16 MiB SHA-1 | `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b` / 0 different bytes |
| C symbol count / code bytes | 24 / 1,604 |
| Translation units | 20 |
| ELF positive-sized game functions | 7,376 |
| ASM-marked entries | 7,352 |
| ELF game-code sections | 73 |
| Unexpected unmarked game functions | 0 |
| Isolated research negative-control tests | 6 / 6 pass |
| Japanese emulator / PC-native runtime | NOT RUN |

Build in a **fresh** pinned `klorfmorf/mnsg` checkout:

```bash
bash decomp/build_japan_twentyfour_c.sh /path/to/fresh-pinned-mnsg /path/to/goemon-dependencies /path/to/goemon-runtime-additions
```

The staged split preserves 20 reviewed Japanese C translation units and all remaining assembly. Four of the six added C objects have 4/12-byte zero-only padding; generated assembly slice `main_37DB8.s.o` contains 12 bytes of zero padding. The original eight C object guards are preserved. The ELF32 metadata adapter fails closed on nonzero tails, symbol extents and relocations, and changes no compiled instructions. The complete linked and recompressed ROM images, source SHA-256 checks, relocation signatures, original linker VMAs and final ELF ownership are independent acceptance gates.

The separate 18-C scripts and manifests remain available for baseline regression. No ROM, extracted assembly, assets or object files are committed.

**Next neighbours:** `func_800377C4_383C4` (36 bytes), `func_8003787C_3847C` (20) and `func_8003790C_3850C` (20) have exact isolated original-address IDO/GNU MIPS instruction matches but **not** full-ROM proof. The `func_80037780_38380` 68-byte C attempt compiled to 64 bytes and differs starting at +0x18. 308-, 324- and 468-byte neighbours remain assembly-owned.

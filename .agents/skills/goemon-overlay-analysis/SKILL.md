---
name: goemon-overlay-analysis
description: "Use for Goemon N64 overlays, file_43 ROM/VMA mapping, ELF sections, rodata, key and Ghost Toys reconstruction."
---

# goemon-overlay-analysis

Read `overlay_file43.py`, its tests and phase 06. file_43 spans ROM `0x6F34E0..0x6FB200` and VMA starts `0x08000000`; never reuse main-segment offset mapping. Verify overlay identity, linked original-address ELF, text/rodata, relocation records, padding, extents and hashes. Add overlap/shift negative tests. Isolated key and Ghost functions remain research until full overlay/ROM proof.

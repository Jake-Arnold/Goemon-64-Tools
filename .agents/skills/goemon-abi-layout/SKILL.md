---
name: goemon-abi-layout
description: "Use to recover Goemon o32 ABI, original struct offsets, signedness, endian widths, aliasing and callback-mutated pointers."
---

# goemon-abi-layout

Inspect original MIPS accesses, callers and `decomp/script_vm.h` / `decomp/object_flags.h`. Record offset, width, signedness, native instruction and confidence. Prefer opaque fields over unsupported types. Distinguish immutable entry resource ID from live global values changed by callbacks. Add offsetof, endian and sentinel tests; host layout alone cannot establish native IDO instruction equivalence.

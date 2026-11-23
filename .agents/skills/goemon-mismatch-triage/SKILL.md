---
name: goemon-mismatch-triage
description: "Use to diagnose near-matching compiler code with register, delay-slot, relocation, section, rodata or entire-unit scheduling mismatches."
---

# goemon-mismatch-triage

Find the **first** original ROM difference. Compare original/candidate symbol length, VMA, instruction bytes, HI16/LO16 relocations, stack saves and adjacent siblings. Classify root cause before testing a single source-level remedy. The previously mismatched object dispatcher is already promoted; do not repeat stale investigation. Store a small mismatch table, not full disassembly in model context. Approximate matching is research only.

Before testing variants, read `decomp/COMPILER_QUIRKS.md`, identify verified behaviours and classify the first mismatch. Record a per-native-attempt quirk outcome even for a negative or no-new-finding result, with original/generated instruction/relocation differences, exact flags, source SHA-256, commands and controlled experiments. Independently reproduce any supposed cross-function quirk.

---
name: goemon-mismatch-triage
description: "Use to diagnose near-matching compiler code with register, delay-slot, relocation, section, rodata or entire-unit scheduling mismatches."
---

# goemon-mismatch-triage

Find the **first** original ROM difference. Compare original/candidate symbol length, VMA, instruction bytes, HI16/LO16 relocations, stack saves and adjacent siblings. Classify root cause before testing a single source-level remedy. The previously mismatched object dispatcher is already promoted; do not repeat stale investigation. Store a small mismatch table, not full disassembly in model context. Approximate matching is research only.

---
name: goemon-unit-promotion
description: "Use to integrate a researched Goemon C candidate into its production source and replace exactly one GLOBAL_ASM ownership claim."
---

# goemon-unit-promotion

Confirm target isn't already C in live manifest. Preserve original translation-unit order, retained ASM neighbors, section alignment and rodata. Compile and compare the **whole** source unit with pinned IDO; check every existing matched sibling. On any mismatch, keep ASM and mark RESEARCH_ONLY. Update manifest and official count only after complete-ROM and symbol-inventory gates. Follow `decomp/plans/EXECUTOR_PROTOCOL.md`.

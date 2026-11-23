---
name: goemon-ido-codegen
description: "Use to refine Goemon C syntax so native IDO 5.3 generates the original register allocation, stack frame, branches and instruction order."
---

# goemon-ido-codegen

Compile with pinned IDO using real source unit and flags (usually `-O2 -mips2 -G 0 -non_shared`); compare linked code at original VMA. Change one justified source hypothesis at a time: signedness, variable lifetime, aliasing, volatile use or control flow. Keep side effects and sibling functions. Log first mismatch, size, relocations, source hash and attempted variant. No raw instruction patches or relaxed comparator.

**Required per attempt:** read `decomp/COMPILER_QUIRKS.md` before native compilation, classify the first mismatch before variants, test relevant verified workarounds with bounded one-variable controls. Save one of four required quirk outcomes, original/generated instruction and relocation differences, exact flags, source SHA-256, commands and failed controls. Do not assume cross-function applicability.

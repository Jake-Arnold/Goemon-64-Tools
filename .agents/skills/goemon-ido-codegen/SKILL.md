---
name: goemon-ido-codegen
description: "Use to refine Goemon C syntax so native IDO 5.3 generates the original register allocation, stack frame, branches and instruction order."
---

# goemon-ido-codegen

Compile with pinned IDO using real source unit and flags (usually `-O2 -mips2 -G 0 -non_shared`); compare linked code at original VMA. Change one justified source hypothesis at a time: signedness, variable lifetime, aliasing, volatile use or control flow. Keep side effects and sibling functions. Log first mismatch, size, relocations, source hash and attempted variant. No raw instruction patches or relaxed comparator.

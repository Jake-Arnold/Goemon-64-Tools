---
name: goemon-evidence-publish
description: "Use after any Goemon matching-C task to write a truthful evidence ledger, update progress, commit and verify remote branch state."
---

# goemon-evidence-publish

Read root `AGENTS.md`, `decomp/CONTINUE.md`, executor protocol and prior `plans/execution` record. Include task ID, starting SHA, source hashes, tests actually executed, original extent, first mismatch and fresh G2 status. Use PASSED_G2, RESEARCH_ONLY, FAILED_NATIVE, BLOCKED_INPUT or DOC_ONLY. Update `PROGRESS.md` in same commit and continuation when next task changes. Exclude ROM/ELF/toolchains/private diagnostics, never force-push or touch main, confirm remote HEAD.

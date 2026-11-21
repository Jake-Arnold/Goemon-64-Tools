---
name: goemon-task-registry
description: "Use for pending Goemon tasks, cross-chat pause/resume/checkpoints, blocked work and conflicting native-C batches."
---

# Goemon persistent task registry (primary intake)

For pending lists, "what's next", `GQ-...` resume or checkpoint requests:

1. Read `AGENTS.md`, `decomp/tasks/README.md`, `decomp/tasks/registry.json` and `decomp/CONTINUE.md`. Fetch the live `chatgptweb/decomp` HEAD. The retired G64-001..100 plan is historical, not the active queue.
2. In a complete checkout use `python3 -m decomp.task_registry list` or `resume GQ-...`; otherwise read the current JSON through GitHub. Sort by priority/ID and **include blocked tasks**. For a selected task inspect the complete record and linked GitHub issues/PRs.
3. Reconcile each task's recorded HEAD, accepted original functions and open PRs before acting. Deduplicate by region, original ROM offset and source owner. Check prerequisites, proof tier, failures and blockers. Research independently while awaiting external gameplay evidence; never invent results.
4. For original C, follow `goemon-autonomous-decomp` and relevant native-MIPS/IDO skills. Require authentic IDO, exact 32 MiB ROM, ELF/semantic relocations, strict inventory and full `decomp.local_ci`. Isolated exact C is **not** a promotion. Never change `main`.
5. At handoff, record actual outcomes, negative trials, provenance, tests, blockers, next steps and evidence. Commit registry plus `PROGRESS.md` (and relevant docs) on `chatgptweb/decomp`, then re-fetch the remote ref. The guarded checkpoint CLI only edits local JSON; it does not commit/push or prove G2.

For a list-only request, do not start compilation or gameplay. Never publish ROMs, original ASM/ELF, game assets, memory dumps, savestates, credentials or proprietary toolchains.

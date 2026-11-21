---
name: goemon-task-registry
description: "Use whenever asked to list pending Goemon tasks, pause or resume work across chats, choose a blocked versus runnable task, or reconcile competing native-C promotion batches."
---

# Goemon persistent task registry (primary intake)

On **any** request containing "pending tasks", "what's next", "task list", "continue GQ-", "resume Goemon", "checkpoint this", or "stop/pause this research", begin with:

1. Read `AGENTS.md`, `decomp/tasks/README.md`, `decomp/tasks/registry.json`, and the latest `decomp/CONTINUE.md`. Fetch live `chatgptweb/decomp` HEAD. **Do not** treat the retired G64-001..100 JSON plan as the active queue.
2. Run `python3 -m decomp.task_registry list` if the checkout is present; otherwise read the JSON with the GitHub connector and sort by priority, then ID. Include **blocked** tasks in the user-facing queue. For selected task, run `python3 -m decomp.task_registry resume GQ-ID` or read its full record and referenced GitHub Issue/PR.
3. Before executing a task, reconcile its `last_reviewed` and registry `reconciled_head` against current accepted functions and open PRs. Resolve conflicts by original region, ROM offset and source owner; no double promotions. Check prerequisites, `proof_tier`, prior errors and held state. Perform bounded independent work if waiting on live tests; do not fabricate unavailable gameplay input.
4. For C work, load the existing `goemon-autonomous-decomp` or narrow original-MIPS/IDO/full-ROM skill. Apply original IDO toolchain, 32 MiB whole-ROM, ELF semantic relocations, inventory and full `decomp.local_ci` acceptance gates. Do not touch `main`.
5. At pause/finish, checkpoint exact verified outcomes, failed hypotheses, source/ROM provenance, tests actually executed, blocker, next action and evidence links. Update registry, `PROGRESS.md`, and relevant docs in one commit/PR to `chatgptweb/decomp` and verify remote branch; **do not mark done merely because a C source matched in isolation.** The CLI's checkpoint changes local JSON only.

If the user only asks what is pending, **do not launch compilation or gameplay experiments**; show a concise sorted registry view. If they select a task, resume within actually available inputs and report status accurately. Never upload ROMs, extracted ASM/ELF, game saves, raw memory dumps, credentials, or proprietary toolchains.
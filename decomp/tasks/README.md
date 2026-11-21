# Goemon resumable work queue

**Entry point for new conversations and agents:** `AGENTS.md` -> this file -> `decomp/tasks/registry.json` -> the selected task's GitHub evidence. The registry is a curated, living handoff, not the archived G64-001..100 plan, a complete issue index or a new C-acceptance ledger.

```bash
python3 -m decomp.task_registry list                 # all pending / externally blocked work
python3 -m decomp.task_registry list --status pending
python3 -m decomp.task_registry list --region japan_0
python3 -m decomp.task_registry show GQ-CRIGHT-001
python3 -m decomp.task_registry resume GQ-USA-001    # full handoff and safety gates
python3 -m decomp.task_registry validate
```

When the user says **"which tasks are pending?"**, **"continue the Goemon backlog"**, or **"resume GQ-..."**, use this registry before consulting the historical 100-task plan. Do not silently hide `blocked_external`, `blocked_input`, `blocked_rebase`, or `blocked_verification` tasks; the user needs to know what cannot be executed remotely. Output the priority, status, blocker, conflicts and next actionable step. For a named ID, show its actual handoff and execute only within the available tool and evidence limits; do not claim mock tests are gameplay, or native isolated exactness is full ROM verification.

## Script artifact upload requirement

For every task that references a runnable script, Project64 hook, verifier, comparator or script kit, **upload its actual source-only files or ZIP to the user in the same task handoff**, with a verified downloadable artifact link, complete dependencies and a run command. Filename-only mentions, checksums and attachments from older chats are insufficient; do not describe a script as available solely because a previous conversation once contained it. Safe repository-hosted source may also be checked in for persistence, but does not replace delivery of the requested artifact. Never include ROM/game-asset bytes, proprietary compilers, savestates or personal memory dumps. If the artifact is unavailable, mark the missing script as a `blocked_input` blocker rather than implying the task is executable. This policy applies to future deliveries, including continuations of existing GQ tasks.

## End-of-session pause / checkpoint protocol

1. Re-fetch `chatgptweb/decomp` HEAD, current issues/PRs, all accepted original-ROM offset sets, and the task's references. Historical task `last_reviewed` and `reconciled_head` are **snapshots**, never automatic claims that a later promotion has not happened. Reconcile and remove/supersede completed work rather than duplicate it.
2. Record a compact, **complete handoff for the work actually investigated**: objective, region/revision, original offsets/VMAs, evidence links and test commands/results, first native mismatch or full-ROM proof, false hypotheses, outstanding blockers, precise next command/experiment, ownership/conflicting PRs and acceptance criteria. Keep confidential ROM/ASM/savestate/trace bytes out of Git. Refer to them by hash and safe provenance.
3. Use a guarded checkpoint before committing a note:
   ```bash
   python3 -m decomp.task_registry fingerprint
   python3 -m decomp.task_registry checkpoint GQ-CRIGHT-001 \
     --status blocked_external \
     --note 'Awaiting paired Project64 traces; no live allocator call observed' \
     --next-step 'Capture normal and held trial from same savestate' \
     --evidence 'https://github.com/Jake-Arnold/Goemon-64-Tools/issues/95' \
     --expected-sha256 '<paste exact fingerprint>'
   ```
   This only edits local JSON. It **does not** make a Git commit, push or validate gameplay/G2. When acceptance is verified, manually set `completion_proof` to the real proof/commit and `status=done` in a reviewed commit. The CLI deliberately refuses to mark tasks done.
4. Update `PROGRESS.md` in the **same commit** as any changed registry, code, research or documentation. Update `decomp/CONTINUE.md` for newly verified C / major operational changes. Push only to `chatgptweb/decomp` after PR review/merge, verify remote SHA and task contents. Do not force-push or touch `main`.
5. If the task is blocked, save the blocker and move to a genuinely independent task. Preserve source and accepted-count provenance. Never create synthetic success records or invent a native ROM gate.

## Promotion conflict and stale-proof safeguards

- `conflicts_with` denotes **potential shared original functions, source owners or publication artifacts**, not a permanent dependency preventing independent research. Two independently native-exact batches can each work, but must not simultaneously publish replacements for the same original ASM owner or shared `combined.json` / inventories.
- Before every promotion, compare original **region + ROM offset + actual source/overlay owner** against current accepted functions and every open pending batch/PR. A candidate in `ISOLATED_EXACT`, `FAILED_NATIVE`, `FAILED_ROM`, `RESEARCH_ONLY`, `PASSED_G2_LOCAL`, or an old issue is not a new accepted function. Only complete native G2 + ELF/relocation + strict inventory + full local CI + remote publication permits `done`/accepted increment.
- Prefer a topic branch and PR for task registry and queued changes. Rebase onto the latest `chatgptweb/decomp` after other merges. If a conflict changes a C owner's original byte/relocation input, **invalidate and rerun the relevant native proofs**; do not combine stale `PASSED_G2_LOCAL` reports arithmetically.
- [PR #149](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/149) (retired G64-001–100 task machinery), [PR #150](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/150) (historical docs), and [PR #153](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/153) (short operational continuation and proof retention audit) are **merged** into `chatgptweb/decomp`. Their original contents and provenance remain archived; they are not pending tasks. The registry has **11 active + 2 completed maintenance** records as of 21 November 2026. Keep this queue independent of the retired plan and preserve discoverability links.

## C-Right live instrumentation

The ROM-independent trace comparator and complete read-only protocol are checked in under [`decomp/tasks/cright_live_trace/`](cright_live_trace/README.md). The Project64 recorder scripts from the original user conversation embed original-game opcode signatures and are **not** committed; use the user-supplied trace-kit ZIP locally. The originating kit's mock tests passed, but are not gameplay evidence. Task `GQ-CRIGHT-001` remains blocked on a real paired Japanese savestate replay. The primary discriminators are `0x802125A0` (held gate), `0x8021BF44` (resolver call), and `0x8021BFBC` (allocator `$a0` argument). See issue #95 for original-ROM research and limitations.

The CLI and registry are ROM-free. Their test entrypoint is:

```bash
python3 -m unittest decomp.test_task_registry -v
```

Both `python3 -m decomp.local_ci` and `--quick` now include registry validation and the C-Right comparator cases; the full command additionally runs the configured original-C host sanitizers. No ROM-free CI run proves native original-ROM matching or gameplay.
## Bomb Text Skip first-bomb Project64 live trace — GQ-VM-001

[Dedicated read-only handoff](bomb_text_skip_live_trace/README.md) records the authentic Japanese first-bomb normal-vs-one-frame-Start procedure. The task is `blocked_external` until the user can manually operate Windows Project64 3.x. The full self-contained source-only recorder/comparator ZIP is delivered in the user's Project conversation as `Goemon_Bomb_Text_Skip_Project64_Trace_Kit_2026-11-21.zip` (SHA-256 `0de4a714b96cbf6158596e236ac72b4033e50653f95180a58ffc6a87e7f3e933`); do not commit its region-specific script instruction signatures or any real JSONL, ROM or savestate. The kit contains two read-only JSONL recorders, a fail-closed paired comparator, manual checklist and synthetic Node/Python tests. Real first-bomb actor/input/VM timing is **not yet observed**; no new matching-C promotions.

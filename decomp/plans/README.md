# Decomp verification protocol and historical evidence

The fixed **G64-001–100 execution plan was closed on 14 November 2026**. Its stale task active catalogue and ten phase packets have been removed from the planning root. The complete original `TASKS_100.json` remains in [`decomp/history/TASKS_100.json`](../history/TASKS_100.json) for the reproducible historical audit; the original architecture and phase packets remain recoverable from Git history, but **must not be used as a live remaining-function or blocker inventory**.

## Current source of truth

- [Live continuation](../CONTINUE.md) — working targets, verified results and region-specific handoff.
- [Canonical USA proof](../results/combined.json) and [inventory](../results/inventory.json) — the published combined-ROM checkpoint; later G2 acceptance reports and [PROGRESS.md](../../PROGRESS.md) may supersede its count.
- [Executor protocol](EXECUTOR_PROTOCOL.md) — function-level original-address, IDO, relocation, full-ROM G2 and publication gates.
- [Candidate promotion](../CANDIDATE_PROMOTION.md), [batch workflow](../BATCH_PIPELINE.md) and existing original-source research — target selection and reproducible evidence.
- `python3 -m decomp.skill_context --status` — compact published canonical proof/inventory snapshot; `--validate` — ROM-free consistency gate.

## Historical material retained

- [Per-task execution evidence](execution/) — dated G64 research attempts, native mismatches, useful trace facts and previously accepted proof.
- [Architect v2 strategy](EXECUTION_STRATEGY_V2.md) — explicitly closed historical strategy, not current scheduling policy.
- [Architect v3 pilot](ARCHITECT_V3_PILOT.md) and [optional REA pilot](REA_PILOT.md) — independent historical research and optional analysis reference.
- [Archived G64-001–100 data](../history/TASKS_100.json) is retained only as historical input for [the research audit](../research/historical_audit_20261117/audit.py); Git history retains the deleted original architecture and phase packet documents.

No original-ROM G2 matching-C claims, assembly ownership, native build inputs, or existing per-task research evidence are changed by the plan retirement.

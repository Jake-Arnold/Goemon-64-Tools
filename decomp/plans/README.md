# Matching-C execution architecture — 100-step plan

**Document type:** executor-grade implementation specification; no implementation claimed. **Target branch:** `chatgptweb/decomp`. Baseline reviewed at `a68881da4b10e2553e7a89b7129d09d64b427435` on 2026-11-11. Refresh live HEAD/manifest before executing any work.

**Read in this order:** root `AGENTS.md`; `decomp/CONTINUE.md`; [EXECUTOR_PROTOCOL.md](EXECUTOR_PROTOCOL.md); [ARCHITECTURE_100.md](ARCHITECTURE_100.md); the chosen phase; then the targeted source files. A weaker model must not infer missing information: use explicit BLOCKED_INPUT or RESEARCH_ONLY outcomes.

## Phase packets
- [01 — Baseline and near-ready promotions](phases/PHASE_01.md) (G64-001–G64-010)
- [02 — Object scheduling and short routines](phases/PHASE_02.md) (G64-011–G64-020)
- [03 — VM resource path](phases/PHASE_03.md) (G64-021–G64-030)
- [04 — VM parser and text loop](phases/PHASE_04.md) (G64-031–G64-040)
- [05 — VM graphics and formatting](phases/PHASE_05.md) (G64-041–G64-050)
- [06 — Overlays and file_43](phases/PHASE_06.md) (G64-051–G64-060)
- [07 — State transitions](phases/PHASE_07.md) (G64-061–G64-070)
- [08 — File/object/scheduler](phases/PHASE_08.md) (G64-071–G64-080)
- [09 — Math and adjacent units](phases/PHASE_09.md) (G64-081–G64-090)
- [10 — Proof automation and camera](phases/PHASE_10.md) (G64-091–G64-100)

## Machine-readable documents
- [TASKS_100.json](TASKS_100.json): 100 structured packets, exact files, dependencies, procedure, negative controls, acceptance, evidence and stop conditions. Task state defaults PLANNED and does not assert execution.
- [ARCHITECTURE_100.md](ARCHITECTURE_100.md): original comprehensive architecture, branch baseline, gates, dependency graph, risk register and compact 100-task overview.

## Default execution order
1. First complete independent near-ready resource wrappers and menu trio (G64-001–010). Their full-unit research match is known, but G2 whole-ROM proof is not.
2. Object dispatcher G64-011–014 is blocked by native full-unit scheduling. Do not delay unrelated work indefinitely.
3. Select next function by evidence/dependencies, not numeric order. VM resources and overlay verification are independent lanes after baseline safety.
4. At every phase boundary run G64-099 rebaseline. Live manifest/results override this plan's historical numeric assumptions.
5. When a phase is blocked, update the task ledger with exact failure evidence and proceed to an independent work unit; leave ASM intact.

**Current authoritative published matching claim:** 142 reconstructed C / 10,652 bytes, 155 total C, 7,221 ASM / 7,376 identified. Conditional initial milestones: resource pair 144/10,724; menu trio 147/10,972; object 148/11,020; four short additional functions 152/11,180. These are not current claims. Neither a successful host test, isolated match, a correct function size, nor a published plan can increase the counts.

**Publication boundary:** No proprietary ROM, asset, generated assembly, binary, private memory, or user-specific path enters this branch. No changes to main, no force-push.

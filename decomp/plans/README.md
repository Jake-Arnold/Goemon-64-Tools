# Matching-C execution architecture — 100-step plan

**Document type:** executor-grade implementation specification; no implementation claimed. **Target branch:** `chatgptweb/decomp`. Baseline reviewed at `a68881da4b10e2553e7a89b7129d09d64b427435` on 2026-11-11. Refresh live HEAD/manifest before executing any work.

**Read in this order:** root `AGENTS.md`; [EXECUTION_STRATEGY_V2.md](EXECUTION_STRATEGY_V2.md); [EXECUTOR_PROTOCOL.md](EXECUTOR_PROTOCOL.md); live proof/CONTINUE, then a compact task brief and **only its phase/focus files**. The full architecture is reference, not an every-task preamble.

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


## Optional REA / Ghidra pilot (not a prerequisite for any of the 100 tasks)

- [REA_PILOT.md](REA_PILOT.md): four gated experiments, source-backed MIPS compatibility audit, exact commands, ten-function control benchmark, VM lookup study, GO/NO_GO decision.
- [REA_PILOT_CONTROLS.json](REA_PILOT_CONTROLS.json): ten independently accepted C functions with manifest-derived original offsets, guest addresses and extents.
- [REA_PILOT_TASKS.json](REA_PILOT_TASKS.json): machine-readable R01–R04 experiments and acceptance/stop conditions.
- `python3 -m unittest decomp.test_rea_pilot_preflight -v` checks the conservative local ELF admission helper with synthetic inputs.

**Major compatibility warning:** pinned Goemon builds use `-mips2`, while REA's documented Ghidra ELF-MIPS admission does not include MIPS-II. Real Goemon `.elf` flags remain uninspected here. No REA analysis on a proprietary target has been run. A read-only direct-Ghidra investigation is the fallback only when the target mapping is independently verified; m2c/IDO + complete-ROM verification are unchanged. Optional research must never block the existing five near-ready promotions.

## Low-token Codex skills

20 targeted skills are indexed at [`.agents/skills/`](../../.agents/skills/README.md). `python3 -m decomp.skill_context --status` and `--task G64-NNN` load compact current task summaries, not the full ~340 KB plan. Validate with `python3 -m unittest decomp.test_skill_context decomp.test_codex_skills -v`. Read only the needed skill; the G2 proof gate is unchanged.

## Architect v2 — revised execution priority

The [current strategy](EXECUTION_STRATEGY_V2.md) supersedes strictly numeric execution. Each pending machine-readable task has an `architect_override_v2` returned by `decomp.skill_context --task`. G64-035 through G64-040, G64-091 and G64-090 are `RESEARCH_ONLY`; `decomp.skill_context --status` reports the lowest-numbered PLANNED ID (G64-041), while the reviewed v2 execution order proceeds to G64-071–080 after the completed G64-090 audit. Preserve task IDs, completed statuses and exact G2. The original numeric notes below are historical, not a fresh result.

## Historical numeric progression
1. G64-001–014 have recorded outcomes: the resource wrappers, menu trio and object dispatcher passed G2; G64-003 was already complete.
2. G64-015–018 were retried and marked `FAILED_NATIVE`; no production ASM ownership changed. G64-019 is `RESEARCH_ONLY`, and G64-020 documents the hard stops.
3. G64-021 is `DOC_ONLY`; G64-022–030 are `RESEARCH_ONLY`: G64-023 reproduced the F038 baseline, G64-024's three variants did not improve it, G64-025's callback mutation model passed, G64-026 pinned the loader frame while its candidate remained nonmatching, G64-027 traced D68C with a ROM-bound guard, G64-028 traced DF98 and its callers with a ROM-bound dispatch guard, G64-029 added a passing DDC4 retry/entry-ID guard with a cached-global negative control, and G64-030 reconciled the live VM proof and inventory and added a typed interface matrix. G64-031 added a ROM-bound DBEC text-loop CFG and addressing guard; G64-032 compared the 0x48/0x50 frame and five source-lifetime variants without a match; G64-033 expanded its MIPS/host differential harness, passed 20,000 seeded cases and killed four targeted mutants; G64-034 recovered DE80's signed token/control-flow graph and corrected the stale 228-byte IDO result; G64-035 tried four bounded DE80 code shapes, rejected a size-only 232-byte function with the wrong frame, and stopped after register-lifetime codegen regressed; G64-036 reconciled all original-observed wrapper paths with G64-034's tests and guard, without inventing gate-helper side effects. No new C candidate passed G2; keep unresolved helpers as ASM. G64-037 pinned and traced the 592-byte ED60 handler and its caller, then retained ASM after one exact-IDO probe first differed at `0x8003ED68`. G64-038 verified the 48-byte `func_8003F6E8_402E8` original extent and its two trailing return pairs; the 40-byte C prefix and 56-byte candidate annotation are not original boundaries. G64-039 added expected fixed DBEC MIPS traces and EB34 callback-order assertions, then composed existing DE80, DF98, ED60 and F6E8 evidence in `VM_PARSER_BEHAVIOR_MATRIX.md`; opaque helper effects remain unknown. G64-040 found no new source-unit-exact parser candidate: EB34 is already in matching C and the remaining reviewed targets stay ASM-owned. G64-091 added an immutable attempt ledger to the persistent batch queue, preserving historical reports and keeping isolated matches below G2. G64-090 audited all 13 `return_zero.c` placeholders against their exact original extents and behavior; each is a nontrivial Memory Pak/PFS routine, so all remain `GLOBAL_ASM`. See `plans/execution/2026-11-11-g64-090-return-zero-audit.json`. Proceed to G64-071–080 under v2.
4. At every phase boundary run G64-099 rebaseline. Live manifest/results override this plan's historical numeric assumptions.
5. When a phase is blocked, update the task ledger with exact failure evidence and proceed to an independent work unit; leave ASM intact.

**Current authoritative published matching claim (2026-11-11):** 148 reconstructed C / 11,020 matched bytes, 161 total C, 7,215 ASM / 7,376 identified entries. The six resource, menu and object functions passed integrated native-unit and full-ROM gates; `results/combined.json` records the exact 33,554,432-byte image comparison. The four short additional functions remain unpromoted after bounded native retries. Neither a host test, isolated match, correct function size, nor plan status can increase the counts.

**Publication boundary:** No proprietary ROM, asset, generated assembly, binary, private memory, or user-specific path enters this branch. No changes to main, no force-push.

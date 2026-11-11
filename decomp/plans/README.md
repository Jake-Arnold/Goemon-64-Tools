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


## Optional REA / Ghidra pilot (not a prerequisite for any of the 100 tasks)

- [REA_PILOT.md](REA_PILOT.md): four gated experiments, source-backed MIPS compatibility audit, exact commands, ten-function control benchmark, VM lookup study, GO/NO_GO decision.
- [REA_PILOT_CONTROLS.json](REA_PILOT_CONTROLS.json): ten independently accepted C functions with manifest-derived original offsets, guest addresses and extents.
- [REA_PILOT_TASKS.json](REA_PILOT_TASKS.json): machine-readable R01–R04 experiments and acceptance/stop conditions.
- `python3 -m unittest decomp.test_rea_pilot_preflight -v` checks the conservative local ELF admission helper with synthetic inputs.

**Major compatibility warning:** pinned Goemon builds use `-mips2`, while REA's documented Ghidra ELF-MIPS admission does not include MIPS-II. Real Goemon `.elf` flags remain uninspected here. No REA analysis on a proprietary target has been run. A read-only direct-Ghidra investigation is the fallback only when the target mapping is independently verified; m2c/IDO + complete-ROM verification are unchanged. Optional research must never block the existing five near-ready promotions.

## Default execution order
1. G64-001–014 have recorded outcomes: the resource wrappers, menu trio and object dispatcher passed G2; G64-003 was already complete.
2. G64-015–018 were retried and marked `FAILED_NATIVE`; no production ASM ownership changed. G64-019 is `RESEARCH_ONLY`, and G64-020 documents the hard stops.
3. G64-021 is `DOC_ONLY`; G64-022 is `RESEARCH_ONLY` after the typed host checks passed and the isolated loader candidate failed native comparison. Continue with G64-023–030 in dependency order, following original evidence rather than assuming every target will promote.
4. At every phase boundary run G64-099 rebaseline. Live manifest/results override this plan's historical numeric assumptions.
5. When a phase is blocked, update the task ledger with exact failure evidence and proceed to an independent work unit; leave ASM intact.

**Current authoritative published matching claim (2026-11-11):** 148 reconstructed C / 11,020 matched bytes, 161 total C, 7,215 ASM / 7,376 identified entries. The six resource, menu and object functions passed integrated native-unit and full-ROM gates; `results/combined.json` records the exact 33,554,432-byte image comparison. The four short additional functions remain unpromoted after bounded native retries. Neither a host test, isolated match, correct function size, nor plan status can increase the counts.

**Publication boundary:** No proprietary ROM, asset, generated assembly, binary, private memory, or user-specific path enters this branch. No changes to main, no force-push.

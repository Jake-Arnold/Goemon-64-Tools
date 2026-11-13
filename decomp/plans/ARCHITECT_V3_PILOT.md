# Architect v3: bounded compiler-guided yield pilot

**Status:** Active; G64-082 was the first selected candidate and passed G2 on 2026-11-13. **Date:** 2026-11-13. **Target:** `Jake-Arnold/Goemon-64-Tools`, `chatgptweb/decomp`.

This optional pilot **supplements but does not replace** [Architect v2](EXECUTION_STRATEGY_V2.md), [executor protocol](EXECUTOR_PROTOCOL.md), or the existing `architect_override_v2` task packets. Preserve their task IDs, dependency graph, strict trial ceilings, evidence ledger, complete-ROM promotion gate, and branch/main boundaries. This document is not a claim of new compiler matches or executed tests.

## Evidence and rationale

At this review, the stored `results/combined.json` reports **149/149 exact matching-C functions, 11,148 matching bytes, and an exact 33,554,432-byte ROM**. `results/inventory.json` reports **162 combined C, 7,214 ASM, and 7,376 identified entries**. G64-074 contributed the latest 128-byte verified production promotion. G64-071–073, G64-075–079 and G64-081 were research-only. G64-080's gate reported zero additional promotions, so a completed task must not be conflated with new production C.

Native IDO mismatch examples include G64-072's zero-input branch-delay-slot difference at +0x04, G64-075/076's first-word mismatches, and G64-081's frame/register spill difference at +0x08 (original stores `$a1` at `sp+0x24`; candidate saves `$ra` at `sp+0x1c`). Host model correctness is valuable but does not imply original compiler instruction identity. These are candidate-specific blockers, not proof that all remaining ASM needs compiler reverse-engineering.

**Goal:** improve *new G2 functions and matching bytes per native variant*, by diagnosing translation-unit context and selecting independently promising candidates. Do not build a large speculative IDO fingerprint database, repeat previous failed variants, or optimise for host-test counts.

## Model split (operational responsibilities, not deployed automation)

| Step | Primary model | Expected product |
| --- | --- | --- |
| 1. Capture live baseline | **Luna Max** | HEAD, task statuses, manifest/source hashes, stored proof freshness |
| 2. Diagnose compilation context | **Sol 6.1 High** | One falsifiable hypothesis involving original unit, ABI, flags, types, scheduling or relocations |
| 3. Design mismatch taxonomy | **Sol 6.1 High** | Diagnostic categories and fail-closed comparator requirements |
| 4. Build/replay compiler fixtures | **Luna Max** | Positive/negative controls and deterministic tool output |
| 5. Define candidate scoring | **Sol 6.1 High** | Eligibility constraints, rank weights, tie-breaks |
| 6. Select up to three pilot candidates | **Sol 6.1 High** | Ranked target brief with dependency check |
| 7. Run bounded native C variants | **Luna Max** | Distinct one-hypothesis source trials, original-VMA comparisons, attempt ledger |
| 8. Stage G2-eligible candidates | **Luna Max** | Actual original-unit proof then fresh full-ROM/inventory checks |
| 9. Publish evidence and next handoff | **Luna Max** | Sanitised execution JSON, PROGRESS, task status and honest match delta |
| 10. Review pilot outcomes | **Sol 6.1 High** | Continue/revise/abort decision based on actual verified yield |

**Escalate from Luna to Sol** when two distinct trials repeat the same unexplained early mismatch (within the first two MIPS words), the cause is ambiguous (stack/register/FPU/branch/relocation), an intended change touches previously verified C siblings/compiler settings/verifier, or isolated and complete-unit results conflict. Sol must supply a discriminating next experiment and stop condition, or explicitly reject further trials. Luna handles ordinary compilation and mechanical verification without a fresh high-effort review each time.

## Execution protocol — ten steps

1. **Refresh authority:** fetch remote HEAD, inspect clean worktree, root `AGENTS.md`, `CONTINUE.md`, v2 protocol, relevant live task packets, `manifest.json`, `combined.json`, `inventory.json`, and G64-091 attempt ledger. The above figures are historical snapshot only.
2. **Pin native context:** for each target, verify original ROM span/hash, VMA, real source translation unit, adjacent accepted C and ASM symbols, IDO 5.3 binary/flags, prototypes, declarations, stack/ABI, linker symbols, alignment and relocations. Distinguish isolated from original-unit compilation.
3. **Classify differences:** report the first causal mismatch with original/candidate machine words, address, function size, stack/frame layout, register assignments, branch delay slots, FPU ordering, relocation and subsequent effect. Use categories `PROVENANCE_OR_EXTENT`, `FRAME`, `REGISTER_LIFETIME`, `BRANCH_DELAY`, `FPU_ORDER`, `RELOCATION_OR_LAYOUT`, `BODY`, `UNKNOWN`. Treat classification as a hypothesis, not a match. Fail closed on shifted VMAs or changed original extents.
4. **Replay reference fixtures:** positively control against verified G64-074 dispatcher, resource wrappers and menu functions; negatively control against F038 relocations, DBEC 0x48/0x50 frames, DE80 branch/register lifetime, G64-072 delay slot and G64-081 stack/FPU. Prefer extending existing `decomp/compare_original.py` and `decomp/probe.py`, not creating a parallel comparator.
5. **Score candidates:** apply the hard eligibility gates and ranking table below. Disqualify already promoted names, unchanged failed signatures, missing original provenance, unsatisfied prerequisites or unrepeatable original-unit builds.
6. **Choose pilot:** up to three *dependency-eligible* functions, selecting by evidence not task number/size. G64-082 and G64-084 can be screened after confirming G64-081's completed status; G64-083 requires G64-082 and G64-085 requires G64-084. Do not silently override those dependencies or change completed task statuses.
7. **Run controlled IDO:** one source hypothesis at a time, pinned original flags and VMA, full instruction and relocation comparison. Record immutable G64-091 attempt hashes; do not rerun equivalent failed source/context combinations. Add host tests only for new ROM-observed behaviour, not for inflated coverage.
8. **Gate promotions:** require exact original translation-unit text *including preserved siblings* and relocations before staging; then fresh 33,554,432-byte ROM identity, symbol inventory and source provenance. Only successful G2 may change production manifest, counts and `GLOBAL_ASM` ownership.
9. **Publish per-target evidence:** source/compiler/ROM hashes; exact size and first mismatch; trial budget; test commands and exits; `ISOLATED_EXACT`, `UNIT_EXACT`, `FULL_ROM_EXACT` or failure; fresh verifier `RUN`/`NOT_RUN`; function/byte delta; next action. Update `PROGRESS.md` *in the same commit* per `AGENTS.md`. Keep all ROMs and proprietary binaries out of Git.
10. **Pilot review:** Sol compares new G2 functions/bytes, number of native variants, deduplicated failures, useful causal findings and effort. Decide to keep this candidate-selection refinement, change ranking, or resume v2 scheduling. Do not expand into open-ended IDO tooling without proof of yield.

## Selection heuristic

Eligibility is mandatory before ranking: original boundary/VMA proven, ASM not previously promoted, true task prerequisites met, runnable pinned IDO/context, and unique nonduplicate hypothesis. Score only eligible targets on a documented **0–100 heuristic**, not a calibrated probability:

| Dimension | Maximum points |
| --- | ---: |
| Original ABI/types and caller relationships confirmed | 25 |
| Already matched C neighbours in the same source unit | 25 |
| Simple original CFG and limited register/stack complexity | 20 |
| ROM-backed interface/behavioural evidence | 15 |
| Manageable previous codegen mismatch and genuinely new hypothesis | 15 |

Rank 3–5 candidates; select no more than three. Shorter size is a weak tie-breaker, not proof of triviality (G64-090 established that `return_zero.c` ASM placeholders are nontrivial Memory Pak/PFS routines).

## Pilot budget and acceptance

- **Up to three candidates, maximum 12 new distinct native source variants overall**, with existing v2 **per-function stricter limits**: <=128 original bytes: <=3 after baseline; 129–512: <=5; >512: <=2. Extra v2 variants (at most two) require measured improvement and a new justification; never exceed the global 12. Completed tasks' exhausted budgets are not reset.
- Inspect source-unit context before brute-force rewrites for +0x00/+0x04/+0x08 mismatches. Merely moving the first mismatch forward one word does not establish convergence. Never accept exact-size-only, toleranced float results, arbitrary assembly patching, weaker comparators or synthetic linker aliases.
- **Aspirational target:** at least two *new G2-verified* functions within the pilot (149 -> at least 151 only if this baseline is still current). Zero new functions is an honest failure of the yield hypothesis, not permission to promote approximate code.
- A research-only candidate never triggers a repeated expensive 32 MiB build without a source-unit-exact candidate or separate justified verifier/provenance change. Record `NOT_RUN` rather than citing an old verifier as fresh.
- Stop after three candidates or 12 variants, whichever occurs first, and require Sol review. Do not declare G64-092 or G64-094 complete from partial diagnostics.

## Integration with the existing 100-task architecture

- **G64-091:** reuse the already written attempt ledger; do not create a second schema.
- **G64-092:** formal task depends on G64-050, G64-080, G64-090. A provisional ranked shortlist here is not formal G64-092 execution or completion.
- **G64-094:** formal task depends on G64-011, G64-023, G64-032, G64-044. Limited existing-fixture diagnosis can proceed without relabelling that task or bypassing required prerequisites.
- **G64-082–086, G64-089:** keep Wave C's actual dependency graph and strict FPU precision, multiplication order and signed-zero requirements.
- **G64-095, G64-099, G64-100:** retain original test/proof and completion criteria. Interim report checking does not complete final G64-099.

Neither Sol nor Luna may modify `main`, force-push, invent verification, reclassify research as production, or commit original ROMs, toolchains or generated assembly. **The deterministic native G2 verifier is authoritative.**

## Per-target handoff fields

`branch_head`, `task_id`, `symbol`, `source_unit`, `original_vma`, `original_rom_offset`, `original_size/hash`, `ido_hash/flags`, `source/context_hash`, `eligibility/ranking_score`, `hypothesis`, `attempt_signature`, `variants_used/limit`, `semantic_test_status`, `first_mismatch_word/category`, `isolated/unit/full_rom/inventory_tiers`, `verified_function_delta`, `verified_byte_delta`, `decision`, `next_owner`.

## Execution checkpoint — G64-082

The plan's Sol/Luna division was used for the G64-082 stop hypothesis and candidate review: Sol recommended the fifth, spill-home-focused source shape and ranked G64-084 first at 87/100 (G64-082 scored 83/100); the Luna read-only G2 audit confirmed the staged source, manifest, report and inventory are consistent. G64-082 consumed five distinct native source variants (the v2 limit for 129–512-byte targets), then passed original-unit and fresh full-ROM/inventory proof with one new function and 328 bytes. The proof now reports 150/150 functions and 11,476 bytes. The comparator fixture replay passed 17 tests, including positive and negative controls. Five distinct G64-091 input/attempt signatures were validated from preserved source/ELF evidence; the queue import records explicitly say no compiler ran during import. The five variants are the complete budget for G64-082; no retry budget remains.

**Next candidate:** G64-084 `func_8000EA74_F674` (72 bytes), Sol rank 1. Luna should run its <=3 post-baseline variants under the v2 cap, record attempt signatures and stop on mismatch or exactness. G64-083 is now dependency-eligible after G64-082 but remains below the selected G64-084 priority. The pilot has used 5 of 12 overall variant slots; the G64-084 task budget is stricter than the remaining global budget.

# Architect v2: evidence-led execution of the remaining 100-task Goemon plan

**Reviewed 2026-11-11 on `chatgptweb/decomp`.** Binding for the still-PLANNED G64 tasks. Do not restart the plan, renumber tasks, alter completed statuses, weaken exact-ROM proof, or touch `main`. Read the compact `python3 -m decomp.skill_context --task G64-NNN` output for the relevant per-task override instead of loading the 361 KB JSON.

## What the work has actually achieved

The stored verified proof at review is **148 reconstructed matching C functions / 11,020 MIPS bytes**, **161 combined C / 7,215 ASM / 7,376 identified entries**, and a complete **33,554,432-byte ROM match** (reference SHA1 `6ea0ed71032ce08fc2745f412d84936382197494`). Initial plan arithmetic of 142/10,652 is historical. G64-001–014 integrated **six** new functions, including the formerly blocked object dispatcher. G64-015–018 failed native byte matching (retain ASM). G64-021–035 produced **fifteen consecutive VM investigations** without adding a verified matching C function. They did produce valuable ROM-backed CFGs, ABI constraints and host tests. Record that as research, not production yield.

Most recent code-reconstruction evidence: G64-034 established original command walker DE80 at **232 bytes**, while its freshly rebuilt isolated IDO candidate was **220 bytes**, not older **228**. G64-035 tried four local C shapes under the v2 budget. The best moved the first mismatch to `0x8003DE88`; a 232-byte function with a wrong `0x30` frame was rejected. G64-036 mapped all original-observed wrapper paths to the reused 11-case harness and ROM guard. Its `DF68` gate is known to decrement `D_801C77A0`, not mutate `D_801C7798`, so no unsupported mutation case was added. G64-037–040 closed the VM research wave without another source-unit-exact candidate; the existing 148-function proof remains unchanged. G64-091 added the signed candidate-attempt ledger and unchanged-input deduplication, with no matching-C promotion. G64-090 audited all 13 `return_zero.c` placeholders; each is a Memory Pak/PFS routine, while the adjacent 8-byte C function is the actual constant-zero function. G64-071 traced `func_80001DF4_29F4`: its 32-bit index uses an 8-byte table stride and a bit-30 mask, unlike the matched sibling's low-16-bit/bit-31 behavior. Its 92-byte IDO candidate first differed at `+0x24`; one explicit-goto variant regressed to 96 bytes and `+0x1C`. Retain assembly and see `plans/execution/2026-11-11-g64-071-file-table-reader.json`. G64-072 traced `func_80001E50_2A50` as a 96-byte unsigned boundary-table helper with a zero sentinel and byte `+3` return. Three bounded 112-byte IDO shapes all first differed at `+0x04`, in the zero-input branch delay slot. Retain assembly; see `plans/execution/2026-11-13-g64-072-file-table-helper.json`. G64-073 traced `80001EB0` as a gated inclusive page mapper over eight-byte table pairs; two original-VMA candidates (304/320 bytes) both first differed at `+0x04` in prologue scheduling, and the global table extent remains unknown. Retain assembly; see `plans/execution/2026-11-13-g64-073-file-table-mapper.json`. **Next is G64-074–080**, beginning with object-list `80036308`.

## Priority schedule (the 65 task IDs pending at this review, each exactly once)

| Wave | IDs | Purpose |
|---|---|---|
| A | 035–040 | Close VM parser with bounded source experiments, preserving unresolved ASM |
| B | 091; 090; 071–080 | Implement attempt deduplication, audit truly small functions, then file/object/scheduler candidates with matching-C siblings |
| C | 081–086; 089 | Independently ready math/angle functions, with strict float/FPU identity |
| D | 041–050 | VM display-list, setup, formatter and integration |
| E | 052–060 | Overlay linked-ELF mapping, proof adapter, then eligible key/Ghost work (051 already DOC_ONLY) |
| F | 061–070 | Scene transitions and engine state, without unverified gameplay changes |
| G | 087–088 | Rotation functions after phase-07 prerequisites |
| H | 092–100 | Candidate ranking, typed contexts, regression proof, camera, rebase and post-100 handoff |

**Why this reorder:** phase 08 is independently accessible from completed tasks and contains file-table, object-list and scheduler functions adjacent to already matching C. It is a better prospect for near-term production yield than indefinite VM compiler searches. This is a hypothesis to test, **not a promise that those functions will match**. A previous FAILED_NATIVE result counts as completed research evidence for an independent follow-on, not as a passed native build. Respect real data prerequisites even when executing out of numerical order.

## Strict research budget and decision point

For every unpromoted function, check the live manifest for duplicate ownership, original exact ROM/VMA/size, pinned source/toolchain, caller ABI, first mismatch and prior attempt hash. **Only one falsifiable hypothesis at a time.**

- Original function <=128 bytes: at most **3** distinct native source variants beyond the baseline.
- 129–512 bytes: at most **5**.
- >512 bytes: at most **2**.
- Additional **2 maximum** only if the first mismatching instruction genuinely moves forward (or relocation/whole-unit evidence improves) and the new hypothesis is documented.
- Pure trace tasks: finish one complete ROM-backed CFG/contract and explicit unknowns without generating compiler variants merely to look busy.
- Focused tests: add a case only when an original behavior path or plausible negative mutant is not already covered. Do not run thousands more randomized cases just to increase the test count.

When the budget fails, **freeze the blocker** (function, source SHA, compiler flags, first native mismatch, tried hypotheses, concrete next required evidence), retain `GLOBAL_ASM`, mark `RESEARCH_ONLY` or `FAILED_NATIVE`, and proceed. A bounded unresolved function is a legitimate completion. Do not repeat the old 762-target scalar sweep.

## Verified-yield lane and gates

At each wave boundary, inspect **up to two** independently unlocked and bounded short candidate opportunities, choosing by original ROM extent, clear o32 ABI, nearby accepted C, and likely complete translation-unit fit. G64-090's audit of the 13 `return_zero.c` placeholders is complete and found no trivial candidate. G64-071–073's reader traces and bounded native stops are complete; current early opportunities are G64-074–077 in `object_flags.c` and G64-078–079 schedulers. Names such as return_zero are not evidence of trivial functionality.

Promote an eligible unit **as soon as** exact pinned native IDO original-unit, neighboring sibling instructions and relocations all match, followed by a **fresh** complete 33,554,432-byte image and original-symbol inventory gate. Never wait for all other functions in a batch to match. Host, REA/Ghidra, isolated function matching, preserved size, or increased test count cannot alter the verified count.

## Verification economy

Run focused host/ROM-anchor tests when a research file changes and broad Python/sanitizer suites at substantive phase or integration checkpoints. Run native IDO if the candidate/source hypothesis changed or conflicting evidence needs reproduction. Do not repeatedly run the expensive 32 MiB verifier for documentation-only changes or an unchanged production source; report `fresh_full_rom=NOT_RUN`. Run it for a staged UNIT_EXACT candidate, changed verifier/build input or explicit reproducibility check. Never reuse an old result as proof of a new candidate.

## Wave-end artifact

Publish one compact record per wave: first/last HEAD, new **G2 function and byte delta**, unit-exact opportunities, reusable compiler/tool/testing lessons, frozen mismatch signatures, tests actually run, private full-ROM gate run/NOT_RUN, and next independently unlocked wave. **Zero new G2 in a wave triggers an efficiency review**, not speculative count inflation. Keep G64-099 formally PLANNED until its later prerequisites complete even though interim rebaselines occur.

## Immediate commands to the executor

1. **G64-035 complete:** four bounded source shapes moved the best first mismatch only to `0x8003DE88`; stop after the next register-lifetime hypothesis regressed. Keep the original assembly.
2. **G64-036 complete** from existing semantic/ROM evidence; no duplicate fuzz or invented helper effects. Complete G64-037–040 with distinct evidence. G64-040 runs G2 only for actual whole-unit exact C, otherwise records a no-promotion checkpoint with existing 148 proof unchanged.
3. G64-091, G64-090, G64-071, G64-072 and G64-073 are complete with no promotion. Execute G64-074–080 next, promoting independently exact source units through full G2 as soon as they qualify.
4. Continue waves C–H in dependency order, use the per-task `architect_override_v2`, and prepare the ranked post-100 yield programme.

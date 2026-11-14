# Consolidated Goemon work queue (2026-11-08)

**Reconciled on 2026-11-14:** The old 142-function checkpoint and ten-function
queue below are historical. Current authority is `decomp/CONTINUE.md` and the
live proof reports: **163 matching C / 12,384 bytes / 176 combined C / 7,200
ASM**. The resource, menu, object, overlay-key, dialogue-window slot setter,
and Impact HP helpers have passed full-ROM verification. The active Impact
follow-up is separate from the 100-task queue below. The resource, menu and
object candidates from the older queue have passed full-ROM verification.
G64-015–018 were retried and remain
`FAILED_NATIVE`; G64-021 is `DOC_ONLY` with its call graph in
`VM_RESOURCE_CALLGRAPH.md`; G64-022 is `RESEARCH_ONLY` with no promotion;
G64-023 reproduced the nonmatching F038 baseline and remains `RESEARCH_ONLY`;
G64-024's three new variants did not improve that baseline and remain
`RESEARCH_ONLY`; G64-025's mutation model passed but its native candidate
remains unpromoted. G64-026 pinned the D468 32-byte frame and saved-register
lifetimes with 36 original-address guards; its 556-byte candidate still differs
from the 548-byte original, so it remains `RESEARCH_ONLY`. G64-027's D68C
control-flow trace is complete and remains `RESEARCH_ONLY`: both dispatch
tables, state returns and callback cursor reloads are tied to the pinned ROM,
with no C candidate. G64-028 traced DF98's signed-token range, 40-entry table,
caller sentinel checks, and paced/unpaced marker, repeat and cursor ordering.
It remains `RESEARCH_ONLY` with no C model. G64-029 added a DDC4 host
regression for callback mutation and entry-ID preservation; its synthetic
cached-global negative control fails, and the production proof remains
unchanged. G64-030 reconciled the live 148-function proof and 7,376-entry
inventory, recorded the current `script_vm.c` split as 43 C / 13 ASM, and added
the typed resource interface matrix in `VM_RESOURCE_CALLGRAPH.md`. DDC4 and its
matched context save/restore siblings remain exact; no new resource candidate
passed G2. Keep D468, D68C, DF98 and F038 as ASM. G64-031 traced DBEC's
472-byte CFG and six branch-likely slots in `VM_TEXT_LOOP_TRACE.md`; its
original assembly ownership is unchanged. G64-032 recorded the 0x50 versus
0x48 frame and five nonmatching native source-shape trials in
`VM_TEXT_LOOP_FRAME.md`. G64-033 expanded the MIPS/host differential model to
ten fixed edge cases plus 10,000 seeded cases and killed four targeted
signedness, bound and alias mutants; it made no C promotion. G64-034 recovered
the DE80 signed-token CFG, expanded ROM-bound and host tests, and corrected the
current pinned IDO result to a 220-byte symbol with a first mismatch at
`0x8003DE84`. G64-035 tested four bounded shapes; the best first mismatch was
`0x8003DE88`, while a size-equal 232-byte function had the wrong frame. G64-036
closed from its eleven existing semantic cases and ROM guard without inventing
gate-helper effects. G64-037 traced `func_8003ED60_3F960` from its 592-byte
original extent, pinned its caller and no-argument ABI, guarded twelve
output-cursor updates, and tried one trace-derived IDO candidate. The first
mismatch is `0x8003ED68`; the function remains `GLOBAL_ASM`. See
`VM_ED60_TRACE.md` and
`plans/execution/2026-11-11-g64-037-ed60-trace.json`. G64-038 verified the
48-byte `func_8003F6E8_402E8` ROM extent and both trailing return pairs; its
40-byte C prefix and 56-byte candidate annotation are not original extents.
The function remains `GLOBAL_ASM`. See
`plans/execution/2026-11-11-g64-038-wrapper-extent.json`. G64-039 adds expected
fixed MIPS traces for DBEC and emit/decode callback-order assertions for EB34,
then cross-references existing DE80, DF98, ED60 and F6E8 evidence. All stubs
remain bounded synthetic hooks; no unknown decoder effects are modeled. No C
ownership or stored proof changed. See `VM_PARSER_BEHAVIOR_MATRIX.md` and
`plans/execution/2026-11-11-g64-039-parser-matrix.json`. G64-040 found no new
source-unit-exact candidate: EB34 is already matching C, while DBEC, DE80,
DF98, ED60 and F6E8 remain ASM-owned. Production and verifier inputs were
unchanged, so the stored 148-function full-ROM proof was retained without a
new build. See `plans/execution/2026-11-11-g64-040-parser-production-gate.json`.
G64-091 then added signed per-function attempt records, legacy report import and
cross-recipe suppression of unchanged completed probes without changing
matching-C ownership. See
`plans/execution/2026-11-11-g64-091-attempt-ledger.json`. G64-090 audited all 13
`return_zero.c` placeholders against the pinned Memory Pak disassembly and
decompressed ROM; all are nontrivial PFS routines and remain `GLOBAL_ASM`. See
`plans/execution/2026-11-11-g64-090-return-zero-audit.json`. G64-071 traced
`func_80001DF4_29F4` as a full-width 8-byte-stride lookup with a bit-30 result;
two bounded native candidates failed exact matching, so it remains `GLOBAL_ASM`.
See `plans/execution/2026-11-11-g64-071-file-table-reader.json`. G64-072 traced
`80001E50` as a four-byte sentinel lookup; three bounded IDO candidates stayed
112 bytes and differed from the original at `+0x04`. See
`plans/execution/2026-11-13-g64-072-file-table-helper.json`. Next under v2:
G64-073 traced `80001EB0` as a gated inclusive page mapper; two IDO candidates
both differed at `+0x04`, so it remains `GLOBAL_ASM`. Its `D_80054ACC` table
extent is not declared in the pinned source. See
`plans/execution/2026-11-13-g64-073-file-table-mapper.json`. G64-074 passed G2: `80036308` is a per-node dispatcher and adds 128 exact matching bytes. G64-075 traced `80036388` as a move-to-front operation, then stopped after three candidates all first differed at `+0x00`; it remains `GLOBAL_ASM`. G64-076 traced `800363F4` as a caller-gated non-head move-to-front operation; two candidates both first differed at `+0x00`, so it also remains `GLOBAL_ASM`. G64-077 traced `80036448` as a 180-byte allocation gate. Four native variants failed exact codegen; both accepted C siblings remain byte-exact, but the target stays `GLOBAL_ASM`. G64-078 traced the 308-byte `8000702C` worker: it receives on owner `+0x40`; message `0x29D` sends owner `+0x20` through each node `+4` destination queue before reloading the `+0` link. The sanitizer-tested host reference rejected a cached-next mutant; production stays `GLOBAL_ASM`. G64-079 traced `80007160` as the 164-byte default task-message handler: the worker passes owner in `$a0` and the 32-bit task `OSMesg` in `$a1`; the handler increments owner `+0x2B4` before its duplicate guard and conditionally calls the queue/task helpers. Its mock reference rejected an increment-after-guard mutant; production remains `GLOBAL_ASM`. G64-080 closed the files/object/scheduler batch gate with zero new functions or bytes; G64-074 remains the only promoted candidate in those units. G64-081 analyzed `8000E2D4` with a test-only reference and three bounded IDO shapes; no candidate matched, so production remains `GLOBAL_ASM`. See `plans/execution/2026-11-13-g64-081-math-helper.json`. G64-082, G64-084, and G64-085 passed fresh G2, adding exact 328-, 72-, and 72-byte matches. The v3 pilot added 3 functions / 472 bytes and closed at 3/3 candidates using 7/12 new variants. G64-086 then passed ordinary v2 with two of five variants, adding 180 exact bytes; at that checkpoint, the proof was 153 functions / 11,800 bytes. G64-083 closed `RESEARCH_ONLY` after two new variants: V1 first differed at `+0x5C` in stack-local placement, V2 enlarged the frame to `0x50` and differed at entry. It remains ASM-owned and G2 was not run. G64-089 ranked the five float-state functions and tried two bounded candidates for 80006B44; V1 differed in 38 target words, while Sol-approved V2 reduced that to 36 but retained the first saved-register mismatch. It remains GLOBAL_ASM; G2 and inventory were not run. See plans/execution/2026-11-13-g64-089-float-state.json. G64-041 completed RESEARCH_ONLY after verifying all 110 original words locally and recording the sanitized 11-command store contract; see plans/execution/2026-11-13-g64-041-display-emitter-trace.json. G64-042/043 are dependency-ready and remain unstarted; G64-087 is RESEARCH_ONLY after two bounded native candidates failed, and G64-088 is the first PLANNED task. The independent Impact HP clamp promotion passed G2; see plans/execution/2026-11-14-impact-hp-clamp-promotion.json. See `plans/execution/2026-11-13-g64-074-object-flags.json`, `plans/execution/2026-11-13-g64-075-object-list-move-to-front.json`, `plans/execution/2026-11-13-g64-076-object-list-move-to-front.json`, `plans/execution/2026-11-13-g64-077-object-allocation-gate.json`, `plans/execution/2026-11-13-g64-078-scheduler-queue.json` and `plans/execution/2026-11-13-g64-079-scheduler-queue-handler.json`. Private ROM and compiler files
remain local under the ignored diagnostics input directory.

Date-stamped work lists below are historical unless labeled as the current VM
residual inventory. For execution order, use `decomp/CONTINUE.md`,
`EXECUTION_STRATEGY_V2.md`, and the first dependency-ready task brief.

This is the repository's cross-conversation handoff for the Goemon toolkit and matching-C projects. Prior ChatGPT conversations named “Goemon” or “Goemon Decomp Continuation” contain useful research but **are not independent sources of current function counts or proof**. Always read `AGENTS.md`, `decomp/CONTINUE.md`, `decomp/manifest.json`, `decomp/results/combined.json`, `decomp/results/inventory.json`, and the live `chatgptweb/decomp` HEAD first. This file records an evidence-bound snapshot, not a claim that old attempts were freshly re-run.

## Verified checkpoint; do not repeat

- **Latest 2026-11-09 independent complete-ROM checkpoint:** **142 matching-C / 10,652 MIPS bytes**, 13 upstream C / 155 combined C / 7,221 remaining ASM of 7,376 identified. `func_8003D9B8_3E5B8` has been promoted following 340/340 exact original bytes, complete 2,331-object Splat/IDO link, full 33,554,432-byte ROM identity, readelf inventory and 1,134 sanitizer-tested host cases. The uninterrupted formal verifier is **still pending**. The 141-function checkpoint below is historical.

- Matching-C branch promotion checkpoint: `869771dc92872a8b4e05f77c7adebe2e7cef260e`. At this checkpoint: **141 reconstructed matching-C functions, 10,312 bytes; 13 upstream C entries; 154 combined C entries; 7,222 assembly entries of 7,376 identified**. VM: 55 C / 14 ASM.
- The **136-byte** `func_8003EFB0_3FBB0` and **44-byte** `func_8003F350_3FF50` have both been promoted. The callback's corrected signed return declaration is integrated. Do not redo the earlier provisional 138/139-function work.
- `decomp/results/combined.json` records exact original-address matches and byte-identical independent assembly/linking of the full **33,554,432-byte** decompressed image, expected SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; the retail input SHA-1 is `df8083a54296b8c151917c5333e1c85f014a2a66`.
- The single uninterrupted formal verification runner timed out; its resumed clean build passed independent full-ROM and inventory comparisons. **An uninterrupted formal verifier run remains outstanding**. Separately, a regenerated full 2,331-object 141-function build has passed independent complete-ROM, original-address, and symbol-inventory comparisons. Never mislabel the interrupted formal run as successful.
- The earlier collision gate (80 bytes), heap no-op (8 bytes), and choice edge (204 bytes) are already included in the 141. Their pinned source/layout guards must remain enforced.

## Next-ten execution plan (2026-11-09)

Follow [NEXT_TEN_FUNCTIONS.md](NEXT_TEN_FUNCTIONS.md) for the prioritized **ten distinct unpromoted** VM function targets, precise acceptance gates, and deliberately deferred high-cost routines. This is a bounded research sequence, not ten pre-verified promotions; the 142 matching-C proof and pending uninterrupted formal verifier remain authoritative.

**Next-ten execution checkpoint (2026-11-09):** all ten selected functions have now been investigated; **zero promoted**. Best new isolated codegen result is resource lookup `func_8003F038_3FC38`, original/native 196 bytes with **25/42** directly comparable positions after a single `volatile s32 half` declaration. Wrapper original span corrected to **48 bytes / 12 words**, not 56. See `NEXT_TEN_FUNCTIONS.md` and `results/vm_next_ten_batch4.json`. The independent 142-function ROM identity and pending uninterrupted formal verifier remain unchanged.

## Next five work packages (2026-11-09)

**Execution checkpoint (2026-11-09):** all five tasks visited; no new promotion. Formal run needs the full current 142-function source rather than the 136-function archive. Overlay `file_43` original mapping/hash reference gate added with 19 tests and both original functions verified. Key gate still isolated-only; Ghost entrance 140-byte new draft is unpromoted and does not supersede the historical two-byte mismatch. See `results/next_five_execution_checkpoint.json` and `NEXT_FIVE_ACTIONS.md`. 

The next technical work order is [NEXT_FIVE_ACTIONS.md](NEXT_FIVE_ACTIONS.md): **formal 142-function verification → VM halfword lookup native-ID0 match → overlay ROM/VMA/layout verifier → key overlay initializer → Ghost Toys overlay entrance**. Tasks #4 and #5 depend on strict overlay verification from #3. This does not supersede historical completed-ten evidence and does not increase the 142-function count.

**Test reliability correction (2026-11-09):** fixed stale `tests/test_decomp_verify.py` 139/140 expectations to live 141/142 manifest claims, plus repaired malformed `compare_original.py` label/jump regexes and synthetic newline fixtures. Old comparator test suite actually failed 4/12; repaired suite passed 13/13 and two private original-ROM/IDO nonmatch checks. **Do not treat stale isolated metrics as verified without recomparison.** The uninterrupted formal 142-function verifier is still the highest verification priority. No count change.

## Historical ten-function list (2026-11-10; superseded)

Follow [NEXT_TEN_MAIN_SEGMENT.md](NEXT_TEN_MAIN_SEGMENT.md) for **ten fresh, still-ASM main-segment functions (528 bytes)** selected after the prior VM ten-function investigation stalled without promotions. The whole-ROM identity proof remains 142 exact-C functions / 10,652 bytes; current-source formal verifier pending. **First two:** `func_8003A1E8_3ADE8` (28 B) and `func_80006274_6E74` (36 B). Original 132/132 private ROM instruction words have been verified. Older VM, overlay and Ghost Toys entries below remain open but are not the new execution order.

**2026-11-10 updated branch formal verifier:** newly refreshed `results/combined.json` records **142/142 original-address matches and full 32 MiB ROM identity; formal verifier complete**. Next-ten research first wave: `func_80034ED4_35AD4`, `func_80034F20_35B20` and `func_80035094_35C94` compile/link individually at original VMA with all **120/120 bytes exact**; **NOT PROMOTED** without fresh 2,331-object integration and ROM proof. 30,000 host mocks and seven negative parser tests passed. Evidence `results/next_ten_main_wave1.json`; current counts still **142 C / 10,652 bytes / 7,221 ASM**.

**2026-11-10 second-wave outcome:** entire new ten-function batch was investigated. The three menu-state functions `func_80011B60_12760`, `func_80011BB4_127B4`, `func_80011C04_12804` are now **exact standalone IDO-linked original MIPS matches (248/248 bytes)** and passed 90,000 synthetic sanitizer-tested cases. With prior wave there are **6/10 exact isolated matches, 368 bytes**, but **ZERO promoted** pending a complete new 2,331-object ROM integration. Authoritative existing formal proof unchanged: 142 matching-C / 10,652 bytes. See `results/next_ten_main_wave2.json`; next task is the full build/inventory promotion gate.

## Historical exact-ROM promotion checkpoint — 20 gated steps (2026-11-10; superseded)

[NEXT_TWENTY_STEPS.md](NEXT_TWENTY_STEPS.md) is the **current execution order**. First reproduce the complete **142-function** formal verifier and six original-address isolated links. Next integrate resource wrappers `func_80034ED4_35AD4`/`func_80034F20_35B20`, object dispatcher `func_80035094_35C94`, and menu trio `func_80011B60_12760`/`func_80011BB4_127B4`/`func_80011C04_12804` under original-unit compilation and full 32 MiB ROM proof. Then retry four nonmatching 28/36/44/52-byte routines. **No promotion is implied by the plan**; existing verified 142/10,652/7,221 remains authoritative.

**Execution status, 2026-11-10:** full-unit research verified resource **112/112** and menu **256/256** bytes; object unit **fails** with two swapped 4-byte instructions at `0x35C9C/0x35CA0`. `results/next_twenty_execution_20261110.json` has the per-step ledger. Prior isolated six matches cannot be blindly promoted: the object compiler changes when compiled beside its already matching sibling. Full current 2,331-object ROM build remains a required blocker; official 142 matching functions unchanged.

## Current VM residual inventory (G64-050; reconciled 2026-11-13)

The canonical machine-readable inventory is
[`results/vm_residual_inventory.json`](results/vm_residual_inventory.json). It
is checked against the live `script_vm.c` manifest ownership and fingerprints,
the pinned upstream source, and the decompressed USA ROM. There are exactly 13
remaining `GLOBAL_ASM` functions in source order. The ordinary generated
[`results/inventory.json`](results/inventory.json) remains unchanged: it is the
whole-project symbol inventory, and its 13 `upstream_unmarked_names` are a
different set of upstream C entries. The residual ledger records each VM
function's original extent/hash, candidate source hash where one exists,
strongest native exactness result, concrete blocker, and next unblock condition.

| Target | Original VMA / ROM / bytes | Strongest exactness evidence | Concrete blocker |
| --- | --- | --- | --- |
| D468 `func_8003D468_3E068` | `8003D468 / 3E068 / 548` | Candidate 556 B; 1/26 direct words, first mismatch `+0x08`. | Candidate frame is 24 B versus original 32 B; current prototype also omits the observed 32-bit return. |
| D68C `func_8003D68C_3E28C` | `8003D68C / 3E28C / 812` | ROM CFG traced and guarded; no C candidate. | Callback effects and source-level dispatch shape remain unresolved. |
| DBEC `func_8003DBEC_3E7EC` | `8003DBEC / 3E7EC / 472` | 472 B native symbol, 53/95 raw comparable nonrelocation words. | Candidate frame is 0x50 versus original 0x48; 17 relocation-layout differences. |
| DE80 `func_8003DE80_3EA80` | `8003DE80 / 3EA80 / 232` | Best bounded candidate: 38/56 differing words, mismatch moved to `+0x08`. | `bltzl` target remains four bytes late; the four source shapes are closed. |
| DF98 `func_8003DF98_3EB98` | `8003DF98 / 3EB98 / 528` | ROM-bound signed-token trace and 40-entry table; no C candidate. | Helper effects remain opaque; no native mismatch exists yet. |
| E234 `func_8003E234_3EE34` | `8003E234 / 3EE34 / 440` | Full-unit candidate 444 B; first target register differs at entry. | `$v0` replaces original `$v1`; later forward-call relocation shifts at unit `+0x118`. |
| E6C0 `func_8003E6C0_3F2C0` | `8003E6C0 / 3F2C0 / 348` | Full-unit candidate 356 B; 45/87 words differ. | First mismatch is saved-register spill at `+0x0C`; growth shifts a forward relocation. |
| EBAC `func_8003EBAC_3F7AC` | `8003EBAC / 3F7AC / 436` | Full-unit candidate 428 B; first target register differs at entry. | `$v0` replaces original `$v1`; a later sibling moves despite section rounding. |
| ED60 `func_8003ED60_3F960` | `8003ED60 / 3F960 / 592` | One isolated probe 584 B; first mismatch at `0x8003ED68`. | 136/146 positions differ; the two F038 call effects remain unresolved. |
| F038 `func_8003F038_3FC38` | `8003F038 / 3FC38 / 196` | Equal-size probe; 25/42 direct words and 3/3 relocation shapes. | Four relocation-layout differences remain; first mismatch `+0x28`; three refinements repeated it. |
| F37C `func_8003F37C_3FF7C` | `8003F37C / 3FF7C / 192` | Equal-size full-unit candidate; all siblings exact. | 36 target words differ; first mismatch `+0x08` swaps float-register scheduling. |
| F480 `func_8003F480_40080` | `8003F480 / 40080 / 164` | Best isolated candidate 156 B, 3/13 direct words. | 15 variants did not reproduce the original `bnel` delay-slot schedule. |
| F6E8 `func_8003F6E8_402E8` | `8003F6E8 / 402E8 / 48` | Exact original extent guarded; no complete C body. | A 40 B prefix omits the second `jr $ra; nop`; the 56 B note is not an original extent. |

Reusable constraints: keep the program cursor separate from the halfword text
cursor; reload mutable globals after callbacks where the original does; preserve
branch-likely delay slots and original spill/frame layouts; distinguish resource
ID, loaded base, relocation delta, and relocated PC; and compare every candidate
inside the full 10,112-byte unit because isolated matches can still move
siblings and forward relocations. The 13 remain ASM-owned; no new G2 or
inventory build was run. Full evidence, including hashes and unblock conditions,
is in the canonical JSON above.

### Separate dialogue-overlay candidates (not part of the 13)

A Sol medium follow-up on branch
`codex/goemon-vm-overlay-followup` at commit
`6b5d0d8958bd87fb850c05008acb29650579bf30` found two isolated exact `file_12`
callbacks: `0x80222034` (20 B) and `0x80222168` (36 B). Both match pinned IDO
bytes at their original overlay VMAs. They remain research-only because the
production manifest lacks the `file_12` unit, section/relocation adapter, and
fresh full-ROM/inventory proof. This branch is separate from
`chatgptweb/decomp`; these candidates are not promoted or included in the 13.
The evidence is in that branch's `decomp/VM_CONVERSATION_TARGETS.md` and
`decomp/results/file12_dialogue_callbacks_research.json`.

### Other non-VM leads

- Overlay key initializer `func_080001BC_6F369C`: a 96-byte isolated probe
  matched, but production overlay ROM/VMA/section proof remains the blocker.
- Ghost Toys entrance: the historical 140-byte draft still has two incorrect
  stack offsets; use `decomp/GHOST_TOYS_CHECKPOINT.md` before any restart.

Use `compare_original.py` with a SHA-verified decompressed reference and private
original assembly for reproducible, relocation-aware diagnostics. Isolated
identity never proves a production-unit or complete-ROM promotion. Do not repeat
exhausted variants without a concrete instruction prediction.

## Main-branch toolkit status (superseded historical backlog)

The user confirmed on 2026-11-08 that the earlier native-warp and story-flag investigation is **already working on `main`**. The former unsolved warp/spawn/Benkei/story-flag checklist in this queue was from early conversations and is no longer an active task. `main` remains the source of truth for that toolkit work; do not revive stale experiments or change `main` under the decomp-only authorization. Continue solely on exact matching-C, original-address/compiler/ROM proof, and relevant safe tests.

## Library, toolchain, and reproducibility notes

- User-supplied Files Library artifacts include `goemon-matching-rebuild.zip`, `toolkit.zip`, `python312.tar.gz`, `mips-binutils.part-00`, `mips-binutils.part-01`, and the USA retail ROM. Re-list and materialize these on **each new execution**; container state is not persistent.
- The two MIPS parts concatenate to a valid inspectable `.tar.gz` archive (555,600,578 combined bytes). The Python 3.12 archive also lists successfully. Validate actual binaries and dependency locks after extraction.
- `goemon-matching-rebuild.zip` contains an older full-build snapshot and has an identified **CRC mismatch** in generated `candidate/asm/usa/file_72.s`. Never invent replacement bytes or treat a partial extraction as a verified clean checkout. Recreate generated assembly only from pinned source/ROM/toolchain using the normal derivation pipeline.
- On 2026-11-08, the recovered archived toolkit checkout at `261ac0badc4cf23ffa0813f44bc5d21097565bad` passed **365 host/unit tests, 4 skips, 0 failures** under `xvfb-run`. This does **not** test the latest 140-function checkout or perform a full-ROM build. A non-Xvfb initial run encountered 15 Tk display errors and was superseded by that passing Xvfb run.
- Remote `git ls-remote` from that container failed DNS resolution; the connected GitHub API remains an alternate source for checking refs and writing reviewed, non-binary documentation. Do not conflate connector access with a local Git fetch.
- Do not commit ROMs, assets, saves, generated assembly, object files, compiler archives, runtime logs, credentials, personal paths or raw memory. Preserve historical proof and diagnostic reports.

## Working rule

The **live `chatgptweb/decomp` branch**, not any conversation's last reply, determines current counts and integrated functions. Implement only substantive, independently validated changes. Record tests (including skips and environment), remaining blockers and next steps in `PROGRESS.md` with every repository change. Commit and push only `chatgptweb/decomp`, without force, and verify the new remote commit SHA.

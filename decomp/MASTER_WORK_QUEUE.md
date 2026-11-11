# Consolidated Goemon work queue (2026-11-08)

**Reconciled on 2026-11-11:** The old 142-function checkpoint and ten-function
queue below are historical. Current authority is `decomp/CONTINUE.md` and the
live proof reports: **148 matching C / 11,020 bytes / 161 combined C / 7,215
ASM**. The resource, menu and object candidates from that older queue have
passed full-ROM verification. G64-015–018 were retried and remain
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
passed G2. Keep D468, D68C, DF98 and F038 as ASM. Continue with G64-031.
All private ROM and compiler files remain local under the ignored diagnostics
input directory.

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

## New active ten-function list (2026-11-10)

Follow [NEXT_TEN_MAIN_SEGMENT.md](NEXT_TEN_MAIN_SEGMENT.md) for **ten fresh, still-ASM main-segment functions (528 bytes)** selected after the prior VM ten-function investigation stalled without promotions. The whole-ROM identity proof remains 142 exact-C functions / 10,652 bytes; current-source formal verifier pending. **First two:** `func_8003A1E8_3ADE8` (28 B) and `func_80006274_6E74` (36 B). Original 132/132 private ROM instruction words have been verified. Older VM, overlay and Ghost Toys entries below remain open but are not the new execution order.

**2026-11-10 updated branch formal verifier:** newly refreshed `results/combined.json` records **142/142 original-address matches and full 32 MiB ROM identity; formal verifier complete**. Next-ten research first wave: `func_80034ED4_35AD4`, `func_80034F20_35B20` and `func_80035094_35C94` compile/link individually at original VMA with all **120/120 bytes exact**; **NOT PROMOTED** without fresh 2,331-object integration and ROM proof. 30,000 host mocks and seven negative parser tests passed. Evidence `results/next_ten_main_wave1.json`; current counts still **142 C / 10,652 bytes / 7,221 ASM**.

**2026-11-10 second-wave outcome:** entire new ten-function batch was investigated. The three menu-state functions `func_80011B60_12760`, `func_80011BB4_127B4`, `func_80011C04_12804` are now **exact standalone IDO-linked original MIPS matches (248/248 bytes)** and passed 90,000 synthetic sanitizer-tested cases. With prior wave there are **6/10 exact isolated matches, 368 bytes**, but **ZERO promoted** pending a complete new 2,331-object ROM integration. Authoritative existing formal proof unchanged: 142 matching-C / 10,652 bytes. See `results/next_ten_main_wave2.json`; next task is the full build/inventory promotion gate.

## Active exact-ROM promotion work plan — 20 gated steps (2026-11-10)

[NEXT_TWENTY_STEPS.md](NEXT_TWENTY_STEPS.md) is the **current execution order**. First reproduce the complete **142-function** formal verifier and six original-address isolated links. Next integrate resource wrappers `func_80034ED4_35AD4`/`func_80034F20_35B20`, object dispatcher `func_80035094_35C94`, and menu trio `func_80011B60_12760`/`func_80011BB4_127B4`/`func_80011C04_12804` under original-unit compilation and full 32 MiB ROM proof. Then retry four nonmatching 28/36/44/52-byte routines. **No promotion is implied by the plan**; existing verified 142/10,652/7,221 remains authoritative.

**Execution status, 2026-11-10:** full-unit research verified resource **112/112** and menu **256/256** bytes; object unit **fails** with two swapped 4-byte instructions at `0x35C9C/0x35CA0`. `results/next_twenty_execution_20261110.json` has the per-step ledger. Prior isolated six matches cannot be blindly promoted: the object compiler changes when compiled beside its already matching sibling. Full current 2,331-object ROM build remains a required blocker; official 142 matching functions unchanged.

## Open matching-C work (ordered)

**2026-11-09 plan execution:** targets **#1–#5** have research-only candidates and synthetic tests, but none match exact original MIPS. #4 VM choice/setup `func_8003E6C0_3F2C0` compiles to 400 B versus 348 B original, with 400 passing host scenarios and 12 private-original guards. See `NEXT_TEN_FUNCTIONS.md` status, `results/vm_next_ten_batch1.json`, `results/vm_next_ten_batch2.json`. **#5:** fourteen isolated command-walker trials (seven host-tested) did not reproduce its original 232-byte instruction layout; see `results/vm_next_ten_batch3.json`. **Next #6 `func_8003DBEC_3E7EC`.** 142-function full-ROM proof and formal flag unchanged.

| Priority | Target | Precise unresolved condition |
| --- | --- | --- |
| P0 | Uninterrupted 142-function formal verifier | Restore exact latest branch/toolchain/baseline and execute `decomp.verify` to completion. Refresh proof provenance only if independently rebuilt output is exact. |
| P2 | VM text loop `func_8003DBEC_3E7EC` | Separate volatile-work/explicit-script-argument research variant now compiles to the original 472-byte symbol with 53/95 comparable nonrelocation instruction positions equal (up from the terminal-state switch draft at 47/95); both variants remain unpromoted, and the new version passed 10,000 synthetic original-MIPS/host-C cases; original-MIPS/host-C differential harness passes 10,000 synthetic cases over two seeds (not an exact instruction match); see candidate and synthetic tests. Earlier 480-byte draft differs in 101 words. Preserve the confirmed distinction between global pointer storage at 0x801C77E8 (with independent halfword at global +0xA) and the script pointer *value* in its first word; also preserve two unsigned controller halfwords, account for six branch-likely delay slots, two counters, dynamically reloaded outer bound, and callback early-return path. This is **static analysis, not a verified match**. |
| P3 | VM loader `func_8003D468_3E068` | Approximately 548-byte original; an old candidate matched 118/137 instruction positions only. Resolve real resource-prefix declarations, address loads, and register allocation. |
| P3 | VM command walker `func_8003DE80_3EA80` | Original 232 bytes; research-only out-of-line negative-token variant compiles 228 bytes, improving directly comparable positions **3/33 → 8/35** without matching the original `bltzl` delay or `$s1/$s2/$s3` lifetimes. Two 1,200-case synthetic host runs passed; no promotion. See `candidates/vm_command_walker_goto_probe.c` and `results/vm_command_walker_goto_probe.json`. |
| P2 | VM resource halfword lookup `func_8003F038_3FC38` | Research-only **196-byte original / 196-byte native IDO** `volatile s32 half` variant, improves to **25/42 direct comparable MIPS positions**, 3/3 matching relocation shapes, 4 relocation-layout differences; 3,000 sanitizer-tested host cases passed. Still UNPROMOTED; resolve original `$v1` index vs candidate `$t6` and stack slot allocation. |
| P3 | VM digit formatter `func_8003F480_40080` | **NEW research-only 164-byte C draft**, original 41 words; 9/41 relocation-masked positional words, only 3/19 directly comparable non-relocation words; 1,000 host cases and 15 original-assembly guards passed. Need reproduce `bnel` delay-slot and `sprintf` argument-load scheduling. **Unpromoted**. |
| Completed | Choice edge `func_8003D0B0_3DCB0` | Promoted 204 original MIPS bytes at `0x8003D0B0`; fresh regenerated 2,331-object build produced exactly matching 32 MiB ROM and a 141-function/7,376-entry verified inventory. 100 host cases passed; uninterrupted formal verifier remains pending. |
| P4 | VM wrapper `func_8003F6E8_402E8` | Verified original archived extent **48 bytes / 12 words**, plus missing final **8-byte `jr $ra; nop`** after the natural 40-byte C prefix. The prior **56-byte** number is a candidate inventory annotation, not an archived original extent. `test_vm_wrapper_extent.py` guards this; do not promote prefix. |
| Completed | VM comparator `func_8003D9B8_3E5B8` | Promoted in latest 142-function, 10,652-byte complete-ROM proof; 340 original MIPS bytes exact, 2,331 linked objects, ROM and readelf inventory exact, 1,134 sanitizer host cases. Uninterrupted formal verifier pending. |
| P5 | Overlay key initializer `func_080001BC_6F369C` | 96-byte isolated linked probe matched; main-segment manifest verifier cannot yet prove overlay ROM/VMA/section layout. |
| P5 | Ghost Toys entrance | Historical 140-byte draft retains two incorrect stack offsets; `decomp/GHOST_TOYS_CHECKPOINT.md` documents them. |

Use `compare_original.py` with a SHA-verified decompressed reference and private original assembly for reproducible, relocation-aware isolated codegen diagnostics. A structurally matching isolated object is never a complete-ROM promotion. Ten parser/negative-control tests passed; see current PROGRESS.md. Do not rerun the unchanged 762-function scalar sweep. After a failed candidate, preserve the mismatch, improve a concrete typed declaration or code shape, and move to another target. Promotion requires the exact original-address MIPS bytes **and** independent full decompressed-ROM byte identity.

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

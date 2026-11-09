# Next ten matching-C functions — evidence-ranked execution plan

Authoritative starting checkpoint (2026-11-09): **142 newly matching C / 10,652 exact MIPS bytes; 13 upstream C; 155 combined C; 7,221 ASM** of 7,376 identified. The latest live proof is an independently recreated 2,331-object, 33,554,432-byte exact decompressed ROM build (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`). **Uninterrupted `decomp.verify` remains pending (`formal_verifier_run_completed=false`).** Verify current branch HEAD, `AGENTS.md`, `CONTINUE.md`, `MASTER_WORK_QUEUE.md`, `manifest.json`, `results/combined.json` and `results/inventory.json` on *each run*; replace these dated totals with newer repository proof when it exists.

## Execution status — 2026-11-09

**All ten of ten targets investigated; zero of ten promoted.** The two 11-command graphics emitters and the 192-byte VM setup function have standalone C candidates and synthetic tests. Neither graphics emitter matches original IDO instructions (440→516 B and 436→500 B); a volatile cursor reduced them to 480 and 464 B but did not increase direct positional matching. The setup source compiles to the original 192-byte extent but differs in float register/argument scheduling (5/18 directly comparable words match). All 267 original MIPS words were checked against the verified USA ROM; 4,300 mock-host scenarios and four parser negative tests passed. Full evidence: `results/vm_next_ten_batch1.json` and dated `PROGRESS.md`. **Target #4:** `func_8003E6C0_3F2C0` has a private-ROM-verified 348-byte original and a nonmatching 400-byte C candidate (0/52 directly comparable positions; 34 relocation-layout differences), with 400/400 synthetic host cases. `results/vm_next_ten_batch2.json` records the evidence. **Target #5:** fourteen codegen variants for the 232-byte command walker failed exact matching; the closest registered out-of-line negative C remains 228 bytes / 8 of 35 direct comparable instructions. Seven variants passed 8,400 total mock-host scenarios. See `results/vm_next_ten_batch3.json`. **Target #6:** isolated native IDO text-loop alias source reproduces 472 bytes/53 direct matches; ten targeted codegen variants did not improve it, and reassembling compiler `.s` differs from native output. See `results/vm_text_loop_native_codegen_probe.json`. **Targets #7–#10:** all investigated, with new 196-byte/25-of-42 direct-match resource lookup probe and correction of wrapper original extent to 48 bytes. See outcomes below. No promotions; next priority is #8 codegen, then deferred targets.** The uninterrupted formal verifier remains pending. No matching-C promotion; 142/10,652/7,221 remains authoritative.

## Outcomes #7–#10 — 2026-11-09

The next-ten *investigation* is complete; no function has passed the original-address and full-ROM promotion gates. Current proof remains **142 C / 10,652 MIPS bytes / 7,221 ASM**, and uninterrupted formal verification remains pending.

| Target | Original ROM extent | Native IDO research result | Decision |
|---|---:|---|---|
| #7 Loader `func_8003D468_3E068` | 548 B | 556-byte canonical C; 1/26 directly comparable MIPS positions; ten targeted interface/alias trials | Unpromoted |
| #8 Resource lookup `func_8003F038_3FC38` | 196 B | **New 196-byte signed-half-index volatile probe, 25/42 direct positional matches**; 3,000 mock tests each for original and new C | Unpromoted; strongest next codegen target |
| #9 Digit formatter `func_8003F480_40080` | 164 B | 160-byte native candidate; none of fifteen focused variants reproduced `bnel` | Unpromoted |
| #10 Wrapper `func_8003F6E8_402E8` | **48 B / 12 original words** | 40-byte prefix matches 9/9 direct and 1/1 call relocation shapes; trailing `jr $ra; nop` absent | Unpromoted |

**Correction:** #10's original archived Splat span is **48 bytes**, not 56. The earlier 56-byte number is a *candidate inventory size* annotation, not the original span. `test_vm_wrapper_extent.py` now rejects this confusion. Source-level C never claims an unreachable 8-byte tail without full exact codegen.

Native IDO `-c` output can differ in size from an IDO-generated `.s` file reassembled with GNU Binutils; compare native-pinned ELF as the source of codegen truth. All four results, method caveats and original SHA-256 evidence are in `results/vm_next_ten_batch4.json`. The highest-value continuation is the improved #8 register/stack allocation, then the deferred high-call-count VM routines and formal verifier.

## First: verification prerequisite (not a function)

Restore a clean pinned build environment using the user's private retail USA ROM (SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`), pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, IDO 5.3, Splat 0.36.3 and pinned GNU MIPS Binutils `2.45.90.20260125`. Regenerate the archive's known CRC-damaged generated `candidate/asm/usa/file_72.s` using Splat from the verified ROM; never invent its bytes. Attempt one uninterrupted `python -m decomp.verify` against the **current 142-function source**, following `CONTINUE.md`. If incomplete, leave its completion flag false and retain independent proof as independent proof. Do not block bounded C research if the formal runner remains unavailable.

## Selected ten functions, in order

The ten names below are **13 current VM ASM placeholders minus three deliberately deferred high-cost functions**. Each function was cross-checked as unpromoted in the live manifest. The original function words in the recovered private archive were independently checked against the SHA-verified decompressed USA ROM. Sizes below are original instruction extents except for the symbol-boundary uncertainty described in #10.

| Priority | Function | Original bytes | Technical approach and measurable target |
|---|---|---:|---|
| 1 | `func_8003E234_3EE34` | 440 | **Display-list emitter**, no calls. Recover the exact ordered two-word graphics-command stores, pointer increments, array indexing, register reuse and return delay slot; test a mock display-list buffer and first/last emitted words. |
| 2 | `func_8003EBAC_3F7AC` | 436 | **Related display-list emitter**, no calls. Reuse only the *confirmed* buffer/command structure from #1; preserve different resource pointers, opcode constants, store order and exit delay slot. Build independently; do not mass-convert with untested macros. |
| 3 | `func_8003F37C_3FF7C` | 192 | **VM setup/callback registration** with three calls, one return and floating-point stores. Establish actual float/value widths, 0x50-byte stack frame, call arguments and callback pointer values, then use exact isolated codegen comparison. |
| 4 | `func_8003E6C0_3F2C0` | 348 | **VM callback/setup path**, four calls, three conditional branches. Derive typed VM structures and callback sequencing from original loads/stores; host-test both sides of each branch and callback-modified globals. |
| 5 | `func_8003DE80_3EA80` | 232 | **Command walker**. Start from the out-of-line negative-arm research C in `candidates/vm_command_walker_goto_probe.c` (228 compiled bytes; 8/35 directly comparable positions). Match the original `bltzl` conditional delay slot and `$s0/$s1/$s2/$s3` lifetimes, without changing semantic exit paths. Retain the 1,200-case mock harness. |
| 6 | `func_8003DBEC_3E7EC` | 472 | **Text loop**. Start from `candidates/vm_text_loop_alias_probe.c` (original symbol size, 53/95 comparable nonrelocation positions). Resolve its six branch-likely slots, original 0x48 versus compiled 0x50 frame, callback reloads, +0xA VM-work halfword, controller unsigned +2/+4, retry vs outer counters. Preserve its 10,000-case differential harness. |
| 7 | `func_8003D468_3E068` | 548 | **Resource loader**. Preserve two distinct global resource-ID reloads after callbacks and the saved *entry* ID used by `func_8003DDC4_3E9C4`; reproduce the original 32-byte frame with saved `$s0/$s1`. Existing typed research draft is 560 bytes; use the 400-case and 1,024-case mutation harnesses, not the obsolete 118/137 positional claim alone. |
| 8 | `func_8003F038_3FC38` | 196 | **Signed halfword resource lookup**. Reconstruct `arg==0x100` bypass, negative division-by-two truncation, two resource calls, optional recovery, and wrapped shifted offset. Current research compiles to 204 bytes; retain 3,000 host cases and original-address control-flow guards. |
| 9 | `func_8003F480_40080` | 164 | **Number-to-halfword formatter**. Restore the original `sprintf` argument registers and `bnel` next-character delay slot. Current size-only C is 164 bytes but matches only 3/19 directly comparable nonrelocation positions; retain the 1,000-case sanitizer harness and 15 original-assembly guards. |
| 10 | `func_8003F6E8_402E8` | **48 baseline*** | **Choice wrapper and unreachable tail**. The **original archived assembly is 48 bytes / 12 words**; reconcile the **56-byte candidate inventory annotation** separately. The earlier natural C reproduced only a 40/48 prefix. Require exact full claimed original address range and layout proof; never promote a prefix or pad with manufactured instructions. |

* #10 is a **symbol extent/layout investigation before C promotion**. Count only verified original function bytes. The provisional sum of the ten baseline extents is **3,076 bytes**. The original 48-byte extent is ROM-verified; the inventory's 56-byte candidate annotation does not redefine it.

## Deferred after these ten

- `func_8003D68C_3E28C`: 812-byte VM routine; 22 calls, seven branch/jump sites and three branch-likely instructions. Defer until supporting interface types stabilize.
- `func_8003DF98_3EB98`: 528-byte VM routine with 21 calls; defer until callback/lookup declarations from the smaller functions are validated.
- `func_8003ED60_3F960`: 592-byte command/graphics path with two calls into `func_8003F038_3FC38`, and two branch-likely instructions. Revisit after #8.
- The separate 96-byte overlay initializer `func_080001BC_6F369C` retains its isolated-linked match but requires explicit overlay ROM/VMA/section-layout proof, not the main-segment manifest shortcut.

These are *not* abandoned. They are deferred to avoid losing runs to high-call-count and layout-blocked targets before shared semantics are established.

## Unit-of-work rules for each of the ten

1. **Evidence:** Recheck current remote HEAD and proof/manifest. Recover private original instructions from the SHA-pinned ROM, verify exact ROM offset/VMA and symbol boundaries, and inventory each read, write, callback, return and delay slot. Never trust an older chat count over the repository.
2. **One change at a time:** Write a separate research C candidate or adjust one evidence-based code shape, declaration, alias assumption or register lifetime. Compile with **pinned IDO 5.3** flags `-O2 -mips2 -G 0 -non_shared`, then GNU MIPS Binutils. Compare via `decomp/compare_original.py` with relocation-aware diagnostics. A matching function *size* or masked relocation shape is **not** an exact match.
3. **Bounded exploration:** Spend a substantive unit identifying the strongest mismatch cluster, then run a few targeted variations (typically up to four) and measure both instructions and behaviour. If none improve a grounded condition, write the specific blocker and move on instead of rerunning generic no-op/permuter sweeps. Never regress a previously verified integration.
4. **Behaviour:** Add targeted host unit tests, ASan/UBSan when supported, and negative controls for pointer/sign/callback edge cases. Original-MIPS differential checks when feasible are stronger than mocks, but neither is an in-game test.
5. **Promotion gate:** Claim the function only after exact original-address/code bytes **and** an independent, complete **33,554,432/33,554,432-byte** decompressed ROM comparison with SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; verify all formerly claimed functions, the 2,331-object build, readelf inventory and ELF metadata/source guards. Do not alter `results/combined.json` or the counts for a failed isolated candidate.
6. **Record/push:** In the same commit as each change, update root `PROGRESS.md` with date, actual commands/tests, limitations and next target; update `CONTINUE.md`/work queue when priorities change. Push **only** `chatgptweb/decomp` after a remote-SHA race check, never force-push. Keep ROM, game assets, original/generated assembly, binaries, toolchains, save data, private paths and diagnostics off GitHub. Do not touch `main`, native warps or story flags.

## Expected milestone (conditional, not a current claim)

If **all ten** selected functions become independently ROM-verified at their baseline sizes: **152 newly matching-C functions; 13,728 exact newly matched bytes; 165 combined C entries; 7,211 ASM entries**. This is an objective, **not** a forecast or automatic counter increase. If fewer than ten meet full acceptance, report only the functions genuinely promoted and move to the deferred queue or broader inventory for the next bounded target.

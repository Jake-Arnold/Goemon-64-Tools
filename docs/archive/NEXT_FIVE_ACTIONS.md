**HISTORICAL / CLOSED PLAN (9 November 2026).** This five-action batch is not an active work queue. Its original 142-function figures and pending-G2 statements are preserved only as dated research evidence. Use [CONTINUE.md](CONTINUE.md), [current README](README.md) and live region-specific proof before selecting new functions.

---

# Next five decomp work packages — 2026-11-09

This is a **five-step technical work plan, not five pre-verified C promotions**.

## Execution checkpoint — 2026-11-09

**The five tasks have been worked through, but none meets every completion gate.** Task 1 is blocked by the locally available archived source containing 136 claims versus 142 on the live branch; no uninterrupted formal verifier run. Task 2's six native IDO lookup experiments did not improve the existing 196-byte/25-of-42 candidate. Task 3 now has a fail-closed private-ROM reference validator for overlay `file_43` (**19 tests passed**, both planned original functions' full bytes verified), **not yet integrated linked-ELF C provenance**. Task 4's 96-byte key initializer retained isolated-linked match and six host mock cases passed, but it is unpromoted. Task 5's new 140-byte Ghost Toys C research draft passed 800 mock scenarios but differs from MIPS and does not supersede the earlier two-byte-near-match. Detailed evidence: `results/next_five_execution_checkpoint.json` and `PROGRESS.md`.

**Authority unchanged:** 142 exact C / 10,652 MIPS bytes / 7,221 ASM. Formal verifier still pending; no overlay promotion or new whole-ROM reconstruction. Next prerequisite is a full current-source checkout and safe linked-overlay proof.

 Use live `chatgptweb/decomp` plus `AGENTS.md`, `CONTINUE.md`, `MASTER_WORK_QUEUE.md`, `manifest.json`, `results/combined.json`, and `results/inventory.json` as the authority on every run.

**Live checkpoint on plan creation:** 142 matching-C functions / 10,652 original MIPS bytes; 13 upstream C; 155 combined C; 7,221 remaining ASM out of 7,376 identified. The existing independent 2,331-object ROM rebuild proved a **33,554,432-byte** exact image, decompressed SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; `formal_verifier_run_completed=false`. The just-completed ten-function investigation yielded **zero new promotions**, but established the candidates described below.

## 1. Complete the uninterrupted 142-function formal verification

**Why first:** the last independent ROM proof is strong but the formal `python -m decomp.verify` run was interrupted. This is a verification debt, not a request to re-promote the 142 functions.

- Restore a clean checkout of the exact live decomp branch, verified 16 MiB retail USA ROM (SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`), pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, Splat 0.36.3, IDO 5.3, and GNU MIPS Binutils `2.45.90.20260125`. Regenerate the archived CRC-damaged assembly via Splat; never repair it with invented bytes. Check cache provenance and source hashes.
- Execute one **uninterrupted** formal verifier with a new isolated workdir/report and complete 2,331-object build, then inventory and all 142 original-address function comparisons. Confirm 32 MiB ROM identity, total function-entry identity and no altered symbol/data/ELF layout. Keep command logs and private files outside Git.
- **Done only when:** actual formal invocation finishes successfully, reports are reviewed and committed proof accurately records the observed result. If environment/bootstrap fails, record the exact blocker, leave `formal_verifier_run_completed=false`, and proceed to #2 without claiming formal success.

## 2. Finish the 196-byte VM resource lookup codegen

**Function:** `func_8003F038_3FC38`, original ROM `0x3FC38`. Best source: `candidates/vm_resource_halfword_volatile_probe.c` (Git blob `c227b09be6e832edc2691f735025781932b268d0`).

- Reproduce **pinned native IDO `-c`** output of 196 bytes, **25/42 directly comparable nonrelocation positions**, 3/3 same-kind relocation instruction shapes, **four remaining relocation-layout differences**. Do not compare an IDO-emitted `.s` that has been reassembled with GNU as if it were native IDO output.
- Disassemble original and candidate at each mismatch. Work on the original `$v1` half-index register versus the candidate `$t6`, saved/spilled argument slots, and signed division truncation. Change **one** evidence-supported declaration, alias or live-range assumption per isolated build; limit successive nonimproving experiments and retain failure data.
- Rerun `test_vm_resource_halfword_probe.c` (3,000 deterministic cases per selected source) under ASan/UBSan and `test_vm_resource_halfword_volatile_probe.py`, alongside private original-ROM instruction guards. Include callback-mutated state and integer-wrap negative controls as warranted.
- **Done only when:** exact original-address machine words are reproduced and the newly integrated complete ROM remains byte-for-byte identical. Otherwise leave it research-only with unchanged function counts, recording the strongest mismatching instructions.

## 3. Add bounded overlay ROM/VMA and section-layout verification

**Why before overlay promotions:** `decomp.verify` and the manifest currently accept **main-segment mappings only**. A 96-byte overlay function has a successful isolated linked probe, but the proof system cannot safely promote it yet.

- Model overlay ID, original ROM offsets, virtual load addresses, section boundaries and relocation/layout metadata explicitly; use the pinned Splat map and original ELF data. Make the default main-segment verifier unchanged.
- Add fail-closed tests for wrong overlay ID, ROM/VMA mapping, overlap with another segment, shifted text/rodata/data sections, duplicate functions, no-padding edge cases and wrong full-ROM SHA-1. Support only an independently verified overlay layout, not a generic bypass.
- **Done when:** a representative overlay candidate can be compiled and linked at its actual ROM/VMA positions and compared against original instructions, with regression tests for both ordinary main-segment and overlay cases. No overlay match count may rise from a verifier feature alone. If exact mapping is unresolved, stop at research/test infrastructure; do not relax checks.

## 4. Integrate the 96-byte overlay key initializer if exact

**Function:** `func_080001BC_6F369C` at ROM `0x6F369C`; source `candidates/key_spawn_gate.c`. The historical **96-byte isolated linked match** is not yet a whole-ROM match.

- Recheck the actual overlay entry, task `+0xD4` field width, symbolic engine call addresses, callback pointer and relocations against the private pinned original.
- Once #3 proves the overlay layout, stage *only* this exact C function while retaining adjacent overlay ASM and assets byte-for-byte. Test both key-collected and key-uncollected host callback paths.
- **Done only when:** all 96 original bytes at `0x6F369C`, all previously matched main-segment functions, the overlay layout, full **33,554,432-byte** ROM and inventory prove identical. Otherwise preserve the isolated match as unpromoted research.

## 5. Resolve the 140-byte Ghost Toys overlay entrance mismatch

**Function:** `func_08006490_6F9970`, overlay file `0x02B`, ROM `0x6F9970`. See `GHOST_TOYS_CHECKPOINT.md` and `results/ghost_entrance_candidate.json`.

- Confirm the original 140-byte / 35-word extent and the *two* known mismatching stack displacements: original **`sp+0x1C`**, candidate **`sp+0x18`** in store and reload positions. This is a compiler spill/live-range problem, not an invitation to patch opcodes.
- Use one original-ABI-based pointer-lifetime/stack-layout change per pinned IDO 5.3 probe; compare the exact linked original words under the verified overlay mapping from #3. Retain logic for the native three story flags, task flags and callback transition without modifying speedrun toolkit features or `main`.
- Run synthetic host tests for both flag conditions and relevant callback behavior. **Done only when:** both differing instructions compile exactly, complete 140-byte function address identity passes, and the whole-ROM/overlay/inventory gates pass. If not, keep the known two-byte mismatch documented and stop bounded experimentation.

## Common controls and sequencing

1. Before every unit, check the **current** remote `chatgptweb/decomp` HEAD, root `AGENTS.md`, both runbooks, current manifest and proof/inventory; adapt this plan if another contributor has already completed a task. Never rewrite `main`, reset worktrees or force-push.
2. Keep copyright ROMs, game assets, private original/generated assembly, toolchains, object files, saves and diagnostics out of Git. Use `compare_original.py` for isolated codegen *research*, native IDO `-c` for compiler comparisons, and the independent full-ROM gate for **promotions**.
3. Distinguish synthetic host tests, original-MIPS differential tests, exact original-address instructions, complete-ROM rebuilds, formal verifier completion and in-game testing. Never infer one kind of evidence from another.
4. Every code/doc change needs a dated root `PROGRESS.md` entry with test commands/results and limitations. Commit and push only `chatgptweb/decomp` after a remote-SHA race check; verify the remote commit.
5. If #3 cannot establish valid overlay section placement, perform #4 and #5 only as bounded **unpromoted research** and retain exact evidence. Do not fabricate a linked ROM or advance counts to satisfy a checklist.

**Conditional milestone:** if #2, #4 and #5 all pass original-address and whole-ROM identity independently, that would be **145 newly matching C / 11,084 exact MIPS bytes / 158 combined C / 7,218 ASM**. This is *not* a prediction or current verification result. If only some pass, report exactly those promotions; the other work packages can still complete as validation/research.

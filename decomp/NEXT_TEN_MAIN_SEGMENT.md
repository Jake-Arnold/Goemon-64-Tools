# Next ten new main-segment matching-C targets — 2026-11-10

**Historical research report, reconciled 2026-11-11:** the six resource, menu,
and object functions documented here have since passed native unit and complete
ROM gates. The remaining four short candidates are still unpromoted and are now
G64-015–018. Use `decomp/CONTINUE.md`, `decomp/manifest.json`, and the current
result reports for live counts; the original isolated-research records below
remain unchanged as historical evidence.

**Current execution sequence:** [NEXT_TWENTY_STEPS.md](NEXT_TWENTY_STEPS.md) (20 gated integration/research steps, 2026-11-10). This file preserves the ten-target inventory and historical isolated codegen findings. **Plan, not promotion.** This replaces the *active investigation order* after the previous ten-target list was fully investigated without new matching functions. Keep the earlier evidence in `NEXT_TEN_FUNCTIONS.md` and `NEXT_FIVE_ACTIONS.md`. This new sequence selects **ten distinct, previously unpromoted main-segment assembly functions** from the latest `chatgptweb/decomp` manifest, none from the previous ten-target batch. The plan deliberately favors small functions with concrete ABI/alias conditions instead of another generic scalar sweep.

## Implementation checkpoint — 2026-11-10

**Seven of ten investigated; three exact in isolated original-address links; zero newly promoted.** The refreshed branch's formal verifier now reports **142/142 original-address functions and 33,554,432-byte ROM identity** (`formal_verifier_run_completed=true`), superseding the historical *pending* note below. #1 engine reset and #2 state writer have nonmatching IDO codegen drafts. **#3 and #4** resource wrappers natively compile and separately link to **36/36 exact original bytes each**. #5 and #6 file-table helpers are correct-size in preliminary native IDO C but instruction registers/branches differ. **#7** object dispatcher natively links to **48/48 exact original bytes**. The exact three-function source and fail-closed proof script are under `candidates/` and `prove_three_wrappers.py`; their host mock suite passed **30,000/30,000** and seven proof negative controls passed. These functions are **NOT** part of the production manifest or new complete ROM proof; do not count them as matching-C until an independently rebuilt 2,331-object full-ROM link and inventory pass after integrating them into their original production units.

**Next:** integrate #3, #4 and #7 only when the full latest checkout can be independently rebuilt, and continue menu-state #8–#10 as separate bounded research. See `results/next_ten_main_wave1.json` and dated `PROGRESS.md`.

## Final next-ten investigation checkpoint — 2026-11-10

**All 10/10 functions investigated; SIX exactly matching in isolated linked source builds; ZERO promoted.** The three formerly unpromoted resource/object wrappers (36+36+48 = 120 B) plus the three new menu routines (84+80+84 = 248 B) total **368 original MIPS bytes** reproduced by pinned native IDO 5.3 and independently linked with `ld.lld` at their original addresses, comparing all code bytes against the SHA-pinned ROM. See `results/next_ten_main_wave1.json` and `results/next_ten_main_wave2.json` and the associated standalone C/proof/host tests. Behaviour: 30,000 wrapper synthetic cases and 90,000 menu synthetic cases passed; seven shared proof negative tests passed.

This is a **codegen/link-layout research milestone, not a matching-C promotion**: candidate C is still outside production units, the complete 2,331-object project build has not been rerun with it, and the manifest/verification counts must stay at **142 verified functions / 10,652 exact MIPS bytes / 155 combined C / 7,221 ASM**. The previous contributor's formal 142-function verifier result remains completed. Next work is full integration with exact unchanged 32 MiB image and readelf inventory, then promotion; **never** treat these 368 research bytes as a new verified ROM count.

## Starting proof and independent original-byte checks

At branch planning HEAD `edea9d606eaf4de0c8f181f73e5ad0e6ff169d28`: **141 newly reconstructed unit functions + 1 reviewed upstream C source patch = 142 verified matching-C claims / 10,652 original MIPS bytes**, plus 13 upstream C = 155 combined C and **7,221 remaining ASM** of 7,376 identified. The previously recorded 2,331-object independent full-ROM identity is for **33,554,432 bytes**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; **uninterrupted formal `decomp.verify` remains pending**.

Research preflight on this plan: read the actual original assembly spans from the user's private archived Splat checkout (not the known corrupted `file_72.s`), checked contiguous ROM/VMA addresses and size annotations, then compared every one of the **132 original instruction words (528 bytes)** with the separately archived decompressed original ROM. Verified the reference has exactly 33,554,432 bytes and SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. All **132/132 words matched**. Each of the ten function names also exists in the current manifest's `assembly_functions` and not its matching-C claims. Private assembly, ROM and binary bytes are never uploaded to GitHub.

## Ordered candidate list

| # | Function | Existing C unit | Original extent | Calls | Conditional branches |
|---|---|---|---:|---:|---:|
| 1 | `func_8003A1E8_3ADE8` | `engine_state.c` | 28 B | 0 | 0 |
| 2 | `func_80006274_6E74` | `state_predicate.c` | 36 B | 0 | 0 |
| 3 | `func_80034ED4_35AD4` | `resource_dispatch.c` | 36 B | 1 | 0 |
| 4 | `func_80034F20_35B20` | `resource_dispatch.c` | 36 B | 1 | 0 |
| 5 | `func_80001D94_2994` | `file_table.c` | 44 B | 0 | 0 |
| 6 | `func_80001DC0_29C0` | `file_table.c` | 52 B | 0 | 1 |
| 7 | `func_80035094_35C94` | `object_dispatch.c` | 48 B | 2 | 0 |
| 8 | `func_80011BB4_127B4` | `empty_menu_hook.c` | 80 B | 0 | 2 |
| 9 | `func_80011B60_12760` | `empty_menu_hook.c` | 84 B | 0 | 2 |
| 10 | `func_80011C04_12804` | `empty_menu_hook.c` | 84 B | 0 | 1 |

## Reconstruction notes and test gates

### 1. `func_8003A1E8_3ADE8` — 28 bytes

Reset global 16-bit state at `D_801C09D8` and byte state at `D_801C09DA` through the original two address-forming sequences; preserve separate `sh`/`sb`, nonvolatile semantics and the return delay slot. Host guard: adjacent fields unchanged.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `67a34a9f05ad07e9b774a39beb484f80f3207f0287120a29b3357af426608838`. Original guest-address and ROM offset are encoded in the function name.

### 2. `func_80006274_6E74` — 36 bytes

Model original global pointer arithmetic and three stores (`sh` flag, `sh` argument, `sw` argument) without a stack-frame allocation; test target widths, offsets and final `sw` in the `jr $ra` delay slot. Verify alignment after base adjustment, not by interpreting the immediate offset alone.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `0fe46b7b771a77a3a4c6e4354902ef27f6211fae3a1ce22839657fa8cdaf1102`. Original guest-address and ROM offset are encoded in the function name.

### 3. `func_80034ED4_35AD4` — 36 bytes

Call existing `func_80034EF8_35AF8` with the current `D_8016DAB4` value; reproduce the original 0x18 stack frame, `$ra` spill and `lw $a0` in the `jal` delay slot. Host guard: exactly one call with current global value.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `b6e4ba1efa16865b5ae60da5cb79335e06098a2e2771be5b53cc99252d21531a`. Original guest-address and ROM offset are encoded in the function name.

### 4. `func_80034F20_35B20` — 36 bytes

Companion wrapper calling `func_80034F44_35B44` rather than `func_80034EF8_35AF8`; keep identical ABI/delay-slot structure but prove it independently. Reuse only verified types and test callback target/argument, not compiled bytes.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `e014867b2e08c89e528e37e0545ac991cd13ce8c105395bffee9be375c9e555e`. Original guest-address and ROM offset are encoded in the function name.

### 5. `func_80001D94_2994` — 44 bytes

Read the second file-table base (`D_800573D8`) indexed by the low 16 bits of the argument; preserve repeated `0x7FFFFFFF` masking and the unusual argument spill in the return delay slot. Compare with already reconstructed sibling `func_80001D68_2968` but do not assume identical base addresses.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `1708e270ec47ebaa4b84177baef1a38736e0c8accb9ce6705d32b7ce4234f05b`. Original guest-address and ROM offset are encoded in the function name.

### 6. `func_80001DC0_29C0` — 52 bytes

Return zero when index is zero; otherwise return the unsigned wrapped difference of the two adjacent word fields for the `index-1` eight-byte entry. Preserve `beqz` delay-slot shift and `subu` in the other return slot. Host tests: zero, first and last valid entries, underflow/wrap.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `7bd81c0b44f1e99efbea292e7ebb54379950980f869c9531fce274baabff9ebd`. Original guest-address and ROM offset are encoded in the function name.

### 7. `func_80035094_35C94` — 48 bytes

Call `func_800362DC_36EDC` with `D_8016DAB4`, then `func_800350C4_35CC4` with the original saved argument. Preserve the 0x18 frame and `lw` call delay slots; test order and that callback-mutated global state does not overwrite the saved argument.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `7f8f2a83dbc5179d76609db3b186ea481e9aa78bd0b1e6f46ceb798637fe0c36`. Original guest-address and ROM offset are encoded in the function name.

### 8. `func_80011BB4_127B4` — 80 bytes

Menu disable: independently guard both pointers, clear bits `0x14` from halfword `+0x22`, zero byte `+0x64`, clear bit `0x80` at byte `+0x4`. Preserve reloaded pointer accesses and two branch delay slots; test null pointers and unrelated bits.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `e001c012b652a5dadd7923706e8728b51a3bce9203c0f0a2130114b831524a52`. Original guest-address and ROM offset are encoded in the function name.

### 9. `func_80011B60_12760` — 84 bytes

Menu enable twin: guard the same two pointers; set halfword bits `0x14`, write `1` to byte `+0x64`, set bit `0x80` in byte `+0x4`. Check pointer reloads, stores and register scheduling separately from #8.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `5573013c23b198d920562b122776d0d45e5e9d999bd2bce92cf2051493652ec6`. Original guest-address and ROM offset are encoded in the function name.

### 10. `func_80011C04_12804` — 84 bytes

Alternate menu update: compute pointer through global index plus `0xC8000` and field `+0x78E8`, guard null; set bits `0x14` at halfword `+0x22` and `0x80` in linked byte `+0x4`. Distinguish actual nested-pointer reads and base reloads from #8/#9.

Original function SHA-256 (private archived assembly cross-checked byte-for-byte with the SHA-pinned ROM): `72715c034f10313d627651394040a836581fed4a3fdda8241556bd38268055bb`. Original guest-address and ROM offset are encoded in the function name.

## Verification prerequisite and work cadence

**Before a new promotion:** restore the complete current **142-function** source checkout; the old archive contains only 136 reconstructed functions and cannot certify the current branch. Run the corrected `tests/test_decomp_verify.py` and `decomp.test_compare_original` (the historic stale-count/regex failures were fixed in commit `edea9d6`). Execute an uninterrupted formal `python -m decomp.verify` and inventory when the complete pinned Splat 0.36.3 / IDO 5.3 / binutils `2.45.90.20260125` environment is available. Do not mark the formal completion flag true on a partial run. An incomplete formal run does not authorize a promotion; an independently complete, current-source full-ROM test is mandatory for every newly promoted function.

For **each candidate**, follow this bounded sequence:

1. Check live remote HEAD, `AGENTS.md`, `CONTINUE.md`, `MASTER_WORK_QUEUE.md`, the manifest and current proof. Recheck the private original code against SHA-verified ROM. Confirm it is still ASM and has not been promoted concurrently.
2. Write minimal typed C in the existing source unit, or an isolated research candidate if codegen is not close. Confirm size and full instruction/relocation identity with **pinned native IDO `-c -O2 -mips2 -G 0 -non_shared`**; do not substitute GNU reassembly of compiler-emitted `.s`, which previously changed branch-delay scheduling. Use corrected `decomp/compare_original.py` for diagnostic matching only, not promotions.
3. Test actual behaviour with bounded host mocks and negative controls; do not conflate mocks with original-MIPS differential tests, original-address ELF identity or game execution. Check side effects, signedness, volatile/global reloads, callback side effects, and exact branch delay slots. Preserve all original ASM not yet replaced.
4. Promote only after **exact original-address machine instructions and relocations**, no unreviewed changed sections, complete **33,554,432/33,554,432-byte ROM identity**, all previously claimed 142 functions and inventories still valid, and the full ELF/2,331-object proof. Record exact new count/bytes from verified evidence in manifest and reports only after that gate passes.
5. Limit exploratory variants to a few evidence-based assumptions per attempt; record precise mismatches and advance when blocked. Update root `PROGRESS.md` in every commit; push only `chatgptweb/decomp` with non-force remote-SHA race protection and independent remote SHA confirmation. Keep private ROMs, original/generated ASM, toolchains, objects, saves and diagnostics out of Git; never modify `main`.

### Dependency groups and fallback queue

- **#1–#2:** scalar state writes with no callbacks; validate byte/halfword widths and delay-slot codegen first.
- **#3–#4:** paired resource wrappers; their 36-byte code differs only in callee, so test the common ABI while requiring independent original-address matches.
- **#5–#6:** adjacent file-table helpers; validate masking, unsigned arithmetic and the unusual return delay slots without copying a sibling's globals.
- **#7:** two-call object wrapper; ensure saved entry argument survives a callback that may mutate globals.
- **#8–#10:** clustered menu flag handling; shared structure tests must not obscure separate original MIPS scheduling and pointer reloads.

If multiple new small functions stall, use reviewed fallback **`func_8000EA74_F674` (72 B)** or **`func_8000EB08_F708` (72 B)** from `angle_variant.c`, after independently rechecking original ROM extents and live ASM status. These are *fallbacks*, not additional claimed targets. The three high-call-count VM functions `func_8003D68C_3E28C`, `func_8003DF98_3EB98`, `func_8003ED60_3F960` remain deferred, as do overlay key/Ghost Toys promotions until linked-overlay source ownership and complete ROM gates are supported.

## Conditional milestone only

If **all ten** pass exact original-address and full-ROM proof, the conditional result would be **152 matching-C / 11,180 newly matched MIPS bytes / 165 combined C / 7,211 remaining ASM**. This is a stretch outcome, not a prediction or a promotion. Actual counts must reflect only individually completed, independently verified functions.

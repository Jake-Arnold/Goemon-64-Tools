# USA Mini clamp: exact original trig-call and angle stack layout, no post-call copy

**21 November 2026 — FAILED_NATIVE / RESEARCH_ONLY.** No matching-C promotion.

Target original USA `func_801CD310_589220`, ROM `0x589220`, guest VMA `0x801CD310`, `file_11`. Pinned SGI IDO 5.3 native C `-O2 -mips2 -G 0 -non_shared`. Original extent **4,320 B**, frame **232 B**.

## Source-level change and independently verified original offsets

The previously exact-trig-call candidate used `union { u16 switch_angles[2]; f32 vecA[3]; }` and copied the first angle to a second stack slot immediately after the trig calls. Original MIPS instead keeps its first angle at `sp+0x6E` until a later `lhu` at `+0x47C`, without the post-call copy. The new source keeps the angle pair and a float trig return adjacent in an object that shares storage with **later `vecC`**, whose first access comes *after* all pair/trig-return uses. The first angle is read directly where it is needed, before the vector reuse. Moving a pre-existing float declaration next to this object shifts IDO's stack layout by four bytes without introducing a new live variable.

The **complete 23,009-byte native compilable C source**, SHA-256 `40714651e898315361dd0e4b70e241c305cd4ced062f9fc193db1cde08b468b5`, is permanently stored in this draft PR as the **source-only gzip** file `angle_stack_exact_20261121/exact_early_stack_no_copy.c.gz` (gzip SHA-256 `3e8467edf39c8e60e2296fb30dc70c780cd2153744c7caa026e36c2e8d96be08`; Git blob `3830c92d8687a1d18c64d88655996864b9e8f591`). Restore via `gzip -dc exact_early_stack_no_copy.c.gz > exact_early_stack_no_copy.c`. This file contains reconstructed research C only; **no original ROM, disassembly, assets, ELF/object or proprietary toolchain**.

| Exact original MIPS property | Original | Native recovered |
| --- | --- | --- |
| First trig JAL (original target `func_80003EA0_4AA0`) | `+0x19C` | **exact** |
| Second trig JAL | `+0x1A4` | **exact** |
| Second-call branch delay `lhu a0` | `+0x1A8`, `sp+0x6C` | **exact instruction word** |
| First-angle halfword storage | `sp+0x6E` | **same slot** |
| Second-angle halfword storage | `sp+0x6C` | **same slot** |
| Second trig return `swc1 f0` | `+0x1B0`, `sp+0x64` | **exact instruction word** |
| Frame | 232 B | **232 B** |
| Extra first-angle reload/store after second call | absent | **absent** |

The original and candidate MIPS words agree at **`+0x1A0`, `+0x1A8`, `+0x1AC`, `+0x1B0`**, with both genuine trig-call relocation offsets exact; the candidate later first-angle load occurs at `+0x464`, from the correct `sp+0x6E` slot, rather than original `+0x47C`.

## Remaining original-versus-candidate mismatch

The **first/second switch-angle store topology is reversed**:

- Original: **five** case-local first-angle halfword stores at `sp+0x6E`; **one** second-angle store at `sp+0x6C` at merge `+0x198`.
- Current C: **five** second-angle halfword case stores at `sp+0x6C`; **one** first-angle store at `sp+0x6E` at merge `+0x198`.

The candidate machine extent is **4,288/4,320 bytes (32 B short)**, **10/889** comparable same-offset nonrelocation words and **4/101** exact original-offset/type/symbol text relocations. The long-lived `$f20` save still differs from original early `$f0` zero at `+0x04`, and the original context `$f14` zero at `+0x1B4` is absent. This is **not whole-function matching C**. The previous copy-containing C has **26/907** same-offset words and **10/101** relocation triples, but the wrong trig/angle slots. Keep both; do not treat isolated stack success as universal global code improvement.

A bounded attempt to assign the *second* angle in each case to an independent `s32/u16` temporary and store it once at the switch merge moved the trig calls **16 bytes early**; rejected. Declaration permutations without a fresh variable moved the grouped stack return to `sp+0x60` and angle to `sp+0x68`; a single scalar declaration-order shift then matched the original `0x64/0x6C` slots with the proper frame. A smaller vector declaration also recovered slots but reduced the frame to 224 B, so it was rejected.

## Actually executed verification

- User retail USA ROM SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, expanded USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. **Unmodified pinned USA rebuild 33,554,432/33,554,432 bytes exact**. This is not a candidate-replaced full ROM.
- Five authentic native IDO 5.3 full-C builds freshly reproduced: `exact_early_stack_no_copy`, `near_stack_no_copy`, `exact_slots_wrong_frame`, prior `previous_copy_baseline` and `failed_second_angle_merge`; measured instruction/ELF/relocation/native layout auditor PASS **expected FAILED_NATIVE** for each.
- Fail-closed original-MIPS gate checks: exact call offsets, original-vs-candidate angle store count, delay-slot `lhu`, `swc1` result store, four exact instruction words, absent extra copy, and later first-angle reload from its original stack slot. **PASS**.
- GCC and Clang independently ran **65,536 switch modes each**, with AddressSanitizer/UBSan, checking angle choices, synthetic trig-call argument order, delayed first-angle read and storage reuse. **PASS** (bounded host fixture only, not complete game semantics).
- Clean source-only archive extraction, SHA256SUMS verification, five IDO native replay builds and GCC+Clang sanitizer replay **PASS**. Companion conversation source archive `GOEMON_CLAMP_EXACT_EARLY_STACK_20261121.zip`, SHA-256 `e281b0f70a4c32d4c65e1a36a90f3419be19829eea53ecc8414bf8df4f4ba9f3`, supplies complete candidate C, all five variants, auditor source, tests and replay scripts.
- Candidate-linked entire USA ROM, current combined `decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci`, emulator gameplay: **NOT RUN** because isolated original-address match fails.

## Next reconstruction

Reconstruct the first-angle case-local stack stores and second-angle merge in **native IDO source**, keeping exact call offsets, original slots and 232-byte frame. Do not chase total function size or use an unproven volatile workaround. Once the full original-address machine words and relocation identity match, and only then, attempt combined original-ROM G2 and full CI. Retain original ASM and PR #144 draft.

Latest independently verified USA production remains **1,965 C / 84,648 instruction bytes / 5,398 ASM** (starting and ending counts equal). `combined.json` and `inventory.json` are older 1,956 snapshots.

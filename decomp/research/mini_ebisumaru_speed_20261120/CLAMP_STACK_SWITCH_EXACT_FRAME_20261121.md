# Mini Ebisumaru 4,320-byte movement clamp — original frame and switch layout (21 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY.** No canonical G2 or matching-C promotion. Target `func_801CD310_589220`, original USA ROM `0x589220`, VMA `0x801CD310`, original 4,320 bytes, original 232-byte stack frame. Original pin `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, authentic IDO 5.3 with pinned `-O2 -mips2 -G 0 -non_shared` flags.

## Native compilation improvements

The prior ABI-corrected source emitted 4,316 bytes but had a 440-byte stack frame. An isolated vector D had become dead under the m2c-derived local-variable model; removing it reduced frame only to 432. A forced fixed-offset struct worsened the frame. Subsequent bounded pooling of lexical non-overlapping `f32`, `f32*`, `u16` and `u8` temporaries reached 304, 280, then the **original 232-byte stack frame**, without inline MIPS, compiler changes or binary patches. **This is a diagnostic source allocation change; source-level aliasing and full control-flow semantic equivalence have not been proved.** Original C still has pointer prototype warnings.

Original MIPS carries incoming third motion argument through `$f12` and saves it at original `sp+0xF0`. The previous second `func_801CE3F0_58A300` call erroneously passed the cap (`arg1`) instead of the saved incoming motion (`arg2`). Passing `arg2` directly corrects the helper argument and restores the matching original stack save. One candidate now reproduces the first **60 original code bytes** up to the first `jal` relocation at offset `+0x3C`.

The original 18-entry `0x8E`–`0x9F` switch had two cases passing through a redundant shared temporary and a backward `goto` in the C draft. Writing their selected value directly to the common target eliminated eight compiled bytes and restored all **18 original jump-table destination code offsets exactly**. This is the structural *case-target position* only; the switch's actual instruction bytes remain nonmatching.

## Verified candidate matrix

| C source (companion ZIP) | ELF FUNC size | Stack frame | 18 switch destinations | Same-offset nonrelocation MIPS | First raw mismatch |
|---|---:|---:|---|---:|---|
| `clamp_frame232_switch_4332.c` | 4,332 B | **232 B** | all exact | 66/912 (846 differ) | `+0x3C` first JAL relocation |
| `clamp_frame232_size_exact_4320.c` | **4,320 B** | **232 B** | all exact | 104/921 (**817 differ**) | `+0x04` floating register selection |
| `clamp_abi_corrected_unpooled_4320.c` | **4,320 B** | 440 B | all exact | 64/917 (853 differ) | `+0x00` frame allocation |

Original in-function `.rel.file_11` contains **101** relocation records. Each native C candidate has **101** text relocations by count/type (33 original call targets in original order, 34 HI16 and 34 LO16); **99 of 101 type+symbol records match in order**, except the HI16/LO16 pair to original `jtbl_8020A85C_5C676C` (native C emits `.rodata`). **Relocation offsets mostly differ**. On the 4,320/232 candidate only 35 relocation records have exactly the original *offset* as well as type/target name. No complete semantic relocation equality is claimed. All nine inline `sqrt.s` and original 18 case groupings are present.

A bounded native IDO matrix of 92 variants modified ordinary `0.0f` to equivalent literal `0` within float-typed contexts. Four generated both **4,320-byte ELF length and 232-byte frame**, but moved the early FP register assignment (first raw difference `+0x04`). The frame-exact 4,332-byte variant retains the stronger 60-byte original raw instruction prefix. These are two independent useful research branches; neither is a full-function original-address native match.

## Reproducibility and limits

Original private USA retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Pinned pristine full-ROM baseline **33,554,432/33,554,432 bytes identical** to original expanded USA ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. **No experimental 4,320-byte clamp C was linked into the retail-equivalent full-ROM image.** Actual tests: original IDO native C compilation and focused MIPS/relocation/jump-table audits PASS for measured properties, original baseline SHA-1 + full comparison PASS, packaged standalone replay PASS, ZIP integrity PASS. Full clamp machine-code match **FAIL**. Combined current `decomp.verify`, strict `decomp.inventory`, full `decomp.local_ci` and emulator gameplay **NOT RUN**.

The original compiler, private ASM/ROM, Splat assets and objects are not committed. Exact research C sources, per-offset instruction ledger, source SHA-256 checksums, type header and read-only replay scripts are available as conversation artifact `GOEMON_CLAMP_STACK_SWITCH_20261121.zip`. Key source SHA-256:
- frame232, switch exact, 4,332 B: `971b7719d65c4a10cabad4605c38b085aa28794bcdd78945992c4dfb09770aaf`
- frame232, size exact, 4,320 B: `7a28a64bbbc16e3be6b6c46fab0742c76a805335b34351cf1a5faf8a128a3ebf`
- ABI-corrected unpooled, size exact, 4,320 B: `54d4dc118bcfc651e1779352ee6cedad88a949e4c2cb4d7506f8b00513382188`

## Next concrete native matching blocker

Original stack allocation and all switch relative destination positions are recovered, but most original-address register selection and stack-slot assignments still diverge. For example original `sp+0xE6` halfword placement versus generated `sp+0xD6`, and original `t3/t4` versus generated `v1/t3` in switch dispatch. **817/921** comparable non-relocation word positions still differ even in the size/frame-exact candidate. Need original basic-block SSA/dataflow and helper signature/lifetime refinement before trying source variants that affect many blocks. Do not reinterpret length/stack/relocation *counts* as a verified matching C function.

Verified production USA at this investigation: **1,956 accepted C / 83,940 original instruction bytes / 5,407 ASM**. No production modifications. Existing three pristine-native-exact Mini-speed functions remain separately researched/unpromoted.

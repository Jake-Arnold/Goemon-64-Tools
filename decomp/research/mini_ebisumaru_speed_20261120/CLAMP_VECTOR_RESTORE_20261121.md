# 21 November 2026 — movement clamp saved-vector reconstruction (full length exact, instructions nonmatching)

**FAILED_NATIVE / RESEARCH_ONLY. No production promotion.** Original USA target `func_801CD310_589220`, ROM `0x589220`, VMA `0x801CD310`, original **4,320 bytes / 232-byte stack frame**, overlay `file_11`.

## Original MIPS dataflow evidence

The original `func_801CE3F0_58A300` call on the negative task+0x78 path saves the three prior task orientation components (`task+0x84`, `+0x88`, `+0x8C`) to stack slots `sp+0xCC`, `sp+0xD0`, `sp+0xD4`, then reloads and restores the components after the helper call. The prior 4,328-byte C reconstruction assigned the three values to `vecD[0..2]` before that call, **but restored the third component from a separate long-lived scalar `pool_8`**. Replacing the final restore with **`M2C_FIELD(arg0, f32 *, 0x8C) = vecD[2];`** makes that C source consume its saved component and alters native register/stack liveness in the right direction. Moving the `vecC[3]` declaration before `pool_2` yields two further original-position instruction matches without changing executable C statements. Complete new research source SHA-256 `6dc2aaa7accd804fe6b670ee2832997d52d5aed7652b3351a9f8ffc13dc007f7`.

## Verified original-address native IDO 5.3 result

- **Genuine ELF FUNC: 4,320/4,320 bytes** (previous 4,328). **Frame: 232/232 bytes**. These coincident totals are NOT a code match.
- Original-position non-relocation instruction identities improve **137/920 → 157/925** (20 additional original-position matches; **768/925 still differ**). Previous exact prologue 15/15, override 13/13 and 292-byte switch/trig region 55/55 are retained.
- Original-relative text relocation position/type/target matches improve **33/101 → 38/101**. Both original/candidate have 101 text relocs with the same types/counts; **99/101 type-and-symbol records match in order**, with only the compiler-owned `.rodata` jump-table pair different from original `jtbl_8020A85C_5C676C`. Other relocation positions differ; complete semantic ELF relocation equality NOT claimed.
- All **33/33 original calls** in original callee order, all **nine native `sqrt.s`**, and **all 18 original numeric jump-table relative target offsets** are retained.
- Original 3D magnitude sqrt `+0x9A8`; candidate now `+0x9B4` (**+12 bytes**, previously +16). Original 2D sqrt `+0xDDC`; candidate `+0xDF0` (**+20 bytes**, previously +24). Neither arithmetic block is native exact.
- `block_gain.csv` provides bounded 0x100-byte region scores: 20 new matching words appear mostly in the final quarter (five in `+0xF00..0xFFF`, ten in `+0x1000..0x10DF`). The earlier context branch `+0x1B4..0x25F` remains **17/39**. Direct zero-lifetime, flag, pointer-prototype and declaration moves did not fix that `$f14/$v1` register discrepancy.

## Authentic tools and limits

Authentic original-ID0 5.3 compilation, ELF function extent and MIPS disassembly, original instruction/relocation/18-case table comparison, user-supplied retail SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`, pristine expanded-USA SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`, and **33,554,432/33,554,432 pristine rebuilt ROM bytes** compared to the original decompressed input: **PASS**. Independent packaged source replay using `replay.sh` and `native_audit.py`: **PASS** for the measured properties. ZIP/source hashes PASS. Multiple normal-C vector-restoration and scoped-lifetime negatives were compiled; restoring the other two components or introducing new scoped saved arrays lost prior matching regions or changed frame.

**Complete native instruction equality FAIL**; a pristine original ROM baseline does not prove a candidate replacement. Experimental C **not integrated into ROM**. The actual combined current `python3 -m decomp.verify`, strict inventory, full `decomp.local_ci` and emulator gameplay **NOT RUN**. Shell GitHub clone still fails DNS; only connected GitHub metadata/commits are remotely available. Canonical USA remains **1,956 matching C / 83,940 original instruction bytes / 5,407 ASM** (live inventory checked today). The four separately native-pristine exact Mini speed/countdown functions remain unpromoted.

Full 21,267-byte C source, type header, native replay, original-position block/relocation tests and variant matrix supplied separately as conversation artifact `GOEMON_CLAMP_VECTOR_RESTORE_20261121.zip`. This report and patch contain **no** original ROM/ASM, extracted assets, native binaries/objects, toolchains or code bytes. Do not merge the draft PR or update canonical acceptance on this result.

**Next:** correct original source-level vector backing-store ownership and aliasing through the 3D/2D movement branches; first unresolved original context live-range still starts at `+0x1B4` (`$f14`, `$v1`). Preserve the strong original-switch and saved-vector results and demand full original-address machine-code equality.

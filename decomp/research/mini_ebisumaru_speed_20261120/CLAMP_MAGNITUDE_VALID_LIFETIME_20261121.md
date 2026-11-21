# USA movement clamp — recover the late 3D magnitude lifetime (21 November 2026)

**RESEARCH_ONLY / FAILED_NATIVE.** Original USA `func_801CD310_589220`, ROM `0x589220`, VMA `0x801CD310`, original 4,320 bytes, stack frame 232 B, `file_11`. No production C or manifest change.

## Actual source-level reconstruction

The independently regenerated complete C scaffold held `pool_fp_2 = 0.0f` live across the middle of the function and replaced it with `sqrtf(...)` on one 3D-magnitude branch. A bounded, semantics-preserving alternative tracks whether the magnitude was computed as `u8 magnitude_valid`, sets it immediately after that square root, and assigns `pool_fp_2=0.0f` only immediately before its later multiplication if no magnitude was computed. The later `func_80003E10_4A10` helper and multiplication remain present on both branches; do **not** replace `0 * factor` with a constant zero because infinities and NaNs matter. The exact source-only delta is in `clamp_magnitude_valid_lifetime_20261121.patch`, against the previously delivered `clamp_motion_arg_split_nonmatching.c`.

This is a research hypothesis about original code structure, not proof of which local declarations the original C used.

## Native IDO 5.3 measured results

| Tested whole-C source | Native FUNC bytes | Frame bytes | Equal at original nonreloc positions | Exact offset/type/symbol relocations |
| --- | ---: | ---: | ---: | ---: |
| Prior motion-arg-corrected scaffold | 4,288 | 232 | 9/882 | 0/101 |
| Magnitude-valid `u8`, select with conditional expression | 4,328 | 232 | 16/895 | 4/101 |
| Magnitude-valid `s32` | 4,328 | 232 | 16/895 | 4/101 |
| **Magnitude-valid `u8`, guarded zero before helper** | **4,320** | **232** | **19/895** | **4/101** |
| Guarded zero after helper | 4,312 | 232 | 17/893 | 4/101 |

All five genuine IDO compilations were replayed from source in a clean temporary directory using the pinned original IDO 5.3 flags `-O2 -mips2 -G 0 -non_shared`. Winning source SHA-256: `06e015d624c2c9be48d0c0e02bb43e882fc02c4e9aec084df39764d5bedd5be4`. This is an improvement over the *separately regenerated scaffold*, not over the earlier more accurate 157-instruction candidate delivered in another conversation attachment.

The size/frame-exact winner is **not** machine-code exact: first non-relocation difference remains `+0x04`; compiler saves `$f20` where the original initializes `$f0`. Both have **33 original calls, nine inline `sqrt.s`, 101 text relocations**; only **99/101** relocation type+symbol records literally agree in original order because IDO uses compiler `.rodata` for the two named-original jump-table relocations. Only **4/101 original-offset/type/symbol relocations** are identical. The original 18 jump-table groupings persist but table destination displacements are **+4,+8,+12,+16,+20 bytes**, not exact. Only 19 of 895 comparable instruction words match; correct total size does not imply four instructions differ.

## Measured original-vs-compiled FPR lifetime

A read-only opcode/disassembly audit using the user's authentic 32 MiB original ROM proves:

- Original early `mtc1 zero,$f0` at `+0x04` supplies three task stores at `+0x18,+0x1C,+0x20` and does not need to be retained for the first helper call at `+0x3C`.
- Candidate saves `$f20` at `+0x04`, initializes zero into `$f20` at `+0x08`, stores it three times at `+0x1C,+0x20,+0x24`, and references it **63 more times after the first helper call**, across **29 intervening helper-call sites**, through `+0xFCC`.
- Original contains **58** explicit FP zero register definitions; candidate has **10**. The source's zero-value lifetime remains much too broad. This is a *measured codegen explanation*; it does not imply full path-sensitive def-use analysis.

## Behaviour, toolchain and ROM gates actually executed

- Authenticated 16 MiB retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`. Decompression SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Fresh pinned original USA full ROM rebuild **33,554,432/33,554,432 bytes identical**, identical 32MiB SHA-1. This is the **unmodified original**, not candidate C integration.
- Full native IDO source compiles and focused ELF/relocation/MIPS audit **PASS structural measured properties; FAIL complete function equality**. Clean artifact extraction/replay **PASS expected FAILED_NATIVE** across five candidate sources.
- **30,000 paired host tests under GCC ASan+UBSan and 30,000 under Clang ASan+UBSan PASS** for the float-representation rewrite, all non-NaN results bit-identical, NaNs class-equivalent; one GCC test observed a distinct NaN sign/payload, none with Clang. The helper is called exactly once. These tests do not prove whole-function gameplay or original-address native semantics.
- Experimental C full ROM link, current accepted-USA combined `python3 -m decomp.verify`, strict inventory, full `decomp.local_ci`, emulator gameplay: **NOT RUN** because original-address instructions still mismatch and a complete current local decomp checkout could not be materialized (shell GitHub DNS unavailable).

## Reproduction and next target

Companion conversation file **`GOEMON_CLAMP_MAGNITUDE_LIFETIME_20261121.zip`**, SHA-256 `d21d25080d85910a57c728e20ee3f7f25431f49006e7ec0aa8a67779a96f5ca7`, contains all 5 candidate C sources, the patch, exact comparator, first-zero/call-lifetime auditor, 30k-case host C fixture, replay shell and JSON evidence. Execute `bash replay.sh` with `GOEMON_UPSTREAM`, `GOEMON_EXPANDED_ROM`, `GOEMON_BASELINE_ELF` and the pinned runtime environment from `GOEMON_BUILD_ENVIRONMENT.md`. The ZIP contains **no ROM, original ASM, extracted assets, object/ELF, tools or native compiler**.

**Next:** Reconstruct the *other* zero-valued register def/use chains around original context gate `+0x1B4` and helper calls, then alter source declarations/branch lifetimes with a bounded IDO experiment. Stop optimizing whole function length independently. Prior stronger 157/925-word source, if its full C can be recovered, remains the preferred matching starting point.

Official USA G2 remains **1,965 C / 84,648 instruction bytes / 5,398 ASM**. Keep PR #144 draft. No promotion.

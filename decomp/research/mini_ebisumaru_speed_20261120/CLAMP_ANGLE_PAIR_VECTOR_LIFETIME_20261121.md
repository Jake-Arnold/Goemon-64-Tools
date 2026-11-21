# USA Mini clamp: original halfword angle-pair and vector storage-lifetime reconstruction

**21 November 2026 · FAILED_NATIVE / RESEARCH_ONLY. No C promotion.**

Original `func_801CD310_589220`, ROM `0x589220`, guest VMA `0x801CD310`, `file_11`, native length **4,320 B**, frame **232 B**. Native original compiler: pinned SGI IDO 5.3 `-O2 -mips2 -G 0 -non_shared`. USA expanded ROM SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.

## Input original-MIPS facts, rechecked against authentic ROM and linked ELF

Original switch angle 1: `sp+0x6E` halfword, five case-group writes. Original angle 2: `$a1` merged by switch cases, single `sh a1,sp+0x6C` at `+0x198`, loaded via `lhu a0,sp+0x6C` in the second trig call's delay slot at `+0x1A8`. First and second `func_80003EA0_4AA0` calls at `+0x19C` and `+0x1A4`; second float return stored at `sp+0x64` at `+0x1B0`. The previous independently reconstructed C used a 32-bit stack spill `sp+0x98`, reload and ANDI, with its calls at +4/+8 drift.

## New bounded IDO source research

Thirteen whole-function C source variants tested a 16-bit angle variable, volatile storage, an adjacent `u16[2]` pair, pairs sharing later vector storage via C union, one second-angle-only union, and the explicit cast. No instruction patching, inline MIPS or toolchain alteration. The *structural* source hypothesis is that a local halfword backing store may have a live interval disjoint from a later 3-float vector. The two measured union sources have no source-level angle reads after the first vector use. This only supports lexical non-overlap; it does **not** establish actual original C stack ownership or complete runtime equivalence.

| Source | Native FUNC | Frame | Same-offset comparable non-relocated words | Exact reloc offset/type/symbol | Trig call drifts |
| --- | ---: | ---: | ---: | ---: | --- |
| Prior `switch_second_pooled_s32.c` | 4,312 B | 232 B | 29/898 | 6/101 | +4 / +8 B |
| Adjacent `u16 switch_angles[2]` | 4,312 B | 240 B | 22/900 | 8/101 | **0 / 0 B** |
| `union_angle_vecA.c`: angle pair / later vector storage | **4,316 B** | **232 B** | 26/907 | **10/101** | **0 / 0 B** |
| `second_union_vecA.c`: only second angle / later vector | 4,328 B | **232 B** | **40/910** | **24/101** | +20 / +20 B |

The pair/vector source now emits **both original trigonometric calls at their exact original offsets with the halfword load in the second call delay slot** while retaining the 232-byte frame. It still has an extra post-call first-angle copy; first-angle and second-angle C stack slots are `sp+0x86`/`sp+0x84`, not original `sp+0x6E`/`sp+0x6C`, and trig return is written `sp+0xD4` at `+0x1B4`, not original `sp+0x64` at `+0x1B0`. It remains 4 bytes short of exact original length and starts with an unwanted `$f20` save at `+0x04`.

The second-angle-only/vector source restores 16 additional instruction positions and 18 more exact relocations relative to the previous candidate, mostly *later* in the function, but loses the early trig call positions and grows 8 bytes beyond original. Do not rank these candidates by one score or claim they can be combined without proof. Original complete C match **FAIL** for every variant.

## Actually executed tests

- SHA-1-authenticated original USA retail `df8083a54296b8c151917c5333e1c85f014a2a66` and expanded `6ea0ed71032ce08fc2745f412d84936382197494`. Clean unmodified full USA ROM **33,554,432/33,554,432 byte-identical**. This does not constitute C replacement-ROM integration.
- **13 native IDO 5.3 C compilations**, exact original-offset MIPS/ELF/frame/relocation/auditor comparisons. All build and produce `FAILED_NATIVE`; all retain 33 calls, 9 native `sqrt.s`, 101 text relocations and the 18-entry switch grouping.
- Fresh clean ZIP extraction and replay of baseline + two Pareto candidates: **PASS expected FAILED_NATIVE**. Checks function extents, stack, exact word comparison, exact relocation triples, original trig-call offsets and original-ROM SHA.
- Original code trig stack ABI signature check: PASS.
- GCC **65,536** and Clang **65,536** host switch-angle equivalence tests under AddressSanitizer/UBSan: PASS. The fixture checks selected angles, scalar results and non-overlapping vector reuse; it does **not** prove whole-function equivalence or original NaN behaviour.
- New production replacement ROM, canonical current all-accepted-USA `decomp.verify`, strict inventory, full `decomp.local_ci` and emulator gameplay: **NOT RUN**. No candidate meets native acceptance.

## Replay deliverable and next block

Companion **source-only** ZIP `GOEMON_CLAMP_ANGLE_PAIR_20261121.zip`, SHA-256 `4be45638fccd1505937294100f8edb6953494d4deae04f4ee8b3a9b8e6255f2d`; includes 13 complete C experimental variants, baseline C, native ELF/MIPS auditor, original call/slot auditor, read-only replay, host fixture, metadata and SHA-256 manifest. No ROM, disassembly, original assets, compiler, object or ELF is included. Run `python3 replay.py --upstream PINNED_MNSG --rom PRIVATE_EXPANDED_USA --elf ORIGINAL_USA_ELF --built-rom EXACT_REBUILT_ROM` after restoring pinned runtime/binutils.

**Next hypothesis:** Original `sp+0x6C/+0x6E` angle halfword positions and trig result `sp+0x64` may require a different stack-backed angle/vector grouping, without the post-call first-angle copy. Recover first-angle long lifetime without forcing earlier case stores into new stack slots; preserve both exact trig call PCs and original 232-byte frame. Reconcile `$f20` only through authentic global source lifetimes.

USA G2 **unchanged at 1,965 accepted C / 84,648 original instruction bytes / 5,398 ASM**; this PR remains draft.

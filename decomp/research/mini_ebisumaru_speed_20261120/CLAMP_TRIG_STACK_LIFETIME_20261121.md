# USA Mini clamp — trigonometric call / switch-angle storage lifetime (21 November 2026)

**FAILED_NATIVE / RESEARCH_ONLY. No matching-C promotion.** Target `func_801CD310_589220`, USA ROM `0x589220`, VMA `0x801CD310`, original `4,320` bytes, frame `232`, owner `file_11`. Original expanded-USA SHA-1: `6ea0ed71032ce08fc2745f412d84936382197494`. Pinned upstream `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, original SGI IDO 5.3 flags.

## New authenticated original-code evidence

The original switch's second trigonometric angle resides in **`$a1`**, rather than a long-lived `u16` stack local. Original code stores a halfword to `sp+0x6C` at function offset `+0x198`, just before **two calls** to `func_80003EA0_4AA0` at `+0x19C` and `+0x1A4`. The halfword loads into the second call argument in its branch delay slot at `+0x1A8`. The second float return (`$f0`) is stored to `sp+0x64` at `+0x1B0`, first reloaded at `+0x39C`. The first angle is written to `sp+0x6E` in each of the five case groups; the scalar selected by the switch is saved at `sp+0x5C`. These offsets and operand/call signatures were checked directly against the private authenticated original MIPS/ELF; no original instruction bytes were published.

The independently regenerated previous C instead used pooled `u16` second-angle locals, stored the second angle in each case rather than once at the call boundary, and generated two trig calls each **20 bytes late**. Four separate/trig-angle variants generally worsened stack allocation and relocated code. Directly passing `pool_u16_2` and swapping vector declaration order generated **identical** native code to baseline.

The new, semantically supported hypothesis writes the constant second angle into an existing, lexically non-overlapping `s32 pool_s32_0` temporary, reusing its lifetime before the later independent assignment, instead of `u16 pool_u16_2/pool_u16_3`. This corrects more case-merge placement **without adding a new stack local**. It does **not** prove the actual original C used that variable.

## Native results (fixed original-address comparison)

| Measurement | Earlier reproducible C | New pooled s32 candidate | Original |
| --- | ---: | ---: | ---: |
| Genuine native ELF FUNC size | 4,324 B | **4,312 B** | 4,320 B |
| Stack frame | 232 B | **232 B** | 232 B |
| Equal non-relocation instruction positions | 24 / 902 | **29 / 898** | Exact required |
| Exact offset/type/symbol text relocations | **10 / 101** | 6 / 101 | 101 |
| First, second trig-call offset drift | +20, +20 | **+4, +8** | zero |
| Context flag-byte load offset drift | +16 | **+4** | zero |
| Same-position comparable words within context window | 0 / 36 | **8 / 37** | Exact required |
| Relative jump-table destination displacements | +4/+8/+12/+16/+20 | **+4 uniformly** | zero |
| Calls / native square roots / text relocs | 33 / 9 / 101 | **33 / 9 / 101** | 33 / 9 / 101 |

All 18 jump-table entries retain the original grouping; the source candidate still uses compiler-owned `.rodata` for two relocations where original uses `jtbl_8020A85C_5C676C`. **99/101** ordered type/symbol pairs match, but only **6/101 exact relocation triples** match. The candidate's second trig return is still stored at `sp+0xD4`, rather than the original `sp+0x64`; the candidate still saves `$f20` at `+0x04` instead of zeroing `$f0`. The original independent `$f14/$f16` zeros remain absent. The 34/43 ordered context operation shapes match without register identity; not original byte equality.

This is an improvement in *early switch/trig/context geometry* and 5 matching instruction positions, but it **loses four exact relocation positions and some later-block matches**. Keep both sources; neither is universally better or native-exact. Older 157/925 source remains historical and was not available for replay.

## Actual tests and source delivery

- Authenticated retail USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`.
- Pinned **unmodified** original USA 33,554,432-byte ROM rebuild and full byte comparison: **PASS**, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`; this is **not a C-integrated ROM test**.
- Eight whole-function IDO 5.3 original-offset audits: native compile/structure PASS, exact native match **FAIL for all eight**. Fixed call/switch/stack ROM checks PASS.
- Four synthetic opcode/stack/relocation tests PASS; source-only host fixture for **all 65,536 u16 switch modes**, GCC and Clang with ASan+UBSan: **PASS** (argument selection and call order only; not whole-game semantic equivalence).
- Fresh ZIP extraction and complete native/host replay: **PASS**; all eight remain `FAILED_NATIVE`.
- Combined current USA `decomp.verify`, strict inventory, full `decomp.local_ci`, candidate replacement-ROM link, emulator gameplay: **NOT RUN**.

Reproducible source-only package `GOEMON_CLAMP_TRIG_LIFETIME_20261121.zip`, SHA-256 `52234c08b7ec24639ef99baa7ff24d9c89e10af3f6bbce274587a81e87f2be68`, includes all **eight complete C sources**, original-offset ABI/stack auditor `audit_trig_boundary.py`, `audit_scaffold.py`, `context_lifetime.py`, `replay_native.py`, tests, evidence JSON and this report. Command after setting the provided pinned runtime and tool paths: `python3 replay_native.py --upstream PATH --rom PATH --elf PATH --built-rom PATH`. Neither the ZIP nor the GitHub evidence includes original ROM/ASM/assets/objects/ELFs/compiler or toolchain.

**Next bounded source reconstruction:** recover the original simultaneous `$a1` second-angle, stack `sp+0x6E` first-angle, `sp+0x5C` scalar and `sp+0x64` trig-result lifetimes across the two calls. Specifically, remove the candidate's `sp+0x98` word spill/reload/ANDI while preserving original call delay-slot semantics. Do not optimize total size independently or claim that uniform +4 drift proves a one-instruction repair.

Latest verified USA production **1,965 accepted C / 84,648 instruction bytes / 5,398 ASM**. Original ASM remains and PR #144 stays draft.

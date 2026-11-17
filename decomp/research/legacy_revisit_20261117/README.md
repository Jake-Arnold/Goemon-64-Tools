# Revisit: two legacy USA original-address C targets (17 Nov 2026)

**Research only.** This retry used the authenticated USA 32 MiB ROM (SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`), original IDO 5.3 and the MIPS linker. Starting verified production is USA **864 C / 37,904 instruction bytes**, Japan **39 C**. Neither candidate passed full native function equality; accepted production is unchanged.

| Original function | Original bytes | New linked C result | First differing offset | Decision |
| --- | ---: | --- | --- | --- |
| `func_80001DF4_29F4` | 92 | 3 variants, all 96 bytes | +0x20, +0x00, +0x14 | `FAILED_NATIVE` |
| `func_8003F6E8_402E8` | 48 | 40-byte exact executable prefix, 40-byte FUNC | +0x28 | `FAILED_NATIVE` |

The original DF4 source shape still requires codegen/branch placement work. All three new variants regress relative to the earlier +0x24 first mismatch. The F6E8 call wrapper's compiled 40-byte prefix is exact, but the original 48-byte FUNC contains an extra `jr $ra; nop` instruction pair; eight bytes of generated linker padding cannot be substituted for those instructions. Retain its entire original `GLOBAL_ASM` extent.

## Reproduce the native trials

Use the pinned upstream `mnsg` checkout at commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`, its `tools/ido-5.3/cc`, and the exact original flags:
`-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2`.
Compile each C source separately and link with the corresponding reviewed `link_df4.ld` or `link_f6e8.ld`, placing the functions at their original guest VMAs. The linker scripts use `SUBALIGN(4)` to avoid the default section alignment relocating the function start. Extract only the linked `.text` bytes; compare each original function's full extent, including trailing instruction words. Do not commit original ROM, MIPS binaries or compiler objects.

The complete, sanitized machine-code measurements, source Git object IDs and test status are in `decomp/results/legacy_native_revisit_20261117.json`. Source types are intentionally minimal test-only prototypes, not a production ABI/schema commitment.

## Actually executed tests

- Native IDO compilations and original-address ELF linkage: all four compilations succeeded; all four full-function comparisons **failed**.
- `python -m unittest decomp.test_vm_wrapper_extent -q`: **6/6 PASS**.
- Full `python -m decomp.local_ci`: **PASS**, including both Python regression suites and C ASan/UBSan display-emitter host fixture.
- Combined USA `decomp.verify`, `decomp.inventory`, and full ROM promotion gate: **NOT RUN**, because no source candidate was full-function native exact.

**Do not change the production manifest, accepted counts or pending registry.** Additional unchanged broad source-shape attempts are unlikely to help. A new retry should first identify a falsifiable change in native register lifetime, exact control-flow shape, or original source-unit boundary.

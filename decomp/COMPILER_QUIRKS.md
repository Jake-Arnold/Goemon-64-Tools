# IDO 5.3 / MIPS matching-C compiler quirks

This is a cumulative evidence-led knowledge base for reusable compiler behavior found while matching original Goemon 64 functions. Consult it before variant searches. Record new findings in the same commit as the associated decomp research or promotion, even when a function remains assembly-owned.

## Entry template

### [Short description] — [verified / hypothesis]

- **Region / function / ROM offset / VMA:**
- **Compiler and flags:**
- **Minimal C example or source reference:**
- **Observed versus expected code generation:**
- **Working expression/type/layout or failed variants:**
- **Reproduction command and evidence paths:**
- **Verification level:** isolated native / combined G2 / research only
- **Applicability and limitations:**

Do not treat an isolated instruction match as proof of relocation or full-ROM equality. Keep observations specific, reproducible and deduplicated; link research artifacts rather than embedding copyrighted original code bytes.
### Embedded original-C prototypes and historical symbol size — verified (USA, original ROM G2 2026-11-22)

- **Region / function / ROM offset / VMA:** USA `func_8000D3B8_DFB8`, `0xDFB8`, `0x8000D3B8`; companion `dialogue_window.c` fields `0xD054..0xD4D0`.
- **Compiler and flags:** SGI IDO 5.3 `-G 0 -non_shared -O2 -mips2`.
- **Minimal C source:** `decomp/research/usa_crossregion51_recovered27_20261122/sources/recovered27_009.c`; stage adapter `decomp/usa_crossregion51_recovered27_g2_promotion.py`.
- **Observed versus expected:** Source compiled standalone as a true 64-byte original function, whereas the previous 2,014-C ELF carried a historical 72-byte function-size annotation for D3B8. Direct compiled source restores the original 64-byte ELF entry with identical ROM instructions; all other 7,375 function entries are unchanged from predecessor. Same 82,103 relocation multiset.
- **Working type/layout:** When replacing ASM pragmas in already-compiled `dialogue_window.c`, the existing `common.h` defines `u32` as `unsigned long`, while a standalone donor header defines it as `unsigned int`. Do not duplicate incompatible C typedefs or `D_80167C48` declaration; use existing canonical declaration and cast the pointer to an observed-layout struct. The source guard preserves matching offsets.
- **Evidence:** `decomp/results/usa_recovered27_2041_g2_20261122.json`; `python3 -m decomp.usa_crossregion51_recovered27_g2_promotion verify` plus full `python3 -m decomp.local_ci`.
- **Verification:** integrated original USA complete ROM / ELF / relocations and strict inventory, no emulator execution. The scalar typedef issue is a source-integration quirk, **not** evidence that isolated IDO generated different MIPS arithmetic.
### Typed f32-array pointer preserves original MIPS load scheduling — verified (USA/Japan donor, original-ROM G2 2026-11-22)

- **Region / function / ROM offset / VMA:** USA `func_08000AC8_72C318` / `0x72C318` / `0x08000AC8` and 18 related setters, original Japan-0 counterpart `func_801D72DC_66982C` at `0x66982C` and other donor pairs. All 19 original byte sequences match region-to-region; translation is based on original instructions, not RAM offset heuristics.
- **Compiler and flags:** original SGI IDO 5.3 `-G 0 -non_shared -O2 -mips2`.
- **Minimal source:** `decomp/research/usa_crossregion51_recovered19_20261122/sources/donor19_000.c`; uses typed `f32 *v=(f32*)((char*)p+0x5C)`, `v[3]`, `v[2]`, `v[1]`, `v[4]` and control-flow expression.
- **Observed vs expected:** m2c-derived equivalent `volatile` field-expression C matched 18 of 21 original words but moved the `addiu v0,a0,0x5C` after two `lwc1` instructions; 448 further typed/volatile variants failed to improve. The published JP `f32` array access generated the exact 21 original MIPS instructions without any instruction patch. Same pattern reproduced for all 19 original USA setters at their individual VMA (1,596 bytes).
- **Verification:** 19/19 isolated native and integrated original 32 MiB USA ROM, exact 7,376 ELF functions, all 82,103 semantic relocations, strict inventory, full CI and GCC ASan/UBSan tests. Do not generalize register allocation without rechecking original instructions.

### Prototyped float callback and unsigned-byte conversion — verified (USA 2026-11-22)

- **Region / function:** `func_80217970_681350` / original ROM `0x681350` and three siblings; `func_8021C818_6861F8` / original ROM `0x6861F8`.
- **Compiler and flags:** SGI IDO 5.3 `-G 0 -non_shared -O2 -mips2`.
- **Source:** `decomp/research/usa_crossregion51_extra5_20261122/sources/*.c`.
- **Observation:** typed `extern int func_800040A8_4CA8(float,float)` produces original 80-byte callback wrapper, while unprototyped declaration changes floating-point ABI register/spill scheduling and padded length. The byte setter using `(float)(unsigned char)value` generates exact original 44-byte function; native object `.text` adds 4 trailing zero pad bytes, safely trimmed before layout integration. Four original R_MIPS_26 relocations at original addresses are exact.
- **Verification:** 5/5 original USA functions full G2 and strict inventory, full CI, host sanitizer tests; no game emulator execution.

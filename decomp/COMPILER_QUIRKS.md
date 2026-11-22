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

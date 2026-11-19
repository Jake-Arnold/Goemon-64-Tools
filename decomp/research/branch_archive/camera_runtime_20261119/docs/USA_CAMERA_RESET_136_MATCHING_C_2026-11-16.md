# USA camera-region reset: exact 136-byte IDO 5.3 matching-C candidate

**Date:** 16 November 2026. **Status:** isolated native proof PASS; production promotion NOT performed.

## Exact target and existing work

- Function: `func_801F97D4_5B56E4`, original USA VMA `0x801F97D4`, original decompressed ROM `[0x5B56E4,0x5B576C)` (136 bytes / 34 MIPS instructions).
- Original ROM source identity: compressed USA SHA-1 `df8083a54296b8c151917c5333e1c85f014a2a66`; decompressed 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- The function is still assembly-owned in production `chatgptweb/decomp` (315 verified C, 152 in `file_11`), within the original assembly chunk `[0x5B43A4,0x5B65D4)`.
- The separate upstream `camera` branch already supplies earlier camera-controller provisional C; this research reuses that work and does not recode the 30 KB draft. Reviewed PR #23/#24/#41 research candidates did not identify an overlap with this exact function.

## Runtime semantics

The original routine clears the 16-bit default camera-mode global at `0x800C7B00`, resets three adjacent 32-bit globals, then iterates over ten records at 40-byte stride (`0x28`) and zeros each record's halfword selector and nine 32-bit fields. User gameplay evidence found the global at `2` in town/outdoor gameplay and `0` in indoor gameplay/loading; its manipulation changed camera perspective. The effective camera task mode may be overridden later by region-table logic, so do not treat this global as the final authoritative mode.

## Compiler match

- Source: `decomp/research/camera_reset_usa_5b56e4.c`.
- Original compiler: IDO 5.3; `-O2 -mips2 -G0 -non_shared -Wab,-r4300_mul` and the pinned USA build defines.
- Link: MIPS big-endian ELF32 at the **original** VMA `0x801F97D4` using the two original global symbols.
- The compiled function's ELF symbol size is exactly **136 bytes**; `.text` includes eight trailing assembler alignment bytes which are outside the function.
- The 136 original ROM instruction bytes and the first 136 linked C bytes are **byte-for-byte identical**; 34/34 MIPS instructions match.
- Original == candidate SHA-256: `f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a`.
- Source SHA-256: `9d47ba199dfd48f5707b7623f45eee5e0853110f725e08bcf4ad7c151f7450c4`.
- The object emits four symbolic `R_MIPS_HI16/LO16` relocations for `D_800BCCC0_BD8C0` and `D_8008CCC0_8D8C0`. This is **candidate relocation evidence**, not a proof that all 8,825 original `file_11` relocations match in the combined ELF.

One source-layout change was decisive: an equivalent `for(i = 0; i < 10; )` loop moved the counter initialization behind two address-setup instructions, eliminating the final three instruction-order differences from the preceding `do…while` source. No inline assembly, binary patches, or relaxed byte comparisons were used.

## Reproduction and regression tests

Run the standalone probe with the authenticated *decompressed* USA ROM and native toolchain paths:

```bash
python3 decomp/research/camera_reset_136_probe.py \
  --rom /path/to/usa/baserom.decompressed.z64 \
  --ido /path/to/ido-5.3/cc \
  --ld /path/to/mips-linux-gnu-ld \
  --objcopy /path/to/mips-linux-gnu-objcopy
```

`tests/test_decomp_camera_reset_136.py`: ROM-free 2/2 PASS (native 1 SKIP); with `GOEMON_USA_DECOMPRESSED_ROM`, `GOEMON_IDO_CC`, `GOEMON_MIPS_LD`, `GOEMON_MIPS_OBJCOPY` and runtime library path set: 3/3 PASS. The standalone probe also independently reported PASS. Script and machine-readable proof are committed without ROMs, generated assembly, binaries, or individual code bytes.

## Production acceptance still required

Do **not** increase the canonical matching-C count from 315 to 316 yet. A subsequent reviewed, opt-in mixed-C/ASM stage must preserve all current 152 `file_11` functions and original object boundaries, replace only this 136-byte slice, and pass complete central `decomp.verify` against the **entire 33,554,432-byte original USA ROM**, all 8,825 semantic `file_11` relocations, the complete 7,376-identity `decomp.inventory`, and full `decomp.local_ci`. This combined private production checkout and central gate were unavailable in the present native sandbox. No ROM rebuild or combined G2 is claimed.

Next controlled step: integrate this exact candidate in a new reviewed stage and run the complete native production gate. If any gate fails, retain the existing assembly and the source-only research proof.

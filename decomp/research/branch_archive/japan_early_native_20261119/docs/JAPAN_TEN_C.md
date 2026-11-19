# Japanese matching C: tenth promotion (16 November 2026)

**Native Japanese ROM build: PASS.** This is the tenth verified original-address C function, not Japanese PC-native gameplay.

## New function

| Item | Result |
| --- | --- |
| Original function | `func_80036D00_37900` |
| ROM offset | `0x37900` |
| Guest RAM VMA | `0x80036D00` |
| Function and `.text` size | 32 bytes |
| Behaviour | Calls `func_8000364C_424C(15)`; the Splat comment identifies the region as warps |
| Compiler | Original native IDO 5.3, `-O2 -mips2` |
| C source SHA-256 | `2723f04618138b20a43935fe81be83048336a0e318dbb9b87131bfc4090aa064` |
| Relocatable `.text` SHA-256 | `7c70158f28f75cceb029fb3b2658ed024d443310cb4a3d920e8d3469dd187fa5` |
| Relocation | Exactly one `R_MIPS_26` at `.text+0x08` targeting `func_8000364C_424C` |

The candidate was linked alongside all nine earlier C functions. The linker map places its object `.text` at `0x80036D00` with size `0x20`. The linked instruction bytes match the Japanese retail reference after applying the reviewed relocation. Remaining original assembly starts at ROM `0x37920` and is unchanged.

## Complete original ROM proof

- Pinned upstream source commit `7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`.
- Exact **33,554,432-byte expanded Japanese ROM** SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, zero differing bytes.
- Exact **16,777,216-byte compressed Japanese retail ROM** SHA-1 `9843ee979b5f6c80f5eda85df0baed9ae7c4e73b`, zero differing bytes.
- Independent local checks passed for source bytes, object symbol extent, original RAM address, exact relocation target and both byte-for-byte ROM comparisons.
- Native ELF function inventory: **7,376** entries, **7,366** assembly-marked and **10** verified C (280 bytes in six translation units); zero unexpected unmarked.

## Rebuild

Run from the Goemon-64-Tools repository with the user's private ROM and both offline dependency directories:

```bash
bash decomp/build_japan_ten_c.sh \
  /path/to/mnsg-japan \
  /path/to/goemon-dependencies \
  /path/to/goemon-runtime-additions
```

The script re-stages all previous verified Japanese source units plus the new warp dispatcher and uses the original Japanese Splat split, IDO 5.3, binutils and Rommy. No original USA source or Splat YAML is modified. **The individual native build/verification stages were executed, but this exact standalone runner and the newly updated formal Python unit tests were not rerun end-to-end.**

## Next candidate discovered but not promoted

`func_80036D20_37920` (ROM `0x37920`, VMA `0x80036D20`, 56 original code bytes) stores halfword `0x260` into `g_system_ptr+0x3AFE0`, then calls `func_8000364C_424C(12)`. Its IDO 5.3 output has the same instruction sequence apart from relocation placeholders, with `R_MIPS_HI16`/`R_MIPS_LO16` to `g_system_ptr` and `R_MIPS_26` to the callee. **It is not a matching-C promotion yet.** The standalone `.text` is padded to 64 bytes; an unadjusted linker replacement would overlap the next live function starting at `0x37958`. Implement a safe object text packing proof or a different segment strategy before linking.

Also investigate the adjacent 96-byte `func_80036C70_37870` transition helper. A fresh USA matching-C G2 and Japanese emulator/native PC runtime remain separate unfinished tasks.

No copyrighted ROM bytes, assembly extraction, assets or compiler binaries are included.

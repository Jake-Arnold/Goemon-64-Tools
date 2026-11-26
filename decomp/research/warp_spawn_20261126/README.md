# Warp spawn chain — 26 November 2026

RESEARCH_ONLY. Four isolated native IDO 5.3 matches, not canonical promotions.
Base: stable/decomp 9932e4bac45bd3f41513b2f6ff0eb8ee438d0997, source archive artifact 15074968037 authenticated by SHA256SUMS and COMMIT.txt. Predecessor hosted CI run 45728666858 succeeded. Upstream 7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee; expanded regional ROM SHA-1 and compiler hash are enforced by replay.py.

| Region | Function | ROM offset | Bytes |
|---|---|---:|---:|
| USA | func_800358E8_364E8 | 0x364E8 | 124 |
| USA | func_800357BC_363BC | 0x363BC | 152 |
| Japan | func_80035558_36158 | 0x36158 | 124 |
| Japan | func_8003542C_3602C | 0x3602C | 152 |

Warp research anchor: stable/toolkit docs/ENTRANCE_WARPS.md. The caller chain forwards position and orientation parameters, then creates/initializes the task; names and parameter types beyond the observed ABI are provisional. Regional references are independent generated original Splat assembly, not copies of the other region. All four positive compiled raw function text (including relocation addends), two named R_MIPS_26 relocations per function, linked original-address function identities and original ROM bytes match. Signed instead of unsigned halfword controls all differ first at +0x10; all four are rejected despite preserving named relocations. Outcome for each attempt: NO_NEW_COMPILER_FINDING (ordinary signedness ABI, not a new compiler quirk). The original-address link uses SUBALIGN(4) to avoid linker inserting alignment before the function. No instructions were patched.

USA original assembly owner 0x35280, Japan original main_34EF0; whole owner and complete ROM not replayed for these candidates. No current canonical ownership overlap, based on the USA accepted predecessor names plus promo65 native names, and Japan strict 2990 inventory. Pending broad-candidate PR filenames inspected for #250, #202, #200, #194, #191, #190, #186, #184, #183; no address-name hit. This is not exhaustive pending prose/manifest deduplication. No native candidate G2, whole owner, strict candidate inventory, candidate promotion integrity, or hosted candidate regression claim. Baseline USA integrity PASS 3052 C, Japan inventory 2990 C. No canonical count change.

## Replay

Prepare the pinned upstream and both regional extracted ROMs using the project build environment documentation, with `mips-linux-gnu-as`, `mips-linux-gnu-ld`, `mips-linux-gnu-objcopy` on PATH and appropriate runtime library path. Run:

```sh
python3 replay.py --upstream /path/to/mnsg-japan \
  --ledger /path/to/Goemon-64-Tools/decomp/COMPILER_QUIRKS.md \
  --output proof-replayed.json
```

The positive/negative source, exact flags, hashes, original function extents and named relocation tuples are in the proof. Only hashes and metadata are distributed; no ROM, original assembly, toolchain or compiled object. Next: object initializer func_80035964_36564 / JP func_800355D4_361D4 and upstream exit decoder / spawn caller; then complete native G2 through canonical promotion pipeline.

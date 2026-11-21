# Original USA file22 1,808-byte renderer — IDO constant-lifetime study

**Status: RESEARCH_ONLY / FAILED_NATIVE. No matching-C promotion.**

Target: `func_801CC0C4_69ECE4`, original USA ROM `0x69ECE4..0x69F3F4`, original VMA `0x801CC0C4`, **1,808 bytes / 452 MIPS instructions**. SHA-1 of the authenticated 32 MiB USA original ROM: `6ea0ed71032ce08fc2745f412d84936382197494`; function SHA-256 `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`.

## Directly inspected original-instruction register allocation

The original ROM's instruction stream was disassembled with MIPS binutils and the original exact bytes were checked against the pinned source:

- Prologue: `addiu sp,sp,-0x140`, then saves `$ra`, `$fp`/`$s8` and `$s7..$s0` at `sp+0x2C` down to `sp+0x08`.
- Guest `0x801CC0F8` loads `0x0705` into **`$fp`**, and `0x801CC118` finishes `0x07054150` using `ori $fp,0x4150`.
- Guest `0x801CC11C` loads `0xE6000000` into **`$ra`**; it remains available for the three E6 display-list commands while the actual return address is preserved on the stack.
- Original **F300** immediate LUI sites (all local to one texture-format branch): `0x801CC4B4`, `0x801CC5A8`, `0x801CC69C`.
- Original **E700** immediate LUI sites: `0x801CC4CC`, `0x801CC5C0`, `0x801CC6B4`.
- The shorter `0x00054150` graphics word also has branch-local construction near `0x801CC4E8`, `0x801CC5DC`, `0x801CC6D0`.

The corrected IDO `-O2` **C candidate**, despite matching graphics output, assigns `0x07054150` to `$s5`, `0x00054150` to `$ra`, `0xE6000000` to `$s6`, `0xF3000000` to `$s7`, and `0xE7000000` to `$fp/$s8`. Its last three values are loop-hoisted, shortening and changing the entire function. The 0x140 stack diagnostic achieves **13 identical entry words**, not the original constant registers or full code. Fake padding arrays remain diagnostic only.

## Actually tested with pinned native IDO 5.3

The source-only script `probe_register_lifetime.py` validates original-ROM SHA-1, original function SHA-256, pinned upstream Git SHA, and the previously tested corrected-C diagnostic source SHA-256. It generates each variant as a **scratch-only C file**, compiles it with original IDO 5.3, checks every native ELF `.text` extent and all source-symbol relocation records, and compares instruction bytes and constant-loading counts against original code. It does not patch code, ROM or accepted decomp files.

| Source hypothesis | IDO option | Native `.text` | Frame | Entry matching prefix | F300/E700 LUI | Global relocations | Exact native? |
|---|---|---:|---:|---:|---|---:|---|
| Existing corrected diagnostic | `-O2` | 1744 | 0x140 | **13** | 1 / 1 | 2 | No |
| Volatile global cursor | `-O2` | 1744 | 0x140 | 13 | 1 / 1 | 2 | No |
| Volatile Gfx field stores | `-O2` | 1744 | 0x140 | 13 | 1 / 1 | 2 | No |
| Three labelled texture paths | `-O2` | 1744 | 0x138 | 0 | 1 / 1 | 2 | No |
| Case-local volatile constants | `-O2` | 1792 | 0x158 | 0 | 1 / 1 | 2 | No |
| Typed 36-byte descriptor | `-O2` | 1728 | 0x140 | 13 | 1 / 1 | 2 | No |
| Clipped coordinates live across lookup | `-O2` | 1744 | 0x148 | 0 | 1 / 1 | 2 | No |
| Explicit local Gfx cursor pointer | `-O2` | **1808** | 0x140 | 13 | 1 / 1 | **78** | No |
| Explicit local Gfx cursor pointer | `-O1` | 2240 | different entry layout | 0 | **3 / 3** | **2** | No |
| Existing corrected diagnostic | `-O1` | 2256 | different entry layout | 0 | **3 / 3** | 78 | No |
| **Original USA reference** | — | **1808** | **0x140** | **452** | **3 / 3** | **2** | Reference |

The superficially size-exact `-O2` cursor pointer variant is **not an improvement in native exactness**: the compiler re-materialises the global address many times and emits 78 relocations where the original requires two. `-O1` suppresses F300/E700 hoisting but does not produce the original size, branch schedule, function entry, stack prologue or object layout. The original function's optimisation flags remain an inference; **do not change verified compiler flags based on one constant-count coincidence**.

### Original-MIPS versus IDO-compiled-MIPS regression

With `--semantic`, the same synthetic-memory interpreter executes the compiler's object code (with **two** legitimate HI16/LO16 relocations resolved) and compares all 64-bit display-list records against the authenticated original function:

- Corrected `-O2` diagnostic: **20/20 scenarios, 5,304/5,304 graphics commands exact**.
- Local-cursor `-O1` diagnostic: **20/20 scenarios, 5,304/5,304 graphics commands exact**.
- The research interpreter's execution window was explicitly extended to each candidate's code extent, and its basic integer decoder extended to support the native `SB` and `SH` stores used by `-O1` output. This is *not* a real gameplay trace or complete MIPS CPU emulator.
- The separately pinned corrected unpadded source still passes its existing regression: 20/20 graphics, original and candidate four invalid-dimension division traps. The rejected *other* compiler variants were tested for code generation and relocation counts, **not** independently for all 20 semantics cases.

This refines the diagnosis: **separate compiler optimisation/memory-lifetime choices are responsible**, but simple C type, volatility, case-block and branch rewrites do not reproduce the original. Recovering the original block-local value lifetimes and exact data/Gfx aliasing from source (rather than adding fake source-local arrays) is the remaining problem. Original ASM stays authoritative.

## Reproduce safely

From this source-only folder, on an authenticated pinned upstream/Splat checkout:

```bash
python3 probe_register_lifetime.py \
  --checkout /path/to/pinned/mnsg \
  --deps /path/to/goemon-dependencies \
  --runtime /path/to/goemon-runtime-additions \
  --output /path/to/new-private-output --semantic
```

Requires only pinned original USA 32 MiB decompressed ROM and original IDO 5.3 installed **locally**, plus Python and `readelf`. The runner refuses pre-existing output and unexpected ROM/toolchain identity. The emitted scratch C/object files and private ROM are not included in this package. The committed JSON contains only compiler statistics, relocation counts and graphics-command **comparison metadata**; no ROM data, assembly dumps, texture assets or binary objects.

**Mandatory pending gates:** full original-address native machine-code equality, current accepted USA stage G2 (full 32 MiB exact ROM, ELF identities, all 82,103 relocation entries), fresh `decomp.verify`, strict inventory, full `decomp.local_ci`. None has been achieved for this still-assembly-owned target. Accepted USA stays **1,965 C functions / 84,648 bytes**.

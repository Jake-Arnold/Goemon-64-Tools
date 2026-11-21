# Original USA file22 large renderer — native IDO frame, stack and lookup study

**Status: RESEARCH_ONLY / FAILED_NATIVE.** The target is the **large** `func_801CC0C4_69ECE4` at ROM `0x69ECE4`, guest `0x801CC0C4`, 1,808 bytes / 452 original MIPS instructions. This is *not* the 60-byte helper. Its original code SHA-256 is `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9` and the user's authentic original 32 MiB USA decompressed ROM SHA-1 is `6ea0ed71032ce08fc2745f412d84936382197494`.

## What was really executed

Native pinned IDO 5.3 compiled the existing 1,744-byte m2c-derived C draft and two **strictly diagnostic** source placements for unknown local storage. No original machine instructions, game assets, generated assembly or patched ROM were used as compiler output. The full target ROM bytes remained the immutable comparison reference.

| Candidate (IDO flags as pinned upstream) | Stack frame | Exact consecutive original words from entry | Raw same word positions | `.text` size | First differing original ROM offset |
| --- | ---: | ---: | ---: | ---: | --- |
| Existing corrected m2c draft | `0xF0` (240 B) | 0 | 21 / 436 | 1,744 B | `0x69ECE4` |
| Add one unused volatile 20-word reserve | `0x140` (320 B) | **12** | 22 / 436 | 1,744 B | `0x69ED14` |
| Distribute 19 unused volatile words at gaps (13/3/2/1) | `0x140` (320 B) | **12** | 22 / 436 | 1,744 B | `0x69ED14` |

**This is a compiler layout experiment, not a matching source claim.** Both diagnostic variants reproduce the original 320-byte frame, all ten original callee-saved stores, and the subsequent `lw` instruction (the first 12 instructions). The first mismatch at original guest `0x801CC0F4` is the choice of temporary register for the original `0xFFFF` constant. Original uses `$t8`; compiled diagnostic uses `$t7`. Full output still differs in size by 64 bytes, the compiler's remaining register assignment/control-flow differs, and object source relocations remain unresolved. The extra volatile locals are not claimed to have existed in Konami's source, nor should they be introduced as production C just to force stack shape.

The first draft's frame discrepancy is therefore **reproducible and isolated**, but fixing it does **not** fix the algorithm's original native codegen.

## Exact original stack uses

All locations below are actual `lw` / `sw` original instruction operands relative to `$sp` (source-derived), **not source-level C variable names**.

| Stack offsets | Live role |
| --- | --- |
| `+0x08..+0x2C` | `$s0..$s7`, `$fp`, `$ra` saved on entry and restored on exit |
| `+0x34` | Outer-loop row's Y pixel coordinate |
| `+0xE0` | Pointer to halfword tile-ID map (descriptor `+0x08`) |
| `+0xE4` | Pointer to byte page map (descriptor `+0x04`) |
| `+0xE8` | Vertical texture-origin clipping offset |
| `+0xF0` | Bottom screen Y coordinate (10.2 display units after scaling) |
| `+0xF8` | Top screen Y coordinate (10.2 display units after scaling) |
| `+0x100` | Previous tile ID, initial `0xFFFF` |
| `+0x138` | Outer row-loop counter, initial zero, 9 iterations |

Significant untouched stack regions within the original 0x140 allocation remain, including `+0x38..+0xDF` and `+0x104..+0x137`. Their original C declarations and allocation reasons are unknown. The diagnostic source groups approximate those gaps without claiming authentic original source identity. The exact original store layout is **not yet recovered**: the gap-distribution trial puts outer index at `+0x13C`, cached tile at `+0x104` and page pointer at `+0xE8`, each four bytes higher than original.

### Nonvolatile register lifetimes (original MIPS)

| Register | Grounded role / use |
| --- | --- |
| `$s0` | Input descriptor, persists across the whole function |
| `$s4` | Current X tile column, 0 through 10 |
| `$s1` / `$s2` | Left/right screen X coordinates, scaled to N64 10.2 units |
| `$s3` | Clipped horizontal S texture-origin adjustment |
| `$s5` / `$s6` | Masked bottom/top Y display-list coordinates |
| `$s7` | Masked vertical T texture-origin adjustment |
| `$fp` | Long-lived graphics word `0x07054150` |
| `$ra` | Saved to stack on entry, reused as graphics word `0xE6000000`, restored for return (there are no outgoing calls) |

The current draft instead hoists more graphics constants across branches and assigns them to different saved registers. This mismatch helps explain register-allocation divergence even after the frame size is corrected. The next native source-shape hypothesis must address **constant lifetime and original local allocation together**, not just append unused arrays. For this >512-byte original target, the two additional bounded native diagnostic variants above were already tested; **no broad automated permuter search was run**.

## Precise tile/page lookup contract recovered from original MIPS

All six **signed** original division operations in the 120-instruction block `0x801CC234..0x801CC414` have known order:

| Original PC | Signed division | Used result |
| --- | --- | --- |
| `0x801CC240` | `x / pixel_width` | Quotient for page column |
| `0x801CC250` | `(x / pixel_width) / grid_columns` | Remainder (`page_x`) |
| `0x801CC2BC` | `y / pixel_height` | Quotient for page row |
| `0x801CC2E8` | `(y / pixel_height) / grid_rows` | Remainder (`page_y`) |
| `0x801CC31C` | `x / pixel_width` again | Remainder for local X tile |
| `0x801CC348` | `y / pixel_height` again | Remainder for local Y tile |

Source-level arithmetic equivalent for the **20 tested positive-geometry cases**, using C signed integer division and remainder (truncate toward zero):

```c
int page_x = (x / pixel_width) % grid_columns;
int page_y = (y / pixel_height) % grid_rows;
unsigned page_id = page_map[page_x + grid_columns * page_y];
int tiles_across = pixel_width / 32;
int tiles_down = pixel_height / 32;
int local_x = (x % pixel_width) / 32;
int local_y = (y % pixel_height) / 32;
int tile_index = page_id * tiles_across * tiles_down
               + local_y * tiles_across + local_x;
unsigned tile_id = tile_map[tile_index];
```

The compiler's `/ 32` generates signed shift and bias correction, not an extra `div` instruction. The original read of the u8 page index is at `0x801CC3AC`; its read of the u16 tile ID is at `0x801CC404`. Original division-by-zero / INT_MIN/(-1) guards are actual MIPS `break`s and must be preserved at the compiler level; this source fragment is **not** a drop-in accepted replacement for exceptional cases.

The added independent `verify_lookup_equations.py` traces both original MIPS loads on each visible tile in the same 20 input scenarios as the previous full-command comparator. **All 1,600 page records and all 1,600 tile records** matched the calculated guest pointer addresses and IDs (**zero mismatches**). This establishes exact intermediate arithmetic for the tested inputs, not just equal final Gfx commands. Existing full graphics comparison still passes **20/20 input scenarios, all 5,304 Gfx records**, and original division guards pass **4/4** with expected trap PC.

## Reproduce

Dependencies: authenticated local original USA 32 MiB decompressed ROM, clean pinned upstream `mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee` with original Splat data generated, local original IDO 5.3 binary under `tools/ido-5.3/cc`, user-supplied dependency/runtime directories, host Python 3 and C compiler. This ZIP has **source only**.

```bash
python3 run_native_stack_study.py \
  --checkout /path/to/pinned/mnsg \
  --deps /path/to/goemon-dependencies \
  --runtime /path/to/goemon-runtime-additions \
  --output /path/to/NEW-stack-diagnostic-directory
python3 verify_lookup_equations.py \
  --rom /path/to/pinned/mnsg/config/usa/baserom.decompressed.z64 \
  --output /path/to/lookup-20.json
python3 compare_model.py \
  --rom /path/to/pinned/mnsg/config/usa/baserom.decompressed.z64 \
  --model file22_tile_display_model.c \
  --output /path/to/semantic-20.json
python3 test_original_traps.py \
  --rom /path/to/pinned/mnsg/config/usa/baserom.decompressed.z64 \
  --output /path/to/guards-4.json
```

Run `run_native_stack_study.py` with an **unused output path**; it refuses overwrites and wrong upstream/ROM hash. JSON contains only counts, offsets, hashes and names, **not ROM bytes or original disassembly**. Any diagnostic `.o` files remain in your private output directory.

## Status and next concrete task

- Original code extent and function identity: **PASS**.
- Actual original IDO 5.3 compilation: **PASS, but FAILED_NATIVE** (1,744 vs original 1,808 bytes).
- Original stack-frame size: **0x140 reproduced in diagnostics only**; variable offsets still differ.
- Precise six-div / 1,600 lookup address/ID comparisons: **PASS for tested cases**.
- Original-MIPS vs host C output: **20/20 full streams exact, 5,304 commands**.
- Four original MIPS division guards: **PASS**.
- Complete accepted-USA-stage exact ROM G2 / ELF / semantic relocation inventory / full `decomp.local_ci`: **NOT_RUN**, because the C candidate is still nonmatching.
- Published USA accepted baseline: **1,965 functions / 84,648 original bytes, unchanged**.

**Next native hypothesis:** match initialization scheduling from original 0x801CC0F4, **reduce hoisted cross-branch constants** so `$fp` holds `0x07054150` and `$ra` holds `0xE6000000`, and align the original sp+0x138 / 0x100 / 0xE4 / 0xE0 locals without synthetic padding. Only then revisit the compiler's six signed division instruction ordering. Preserve the 20-case semantic oracle after any source change. Do not treat source-level agreement or diagnostic padding as exact matching C.

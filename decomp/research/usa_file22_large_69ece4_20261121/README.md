# Original USA file22: direct analysis of func_801CC0C4_69ECE4

**RESEARCH_ONLY / FAILED_NATIVE.** This is the 1,808-byte large function, not the separately exact-matched 60-byte helper. This PR does NOT change canonical accepted-C ownership, manifest, original ASM, game binaries or the main branch.

## Verified function identity

- User-owned authentic original USA decompressed ROM: 33,554,432 bytes, SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`.
- Pinned upstream `klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`; extracted owner `asm/usa/69E080.s` in original static overlay file22.
- Original ROM: `[0x0069ECE4,0x0069F3F4)`, guest: `[0x801CC0C4,0x801CC7D4)`, **0x710 = 1,808 bytes = 452 instructions**. Original function SHA-256: `eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`. The Splat extent and authenticated ROM slice were independently checked.
- Stack: **0x140 bytes**, saving `$ra,$fp,$s0..$s7`. **75 basic blocks**, 46 conditional branches, exactly two backward branches (`0x801CC780 -> 0x801CC1AC` and `0x801CC790 -> 0x801CC128`), 6 signed divide instructions with 12 trap/break instructions, 4 unsigned multiplies, 68 loads, 98 stores. The target body has **zero jal/jalr** calls.
- One direct caller within the same overlay: `func_801CBF98_69EBB8` calls the target at **0x801CC08C**. Original wrapper checks the first halfword of `D_801D7030_6A9C50`, then passes that global as argument 0. The existing 60-byte exact C neighbour `func_801CBF5C_69EB7C` copies 36 bytes from static `D_801D536C_6A7F8C` into that global earlier during initialization.
- **Only direct global used by the target**: the display-list write pointer `D_801D701C_6A9C3C`. Several indirect input-map/texture reads, no callee calls. This is **a graphics tile/display-list builder**, not an unknown general dispatcher.

## Input descriptor (conservative original MIPS ABI)

The input is a **36-byte struct**, inferred from load offsets and independently supported by the 36-byte original helper. The original static descriptor at ROM `0x6A7F8C` has **format 2, page columns 1, page rows 1, pixel width 320, pixel height 256**. This is a source-data observation, not a claim that values are immutable at runtime.

| Offset | Access | Interpretation |
|---|---|---|
| +0x00 | caller `lhu` | enabling halfword |
| +0x04 | target `lw`, then `lbu` | byte page-index map pointer |
| +0x08 | `lw`, then `lhu` | u16 tile-ID map pointer |
| +0x0C | `lw`, then `lhu` in formats 1/2 | u16 descriptor lookup |
| +0x10 | `lw` | texture base guest pointer |
| +0x14 | not read by target | unknown / unverified |
| +0x1A | `lbu` | texture mode 0 / 1 / 2 |
| +0x1C/+0x1E | signed `lh` | page grid width / height |
| +0x20/+0x22 | signed `lh` | page pixel width / height |

## Recoverable algorithm (hypothesis, not matching C)

Nine outer iterations traverse Y cells of 32 pixels; eleven inner iterations traverse X cells of 32 pixels. Bounds clipped to screen **320×240** yield **80 drawn cells** on the default 1×1 page descriptor (10 columns, 8 rows).

For each visible cell with top-left (x,y):

```text
page_x = (x / page_width) % grid_columns
page_y = (y / page_height) % grid_rows
page_id = page_map[page_x + grid_columns*page_y]  # u8

tiles_across = page_width / 32
tiles_down   = page_height / 32
tile_index   = page_id*(tiles_across*tiles_down)
             + ((y % page_height) / 32)*tiles_across
             + ((x % page_width) / 32)
tile_id = tile_map[tile_index]                     # u16

if tile_id differs from last_tile_id:
    emit 7 texture load/setup Gfx entries per active format (0,1,2)
emit E4 display rectangle, B4 texture coordinate, B3 slope entries
```

Format 0 emits `FD10/F510/E6/F3/E7/F510/F2`; formats 1 and 2 use `FD50/F550/E6/F3/E7/F548 or F540/F2`. Each Gfx record consists of two 32-bit words and increments the shared display-list cursor by 8 bytes. The `E4` rectangle uses 10.2 screen coordinates (pixels ×4). Tile changes are cached; repeated IDs avoid seven setup entries. The final command is `B3000000,10000400`. The original MIPS guards divide-by-zero and INT_MIN/−1 through `break` instructions.

**Caution:** the host C model applies extra bounds/capacity checks not present in the original, and there has been **no comparison of complete Gfx command sequences against actual game/emulated MIPS runtime output**. Model tests validate internal consistency only. The m2c draft has unresolved edge semantics (especially signed negative-coordinate cases). No original ASM or ROM bytes are included in any source.

## Actual native and host test results (21 Nov 2026)

- Structural analysis from authenticated ROM and exact original source: **PASS**, CFG 75 blocks / two back edges. Generated machine-readable metadata and Graphviz CFG from source-only script, without distributing original disassembly.
- Host semantic **model**: GCC ASan/UBSan PASS and Clang ASan/UBSan PASS for 0/1/2 mode setup, synthetic 80-tile scan, texture-ID caching, clipping and bounds/capacity rejects. These do **not** establish original equivalence.
- **IDO 5.3 trial 1** from original m2c draft: **FAILED_NATIVE**; emitted text **1,760 bytes** vs expected **1,808**; only **14/440** unrelocated positional machine-word equalities. At entry the original stack frame is `0x140`, trial emitted `0xF0`.
- **IDO 5.3 trial 2**, after pointer width and signed-branch corrections: **FAILED_NATIVE**; text **1,744 bytes**, **21/436** unrelocated positional word equalities; first mismatch at original ROM **0x69ECE4**. The isolated native C object contains two HI16/LO16 relocations to `D_801D701C_6A9C3C`, but those do not establish original linker correctness. The trial emits a different prologue and register allocation.
- Both bounded source variants for a >512-byte target were tried, per the existing executor budget. No exact match: **full source-unit linking, USA1,965 accepted-stage G2, strict inventory, and full decomp.local_ci NOT_RUN**. Do not promote.
- This is new *direct* large-function analysis. Separate 60-byte helper [PR #160](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/160) remains scratch exact, not canonical; runtime file22 evidence is in [decomp PR #156](https://github.com/Jake-Arnold/Goemon-64-Tools/pull/156).

## Reproduction and source kit

The exact **source-only** package was handed to the user in ChatGPT as `goemon-usa-file22-large-cfg-ido-research-20261121.zip`, SHA-256 **`eac49d831bc7792be72eb787a8d6d45236da57956e833e0e352aa9f9e29e3b84`**. It includes:
`analyze_file22_function.py`, `verify_file22_large_research.py`, the annotated m2c-to-C IDO draft, the C tile rendering host model, synthetic sanitizer test, original-code SHA-verified CFG metadata, Graphviz DOT and a sanitized failed-native proof. No original raw disassembly/ASM, ROMs, binaries, MIPS objects, proprietary compiler or game assets.

On locally pinned original-USA upstream with restored private toolchain:

```bash
python3 verify_file22_large_research.py \
  --checkout /path/to/pinned/mnsg \
  --deps /path/to/goemon-dependencies \
  --runtime /path/to/goemon-runtime-additions \
  --output /path/to/NEW-output-directory
```

This reproduces the IDO mismatch and host-only model tests without modifying the upstream checkout. `dot -Tsvg cfg.dot -o cfg.svg` renders the 75-block CFG.

## Repository boundary and next technical hypothesis

The executable hook integration legitimately lives in [native recompilation PR #1](https://github.com/Jake-Arnold/Goemon64Recomp-JP/pull/1), because it instruments `Goemon64Recomp-JP` runtime. **Matching C, semantics, data layout and proof are owned by this `Goemon-64-Tools` decomp research**, not the native launcher. The two need links, not duplicated runtime patch code.

To progress beyond the failed IDO drafts, reconstruct the precise original stack variables/copy patterns and register live ranges around outer loop `0x801CC128` and inner loop `0x801CC1AC`, then pursue a specific IDO source-level hypothesis with measured first-mismatch improvement. Do not rerun loader probes or promote from synthetic tests. Accepted USA baseline remains **1,965 C / 84,648 bytes**.

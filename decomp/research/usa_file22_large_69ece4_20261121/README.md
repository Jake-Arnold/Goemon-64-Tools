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

## Stack/data-liveness observations for next IDO hypothesis

All offsets below are direct, source-verified original MIPS stack accesses, **not inferred C member offsets**:

| Original stack offset | Data role / original reads and writes |
|---|---|
| `sp+0x138` | outer 0..8 row counter; initialized at `0x801CC114`, read at outer-loop header `0x801CC128` and incremented in outer loop tail |
| `sp+0x100` | previous tile ID cache; initialized to `0xFFFF`, compared at `0x801CC408`, updated at `0x801CC414` |
| `sp+0xE4` | pointer loaded from descriptor `+0x04` (byte page map), saved at `0x801CC0FC` |
| `sp+0xE0` | pointer loaded from descriptor `+0x08` (u16 tile ID array), saved at `0x801CC124` |
| `sp+0x34` | outer row pixel coordinate `row * 32`, stored at `0x801CC14C` |
| `sp+0xF8` | clipped top coordinate subsequently shifted by two for 10.2 rectangle command |
| `sp+0xF0` | clipped bottom coordinate shifted by two for 10.2 rectangle command |
| `sp+0xE8` | vertical clipping/texture origin compensation, shifted by five |

Register lifetime clues: `$s0` preserves the input descriptor pointer and `$s4` is the inner loop column counter. `$fp` holds the texture tile-setup word `0x07054150`; `$ra` is saved in the prologue and **reused internally as constant `0xE6000000`** because this function executes no outgoing calls, then restored before return. This is important for reproducing exact IDO scheduling; omitting these long-lived constants in C explains some register allocation differences but does not, by itself, prove a matching source.

**Return value:** the only exit is the original `jr $ra` epilogue. The caller does not consume a specific return value. An intended `void` return is a supported source hypothesis, but no independent C type declaration has been recovered; do not claim a proven original prototype.

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


## Source-image attribution and text-token exclusion (21 November 2026)

This additional experiment was run against the SHA-1-pinned user-owned
33,554,432-byte original USA decompressed ROM, **not** a fabricated texture
or an inferred screenshot. Original file/resource 22 is
ROM `[0x69E080,0x6A9920)`, virtual `[0x801CB460,0x801D7060)`.

The default descriptor source `D_801D536C_6A7F8C` at ROM
`0x6A7F8C` has mode 2 and a 1x1 page grid of 320x256 source pixels.
Its guest pointers and reconstructed source meanings are:
- `+0x04 = 0x801D4C30`, one-byte page map (page index zero);
- `+0x08 = 0x801D4B90`, 80-entry u16 tile map (10 columns, 8 rows);
- `+0x0C = 0x801D4CD8`, per-tile u16 descriptor lookup;
- `+0x10 = 0x801D4190`, texture-byte base;
- `+0x14 = 0x801D4D28`, pointer to 16 consecutive 16-bit RGBA5551
  palette entries; **this pointer is not read in the large function itself**.
  The palette's use by the surrounding display-list setup must be traced
  separately before claiming every rendering side effect.

The eight original tilemap rows are uniform and use tile IDs
`[0,0,0,0,4,3,2,1]`, with ten repeated copies across each row.
Five original CI4-style 32x32 indexed tiles, 512 bytes each, combine
with the source palette to reconstruct a **320x240 black-to-dark-blue
vertical gradient** (black at the top, muted blue at the bottom).
The locally reconstructed PNG is a **background-only source-data preview**,
not a captured guest frame and not a complete screenshot with title/logo.

**Text-token test:** the original file22 resource contains **zero**
aligned instances of the script opcode `0x00008010`, the static text
record command used by the USA dialogue index in
`Goemon-64-Tools/main:practice/dialogue_rom.py`.
The large target's original instructions contain no call to the
dialogue glyph parser and no signed-halfword text-token stream walk:
its u16 values are **tile IDs and per-tile descriptors**, not glyph
codes. The Japanese `practice/dialogue_japan.py` mapping (including the
160-kana block) is region-specific and cannot be used to interpret the
USA texture bytes. Accordingly, **there is no direct embedded text for
our token table to decode in this renderer**. This does not exclude
other startup overlays drawing text above this background.

The previous actual USA run entered the routine in startup outer state 3
around t=0.612 s; file22 was replaced by file20 around t=2.412 s.
This strongly supports a **startup/intro presentation backdrop**, rather
than the recurring stage dialogue-box background (which is handled by
separate main-segment text/window paths). The **specific named startup
screen remains unconfirmed** without a time-synchronised game screenshot.

Read-only source-only reconstruction kit delivered in the ChatGPT
conversation: `goemon-file22-background-attribution-source-20261121.zip`
SHA-256 `cfbd3eca8a5f89db06310753cc5ccb3053ca2cbf2e07f8cc07a958ebdd08fb07`,
containing a pinned-ROM decoder, metadata report and reproduction guide.
No ROM bytes, raw extracted ASM, private game asset or generated preview
is included in this PR. The original 1,808-byte C candidate remains
FAILED_NATIVE; no fresh IDO pass or accepted-count increase is claimed.

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

## 2026-11-21 original-MIPS-to-C **graphics output equivalence** (new, source-grounded)

**Evidence status: RESEARCH_ONLY / BEHAVIOURALLY_EQUIVALENT_FOR_20_CONTROLLED_CASES / FAILED_NATIVE_IDO.**
This is direct progress on the **1,808-byte function itself** rather than on another helper.

A self-contained original-MIPS integer interpreter was written against the
user's actual authenticated USA 32 MiB decompressed ROM (SHA-1
`6ea0ed71032ce08fc2745f412d84936382197494`). It authenticates the
original 1,808-byte function slice (SHA-256
`eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`),
maps the original file22 overlay and 36-byte static descriptor into
synthetic big-endian guest address space, seeds an empty Gfx output buffer
and executes **the genuine original MIPS integer instructions** until
the original `jr $ra` return. It implements branch-delay execution
(including annulled branch-likely), 32-bit signed division with original
compiler-emitted guards, HI/LO multiply, signed/unsigned loads, and guest
stores. It does **not** use a real emulated N64 game frame.

The independently host-compiled research C model
`file22_tile_display_model.c` was then run against the **same 20 input
sets**, and both outputs compared **every 64-bit Gfx record**, not just
counts or hashes:

| Parameter | Cases | Result |
|---|---|---|
| Modes | 0,1,2 and unsupported selector 3 | 4 |
| Input geometry/map | Original, reordered tile rows, all-zero rows, synthetic 2x2 pages of 160x128 px, synthetic 5x4 pages of 64x64 px | 5 |
| All pairs | **20 / 20 exact output comparisons**, **5,304 / 5,304 Gfx entries**, **0 word differences** | **PASS** |

The authentic original mode-2 descriptor produces **12,568 original MIPS
instruction executions**, 80 rectangles, five changes of tile texture,
**275 64-bit commands** (2,200 bytes). Full command-stream SHA-256:
`686ed1d46bc0029443baaf867759f648861f43ff21f35acf24f4b12788833091`.
Mode 3 emits just the 80×3 rectangle commands (240) and no texture setup.

The compiler-generated original `break 7` division guards were reached
at the exact expected PCs for four deliberately invalid synthetic
dimensions: source width=0 at `0x801CC270`, source height=0 at
`0x801CC2CC`, page columns=0 at `0x801CC294`, and page rows=0 at
`0x801CC2F4`. All **four guarded exception paths PASS**.

Across formats 0–3 and the positive default geometry, **409 of 452**
unique original instruction addresses are executed (90.5%). The four
invalid-input guards extend that observed set to **413 of 452** unique PCs;
the remainder primarily includes signed-coordinate/exception branches
outside the tested input domain. **PC coverage is of this isolated
synthetic interpreter, NOT a real guest PC sample.**

### Exact eleven-phase partition and native-matching priorities

| Stage | Original guest instruction range (end exclusive) | Static instructions |
| --- | --- | ---: |
| Initial 0x140 frame, source setup and globals | `0x801CC0C4..0x801CC128` | 25 |
| Outer Y scan and vertical clipping | `0x801CC128..0x801CC1AC` | 33 |
| Inner X scan and horizontal clipping | `0x801CC1AC..0x801CC234` | 34 |
| Signed division, page and tile resolution | `0x801CC234..0x801CC414` | 120 |
| Last-tile cache and format selection | `0x801CC414..0x801CC444` | 12 |
| Format-0 seven-command setup | `0x801CC444..0x801CC528` | 57 |
| Format-1 seven-command setup | `0x801CC528..0x801CC620` | 62 |
| Format-2 seven-command setup | `0x801CC620..0x801CC70C` | 59 |
| Three rectangle / S-T / slope commands | `0x801CC70C..0x801CC780` | 29 |
| Inner-loop tail | `0x801CC780..0x801CC790` | 4 |
| Outer-loop tail and saved-register return | `0x801CC790..0x801CC7D4` | 17 |

These boundaries account for **all 452 original instruction positions**,
including delay slots. The **tile/page index region alone executed 7,035
instructions** on original format-2 input, more than half the function's
dynamic work. This suggests a bounded, focused IDO matching strategy:
retain the behaviourally verified C equations, recover register
live ranges/stack slots for the entry and division/lookup region, and
compare original/native output block-by-block rather than guessing the
entire routine again. In particular the original saves `$s0..$s7` and
`$ra/$fp`, uses stack `0x140`, and carries long-lived
`$fp=0x07054150` and `$ra=0xE6000000` constants. The first two
original IDO C hypotheses still generate **1,760 and 1,744 bytes**,
not original **1,808**. **No new IDO exactness or full-ROM G2 is claimed.**

### Reproducibility and limitations

A tested **source-only ZIP** (no ROM, original assembly/code dump, game
asset, game memory trace or proprietary compiler) was delivered in ChatGPT:
`goemon-usa-file22-mips-c-semantic-proof-20261121.zip`, SHA-256
`27d2345b2b27694fc3b57133300dd38af990ddb8a7756bdd4b87a3ff32dc652d`.
It contains `trace_original_file22_mips.py`, `compare_model.py`,
`phase_report.py`, `test_original_traps.py`, model C source,
metadata-only evidence and a reproduction README. After independently
extracting the final ZIP, all 20/20 commands tests, 409-PC coverage and
4/4 break guard checks were rerun and PASS. It requires the user's own
SHA-1-pinned original USA 32 MiB decompressed ROM, Python 3 and a host C
compiler; it writes reports to locally chosen paths.

The interpreter itself is research code, **not** a separately validated
production MIPS emulator; exact output for 20 synthetic experiments does
not prove universal signed-range behaviour or original source syntax.
This does not prove a sampled real-game PC, frequency of live redraw,
file22 ownership for the entire ~4-second on-screen gradient, native
compiler instruction equality, or production C acceptance. A completed
frame may persist after its original overlay code is overwritten.
The prior full-ROM/ELF/relocation G2 gates were not run on this
**still-nonmatching 1,808-byte function**. USA accepted C remains 1,965.

## New original-USA native-stack and lookup-equation study (21 November 2026)

**New source-owned, independently rerun experiment:** [native_stack_study/README.md](native_stack_study/README.md) contains the tested exact original stack map, original $s0..s7/$fp/$ra lifetimes, six signed-division order, small IDO C probe harness, and executable original-MIPS intermediate-load oracle. All nine source files are committed in [native_stack_study/](native_stack_study/) without any ROM, extracted ASM, object, toolchain or runtime memory dump.

- Original IDO 5.3 compiler compiled the existing corrected draft: `1744 B` object, `0xF0` stack, **21/436** raw positional machine words (unresolved relocations), first mismatch at original ROM `0x69ECE4`.
- A **source-diagnostic only** unused-volatiles probe reproduces the original `0x140` stack and first **12 consecutive identical MIPS instruction words**, moving the first mismatch to original ROM `0x69ED14` (guest `0x801CC0F4`). It still emits `1744 B` versus original `1808 B`, with **22/436** raw same-word positions. A layout-aware 13/3/2/1 reserve distribution also produces `0x140` and **12 exact initial words**, but still places original local slots four bytes off. **Never claim these speculative arrays are actual Konami source.**
- Original register evidence: `$s0` descriptor; `$s4` inner X column; `$s1/$s2/$s3` clipped X/texture origin; `$s5/$s6/$s7` Y coordinates and T origin; `$fp=0x07054150`; and saved/restored `$ra` reused as `0xE6000000` while no calls occur. The current draft hoists more texture constants into different saved registers, explaining why frame-size matching alone is insufficient.
- The independent address-level MIPS lookup tracer verifies **1,600/1,600** page+tile intermediate lookups across the 20 input cases, matching guest **page-map pointer, page ID, tile-map pointer and tile ID** using the six recovered original signed divisions. No intermediate differences.
- Existing full display-list oracle was re-run from a **fresh extracted package**: **20/20** identical command streams, **5,304/5,304** 64-bit commands. Original MIPS divide-guard tests: **4/4 exact break PCs**.
- Full source-only ZIP in the ChatGPT handoff `goemon-usa-file22-native-ido-stack-lookup-study-20261121.zip`, SHA-256 `01ec23e186fc0be59512d8c2c174b6169bc1b7a6b2f2ad84997ce65dc550f6ff`. Verified every ZIP source Git blob SHA against the generated local source. Direct commands are documented in `native_stack_study/README.md`.
- **Status:** `RESEARCH_ONLY / FAILED_NATIVE`. These diagnostic probes exhaust the bounded additional original IDO variants for this attempted source shape; no native original-address full match, no new G2, strict inventory or full local CI. Published USA matching C remains **1965 / 84648 bytes**.


## Repository boundary and next technical hypothesis

The executable hook integration legitimately lives in [native recompilation PR #1](https://github.com/Jake-Arnold/Goemon64Recomp-JP/pull/1), because it instruments `Goemon64Recomp-JP` runtime. **Matching C, semantics, data layout and proof are owned by this `Goemon-64-Tools` decomp research**, not the native launcher. The two need links, not duplicated runtime patch code.

To progress beyond the failed IDO drafts, reconstruct the precise original stack variables/copy patterns and register live ranges around outer loop `0x801CC128` and inner loop `0x801CC1AC`, then pursue a specific IDO source-level hypothesis with measured first-mismatch improvement. Do not rerun loader probes or promote from synthetic tests. Accepted USA baseline remains **1,965 C / 84,648 bytes**.

# Original USA file22 large renderer: actual IDO-compiled MIPS semantic fix

**Status: RESEARCH_ONLY / BEHAVIOURALLY_EQUIVALENT_IN_20_CONTROLLED_CASES / FAILED_NATIVE.**

Target: original USA `func_801CC0C4_69ECE4`, ROM `0x69ECE4..0x69F3F4`, guest
`0x801CC0C4..0x801CC7D4`, **1,808 bytes/452 original instructions**.
Original function SHA-256:
`eaccca6679247d56785806a92a2efe4c1adb73368f723b76d4b6aab5040ef3a9`.
Authenticated USA decompressed 32 MiB ROM SHA-1:
`6ea0ed71032ce08fc2745f412d84936382197494`.

## Significant discovery: earlier IDO source had a real arithmetic bug

The prior `file22_ido_trial.c` declared its tile-index-map pointer as `u16*`
but then added a *byte* offset expression to that halfword pointer. The
original expression multiplied each tile-index term by two; the C pointer
addition multiplied it by two **again**. This caused incorrect tile IDs and
texture-cache misses. The old, real IDO-compiled MIPS renders **429** Gfx
commands for the original mode-2 startup data instead of **275**.

The corrected source removes exactly the three redundant `* 2` terms from the
`spE0` pointer addition; C pointer arithmetic now supplies the required
2-byte stride once. The original MIPS intermediate-read oracle had already
proved the correct page and tile equations independently; this exercise
finally checks that the actual IDO C source implements them.

## Measured comparisons (actually executed with original IDO 5.3)

Each of the four C source variants is compiled with the pinned native IDO
5.3 and original `-O2 -mips2` flags. The harness reads the original
ROM-backed MIPS routine and the compiled candidate instructions, requires
the original global pointer's exact **two HI16/LO16 relocations**, links
them to the original guest symbol in *synthetic RAM*, and runs each complete
function in the same original-instruction interpreter. **Every** pair of
64-bit graphics commands is compared over **20** modes/layouts, not just
counts or hashes.

| Source | IDO `.text` | Stack | Exact entry prefix | Full original-MIPS-vs-IDO Gfx streams |
|---|---:|---:|---:|---:|
| Prior double-scaled m2c negative control | 1,744 bytes | 0xF0 | 0 instructions | **8/20 PASS; 12 FAIL** |
| Corrected C, no artificial stack storage | 1,744 | 0xF0 | 0 | **20/20 PASS** |
| Corrected C with earlier frame-padding diagnostic | 1,744 | 0x140 | 13 | **20/20 PASS** |
| Corrected C, 8 original stack offsets matched diagnostically | 1,744 | 0x140 | 13 | **20/20 PASS** |

Across 20 standard inputs (four texture modes × five original/synthetic
page/tile layouts), the corrected original-IDO MIPS and authenticated
original ROM MIPS emit **5,304/5,304 identical Gfx commands**, zero
mismatches. The original source mode2 emits **275** commands, including
80 rectangles and five 7-command texture setups. The old double-scaled
negative control gives 4,122 mismatching command positions across its
12 failing cases, and 429 commands instead of 275 on the default modes
0/1/2. In mode3, no tile setup is generated, so the old bug is not exposed.

The original and corrected compiled variants both trap on the same four
invalid-dimension classes (zero page width/height and zero grid columns/rows).
The **guest break PCs differ** because the native generated machine code is
not exact; this is not a claim of identical exception instruction placement.

The earlier independent *host*-compiled C model was rerun: **20/20** streams,
5,304/5,304 commands. The original instruction intermediate address oracle
was rerun: **1,600/1,600** page/tile lookups. The original four division
traps remain verified at original instruction addresses. No emulator frame
or real-game PC was sampled here; all execution is isolated/synthetic.

## Stack-frame and saved-register findings

Original IDO object saves `$ra,$fp,$s7..$s0`, stack frame **0x140**. The
corrected source without padding is **0xF0** and differs from the first
instruction. Additional, clearly **artificial** unused local arrays can
coax IDO into a **0x140** frame and match the first **13 consecutive
original 32-bit instruction words**, plus the observed functional stack
**offsets** `0x34`, `0xE0`, `0xE4`, `0xE8`, `0xF0`, `0xF8`, `0x100`, `0x138`.
The instruction counts at those offsets still differ: the diagnostic's row
counter is loaded twice in the inner loop header where the original often
loads it four times. Do **not** infer that the original Konami source
contained these unused arrays or accept them as a real decomp source.

Important remaining original-native discrepancy: the original holds
`0x07054150` in `$fp` and `0xE6000000` in `$ra`, but the corrected candidate
assigns these long-lived constants to different callee-saved registers.
Original case-local `lui` counts: `0xF300` **3**, `0xE700` **3**; candidate
hoists each to **1**. The original uses **452 instructions (1,808 bytes)**;
the corrected IDO model uses **436 (1,744 bytes)**, 64 bytes shorter.
The original and corrected *semantic outputs* match on tested cases but
machine code, register allocation, loop scheduling and relocation placement
do not. A source-level `switch` to `if/else` or typed `Gfx` pointer rewrite
was also tested and did not solve constant hoisting. A global pointer alias
increased text to 1,792 bytes but introduced **78** symbol relocations
rather than the original two; it is **not** a valid closer matching path.

## Reproduction (read-only; original ROM/compiler required locally)

The source-only kit contains:

- `reproduce_compiled_ido.py`: native toolchain compile, original-MIPS vs
  translated candidate-MIPS 20-case byte-exact Gfx comparison, four traps
  and fail-closed relocation checks.
- `trace_original_file22_mips.py`: the existing minimal original-MIPS integer
  interpreter, executing actual ROM instructions in synthetic guest RAM.
- `prior_nonmatching_double_scaled.c`: legacy **incorrect** negative control.
- `usa_file22_1808_corrected_semantic.c`: corrected arithmetic, no fake locals.
- `usa_file22_1808_stack_layout_diagnostic.c`: corrected arithmetic plus
  former diagnostic frame padding.
- `usa_file22_1808_all_eight_stack_slots_DIAGNOSTIC.c`: corrected arithmetic
  plus synthetic allocation probes that reproduce all eight source-backed
  stack addresses; **not original C source**.
- `compare_model.py`, `file22_tile_display_model.c`,
  `verify_lookup_equations.py`, `test_original_traps.py`: previous independent
  reference tests, unchanged.
- `evidence.json`: count/hash/check summaries only.

On a pinned, **already SPLAT-decompressed** original-USA checkout
`klorfmorf/mnsg@7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee`:

```bash
python3 reproduce_compiled_ido.py \
  --checkout /path/to/pinned/mnsg \
  --deps /path/to/goemon-dependencies \
  --runtime /path/to/goemon-runtime-additions \
  --output /path/to/NEW-private-output-directory
```

The script refuses wrong ROM SHA-1/function SHA-256, unexpected IDO symbol
relocations, pre-existing output directory and failed semantic regression.
Generated original compiler object files are **private local scratch only**.
No ROM, extracted original ASM, raw code bytes, game data, palette,
texture asset, proprietary toolchain, compiled objects or generated output
were placed in this archive.

**Not run:** complete accepted-USA1,965-stage G2, original-ROM linked
candidate replacement, complete ELF identity/82,103 relocation match,
strict accepted C inventory, full `decomp.local_ci`, gameplay emulation.
Those are deliberately blocked until native machine code matches.
The canonical USA accepted baseline remains **1,965 functions / 84,648
original instruction bytes**. No merge or promotion authorized by these
semantics checks alone.

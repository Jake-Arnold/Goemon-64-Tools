# USA dialogue window horizontal geometry — 19 November 2026

**ROM:** Original decompressed USA 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Original instruction addresses below use USA guest MIPS; main-segment ROM image offset is VMA minus `0x7FFFF400`. This is source analysis for the existing Toolkit, **not** a matching-C promotion or an emulator display test of the new algorithm.

## Why the former 256 value was misleading

The style table at guest `0x800627F0` / image `0x633F0` contains 12 records of 36 bytes. Each record includes the background CI4 texture pointer (word 0), palette/TLUT pointer (word 1), stride (word 2 = **256**), columns (word 3 = 8), and rows (word 4 = 5/7/9). The window's `+0x3E` field receives the stride and texture processing uses it; **the 256-pixel stride does not imply 256 pixels of painted window background**.

Reading every CI4 pixel from original image texture pointers, decoding the 16-entry RGBA16 palette and treating alpha bit zero as transparent shows:

| Styles | Texture VMA | Palette VMA | Source stride | Opaque visible horizontal span | Background height |
| --- | --- | --- | ---: | --- | ---: |
| 0–1 | `0x8005BB70` | `0x80062770` | 256 | `[0, 256)` | 72 |
| 2–3 | `0x80060370` | `0x80062790` | 256 | `[0, 160)` | 56 |
| 4–5 | `0x8005DF70` | `0x80062790` | 256 | `[0, 160)` | 40 |
| 6–11 | `0x8005BB70` | per native style table | 256 | `[0, 256)` | 72 |

Source-pixel sample at mid-height shows the decorative last four columns in all three types of artwork; these are reserved in the conservative content estimate. The index/palette assumptions and expected span are asserted against the pinned ROM in tests. A tampered transparency entry fails closed rather than silently expanding the inferred width.

## Original glyph placement and the conservative horizontal limit

- `8000C7A8`: initial window text x origin at `window +0x50` is **10** (`sw` / original window allocation path).
- `8000D0A0`: glyph allocator `D060` loads that `+0x50` x origin, then `8000D0A4` adds the current horizontal advance `+0x6E`.
- `8000D1E0`: the glyph entry starts **4** units farther to the right than the allocation argument.
- `8000D1D0 / 8000D1EC`: entry drawing width is **10** units. (`li 10`, then `sh` into entry `+0xC`.)
- `8000D138..8000D154`: after emitting a token, `+0x6E` advances by the ROM's byte width table `0x8005BB10` (`0x5C710`) **plus 1**. Known advances range from 3 through 9.

For initial unscaled window geometry, the glyph entry's horizontal draw box begins at **window x + 14 + prefix text advances**. The visible right border starts at artwork width minus 4. To guarantee that even a final *narrow* glyph's 10-unit box does not overlap it, take the conservative total-advance bound:

`safe_advance_limit = opaque_artwork_width − 4 (right border) − 14 (text x start) − 10 (glyph box width) + 3 (smallest native glyph advance)`

This yields **135 font-advance units** for styles 2–5, and **231 units** for styles 0–1/6–11. These are safe estimates for the initial unscaled artwork, not exact per-string maximum occupancy or guaranteed clipping positions. Different final glyph widths could sometimes fit more. Conditional, animated, scaled or custom-modified windows remain separately unverified.

### Kai Highway case (resource 82)

Original source-backed script trace: at `+0x40` sets style 5, opens the window with `+0x50`, prints `[Kai]` at `+0x58` with native `-60`, then references the editable `+0x1C` area-name record with `+0x60`. The area name starts on **line 2 of 2**. Original record's eight leading spaces occupy **72 advance units** and the original full line's peak width is **122**. The user's edited `Monster Monster Monster` has width **165**, exceeding the 135-unit source-based conservative horizontal limit and matching the observed in-game overflow.

## Toolkit behavior and deliberate guardrails

The **Native (auto when traced)** window profile is now the default. Where a static direct-script path identifies the style, the editor reports source-derived artwork width, conservative advance limit, line start and remaining line capacity, and warns of overflowing edits without needing a manual value. Manual width/line entries are disabled for this profile and remain available under manual profiles. A manual value can tighten, but **cannot override** a known native conservative bound. Native wrapping is permitted only when two or more lines remain and all original safety checks pass; single-line area names are rejected. When no source-backed style is known, the UI refuses native wrap and gives no invented automatic width.

## What still needs runtime confirmation

- The actual per-glyph RDP texture rectangle and any dynamic per-window scaling/clipping flags as used in particular cutscenes (the proposed cap is deliberately conservative).
- Lines rendered while opening/closing the animated window; arbitrary callbacks and indirect style changes are not inferred from local static patterns.
- Visible effects of control `-57..-50` beyond source-verified window-field writes.
- Multi-page conversation graph traversal, indirect text references and generated RAM text.
- A live Project64/Mupen test of new opt-in native wrapping for a normal NPC dialogue box; the user's screenshots verify width overflow and native `-60` newlines for Kai, not this new automatic choice.

**Verification:** 51 focused dialogue/ROM/GUI tests passed under portable Python 3.12.16 + Xvfb + `lzkn64==0.2.0`; original USA compressed and decompressed images were provided and SHA-1-pinned. Tests do not imply full Toolkit Linux/Windows regression, JP support or a fresh in-game test.

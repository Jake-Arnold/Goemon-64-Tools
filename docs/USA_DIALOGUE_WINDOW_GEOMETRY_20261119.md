# USA dialogue window geometry and control evidence — 19 November 2026

Source: original USA N64 decompressed image, 32 MiB SHA-1 `6ea0ed71032ce08fc2745f412d84936382197494`. Main-segment image offset = guest VMA − `0x7FFFF400`. Original MIPS is the evidence; these are not matching-C claims.

## What is proved directly by original instructions

- `800038B4` calls `8000B8A4` with `0x800627F0` and `8000B8AC` stores the pointer to `0x80167C54`. This is the **12-row, 36-byte window style table** at decompressed ROM `0x633F0`.
- `8000C260` uses the style index passed via VM word `0x801C7768`. At `8000C28C..8000C2BC`, it copies entries of the selected style into arguments for `8000C6A8`. Do not mistake style-table word +8 (`256`) for independently verified textbox width; it also participates in texture geometry.
- `8000C6A8` stores style words +8/+12/+16 in window fields `+0x3E/+0x40/+0x42`; stores the product of the latter two fields in `+0x6A`. Its initial font y-inset at `+0x54` is **7** and line step at `+0x76` is **16**.
- `8000C3EC` implements the native `-60` line break: zero `+0x6C` (column) and `+0x6E` (horizontal advance), increment `+0x72` (line index), add `+0x76` (16) to the drawing y-offset at `+0x74`.
- Glyph bitmaps contain 12 rows and the renderer's glyph-entry pool contains 120 slots. Thus under the default initial layout, a **conservative full-glyph line count** is `1 + floor((background_height - 7 - 12) / 16)` for a nonnegative result. This count applies to the default unscaled style window with no runtime geometry changes. It is not a complete clipping or presentation simulation.

| Style indices | Style words +12/+16 | Background height | Conservative complete lines |
| --- | --- | ---: | ---: |
| 0–1, 6–11 | 8 × 9 | 72 | 4 |
| 2–3 | 8 × 7 | 56 | 3 |
| 4–5 | 8 × 5 | 40 | 2 |

These values are inferred for visible full glyph rows from the *original* dimensions/insets and the 12-row font. Window open/close animations, transforms, and subsequent control commands may alter rendered placement. The Toolkit reports these counts only when a **bounded straight-line static script path** identifies a window style; other records retain manual limits.

## Kai Highway resource 82 — verified static script path

Resource 82 at decompressed `0x73E130`, virtual start `0x08000000`:

| Resource-relative script offset | Command / result |
| --- | --- |
| `+0x40` | `0x8004`: immediate assignment `0x801C7768 = 5` |
| `+0x50` | `0x8010`: text record `+0x0` opens window (`-70`) |
| `+0x58` | `0x8010`: text record `+0x4` prints the `[Kai]` heading and `-60` line break |
| `+0x60` | `0x8010`: text record `+0x1C` starts on **line 2 of 2** |

The initial `Highway` text record contains eight *real* leading space tokens. Font table at image `0x5C710` gives space advance `8 + 1 = 9` each, so the indentation contributes **72 horizontal font units**. This explains the user's first overlong text starting partway through the box. Omitting the spaces explains the left-aligned lines in the subsequent in-game screenshot.

The user's test replacement with eight explicit lines spans below the visible area-name background; this is visual evidence that newlines continue moving the glyph origin without expanding the box, and that this tested style does not clip text to its painted bounds. It does not prove clipping behavior for all window types.

### Width remains unresolved

The style's `256` field is **not** a defensible maximum horizontal glyph advance. We have not established the relationship among the native background edge, 7–10-pixel text inset, rendering transforms, glyph advance table, and screenshot scaling. A correct automatic *horizontal* limit must account for context: for this resource, the area-name text starts after a prior command's line break and may carry significant leading indentation. Until the drawing pipeline gives a source-verified limit, the Toolkit **does not auto-populate Max glyph width** and calls it a manual cap.

### Formatting controls partially recovered

Original `8003DF98` dispatches signed `-71..-32`. The following functions reveal native window-field writes, though *visible effects* remain unverified:

| Control | Original helper(s) | Observed field effect |
| --- | --- | --- |
| -57 | `8000C640` | Clear flag `0x10` at window `+0x1C` |
| -56 | `8000C5E4`, `8000C60C` | Write float32 `2.0` to `+0x88`, set flag `0x10` at `+0x1C` |
| -55 | `8000C5A4` | Clear flag `0x08` at `+0x1C` |
| -54 | `8000C570`, `8000C568` | Set flag `0x08`; latter helper does not mutate window |
| -53/-52 | `8000C430` | Set signed halfword `+0x70 = 9` |
| -51 | `8000C488` | Clear flag `0x02` at `+0x1C` |
| -50 | `8000C454` | Set flag `0x02` at `+0x1C` |

The editor continues to treat these controls conservatively for automatic text wrapping; mapping a field write is not proof that the visual result is safe to reorder.

### Script reference coverage

The existing extractor indexed 5,186 unique static text candidates across 42 resources. The conservative source-backed context analysis identifies an unbranched style context for **963 of those 5,186 records**. That count is *not* a list of proven reachable dialogue: the `0x8010` reference scan can find non-executed command-shaped data. The remainder may use branches, callbacks, dynamic setup, or sequences outside the current bounded parser. Indirect pointer and full reachability proof is still outstanding.

### Follow-up source targets

- Trace glyph display-list output and text-to-window coordinate scaling from `8000D060`, `8000D180`, `8000B8F0` and `8000C904`; derive the real per-style **horizontal** text bounds.
- Test line-capacity and clipping for dialogue styles 0/2/4/5/7 with controlled screenshots or instruction-level renderer traces, including window animation/scale state.
- Trace callers and readers of window flags `+0x1C` and formatting parameter `+0x70/+0x88`; label visual semantics only when confirmed.
- Extend VM script graph handling beyond straight-line `0x8004`/`0x8010`, including branch, choice and callback edges, and add instruction-write traces for generated RAM text.

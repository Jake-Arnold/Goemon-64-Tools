# Japan-0 Plasma sample: verified glyphs and read-only romaji search — 2026-11-19

## Original-ROM evidence and screenshot

The user supplied a Japanese gameplay screenshot showing the stylized phrase
`プラズマぁ！！` in a green text window. In the original Japan-0 decompressed
32 MiB ROM (SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`),
resource **112**, text offset **+0x0C**, contains the ordered signed 16-bit tokens:

`13,13,-56,-50,166,13,132,13,151,13,124,13,89,13,212,13,212,-51,-57,-60`

Token `13` is a space between dramatic display characters; `-56/-50/-51/-57`
are original formatting controls; `-60` ends the line. The *seven* non-space
glyphs, in sequence, match the screenshot exactly:

| Token | Screenshot glyph | Confidence |
| --- | --- | --- |
| 166 | プ | In-game screenshot aligned with original resource 112 |
| 132 | ラ | Same |
| 151 | ズ | Same |
| 124 | マ | Same |
| 89 | ぁ | Same |
| 212 | ！ | Same; appears twice |

The record's original negative controls are **not** reinterpreted as text. An
additional source record 112+0x1E4 repeats the same `166,132,151,124,89`
sequence with different display styling. Resource 112 contains 201 candidate
text records; it is a **static resource grouping**, not a proved runtime
conversation graph. The extracted `166,132,151,124` sequence occurs in 62
candidate records across resources 96 and 112. It identifies a repeated
Plasma phrase/name. No conclusion about unrelated glyph IDs is inferred.

## Search implementation

- Add exact screenshot-backed glyphs to `JP_CONFIRMED_GLYPHS`, allowing direct
  Unicode editing of those specific characters without enabling the remaining
  hypothetical kana series.
- `romanized_japan_search(tokens)` applies basic 46-character gojuon romanization
  plus *only screenshot-proven* extra voiced/small kana (`pu`, `zu`, `do`, `a`).
  `japanese_query_matches` searches romanized keys while keeping unmapped
  glyphs as hard barriers rather than fabricating readings.
- When the **Show inferred kana** checkbox is on, the dialogue search now accepts
  Japanese Unicode or case-insensitive romanized substrings such as `pu`,
  `pura`, `purazuma`, `purazumaa`. It also supports exact `resource:112` and
  narrowed `resource:112 pu` queries. A **Show selected resource** button
  displays all statically indexed records from that resource.
- The compact-space search variant ignores token `13` so the user can find a
  theatrically spaced `プ ラ ズ マ` by searching `purazuma`. A normal-space
  variant is retained. Unknown glyphs and `-60` remain search barriers.
- Results are read-only query matching. The unverified 46+46 kana hypothesis
  remains separate from the confirmed Unicode ROM encoder.

## Test observations

With the pinned original ROM: 103 indexed candidate records match `pu`, 65
match `purazuma`, and 3 match `purazumaa`. These are search hits, not confirmed
executed dialogue lines. The exact 112+0x0C record round-trips through the
Japanese encoder unchanged, including formatting and spacing controls.

**Limits:** General dakuten/handakuten mappings, small kana beyond `ぁ`, kanji
and Latin glyphs remain unresolved. The romaji implementation is deliberately
basic; it is a search aid, not a complete Japanese IME or translator. A runtime
edit of these new glyphs still requires an in-emulator verification. No ROM
assets, font files or screenshots are added to the Git repository.

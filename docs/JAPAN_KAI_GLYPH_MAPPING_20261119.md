# Japan-0 first screenshot-verified Unicode character mappings — 2026-11-19

Source: user-supplied Project64 screenshot of the original Japanese Kai area-name banner. The two displayed lines have been matched against the original 32 MiB decompressed Japanese ROM, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`, resource ID **82**.

## Matched records

- Resource **82 +0x04** at decompressed image `0x742344`: `13, 13, 292, -33, 99, 95, -32, 293, -60`. Visual header `【カイ】` with orange `カイ` and white brackets. The first two 13 values are leading spaces. The negative tokens are **control codes**, not font glyphs: `-33` changes presentation style/colour and `-32` resets it. `-60` is the native newline.
- Resource **82 +0x18** at image `0x742358`: `13, 13, 13, 13, 13, 19, 15, 78, 16`. Visual subtitle `かいどう` following five indentation spaces.

## Glyphs supported by this observation

| Signed 16-bit token | Unicode glyph |
| --- | --- |
| 292 | 【 |
| 293 | 】 |
| 99 | カ |
| 95 | イ |
| 19 | か |
| 15 | い |
| 78 | ど |
| 16 | う |

Existing Japanese space/padding token `13` remains mapped to ASCII space in the tool. All other positive IDs continue to use `<token:N>`; no general Shift-JIS conversion or global Unicode order is inferred from these two records. Encoded replacement text always preserves unknown token IDs and the original ordered controls. This is **partial** Unicode coverage, not a completed Japanese glyph atlas.

Note: this screenshot matches the unmodified Japanese game. It does not yet verify modified Japanese Unicode replacements displayed in an emulator. The encoder and repacker tests verify that an unchanged record round-trips exactly to the original signed-halfword tokens and that a known-glyph edit preserves controls.

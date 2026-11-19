# Original Japan-0: all 160 source-order kana positions mapped

Date: 19 November 2026. This research used only the user's original,
SHA-1-verified 32 MiB Japanese ROM `6f8745fecc3a5e7d4918c7a73353eb0726116ded`,
and prior original-game screenshots. No original ROM bytes or asset images
are included in the repository.

## Evidence beyond previous 76 individually proven positions

The original source has 5,039 statically indexed Japanese text records.
An independent full-resource-table scan used each resource's direct 0x8010
text command, parsed signed halfwords until sentinel -1, and counted only
nonnegative kana glyph IDs 14..173. Results:

- **44,077 kana-token occurrences** within the proposed 160 positions.
- **157 / 160 different kana IDs actually occur** in those indexed records.
- **No occurrences** of 138 (predicted ヲ), 155 (predicted ヂ), or
  171 (predicted ゥ). The table assigns them by source ordering only.
- **76 of the 160** are separately anchored to exact original-game
  screenshots and ROM records. All anchors agree with the proposed order.
- A uniform **+80** separates the equivalent hiragana and katakana
  gojūon, small, voiced and small-vowel subgroups.

Examples of complete, coherent Japanese substrings decoded by this same
structure at unrelated original resource offsets:

| Resource offset | Source-order decoded substring |
|---|---|
| 99 +0x5F0 | エイリアンのタマシイよびだしちゃって |
| 112 +0x1720 | キュウリつくりのめいじんにあうには |
| 106 +0x4 | めいぶつスタミナだんごはどうだい |
| 96 +0x14EC | キセルしょくにんのモクベエがもってた |

The coherent texts strongly corroborate the proposed block order across
many scene resources. This is linguistic and structural corroboration,
**not** individual raster verification for every kana.

## Structurally decoded original glyph ranges

| Tokens | Hiragana/Katakana role |
|---|---|
| 14–59 | Hiragana base gojūon (46) |
| 60–63 | Hiragana small っゃゅょ (4) |
| 64–88 | Hiragana voiced/semi-voiced (25) |
| 89–93 | Hiragana small vowels ぁぃぅぇぉ (5) |
| 94–139 | Katakana base gojūon (46) |
| 140–143 | Katakana small ッャュョ (4) |
| 144–168 | Katakana voiced/semi-voiced (25) |
| 169–173 | Katakana small vowels ァィゥェォ (5) |

The canonical table is `practice/dialogue_kana_table.py`.
The original screenshot-confirmed dictionary is deliberately retained
as a separate provenance set. All 160 source-order kana are now usable
for Unicode editing; the 84 not individually verified by screenshot
retain their inference label. The explicit negative control token
sequence, max-length validation and no-op original-ROM roundtrips
are unchanged. Unknown kanji, lowercase letters and most digits
still require explicit `<token:N>` until further mapping.

## Verification and limits

`tests/test_dialogue_full_kana.py` checks all 160 glyph IDs, complete
reversible decoding, zero contradictions to 76 screenshot anchors, and
preservation of all VM controls. With `GOEMON_JP_DECOMPRESSED_ROM`
set to the verified original, it additionally verifies corpus counts
and all 5,039 records' exact encode/decode token equivalence.

The three unused glyphs and individual raster shapes of the other
pattern-derived positions remain untested on-screen. The game
also contains numerous kanji and punctuation glyphs outside 14..173;
therefore this is **complete 160-kana block decoding**, not a claim
that all Japanese characters in the entire game are solved. Japanese
font widths and line geometry remain unverified.

# Original Japan ROM: Hagure Town / Oedo — 13 screenshot alignments

19 November 2026. The user supplied 13 screenshots showing the area banner, the Chappy/dog conversation, UFO reaction and laughter, a fortune-teller advertisement, and a conversation about Mount Fuji. We matched the visible Japanese character order to signed 16-bit glyph tokens in the **verified original Japan-0 decompressed ROM**, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. The screenshots and ROM assets are NOT committed. The following entries are transcriptions for reproducible mapping, not inferred runtime addresses.

**Result: all 13 screenshots, 29 independent original text records, 63 previously unknown token→Unicode glyph IDs.** The previously verified 45 IDs plus these 63 yield **108 screenshot-verified glyph IDs**. Tokens whose meanings were only inferred stay in the existing *read-only* kana preview. New screenshot-backed glyphs may now be typed in the Japanese editor, subject to original negative control preservation and current ROM rebuild bounds.

The 13 screens are not a single runtime dialogue chain: they include **two original resources, 93 (area banner) and 96 (Oedo town scripted NPCs)**. Some screenshots display typewriter text mid-animation; our comparisons use the matching complete original records. Resource 96 records at offsets `0x2D98`–`0x2E00` also help show that this is a character-dialogue block rather than an automatic layout of unrelated fragments.

## Source screenshot to exact original offsets

| Screenshot | Resource and offset(s) | Text visible or completed source line(s) |
|---:|---|---|
| 1 | `93 +0xC84, 93 +0xC94` | 【大江戸 / ・はぐれ町】 |
| 2 | `96 +0x2D98` | 「UFOだって？ |
| 3 | `96 +0x2DAC, 96 +0x2DCC` | ハハハハハハハハハハハハハ / ハハハハハハハハハハ・・・ |
| 4 | `96 +0x2DEC, 96 +0x2E00` | そんなことより、 / うちのチャッピーは、いいイヌだろう！ |
| 5 | `96 +0x2BFC, 96 +0x2C20, 96 +0x2C44` | チャッピー「あ〜だる〜ぅ・・・ / はやく、メシくって / ねたいワン」 |
| 6 | `96 +0x2C60, 96 +0x2C78` | チャッピー「なんか、 / しんどいんだワン」 |
| 7 | `96 +0x4E10, 96 +0x4E28` | にしへ行けば、 / ふじ山あり！ |
| 8 | `96 +0x4DDC, 96 +0x4DF4` | ピタリと、あたる！ / うらない屋スグソコ！ |
| 9 | `96 +0x1A78, 96 +0x1A98, 96 +0x1AA8` | 「こまった・・・こまった！ / あ〜〜あ / こまった、こまった・・・・・・ |
| 10 | `96 +0x1ACC, 96 +0x1AE8, 96 +0x1B04` | そんな、こまった時には / うらない屋に行くのが / いちばんじゃよ！ |
| 11 | `96 +0x1B18, 96 +0x1B34` | プラズマパワーで、 / なやみもかいけつじゃて！！ |
| 12 | `96 +0x278C, 96 +0x27A8` | 「わしゃ、ふじ山に / のぼりに来たんじゃ・・・ |
| 13 | `96 +0x27C8, 96 +0x27E0, 96 +0x280C` | たしか、やくにんから / うらない屋のカドをまがったとこから / 行けるってのは聞いたんじゃがのぉ |

## Newly confirmed token mappings

The table below lists **only** additions verified against these 13 images, not previously verified glyphs and not the other speculative kana positions. Each mapping is backed by at least one of the 29 transcript-aligned records. The complete editable table is `JP_CONFIRMED_GLYPHS` in `practice/dialogue_japan.py`.

| Token ID | Glyph | Token ID | Glyph | Token ID | Glyph |
|---:|:---:|---:|:---:|---:|:---:|
| `14` | あ | `21` | く | `22` | け |
| `23` | こ | `25` | し | `28` | そ |
| `29` | た | `30` | ち | `31` | つ |
| `32` | て | `33` | と | `34` | な |
| `35` | に | `37` | ね | `38` | の |
| `39` | は | `41` | ふ | `42` | へ |
| `44` | ま | `45` | み | `48` | も |
| `49` | や | `51` | よ | `52` | ら |
| `53` | り | `54` | る | `55` | れ |
| `56` | ろ | `57` | わ | `58` | を |
| `59` | ん | `66` | ぐ | `83` | ぼ |
| `91` | ぅ | `93` | ぉ | `103` | コ |
| `105` | シ | `106` | ス | `108` | ソ |
| `109` | タ | `110` | チ | `116` | ヌ |
| `119` | ハ | `127` | メ | `133` | リ |
| `137` | ワ | `139` | ン | `140` | ッ |
| `141` | ャ | `146` | グ | `158` | ド |
| `164` | パ | `165` | ピ | `175` | ー |
| `191` | F | `200` | O | `206` | U |
| `224` | ？ | `276` | 町 | `302` | 行 |
| `318` | 時 | `324` | 来 | `337` | 聞 |

## Important interpretation

- The **basic kana and +80 pair ordering** remain consistent with all new screenshot checks. The confirmed IDs are now much denser, but they do **not** individually prove every position in the 160-slot hypothesis. Unverified characters stay read-only.
- **New strictly read-only research preview:** `practice/dialogue_kana.py` now tentatively displays uppercase glyph IDs **186–211** as `A–Z` and **176–185** as `０–９`. The screenshot-proven `U=206`, `F=191`, `O=200`, `０=176` and `１=177` fit this ordering; the original ROM also contains `204,205,186,203,205` in a `START` button prompt. These additional proposed letters and digits are **not editable** until confirmed. The old 160-slot kana hypothesis is unchanged (76 screenshot-verified, 84 unverified).
- **Latin glyphs exist in the Japanese game's font:** the `UFOだって？` screenshot aligns token IDs `206='U'`, `191='F'`, and `200='O'`. Only these three Latin letters are now screenshot-verified. Do **not** extrapolate the alphabet from three unrelated IDs without font analysis. The punctuation glyph `224='？'` is also proven by the same record.
- The repeated laugh contains 13 `ハ` in one record and **10** `ハ` in the next, followed by three middle dots. Similar repeated strings can be misleading; the exact number of occurrences and the adjacent record offsets were verified against the ROM.
- Source 93 +0xC84/+0xC94 renders an area banner in two records; `276='町'` is reused in other Town references. Long scene transitions should not be interpreted as single-record dialogue.
- The screenshot showing the merchant's recommendation uses `318='時'`, `302='行'`; the Mount Fuji quest line also gives `324='来'` and `337='聞'`. These are useful *kanji* examples outside the contiguous kana chart.
- This is **static text-reference indexing**; it does not prove every dialogue variant or the complete VM branch ordering. No modified Japanese ROM was verified visually in an emulator.

## Repeatable test evidence

Run the original-ROM and UI suite under portable Python/LZKN64/Xvfb. `tests/test_dialogue_oedo_screens.py` requires the verified Japan ROM path and checks all 29 lines against the ROM, all 63 new mappings, exact byte-for-byte token encode/decode, preservation of negative controls, and rejection of remaining unverified Latin/kana. The original USA editor, variable-length ROM relocation, compression behavior and overall source compatibility must remain unchanged. No external dependency changes are needed for this mapping.

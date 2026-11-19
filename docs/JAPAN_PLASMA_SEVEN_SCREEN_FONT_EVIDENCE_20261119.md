# Japanese Plasma dialogue — seven screenshot alignment and kana-table evidence

19 November 2026. Source: user's seven consecutive *Ganbare Goemon: Neo Momoyama Bakufu no Odori* gameplay screenshots following the earlier large “プラズマぁ！！” screenshot. Record offsets and glyph IDs are verified against the original 32 MiB Japan-0 decompressed ROM, SHA-1 `6f8745fecc3a5e7d4918c7a73353eb0726116ded`. Japanese text shown below was transcribed from the user's screenshots, and aligned with the original ROM's corresponding signed 16-bit records. Do not use the screenshots or original ROM bytes as committed assets.

## Whole dialogue segment — resource 112

| Screenshot | Original record offsets within resource 112 | Displayed text represented by these records |
|---|---|---|
| 1 — fortune teller introduction | `+0x60`, `+0x74`, `+0x8C` | `プラズマおやぢ` / `「どぴょぴょ〜ん！` / `プラズマうらないへ、ようこそじゃ」` |
| 2 — price/choice | `+0xB8`, `+0xDC`; choices `+0xFC`, `+0x118` | `「おぬしのなやみを、１０両で` / `かいけつしてプラズマ〜！」`; `お、おねがいします` / `い・・・いいや` |
| 3 — fortune begins | `+0x134`, `+0x144` | `「うむ、` / `では、うらなってしんぜよう！！」` |
| 4 — repeated catchphrase | `+0x16C`, `+0x194`, `+0x1BC` | Three lines of repeated `ぷ`, ending `っ・・・」` |
| 5 — callout | `+0x1E4` | `プラズマぁ〜！` (with per-character spaces and inline style controls) |
| 6 — castle | `+0x290`, `+0x2B8` | `「大江戸城（おおえどじょう）に` / `入りたければ・・・` |
| 7 — directions | `+0x2D0`, `+0x300`, `+0x328` | `このうらない屋からむかってひだりの` / `出入口から、【カイのかいどう】に出て` / `「ふじ山」へ、むかうプラズマ！` |

All 18 quoted record offsets exist within resource 112. Exact source token-to-Japanese-text comparisons are executable regressions in `tests/test_dialogue_kana.py`, not just prose claims. The screenshots demonstrate one possible runtime branch; they do **not** prove all candidates in resource 112 execute in that order, nor do they prove complete reference reachability.

## New directly screen-matched glyph IDs

These are added to `JP_CONFIRMED_GLYPHS`; they can be used for Unicode editing, subject to the existing control-token preservation and bounded JP ROM relocation rules. They **do not** assign semantics to the negative VM formatting tokens.

| Token ID | Character | Evidence |
|---:|---|---|
| 75 | ぢ | `プラズマおやぢ` |
| 295 | 「 | Dialogue opening quote |
| 85 | ぴ | `どぴょぴょ` |
| 63 | ょ | `どぴょぴょ`; also `じょう` |
| 303 | 〜 | `〜ん` and `プラズマぁ〜！` |
| 296 | 、 | Punctuation throughout dialogue |
| 70 | じ | `じゃ`, `じょう`, `ふじ山` |
| 61 | ゃ | `じゃ` |
| 297 | 」 | Dialogue closing quote |
| 177 | １ | `１０両` |
| 176 | ０ | `１０両` |
| 236 | 両 | `１０両` |
| 77 | で | `１０両で`; `では` |
| 64 | が | `おねがいします` |
| 232 | ・ | Repeated dialogue hesitation dots |
| 60 | っ | `うらなって`, `むかって`, repeated-pu ending |
| 72 | ぜ | `しんぜよう` |
| 86 | ぷ | Forty-plus consecutive `ぷ` glyphs |
| 291 | 大 | `大江戸城` |
| 273 | 江 | `大江戸城` |
| 274 | 戸 | `大江戸城` |
| 275 | 城 | `大江戸城` |
| 258 | （ | Parenthesized reading |
| 259 | ） | Parenthesized reading |
| 304 | 入 | `入りたければ` / `出入口` |
| 79 | ば | `たければ` |
| 341 | 屋 | `うらない屋` |
| 74 | だ | `ひだり` |
| 334 | 出 | `出入口`, `に出て` |
| 305 | 口 | `出入口` |
| 278 | 山 | `ふじ山` |

Earlier screenshot-confirmed Kai and Plasma glyphs remain unchanged. The combined verified set contains 45 unique glyph IDs.

## Systematic kana font hypothesis

The screenshot pair `15=い / 95=イ` and `19=か / 99=カ` supports a `+80` hiragana→katakana ID offset. The new screenshots provide further independent anchors: `64=が`, `70=じ`, `74=だ`, `75=ぢ`, `77=で`, `78=ど`, `79=ば`, `85=ぴ`, `86=ぷ`, `151=ズ`, `166=プ`, plus small `っ/ゃ/ょ/ぁ`. These fit the following contiguous sequence:

| Range | Interpreted (hypothesis, except proven IDs) |
|---|---|
| 14–59 | Basic 46 hiragana in gojūon order |
| 60–63 | Small っ ゃ ゅ ょ |
| 64–88 | Voiced/semi-voiced hiragana (が–ぽ) |
| 89–93 | Small vowels ぁ–ぉ |
| 94–139 | Basic 46 katakana in gojūon order |
| 140–143 | Small ッ ャ ュ ョ |
| 144–168 | Voiced/semi-voiced katakana (ガ–ポ) |
| 169–173 | Small vowels ァ–ォ |

This yields 160 *predicted* kana positions, including the screenshot-proven IDs. The guesses stay confined to `JP_KANA_HYPOTHESIS` and read-only/romaji search; only `JP_CONFIRMED_GLYPHS` is writable via direct Unicode. Other original Japanese glyph IDs, including unverified kanji and special formatting glyphs, remain explicit `<token:N>` values. A single confirmed mapping is not proof that every position in the range matches.

## Search/list behavior

The prior GUI drew only the first 800 rows despite indexing all 5,039 JP and 5,186 USA candidates. `DialogueRegionMixin` now draws the entire matched set for both regions (no 800 cap). With the experimental kana toggle, resource `112` and romaji searches still use the inferred/verified mapping. Matching 5,039 candidate records does not guarantee all are runtime-reachable.

## Test and publication rules

Run the source-pinned dialogue suite under Xvfb and the supplied portable Python/LZKN64 runtime. Check the exact original ROM hashes, source-record offsets, token round-trips and a GUI list larger than 800. Do not commit ROMs, extracted art or screenshot files. Do not describe Japanese layout or indirect script references as fully recovered.

# Japanese original-renderer glyph probe: pages 2–4 of 4

Date: 20 November 2026. Companion: `docs/JAPAN_GLYPH_PROBE_PAGE1_20261120.md`.
Original Japan-0 decompressed ROM SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
Evidence: three user-supplied Project64 screenshots, in page order, displaying the generated `jp-glyph-probe-02-of-04.z64`, `03-of-04`, `04-of-04` at Kai Highway (original text record **resource 82 +0x18**). Images and ROM bytes remain outside Git.

## Method and original-manifest reconstruction

The probe writer (Toolkit v0.11.74) sorted **111** positive glyph token IDs absent from its pre-probe **215-glyph** editable map; it excluded suspect non-glyph ID `11` and split them into seven columns by four rows. Because the original generated JSON is user-local, the row order was independently reconstructed from the pinned 32 MiB original decompressed ROM using the committed source's aligned in-resource `0x8010` dialogue scanner. This produced **5,039** records, matching the previous index, and **84** unknown IDs after the already accepted 28 from page one. Re-inserting those 28 and sorting reproduces **exactly** the documented page-one token sequence, followed by the pages below. Each screenshot was aligned row-major against these token positions.

The original Kai area-name artwork is short. Rows 2–4 appear outside the painted banner and partially overlap world objects; visual interpretation is corroborated below against *unchanged original* game dialogue contexts. Do not infer textbox geometry from this probe.

## Page 2 — 28 IDs

| Row | Token IDs | Observed text |
| --- | --- | --- |
| 1 | 308 309 310 311 312 313 314 | 人 銀 力 金 千 花 星 |
| 2 | 315 316 317 319 320 321 322 | 火 丸 目 間 茶 店 方 |
| 3 | 323 325 326 327 328 329 330 | 思 外 子 男 ♪ 国 地 |
| 4 | 331 332 333 335 336 338 339 | 九 州 女 社 員 語 卍 |

In particular, `317=目` is **not** the existing `230=日`. The page-one and page-two forms are visually different and have separate token values.

## Page 3 — 28 IDs

| Row | Token IDs | Observed text |
| --- | --- | --- |
| 1 | 340 342 343 344 345 346 347 | 長 話 家 四 文 字 川 |
| 2 | 348 349 350 351 352 353 354 | 小 池 竹 上 流 回 落 |
| 3 | 355 356 357 358 359 360 361 | 石 ○ 氷 犬 神 名 警 |
| 4 | 362 363 364 365 366 367 368 | 告 発 生 島 木 客 桜 |

`356` is entered as the hollow-circle Unicode `○`, not ideographic zero `〇`, following its repeated placeholder-circle usage in original dialogue (`356,356,356` in resource 112). `344=四` is supported by the original consecutive `344,329` = 四国, and `368=桜` by `368,365` = 桜島.

## Page 4 — 27 IDs

| Row | Token IDs | Observed text |
| --- | --- | --- |
| 1 | 369 370 371 372 373 374 375 | 先 向 調 艦 愛 夢 仁 |
| 2 | 376 377 378 379 380 381 382 | 王 良 早 o i n g |
| 3 | 383 384 385 386 387 388 389 | w a k e h c 野 |
| 4 | 390 391 392 393 394 395 | 表 示 破 損 現 犯 |

`372=艦` occurs after original `291=大,289=戦`, spelling 大戦艦 (resource 114).
`375=仁` immediately precedes `376=王` (仁王) in resource 114.
`382=g` is *not* `号`: resource 119 contains `192,379,380,381,382,13,199,379,383`, spelling **Going Now** with known `192=G`, `199=N`. Lowercase `o i n g w a k e h c` are independent native glyphs, not new uppercase Latin tokens.
The partly occluded final `395=犯` is confirmed by original resource 81 containing `394,302,395` = 現行犯.

## Results and boundaries

- **Page 2–4 newly observed:** 83 distinct IDs (28 + 28 + 27).
- **All four pages newly observed:** 111 distinct IDs.
- **Screenshot-confirmed glyph IDs:** 159 → **242**.
- **Directly editable glyph IDs:** 243 → **326**. This includes the existing **84** structurally inferred but not screenshot-proven kana.
- **Unmapped IDs in the original 5,039-record static index:** 84 → **1**; only excluded **ID 11** remains, with one indexed occurrence. It is not automatically labelled a printable glyph or VM control.
- `183=７` is still an **unobserved** ordered-font inference, not a screenshot-proven glyph. The original renderer's backing texture layout remains unknown. This is a full mapping of **this four-page indexed probe**, not a full original ROM font extraction.
- Production code changes only Unicode token decoding/encoding and UI counts. Negative control tokens, original text bytes, region-specific ROM writer and repacking guards are unchanged.
- Automated coverage: `tests/test_dialogue_glyph_probe_pages234.py`, the existing page-one test, and updated Oedo/kana/UI/probe tests. Run current CI; no unexecuted green claim is made by this document.

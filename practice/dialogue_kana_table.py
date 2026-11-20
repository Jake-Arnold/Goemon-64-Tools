"""Pattern-derived Japanese ROM kana font table, with evidence boundaries.

Original Japan-0 dialogue uses 160 consecutive kana IDs, 14..173.
76 positions have independent screenshot proof; original static dialogue
uses 157 positions (44,077 occurrences) across 5,039 records. Unobserved:
138=ヲ, 155=ヂ, 171=ゥ. These three follow the same block sequence
but are not individually raster-verified.
"""
from __future__ import annotations

HIRAGANA = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
KATAKANA = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
HIRAGANA_START = 14
KATAKANA_START = 94
KANA_OFFSET = 80
HIRA_SMALL = 'っゃゅょ'
KATA_SMALL = 'ッャュョ'
HIRA_VOICED = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'
KATA_VOICED = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
HIRA_SMALL_VOWELS = 'ぁぃぅぇぉ'
KATA_SMALL_VOWELS = 'ァィゥェォ'
KANA_GROUPS = (
    (14, HIRAGANA), (60, HIRA_SMALL), (64, HIRA_VOICED),
    (89, HIRA_SMALL_VOWELS), (94, KATAKANA), (140, KATA_SMALL),
    (144, KATA_VOICED), (169, KATA_SMALL_VOWELS),
)
assert len(HIRAGANA) == len(KATAKANA) == 46
assert len(HIRA_VOICED) == len(KATA_VOICED) == 25
assert KATAKANA_START - HIRAGANA_START == KANA_OFFSET
JP_KANA_HYPOTHESIS = {
    start + index: glyph
    for start, group in KANA_GROUPS for index, glyph in enumerate(group)
}
JP_UNOBSERVED_KANA_IDS = frozenset((138, 155, 171))
assert len(JP_KANA_HYPOTHESIS) == 160
assert sorted(JP_KANA_HYPOTHESIS) == list(range(14, 174))
assert len(set(JP_KANA_HYPOTHESIS.values())) == 160

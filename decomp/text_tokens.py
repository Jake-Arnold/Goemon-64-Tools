"""Original Goemon USA / Japan-0 signed-halfword text tokens, read only.

This file carries the canonical mappings from toolkit main revision
1a58d3c159c47d0e02b4fbd1fb12e0748871cd73:
practice/dialogue_rom.py, practice/dialogue_japan.py, and
practice/dialogue_kana_table.py. Review upstream changes before resyncing.

Mappings are not original game code or dialogue. Negative IDs other than the
documented common controls remain opaque. Japanese screenshot-backed glyphs
are distinct from inferred source-order kana. Token 11 is a visible alias
for ！, but decoding it as Unicode would lose its original numeric identity.
"""
from __future__ import annotations

import re
import struct

GLYPHS = {n: chr(n + 32) for n in (
    0, 1, 7, 12, 13, 14, 15, 26, 27, 29, 31,
    *range(16, 26), *range(33, 59), *range(65, 91),
)}
GLYPHS.update({59: '[', 60: ',', 61: ']', 62: '"', 64: '.'})
CONTROLS = {
    -71: '<close-window>', -70: '<open-window>', -63: '<clear-glyphs>',
    -62: '<state-4>', -61: '<state-3>', -60: '\n',
}
GLYPH_TO_TOKEN = {value: key for key, value in GLYPHS.items()}
CONTROL_TO_TOKEN = {value: key for key, value in CONTROLS.items() if value != '\n'}
TAG_PATTERN = re.compile(r'<token:([+-]?\d+)>|<(close-window|open-window|clear-glyphs|state-4|state-3)>')

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
assert sorted(JP_KANA_HYPOTHESIS) == list(range(14, 174))assert len(set(JP_KANA_HYPOTHESIS.values())) == 160

JP_CONFIRMED_GLYPHS = {
    292: '【', 293: '】', 99: 'カ', 95: 'イ',
    19: 'か', 15: 'い', 78: 'ど', 16: 'う',
    166: 'プ', 132: 'ラ', 151: 'ズ', 124: 'マ', 89: 'ぁ', 212: '！',
    # Screen-verified Plasma fortune-teller sequence, resource 112.
    # Screenshot line matching is recorded in docs/JAPAN_PLASMA_SCREENSHOT_ALIGNMENT_20261119.md.
    # These are character tokens, NOT script controls: preserve all negative IDs.
    75: 'ぢ', 295: '「', 85: 'ぴ', 63: 'ょ', 303: '〜',
    296: '、', 70: 'じ', 61: 'ゃ', 297: '」',
    177: '１', 176: '０', 236: '両', 77: 'で',
    64: 'が', 232: '・', 60: 'っ', 72: 'ぜ', 86: 'ぷ',
    291: '大', 273: '江', 274: '戸', 275: '城',
    258: '（', 259: '）', 304: '入', 79: 'ば',
    341: '屋', 74: 'だ', 334: '出', 305: '口', 278: '山',
    # Thirteen additional user gameplay screenshots: Oedo/Hagure title and
    # Oedo NPC speech, pinned Japan-0 resources 93 and 96.
    # Each ID was aligned by character position across 29 original 16-bit
    # records (including the entire text segment, not just a fuzzy substring).
    # Provenance: docs/JAPAN_OEDO_THIRTEEN_SCREEN_ALIGNMENT_20261119.md
    14: 'あ', 21: 'く', 22: 'け', 23: 'こ', 25: 'し', 28: 'そ',
    29: 'た', 30: 'ち', 31: 'つ', 32: 'て', 33: 'と', 34: 'な',
    35: 'に', 37: 'ね', 38: 'の', 39: 'は', 41: 'ふ', 42: 'へ',
    44: 'ま', 45: 'み', 48: 'も', 49: 'や', 51: 'よ', 52: 'ら',
    53: 'り', 54: 'る', 55: 'れ', 56: 'ろ', 57: 'わ', 58: 'を',
    59: 'ん', 66: 'ぐ', 83: 'ぼ', 91: 'ぅ', 93: 'ぉ', 103: 'コ',
    105: 'シ', 106: 'ス', 108: 'ソ', 109: 'タ', 110: 'チ', 116: 'ヌ',
    119: 'ハ', 127: 'メ', 133: 'リ', 137: 'ワ', 139: 'ン', 140: 'ッ',
    141: 'ャ', 146: 'グ', 158: 'ド', 164: 'パ', 165: 'ピ', 175: 'ー',
    191: 'F', 200: 'O', 206: 'U', 224: '？', 276: '町', 302: '行',
    318: '時', 324: '来', 337: '聞',
    # Two user Project64 screenshots with the exact sequential 186..211 payload:
    # the first proves A..U, the second shows ABCDEFG / HIJKLMN /
    # OPQRSTU / VWXYZ in four manually split lines (V..Z now legible).
    # All A..Z are verified on-screen in a modified original-Japan ROM.
    # In the Kai banner, extra lines draw below the fixed-height window.
    **{186 + index: chr(ord('A') + index) for index in range(26)},
    # Project64 page-1 native glyph probe, 20 Nov 2026: original Japan
    # resource 82 +0x18 test ROM, 7 columns x 4 rows in manifest order.
    # White punctuation at ID 226 is a small Japanese sentence stop.
    # ID 300/301 display square opening/closing bracket strokes.
    # Probe row 1:
    178: '２', 179: '３', 180: '４', 181: '５', 182: '６', 184: '８', 185: '９',
    # Probe row 2:
    226: '。', 229: '旅', 230: '日', 239: '数', 242: '中', 245: '見', 256: '本',
    # Probe row 3:
    257: '体', 265: '場', 277: '村', 284: '北', 286: '東', 287: '寺', 289: '戦',
    # Probe row 4:
    294: '前', 298: '下', 299: '止', 300: '［', 301: '］', 306: '水', 307: '海',
    # Project64 native glyph probe pages 2–4 (20 November 2026).
    # Exact source-token order reconstructed from the original Japan-0
    # 5,039-record index and the 111-ID v0.11.74 probe manifest.
    # Four-line Kai banner screenshots; see evidence report for contexts.
    # Probe page 2:
    308: '人', 309: '銀', 310: '力', 311: '金', 312: '千', 313: '花', 314: '星',
    315: '火', 316: '丸', 317: '目', 319: '間', 320: '茶', 321: '店', 322: '方',
    323: '思', 325: '外', 326: '子', 327: '男', 328: '♪', 329: '国', 330: '地',
    331: '九', 332: '州', 333: '女', 335: '社', 336: '員', 338: '語', 339: '卍',
    # Probe page 3:
    340: '長', 342: '話', 343: '家', 344: '四', 345: '文', 346: '字', 347: '川',
    348: '小', 349: '池', 350: '竹', 351: '上', 352: '流', 353: '回', 354: '落',
    355: '石', 356: '○', 357: '氷', 358: '犬', 359: '神', 360: '名', 361: '警',
    362: '告', 363: '発', 364: '生', 365: '島', 366: '木', 367: '客', 368: '桜',
    # Probe page 4:
    369: '先', 370: '向', 371: '調', 372: '艦', 373: '愛', 374: '夢', 375: '仁',
    376: '王', 377: '良', 378: '早', 379: 'o', 380: 'i', 381: 'n', 382: 'g',
    383: 'w', 384: 'a', 385: 'k', 386: 'e', 387: 'h', 388: 'c', 389: '野',
    390: '表', 391: '示', 392: '破', 393: '損', 394: '現', 395: '犯',
}
# Two 20 Nov 2026 screenshots (token-11 native ROM and token-212 control)
# show the same visible exclamation mark. An alias is not a new Unicode
# editor character: preserve source token 11 as <token:11> and encode ！ to 212.
JP_NATIVE_RENDERED_ALIASES = {11: '！'}
JP_SCREENSHOT_CONFIRMED_TOKEN_COUNT = len(JP_CONFIRMED_GLYPHS) + len(JP_NATIVE_RENDERED_ALIASES)
# Keep screenshot proof separate from the font-order extrapolation.
for _id, _character in JP_CONFIRMED_GLYPHS.items():
    if _id in JP_KANA_HYPOTHESIS and JP_KANA_HYPOTHESIS[_id] != _character:
        raise AssertionError(f'Kana order conflicts with screenshot token {_id}')
JP_EDITABLE_GLYPHS = {**JP_KANA_HYPOTHESIS, **JP_CONFIRMED_GLYPHS}
JP_CONFIRMED_GLYPH_TO_TOKEN = {character: token for token, character in JP_CONFIRMED_GLYPHS.items()}
JP_EDITABLE_GLYPH_TO_TOKEN = {character: token for token, character in JP_EDITABLE_GLYPHS.items()}
assert len(JP_EDITABLE_GLYPHS) == len(JP_EDITABLE_GLYPH_TO_TOKEN) == 326

# USA original DF98 negative-token observations, from toolkit practice/dialogue_layout.py.
# They are not automatically assigned to the Japanese implementation.
CONTROL_NOTES = {
    -71: 'close-window request',
    -70: 'open-window request',
    -63: 'clear glyphs/reset layout',
    -62: 'state 4 (continuation/close handling)',
    -61: 'state 3 (continue prompt)',
    -60: 'explicit line break',
    -57: 'clear window flags +0x1C bit 0x10; visual effect unverified',
    -56: 'set window float +0x88 to 2.0 and flags +0x1C bit 0x10',
    -55: 'clear window flags +0x1C bit 0x08; visual effect unverified',
    -54: 'set window flags +0x1C bit 0x08; secondary helper is no-op',
    -53: 'set window halfword +0x70 to 9; visual effect unverified',
    -52: 'set window halfword +0x70 to 9; visual effect unverified',
    -51: 'clear window flags +0x1C bit 0x02; visual effect unverified',
    -50: 'set window flags +0x1C bit 0x02; visual effect unverified',
    -37: 'presentation selector 0',
    -36: 'presentation selector 2',
    -35: 'presentation selector 4',
    -34: 'presentation selector 6',
    -33: 'presentation selector 8',
    -32: 'presentation selector 0',
}
NOOP_TOKENS = set(range(-69, -63)) | {-59, -58} | set(range(-49, -37))
OPAQUE_LAYOUT_TOKENS = set(range(-57, -49))

# A decoded record must reconstruct its original signed-halfword sequence.
# For USA, glyphs with several token IDs are emitted as numeric tags. For JP,
# token 11 is kept numeric, although a display-only preview may show ！.
def _region(region: str) -> str:
    if region not in ('usa', 'japan_0'):
        raise ValueError('Expected region usa or japan_0')
    return region


def token_glyphs(region: str) -> dict[int, str]:
    _region(region)
    if region == 'usa':
        return GLYPHS
    return {13: ' ', **JP_EDITABLE_GLYPHS}


def duplicate_glyph_ids(region: str) -> frozenset[int]:
    glyphs = token_glyphs(region)
    counts: dict[str, int] = {}
    for value in glyphs.values():
        counts[value] = counts.get(value, 0) + 1
    return frozenset(i for i, ch in glyphs.items() if counts[ch] > 1)


def decode_tokens(region: str, tokens, *, visual_aliases: bool = False) -> str:
    glyphs = token_glyphs(region)
    duplicate = duplicate_glyph_ids(region)
    parts = []
    for token in tokens:
        if type(token) is not int or not -32768 <= token <= 32767 or token == -1:
            raise ValueError('Expected signed 16-bit text tokens excluding terminator -1')
        if token == -60:
            parts.append('\n')
        elif token in CONTROLS:
            parts.append(CONTROLS[token])
        elif region == 'japan_0' and token in JP_NATIVE_RENDERED_ALIASES:
            parts.append(JP_NATIVE_RENDERED_ALIASES[token] if visual_aliases
                         else f'<token:{token}>')
        elif token in glyphs:
            parts.append(glyphs[token] if visual_aliases or token not in duplicate
                         else f'<token:{token}>')
        else:
            parts.append(f'<token:{token}>')
    return ''.join(parts)


_UNIQUE_REVERSE: dict[str, dict[str, int]] = {}
_TAG = re.compile(r'<token:([+-]?\d+)>|<(close-window|open-window|clear-glyphs|state-4|state-3)>')


def encode_tokens(region: str, text: str) -> tuple[int, ...]:
    glyphs = token_glyphs(region)
    if region not in _UNIQUE_REVERSE:
        duplicates = duplicate_glyph_ids(region)
        _UNIQUE_REVERSE[region] = {ch: i for i, ch in glyphs.items()
                                   if i not in duplicates}
    inverse = _UNIQUE_REVERSE[region]
    result = []
    pos = 0
    while pos < len(text):
        ch = text[pos]
        if ch == '<':
            match = _TAG.match(text, pos)
            if match is None:
                raise ValueError(f'Unrecognised token markup at character {pos}')
            token = (int(match.group(1)) if match.group(1) is not None
                     else CONTROL_TO_TOKEN[f'<{match.group(2)}>'])
            pos = match.end()
        elif ch == '\n':
            token = -60
            pos += 1
        elif ch in inverse:
            token = inverse[ch]
            pos += 1
        else:
            raise ValueError(f'Unmapped or ambiguous {region} glyph {ch!r}; use <token:N>')
        if not -32768 <= token <= 32767 or token == -1:
            raise ValueError(f'Invalid signed token {token}')
        result.append(token)
    return tuple(result)


def token_bytes(tokens) -> bytes:
    values = tuple(tokens)
    if any(type(t) is not int or t == -1 or not -32768 <= t <= 32767
           for t in values):
        raise ValueError('Invalid text payload token')
    return struct.pack(f'>{len(values)}h', *values)


def roundtrip_original(region: str, tokens) -> bool:
    original = tuple(tokens)
    return encode_tokens(region, decode_tokens(region, original)) == original

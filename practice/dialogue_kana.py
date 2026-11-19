"""Unverified Japan-0 kana ordering hypothesis for read-only inspection.

EVIDENCE: Screenshot-verified pairs 15=い/95=イ and 19=か/99=カ,
plus 16=う. Both script pairs are exactly 80 token IDs apart.

CONJECTURE: Six sequential base/small/voiced/small-vowel kana blocks starting at 14 and 94. No other character
in these ranges is treated as verified for ROM writing. This is intentionally
separate from JP_CONFIRMED_GLYPHS and encode_japan_text.
"""
from __future__ import annotations

from practice.dialogue_japan import JP_CONFIRMED_GLYPHS
from practice.dialogue_rom import CONTROLS

HIRAGANA = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
KATAKANA = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
HIRAGANA_START = 14
KATAKANA_START = 94
KANA_OFFSET = KATAKANA_START - HIRAGANA_START

# Screen-verified tokens live in JP_CONFIRMED_GLYPHS. These contiguous
# *proposed* blocks are for reading/searching only; the Japanese ROM encoder
# must NOT accept speculative characters based on this table.
HIRA_SMALL = 'っゃゅょ'
KATA_SMALL = 'ッャュョ'
HIRA_VOICED = 'がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ'
KATA_VOICED = 'ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ'
HIRA_SMALL_VOWELS = 'ぁぃぅぇぉ'
KATA_SMALL_VOWELS = 'ァィゥェォ'
assert len(HIRA_VOICED) == len(KATA_VOICED) == 25

JP_KANA_HYPOTHESIS = {
    **{14+i: c for i,c in enumerate(HIRAGANA)},
    **{60+i: c for i,c in enumerate(HIRA_SMALL)},
    **{64+i: c for i,c in enumerate(HIRA_VOICED)},
    **{89+i: c for i,c in enumerate(HIRA_SMALL_VOWELS)},
    **{94+i: c for i,c in enumerate(KATAKANA)},
    **{140+i: c for i,c in enumerate(KATA_SMALL)},
    **{144+i: c for i,c in enumerate(KATA_VOICED)},
    **{169+i: c for i,c in enumerate(KATA_SMALL_VOWELS)},
}
# Two further contiguous blocks are suggested by the screenshot-proven UFO
# (206=U,191=F,200=O), together with the ROM's literal START button context
# (204,205,186,203,205) and the prior screenshot-proven 176=０,177=１.
# Screenshot #2 now verifies the entire A-Z sequence. Only the remaining
# *digits* ２–９ are still unverified predictions. Kana conjectures are
# unchanged. A-Z in this hypothesis dictionary are overridden by the same
# verified entries in JP_CONFIRMED_GLYPHS.
JP_LATIN_HYPOTHESIS = {186+i: chr(ord('A')+i) for i in range(26)}
JP_DIGIT_HYPOTHESIS = {176+i: chr(ord('０')+i) for i in range(10)}
JP_GLYPH_HYPOTHESIS = {**JP_KANA_HYPOTHESIS, **JP_LATIN_HYPOTHESIS,
                       **JP_DIGIT_HYPOTHESIS}

# Half-width/native typography outside the sequential kana range is intentionally
# not inferred from a single sample.
for _id, _character in JP_CONFIRMED_GLYPHS.items():
    if _id in JP_GLYPH_HYPOTHESIS and JP_GLYPH_HYPOTHESIS[_id] != _character:
        raise AssertionError(f'Kana hypothesis contradicts verified token {_id}')

def decode_japan_kana_preview(tokens: tuple[int, ...]) -> str:
    """Human-readable *hypothesis*, never intended for direct ROM encoding."""
    return ''.join(
        ' ' if value == 13 else
        JP_CONFIRMED_GLYPHS.get(value, JP_GLYPH_HYPOTHESIS.get(
            value, CONTROLS.get(value, f'<token:{value}>')))
        for value in tokens
    )


def inferred_kana_count(tokens: tuple[int, ...]) -> int:
    """Count guessed characters as distinct from screenshot-confirmed ones."""
    return sum(value in JP_KANA_HYPOTHESIS and value not in JP_CONFIRMED_GLYPHS
               for value in tokens)


def inferred_glyph_count(tokens: tuple[int, ...]) -> int:
    """All guessed kana, digits and Latin positions (not source-proven glyphs)."""
    return sum(t in JP_GLYPH_HYPOTHESIS and t not in JP_CONFIRMED_GLYPHS
               for t in tokens)


# Search-only romanization for the proposed gojuon and voiced blocks.
# Mixed-case or user queries never introduce newly inferred Unicode into ROMs.
GOJUON_ROMAJI = (
    'a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to '
    'na ni nu ne no ha hi fu he ho ma mi mu me mo ya yu yo '
    'ra ri ru re ro wa wo n'
).split()
VOICED_ROMAJI = (
    'ga gi gu ge go za ji zu ze zo da di du de do '
    'ba bi bu be bo pa pi pu pe po'
).split()
assert len(GOJUON_ROMAJI)==46 and len(VOICED_ROMAJI)==25
ROMAJI_BY_TOKEN = {
    **{14+i: value for i,value in enumerate(GOJUON_ROMAJI)},
    **{94+i: value for i,value in enumerate(GOJUON_ROMAJI)},
    **{60+i: value for i,value in enumerate(('xtsu','ya','yu','yo'))},
    **{140+i: value for i,value in enumerate(('xtsu','ya','yu','yo'))},
    **{64+i: value for i,value in enumerate(VOICED_ROMAJI)},
    **{144+i: value for i,value in enumerate(VOICED_ROMAJI)},
    **{89+i: value for i,value in enumerate(('a','i','u','e','o'))},
    **{169+i: value for i,value in enumerate(('a','i','u','e','o'))},
}

def romanized_japan_search(tokens: tuple[int, ...], *, compact_spaces: bool = False) -> str:
    """Hypothetical romaji search key, with unknown glyphs as hard barriers.

    Ignore native display-colour/spacing commands, but do not accidentally
    join across an unmapped glyph, a record terminator or a line break.
    For oversized dramatic text, optional compact_spaces matches words whose
    source intentionally places a space between *every* character.
    """
    result = []
    for token in tokens:
        if token == 13:
            if not compact_spaces:
                result.append(' ')
        elif token in ROMAJI_BY_TOKEN:
            result.append(ROMAJI_BY_TOKEN[token])
        elif token == -60:
            result.append('\n')
        elif token == -1:
            break
        elif token < 0:
            # Original control tokens affect style/state, not glyph meaning.
            # Keep line-break and terminator barriers above.
            continue
        elif JP_CONFIRMED_GLYPHS.get(token) == '！':
            result.append('!')
        elif token in JP_CONFIRMED_GLYPHS:
            # Other proven punctuation/brackets must not make false romaji.
            result.append('|')
        else:
            result.append('|')
    return ''.join(result)


def japanese_query_matches(tokens: tuple[int, ...], query: str) -> bool:
    """Match a romanized query without treating unsupported glyphs as known."""
    query = query.strip().casefold()
    if not query or not query.isascii() or not any('a' <= c <= 'z' for c in query):
        return False
    return (query in romanized_japan_search(tokens).casefold() or
            query in romanized_japan_search(tokens, compact_spaces=True).casefold())

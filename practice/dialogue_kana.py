"""Original Japan font-order kana provenance and romaji/digit preview.

All 160 source-order kana are now directly editable. Their 84 not
individually screenshot-confirmed positions retain inferred provenance.
Other unverified glyphs, including most digits, remain numeric.
"""
from __future__ import annotations

from practice.dialogue_japan import JP_CONFIRMED_GLYPHS
from practice.dialogue_rom import CONTROLS

from practice.dialogue_kana_table import (
    HIRAGANA, KATAKANA, HIRAGANA_START, KATAKANA_START, KANA_OFFSET,
    HIRA_SMALL, KATA_SMALL, HIRA_VOICED, KATA_VOICED,
    HIRA_SMALL_VOWELS, KATA_SMALL_VOWELS, JP_KANA_HYPOTHESIS,
)

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
    """Readable kana with additional optional digit/font-order guesses."""
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
    """Source-order glyphs lacking individual gameplay screenshot proof."""
    return sum(t in JP_GLYPH_HYPOTHESIS and t not in JP_CONFIRMED_GLYPHS
               for t in tokens)


# Search-only romanization of the source-order gojuon and voiced kana.
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

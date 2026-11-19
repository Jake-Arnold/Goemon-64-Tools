"""Unverified Japan-0 kana ordering hypothesis for read-only inspection.

EVIDENCE: Screenshot-verified pairs 15=い/95=イ and 19=か/99=カ,
plus 16=う. Both script pairs are exactly 80 token IDs apart.

CONJECTURE: Simple gojuon order starting at 14 and 94. No other character
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

# Explicitly hypothetical: these 92 candidates do NOT extend the encoder.
JP_KANA_HYPOTHESIS = {
    **{HIRAGANA_START + i: c for i, c in enumerate(HIRAGANA)},
    **{KATAKANA_START + i: c for i, c in enumerate(KATAKANA)},
}

# Verify our hypotheses don't contradict the small set of screenshot proofs.
for _id, _character in JP_CONFIRMED_GLYPHS.items():
    if _id in JP_KANA_HYPOTHESIS and JP_KANA_HYPOTHESIS[_id] != _character:
        raise AssertionError(f'Kana hypothesis contradicts verified token {_id}')


def decode_japan_kana_preview(tokens: tuple[int, ...]) -> str:
    """Human-readable *hypothesis*, never intended for direct ROM encoding."""
    return ''.join(
        ' ' if value == 13 else
        JP_CONFIRMED_GLYPHS.get(value, JP_KANA_HYPOTHESIS.get(
            value, CONTROLS.get(value, f'<token:{value}>')))
        for value in tokens
    )


def inferred_kana_count(tokens: tuple[int, ...]) -> int:
    """Count guessed characters as distinct from screenshot-confirmed ones."""
    return sum(value in JP_KANA_HYPOTHESIS and value not in JP_CONFIRMED_GLYPHS
               for value in tokens)

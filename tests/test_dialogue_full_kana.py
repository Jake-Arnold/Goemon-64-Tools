"""Structural Japanese kana map coverage and round-trip safety.

No original game assets are embedded. Corpus test runs only when an original,
SHA-1-pinned Japanese decompressed ROM is explicitly present.
"""
from __future__ import annotations
from collections import Counter
import os
import unittest

from practice.dialogue_kana_table import (
    JP_KANA_HYPOTHESIS, JP_UNOBSERVED_KANA_IDS, KANA_GROUPS,
    HIRAGANA, KATAKANA, KANA_OFFSET)
from practice.dialogue_japan import (
    JP_CONFIRMED_GLYPHS, JP_EDITABLE_GLYPHS,
    decode_japan_tokens, encode_japan_text,
    extract_japan_dialogue, load_japan_image,
    JapanDialogueRecord, validate_japan_replacement)


class StructuralKanaTests(unittest.TestCase):
    def test_all_eight_source_order_blocks_cover_exactly_160_distinct_glyphs(self):
        self.assertEqual(len(KANA_GROUPS),8)
        self.assertEqual(len(JP_KANA_HYPOTHESIS),160)
        self.assertEqual(sorted(JP_KANA_HYPOTHESIS),list(range(14,174)))
        self.assertEqual(len(set(JP_KANA_HYPOTHESIS.values())),160)
        self.assertEqual(KANA_OFFSET,80)
        for i in range(46):
            self.assertEqual(JP_KANA_HYPOTHESIS[14+i],HIRAGANA[i])
            self.assertEqual(JP_KANA_HYPOTHESIS[94+i],KATAKANA[i])

    def test_all_76_screen_anchors_agree_and_84_other_positions_are_attributed(self):
        self.assertEqual(len(JP_CONFIRMED_GLYPHS),131)
        overlap=set(JP_CONFIRMED_GLYPHS)&set(JP_KANA_HYPOTHESIS)
        self.assertEqual(len(overlap),76)
        self.assertEqual(len(JP_KANA_HYPOTHESIS)-len(overlap),84)
        for token in overlap:
            self.assertEqual(JP_CONFIRMED_GLYPHS[token],JP_KANA_HYPOTHESIS[token])
        self.assertEqual(len(JP_EDITABLE_GLYPHS),215)

    def test_all_160_kana_round_trip_without_token_changes(self):
        tokens=tuple(range(14,174))
        glyphs=decode_japan_tokens(tokens)
        self.assertEqual(len(glyphs),160)
        self.assertEqual(encode_japan_text(glyphs),tokens)
        for token,glyph in JP_KANA_HYPOTHESIS.items():
            with self.subTest(token=token,glyph=glyph):
                self.assertEqual(encode_japan_text(glyph),(token,))

    def test_three_unobserved_positions_remain_labelled_inferred(self):
        self.assertEqual(JP_UNOBSERVED_KANA_IDS,frozenset({138,155,171}))
        self.assertEqual(
            tuple(JP_KANA_HYPOTHESIS[t] for t in sorted(JP_UNOBSERVED_KANA_IDS)),
            ('ヲ','ヂ','ゥ'))
        for token in JP_UNOBSERVED_KANA_IDS:
            self.assertNotIn(token,JP_CONFIRMED_GLYPHS)

    def test_native_controls_and_unmapped_kanji_remain_guarded(self):
        for glyph in ('漢','字','ヵ','ゔ','２','z'):
            with self.subTest(glyph=glyph),self.assertRaises(ValueError):
                encode_japan_text(glyph)
        self.assertEqual(encode_japan_text('<token:395>'),(395,))
        original=JapanDialogueRecord(112,0x20,0x700020,(14,-33,15,-32),(0x08,))
        self.assertEqual(validate_japan_replacement(original,'あ<token:-33>き<token:-32>\n'),
                         (14,-33,20,-32,-60))
        with self.assertRaises(ValueError):
            validate_japan_replacement(original,'あき<token:-32>\n')


class OriginalJapanKanaCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not src:
            raise unittest.SkipTest('Original SHA-1-pinned Japanese ROM not provided')
        cls.records=extract_japan_dialogue(load_japan_image(src))

    def test_5039_source_records_44077_kana_and_157_positions_used(self):
        self.assertEqual(len(self.records),5039)
        frequencies=Counter(t for r in self.records for t in r.tokens if t in JP_KANA_HYPOTHESIS)
        self.assertEqual(sum(frequencies.values()),44077)
        self.assertEqual(len(frequencies),157)
        self.assertEqual(set(JP_KANA_HYPOTHESIS)-set(frequencies),
                         set(JP_UNOBSERVED_KANA_IDS))

    def test_5039_original_records_round_trip_byte_identically(self):
        for record in self.records:
            with self.subTest(key=record.key):
                self.assertEqual(encode_japan_text(record.text),record.tokens)


if __name__=='__main__':
    unittest.main()

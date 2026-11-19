"""Tests for Japan-0 speculative kana preview; hypotheses must never write ROMs."""
from __future__ import annotations

import os
import unittest

from practice.dialogue_japan import (encode_japan_text, decode_japan_tokens,
                                     extract_japan_dialogue, load_japan_image)
from practice.dialogue_kana import (
    HIRAGANA, KATAKANA, JP_KANA_HYPOTHESIS,
    decode_japan_kana_preview, inferred_kana_count,
)


class KanaHypothesisTests(unittest.TestCase):
    def test_predicted_gojuon_ranges_and_offset(self):
        self.assertEqual(len(HIRAGANA),46)
        self.assertEqual(len(KATAKANA),46)
        self.assertEqual(len(JP_KANA_HYPOTHESIS),92)
        self.assertEqual(JP_KANA_HYPOTHESIS[14],'あ')
        self.assertEqual(JP_KANA_HYPOTHESIS[15],'い')
        self.assertEqual(JP_KANA_HYPOTHESIS[19],'か')
        self.assertEqual(JP_KANA_HYPOTHESIS[95],'イ')
        self.assertEqual(JP_KANA_HYPOTHESIS[99],'カ')
        self.assertEqual(JP_KANA_HYPOTHESIS[139],'ン')

    def test_preview_keeps_proven_glyphs_and_controls(self):
        title=(13,13,292,-33,99,95,-32,293,-60)
        road=(13,13,13,13,13,19,15,78,16)
        self.assertEqual(decode_japan_kana_preview(title),
                         '  【<token:-33>カイ<token:-32>】\n')
        self.assertEqual(decode_japan_kana_preview(road),'     かいどう')
        self.assertEqual(inferred_kana_count(road),0)
        self.assertEqual(decode_japan_kana_preview((14,20,94,100,78,250)),
                         'あきアキど<token:250>')
        self.assertEqual(inferred_kana_count((14,20,94,100,78,250)),4)

    def test_unverified_preview_is_not_accepted_by_encoder(self):
        raw=(14,20,94,100)
        self.assertEqual(decode_japan_tokens(raw),
                         '<token:14><token:20><token:94><token:100>')
        with self.assertRaises(ValueError):
            encode_japan_text(decode_japan_kana_preview(raw))
        # Exact original bytes remain round-trip safe in the actual editor.
        self.assertEqual(encode_japan_text(decode_japan_tokens(raw)),raw)

    def test_original_jp_record_preview_is_reproducible(self):
        source=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not source:self.skipTest('Set GOEMON_JP_DECOMPRESSED_ROM')
        records=extract_japan_dialogue(load_japan_image(source))
        self.assertEqual(len(records),5039)
        for offset in (4,0x18):
            rec=next(r for r in records if r.resource_id==82 and r.text_offset==offset)
            self.assertEqual(decode_japan_kana_preview(rec.tokens),rec.text)
            self.assertEqual(encode_japan_text(rec.text),rec.tokens)


if __name__ == '__main__':
    unittest.main()

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
        self.assertEqual(len(JP_KANA_HYPOTHESIS),160)
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
        self.assertEqual(inferred_kana_count((14,20,94,100,78,250)),3)

    def test_unverified_preview_is_not_accepted_by_encoder(self):
        raw=(17,20,94,100)
        self.assertEqual(decode_japan_tokens(raw),
                         '<token:17><token:20><token:94><token:100>')
        with self.assertRaises(ValueError):
            encode_japan_text(decode_japan_kana_preview(raw))
        # Exact original bytes remain round-trip safe in the actual editor.
        self.assertEqual(encode_japan_text(decode_japan_tokens(raw)),raw)

    def test_uppercase_and_digits_hypotheses_remain_readonly(self):
        from practice.dialogue_kana import (JP_LATIN_HYPOTHESIS,
            JP_DIGIT_HYPOTHESIS, inferred_glyph_count)
        self.assertEqual(len(JP_LATIN_HYPOTHESIS),26)
        self.assertEqual(len(JP_DIGIT_HYPOTHESIS),10)
        self.assertEqual(JP_LATIN_HYPOTHESIS[191],'F')
        self.assertEqual(JP_LATIN_HYPOTHESIS[200],'O')
        self.assertEqual(JP_LATIN_HYPOTHESIS[206],'U')
        self.assertEqual(decode_japan_kana_preview((204,205,186,203,205)),'START')
        self.assertEqual(decode_japan_kana_preview((176,177,178,185)),'０１２９')
        self.assertEqual(inferred_glyph_count((191,200,206,204,205,186,203,205)),0)
        self.assertEqual(encode_japan_text('UFO'),(206,191,200))
        self.assertEqual(encode_japan_text('START'),(204,205,186,203,205))
        self.assertEqual(inferred_glyph_count((207,208,209,210,211)),5)
        with self.assertRaises(ValueError):encode_japan_text('VWXYZ')
        with self.assertRaises(ValueError):encode_japan_text('２')

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


class RomajiSearchTests(unittest.TestCase):
    def test_romanized_kana_and_voiced_plasma(self):
        from practice.dialogue_kana import romanized_japan_search, japanese_query_matches
        # Original game dramatically spaces the Plasma callout across glyphs.
        sample=(13,13,-56,-50,166,13,132,13,151,13,124,13,89,13,212,13,212,-51,-57,-60)
        self.assertEqual(romanized_japan_search(sample,compact_spaces=True), 'purazumaa!!\n')
        for query in ('pu','PU','pura','purazuma','purazumaa'):
            self.assertTrue(japanese_query_matches(sample,query),query)
        self.assertFalse(japanese_query_matches(sample,'kana'))
        self.assertFalse(japanese_query_matches(sample,'plasma'))
        self.assertEqual(decode_japan_kana_preview(sample),
            '  <token:-56><token:-50>プ ラ ズ マ ぁ ！ ！<token:-51><token:-57>\n')
        self.assertEqual(encode_japan_text(decode_japan_kana_preview(sample)),sample)

    def test_guesses_never_enter_rom_encoder(self):
        # Only screenshot-aligned characters are promoted, not the gojuon hypothesis.
        for glyph in ('え','キ','ぬ'):
            with self.assertRaises(ValueError):
                encode_japan_text(glyph)
        self.assertEqual(encode_japan_text('プラズマぁ！！'),(166,132,151,124,89,212,212))

    def test_unknown_tokens_block_romanized_false_positives(self):
        from practice.dialogue_kana import japanese_query_matches
        self.assertFalse(japanese_query_matches((166,250,132),'pura'))
        self.assertTrue(japanese_query_matches((166,250,132),'pu'))
        self.assertTrue(japanese_query_matches((166,250,132),'ra'))

    def test_original_plasma_dialogue_match(self):
        from practice.dialogue_kana import japanese_query_matches
        source=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not source:self.skipTest('Set GOEMON_JP_DECOMPRESSED_ROM')
        records=extract_japan_dialogue(load_japan_image(source))
        match=next(r for r in records if r.resource_id==112 and r.text_offset==0x0c)
        self.assertEqual(match.tokens,
            (13,13,-56,-50,166,13,132,13,151,13,124,13,89,13,212,13,212,-51,-57,-60))
        self.assertTrue(japanese_query_matches(match.tokens,'purazuma'))
        self.assertEqual(encode_japan_text(match.text),match.tokens)


class PlasmaScreenshotSequenceTests(unittest.TestCase):
    """All seven user screens, exact original JP text-record boundaries.

    The user supplied gameplay screenshots; the expected words below come
    from those images, not an independent automated Japanese transcription.
    """
    @classmethod
    def setUpClass(cls):
        import re
        cls.re=re
        source=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not source:raise unittest.SkipTest('Set GOEMON_JP_DECOMPRESSED_ROM')
        cls.records={r.text_offset:r for r in extract_japan_dialogue(load_japan_image(source))
                     if r.resource_id==112}

    def display(self,offset):
        text=decode_japan_kana_preview(self.records[offset].tokens)
        return self.re.sub(r'<[^>]*>', '', text).strip()

    def test_greeting_screenshot_1(self):
        self.assertEqual(self.display(0x60),'プラズマおやぢ')
        self.assertEqual(self.display(0x74),'「どぴょぴょ〜ん！')
        self.assertEqual(self.display(0x8c),'プラズマうらないへ、ようこそじゃ」')

    def test_fee_and_choices_screenshot_2(self):
        self.assertEqual(self.display(0xb8),'「おぬしのなやみを、１０両で')
        self.assertEqual(self.display(0xdc),'かいけつしてプラズマ〜！」')
        self.assertEqual(self.display(0xfc),'お、おねがいします')
        self.assertEqual(self.display(0x118),'い・・・いいや')

    def test_divination_screenshot_3(self):
        self.assertEqual(self.display(0x134),'「うむ、')
        self.assertEqual(self.display(0x144),'では、うらなってしんぜよう！！」')

    def test_repeated_pu_screenshot_4(self):
        self.assertEqual(self.display(0x16c),'「'+'ぷ'*16)
        self.assertEqual(self.display(0x194),'ぷ'*16)
        self.assertEqual(self.display(0x1bc),'ぷ'*12+'っ・・・」')

    def test_plasma_screenshot_5(self):
        self.assertEqual(''.join(self.display(0x1e4).split()),'プラズマぁ〜！')

    def test_oedo_screenshot_6(self):
        self.assertEqual(self.display(0x290),'「大江戸城（おおえどじょう）に')
        self.assertEqual(self.display(0x2b8),'入りたければ・・・')

    def test_directions_screenshot_7(self):
        self.assertEqual(self.display(0x2d0),'このうらない屋からむかってひだりの')
        self.assertEqual(self.display(0x300),'出入口から、【カイのかいどう】に出て')
        self.assertEqual(self.display(0x328),'「ふじ山」へ、むかうプラズマ！')

    def test_records_reencode_identically_after_mapping_expansion(self):
        for r in self.records.values():
            self.assertEqual(encode_japan_text(r.text),r.tokens)

    def test_unverified_hypothesis_still_cannot_be_staged(self):
        # User-verified glyph IDs were promoted, but inferred symbols are not.
        for symbol in ('ぎ','ゅ','ギ','ぽ'):
            with self.assertRaises(ValueError):
                encode_japan_text(symbol)
        self.assertEqual(encode_japan_text('「ぷぷっ・・・」'),
                         (295,86,86,60,232,232,232,297))

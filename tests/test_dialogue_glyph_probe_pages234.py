"""Original Project64 glyph probe pages 2–4, original-Japan source order.

Screenshot transcriptions; game images and original ROM bytes are not bundled.
"""
import os
import unittest
from practice.dialogue_japan import (
    JP_CONFIRMED_GLYPHS, JP_EDITABLE_GLYPHS,
    encode_japan_text, decode_japan_tokens,
    extract_japan_dialogue, load_japan_image,
)
from practice.dialogue_glyph_probe import make_probe_pages, unknown_token_counts
from tests.test_dialogue_glyph_probe_page1 import PAGE_ONE

PAGE_2_TO_4 = [[[308,"人"],[309,"銀"],[310,"力"],[311,"金"],[312,"千"],[313,"花"],[314,"星"],[315,"火"],[316,"丸"],[317,"目"],[319,"間"],[320,"茶"],[321,"店"],[322,"方"],[323,"思"],[325,"外"],[326,"子"],[327,"男"],[328,"♪"],[329,"国"],[330,"地"],[331,"九"],[332,"州"],[333,"女"],[335,"社"],[336,"員"],[338,"語"],[339,"卍"]],[[340,"長"],[342,"話"],[343,"家"],[344,"四"],[345,"文"],[346,"字"],[347,"川"],[348,"小"],[349,"池"],[350,"竹"],[351,"上"],[352,"流"],[353,"回"],[354,"落"],[355,"石"],[356,"○"],[357,"氷"],[358,"犬"],[359,"神"],[360,"名"],[361,"警"],[362,"告"],[363,"発"],[364,"生"],[365,"島"],[366,"木"],[367,"客"],[368,"桜"]],[[369,"先"],[370,"向"],[371,"調"],[372,"艦"],[373,"愛"],[374,"夢"],[375,"仁"],[376,"王"],[377,"良"],[378,"早"],[379,"o"],[380,"i"],[381,"n"],[382,"g"],[383,"w"],[384,"a"],[385,"k"],[386,"e"],[387,"h"],[388,"c"],[389,"野"],[390,"表"],[391,"示"],[392,"破"],[393,"損"],[394,"現"],[395,"犯"]]]
PROBE_ROWS = [PAGE_2_TO_4[0][i:i+7] for i in range(0,28,7)]
PROBE_ROWS += [PAGE_2_TO_4[1][i:i+7] for i in range(0,28,7)]
PROBE_ROWS += [PAGE_2_TO_4[2][i:i+7] for i in range(0,27,7)]


class Project64RemainingGlyphTests(unittest.TestCase):
    def test_83_new_glyphs_align_to_original_manifest_positions(self):
        self.assertEqual([len(page) for page in PAGE_2_TO_4],[28,28,27])
        self.assertEqual([len(row) for row in PROBE_ROWS],[7]*11+[6])
        original_page_one=[token for row in PAGE_ONE for token,_ in row]
        all_ids=original_page_one+[token for page in PAGE_2_TO_4 for token,_ in page]
        self.assertEqual(len(all_ids),111)
        self.assertEqual(all_ids,sorted(all_ids))
        manifest=make_probe_pages(all_ids)
        self.assertEqual([len(p.ids) for p in manifest],[28,28,28,27])
        for page_expected,page_actual in zip([PAGE_ONE]+[
                [page[i:i+7] for i in range(0,len(page),7)]
                for page in PAGE_2_TO_4],manifest):
            self.assertEqual([[token for token,_ in row] for row in page_expected],
                             [list(row) for row in page_actual.rows])
        for page in PAGE_2_TO_4:
            for token,glyph in page:
                with self.subTest(token=token,glyph=glyph):
                    self.assertEqual(JP_CONFIRMED_GLYPHS[token],glyph)
                    self.assertEqual(decode_japan_tokens((token,)),glyph)
                    self.assertEqual(encode_japan_text(glyph),(token,))

    def test_glossary_counts_and_uniqueness(self):
        self.assertEqual(len(JP_CONFIRMED_GLYPHS),242)
        self.assertEqual(len(set(JP_CONFIRMED_GLYPHS.values())),242)
        self.assertEqual(len(JP_EDITABLE_GLYPHS),326)

    def test_independently_recognisable_source_contexts(self):
        self.assertEqual(encode_japan_text('四国'),(344,329))
        self.assertEqual(encode_japan_text('桜島'),(368,365))
        self.assertEqual(encode_japan_text('大戦艦'),(291,289,372))
        self.assertEqual(encode_japan_text('現行犯'),(394,302,395))
        self.assertEqual(encode_japan_text('Going Now'),(192,379,380,381,382,13,199,379,383))
        self.assertEqual(encode_japan_text('○○○'),(356,356,356))
        self.assertEqual(encode_japan_text('目'),(317,))
        self.assertEqual(encode_japan_text('日'),(230,))
        self.assertEqual(encode_japan_text('♪卍'),(328,339))
        with self.assertRaises(ValueError):encode_japan_text('７')

    def test_only_excluded_suspect_11_remains_in_original_index(self):
        source=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not source:self.skipTest('Pinned original JP ROM not supplied')
        records=extract_japan_dialogue(load_japan_image(source))
        self.assertEqual(len(records),5039)
        remaining=unknown_token_counts(records)
        self.assertEqual(dict(remaining),{11:1})


if __name__=='__main__':unittest.main()

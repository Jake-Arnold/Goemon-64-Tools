"""User-proven Project64 page-one glyphs and source-index integrity."""
import os
import unittest
from practice.dialogue_japan import (
    JP_CONFIRMED_GLYPHS, JP_EDITABLE_GLYPHS,
    encode_japan_text, decode_japan_tokens,
    extract_japan_dialogue, load_japan_image)
from practice.dialogue_glyph_probe import unknown_token_counts

PAGE_ONE = [[[178,"２"],[179,"３"],[180,"４"],[181,"５"],[182,"６"],[184,"８"],[185,"９"]],[[226,"。"],[229,"旅"],[230,"日"],[239,"数"],[242,"中"],[245,"見"],[256,"本"]],[[257,"体"],[265,"場"],[277,"村"],[284,"北"],[286,"東"],[287,"寺"],[289,"戦"]],[[294,"前"],[298,"下"],[299,"止"],[300,"［"],[301,"］"],[306,"水"],[307,"海"]]]

class Project64PageOneGlyphTests(unittest.TestCase):
    def test_visible_28_glyphs_follow_exact_manifest_positions(self):
        self.assertEqual(len(PAGE_ONE),4)
        self.assertTrue(all(len(row)==7 for row in PAGE_ONE))
        for row in PAGE_ONE:
            for token,glyph in row:
                with self.subTest(token=token,glyph=glyph):
                    self.assertEqual(JP_CONFIRMED_GLYPHS[token],glyph)
                    self.assertEqual(decode_japan_tokens((token,)),glyph)
                    self.assertEqual(encode_japan_text(glyph),(token,))
        self.assertEqual(len(JP_CONFIRMED_GLYPHS),242)
        self.assertEqual(len(JP_EDITABLE_GLYPHS),326)

    def test_digits_7_remains_unproved(self):
        with self.assertRaises(ValueError):
            encode_japan_text('７')
        self.assertEqual(encode_japan_text('２３４５６８９'),(178,179,180,181,182,184,185))

    def test_original_index_unknown_count_after_all_pages(self):
        source=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not source:self.skipTest('Pinned original Japanese ROM not supplied')
        records=extract_japan_dialogue(load_japan_image(source))
        remaining=unknown_token_counts(records)
        self.assertEqual(dict(remaining),{})
        self.assertNotIn(226,remaining)
        self.assertNotIn(11,remaining)

"""Japan token 11: native visual ！ alias with exact original ID preserved."""
import os
import struct
import unittest

from practice.dialogue_japan import (
    JP_CONFIRMED_GLYPHS, JP_EDITABLE_GLYPHS,
    JP_NATIVE_RENDERED_ALIASES, JP_SCREENSHOT_CONFIRMED_TOKEN_COUNT,
    decode_japan_tokens, encode_japan_text,
    extract_japan_dialogue, load_japan_image)
from practice.dialogue_glyph_probe import unknown_token_counts


class Token11GuardTests(unittest.TestCase):
    def test_token_11_is_visual_alias_not_a_canonical_editor_token(self):
        self.assertNotIn(11, JP_CONFIRMED_GLYPHS)
        self.assertNotIn(11, JP_EDITABLE_GLYPHS)
        self.assertEqual(JP_NATIVE_RENDERED_ALIASES, {11: '！'})
        self.assertEqual(JP_SCREENSHOT_CONFIRMED_TOKEN_COUNT, 243)
        self.assertEqual(encode_japan_text('！'), (212,))
        self.assertEqual(decode_japan_tokens((11, 212), visual_aliases=True), '！！')
        self.assertEqual(decode_japan_tokens((16, 303, 59, 11, -60),
                                             visual_aliases=True), 'う〜ん！\n')
        self.assertEqual(decode_japan_tokens((16, 303, 59, 11, -60)),
                         'う〜ん<token:11>\n')
        self.assertEqual(encode_japan_text('う〜ん<token:11>\n'),
                         (16, 303, 59, 11, -60))
        from practice.dialogue_kana import decode_japan_kana_preview
        self.assertEqual(decode_japan_kana_preview((16, 303, 59, 11, -60)), 'う〜ん！\n')
        self.assertEqual(encode_japan_text('う〜ん！\n'), (16, 303, 59, 212, -60))

    def test_probe_changes_exactly_one_positive_glyph(self):
        original = (13,13,13,13,13,19,15,78,16)
        for candidate, label in ((11, '<token:11>'), (212, '！')):
            edited = original[:7] + (candidate,) + original[8:]
            self.assertEqual(len(original), len(edited))
            self.assertEqual([i for i,(a,b) in enumerate(zip(original,edited))
                              if a!=b], [7])
            self.assertEqual(encode_japan_text('     かい' + label + 'う'), edited)


class OriginalToken11SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not path:
            raise unittest.SkipTest('Original Japan-0 decompressed ROM not supplied')
        cls.image = load_japan_image(path)
        cls.records = extract_japan_dialogue(cls.image)

    def test_one_original_record_at_verified_address(self):
        self.assertEqual(len(self.records), 5039)
        rows = [r for r in self.records if 11 in r.tokens]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual((row.resource_id,row.text_offset,row.image_offset),
                         (97,0x2B60,0x75A140))
        self.assertEqual(row.references,(0x73FC,))
        self.assertEqual(row.tokens,(16,303,59,11,-60))
        self.assertEqual(struct.unpack_from('>6h',self.image,0x75A140),
                         (16,303,59,11,-60,-1))
        self.assertEqual(struct.unpack_from('>II',self.image,0x75E9DC),
                         (0x8010,0x08002B60))
        self.assertEqual(dict(unknown_token_counts(self.records)), {})


if __name__ == '__main__':
    unittest.main()

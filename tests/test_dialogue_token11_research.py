"""Japan token 11: static source proof, not a native-rendered glyph mapping."""
import os
import struct
import unittest

from practice.dialogue_japan import (
    JP_CONFIRMED_GLYPHS, JP_EDITABLE_GLYPHS,
    decode_japan_tokens, encode_japan_text,
    extract_japan_dialogue, load_japan_image)
from practice.dialogue_glyph_probe import unknown_token_counts


class Token11GuardTests(unittest.TestCase):
    def test_token_11_stays_unclassified(self):
        self.assertNotIn(11, JP_CONFIRMED_GLYPHS)
        self.assertNotIn(11, JP_EDITABLE_GLYPHS)
        self.assertEqual(decode_japan_tokens((16, 303, 59, 11, -60)),
                         'う〜ん<token:11>\n')
        self.assertEqual(encode_japan_text('う〜ん<token:11>\n'),
                         (16, 303, 59, 11, -60))

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
        self.assertEqual(dict(unknown_token_counts(self.records)), {11:1})


if __name__ == '__main__':
    unittest.main()

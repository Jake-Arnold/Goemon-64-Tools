"""13 user-gameplay-screenshot ROM alignments for Hagure Town / Oedo.

Each Japanese line was visually read from the user-provided screenshot and
aligned, position by position, with a pinned original Japan ROM record.
This fixture contains transcriptions and offsets, not uploaded screenshots or ROM data.
"""
from __future__ import annotations

import os
import unittest

from practice.dialogue_japan import (JP_CONFIRMED_GLYPHS, JP_DECOMPRESSED_SHA1,
    encode_japan_text, extract_japan_dialogue, load_japan_image)
from practice.dialogue_kana import JP_KANA_HYPOTHESIS

SCREEN_LINES = (
    (  # Screenshot 1
        (93, 0xC84, '【大江戸'),
        (93, 0xC94, '・はぐれ町】'),
    ),
    (  # Screenshot 2
        (96, 0x2D98, '「UFOだって？'),
    ),
    (  # Screenshot 3
        (96, 0x2DAC, 'ハハハハハハハハハハハハハ'),
        (96, 0x2DCC, 'ハハハハハハハハハハ・・・'),
    ),
    (  # Screenshot 4
        (96, 0x2DEC, 'そんなことより、'),
        (96, 0x2E00, 'うちのチャッピーは、いいイヌだろう！'),
    ),
    (  # Screenshot 5
        (96, 0x2BFC, 'チャッピー「あ〜だる〜ぅ・・・'),
        (96, 0x2C20, 'はやく、メシくって'),
        (96, 0x2C44, 'ねたいワン」'),
    ),
    (  # Screenshot 6
        (96, 0x2C60, 'チャッピー「なんか、'),
        (96, 0x2C78, 'しんどいんだワン」'),
    ),
    (  # Screenshot 7
        (96, 0x4E10, 'にしへ行けば、'),
        (96, 0x4E28, 'ふじ山あり！'),
    ),
    (  # Screenshot 8
        (96, 0x4DDC, 'ピタリと、あたる！'),
        (96, 0x4DF4, 'うらない屋スグソコ！'),
    ),
    (  # Screenshot 9
        (96, 0x1A78, '「こまった・・・こまった！'),
        (96, 0x1A98, 'あ〜〜あ'),
        (96, 0x1AA8, 'こまった、こまった・・・・・・'),
    ),
    (  # Screenshot 10
        (96, 0x1ACC, 'そんな、こまった時には'),
        (96, 0x1AE8, 'うらない屋に行くのが'),
        (96, 0x1B04, 'いちばんじゃよ！'),
    ),
    (  # Screenshot 11
        (96, 0x1B18, 'プラズマパワーで、'),
        (96, 0x1B34, 'なやみもかいけつじゃて！！'),
    ),
    (  # Screenshot 12
        (96, 0x278C, '「わしゃ、ふじ山に'),
        (96, 0x27A8, 'のぼりに来たんじゃ・・・'),
    ),
    (  # Screenshot 13
        (96, 0x27C8, 'たしか、やくにんから'),
        (96, 0x27E0, 'うらない屋のカドをまがったとこから'),
        (96, 0x280C, '行けるってのは聞いたんじゃがのぉ'),
    ),
)

NEW_SCREENSHOT_GLYPHS = {
    14: 'あ',
    21: 'く',
    22: 'け',
    23: 'こ',
    25: 'し',
    28: 'そ',
    29: 'た',
    30: 'ち',
    31: 'つ',
    32: 'て',
    33: 'と',
    34: 'な',
    35: 'に',
    37: 'ね',
    38: 'の',
    39: 'は',
    41: 'ふ',
    42: 'へ',
    44: 'ま',
    45: 'み',
    48: 'も',
    49: 'や',
    51: 'よ',
    52: 'ら',
    53: 'り',
    54: 'る',
    55: 'れ',
    56: 'ろ',
    57: 'わ',
    58: 'を',
    59: 'ん',
    66: 'ぐ',
    83: 'ぼ',
    91: 'ぅ',
    93: 'ぉ',
    103: 'コ',
    105: 'シ',
    106: 'ス',
    108: 'ソ',
    109: 'タ',
    110: 'チ',
    116: 'ヌ',
    119: 'ハ',
    127: 'メ',
    133: 'リ',
    137: 'ワ',
    139: 'ン',
    140: 'ッ',
    141: 'ャ',
    146: 'グ',
    158: 'ド',
    164: 'パ',
    165: 'ピ',
    175: 'ー',
    191: 'F',
    200: 'O',
    206: 'U',
    224: '？',
    276: '町',
    302: '行',
    318: '時',
    324: '来',
    337: '聞',
}

class OedoScreenshotAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rom_path = os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        if not rom_path:raise unittest.SkipTest('Set GOEMON_JP_DECOMPRESSED_ROM')
        source = load_japan_image(rom_path)  # Enforces original ROM SHA-1.
        cls.records = {(r.resource_id, r.text_offset):r
                       for r in extract_japan_dialogue(source)}

    def test_all_thirteen_screens_match_original_individual_records(self):
        self.assertEqual(len(SCREEN_LINES),13)
        self.assertEqual(sum(map(len, SCREEN_LINES)),29)
        for screen_idx,lines in enumerate(SCREEN_LINES, 1):
            for rid,off,transcription in lines:
                with self.subTest(screen=screen_idx,resource=rid,offset=hex(off)):
                    record=self.records[(rid,off)]
                    characters=[JP_CONFIRMED_GLYPHS.get(token) for token in record.tokens
                                if token>=0 and token!=13]
                    self.assertNotIn(None,characters)
                    self.assertEqual(''.join(characters),transcription)
                    # Exact control, newline and indent values survive encoding.
                    self.assertEqual(encode_japan_text(record.text),record.tokens)

    def test_63_newly_confirmed_ids_have_unique_inverse_and_compatible_kana(self):
        self.assertEqual(len(NEW_SCREENSHOT_GLYPHS),63)
        self.assertEqual(len(JP_CONFIRMED_GLYPHS),108)
        self.assertEqual(len(set(JP_CONFIRMED_GLYPHS.values())),108)
        for token,character in NEW_SCREENSHOT_GLYPHS.items():
            self.assertEqual(JP_CONFIRMED_GLYPHS[token],character)
            self.assertEqual(encode_japan_text(character),(token,))
            if token in JP_KANA_HYPOTHESIS:
                self.assertEqual(JP_KANA_HYPOTHESIS[token],character)

    def test_new_latin_letters_and_unknowns(self):
        self.assertEqual(encode_japan_text('UFO'),(206,191,200))
        self.assertEqual(encode_japan_text('「UFOだって？'),(295,206,191,200,74,60,32,224))
        for value in ('B','C','A','お','ぬ','ギ'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                encode_japan_text(value)

    def test_every_new_id_is_present_at_a_screen_aligned_position(self):
        aligned={}
        for lines in SCREEN_LINES:
            for rid,offset,transcription in lines:
                tokens=[t for t in self.records[(rid,offset)].tokens if t>=0 and t!=13]
                self.assertEqual(len(tokens),len(transcription))
                for token,letter in zip(tokens,transcription):
                    if token in aligned:self.assertEqual(aligned[token],letter)
                    aligned[token]=letter
        for token,ch in NEW_SCREENSHOT_GLYPHS.items():
            self.assertEqual(aligned[token],ch)

if __name__ == "__main__":unittest.main()

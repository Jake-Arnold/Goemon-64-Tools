"""USA Goemon dialogue extraction/patch tests; never bundle copyrighted ROM bytes."""
from __future__ import annotations
from dataclasses import replace
import os
import struct
import tempfile
import unittest
from pathlib import Path

from practice.dialogue_rom import (
    USA_DECOMPRESSED_SHA1, ROM_SIZE, DialogueRecord, decode_tokens,
    encode_text, extract_dialogue, load_usa_image, patch_image,
    validate_replacement, save_patched_image,
)


class DialogueEncodingTests(unittest.TestCase):
    def test_known_tokens(self):
        self.assertEqual(decode_tokens((57, 65, 69, 26, 51, 79)), 'Yae:So')
        self.assertEqual(encode_text('Yae:So'), (57, 65, 69, 26, 51, 79))

    def test_controls_roundtrip(self):
        tokens = (-70, 57, -60, 65, -61, -62, -63, -71, -33, -37)
        self.assertEqual(encode_text(decode_tokens(tokens)), tokens)

    def test_unknown_glyph_rejected(self):
        with self.assertRaises(ValueError):
            encode_text('€')
        with self.assertRaises(ValueError):
            encode_text('<script>')
        with self.assertRaises(ValueError):
            encode_text('<token:-1>')

    def test_original_control_slots_unchanged(self):
        r = DialogueRecord(96, 2, 0x110000, (40, -60, 65), (8,))
        self.assertEqual(validate_replacement(r, 'I\na'), (41, -60, 65))
        with self.assertRaises(ValueError):
            validate_replacement(r, 'Iaa')
        with self.assertRaises(ValueError):
            validate_replacement(r, 'I\naa')


class DialogueOriginalImageTests(unittest.TestCase):
    """ROM tests only run when GOEMON_USA_DECOMPRESSED_ROM is supplied locally."""
    @classmethod
    def setUpClass(cls):
        path = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not path:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM for original-ROM tests')
        cls.path = Path(path)
        cls.image = load_usa_image(cls.path)
        cls.records = extract_dialogue(cls.image)

    def test_known_zazen_gate_record(self):
        known = next(r for r in self.records if r.resource_id == 97 and r.text_offset == 4)
        self.assertIn(0x9608, known.references)
        self.assertEqual(known.tokens[0], 57)
        self.assertEqual(known.image_offset, 0x759DF4)

    def test_exact_noop_preserves_original_bytes(self):
        r = next(r for r in self.records if r.resource_id == 97 and r.text_offset == 4)
        edited = patch_image(self.image, self.records, {r.key: r.text})
        self.assertEqual(edited, self.image)

    def test_original_header_tables_are_unmodified(self):
        r = next(r for r in self.records if r.resource_id == 97 and r.text_offset == 4)
        original = r.text
        replacement = ('X' if original[0] != 'X' else 'Y') + original[1:]
        patched = patch_image(self.image, self.records, {r.key: replacement})
        self.assertEqual(patched[:r.image_offset], self.image[:r.image_offset])
        self.assertEqual(patched[r.image_offset+len(r.tokens)*2:],
                         self.image[r.image_offset+len(r.tokens)*2:])
        self.assertEqual(struct.unpack_from('>h', patched, r.image_offset)[0],
                         encode_text(replacement)[0])
        self.assertEqual(patched[r.image_offset+len(r.tokens)*2:r.image_offset+len(r.tokens)*2+2],
                         self.image[r.image_offset+len(r.tokens)*2:r.image_offset+len(r.tokens)*2+2])

    def test_stale_record_rejected(self):
        r = self.records[0]
        wrong = replace(r, image_offset=r.image_offset+2)
        with self.assertRaises(ValueError):
            patch_image(self.image, [wrong], {wrong.key: wrong.text})

    def test_save_refuses_overwriting_source(self):
        r = self.records[0]
        with self.assertRaises(ValueError):
            save_patched_image(self.path, self.path, self.records, {r.key: r.text})


if __name__ == '__main__':
    unittest.main()

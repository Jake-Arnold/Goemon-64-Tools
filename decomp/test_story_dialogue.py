"""ROM-free regressions for regional token decoding and dialogue story anchors."""
from __future__ import annotations

import struct
import unittest

from decomp import story_dialogue as story
from decomp import text_tokens as tokens


class TokenCatalogueTests(unittest.TestCase):
    def test_japanese_provenance_counts(self):
        self.assertEqual(tokens.JP_SCREENSHOT_CONFIRMED_TOKEN_COUNT, 243)
        self.assertEqual(len(tokens.JP_CONFIRMED_GLYPHS), 242)
        self.assertEqual(len(tokens.JP_KANA_HYPOTHESIS), 160)
        self.assertEqual(len(tokens.JP_EDITABLE_GLYPHS), 326)
        self.assertNotIn(183, tokens.JP_EDITABLE_GLYPHS)

    def test_japanese_source_roundtrip_preserves_native_alias(self):
        original = (13, 19, 15, 78, 16, -60, 11, 212, -57)
        source = tokens.decode_tokens('japan_0', original)
        self.assertIn('<token:11>', source)
        self.assertIn('<token:-57>', source)
        self.assertEqual(tokens.encode_tokens('japan_0', source), original)
        self.assertTrue(tokens.roundtrip_original('japan_0', original))
        self.assertEqual(tokens.decode_tokens('japan_0', (11, 212),
                                              visual_aliases=True), '！！')
        self.assertEqual(tokens.encode_tokens('japan_0', '！'), (212,))

    def test_us_duplicate_glyphs_remain_numeric(self):
        self.assertEqual(tokens.decode_tokens('usa', (12, 60)), '<token:12><token:60>')
        self.assertEqual(tokens.decode_tokens('usa', (12, 60),
                                              visual_aliases=True), ',,')
        self.assertTrue(tokens.roundtrip_original('usa', (12, 60, -60, -57, 65)))
        with self.assertRaises(ValueError):
            tokens.encode_tokens('usa', ',')

    def test_region_independence(self):
        self.assertEqual(tokens.decode_tokens('japan_0', (13,)), ' ')
        self.assertEqual(tokens.decode_tokens('usa', (13,)), '-')
        with self.assertRaises(ValueError):
            tokens.decode_tokens('japan', (13,))

    def test_signed_halfword_encoding_and_invalid_terminator(self):
        self.assertEqual(tokens.token_bytes((-71, 11, 212)),
                         struct.pack('>hhh', -71, 11, 212))
        with self.assertRaises(ValueError):
            tokens.encode_tokens('japan_0', '<token:-1>')
        with self.assertRaises(ValueError):
            tokens.token_bytes((32768,))
        with self.assertRaises(ValueError):
            tokens.encode_tokens('usa', '<token:32768>')

    def test_usa_control_dispatch_notes_are_region_specific(self):
        self.assertIn('presentation selector', tokens.CONTROL_NOTES[-33])
        self.assertIn('window', tokens.CONTROL_NOTES[-56])
        self.assertIn(-69, tokens.NOOP_TOKENS)

    def test_common_controls_and_opaque_negatives(self):
        source = tokens.decode_tokens('usa', (-70, -60, -61, -71, -32))
        self.assertEqual(source, '<open-window>\n<state-3><close-window><token:-32>')
        self.assertEqual(tokens.encode_tokens('usa', source),
                         (-70, -60, -61, -71, -32))


class StoryAnchorTests(unittest.TestCase):
    def setUp(self):
        raw = bytearray(0x70)
        struct.pack_into('>II', raw, 0x08, 0x8010, 0x08000020)
        struct.pack_into('>II', raw, 0x14, 0x8010, 0x08000020)
        struct.pack_into('>5h', raw, 0x20, 13, 19, 15, -60, -1)
        self.records = story.scan_resource('japan_0', 97, 0x75A140,
                                           0x08000000, bytes(raw))

    def test_two_static_references_one_anchor(self):
        self.assertEqual(len(self.records), 1)
        anchor = self.records[0]
        self.assertEqual(anchor.key, 'japan_0:97:0x20')
        self.assertEqual(anchor.references, (0x08, 0x14))
        self.assertEqual(anchor.tokens, (13, 19, 15, -60))
        self.assertEqual(anchor.decompressed_text_offset, 0x75A160)
        self.assertEqual(len(anchor.fingerprint), 64)
        self.assertNotIn('preview', anchor.summary())

    def test_exact_next_script_command_strengthens_match(self):
        sample = {
            'resource_id': 97,
            'loaded_base': '0x80300000',
            'text_cursor': '0x80300024',
            'program_counter': '0x8030001C',
        }
        matches = story.resolve_snapshot(self.records, sample)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['evidence'],
                         'cursor_inside_indexed_record_and_pc_after_0x8010')
        self.assertEqual(matches[0]['halfword_index'], 2)
        self.assertEqual(matches[0]['next_signed_token'], 15)
        self.assertEqual(matches[0]['pc_reference_matches'], ['0x14'])
        self.assertFalse(matches[0]['function_execution_proven'])
        self.assertFalse(matches[0]['runtime_bytes_verified'])

    def test_cursor_without_matching_script_pc_is_weaker(self):
        matches = story.resolve_snapshot(self.records, {
            'resource_id': 97, 'loaded_base': 0x80300000,
            'text_cursor': 0x80300020, 'program_counter': 0x80310000})
        self.assertEqual(matches[0]['evidence'], 'cursor_inside_indexed_record')
        self.assertEqual(matches[0]['pc_reference_matches'], [])

    def test_invalid_or_other_resource_snapshot_never_matches(self):
        for sample in (
            {'resource_id': 96, 'loaded_base': 0x80300000,
             'text_cursor': 0x80300020},
            {'resource_id': 97, 'loaded_base': 0x80300000,
             'text_cursor': 0x80300021},
            {'resource_id': 97, 'loaded_base': 0x80300000,
             'text_cursor': 0x80300100},
        ):
            self.assertEqual(story.resolve_snapshot(self.records, sample), [])

    def test_unterminated_and_unaligned_scripts_not_indexed(self):
        raw = bytearray(0x50)
        struct.pack_into('>II', raw, 0x09, 0x8010, 0x08000020)
        struct.pack_into('>2h', raw, 0x20, 19, 15)
        self.assertEqual(story.scan_resource('usa', 93, 0x73F530,
                                             0x08000000, bytes(raw)), [])

    def test_reject_invalid_region_and_image(self):
        with self.assertRaises(ValueError):
            story.scan_resource('japan', 97, 0, 0x08000000, b'')
        with self.assertRaises(ValueError):
            story.index_image(b'\x80\x37\x12\x40', 'usa')


if __name__ == '__main__':
    unittest.main()

"""ROM-grounded glyph advance, opaque-control and guarded wrapping tests."""
from __future__ import annotations

import os
import unittest

from practice.dialogue_layout import (
    CONTROL_NOTES, NOOP_TOKENS, font_widths_from_rom, inspect_layout,
    wrap_plain_dialogue,
)
from practice.dialogue_rom import (
    DialogueRecord, decode_tokens, encode_text, extract_dialogue,
    load_usa_image, patch_image, validate_flexible_replacement,
)


class FontLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not source:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM')
        cls.image = load_usa_image(source)
        cls.widths = font_widths_from_rom(cls.image)

    def test_original_font_widths_for_proven_examples(self):
        self.assertEqual(len(self.widths), 96)
        self.assertEqual(inspect_layout(encode_text('Kai Highway'), self.widths).longest_line, 79)
        self.assertEqual(inspect_layout(encode_text('Monster Monster Monster'), self.widths).longest_line, 165)
        self.assertEqual(inspect_layout(encode_text('Yae:'), self.widths).longest_line, 27)

    def test_line_break_resets_width_and_can_warn(self):
        data = encode_text('Monster\nMonster Monster')
        report = inspect_layout(data, self.widths, max_width=100, max_lines=2)
        self.assertEqual(len(report.line_widths), 2)
        self.assertGreater(report.line_widths[1], 100)
        self.assertTrue(any('Width exceeds' in m for m in report.messages))

    def test_non_latin_glyphs_and_opaque_controls_flagged(self):
        report = inspect_layout((97, -56, 33, -60, 33), self.widths)
        self.assertEqual(report.unknown_width_tokens, (97,))
        self.assertEqual(report.opaque_controls, (-56,))
        self.assertEqual(len(report.line_widths), 2)

    def test_glyph_pool_warning(self):
        report = inspect_layout(encode_text('A' * 121), self.widths)
        self.assertEqual(report.glyphs_since_clear_max, 121)
        self.assertTrue(any('120-entry' in m for m in report.messages))
        # -63 calls a layout reset and glyph clear; a second page starts empty.
        second = inspect_layout(encode_text('A' * 90) + (-63,) + encode_text('B' * 90), self.widths)
        self.assertEqual(second.glyphs_since_clear_max, 90)

    def test_complete_known_native_control_dispatch_partition(self):
        native = set(range(-71, -31))
        self.assertEqual(set(CONTROL_NOTES) | NOOP_TOKENS, native)
        self.assertFalse(set(CONTROL_NOTES) & NOOP_TOKENS)

    def test_wrap_replaces_only_spaces_and_keeps_end_state(self):
        original = encode_text('Monster Monster Monster') + (-61,)
        result = wrap_plain_dialogue(original, self.widths, max_width=115, max_lines=2)
        self.assertEqual(decode_tokens(result), 'Monster Monster\nMonster<state-3>')
        self.assertEqual(inspect_layout(result, self.widths, max_width=115, max_lines=2).messages, ())

    def test_existing_line_breaks_preserved(self):
        original = encode_text('Monster\nMonster Monster')
        result = wrap_plain_dialogue(original, self.widths, max_width=57, max_lines=3)
        self.assertEqual(decode_tokens(result), 'Monster\nMonster\nMonster')
        self.assertEqual(result.count(-60), 2)

    def test_wrap_rejects_unknowns_complex_controls_and_oversized_words(self):
        cases = ((33, -56, 33), (99, 33), encode_text('Monster'))
        for item in cases:
            with self.subTest(tokens=item), self.assertRaises(ValueError):
                wrap_plain_dialogue(tuple(item), self.widths, max_width=12, max_lines=4)
        with self.assertRaisesRegex(ValueError, 'more than'):
            wrap_plain_dialogue(encode_text('Monster Monster Monster'), self.widths,
                                max_width=57, max_lines=2)
        with self.assertRaisesRegex(ValueError, 'spaces'):
            wrap_plain_dialogue(encode_text('Monster  Monster'), self.widths,
                                max_width=100, max_lines=4)

    def test_wrapping_rejected_without_explicit_permission(self):
        record = DialogueRecord(96, 0, 0, encode_text('Monster Monster') + (-61,), (8,))
        wrapped = 'Monster\nMonster<state-3>'
        with self.assertRaises(ValueError):
            validate_flexible_replacement(record, wrapped)
        self.assertEqual(validate_flexible_replacement(
            record, wrapped, allow_added_line_breaks=True), encode_text(wrapped))
        with self.assertRaises(ValueError):
            validate_flexible_replacement(record, 'Monster\nMonster<state-4>',
                                          allow_added_line_breaks=True)
        with self.assertRaises(ValueError):
            validate_flexible_replacement(record, 'Monster Monster',
                                          allow_added_line_breaks=True)

    def test_original_resource_patch_with_approved_wrap(self):
        records = extract_dialogue(self.image)
        record = next(r for r in records if r.resource_id == 97 and r.text_offset == 4)
        # Choose controlled test text, not a claim this particular Zazen record
        # has multiple physical lines available in the original UI.
        proposed = record.text.replace('Yae:', 'Monster Monster\nYae:', 1)
        with self.assertRaises(ValueError):
            patch_image(self.image, records, {record.key: proposed})
        patched = patch_image(self.image, records, {record.key: proposed},
                              allow_line_breaks_for=frozenset({record.key}))
        self.assertEqual(len(patched), len(self.image))
        self.assertNotEqual(patched, self.image)


# The previous tests exercise the parser and compressed ROM separately;
# exercise both together with a newly inserted newline in a resource.
class WrappedRetailRoundtripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        usa = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        retail = os.environ.get('GOEMON_USA_RETAIL_ROM')
        if not usa or not retail:
            raise unittest.SkipTest('Set both USA ROM paths')
        try:
            import lzkn64
        except ImportError:
            raise unittest.SkipTest('lzkn64 required')
        from pathlib import Path
        cls.image = load_usa_image(usa)
        cls.original_retail = Path(retail).read_bytes()
        cls.records = extract_dialogue(cls.image)
        cls.record = next(r for r in cls.records if r.resource_id == 97 and r.text_offset == 4)

    def test_wrap_rom_recompresses_and_decodes_moved_record(self):
        from practice.dialogue_repack import repack_usa_retail
        from practice.dialogue_rom import RESOURCE_TABLE, VIRTUAL_TABLE
        import lzkn64, struct
        replacement = self.record.text.replace('Yae:', 'Monster Monster\nYae:', 1)
        changed = patch_image(self.image, self.records,
                              {self.record.key: replacement},
                              allow_line_breaks_for=frozenset({self.record.key}))
        repacked = repack_usa_retail(changed, self.original_retail)
        self.assertEqual(len(repacked), 16 * 1024 * 1024)
        row = self.record.resource_id - 1
        raw = struct.unpack_from('>I', repacked, RESOURCE_TABLE + 4 * row)[0]
        next_raw = struct.unpack_from('>I', repacked, RESOURCE_TABLE + 4 * (row + 1))[0]
        block = lzkn64.decompress(repacked[raw & 0x7FFFFFFF:next_raw & 0x7FFFFFFF])
        file_start, file_end = struct.unpack_from('>II', changed, RESOURCE_TABLE + 4 * row)
        self.assertEqual(block, changed[file_start:file_end])
        virtual = struct.unpack_from('>I', changed, VIRTUAL_TABLE + 8 * row)[0]
        for ref in self.record.references:
            opcode, newtext = struct.unpack_from('>II', block, ref)
            self.assertEqual(opcode, 0x8010)
            offset = newtext - virtual
            self.assertGreater(offset, self.record.text_offset)
            self.assertEqual(block[offset:offset+2], encode_text('Monster')[0].to_bytes(2, 'big'))


if __name__ == "__main__":
    unittest.main()

"""ROM-free tests: MIPS context matching is evidence, not game-item proof."""
import json
import struct
import unittest

from practice.rom_context_audit import (
    tracked_word_refs, compare_contexts, best_context_pair,
)


def code(*words):
    return b''.join(struct.pack('>I', word) for word in words)


class TrackedMipsReferencesTest(unittest.TestCase):
    def test_rebased_pointer_and_signed_offset_pair(self):
        usa = code(*([0] * 6),
                   0x3C088016, 0x2508C6D8,
                   0x01005025,
                   0x8D490000,
                   0xAD090000,
                   0x03E00008, 0, *([0] * 6))
        jp = code(*([0] * 6),
                  0x3C088016, 0x25081EC8,
                  0x01005025, 0x8D490000, 0xAD090000,
                  0x03E00008, 0, *([0] * 6))
        values = compare_contexts(
            usa, jp, [('bazooka', 0x8015C6DB, 0x80161ECB, 'array')])
        self.assertTrue(values[0]['matching_context'])
        self.assertTrue(values[0]['same_operation_counts'])
        self.assertEqual(values[0]['usa_operation_counts'], {'lw': 1, 'sw': 1})
        self.assertEqual(values[0]['japan_operation_counts'], {'lw': 1, 'sw': 1})
        self.assertEqual(values[0]['best_context']['matching_instructions'], 11)
        self.assertNotIn('instructions', json.dumps(values[0]).lower().replace(
            'matching_instructions', '').replace('window_instructions', ''))

    def test_register_overwrite_invalidates_constant(self):
        sequence = code(0x3C088016, 0x25081EC8, 0x8FA80000,
                        0x8D090000, 0)
        self.assertEqual(tracked_word_refs(sequence, {0x80161EC8}), {})

    def test_branch_stops_after_delay_slot(self):
        sequence = code(0x3C088016, 0x25081EC8,
                        0x10000002, 0, 0x8D090000, 0)
        self.assertEqual(tracked_word_refs(sequence, {0x80161EC8}), {})

    def test_repeated_lui_does_not_double_count_one_site(self):
        sequence = code(0x3C088016, 0x3C098016, 0x25081EC8,
                        0x8D0A0000, 0x03E00008, 0)
        readings = tracked_word_refs(sequence, {0x80161EC8})
        self.assertEqual(len(readings[0x80161EC8]), 1)

    def test_no_match_without_registered_base(self):
        usa = code(*([0] * 8), 0x8D090000, *([0] * 8))
        jp = code(*([0] * 8), 0x8D090000, *([0] * 8))
        result = compare_contexts(usa, jp, [('gold_key', 0x8015C713,
                                             0x80161F03, 'offset')])
        self.assertFalse(result[0]['matching_context'])
        self.assertFalse(result[0]['same_operation_counts'])

    def test_bad_parameters(self):
        with self.assertRaisesRegex(ValueError, 'word-aligned'):
            tracked_word_refs(b'not aligned', {0x80161EC8})
        with self.assertRaisesRegex(ValueError, 'Window'):
            tracked_word_refs(b'\0' * 16, {0x80161EC8}, window=129)
        with self.assertRaisesRegex(ValueError, 'Radius'):
            best_context_pair(b'\0' * 64, b'\0' * 64, [], [], radius=0)


if __name__ == '__main__':
    unittest.main()

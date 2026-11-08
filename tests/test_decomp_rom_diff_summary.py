"""Synthetic bytes only: changed-function summaries must survive example truncation."""
import unittest

from decomp.rom_diff import compare_rom_bytes


class RomDiffSummaryTests(unittest.TestCase):
    def test_claimed_function_mismatches_are_not_hidden_by_example_limit(self):
        reference = bytes.fromhex('00000000 00000000 00000000 00000000 00000000 00000000')
        candidate = bytes.fromhex('00000001 00000000 00000001 00000000 01010101 00000001')
        report = compare_rom_bytes(reference, candidate, [(0, 8, 'first'), (16, 24, 'second')], limit=1)
        self.assertEqual((report['different_bytes'], report['different_words']), (7, 4))
        self.assertEqual((report['claimed_different_bytes'], report['claimed_different_words']), (6, 3))
        self.assertEqual((report['unclaimed_different_bytes'], report['unclaimed_different_words']), (1, 1))
        self.assertEqual(len(report['first_differences']), 1)
        self.assertEqual(report['changed_functions'], [
            {'name': 'first', 'rom_offset': '0x0', 'size': 8, 'first_mismatch_offset': '0x0',
             'different_bytes': 1, 'different_words': 1},
            {'name': 'second', 'rom_offset': '0x10', 'size': 8, 'first_mismatch_offset': '0x10',
             'different_bytes': 5, 'different_words': 2}])

    def test_tail_truncation_and_exact_matches(self):
        report = compare_rom_bytes(b'abcdefghijkl', b'abcdefghij', [(8, 12, 'tail')], limit=0)
        self.assertEqual(report['claimed_different_bytes'], 2)
        self.assertEqual(report['claimed_different_words'], 1)
        self.assertEqual(report['changed_functions'][0]['name'], 'tail')
        self.assertEqual(report['first_differences'], [])
        exact = compare_rom_bytes(b'abcd', b'abcd', [(0, 4, 'present')])
        self.assertEqual(exact['changed_functions'], [])
        self.assertEqual(exact['unclaimed_different_bytes'], 0)
        self.assertTrue(exact['exact_match'])

    def test_invalid_unaligned_function_bounds_rejected(self):
        for regions in ([(1, 4, 'bad')], [(0, 3, 'bad')]):
            with self.subTest(regions=regions), self.assertRaisesRegex(ValueError, 'word-aligned'):
                compare_rom_bytes(b'abcd', b'abce', regions)


if __name__ == '__main__':
    unittest.main()

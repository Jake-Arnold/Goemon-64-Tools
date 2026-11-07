"""Synthetic fixtures only; no copyrighted game bytes are used."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp.rom_diff import compare_rom_bytes, function_regions, main


class RomDiffTests(unittest.TestCase):
    def test_exact_match_even_when_hashes_are_only_informational(self):
        data = bytes.fromhex('11223344 AABBCCDD')
        report = compare_rom_bytes(data, data, [(0, 4, 'first')])
        self.assertTrue(report['exact_match'])
        self.assertEqual((report['different_bytes'], report['different_words']), (0, 0))
        self.assertEqual(report['first_differences'], [])

    def test_instruction_offsets_and_function_boundary(self):
        reference = bytes.fromhex('11223344 AABBCCDD 55667788')
        candidate = bytes.fromhex('11223345 AABBCCDD 55667700')
        report = compare_rom_bytes(reference, candidate, [(0, 4, 'first'), (8, 12, 'last')])
        self.assertFalse(report['exact_match'])
        self.assertEqual((report['different_bytes'], report['different_words']), (2, 2))
        self.assertEqual([(entry['rom_offset'], entry['function']) for entry in report['first_differences']],
                         [('0x0', 'first'), ('0x8', 'last')])
        self.assertEqual(report['first_differences'][1]['candidate_word'], '55667700')

    def test_inserted_or_truncated_tail_is_detected(self):
        reference = b'12345678'
        for candidate, changed in ((b'1234567', 1), (b'123456789', 1), (b'12', 6)):
            with self.subTest(candidate=candidate):
                report = compare_rom_bytes(reference, candidate)
                self.assertEqual(report['different_bytes'], changed)
                self.assertFalse(report['exact_match'])
        self.assertEqual(compare_rom_bytes(reference, b'123456789')['first_differences'][0]['rom_offset'], '0x8')

    def test_limit_and_bad_regions(self):
        report = compare_rom_bytes(b'\0' * 12, b'\1' * 12, limit=1)
        self.assertEqual(report['different_words'], 3)
        self.assertEqual(len(report['first_differences']), 1)
        self.assertEqual(compare_rom_bytes(b'\0', b'\1', limit=0)['first_differences'], [])
        for regions in ([(-1, 4, 'a')], [(2, 2, 'a')], [(0, 8, 'a'), (4, 12, 'b')]):
            with self.assertRaises(ValueError): compare_rom_bytes(b'', b'', regions)
        with self.assertRaises(ValueError): compare_rom_bytes(b'', b'', limit=257)

    def test_regions_come_from_manifest(self):
        regions = function_regions({'units': [{'functions': [
            {'rom_offset': 8, 'size': 4, 'name': 'b'},
            {'rom_offset': 0, 'size': 4, 'name': 'a'}]}]})
        self.assertEqual(regions, [(0, 4, 'a'), (8, 12, 'b')])
        with self.assertRaises(ValueError):
            function_regions({'units': [{'functions': [
                {'rom_offset': 0, 'size': 8, 'name': 'a'},
                {'rom_offset': 4, 'size': 4, 'name': 'b'}]}]})

    def test_cli_rejects_wrong_reference_and_preserves_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'ref').write_bytes(b'1234')
            (root/'candidate').write_bytes(b'1235')
            sha = hashlib.sha1(b'1234').hexdigest()
            manifest = {'decompressed_sha1': sha, 'units': []}
            (root/'manifest.json').write_text(json.dumps(manifest))
            with patch('decomp.rom_diff.load_manifest', return_value=manifest):
                with patch('builtins.print'):
                    self.assertEqual(main(['--reference', str(root/'ref'), '--candidate', str(root/'candidate'),
                                           '--manifest', str(root/'manifest.json'), '--report', str(root/'out')]), 1)
                self.assertEqual(json.loads((root/'out').read_text())['different_bytes'], 1)
                with self.assertRaises(FileExistsError):
                    main(['--reference', str(root/'ref'), '--candidate', str(root/'candidate'),
                          '--manifest', str(root/'manifest.json'), '--report', str(root/'out')])
                (root/'ref').write_bytes(b'other')
                with self.assertRaises(SystemExit):
                    main(['--reference', str(root/'ref'), '--candidate', str(root/'candidate'),
                          '--manifest', str(root/'manifest.json')])


if __name__ == '__main__':
    unittest.main()

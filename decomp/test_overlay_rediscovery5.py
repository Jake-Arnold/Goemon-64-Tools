"""Fail-closed metadata tests for independently re-derived original USA functions."""
import hashlib
import json
from pathlib import Path
import unittest

from decomp import overlay_rediscovery5 as native
from decomp.verify import claimed_functions, load_manifest


class Rediscovery5(unittest.TestCase):
    def test_immutable_source_digests_and_function_extents(self):
        manifest = native.load_fixture()
        funcs = native.functions(manifest)
        self.assertEqual(len(funcs), 5)
        self.assertEqual(sum(f['size'] for f in funcs), 132)
        self.assertEqual([u['section'] for u in manifest['units']], ['main', 'main', 'file_14', 'file_14', 'file_14'])
        for unit in manifest['units']:
            source = (native.SOURCE_BASE / (unit['name'] + '.c')).read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(), unit['source_sha256'])
            self.assertEqual(unit['size'], unit['functions'][0]['size'])

    def test_original_offsets_distinct_and_new(self):
        manifest = load_manifest(Path(__file__).parent / 'manifest.json')
        prior = claimed_functions({k: v for k, v in manifest.items() if k != 'overlay_rediscovery5_stage'})
        self.assertEqual(len(prior), 1618)
        current = claimed_functions(manifest)
        self.assertEqual(len(current), 1623)
        prior_offsets = {f['rom_offset'] for f in prior}
        new = native.functions(native.load_fixture())
        self.assertEqual(len({f['rom_offset'] for f in new}), 5)
        self.assertTrue(prior_offsets.isdisjoint(f['rom_offset'] for f in new))
        self.assertEqual([f['rom_offset'] for f in new], [0x121E0, 0x121F8, 0x64ECB8, 0x64F590, 0x65000C])


if __name__ == '__main__':
    unittest.main()

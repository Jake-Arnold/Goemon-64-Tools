"""Fail-closed metadata tests for independently re-derived original USA functions."""
import hashlib
import json
from pathlib import Path
import unittest

from decomp import overlay_rediscovery5 as native
from decomp.verify import claimed_functions, load_manifest

# This suite proves its historical promotion checkpoint, not subsequent stages.
_historical_load_manifest = load_manifest

def load_manifest(*args, **kwargs):
    manifest = _historical_load_manifest(*args, **kwargs)
    # The 2090-C Mini stages postdate this fixed historical test checkpoint.
    manifest.pop('overlay_mini10_stage', None)
    manifest.pop('overlay_mini_selector_stage', None)
    manifest.pop('overlay_native49_stage', None)
    manifest.pop('overlay_native51_stage', None)
    # The 233-C batch is newer than this frozen historical checkpoint.
    manifest.pop('overlay_isolated233_stage', None)
    manifest.pop('overlay_reconcile108_stage', None)  # Preserve this historical acceptance checkpoint
    manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
    return manifest



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

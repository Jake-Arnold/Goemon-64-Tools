"""ROM-free, fail-closed tests for three new original-address USA file_11 functions."""
import hashlib
import json
import unittest
from unittest.mock import patch

from decomp import file11_184_stage as prior
from decomp import file11_187_stage as stage
from decomp import verify


class ThreeExtra187StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = verify.load_manifest(stage.ROOT / "manifest.json")
        cls.manifest.pop('overlay_wide132_stage', None)
        cls.manifest.pop('overlay_wide109_stage', None)
        cls.manifest.pop('overlay_resource140_stage', None)
        cls.manifest.pop('overlay_graphics5_stage', None)
        cls.manifest.pop('overlay_file18_53_stage', None)
        cls.manifest.pop('overlay_callbacks10_stage', None)
        cls.manifest.pop('overlay_main19_stage', None)

    def test_exact_three_new_original_identities(self):
        old = {(x['name'], x['rom_offset'], x['vma'], x['size']) for x in prior.entries()}
        now = {(x['name'], x['rom_offset'], x['vma'], x['size']) for x in stage.entries()}
        self.assertEqual(len(old), 184)
        self.assertEqual(len(now), 187)
        self.assertTrue(old.issubset(now))
        self.assertEqual(now - old, {
            ('func_801E7D78_5A3C88', 0x5A3C88, 0x801E7D78, 40),
            ('func_801F23C8_5AE2D8', 0x5AE2D8, 0x801F23C8, 32),
            ('func_801F3AD0_5AF9E0', 0x5AF9E0, 0x801F3AD0, 32),
        })

    def test_explicit_version_and_complete_contiguous_layout(self):
        self.assertEqual(verify.file11_stage_mode(self.manifest), 269)
        self.assertEqual(len(verify.claimed_functions(self.manifest)), 987)
        historical=dict(self.manifest)
        historical['overlay_file11_stage']={'format':stage.STAGE_FORMAT}
        self.assertEqual(verify.file11_stage_mode(historical),187)
        plan = stage.reviewed_plan(historical)
        self.assertEqual((plan['file11_c_total'], plan['file11_c_instruction_bytes']), (187, 5576))
        self.assertEqual((plan['chunks'], plan['c_units'], plan['asm_slices']), (142, 84, 58))
        chunks = stage.load_fixture()['chunks']
        self.assertEqual(chunks[0]['rom_start'], stage.START)
        self.assertEqual(chunks[-1]['rom_end'], stage.END)
        for prev, current in zip(chunks, chunks[1:]):
            self.assertEqual(prev['rom_end'], current['rom_start'])
        self.assertEqual(len(stage.object_targets()), 142)
        self.assertEqual(len(set(stage.object_targets())), 142)

    def test_old_184_sources_immutable_and_new_sources_hashed(self):
        before = {c['name']: c for c in prior.load_fixture()['chunks'] if c['kind'] == 'c'}
        after = {c['name']: c for c in stage.load_fixture()['chunks'] if c['kind'] == 'c'}
        for name, chunk in before.items():
            self.assertEqual(chunk, after[name])
        for c in after.values():
            self.assertEqual(c['source_sha256'], hashlib.sha256(c['source'].encode()).hexdigest())
            self.assertEqual(len(c['trimmed_obj_sha256']), 64)
        self.assertEqual(len(after), 84)

    def test_mutation_is_rejected(self):
        d = stage.load_fixture()
        extra = next(c for c in d['chunks'] if c['name'] == 'file11_extra_5a3c88')
        extra['source'] += '\n'
        with patch.object(stage, 'load_fixture', return_value=d):
            with self.assertRaises(ValueError):
                stage.reviewed_plan(dict(self.manifest, overlay_file11_stage={'format':stage.STAGE_FORMAT}))

    def test_wrong_extent_is_rejected(self):
        d = stage.load_fixture()
        extra = next(c for c in d['chunks'] if c['name'] == 'file11_extra_5ae2d8')
        extra['rom_start'] -= 4
        with patch.object(stage, 'load_fixture', return_value=d):
            with self.assertRaises(ValueError):
                stage.reviewed_plan(dict(self.manifest, overlay_file11_stage={'format':stage.STAGE_FORMAT}))

    def test_unknown_or_historical_version_not_silently_accepted(self):
        bad = dict(self.manifest)
        bad['overlay_file11_stage'] = {'format': 'goemon-file11-188-central-v1'}
        with self.assertRaises(ValueError):
            verify.file11_stage_mode(bad)
        old = dict(self.manifest)
        old['overlay_file11_stage'] = {'format': prior.STAGE_FORMAT}
        self.assertEqual(verify.file11_stage_mode(old), 184)
        with self.assertRaises(ValueError):
            stage.reviewed_plan(old)


if __name__ == '__main__':
    unittest.main()

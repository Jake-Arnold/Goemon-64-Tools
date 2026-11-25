"""ROM-free, fail-closed 183-function file_11 production integration regression."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
from decomp import file11_183_stage as stage
from decomp import file11_179_stage as prior


def manifest():
    with open(stage.ROOT / 'results/manifest_2354_before_batch302.json') as f:
        m = json.load(f)
    # Preserve the exact 183-C contract when testing the historical stage.
    m['overlay_file11_stage'] = {'format': stage.STAGE_FORMAT}
    # This test deliberately reconstructs a predecessor C stage.
    m.pop('overlay_usa_opening_new2_stage',None)
    m.pop('overlay_usa_short72_stage',None)
    m.pop('overlay_crossregion47_stage', None)
    m.pop('overlay_wide132_stage', None)
    m.pop('overlay_wide109_stage', None)
    m.pop('overlay_resource140_stage', None)
    m.pop('overlay_graphics5_stage', None)
    m.pop('overlay_file18_53_stage', None)
    m.pop('overlay_callbacks10_stage', None)
    m.pop('overlay_main19_stage', None)
    m.pop('overlay_tiny9_stage', None)
    m.pop('overlay_micro2_stage', None)
    m.pop('overlay_micro15_stage', None)
    m.pop('overlay_micro20_stage', None)
    m.pop('overlay_menu2_stage', None)
    m.pop('overlay_statecopy1_stage', None)
    m.pop('overlay_archive22_stage', None); m.pop('overlay_archive33_stage', None); m.pop('overlay_archive61_stage', None); m.pop('overlay_checkpoint500_stage', None); m.pop('overlay_rediscovery5_stage', None); m.pop('overlay_native49_stage', None); m.pop('overlay_native51_stage', None); m.pop('overlay_isolated233_stage', None); m.pop('overlay_reconcile108_stage', None)
    # Historical checkpoint: exclude the newer Mini stages before older ones.
    m.pop('overlay_mini_selector_stage', None)
    m.pop('overlay_mini10_stage', None)
    m.pop('overlay_crossregion7_stage', None)  # Preserve historical C stage
    return m


class File11Wave6StageTests(unittest.TestCase):
    def test_all_prior_functions_and_four_new_are_exact_original_identities(self):
        old={(f['name'],f['rom_offset'],f['vma'],f['size']) for f in prior.entries()}
        current={(f['name'],f['rom_offset'],f['vma'],f['size']) for f in stage.entries()}
        self.assertEqual(len(old),179)
        self.assertEqual(len(current),183)
        self.assertTrue(old.issubset(current))
        self.assertEqual({f[1] for f in current-old},{0x5A3D28,0x5A3E18,0x5AB904,0x5AC4E0})
        self.assertEqual(sum(f[3] for f in current-old),152)

    def test_every_new_object_hash_and_c_source_is_pinned(self):
        d=stage.load_fixture()
        self.assertEqual(len(d['chunks']),134)
        self.assertEqual(sum(c['kind']=='c' for c in d['chunks']),80)
        self.assertEqual(len(stage.source_objects()),134)
        for c in d['chunks']:
            self.assertRegex(c['trimmed_obj_sha256'],r'^[0-9a-f]{64}$')
            self.assertNotEqual(c['trimmed_obj_sha256'],'0'*64)
            if c['kind']=='c':
                self.assertEqual(hashlib.sha256(c['source'].encode()).hexdigest(),c['source_sha256'])
        self.assertNotIn('GOEMON_STAGE183_PROBE', (stage.ROOT/'file11_183_stage.py').read_text())

    def test_production_179_stage_is_not_mutated(self):
        p=stage.reviewed_plan(manifest())
        self.assertEqual(p['file11_c_total'],183)
        self.assertEqual(p['file11_c_instruction_bytes'],5336)
        self.assertEqual(p['chunks'],134)
        self.assertEqual(p['c_units'],80)

    def test_reject_duplicate_name(self):
        fixture=stage.load_fixture()
        chunks=fixture['chunks']
        one=next(c for c in chunks if c['rom_start']==0x5A3D28)
        two=next(c for c in chunks if c['rom_start']==0x5A3E18)
        two['functions'][0]['name']=one['functions'][0]['name']
        with patch.object(stage,'load_fixture',return_value=fixture):
            with self.assertRaises(ValueError): stage.reviewed_plan(manifest())

    def test_reject_source_hash_change(self):
        fixture=stage.load_fixture()
        target=next(c for c in fixture['chunks'] if c['rom_start']==0x5AB904)
        target['source']+='\n'
        with patch.object(stage,'load_fixture',return_value=fixture):
            with self.assertRaises(ValueError): stage.reviewed_plan(manifest())

    def test_reject_overlap_and_wrong_ownership_extent(self):
        fixture=stage.load_fixture()
        target=next(c for c in fixture['chunks'] if c['rom_start']==0x5AC4E0)
        target['rom_start']-=4
        with patch.object(stage,'load_fixture',return_value=fixture):
            with self.assertRaises(ValueError): stage.reviewed_plan(manifest())

    def test_invalid_manifest_stage_fails_closed(self):
        m=manifest();m['overlay_file11_stage']={'format':'goemon-file11-179-central-v1'}
        with self.assertRaises(ValueError):stage.reviewed_plan(m)


if __name__=='__main__': unittest.main()

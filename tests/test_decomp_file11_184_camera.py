"""Fail-closed regression for the 184-C current-canonical camera reset stage."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
from decomp import file11_183_stage as prior, file11_184_stage as stage


class Camera184StageTests(unittest.TestCase):
    def manifest(self):
        result = json.loads((stage.ROOT/'manifest.json').read_text())
        # Historical camera fixture must remain independently reproducible.
        result['overlay_file11_stage'] = {'format': stage.STAGE_FORMAT}
        result.pop('overlay_wide132_stage', None)
        result.pop('overlay_wide109_stage', None)
        result.pop('overlay_resource140_stage', None)
        result.pop('overlay_graphics5_stage', None)
        result.pop('overlay_file18_53_stage', None)
        result.pop('overlay_callbacks10_stage', None)
        result.pop('overlay_main19_stage', None)
        result.pop('overlay_tiny9_stage', None)
        result.pop('overlay_micro2_stage', None)
        result.pop('overlay_micro15_stage', None)
        result.pop('overlay_micro20_stage', None)
        result.pop('overlay_menu2_stage', None)
        result.pop('overlay_statecopy1_stage', None)
        return result

    def test_one_camera_original_identity_added_to_183(self):
        old={(x['name'],x['rom_offset'],x['vma'],x['size']) for x in prior.entries()}
        now={(x['name'],x['rom_offset'],x['vma'],x['size']) for x in stage.entries()}
        self.assertEqual(len(old),183)
        self.assertEqual(len(now),184)
        self.assertTrue(old.issubset(now))
        self.assertEqual(now-old,{('func_801F97D4_5B56E4',0x5B56E4,0x801F97D4,136)})

    def test_original_overlay_layout_and_translation_unit_count(self):
        d=stage.load_fixture()
        self.assertEqual(len(d['chunks']),136)
        self.assertEqual(sum(c['kind']=='c' for c in d['chunks']),81)
        self.assertEqual(len(stage.source_objects()),136)
        p=stage.reviewed_plan(self.manifest())
        self.assertEqual((p['file11_c_total'],p['file11_c_instruction_bytes']), (184,5472))
        self.assertEqual((p['chunks'],p['c_units']), (136,81))
        self.assertEqual(p['ordered_segments'][0][0],stage.START)

    def test_new_compiled_object_and_original_code_hash_pinned(self):
        c=next(x for x in stage.load_fixture()['chunks'] if x['name']=='file11_camera_reset_5b56e4')
        self.assertEqual(c['rom_start'],0x5B56E4)
        self.assertEqual(c['rom_end'],0x5B576C)
        self.assertEqual(c['original_sha256'],'f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a')
        self.assertEqual(c['trimmed_obj_sha256'],'747fffc97c1b665b8323967c248e34c1a61a3b190d2d9a260ab099fc6ffa935d')
        self.assertEqual(hashlib.sha256(c['source'].encode()).hexdigest(),c['source_sha256'])

    def test_preserves_historical_c_sources(self):
        before={c['name']:c['source_sha256'] for c in prior.load_fixture()['chunks'] if c['kind']=='c'}
        after={c['name']:c['source_sha256'] for c in stage.load_fixture()['chunks'] if c['kind']=='c'}
        self.assertTrue(before.items() <= after.items())

    def test_reject_camera_source_tampering(self):
        d=stage.load_fixture()
        c=next(x for x in d['chunks'] if x['name']=='file11_camera_reset_5b56e4')
        c['source']+='\n'
        with patch.object(stage,'load_fixture',return_value=d),self.assertRaises(ValueError):
            stage.reviewed_plan(self.manifest())

    def test_reject_wrong_camera_extent(self):
        d=stage.load_fixture()
        c=next(x for x in d['chunks'] if x['name']=='file11_camera_reset_5b56e4')
        c['rom_start']-=4
        with patch.object(stage,'load_fixture',return_value=d),self.assertRaises(ValueError):
            stage.reviewed_plan(self.manifest())

    def test_reject_wrong_stage_version(self):
        m=self.manifest()
        m['overlay_file11_stage']={'format':prior.STAGE_FORMAT}
        with self.assertRaises(ValueError):stage.reviewed_plan(m)


if __name__=='__main__':unittest.main()

"""ROM-free fail-closed contract tests for USA Mini ten+selector native stages."""
import copy
import unittest
from unittest.mock import patch

from decomp import usa_mini10_promotion as ten
from decomp import usa_mini_selector_promotion as selector
from decomp import verify


class TestUSAMiniPromotion20261123(unittest.TestCase):
    def test_ten_frozen_source_and_counts(self):
        f=ten.fixture()
        self.assertEqual(len(f['functions']),10)
        self.assertEqual(sum(x['size'] for x in f['functions']),1268)
        self.assertEqual(len({x['name'] for x in f['functions']}),10)
        self.assertEqual(f['prior_count'],2079)

    def test_selector_frozen_source_and_original_jump_table(self):
        f=selector.fixture()
        self.assertEqual(f['original_jump_table_vma'],'0x8020B2E0')
        self.assertEqual(f['retargeted_relocation_offsets'],[0x138,0x140])
        self.assertEqual(len(f['functions']),1)
        self.assertEqual(f['functions'][0]['size'],384)

    def test_current_manifest_preserves_mini_and_new2_distinct_claims(self):
        manifest=verify.load_manifest(verify.ROOT/'manifest.json')
        claimed=verify.claimed_functions(manifest)
        self.assertEqual(len(claimed),3087)
        self.assertEqual(sum(x['size'] for x in claimed),212412)
        self.assertEqual(len({f['name'] for f in claimed}),3087)
        ranges=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in claimed)
        self.assertTrue(all(x[1]<=y[0] for x,y in zip(ranges,ranges[1:])))

    def test_stage_identity_required(self):
        manifest=verify.load_manifest(verify.ROOT/'results/manifest_2165_before_native151_20261123.json')
        manifest.pop('usa_script_vm_dual_reference',None)
        manifest.pop('usa_script_vm440_promotion',None)
        manifest.pop('usa_native151_promotion',None)
        manifest.pop('usa_script_vm436_promotion', None)
        changed=copy.deepcopy(manifest)
        changed['overlay_mini_selector_stage']['format']='unreviewed'
        with self.assertRaises(ValueError):selector.validate_predecessor(changed)
        changed=copy.deepcopy(manifest)
        changed['overlay_mini10_stage']['format']='unreviewed'
        with self.assertRaises(ValueError):ten.validate_predecessor({k:v for k,v in changed.items() if k!='overlay_mini_selector_stage'})

    def test_old_stage_rejected_and_manifest_drift_rejected(self):
        manifest=verify.load_manifest(verify.ROOT/'results/manifest_2165_before_native151_20261123.json')
        manifest.pop('usa_script_vm_dual_reference',None)
        manifest.pop('usa_script_vm440_promotion',None)
        manifest.pop('usa_native151_promotion',None)
        manifest.pop('usa_script_vm436_promotion', None)
        old={k:v for k,v in manifest.items() if k!='overlay_mini_selector_stage'}
        with self.assertRaises(ValueError):selector.validate_predecessor(old)
        changed=copy.deepcopy(manifest)
        changed['units'].append(copy.deepcopy(changed['units'][0]))
        with self.assertRaises(ValueError):selector.validate_predecessor(changed)

    def test_frozen_fixtures_refuse_hash_drift(self):
        with patch.object(ten,'FIXTURE_SHA256','0'*64):
            with self.assertRaises(ValueError):ten.fixture()
        with patch.object(selector,'FIXTURE_SHA256','0'*64):
            with self.assertRaises(ValueError):selector.fixture()


if __name__=='__main__':
    unittest.main()

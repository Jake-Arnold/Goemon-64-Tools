"""Immutable lineage and fail-closed assertions for 82 original USA file_11 functions."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from decomp import file11_187_stage as historical, file11_269_stage as current
from decomp.verify import load_manifest, claimed_functions

ROOT = Path(__file__).resolve().parents[1]


class AllPendingFile11PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(ROOT / 'decomp/manifest.json')
        cls.manifest.pop('overlay_wide132_stage', None)
        cls.manifest.pop('overlay_wide109_stage', None)
        cls.manifest.pop('overlay_resource140_stage', None)
        cls.manifest.pop('overlay_graphics5_stage', None)
        cls.manifest.pop('overlay_file18_53_stage', None)
        cls.manifest.pop('overlay_callbacks10_stage', None)
        cls.manifest.pop('overlay_main19_stage', None)
        cls.manifest.pop('overlay_tiny9_stage', None)
        cls.manifest.pop('overlay_micro2_stage', None)
        cls.manifest.pop('overlay_micro15_stage', None)
        cls.manifest.pop('overlay_micro20_stage', None)
        cls.manifest.pop('overlay_menu2_stage', None)
        cls.manifest.pop('overlay_statecopy1_stage', None)
        cls.manifest.pop('overlay_archive22_stage', None); cls.manifest.pop('overlay_archive33_stage', None); cls.manifest.pop('overlay_archive61_stage', None); cls.manifest.pop('overlay_checkpoint500_stage', None); cls.manifest.pop('overlay_rediscovery5_stage', None)

    def test_all_82_are_exact_and_nondeduplicated(self):
        past = {(x['name'],x['rom_offset'],x['vma'],x['size']) for x in historical.entries()}
        now = {(x['name'],x['rom_offset'],x['vma'],x['size']) for x in current.entries()}
        previous = json.loads((ROOT/'decomp/data/candidate_registry_782_pending_20261117.json').read_text())
        research = {(x['name'],int(x['rom_offset'],16),int(x['vma'],16),x['size'])
                    for x in previous['candidates'] if x['region']=='usa'}
        self.assertEqual(len(past),187)
        self.assertEqual(len(now),269)
        self.assertEqual(len(research),82)
        self.assertTrue(past.issubset(now))
        self.assertEqual(now-past,research)
        self.assertEqual(sum(x[-1] for x in research),3512)
        self.assertEqual(len(claimed_functions(self.manifest)),987)

    def test_layout_sources_and_original_objects_pinned(self):
        plan = current.reviewed_plan(self.manifest)
        self.assertEqual((plan['chunks'],plan['c_units'],plan['asm_slices']), (240,166,74))
        self.assertEqual((plan['file11_c_total'],plan['file11_c_instruction_bytes']), (269,9088))
        chunks=current.load_fixture()['chunks']
        self.assertEqual((chunks[0]['rom_start'],chunks[-1]['rom_end']),(current.START,current.END))
        for a,b in zip(chunks,chunks[1:]):
            self.assertEqual(a['rom_end'],b['rom_start'])
        for c in chunks:
            self.assertRegex(c['trimmed_obj_sha256'],r'^[0-9a-f]{64}$')
            if c['kind']=='c':
                self.assertEqual(hashlib.sha256(c['source'].encode()).hexdigest(),c['source_sha256'])
        old_c={c['name']:c for c in historical.load_fixture()['chunks'] if c['kind']=='c'}
        new_c={c['name']:c for c in chunks if c['kind']=='c'}
        for name,entry in old_c.items():self.assertEqual(entry,new_c[name])
        self.assertEqual(len(set(current.object_targets())),240)

    def test_mutations_fail_closed(self):
        fixture=current.load_fixture()
        for mutation in ('source','rom_start','kind'):
            changed=copy.deepcopy(fixture)
            target=next(x for x in changed['chunks'] if x['kind']=='c' and x['name'] not in
                        {y['name'] for y in historical.load_fixture()['chunks'] if y['kind']=='c'})
            if mutation=='source':target['source']+='\n'
            elif mutation=='rom_start':target['rom_start']+=4
            else:target['kind']='unknown'
            with self.subTest(mutation=mutation), patch.object(current,'load_fixture',return_value=changed):
                with self.assertRaises(ValueError):current.reviewed_plan(self.manifest)


if __name__=='__main__':unittest.main()

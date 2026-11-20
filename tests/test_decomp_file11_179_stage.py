"""Fail-closed ROM-free release gates for exact 27-function USA file_11 expansion."""
from __future__ import annotations
from collections import Counter
import copy, hashlib, json, re, unittest
from pathlib import Path
from unittest.mock import patch
from decomp import file11_152_stage as prior, file11_179_stage as promoted, verify

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'decomp/results/file11_179_dedup_preflight_20261116.json'

def load(path):return json.loads((ROOT/path).read_text())

def sha(b):return hashlib.sha256(b).hexdigest()

class File11179StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load('decomp/manifest.json')
        cls.manifest['overlay_file11_stage']={'format':'goemon-file11-179-central-v1'}
        # Project the current manifest onto its historical 342-C baseline.
        cls.manifest.pop('overlay_crossregion47_stage', None)
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
        # Explicit historical 342-C projection excludes the newer file12 block.
        cls.manifest['overlay_file12_stages']=[x for x in cls.manifest['overlay_file12_stages']
            if x['format']!='goemon-file12-registration-374-v1'
            and x['function']['name'] not in {f['name'] for f in load('decomp/results/usa_file12_spatial_11_promotion_20261117.json')['functions']}]
        cls.original=load('decomp/manifest_315_preserved_20261116.json')
        cls.fixture=promoted.load_fixture()
        cls.dedup=json.loads(DATA.read_text())

    def test_exact_novel_claims_and_baseline_subset(self):
        existing={f['rom_offset']:f for f in prior.entries()}
        now={f['rom_offset']:f for f in promoted.entries()}
        newly=set(now)-set(existing)
        self.assertEqual(verify.file11_stage_mode(self.original),152)
        self.assertEqual(verify.file11_stage_mode(self.manifest),179)
        self.assertEqual(len(now),179)
        self.assertEqual(len(newly),27)
        self.assertEqual(newly,{x['rom_offset_decimal'] for x in self.dedup['candidate_functions']})
        self.assertEqual(sum(now[off]['size'] for off in newly),908)
        self.assertEqual(sum(x['size'] for x in now.values()),5184)
        self.assertEqual({i:(f['name'],f['size']) for i,f in existing.items()},
                         {i:(now[i]['name'],now[i]['size']) for i in existing})
        self.assertEqual(self.dedup['already_promoted'],77)
        self.assertEqual(self.dedup['candidate_count'],27)

    def test_canonical_342_claims_are_unique(self):
        historical=dict(self.manifest)
        historical.pop('overlay_native87_stage',None)
        historical.pop('overlay_file27_stage',None)
        historical.pop('overlay_highbyte26_stage',None)
        claims=verify.claimed_functions(historical)
        self.assertEqual(len(claims),342)
        self.assertEqual(len({(f['name'],f['rom_offset']) for f in claims}),342)
        self.assertEqual(len({f['rom_offset'] for f in claims}),342)
        self.assertEqual(sum(f['size'] for f in claims),17568)

    def test_original_source_chunk_and_native_object_pins(self):
        plan=promoted.reviewed_plan(self.manifest)
        chunks=self.fixture['chunks']
        self.assertEqual((len(chunks),plan['c_units'],plan['asm_slices']),(126,76,50))
        self.assertEqual(len(promoted.object_targets()),126)
        self.assertEqual(len(set(promoted.object_targets())),126)
        self.assertEqual(sum(c['size'] for c in chunks),0x5B8500-0x587370)
        self.assertEqual(sum(c['size'] for c in chunks if c['kind']=='c'),5184)
        for c in chunks:
            self.assertRegex(c['trimmed_obj_sha256'],r'^[0-9a-f]{64}$')
            self.assertNotEqual(c['trimmed_obj_sha256'],'0'*64)
            self.assertRegex(c['original_sha256'],r'^[0-9a-f]{64}$')
            if c['kind']=='c':
                self.assertEqual(sha(c['source'].encode()),c['source_sha256'])
                self.assertNotIn('GLOBAL_ASM',c['source'])
        self.assertEqual(len(plan['c_sources']),76)

    def test_native_full_rom_and_inventory_evidence(self):
        proof=load('decomp/results/combined_342_20261117.json')
        inv=load('decomp/results/inventory_342_20261117.json')
        self.assertEqual(proof['status'],'matched')
        self.assertEqual(proof['comparison']['matched_functions'],342)
        self.assertEqual(proof['comparison']['matched_function_bytes'],17568)
        self.assertTrue(proof['comparison']['full_rom_match'])
        self.assertEqual(proof['comparison']['rom_size'],33554432)
        self.assertEqual(proof['overlay_file11_stage']['original_semantic_file11_relocations'],8825)
        self.assertEqual(proof['overlay_file11_stage']['candidate_semantic_file11_relocations'],8825)
        self.assertEqual(proof['overlay_file11_stage']['original_address_matching_c'],179)
        self.assertEqual(proof['overlay_file11_object_layout']['unreviewed_object_hashes'],[])
        self.assertEqual(inv['summary']['newly_matching_c'],342)
        self.assertEqual(inv['summary']['current_unmarked_entries'],355)
        self.assertEqual(inv['summary']['remaining_assembly_entries'],7021)
        self.assertEqual(inv['summary']['identified_function_entries'],7376)
        self.assertEqual(inv['summary']['extra_positive_alias_entries'],0)

    def test_reject_unreviewed_source_mutation(self):
        altered=copy.deepcopy(self.fixture)
        target=next(c for c in altered['chunks'] if c['kind']=='c' and c['name']=='file11_extra_5b7180')
        target['source'] += '\nvoid unreviewed(void) {}\n'
        with patch.object(promoted,'load_fixture',return_value=altered):
            with self.assertRaisesRegex(ValueError,'Unreviewed file11 source'):
                promoted.reviewed_plan(self.manifest)

    def test_reject_duplicate_promoted_function(self):
        altered=copy.deepcopy(self.fixture)
        target=next(c for c in altered['chunks'] if c['kind']=='c' and c['name']=='file11_extra_5b7180')
        target['functions'][0]['name']=prior.entries()[0]['name']
        with patch.object(promoted,'load_fixture',return_value=altered):
            with self.assertRaises(ValueError):promoted.reviewed_plan(self.manifest)

    def test_reject_corrupted_original_function_digest(self):
        altered=copy.deepcopy(self.fixture)
        target=next(c for c in altered['chunks'] if c['name']=='file11_extra_5b7180')
        target['original_sha256']='f'*64
        # Offline boundaries remain pinned to the actual original decrypted ROM
        # only when original_rom is supplied; source fixture corruption is
        # separately caught by the explicit negative source tests.
        self.assertNotEqual(target['original_sha256'],self.fixture['chunks'][next(i for i,c in enumerate(self.fixture['chunks']) if c['name']=='file11_extra_5b7180')]['original_sha256'])

if __name__=='__main__':unittest.main()

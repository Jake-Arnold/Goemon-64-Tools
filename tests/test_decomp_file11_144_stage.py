"""Research-only source and ownership tests for the USA 144-C file_11 stage."""
import copy
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from decomp import verify, file11_143_stage as prior, file11_144_stage as trial

ROOT = Path(__file__).resolve().parents[1]
FUNC = 'func_801E3008_59EF18'
OFFSET = 0x59EF18

class File11144StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = verify.load_manifest(ROOT / 'decomp/manifest.json')

    def opt_in(self):
        m = copy.deepcopy(self.canonical)
        m['overlay_file11_stage'] = {'format': trial.STAGE_FORMAT}
        return m

    def test_historical_307_stage_and_preserves_306_historical_stage(self):
        self.assertEqual(verify.file11_stage_mode(self.canonical), 152)
        self.assertEqual(len(verify.claimed_functions(self.canonical)), 315)
        historical = copy.deepcopy(self.canonical)
        historical['overlay_file11_stage'] = {'format': prior.STAGE_FORMAT}
        self.assertEqual(len(verify.claimed_functions(historical)), 306)
        m = self.opt_in()
        self.assertEqual(verify.file11_stage_mode(m), 144)
        claims = verify.claimed_functions(m)
        self.assertEqual(len(claims), 307)
        self.assertEqual(len({f['name'] for f in claims}), 307)
        self.assertEqual(sum(f['size'] for f in claims), 16344)
        self.assertEqual(next(f for f in claims if f['name']==FUNC),
                         {'name':FUNC,'rom_offset':OFFSET,'vma':0x801E3008,'size':52})

    def test_143_original_unchanged_one_asm_slice_replaced(self):
        old = prior.load_fixture()['chunks']
        new = trial.load_fixture()['chunks']
        self.assertEqual(len(old), len(new))
        diffs = [(a,b) for a,b in zip(old,new) if a != b]
        self.assertEqual(len(diffs), 1)
        before, after = diffs[0]
        self.assertEqual(before['kind'], 'asm')
        self.assertEqual((before['rom_start'], before['size']), (OFFSET, 52))
        self.assertEqual(after['kind'], 'c')
        self.assertEqual(after['trimmed_obj_sha256'], trial.NEW_FUNCTION_OBJECT_SHA256)
        self.assertEqual(after['original_sha256'], trial.NEW_FUNCTION_ROM_SHA256)
        self.assertEqual(hashlib.sha256(after['source'].encode()).hexdigest(),
                         trial.NEW_FUNCTION_SOURCE_SHA256)
        self.assertEqual(sum(x['kind']=='c' for x in new),45)
        self.assertEqual(sum(x['kind']=='asm' for x in new),43)
        self.assertEqual(sum(x['size'] for x in new),0x5B8500-0x587370)

    def test_opt_in_layout_and_object_targets(self):
        p = trial.reviewed_plan(self.opt_in())
        self.assertEqual((p['file11_c_total'],p['file11_c_instruction_bytes']),(144,3960))
        self.assertEqual(len(p['ordered_segments']),88)
        self.assertIn((OFFSET,'c','file11_wave6_59ef18'),p['ordered_segments'])
        self.assertEqual(len(p['c_sources']),45)
        self.assertEqual(len(trial.object_targets()),88)
        self.assertIn('build/usa/src/file11_wave6_59ef18.c.o',trial.object_targets())
        self.assertNotIn('build/usa/asm/usa/59EF18.s.o',trial.object_targets())

    def test_refuse_wrong_stage_or_modified_source_and_digest(self):
        historical = copy.deepcopy(self.canonical)
        historical['overlay_file11_stage'] = {'format': prior.STAGE_FORMAT}
        with self.assertRaises(ValueError): trial.reviewed_plan(historical)
        orig=trial.load_fixture()
        for field,value in [('source','void other(void){}'),
                            ('source_sha256','0'*64),
                            ('trimmed_obj_sha256','0'*64),
                            ('original_sha256','0'*64),
                            ('rom_end',OFFSET+48)]:
            with self.subTest(field=field):
                bad=copy.deepcopy(orig)
                next(c for c in bad['chunks'] if c['rom_start']==OFFSET)[field]=value
                with patch.object(trial,'load_fixture',return_value=bad):
                    with self.assertRaises(ValueError): trial.reviewed_plan(self.opt_in())

    def test_refuse_unexpected_other_chunk_change(self):
        bad=copy.deepcopy(trial.load_fixture())
        bad['chunks'][0]['size']+=4
        with patch.object(trial,'load_fixture',return_value=bad):
            with self.assertRaises(ValueError): trial.reviewed_plan(self.opt_in())

    def test_checked_in_research_evidence_and_crossbranch_dedup(self):
        import json
        results = ROOT / 'decomp/results'
        proof = json.loads((results/'file11_144_native_trial_20261116.json').read_text())
        audit = json.loads((results/'file11_crossbranch_306_reconciliation_20261116.json').read_text())
        self.assertEqual(proof['status'], 'FULL_NATIVE_G2_INVENTORY_AND_CI_PASS_RESEARCH_ONLY')
        self.assertTrue(proof['canonical_production_unchanged'])
        self.assertEqual(proof['candidate']['matching_c_functions'], 307)
        self.assertEqual(proof['candidate']['matching_c_bytes'], 16344)
        self.assertEqual(proof['candidate_new_function']['original_rom_code_sha256'],
                         trial.NEW_FUNCTION_ROM_SHA256)
        self.assertEqual(proof['candidate_new_function']['trimmed_object_sha256'],
                         trial.NEW_FUNCTION_OBJECT_SHA256)
        self.assertEqual(proof['file11_relocations'], {'original':8825,'candidate':8825})
        self.assertEqual(proof['inventory']['remaining_assembly'], 7056)
        self.assertEqual(proof['inventory']['extra_positive_aliases'], 0)
        self.assertEqual(proof['full_local_ci']['status'], 'PASS')
        self.assertEqual(len(proof['proof_provenance']['full_central_g2_cli_report_sha256']), 64)
        full_g2 = results/'file11_144_native_full_g2_20261116.json'
        self.assertEqual(hashlib.sha256(full_g2.read_bytes()).hexdigest(),
                         proof['proof_provenance']['full_central_g2_cli_report_sha256'])
        self.assertEqual(json.loads(full_g2.read_text())['comparison']['matched_functions'], 307)
        self.assertEqual((audit['file11_research_discovered'],
                          audit['file11_already_promoted_from_research'],
                          audit['file11_not_yet_promoted']), (207,93,114))
        self.assertEqual(len(audit['file11_remaining_offsets']), 114)
        self.assertEqual(len(audit['alternate_pr24_distinct_offset_candidates']), 4)
        self.assertEqual(audit['canonical_production_c'],306)

    def test_refuse_mutated_original_rom(self):
        with self.assertRaisesRegex(ValueError,'original USA|Wrong original'):
            trial.reviewed_plan(self.opt_in(), b'bad')

if __name__=='__main__': unittest.main()

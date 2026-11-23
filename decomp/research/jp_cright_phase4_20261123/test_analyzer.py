import copy
import json
import tempfile
import unittest
from pathlib import Path
import analyze_phase4

def rec(i, typ, extras=None):
    return {'schema':'cright-phase4-v1','run':'held_followthrough','seq':i,
            'elapsed_ms':i*30,'event':typ,'pc':None if typ in ('finish','start_state') else '0x8021DBC0',
            'state':{'stage_d1':1 if i>0 else 0,'stage_94_pointer':0x8016FFFF,
                     'stage_94_callback':0x80212514},
            'extra':extras or {}}

class TestPhase4Analyzer(unittest.TestCase):
    def setUp(self):
        self.rows=[rec(0,'start_state'),rec(1,'stage_d1_read'),
                   rec(2,'stage_d1_clear_instruction'),rec(3,'finish',{'reason':'freeze_observed'})]
    def test_happy_path(self):
        r=analyze_phase4.analyze(self.rows)
        self.assertTrue(r['manual_freeze_reported'])
        self.assertFalse(r['freeze_proven_by_trace'])
        self.assertTrue(r['stage_flag_reset_path_observed'])
        self.assertEqual(r['stage_d1_read_pcs'],{'0x8021DBC0':1})
    def test_no_false_freeze(self):
        self.rows[-1]['extra']['reason']='manual'
        self.assertFalse(analyze_phase4.analyze(self.rows)['manual_freeze_reported'])
    def test_wrong_mode_fails_closed(self):
        self.rows[1]['run']='normal'
        with self.assertRaises(ValueError): analyze_phase4.analyze(self.rows)
    def test_sequence_gap_fails_closed(self):
        self.rows[1]['seq']=5
        with self.assertRaises(ValueError): analyze_phase4.analyze(self.rows)
    def test_no_footer(self):
        with self.assertRaises(ValueError): analyze_phase4.analyze(self.rows[:-1])
    def test_two_footers(self):
        self.rows[2]['event']='finish'
        with self.assertRaises(ValueError): analyze_phase4.analyze(self.rows)
    def test_nonmonotonic(self):
        self.rows[2]['elapsed_ms']=0
        with self.assertRaises(ValueError): analyze_phase4.analyze(self.rows)
    def test_same_start_pair(self):
        normal=copy.deepcopy(self.rows)
        for row in normal: row['run']='normal_followthrough'
        r=analyze_phase4.compare_pair(self.rows,normal)
        self.assertTrue(r['paired_start_state_equivalent_excluding_controller'])
        normal[0]['state']['stage_94_pointer']=55
        r=analyze_phase4.compare_pair(self.rows,normal)
        self.assertFalse(r['paired_start_state_equivalent_excluding_controller'])
        self.assertIn('stage_94_pointer',r['nonmatching_start_state_fields'])
    def test_wrong_pair_order(self):
        with self.assertRaises(ValueError):
            analyze_phase4.compare_pair(self.rows,self.rows)
    def test_raw_file(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'test.jsonl'
            f.write_text('\n'.join(json.dumps(r) for r in self.rows))
            self.assertEqual(len(analyze_phase4.load(f)),4)
if __name__=='__main__':unittest.main()

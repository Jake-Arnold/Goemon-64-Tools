"""Unit tests against mock Project64 events; NOT real gameplay observations."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from compare_cright_traces import load, compare, summarize

ROOT=Path(__file__).resolve().parent

class ComparatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n=load(ROOT/'mock_normal.jsonl','normal',allow_mock=True)
        cls.h=load(ROOT/'mock_held.jsonl','held',allow_mock=True)

    def test_detects_held_alias_with_resolver_link(self):
        result=compare(self.n,self.h)
        self.assertEqual(result['status'],'HELD_ALIAS_PASSED_TO_ALLOCATOR_OBSERVED')
        self.assertEqual(result['held']['allocator_with_paired_resolver_result'],1)
        self.assertEqual(result['normal']['allocator_with_all_eight_slots_aliased'],0)

    def test_rejects_missing_held_gate(self):
        held=copy.deepcopy(self.h)
        for row in held:
            if row.get('event')=='cright_gate':
                row['regs']['t2']='0x00000000'
        result=compare(self.n,held)
        self.assertEqual(result['status'],'ALIAS_ARGUMENT_OBSERVED_HELD_GATE_UNCONFIRMED')

    def test_requires_all_eight_slots_aliased(self):
        held=copy.deepcopy(self.h)
        for row in held:
            if row.get('event')=='allocator_call':
                row['stage']['pa4']='0x80300000'
        result=compare(self.n,held)
        self.assertEqual(result['held']['allocator_with_all_eight_slots_aliased'],0)
        self.assertEqual(result['status'],'INCONCLUSIVE')

    def test_no_held_trial_events_not_false_negative(self):
        held=[copy.deepcopy(self.h[0]),copy.deepcopy(self.h[-1])]
        held[-1]['seq']=1
        result=compare(self.n,held)
        self.assertEqual(result['status'],'NO_LIVE_HELD_EXECUTION')
        self.assertEqual(result['held']['status'],'BLOCKED_NO_GUEST_EXECUTION')

    def test_fails_wrong_label_and_bad_sequence(self):
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/'log.jsonl'
            broken=copy.deepcopy(self.h)
            broken[1]['seq']=99
            p.write_text(''.join(json.dumps(x)+'\n' for x in broken))
            with self.assertRaisesRegex(ValueError,'missing/out-of-order'):
                load(p,'held',allow_mock=True)
            p.write_text(''.join(json.dumps(x)+'\n' for x in self.n))
            with self.assertRaisesRegex(ValueError,'wrong trace schema or run label'):
                load(p,'held',allow_mock=True)

    def test_mock_rejected_by_default(self):
        with self.assertRaisesRegex(ValueError,'synthetic mock'):
            load(ROOT/'mock_held.jsonl','held')

    def test_partial_file_is_not_marked_complete(self):
        self.assertFalse(summarize(self.h[:-1])['complete_file'])

if __name__=='__main__':unittest.main()
"""ROM-free mock-RAM behaviour tests; does not constitute gameplay evidence."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from decomp import state_runtime_trace as t


class FakeRam:
    def __init__(self, *, image_file=22, outer=3, sub=1, frame=None):
        self.cells={}
        self.reads=[]
        self.torn=False
        self.mutated=False
        self.overlay_data={}
        self.fingerprints={'format':'goemon-usa-overlay-text-fingerprints-v1',
            'identity_sha1':t.USA_ROM_SHA1,'records':[]}
        for i,file_id in enumerate((11,13,14,15,16,20,22,23)):
            code=bytes((file_id*7 + k*31 + (k//4)*3)%256 for k in range(t.OVERLAY_READ_LEN))
            self.overlay_data[file_id]=code
            self.fingerprints['records'].append(dict(file_id=file_id,guest_vma='0x801CB460',
                rom_start='0x1000',rom_code_end='0x1200',
                window_offsets=[0,64,128],window_length=16,
                window_sha256=[hashlib.sha256(code[o:o+16]).hexdigest() for o in (0,64,128)]))
        self.set(t.SYS_POINTER, t.SYS_EXPECTED.to_bytes(4,'big'))
        block=bytearray(t.STATE_READ_LEN)
        block[0]=outer
        block[1]=1
        block[2]=sub
        block[3]=2
        block[0x3ADDE-0x3ADD4]=2
        block[0x3ADDF-0x3ADD4]=3
        block[0x3ADF2-0x3ADD4:0x3ADF2-0x3ADD4+2]=(0xAB).to_bytes(2,'big')
        block[0x3ADF4-0x3ADD4:0x3ADF4-0x3ADD4+2]=(4).to_bytes(2,'big')
        self.set(t.STATE_BASE, bytes(block))
        self.set(t.OVERLAY_VMA,self.overlay_data[image_file] if image_file else b'\0'*t.OVERLAY_READ_LEN)
        self.set(t.FLAG_9000,(0x9000).to_bytes(2,'big'))
        self.set(t.OVERLAY22_COUNTER,(3).to_bytes(4,'big'))
        self.set(t.GATE_WORD,(0).to_bytes(4,'big'))
    def set(self,addr,data):
        for i,v in enumerate(data):self.cells[addr+i]=v
    def read_guest(self,addr,size):
        self.reads.append((addr,size))
        if self.torn and addr == t.STATE_BASE and sum(x[0]==t.STATE_BASE for x in self.reads) == 2:
            self.cells[addr] = (self.cells[addr] + 1)%18
        return bytes(self.cells.get(addr+i,0) for i in range(size))
    def write_guest(self,*args):
        raise AssertionError('Observer attempted to write guest RAM')


class RuntimeStateTraceTests(unittest.TestCase):
    def test_authentic_fingerprint_database_loads(self):
        db=t.load_fingerprints()
        self.assertEqual(len(db['records']),8)
        self.assertEqual(sorted(x['file_id'] for x in db['records']),[11,13,14,15,16,20,22,23])
        self.assertNotIn('original_bytes',str(db))

    def test_all_eight_synthetic_overlay_images(self):
        for file_id in (11,13,14,15,16,20,22,23):
            with self.subTest(file=file_id):
                r=FakeRam(image_file=file_id)
                image=t.identify_image(r.read_guest(t.OVERLAY_VMA,t.OVERLAY_READ_LEN),r.fingerprints)
                self.assertEqual(image['image_file_id'],file_id)
                self.assertFalse(image['active_resource_confirmed'])
                self.assertEqual(t.capture_poll(r,r.fingerprints)['values']['overlay']['image_file_id'],file_id)

    def test_read_only_poll_captures_live_lookalike_without_atomic_claim(self):
        ram=FakeRam(image_file=22)
        frame=t.capture_poll(ram,ram.fingerprints,elapsed_ms=20)
        self.assertIsNone(frame['guest_frame'])
        self.assertIsNone(frame['guest_pc'])
        self.assertEqual(frame['capture_kind'],'host_poll_non_atomic')
        self.assertEqual(frame['values']['outer_state'],3)
        self.assertEqual(frame['values']['secondary_state'],1)
        self.assertEqual(frame['values']['vm_substate'],2)
        self.assertEqual(frame['values']['stepw_end'],1)
        self.assertEqual(frame['values']['map_id'],0xAB)
        self.assertEqual(frame['values']['scheduler_mode'],4)
        self.assertEqual(frame['values']['flag_9000_word'],0x9000)
        self.assertEqual(frame['values']['file22_counter'],3)
        self.assertEqual(frame['values']['overlay']['image_file_id'],22)
        self.assertFalse(frame['values']['overlay']['active_resource_confirmed'])
        self.assertTrue(all(n<256 for _,n in ram.reads))

    def test_non22_overlays_do_not_read_stale_counter(self):
        ram=FakeRam(image_file=15)
        item=t.capture_poll(ram,ram.fingerprints)
        self.assertIsNone(item['values']['file22_counter'])
        self.assertNotIn((t.OVERLAY22_COUNTER,4),ram.reads)

    def test_unknown_image_fails_closed(self):
        ram=FakeRam(image_file=None)
        item=t.capture_poll(ram,ram.fingerprints)
        self.assertIsNone(item['values']['overlay']['image_file_id'])
        self.assertFalse(item['values']['overlay']['active_resource_confirmed'])

    def test_torn_sample_rejected(self):
        ram=FakeRam()
        ram.torn=True
        with self.assertRaisesRegex(ValueError,'Snapshot changed'):
            t.capture_poll(ram,ram.fingerprints)

    def test_wrong_sys_pointer_rejected(self):
        ram=FakeRam()
        ram.set(t.SYS_POINTER,(0).to_bytes(4,'big'))
        with self.assertRaisesRegex(ValueError,'not validated'):
            t.capture_poll(ram,ram.fingerprints)

    def test_halted_callback_loader_provenance_and_disagreement(self):
        ram=FakeRam()
        frame=t.capture_halted_frame(ram,ram.fingerprints,frame=120,guest_pc=0x801CB53C,
                                     proven_loader_file_id=22)
        self.assertEqual(frame['guest_frame'],120)
        self.assertTrue(frame['values']['overlay']['active_resource_confirmed'])
        self.assertIn('caller_supplied',frame['values']['overlay']['loader_provenance'])
        self.assertTrue(frame['values']['overlay']['guest_pc_inside_fingerprinted_text'])
        self.assertEqual(frame['values']['overlay']['executing_code_image_file_id'],22)
        with self.assertRaisesRegex(ValueError,'disagrees'):
            t.capture_halted_frame(ram,ram.fingerprints,frame=120,guest_pc=0x801CB53C,
                                   proven_loader_file_id=15)
        with self.assertRaises(ValueError):
            t.capture_halted_frame(ram,ram.fingerprints,frame=-1,guest_pc=0x801CB53C)

    def test_change_edges_do_not_assert_cause_without_execution_evidence(self):
        ram=FakeRam(outer=3,image_file=22)
        a=t.capture_poll(ram,ram.fingerprints)
        ram.set(t.STATE_BASE,bytes([4]))
        b=t.capture_poll(ram,ram.fingerprints)
        data=t.summarize([a,b])
        self.assertEqual(data['samples'],2)
        self.assertEqual(data['sampling_evidence'],'host_poll_not_same_frame')
        self.assertEqual(data['observed_transitions'][0]['static_consistency'],
                         'consistent_with_file22_overlay_state3_to4_path')
        self.assertEqual(data['observed_transitions'][0]['causal_attribution'],'NOT_PROVEN_NO_EXECUTED_PC_PROOF')

    def test_frame_order_validation(self):
        ram=FakeRam()
        a=t.capture_halted_frame(ram,ram.fingerprints,frame=17,guest_pc=0x80002040)
        b=t.capture_halted_frame(ram,ram.fingerprints,frame=17,guest_pc=0x80002040)
        with self.assertRaisesRegex(ValueError,'strictly increasing'):
            t.summarize([a,b])

    def test_cannot_overwrite_existing_report(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'report.json'
            t.save_report(target,t.summarize([]))
            with self.assertRaises(FileExistsError):t.save_report(target,t.summarize([]))

    def test_declares_missing_gameplay_data_not_synthetic_as_real(self):
        r=t.summarize([])
        self.assertEqual(r['samples'],0)
        self.assertNotIn('confirmed_in_game',json.dumps(r))

if __name__=='__main__':unittest.main()

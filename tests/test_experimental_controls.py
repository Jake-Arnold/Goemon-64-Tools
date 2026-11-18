"""Controlled, synthetic memory tests; not evidence of live warp/movement success."""
from __future__ import annotations
import struct
import unittest
from practice.experimental_controls import stage_reload_trial, task_float_probe
from practice.scene_controls import PENDING_MAP_ADDR, EXIT_REQUEST_ADDR
from practice.checkpoints import MAP_ADDR, STATE_ADDR
from tests.test_checkpoint import TestCheckpoint

SCENES={35:'Sample source',353:'Destination'}

class TestExperiments(unittest.TestCase):
    def make(self):
        _,ram=TestCheckpoint().sample()
        ram.write_guest(PENDING_MAP_ADDR,(35).to_bytes(2,'big'))
        return ram

    def test_reload_only_pending_then_state(self):
        r=self.make()
        before_exit=r.read_guest(EXIT_REQUEST_ADDR,1)
        before_current=r.read_guest(MAP_ADDR,2)
        response=stage_reload_trial(r,353,SCENES)
        self.assertEqual(response['status'],'reload_requested_character_and_spawn_unverified')
        self.assertEqual(r.read_guest(PENDING_MAP_ADDR,2),b'\x01\x61')
        self.assertEqual(r.read_guest(STATE_ADDR,1),b'\x0c')
        self.assertEqual(r.read_guest(EXIT_REQUEST_ADDR,1),before_exit)
        self.assertEqual(r.read_guest(MAP_ADDR,2),before_current)
        self.assertEqual(len(response['source_position']),3)

    def test_stage_selected_character_before_state_reload(self):
        from practice.experimental_controls import ACTIVE_CHARACTER_ADDR
        r=self.make()
        self.assertEqual(r.u32(ACTIVE_CHARACTER_ADDR),0)
        response=stage_reload_trial(r,353,SCENES,spawn_character=2)
        self.assertEqual(response['source_character'],0)
        self.assertEqual(response['requested_character'],2)
        self.assertTrue(response['character_staged'])
        self.assertEqual(r.u32(ACTIVE_CHARACTER_ADDR),2)
        self.assertEqual(r.u8(STATE_ADDR),12)
        self.assertEqual(r.u16(PENDING_MAP_ADDR),353)
        self.assertEqual(r.snapshot()['character'],2)

    def test_invalid_character_fails_before_any_memory_write(self):
        from practice.experimental_controls import ACTIVE_CHARACTER_ADDR
        for character in (-1,4,True,2.0,'2'):
            r=self.make()
            before=(r.read_guest(PENDING_MAP_ADDR,2),r.read_guest(ACTIVE_CHARACTER_ADDR,4))
            with self.assertRaises(ValueError):
                stage_reload_trial(r,353,SCENES,spawn_character=character)
            self.assertEqual((r.read_guest(PENDING_MAP_ADDR,2),r.read_guest(ACTIVE_CHARACTER_ADDR,4)),before)

    def test_character_staging_failure_rolls_back_while_still_in_gameplay(self):
        from practice.experimental_controls import ACTIVE_CHARACTER_ADDR
        r=self.make()
        previous_pending=r.read_guest(PENDING_MAP_ADDR,2)
        previous_character=r.read_guest(ACTIVE_CHARACTER_ADDR,4)
        original_write=r.write_guest
        def fail_character(addr,value):
            if addr==ACTIVE_CHARACTER_ADDR and value==(3).to_bytes(4,'big'):
                raise OSError('synthetic character write error')
            original_write(addr,value)
        r.write_guest=fail_character
        with self.assertRaisesRegex(OSError,'synthetic'):
            stage_reload_trial(r,353,SCENES,spawn_character=3)
        self.assertEqual(r.read_guest(PENDING_MAP_ADDR,2),previous_pending)
        self.assertEqual(r.read_guest(ACTIVE_CHARACTER_ADDR,4),previous_character)
        self.assertEqual(r.u8(STATE_ADDR),13)

    def test_invalid_destination_does_not_change_any_byte(self):
        for dest in (-1,353.0,True,9876):
            r=self.make()
            before=(r.read_guest(STATE_ADDR,1),r.read_guest(PENDING_MAP_ADDR,2))
            with self.assertRaises(ValueError):stage_reload_trial(r,dest,SCENES)
            self.assertEqual(before,(r.read_guest(STATE_ADDR,1),r.read_guest(PENDING_MAP_ADDR,2)))

    def test_reloading_outside_gameplay_not_allowed(self):
        r=self.make();r.write_guest(STATE_ADDR,b'\x0a')
        with self.assertRaisesRegex(RuntimeError,'engine=0x0A'):stage_reload_trial(r,353,SCENES)
        self.assertEqual(r.read_guest(PENDING_MAP_ADDR,2),(35).to_bytes(2,'big'))

    def test_pulse_one_float_only(self):
        r=self.make()
        task=r.snapshot()['task_ptr']
        r.write_guest(task+0x68,struct.pack('>f',1.5))
        r.write_guest(task+0x6C,b'\x12\x34\x56\x78')
        result=task_float_probe(r,direction=-1)
        self.assertEqual(result['address'],f'0x{task+0x68:08X}')
        self.assertEqual(result['bytes_written'],'C0800000')
        self.assertEqual(r.read_guest(task+0x68,4),struct.pack('>f',-4.0))
        self.assertEqual(r.read_guest(task+0x6C,4),bytes.fromhex('12345678'))

    def test_speed_pulse_scales_current_or_bumps_zero(self):
        r=self.make();task=r.snapshot()['task_ptr']
        r.write_guest(task+0x68,struct.pack('>f',-2.0))
        res=task_float_probe(r,speedup=True)
        self.assertEqual(res['new_f32'],-3.)
        r.write_guest(task+0x68,b'\x00'*4)
        res=task_float_probe(r,speedup=True)
        self.assertEqual(res['new_f32'],4.)

    def test_invalid_float_rejected(self):
        r=self.make();task=r.snapshot()['task_ptr']
        r.write_guest(task+0x68,struct.pack('>f',float('nan')))
        with self.assertRaisesRegex(ValueError,'Unreasonable'):task_float_probe(r)

if __name__=='__main__':unittest.main()

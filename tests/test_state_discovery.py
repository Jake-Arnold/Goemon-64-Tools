"""State discovery uses synthetic N64 guest bytes; no game connection needed."""
from __future__ import annotations
import struct
import unittest
from practice.state_discovery import capture_state,compare_captures,measured_velocity,PROBE_ACTIONS


class Memory:
    def __init__(self):
        self.data={0x8015C5DF:0, 0x800C7AB2:0, 0x800C7AB3:90}
        self.bytes_read=0
    def read_guest(self,addr,length):
        self.bytes_read+=length
        return bytes(self.data.get(addr+i,0) for i in range(length))
    def u32(self,addr):return int.from_bytes(self.read_guest(addr,4),'big')
    def u16(self,addr):return int.from_bytes(self.read_guest(addr,2),'big')
    def snapshot(self):return {'player_ptr':0x80123400,'task_ptr':0x801234A0}
    def write(self,addr,data):
        for i,c in enumerate(data):self.data[addr+i]=c


class StateDiscoveryTests(unittest.TestCase):
    def test_five_questions_have_actionable_instructions(self):
        self.assertEqual(len(PROBE_ACTIONS),5)
        self.assertIn('C-Right',PROBE_ACTIONS['Map displayed'])
        self.assertIn('C-Up',PROBE_ACTIONS['Magic active'])

    def test_reversed_boolean_and_persistent_destination_flags(self):
        mem=Memory()
        addr=0x8015C8F7
        a=capture_state(mem,'Travel A')
        mem.write(addr,b'\x01')
        b=capture_state(mem,'Travel B')
        c=capture_state(mem,'Travel C')
        report=compare_captures(a,b)
        matches=[r for r in report['candidates'] if r['address']==f'0x{addr:08X}']
        self.assertEqual(len(matches),1)
        self.assertEqual(report['counts']['reverting_changes'],0)  # No C capture: no verified reversals.
        self.assertEqual(matches[0]['kind'],'boolean')
        self.assertEqual(matches[0]['xor_mask'],'01')
        # A third capture that did not revert must filter out the persistent flag.
        self.assertEqual(compare_captures(a,b,c)['counts']['candidate_count'],0)
        mem.write(addr,b'\x00')
        d=capture_state(mem,'Travel D')
        restored=compare_captures(a,b,d)
        self.assertTrue(restored['candidates'][0]['reverted'])
        self.assertEqual(restored['counts']['reverting_changes'],1)

    def test_dynamic_float_candidate_and_pointer_changes(self):
        mem=Memory()
        addr=0x801234A0+0x68
        mem.write(addr,struct.pack('>f',0.0))
        a=capture_state(mem,'Velocity A')
        mem.write(addr,struct.pack('>f',4.25))
        b=capture_state(mem,'Velocity B')
        report=compare_captures(a,b)
        self.assertTrue(any(row['address']==f'0x{addr:08X}' and row['kind']=='f32 candidate'
                            for row in report['candidates']))
        self.assertFalse(any('data' in r for r in report['candidates']))
        self.assertEqual(report['capture_A']['character'],0)

    def test_character_scope_and_capture_checks(self):
        mem=Memory()
        with self.assertRaises(ValueError):capture_state(mem,' ',scope='wide')
        with self.assertRaises(ValueError):capture_state(mem,'before',scope='invalid')
        a=capture_state(mem,'a',scope='focused')
        # Different dynamic player pointers cannot be mistaken for stable addresses.
        b=capture_state(mem,'b',snapshot={'player_ptr':0x80145000,'task_ptr':0x801450C0})
        self.assertEqual(compare_captures(a,b)['counts']['candidate_count'],0)

    def test_measured_velocity_only_same_valid_player_and_dt(self):
        a=dict(player_ptr=0x80100000,character=0,loading=0,x=1.,y=2.,z=5.)
        b=dict(player_ptr=0x80100000,character=0,loading=0,x=3.,y=2.,z=4.)
        self.assertEqual(measured_velocity(b,a,.5),(4.,0.,-2.))
        self.assertIsNone(measured_velocity(b,a,0))
        self.assertIsNone(measured_velocity({**b,'player_ptr':0x80101000},a,.5))
        self.assertIsNone(measured_velocity({**b,'character':1},a,.5))
        self.assertIsNone(measured_velocity({**b,'loading':1},a,.5))


if __name__=='__main__':unittest.main()

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
        self.assertEqual(len(PROBE_ACTIONS),7)
        self.assertIn('Benkei',PROBE_ACTIONS['Storyline event / quest flag'])
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

    def test_storyline_saved_event_bit_shortlist(self):
        mem=Memory()
        a=capture_state(mem,'Storyline event / quest flag A')
        mem.write(0x8015C609,b'\x20')
        mem.write(0x8015C700,b'\x20')
        b=capture_state(mem,'Storyline event / quest flag B')
        report=compare_captures(a,b)
        self.assertEqual(report['counts']['reverting_changes'],0)
        self.assertEqual(report['event_flag_changes'],[
            {'address':'0x8015C609','before':'00','after':'20',
             'bits_set':'20','bits_cleared':'00','confirmed':False}])
        event=next(v for v in report['candidates'] if v['address']=='0x8015C609')
        self.assertEqual(event['kind'],'saved event flag candidate')

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

    def test_capture_without_player_and_unknown_character(self):
        mem=Memory()
        mem.write(0x8015C5DC,(0xFFFFFFFF).to_bytes(4,'big'))
        snap={'player_ptr':0,'task_ptr':0}
        a=capture_state(mem,'title A',snapshot=snap)
        self.assertIsNone(a.character)
        self.assertEqual({r.name for r in a.regions},{'system','game_data'})
        mem.write(0x8015C5DC,(0).to_bytes(4,'big'))
        b=capture_state(mem,'title B',snapshot=snap)
        self.assertIsNone(compare_captures(a,b)['capture_A']['character'])
        mem.write(0x8015C5DC,(0xFFFFFFFF).to_bytes(4,'big'))
        # Read-only global probes tolerate a stale character ID even with a
        # previous player pointer; they do not validate player actions.
        self.assertIsNone(capture_state(mem,'invalid',
                                        snapshot={'player_ptr':0x80100000,'task_ptr':0}).character)


    def test_invalid_special_mode_player_does_not_block_global_captures(self):
        mem=Memory()
        mem.write(0x8015C5DC,(0xFFFFFFFF).to_bytes(4,'big'))
        mem.write(0x800C7AA4,b'\x04')
        class ImpactMemory(Memory):
            def snapshot(self):
                raise ValueError('Invalid player object pointer 0xA4600014')
            def snapshot_for_monitoring(self):
                return {'player_ptr': None, 'task_ptr': None, 'character': None,
                        'player_unavailable_reason': 'Invalid player object pointer 0xA4600014'}
        impact=ImpactMemory()
        impact.data.update(mem.data)
        a=capture_state(impact,'Impact A')
        impact.write(0x800C7AA4,b'\x07')
        b=capture_state(impact,'Impact B')
        diff=compare_captures(a,b)
        self.assertIsNone(a.character)
        self.assertEqual({r.name for r in a.regions},{'system','game_data'})
        self.assertTrue(any(r['address']=='0x800C7AA4' for r in diff['candidates']))

    def test_invalid_optional_dynamic_pointer_is_skipped(self):
        mem=Memory()
        before=capture_state(mem,'A',snapshot={'player_ptr':0xA4600014,'task_ptr':0x801234A0})
        self.assertEqual({r.name for r in before.regions},
                         {'system','game_data','player_task'})

    def test_failed_optional_dynamic_region_does_not_block_capture(self):
        class BrokenTaskMemory(Memory):
            def read_guest(self,addr,length):
                if addr==0x801234A0:
                    raise OSError('task disappeared')
                return super().read_guest(addr,length)
        mem=BrokenTaskMemory()
        snap={'player_ptr':0xA4600014,'task_ptr':0x801234A0}
        before=capture_state(mem,'A',snapshot=snap)
        self.assertEqual({r.name for r in before.regions},{'system','game_data'})
        mem.write(0x800C7AA4,b'\x02')
        after=capture_state(mem,'B',snapshot=snap)
        self.assertTrue(any(x['address']=='0x800C7AA4'
                        for x in compare_captures(before,after)['candidates']))

    def test_measured_velocity_only_same_valid_player_and_dt(self):
        a=dict(player_ptr=0x80100000,character=0,loading=0,x=1.,y=2.,z=5.)
        b=dict(player_ptr=0x80100000,character=0,loading=0,x=3.,y=2.,z=4.)
        self.assertEqual(measured_velocity(b,a,.5),(4.,0.,-2.))
        self.assertIsNone(measured_velocity(b,a,0))
        self.assertIsNone(measured_velocity({**b,'player_ptr':0x80101000},a,.5))
        self.assertIsNone(measured_velocity({**b,'character':1},a,.5))
        self.assertIsNone(measured_velocity({**b,'loading':1},a,.5))


if __name__=='__main__':unittest.main()

import struct
import unittest
from pathlib import Path
import json
from decomp.plasma_conditions import (ADVICE_END, ADVICE_START, flag_location,
                                      instantiated_actor_messages, scan_advice)

class PlasmaConditionsTests(unittest.TestCase):
    def test_flag_locations_match_user_confirmed_priority_bits(self):
        self.assertEqual(flag_location(0x010),('0x8015C60A','0x01'))
        self.assertEqual(flag_location(0x000),('0x8015C608','0x01'))
        self.assertEqual(flag_location(0x044),('0x8015C610','0x10'))
        with self.assertRaises(ValueError):flag_location(800)

    def test_instance_binding_ignores_unused_definitions(self):
        room=bytearray(104)
        # Definition 0 is instantiated; definition 1 is not.
        struct.pack_into('>H',room,0,0x306);struct.pack_into('>H',room,10,0x288)
        struct.pack_into('>H',room,16,0x306);struct.pack_into('>H',room,26,0x123)
        room[32+12:32+14]=b'\x08\x00'
        struct.pack_into('>H',room,32+14,0)
        struct.pack_into('>HHH',room,72+20,1,1,1)
        self.assertEqual(instantiated_actor_messages(room,32,72,100,0x306),[{'definition':0,'message':0x288}])
        room[32+12]=0; room[32]=1
        with self.assertRaises(ValueError):instantiated_actor_messages(room,32,72,100,0x306)

    def test_opcode_scan_rejects_wrong_entry_and_branch_target(self):
        script=bytearray(ADVICE_END)
        with self.assertRaisesRegex(ValueError,'entry jump'):scan_advice(script)
        struct.pack_into('>II',script,0x319C,0x800A,0x08003208)
        struct.pack_into('>III',script,ADVICE_START,0x8022,0x10,0x09003208)
        with self.assertRaisesRegex(ValueError,'branch target'):scan_advice(script)
        struct.pack_into('>I',script,ADVICE_START+8,0x08003208)
        with self.assertRaisesRegex(ValueError,'inventory changed'):scan_advice(script)

    def test_published_metadata_covers_common_event_and_complete_branch_inventory(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/plasma_conditions.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual([x['stage'] for x in data['rooms']],[423,424,425,426])
        self.assertTrue(all(x['event_id']=='0x288' for x in data['rooms']))
        self.assertEqual((data['flag_checks'],data['distinct_checked_flags'],data['set_operations']),(40,37,11))
        from practice.story_progress import FLAGS
        tracked={flag.flag_id for flag in FLAGS}
        self.assertTrue({int(op['flag_id'],16) for op in data['operations']} <= tracked)
        checks=[x for x in data['operations'] if x['operation']=='branch_if_set']
        self.assertEqual([(x['flag_id'],x['address'],x['mask']) for x in checks[:2]],
                         [('0x010','0x8015C60A','0x01'),('0x000','0x8015C608','0x01')])
        self.assertEqual(next(x for x in checks if x['flag_id']=='0x044')['target_file_offset'],'0x3A34')

    def test_published_writer_leads_are_bounded_and_distinguish_sources(self):
        path=Path(__file__).resolve().parents[1]/'decomp/results/plasma_writers.json'
        result=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(len(result['flag_ids']),39)
        self.assertEqual(len(result['writers']),69)
        self.assertTrue(all(w['operation'] in ('set','clear') for w in result['writers']))
        self.assertEqual({w['rom_offset'] for w in result['writers'] if w['flag_id']=='0x044'},
                         {'0x76DA60','0x76DACC','0x7A2450'})
        self.assertIn('no native scan',result['limitation'])

if __name__=='__main__':unittest.main()

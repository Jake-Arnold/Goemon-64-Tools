import struct
import unittest
from research.rom.pickup_placements import room_pickups,extract
from practice.story_progress import FLAGS,PLACEMENT_PICKUPS


def room_fixture():
    instance=48;footer=108;ending=136;room=bytearray(ending)
    for index,actor,flag in ((0,0x86,0xFF),(1,0x87,0x105),(2,0x87,0x108)):
        struct.pack_into('>H',room,index*16,actor)
        struct.pack_into('>H',room,index*16+4,flag)
    for offset,index in ((48,0),(68,1)):
        room[offset+12:offset+16]=struct.pack('>HH',0x0800,index*16)
    return room,instance,footer,ending


class PickupPlacementTests(unittest.TestCase):
    def test_only_instantiated_definitions_and_big_endian_ids(self):
        room,instance,footer,ending=room_fixture()
        rows=room_pickups(57,0x36C,room,instance,footer,ending)
        self.assertEqual([r['flag_id'] for r in rows],[0xFF,0x105])
        self.assertEqual([r['address'] for r in rows],['0x8015C627','0x8015C628'])
        self.assertEqual([r['mask'] for r in rows],['0x80','0x20'])
        self.assertEqual([r['actor_id'] for r in rows],[0x86,0x87])
        self.assertTrue(all(r['stage']==57 for r in rows))

    def test_grid_duplicates_and_invalid_metadata(self):
        room,instance,footer,ending=room_fixture()
        struct.pack_into('>HHH',room,footer+20,1,1,1)
        room.extend(struct.pack('>I',0x08000000|instance))
        self.assertEqual(len(room_pickups(1,1,room,instance,footer,ending)),2)
        struct.pack_into('>I',room,ending,0x09000000|instance)
        with self.assertRaisesRegex(ValueError,'pointer'):room_pickups(1,1,room,instance,footer,ending)
        room,instance,footer,ending=room_fixture()
        struct.pack_into('>H',room,4,800)
        with self.assertRaisesRegex(ValueError,'bank'):room_pickups(1,1,room,instance,footer,ending)
        room,instance,footer,ending=room_fixture();room[60:62]=b'xx'
        with self.assertRaisesRegex(ValueError,'header'):room_pickups(1,1,room,instance,footer,ending)
        with self.assertRaises(ValueError):room_pickups(1,1,room,instance+1,footer,ending)
        with self.assertRaises(ValueError):extract(bytes.fromhex('80371240'))

    def test_all_ten_pickups_have_distinct_ids_and_separate_provenance(self):
        manual={f.flag_id for f in FLAGS if f.key in ('oedo_elly_collected','ghost_arrow_collected','musical_arrow_collected')}
        derived={f.flag_id for f in PLACEMENT_PICKUPS}
        self.assertEqual(len(derived),7)
        self.assertFalse(manual&derived)
        self.assertEqual(manual|derived,set(range(0xFF,0x109)))
        for f in PLACEMENT_PICKUPS:
            self.assertIn('ROM instantiated placement',f.evidence)
            self.assertIn('not live-tested',f.evidence)

    def test_doll_actor_selection_does_not_change_default_map_scope(self):
        room,instance,footer,ending=room_fixture()
        struct.pack_into('>H',room,0,0x88)
        struct.pack_into('>H',room,4,0xDB)
        struct.pack_into('>H',room,16,0x89)
        struct.pack_into('>H',room,20,0xF2)
        self.assertEqual(room_pickups(1,1,room,instance,footer,ending),[])
        rows=room_pickups(1,1,room,instance,footer,ending,actor_ids={0x88,0x89})
        self.assertEqual([r['pickup'] for r in rows],['Silver Fortune Doll','Gold Fortune Doll'])
        self.assertEqual([r['flag_id'] for r in rows],[0xDB,0xF2])
        with self.assertRaisesRegex(ValueError,'selection'):room_pickups(1,1,room,instance,footer,ending,actor_ids={0x01})
        with self.assertRaisesRegex(ValueError,'kind'):extract(b'',kind='unknown')

    def test_published_doll_metadata_corroborates_manual_samples_and_shared_flag(self):
        import json
        from pathlib import Path
        from collections import Counter
        from practice.story_progress import DOLL_PLACEMENT_FLAGS
        report=json.loads((Path(__file__).resolve().parents[1]/'research/rom/results/fortune_doll_placements.json').read_text())
        rows=report['pickups'];counts=Counter(r['flag_id'] for r in rows)
        self.assertEqual(len(rows),44);self.assertEqual(len(counts),43)
        self.assertEqual(sum(r['actor_id']==0x88 for r in rows),39)
        self.assertEqual(sum(r['actor_id']==0x89 for r in rows),5)
        self.assertEqual(counts[0xEF],2)
        self.assertTrue(all(any(r['stage']==stage and r['flag_id']==flag for r in rows) for stage,flag in ((356,0xED),(381,0xF1),(301,0xDB))))
        named={f.flag_id for f in FLAGS}
        self.assertTrue(set(counts)<=named)
        self.assertEqual(len(DOLL_PLACEMENT_FLAGS),40)
        self.assertEqual(len({f.label for f in DOLL_PLACEMENT_FLAGS}),40)
        self.assertTrue(all('not live-collected' in f.evidence for f in DOLL_PLACEMENT_FLAGS))

    def test_complete_doll_flag_catalog_distinguishes_native_rewards(self):
        import json
        from pathlib import Path
        r=json.loads((Path(__file__).resolve().parents[1]/'research/rom/results/fortune_doll_catalog.json').read_text())
        entries=r['entries'];flags={x['flag_id'] for x in entries}
        self.assertEqual(len(entries),45);self.assertEqual(len(flags),45)
        self.assertEqual(flags,set(range(0xCA,0xF7)))
        self.assertEqual(sum(x['reward']=='silver' for x in entries),40)
        self.assertEqual(sum(x['reward']=='gold' for x in entries),5)
        self.assertEqual(sum(x['source']=='instantiated_room_definition' for x in entries),43)
        shishi=next(x for x in entries if x['flag_id']==0xEE)
        self.assertEqual((shishi['address'],shishi['mask']),('0x8015C625','0x40'))
        self.assertEqual(shishi['task_flag_word'],'0x00EE0000')
        self.assertEqual(shishi['pickup_callback'],'0x08000514')
        self.assertTrue(flags<={f.flag_id for f in FLAGS})
        self.assertTrue(all(not x['live_tested_by_assistant'] for x in entries))

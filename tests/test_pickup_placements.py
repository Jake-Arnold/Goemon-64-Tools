import struct
import unittest
from decomp.pickup_placements import room_pickups,extract
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

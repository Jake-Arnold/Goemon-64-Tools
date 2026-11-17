import copy
import struct
import tempfile
import unittest
from pathlib import Path

from practice.room_actors import (SCHEMA, actors_for_stage, actor_names, digest,
                                  parse_room, validate_actors, save_actors, load_actors)
from practice.entrances import US_RETAIL_SHA1


def room_fixture():
    # Two definitions: exit, unknown actor. One base group with two placements,
    # one spatial group repeating the unknown actor twice. Grid references share it.
    definitions = bytearray(2 * 16)
    struct.pack_into('>H', definitions, 0, 0x8C)
    struct.pack_into('>H', definitions, 16, 0x321)
    def record(pointer):
        r=bytearray(20);r[12:14]=b'\x08\x00';struct.pack_into('>H',r,14,pointer);return r
    base = record(0)+record(16)+bytes(20)
    spatial = record(16)+record(16)+bytes(20)
    instance = 32
    footer = instance+len(base)+len(spatial)
    raw=bytearray(definitions+base+spatial+bytes(28))
    ending=len(raw)
    struct.pack_into('>HHH',raw,footer+20,2,1,1)
    raw+=struct.pack('>II',0x08000000+instance+len(base),0x08000000+instance+len(base))
    return raw, instance, footer, ending


def atlas_fixture():
    raw, start, footer, end=room_fixture()
    rows=parse_room(353,0x40B,raw,start,footer,end, names={0x8C:('Exit','code'),0x321:('Mystery','test')})
    payload=dict(format=SCHEMA,region='usa',rom_sha1=US_RETAIL_SHA1,
                 evidence='Static ROM room placement references; NOT live spawned actors',
                 rooms=[dict(stage=353,room_file=0x40B,count=len(rows))], placements=rows)
    return dict(payload=payload,sha256=digest(payload))


class RoomActorTests(unittest.TestCase):
    def test_preserves_instances_and_deduplicates_shared_grid_group(self):
        atlas=atlas_fixture()
        rows=actors_for_stage(atlas,353)
        self.assertEqual(len(rows),4)
        self.assertEqual([r['actor_id'] for r in rows],[0x8C,0x321,0x321,0x321])
        self.assertEqual(rows[0]['cells'],[-1])
        self.assertEqual(rows[-1]['cells'],[0,1])
        self.assertEqual(len(set((r['group_offset'],r['record_offset']) for r in rows)),4)
        self.assertEqual(actors_for_stage(atlas,352),[])

    def test_rejects_bad_instance_bounds_and_definitions(self):
        raw,start,footer,end=room_fixture()
        for args in ((start+1,footer,end),(start,footer,end-1),(start,footer+100,end)):
            with self.assertRaises(ValueError): parse_room(353,0x40B,raw,*args)
        damaged=bytearray(raw)
        damaged[start+12:start+14]=b'\x09\x00'
        with self.assertRaisesRegex(ValueError,'header'): parse_room(353,0x40B,damaged,start,footer,end)
        damaged=bytearray(raw)
        struct.pack_into('>H',damaged,start+14,17)
        with self.assertRaisesRegex(ValueError,'definition'): parse_room(353,0x40B,damaged,start,footer,end)
        damaged=bytearray(raw)
        struct.pack_into('>I',damaged,end,0x09000000+start+60)
        with self.assertRaisesRegex(ValueError,'prefix'): parse_room(353,0x40B,damaged,start,footer,end)
        damaged=bytearray(raw)
        damaged[start+40:start+60] = bytearray(20)
        damaged[start+100:start+120] = bytes([1])*20
        with self.assertRaises(ValueError):parse_room(353,0x40B,damaged,start,footer,end)

    def test_integrity_counts_and_cache(self):
        atlas=atlas_fixture()
        validate_actors(atlas)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'rooms.json'
            self.assertIsNone(load_actors(path))
            save_actors(path,atlas)
            self.assertEqual(load_actors(path),atlas)
        wrong=copy.deepcopy(atlas)
        wrong['payload']['placements'][0]['name']='Tampered'
        with self.assertRaisesRegex(ValueError,'checksum'):validate_actors(wrong)
        wrong['sha256']=digest(wrong['payload'])
        validate_actors(wrong)  # Checksum checks accidental corruption, not authenticity.
        wrong['payload']['rooms'][0]['count']+=1
        wrong['sha256']=digest(wrong['payload'])
        with self.assertRaisesRegex(ValueError,'counts'):validate_actors(wrong)
        wrong=copy.deepcopy(atlas)
        wrong['payload']['placements'].append(copy.deepcopy(wrong['payload']['placements'][0]))
        wrong['sha256']=digest(wrong['payload'])
        with self.assertRaisesRegex(ValueError,'Duplicate'):validate_actors(wrong)

    def test_labels_and_missing_external_catalog(self):
        with tempfile.TemporaryDirectory() as folder:
            names=actor_names(Path(folder)/'missing.json')
            self.assertEqual(names[0x08C][0],'Exit')
            self.assertNotIn(0x321,names)


if __name__=='__main__':unittest.main()

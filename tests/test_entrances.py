import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
from practice.entrances import Spawn,canonical_rom,decompress_block,room_entrances,validate_atlas,save_atlas,load_atlas,incoming,spawn_from_entry,digest,SCHEMA,US_RETAIL_SHA1,RomFiles


def compressed(payload):return (len(payload)+4).to_bytes(4,'big')+payload


def room_fixture():
    definitions=struct.pack('>HHHhhhHBB',0x8C,0,2,-10,20,30,0x100,0x21,0x10)
    definitions+=struct.pack('>HHHhhhHBB',0x8C,0,2,100,200,300,0x200,0x22,0x10)
    instance=bytearray(20);instance[12:14]=b'\x08\x00'
    footer=bytes(28)
    return definitions+instance+bytes(20)+footer,32,72,100


def atlas_fixture():
    room,instance,footer,ending=room_fixture()
    entries=room_entrances(1,0x337,room,instance,footer,ending)
    payload=dict(format=SCHEMA,rom_sha1=US_RETAIL_SHA1,rooms=[1,2],entries=entries)
    return {'payload':payload,'sha256':digest(payload)}


class EntranceParsingTests(unittest.TestCase):
    def test_rom_byte_orders_and_unknown_identity(self):
        original=bytes.fromhex('8037124011223344')
        swapped=bytes.fromhex('3780401222114433')
        little=bytes.fromhex('4012378044332211')
        self.assertEqual(canonical_rom(swapped),original)
        self.assertEqual(canonical_rom(little),original)
        self.assertEqual(canonical_rom(original),original)
        with self.assertRaises(ValueError):canonical_rom(b'bad')
        with self.assertRaisesRegex(ValueError,'verified original'):RomFiles(original)

    def test_compression_literals_runs_zeros_and_overlap(self):
        self.assertEqual(decompress_block(compressed(b'\x83abc\x08\x03')),b'abcabca')
        self.assertEqual(decompress_block(compressed(b'\xC1x\xE0\xFF\x05')),b'xxx'+bytes(9))
        self.assertEqual(decompress_block(compressed(b'\x00')),bytes(2))
        self.assertEqual(decompress_block(compressed(b'\x00\x00')),bytes(2))
        for bad in (b'',b'\0\0\0\x10',compressed(b'\x83a'),compressed(b'\x00\x0A'),compressed(b'\xC0')):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):decompress_block(bad)
        with self.assertRaisesRegex(ValueError,'limit'):decompress_block(compressed(b'\xE1'),maximum=2)

    def test_only_instantiated_exits_and_native_axis_order(self):
        data,instance,footer,ending=room_fixture()
        rows=room_entrances(1,0x337,data,instance,footer,ending)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['position'],[-10,20,30])
        self.assertEqual(rows[0]['exit_id'],1)
        self.assertEqual(rows[0]['destination'],2)
        self.assertEqual(rows[0]['definition'],0)

    def test_repeated_grid_group_does_not_duplicate_exit(self):
        data,instance,footer,ending=room_fixture();data=bytearray(data)
        struct.pack_into('>HHH',data,footer+20,1,1,1)
        data.extend(struct.pack('>I',0x08000000|instance))
        self.assertEqual(len(room_entrances(1,0x337,data,instance,footer,ending)),1)
        struct.pack_into('>I',data,ending,0x09000000|instance)
        with self.assertRaises(ValueError):room_entrances(1,0x337,data,instance,footer,ending)

    def test_bad_room_offsets_and_unterminated_instances(self):
        data,instance,footer,ending=room_fixture()
        for parameters in ((31,footer,ending),(instance,footer,ending-1),(instance,1000,1028)):
            with self.assertRaises(ValueError):room_entrances(1,0x337,data,*parameters)
        broken=bytearray(data);broken[instance+20+12:instance+20+14]=b'\x08\x00'
        with self.assertRaises(ValueError):room_entrances(1,0x337,broken,instance,footer,ending)

    def test_cache_roundtrip_checksums_duplicates_and_nonfinite_coordinates(self):
        atlas=atlas_fixture();validate_atlas(atlas)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'atlas.json';save_atlas(path,atlas)
            self.assertEqual(load_atlas(path),atlas)
            self.assertIsNone(load_atlas(Path(folder)/'missing'))
        changed=copy.deepcopy(atlas);changed['payload']['entries'][0]['position'][0]=9
        with self.assertRaises(ValueError):validate_atlas(changed)
        for value in (float('nan'),float('inf'),True,40000):
            changed=copy.deepcopy(atlas);changed['payload']['entries'][0]['position'][0]=value;changed['sha256']=digest(changed['payload'])
            with self.assertRaises(ValueError):validate_atlas(changed)
        changed=copy.deepcopy(atlas);changed['payload']['entries']*=2;changed['sha256']=digest(changed['payload'])
        with self.assertRaises(ValueError):validate_atlas(changed)

    def test_spawn_packet_and_destination_lookup(self):
        entry=incoming(atlas_fixture(),2)[0];spawn=spawn_from_entry(entry)
        self.assertEqual(spawn.pending_bytes(),struct.pack('>HHhhhH',2,0x10,-10,20,30,0x100))
        self.assertEqual(incoming(atlas_fixture(),1),[])
        self.assertEqual(Spawn(2,(1.25,-2.75,3.5)).pending_bytes()[4:10],struct.pack('>hhh',1,-3,4))
        for spawn in (Spawn(True,(0,0,0)),Spawn(2,(0,0,0),mode=65536),Spawn(2,(0,0,0),heading=True)):
            with self.assertRaises(ValueError):spawn.pending_bytes()

    def test_native_default_records_allow_full_mode_word(self):
        spawn=Spawn(370,(0,-75,68),0x200,0x200,'Native default')
        self.assertEqual(struct.unpack('>HHhhhH',spawn.pending_bytes()),(370,0x200,0,-75,68,0x200))
        atlas=atlas_fixture();row=copy.deepcopy(atlas['payload']['entries'][0])
        row.update(id='default:2',kind='default',source_map=None,source_file=None,mode=0x200)
        atlas['payload']['entries'].append(row);atlas['sha256']=digest(atlas['payload'])
        validate_atlas(atlas)
        self.assertIn('Native default',spawn_from_entry(row).label)

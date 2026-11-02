import struct
import io
from contextlib import redirect_stderr
import tempfile
import unittest
from pathlib import Path

from practice.rom_flag_trace import flag_location,file_ranges,scan_candidates,scan_indirect_calls,analyze_rom,main


class RomFlagTraceTests(unittest.TestCase):
    def test_indirect_call_literal_and_rejection_of_clobbers_and_branches(self):
        def sample(middle):
            words=[(15<<26)|(25<<16)|0x8002,
                   (9<<26)|(25<<21)|(25<<16)|0x40DC,*middle,
                   (25<<21)|(31<<11)|9,(9<<26)|(4<<16)|0x23]
            return struct.pack('>'+str(len(words))+'I',*words)
        data=sample([(43<<26)|(29<<21)|(31<<16)|0x1C])  # Harmless stack store.
        hits=scan_indirect_calls(data,[(62,0,len(data))],{62})
        self.assertEqual(len(hits),1)
        self.assertEqual((hits[0]['address'],hits[0]['mask'],hits[0]['operation']),('0x8015C60C','0x08','test'))
        self.assertEqual(scan_indirect_calls(data,[(62,0,len(data))],{61}),[])
        for middle in ([(9<<26)|(25<<16)|1],[(4<<26)|1]):
            data=sample(middle)
            self.assertEqual(scan_indirect_calls(data,[(62,0,len(data))],{62}),[])

    def test_indirect_call_rejects_nonliteral_argument_and_truncation(self):
        data=struct.pack('>4I',(15<<26)|(2<<16)|0x8002,
            (9<<26)|(2<<21)|(2<<16)|0x4038,(2<<21)|(31<<11)|9,
            (9<<26)|(3<<21)|(4<<16)|0x23)
        self.assertEqual(scan_indirect_calls(data,[(62,0,len(data))],{62}),[])
        self.assertEqual(scan_indirect_calls(data[:-4],[(62,0,len(data)-4)],{62}),[])

    def test_known_bit_ids_and_bounds(self):
        for flag,address,mask in ((0x25,0x8015C60C,0x20),(0x2D,0x8015C60D,0x20),
                                 (0x2F,0x8015C60D,0x80),(0x31,0x8015C60E,2),
                                 (0x33,0x8015C60E,8),(0x34,0x8015C60E,0x10)):
            self.assertEqual(flag_location(flag),(address,mask))
        for value in (-1,800,True):
            with self.assertRaises(ValueError):flag_location(value)

    def test_aligned_patterns_filters_branch_resolution_and_bounds(self):
        data=bytearray(256)
        struct.pack_into('>II',data,16,0x8020,0x25)
        struct.pack_into('>III',data,40,0x8022,0x2F,0x08000060)
        struct.pack_into('>III',data,64,0x8022,0x2E,0x09000020)
        struct.pack_into('>II',data,89,0x8020,0x34)  # Unaligned decoy.
        struct.pack_into('>II',data,120,0x8021,900)  # Outside primary flags.
        struct.pack_into('>II',data,140,0x8020,0x31)  # Outside supplied file.
        struct.pack_into('>II',data,248,0x8022,0x31)  # Truncated branch.
        hits=scan_candidates(data,[(97,16,128),(98,240,256)])
        self.assertEqual(len(hits),3)
        self.assertEqual(hits[1]['local_branch_rom_offset'],'0x70')
        self.assertIsNone(hits[2]['local_branch_rom_offset'])
        self.assertEqual(len(scan_candidates(data,[(97,16,128)],[0x2F])),1)
        self.assertTrue(all(h['status']=='opcode_pattern_candidate' for h in hits))

    def test_table_and_invalid_compression_order_termination(self):
        def make(values):
            signature=b'Nisitenma-Ichigo'
            data=bytearray(128);data[:len(signature)]=signature
            for i,value in enumerate(values):struct.pack_into('>I',data,len(signature)+i*4,value)
            return data
        self.assertEqual(file_ranges(make([64,80,100,0])),[(1,64,80),(2,80,100)])
        for values in ([64,0x80000050,100,0],[80,64,100,0],[64,200,0],[64,0]):
            with self.assertRaises(ValueError):file_ranges(make(values))
        with self.assertRaises(ValueError):file_ranges(b'bad ROM')

    def test_unknown_rom_rejected_and_input_never_overwritten(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):analyze_rom(b'not a ROM')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'test.z64';path.write_bytes(b'input')
            with redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                main(['--rom',str(path),'--output',str(path)])
            self.assertEqual(path.read_bytes(),b'input')

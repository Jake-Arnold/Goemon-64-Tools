"""ROM-free tests for region-checked Goemon recompilation input generation."""
import hashlib
import struct
import unittest
from unittest.mock import patch
from decomp import recomp_rom_input as build


def minimal_rom():
    rom = bytearray(0x1000000)
    rom[:4] = bytes.fromhex('80371240')
    rom[0x3B:0x3F] = b'NG5J'
    table = 0x180000
    rom[table:table+len(build.SIGNATURE)] = build.SIGNATURE
    off = table + len(build.SIGNATURE)
    start = 0x200000
    data = struct.pack('>I', 9) + b'\x84ABCD'
    rom[start:start+len(data)] = data
    raw = b'hello'
    rom[start+len(data):start+len(data)+len(raw)] = raw
    vals = [start | 0x80000000, start+len(data)]
    vals.extend([start+len(data)+len(raw)] * (build.FILE_POINTERS-2))
    struct.pack_into('>'+('I'*build.FILE_POINTERS),rom,off,*vals)
    return bytes(rom)


class Tests(unittest.TestCase):
    def test_region_constants(self):
        self.assertEqual(build.REGIONS['usa'][1], 'df8083a54296b8c151917c5333e1c85f014a2a66')
        self.assertEqual(build.REGIONS['japan_0'][2], '6f8745fecc3a5e7d4918c7a73353eb0726116ded')

    def test_rejects_unknown_rom_or_revision(self):
        with self.assertRaises(ValueError): build.expand(b'broken', 'japan_0')
        with self.assertRaises(ValueError): build.expand(minimal_rom(), 'japan_0')
        with self.assertRaises(ValueError): build.expand(minimal_rom(), 'unknown')

    def test_eligible_synthetic_lz_payload_and_16_byte_alignment(self):
        rom = minimal_rom()
        sha = hashlib.sha1(rom).hexdigest()
        code, _, expected = build.REGIONS['japan_0']
        with patch.dict(build.REGIONS, {'japan_0': (code, sha, expected)}):
            with self.assertRaisesRegex(ValueError, 'Decompressed SHA-1 mismatch') as cm:
                build.expand(rom, 'japan_0')
            actual = str(cm.exception).split('mismatch: ')[1].split(';')[0]
            with patch.dict(build.REGIONS, {'japan_0': (code, sha, actual)}):
                result, stats = build.expand(rom, 'japan_0')
        self.assertEqual(stats['populated_files'], 2)
        self.assertEqual(stats['compressed_files'], 1)
        self.assertEqual(result[0x200000:0x200004], b'ABCD')
        self.assertEqual(result[0x200010:0x200015], b'hello')
        self.assertEqual(struct.unpack_from('>3I',result,0x180000+len(build.SIGNATURE)),
                         (0x200000, 0x200010, 0x200020))

    def test_wrong_region_never_builds(self):
        rom = minimal_rom()
        sha = hashlib.sha1(rom).hexdigest()
        with patch.dict(build.REGIONS, {'japan_0': (b'NG5E', sha, 'x')}):
            with self.assertRaisesRegex(ValueError, 'Wrong ROM region'):
                build.expand(rom,'japan_0')

    def test_bad_table_never_builds(self):
        rom = bytearray(minimal_rom())
        ptr = 0x180000+len(build.SIGNATURE)
        struct.pack_into('>I',rom,ptr+4,0x180)
        sha = hashlib.sha1(rom).hexdigest()
        with patch.dict(build.REGIONS, {'japan_0': (b'NG5J', sha, 'x')}):
            with self.assertRaisesRegex(ValueError, 'Bad file-table entry'):
                build.expand(rom,'japan_0')


if __name__=='__main__': unittest.main()

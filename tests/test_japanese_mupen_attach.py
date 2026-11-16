"""ROM-free Japanese Mupen64Plus attach safety tests.

Tests use an 8 MiB synthetic RDRAM mapping, never a real emulator process.
"""
from __future__ import annotations
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from practice import japanese_mupen_attach as jp

BASE=0x10000000
OFFSETS=(0x450, 0x600, 0x2400)
PROBES=tuple((o, bytes(((o+i*3)&0xff) for i in range(jp.PROBE_BYTES)))
             for o in OFFSETS)


class Process:
    def __init__(self, endian='wordswapped', duplicate=False):
        self.memory=bytearray(jp.RDRAM_SIZE * (2 if duplicate else 1))
        for offset, value in PROBES:
            data=(jp._swapped_words(value) if endian=='wordswapped' else
                  jp._swapped_pairs(value) if endian=='byteswapped' else value)
            self.memory[offset:offset+len(data)] = data
            if duplicate:
                other=jp.RDRAM_SIZE+offset
                self.memory[other:other+len(data)] = data

    def regions(self):
        return [(BASE,len(self.memory))]

    def read(self,ptr,length):
        off=ptr-BASE
        if off<0 or off+length>len(self.memory):
            raise OSError('outside test process mapping')
        return bytes(self.memory[off:off+length])


class JapaneseMupenAttachTests(unittest.TestCase):
    def test_word_swap(self):
        self.assertEqual(jp._swapped_words(b'ABCD1234'),b'DCBA4321')

    def test_detect_word_swapped_mupen(self):
        reader,base,endian=jp.discover_japanese_mupen_rdram(
            Process(),PROBES,max_scan_mb=12)
        self.assertEqual((base,endian),(BASE,'wordswapped'))
        self.assertEqual(reader.read_guest(0x80000450,64),PROBES[0][1])

    def test_detect_big_endian(self):
        _,base,endian=jp.discover_japanese_mupen_rdram(
            Process('big'),PROBES,max_scan_mb=12)
        self.assertEqual((base,endian),(BASE,'big'))

    def test_detect_byte_swapped_with_unaligned_guest_reads_and_writes(self):
        proc=Process('byteswapped')
        rdram,base,endian=jp.discover_japanese_mupen_rdram(
            proc,PROBES,max_scan_mb=12)
        self.assertEqual((base,endian),(BASE,'byteswapped'))
        self.assertEqual(rdram.read_guest(0x80000451,5),PROBES[0][1][1:6])
        before=rdram.read_guest(0x80000450,10)
        # Test a byte write straddling a 16-bit pair; only targeted guest
        # bytes change, and neighboring executable bytes are preserved.
        payload=b'XYZ'
        proc.write=lambda address,data: proc.memory.__setitem__(
            slice(address-BASE,address-BASE+len(data)), data)
        rdram.write_guest(0x80000453,payload)
        updated=rdram.read_guest(0x80000450,10)
        self.assertEqual(updated, before[:3]+payload+before[6:])

    def test_manual_base_requires_three_probes(self):
        process=Process()
        with self.assertRaises(RuntimeError):
            jp.discover_japanese_mupen_rdram(process,PROBES,base_hint=BASE+16)
        self.assertEqual(
            jp.discover_japanese_mupen_rdram(process,PROBES,base_hint=BASE)[1],BASE)

    def test_reject_modified_code(self):
        process=Process()
        process.memory[OFFSETS[2]]=0
        with self.assertRaisesRegex(RuntimeError,'No Japanese'):
            jp.discover_japanese_mupen_rdram(process,PROBES,max_scan_mb=12)

    def test_ambiguous_copies_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError,'Ambiguous'):
            jp.discover_japanese_mupen_rdram(
                Process(duplicate=True),PROBES,max_scan_mb=20)

    def test_reject_wrong_endian_and_alignment(self):
        with self.assertRaises(ValueError):
            jp.validate_rdram_base(Process(),BASE,'big',PROBES)
        with self.assertRaises(ValueError):
            jp.validate_rdram_base(Process(),BASE+3,'wordswapped',PROBES)

    def test_rom_probe_offsets_and_identity(self):
        rom=bytearray(0x4000)
        for i in range(0x1000,len(rom)):
            rom[i] = i & 255
        with TemporaryDirectory() as folder:
            p=Path(folder)/'fake.z64'
            p.write_bytes(rom)
            with patch.object(jp,'identify_rom',return_value=SimpleNamespace(key='japan')), \
                 patch.object(jp,'canonical_rom',return_value=rom):
                probes=jp.verified_japan_probes(p)
            self.assertEqual(probes[0][0],0x450)
            self.assertEqual(probes[0][1],rom[0x1050:0x1090])
            with patch.object(jp,'identify_rom',return_value=SimpleNamespace(key='usa')):
                with self.assertRaisesRegex(ValueError,'not Japan'):
                    jp.verified_japan_probes(p)

    def test_permission_denied_not_suppressed(self):
        class Restricted(Process):
            def read(self,*args):
                raise PermissionError('Linux Yama denied process_vm_readv')
        with self.assertRaises(PermissionError):
            jp.discover_japanese_mupen_rdram(Restricted(),PROBES,max_scan_mb=12)


if __name__=='__main__':
    unittest.main()

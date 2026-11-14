"""Pure synthetic tests; no emulator, ROM assets, root or writes required."""
import importlib
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


class FakeProcess:
    def __init__(self, ranges):
        self.ranges = ranges
        self.writes = []
    def read(self, addr, n):
        for base, block in self.ranges:
            if base <= addr and addr + n <= base + len(block):
                return bytes(block[addr-base:addr-base+n])
        raise OSError("Unmapped memory")
    def write(self, addr, data):
        self.writes.append((addr, data))
        raise AssertionError("Read-only probe attempted to write")
    def close(self):
        pass


class FakeRdram:
    def __init__(self, process, base, endian):
        self.process, self.base, self.endian = process, base, endian
    def read_guest(self, addr, n):
        off=addr&0x7FFFFF
        raw=self.process.read(self.base+(off&~3), ((off+n+3)&~3)-(off&~3))
        if self.endian=='wordswapped':
            raw=b''.join(raw[i:i+4][::-1] for i in range(0,len(raw),4))
        return raw[off%4:off%4+n]


def _load_module():
    # Import production implementation with minimal synthetic collaborators.
    # In the full project these are the existing autosplitter/practice modules.
    mem=types.ModuleType("autosplitter.memory")
    mem.HostProcess=lambda pid,writable: None
    mem.Rdram=FakeRdram
    ent=types.ModuleType("practice.entrances")
    ent.canonical_rom=lambda b:b
    emu=types.ModuleType("practice.emulator_savestates")
    emu.verified_emulator_pid=lambda pid,target:(pid,target)
    emu.find_emulator_pid=lambda target:(42,target)
    with patch.dict(sys.modules, {'autosplitter': types.ModuleType('autosplitter'),
                                  'autosplitter.memory':mem,
                                  'practice': types.ModuleType('practice'),
                                  'practice.entrances':ent,
                                  'practice.emulator_savestates':emu}):
        import importlib.util
        path=Path(__file__).resolve().parents[1]/'practice'/'japan_mupen_rdram.py'
        spec=importlib.util.spec_from_file_location('japan_mupen_probe_test_module',path)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


mod=_load_module()


def synth(endian='wordswapped'):
    rom=bytearray(0x50000)
    rom[0xC00:0xD00]=bytes((i*7+1)&0xff for i in range(256))
    for off in mod.FINGERPRINT_OFFSETS:
        for i in range(64):
            rom[off+mod.ROM_RAM_OFFSET+i]=(off//0x10000 * 37 + i*17+5)&0xff
    ram=bytearray(mod.RDRAM_MIN_SIZE)
    for off,p in zip(mod.FINGERPRINT_OFFSETS,mod.fingerprints(rom,endian)):
        ram[off:off+len(p)]=p
    return bytes(rom),ram


class TestJapaneseMupenProbe(unittest.TestCase):
    def test_accepts_correct_japanese_rom_and_rejects_modified_hash(self):
        import hashlib
        rom=bytearray(0x1000000)
        rom[:4]=bytes.fromhex('80371240')
        rom[0x3B:0x3F]=b'NG5J'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'owned.jp.z64'
            p.write_bytes(rom)
            with patch.object(mod,'JP_ORIGINAL_SHA1',hashlib.sha1(rom).hexdigest()):
                self.assertEqual(mod.checked_japan_rom(p), bytes(rom))
                rom[0x500] ^= 0xFF
                p.write_bytes(rom)
                with self.assertRaisesRegex(ValueError,'revision/hash'):
                    mod.checked_japan_rom(p)

    def test_finds_unique_wordswapped_and_big_endian_ram(self):
        for endian in ('big','wordswapped'):
            rom,ram=synth(endian)
            p=FakeProcess([(0x20000000,ram)])
            result=mod.find_japanese_rdram(p,rom,[(0x20000000,len(ram))],max_scan_bytes=8*1024*1024)
            self.assertEqual(result,(0x20000000,endian))
            self.assertEqual(p.writes,[])

    def test_manual_base_validation_prevents_rom_decoy(self):
        rom,ram=synth('big')
        p=FakeProcess([(0x20000000,ram)])
        with patch.object(mod,'checked_japan_rom',return_value=rom), \
             patch.object(mod,'HostProcess',return_value=p):
            proc,mem=mod.attach_japanese_mupen(42,Path('/unused'),0x20000000)
            self.assertIs(proc,p)
            self.assertEqual(mem.base,0x20000000)
            self.assertEqual(mem.endian,'big')
        # A RAM-like match which contains the ROM bootcode at the false base
        # is rejected even when the supplied base was explicit.
        decoy=bytearray(ram)
        decoy[:256]=rom[0xC00:0xD00]
        p=FakeProcess([(0x20000000,decoy)])
        with patch.object(mod,'checked_japan_rom',return_value=rom), \
             patch.object(mod,'HostProcess',return_value=p):
            with self.assertRaisesRegex(ValueError,'cartridge ROM buffer'):
                mod.attach_japanese_mupen(42,Path('/unused'),0x20000000)

        def test_rejects_single_anchor_match(self):
        rom,ram=synth('big')
        ram[0x30000]^=0xff
        p=FakeProcess([(0x20000000,ram)])
        with self.assertRaisesRegex(RuntimeError,'No verified'):
            mod.find_japanese_rdram(p,rom,[(0x20000000,len(ram))])

    def test_rejects_ambiguous_ram_copies(self):
        rom,ram=synth('big')
        p=FakeProcess([(0x20000000,ram),(0x30000000,bytearray(ram))])
        with self.assertRaisesRegex(RuntimeError,'Multiple possible'):
            mod.find_japanese_rdram(p,rom,[(0x20000000,len(ram)),(0x30000000,len(ram))])

    def test_rejects_rom_image_decoy(self):
        rom,ram=synth('big')
        # An in-memory game ROM has the same code anchors 0xC00 bytes later.
        rom_blob=bytearray(0x1000000)
        rom_blob[:len(rom)]=rom
        p=FakeProcess([(0x30000000,rom_blob)])
        with self.assertRaisesRegex(RuntimeError,'No verified'):
            mod.find_japanese_rdram(p,rom,[(0x30000000,len(rom_blob))])

    def test_scan_budget_blocks_extra_regions(self):
        rom,ram=synth('big')
        p=FakeProcess([(0x20000000,bytearray(len(ram))),(0x30000000,ram)])
        with self.assertRaisesRegex(RuntimeError,'No verified'):
            mod.find_japanese_rdram(p,rom,[(0x20000000,len(ram)),(0x30000000,len(ram))],
                                    max_scan_bytes=len(ram))


if __name__=='__main__':
    unittest.main()

import unittest
import hashlib
import json
import struct
from pathlib import Path
import importlib.util

ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('slotcheck',ROOT/'verify_rom_pointer_slots.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class OriginalPointerSlotProofTest(unittest.TestCase):
    def test_signed_16(self):
        self.assertEqual(mod.sign16(0xc5c8),-0x3a38)
        self.assertEqual(mod.sign16(0x1db8),0x1db8)
    def test_known_region_pair(self):
        self.assertEqual(mod.EXPECTED['japan']-mod.EXPECTED['usa'],0x57f0)
    def test_bad_rom_rejected(self):
        with self.assertRaisesRegex(ValueError,'not 16 MiB'):
            mod.prove('usa',b'not a ROM')
    def test_decode_registers(self):
        # Synthetic independently authored MIPS test words; not original instructions.
        w=(15<<26)|(0<<21)|(2<<16)|0x1234
        self.assertEqual((mod.op(w),mod.rs(w),mod.rt(w),mod.imm(w)),(15,0,2,0x1234))
    def test_metadata_mirrored_and_read_only(self):
        meta=json.loads((ROOT/'crosswalk.json').read_text())
        proof=json.loads((ROOT/'original_rom_pointer_proof.json').read_text())
        entries=meta['entries']
        self.assertEqual(len(entries),2)
        for e in entries:
            other='usa' if e['region']=='japan' else 'japan'
            self.assertEqual(e['address'],proof[e['region']]['symbol_slot'])
            self.assertEqual(e['counterpart'],proof[other]['symbol_slot'])
            self.assertEqual(e['width'],4)
            self.assertFalse(e['may_auto_write'])
            self.assertFalse(e['live_readable'])
        self.assertFalse(meta['gameplay_verified'])
    def test_synthetic_japan_lw_layout_and_bad_opcode(self):
        # Synthetic ROM only: override SHA gate solely for this unit test.
        sample=bytearray(16_777_216)
        sample[:4]=b'\x80\x37\x12\x40'
        struct.pack_into('>I',sample,0x4D70,(15<<26)|(2<<16)|0x8016)
        struct.pack_into('>I',sample,0x4D74,(35<<26)|(2<<21)|(2<<16)|0x1DB8)
        old=mod.SHA['japan']
        try:
            mod.SHA['japan']=hashlib.sha1(sample).hexdigest()
            self.assertEqual(mod.prove('japan',bytes(sample))['symbol_slot'],'0x80161DB8')
            # Change LW to SW and make SHA admissible again to reach opcode check.
            struct.pack_into('>I',sample,0x4D74,(43<<26)|(2<<21)|(2<<16)|0x1DB8)
            mod.SHA['japan']=hashlib.sha1(sample).hexdigest()
            with self.assertRaisesRegex(ValueError,'not expected LW'):
                mod.prove('japan',bytes(sample))
        finally:
            mod.SHA['japan']=old
    def test_synthetic_usa_store_layout(self):
        sample=bytearray(16_777_216)
        sample[:4]=b'\x80\x37\x12\x40'
        struct.pack_into('>I',sample,0x4D8C,(15<<26)|(2<<16)|0x8016)
        struct.pack_into('>I',sample,0x4D94,(9<<26)|(2<<21)|(2<<16)|0xC5C8)
        struct.pack_into('>I',sample,0x4D9C,(43<<26)|(2<<21)|(14<<16))
        old=mod.SHA['usa']
        try:
            mod.SHA['usa']=hashlib.sha1(sample).hexdigest()
            self.assertEqual(mod.prove('usa',bytes(sample))['symbol_slot'],'0x8015C5C8')
        finally:
            mod.SHA['usa']=old
    def test_instruction_mutation_rejected(self):
        # Never retain altered ROM bytes: SHA1 must gate before decoding.
        # A synthetic correctly sized N64 image reaches the SHA gate,
        # so no unverified opcode can be interpreted as source evidence.
        buf=bytearray(16_777_216)
        buf[0:4]=b'\x80\x37\x12\x40'
        with self.assertRaisesRegex(ValueError,'SHA1 mismatch'):
            mod.prove('usa',bytes(buf))

if __name__=='__main__':unittest.main()

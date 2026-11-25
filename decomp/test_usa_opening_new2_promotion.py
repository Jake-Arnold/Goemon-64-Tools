"""ROM-free invariants for exact original USA file18 48B+44B C stage."""
import copy
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from decomp import usa_opening_new2_promotion as stage
from decomp import verify


def synthetic_mips_object(name='D_CF8F8', info=0x11, machine=8):
    """Generate an original authored synthetic ELF32, not game ASM/data."""
    buf=bytearray(0x300)
    buf[:16]=b'\x7fELF\x01\x02\x01'+bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH',buf,16,1,machine,1,0,0,0x100,0,52,0,0,40,6,5)
    buf[0x40:0x48]=b'\0'*8
    buf[0x48:0x50]=bytes(8)
    strings=('\0'+name+'\0').encode()
    buf[0x70:0x70+len(strings)]=strings
    names=b'\0.text\0.rel.text\0.symtab\0.strtab\0.shstrtab\0'
    buf[0xa0:0xa0+len(names)]=names
    # One all-zero ELF symbol, then one undefined GLOBAL object (candidate source datum).
    struct.pack_into('>IIIBBH',buf,0x60,1,0,0,info,0,0)
    headers=[(0,0,0,0,0,0,0,0,0,0),
             (1,1,6,0,0x40,8,0,0,4,0),
             (7,9,0,0,0x48,8,3,1,4,8),
             (17,2,0,0,0x50,32,4,1,4,16),
             (25,3,0,0,0x70,len(strings),0,0,1,0),
             (33,3,0,0,0xa0,len(names),0,0,1,0)]
    for i,x in enumerate(headers):struct.pack_into('>IIIIIIIIII',buf,0x100+i*40,*x)
    return bytes(buf)

class OpeningNew2Tests(unittest.TestCase):
    def test_frozen_fixture_and_original_offsets(self):
        d=stage.fixture();self.assertEqual(len(d['functions']),2)
        self.assertEqual(sum(f['size'] for f in d['functions']),92)
        self.assertEqual(tuple((f['name'],f['rom_offset'],f['vma'],f['size']) for f in d['functions']),stage.EXPECTED)
    def test_current_claims_are_exactly_post2090(self):
        m=verify.load_manifest(verify.ROOT/'results/manifest_2354_before_batch302.json');m.pop('overlay_usa_short72_stage',None);fs=verify.claimed_functions(m)
        self.assertEqual(len(fs),2092)
        self.assertEqual(sum(f['size'] for f in fs),94760)
        old={k:v for k,v in m.items() if k!='overlay_usa_opening_new2_stage'}
        self.assertEqual(len(verify.claimed_functions(old)),2090)
        self.assertEqual(sum(f['size'] for f in verify.claimed_functions(old)),94668)
    def test_duplicate_and_bad_stage_rejected(self):
        m=verify.load_manifest(verify.ROOT/'results/manifest_2354_before_batch302.json');m['overlay_usa_opening_new2_stage']['format']='bad'
        with self.assertRaises(ValueError):stage.validate_predecessor(m)
    def test_unreviewed_source_hash_rejected(self):
        with patch.object(stage,'FIXTURE_HASH','0'*64):
            with self.assertRaises(ValueError):stage.fixture()
    def test_metadata_only_corrects_one_symbol_byte(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'native.o';raw=synthetic_mips_object();p.write_bytes(raw)
            rec=stage.patch_absolute_symbol_type(p)
            after=p.read_bytes()
            self.assertEqual(len(after),len(raw))
            self.assertEqual(sum(a!=b for a,b in zip(after,raw)),1)
            self.assertEqual(after[0x60+12],0x10)
            self.assertEqual(after[0x40:0x50],raw[0x40:0x50])
            self.assertTrue(rec['native_MIPS_instructions_untouched'])
    def test_wrong_original_symbol_type_rejected_without_change(self):
        for kind in (0x10,0x12,0x01):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                p=Path(d)/'native.o';raw=synthetic_mips_object(info=kind);p.write_bytes(raw)
                with self.assertRaises(ValueError):stage.patch_absolute_symbol_type(p)
                self.assertEqual(p.read_bytes(),raw)
    def test_wrong_symbol_name_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'native.o';raw=synthetic_mips_object(name='D_WRONG');p.write_bytes(raw)
            with self.assertRaises(ValueError):stage.patch_absolute_symbol_type(p)
            self.assertEqual(p.read_bytes(),raw)
    def test_wrong_machine_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'native.o';raw=synthetic_mips_object(machine=62);p.write_bytes(raw)
            with self.assertRaises(ValueError):stage.patch_absolute_symbol_type(p)
            self.assertEqual(p.read_bytes(),raw)

if __name__=='__main__':unittest.main()

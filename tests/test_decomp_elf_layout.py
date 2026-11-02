"""Synthetic MIPS objects only: no retail instructions or jump targets."""
from pathlib import Path
import struct
import tempfile
import unittest
from decomp.elf_layout import pack_vm_assignment_rodata, pack_object_file


def fixture():
    names=b'\0.text\0.rodata\0.rel.rodata\0.symtab\0.strtab\0.shstrtab\0'
    data=bytearray(52)
    sections=[(0,)*10]
    def section(name,kind,flags,payload,link=0,info=0,align=4,entry=0):
        offset=len(data);data.extend(payload)
        sections.append((names.index(name+b'\0'),kind,flags,0,offset,len(payload),link,info,align,entry))
    section(b'.text',1,6,b'\x11\x22\x33\x44')
    section(b'.rodata',1,2,bytes(range(60))+bytes(4),align=16)
    section(b'.rel.rodata',9,0,b''.join(struct.pack('>II',i,0x102) for i in range(0,60,4)),4,2,entry=8)
    section(b'.symtab',2,0,bytes(16)+struct.pack('>IIIBBH',0,0,0,3,0,1),5,2,entry=16)
    section(b'.strtab',3,0,b'\0',align=1)
    section(b'.shstrtab',3,0,names,align=1)
    shoff=len(data)
    for header in sections:data.extend(struct.pack('>10I',*header))
    data[:16]=b'\x7fELF\x01\x02\x01'+bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH',data,16,1,8,1,0,0,shoff,0,52,0,0,40,7,6)
    return data,sections,shoff


class ElfLayoutTests(unittest.TestCase):
    def test_only_two_section_metadata_fields_change(self):
        original,sections,shoff=fixture()
        packed,evidence=pack_vm_assignment_rodata(original)
        allowed=set(range(shoff+80+20,shoff+80+24))|set(range(shoff+80+32,shoff+80+36))
        self.assertEqual(len(original),len(packed))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(original,packed))))
        for s in sections:self.assertEqual(original[s[4]:s[4]+s[5]],packed[s[4]:s[4]+s[5]])
        self.assertEqual(struct.unpack_from('>I',packed,shoff+100)[0],60)
        self.assertEqual(struct.unpack_from('>I',packed,shoff+112)[0],4)
        self.assertEqual(evidence['relocations_retained'],15)
        self.assertEqual(evidence['payload_bytes_changed'],0)
        with self.assertRaises(ValueError):pack_vm_assignment_rodata(packed)

    def test_malformed_layout_rejected(self):
        original,sections,shoff=fixture()
        mutations=[(5,b'\x01'),(18,b'\0\x03'),(sections[2][4]+60,b'\x01'),
            (shoff+100,struct.pack('>I',60)),(shoff+112,struct.pack('>I',8)),
            (shoff+3*40+20,struct.pack('>I',112)),
            (sections[3][4],struct.pack('>I',4)),
            (sections[3][4]+4,struct.pack('>I',0x103)),
            (sections[3][4]+4,struct.pack('>I',0x202)),
            (sections[4][4]+16+14,struct.pack('>H',2)),
            (shoff+3*40+28,struct.pack('>I',1))]
        for offset,value in mutations:
            with self.subTest(offset=offset,value=value):
                changed=original.copy();changed[offset:offset+len(value)]=value
                with self.assertRaises(ValueError):pack_vm_assignment_rodata(changed)
        # A symbol at the discarded padding boundary must be rejected.
        changed=original.copy()
        struct.pack_into('>I',changed,sections[4][4]+16+4,60)
        struct.pack_into('>H',changed,sections[4][4]+16+14,2)
        with self.assertRaises(ValueError):pack_vm_assignment_rodata(changed)
        for short in (b'',bytes(original[:30]),bytes(original[:-1])):
            with self.assertRaises(ValueError):pack_vm_assignment_rodata(short)

    def test_file_backup_is_exclusive_and_validation_precedes_writes(self):
        original,_,_=fixture()
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'synthetic.o';path.write_bytes(original)
            pack_object_file(path)
            backup=Path(str(path)+'.before-layout')
            self.assertEqual(backup.read_bytes(),original)
            path.write_bytes(original)
            with self.assertRaises(FileExistsError):pack_object_file(path)
            self.assertEqual(path.read_bytes(),original)
            path.write_bytes(b'bad')
            with self.assertRaises(ValueError):pack_object_file(path)
            self.assertEqual(path.read_bytes(),b'bad')

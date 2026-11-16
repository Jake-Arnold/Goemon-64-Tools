"""ROM-free ELF tests: relocation-preserving section-header trim."""
import struct
import unittest
from decomp.research.trim_elf32_mips_text import trim_text_section


def fixture(rel_offset=4, bad_tail=False):
    names=b"\0.text\0.rel.text\0.shstrtab\0"
    offsets={".text":1,".rel.text":7,".shstrtab":17}
    raw=bytearray(320)
    raw[:6]=b'\x7fELF\x01\x02'
    struct.pack_into('>H',raw,16,1)      # ET_REL
    struct.pack_into('>H',raw,18,8)      # EM_MIPS
    struct.pack_into('>I',raw,32,160)    # e_shoff
    struct.pack_into('>HHH',raw,46,40,4,3)
    raw[64:84] = b'\x12\x34\x56\x78'*5
    if bad_tail:raw[84]=1
    struct.pack_into('>II',raw,96,rel_offset,2)  # one ELF32 Rel
    raw[112:112+len(names)]=names
    def section(idx,name,typ,offset,length,align=4):
        sh=160+idx*40
        struct.pack_into('>II',raw,sh,offsets[name],typ)
        struct.pack_into('>II',raw,sh+16,offset,length)
        struct.pack_into('>I',raw,sh+32,align)
    section(1,'.text',1,64,32,16)
    section(2,'.rel.text',9,96,8,4)
    section(3,'.shstrtab',3,112,len(names),1)
    return bytes(raw)


class ElfTrimTest(unittest.TestCase):
    def test_shortens_section_without_stripping_relocation(self):
        original=fixture()
        altered=trim_text_section(original,20)
        self.assertEqual(len(altered),len(original))
        self.assertEqual(struct.unpack_from('>I',altered,200+20)[0],20)
        self.assertEqual(struct.unpack_from('>I',altered,200+32)[0],4)
        self.assertEqual(altered[64:112],original[64:112])
        self.assertEqual(altered[96:104],original[96:104])
        for i,(a,b) in enumerate(zip(original,altered)):
            if i not in list(range(220,224))+list(range(232,236)):
                self.assertEqual(a,b)

    def test_rejects_nonzero_trimmed_bytes(self):
        with self.assertRaisesRegex(ValueError,'Nonzero'):
            trim_text_section(fixture(bad_tail=True),20)

    def test_rejects_truncated_relocation(self):
        with self.assertRaisesRegex(ValueError,'relocation'):
            trim_text_section(fixture(rel_offset=20),20)

    def test_rejects_bad_elf_and_length(self):
        with self.assertRaises(ValueError):trim_text_section(b'\0'*320,20)
        with self.assertRaises(ValueError):trim_text_section(fixture(),36)
        with self.assertRaises(ValueError):trim_text_section(fixture(),19)


if __name__ == '__main__':
    unittest.main()
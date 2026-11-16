"""ROM-free fail-closed tests for Japanese 18-C staging and ELF metadata packing."""
from __future__ import annotations
from pathlib import Path
import struct
import tempfile
import unittest
from decomp import japan_eighteen_c as jp
from decomp.japan_relocation_policy import REVIEWED, verify_text_relocations


def fake_elf(*, rel_offset=12, nonzero=False, code_len=56):
    data=bytearray(280)
    data[:6]=b'\x7fELF\x01\x02'
    struct.pack_into('>H',data,16,1)
    struct.pack_into('>I',data,32,160)
    struct.pack_into('>H',data,46,40)
    struct.pack_into('>H',data,48,3)
    data[64:64+code_len]=b'\x11'*code_len
    if nonzero:data[64+code_len]=1
    off=160+40
    struct.pack_into('>II',data,off+4,1,6)
    struct.pack_into('>III',data,off+16,64,64,0)
    struct.pack_into('>I',data,off+32,16)
    off=160+80
    struct.pack_into('>I',data,off+4,9)
    struct.pack_into('>I',data,off+16,128)
    struct.pack_into('>I',data,off+20,8)
    struct.pack_into('>I',data,off+28,1)
    struct.pack_into('>I',data,128,rel_offset)
    return bytes(data)


class Japanese18CStructureTests(unittest.TestCase):
    def test_staging_preserves_all_known_main_boundaries(self):
        base='sha1: '+jp.PINNED_SHA1+'\n'
        keys=[old.replace(', asm,',', c,') for old,_ in jp.SEGMENTS]
        base+='\n'.join(keys)+'\n'
        for i in range(189-len(keys)):
            base+=f'    - [0x{0x800000+i*16:X}, c, dummy{i}]\n'
        out=jp.render_config(base)
        self.assertEqual(out.count(', c,'),14)
        for _,replacement in jp.SEGMENTS:
            self.assertIn(replacement,out)
        with self.assertRaisesRegex(ValueError,'189'):
            jp.render_config(base[:-1].replace('dummy0','absent',1).replace(', c, dummy1',', asm, dummy1'))
        with self.assertRaisesRegex(ValueError,'ROM'):
            jp.render_config(base.replace(jp.PINNED_SHA1,'0'*40))

    def test_generated_staging_refuses_user_edited_source(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/'repo';source.joinpath('japan_matching').mkdir(parents=True)
            for name in jp.SOURCE_NAMES:
                (source/'japan_matching'/(name+'.c')).write_text('void original(void) {}')
            jp.install_sources(root,source)
            altered=root/'src/jp_warp_37920.c'
            altered.write_text('void user_override(void){}')
            with self.assertRaises(FileExistsError):jp.install_sources(root,source)

    def test_section_trim_changes_only_elf_metadata(self):
        raw=fake_elf()
        packed,proof=jp.pack_text_metadata(raw,56)
        self.assertEqual(proof['zero_bytes_trimmed'],8)
        self.assertEqual(proof['relocations_preserved'],1)
        self.assertEqual(len(raw),len(packed))
        self.assertEqual(raw[64:160],packed[64:160])
        self.assertEqual(struct.unpack_from('>I',packed,200+20)[0],56)
        self.assertEqual(struct.unpack_from('>I',packed,200+32)[0],4)
        self.assertEqual(proof['bytes_changed'],2)

    def test_rejects_nonzero_alignment_padding(self):
        with self.assertRaisesRegex(ValueError,'Nonzero'):
            jp.pack_text_metadata(fake_elf(nonzero=True),56)

    def test_rejects_relocation_into_trimmed_padding(self):
        with self.assertRaisesRegex(ValueError,'Relocation'):
            jp.pack_text_metadata(fake_elf(rel_offset=60),56)

    def test_rejects_unexpected_elf_layout(self):
        with self.assertRaisesRegex(ValueError,'ELF'):
            jp.pack_text_metadata(b'bad',56)
        with self.assertRaisesRegex(ValueError,'extent'):
            jp.pack_text_metadata(fake_elf(),68)

    def test_18_c_layout_has_fourteen_source_units(self):
        self.assertEqual(len(jp.SOURCE_NAMES),14)
        self.assertEqual(len(jp.REVIEWED),8)
        self.assertEqual(sum(size for _stem,_fn,size in jp.REVIEWED),476)

    def test_exact_relocation_signatures_fail_closed(self):
        for source,expected in REVIEWED.items():
            body='\n'.join(' '.join(row) for row in expected)
            self.assertEqual(verify_text_relocations(source,body),len(expected))
            if expected:
                with self.assertRaisesRegex(ValueError,'Unreviewed'):
                    verify_text_relocations(source,body.replace(expected[0][2],'wrong_symbol',1))
        self.assertEqual(verify_text_relocations('japan_matching/jp_bit_array.c',''),0)

if __name__=='__main__':unittest.main()

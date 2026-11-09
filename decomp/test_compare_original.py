"""Synthetic safety controls for compare_original; no copyrighted ROM inputs."""
import hashlib
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import compare_original as mod

NAME = "func_8003DE80_3EA80"
VMA = 0x8003DE80
OFF = 0x3EA80

def asm(rows):
    return "glabel " + NAME + "\n" + "\n".join(
        f"/* {OFF+4*i:X} {VMA+4*i:08X} {word:08X} */ {op}"
        for i, (word, op) in enumerate(rows)
    ) + "\nendlabel " + NAME + "\n"

class ComparisonSafety(unittest.TestCase):
    def test_original_range_and_relocations(self):
        off, rows = mod.original_rows(asm([
            (0x27bdffd8, 'addiu $sp, $sp, -0x28'),
            (0x3c02801c, 'lui $v0, %hi(D_801C77E8)'),
            (0x0c004000, 'jal callback')]), NAME)
        self.assertEqual(off, OFF)
        self.assertEqual(rows, [(0x27bdffd8,None),(0x3c02801c,'HI16'),(0x0c004000,'26')])

    def test_function_scope_ignores_neighbor_functions(self):
        before = 'glabel other\\n/* 3EA7C 8003DE7C 00000000 */ nop\\nendlabel other\\n'
        after = 'glabel next\\n/* 3EA84 8003DE84 00000000 */ nop\\nendlabel next\\n'
        off, rows = mod.original_rows(before + asm([(0x27bdffd8, 'addiu $sp, $sp, -0x28')]) + after, NAME)
        self.assertEqual((off, rows), (OFF, [(0x27bdffd8, None)]))

    def test_nested_or_duplicate_labels_rejected(self):
        body = asm([(0x27bdffd8, 'addiu $sp, $sp, -0x28')])
        with self.assertRaisesRegex(ValueError, 'ambiguous duplicate'):
            mod.original_rows(body + body, NAME)
        with self.assertRaisesRegex(ValueError, 'nested or overlapping'):
            mod.original_rows(body.replace('endlabel '+NAME, 'glabel next\\nendlabel next\\nendlabel '+NAME), NAME)

    def test_duplicate_and_gapped_address_rejected(self):
        line = f'/* {OFF:X} {VMA:08X} 00000000 */ nop'
        with self.assertRaisesRegex(ValueError, 'noncontiguous'):
            mod.original_rows('glabel '+NAME+'\n'+line+'\n'+line+'\nendlabel '+NAME, NAME)
        with self.assertRaisesRegex(ValueError, 'noncontiguous'):
            mod.original_rows('glabel '+NAME+'\n/* 3EA84 8003DE80 00000000 */ nop\nendlabel '+NAME, NAME)

    def test_wrong_label_and_function_mapping_rejected(self):
        with self.assertRaisesRegex(ValueError, 'missing original function label'):
            mod.original_rows('glabel wrong\nendlabel wrong',NAME)
        with self.assertRaisesRegex(ValueError, 'mapping'):
            mod.original_rows('glabel func_8003DE80_3EA84', 'func_8003DE80_3EA84')

    def test_elf_header_wrong_arch_rejected(self):
        s = '  11: 00000000  12 FUNC GLOBAL DEFAULT 1 '+NAME
        with self.assertRaisesRegex(ValueError, 'ELF32'):
            mod.parse_elf_info('Class: ELF64\nData: 2\'s complement, big endian\nMachine: MIPS',s,NAME)
        with self.assertRaisesRegex(ValueError, 'MIPS'):
            mod.parse_elf_info('Class: ELF32\nData: 2\'s complement, big endian\nMachine: ARM',s,NAME)

    def test_duplicate_and_missing_symbol_rejected(self):
        header='Class: ELF32\nData: 2\'s complement, big endian\nMachine: MIPS'
        s='  11: 00000000  12 FUNC GLOBAL DEFAULT 1 '+NAME
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            mod.parse_elf_info(header,s+'\n'+s,NAME)
        with self.assertRaisesRegex(ValueError, 'missing'):
            mod.parse_elf_info(header,s,NAME+'BROKEN')

    def test_objdump_parses_mips_relocations(self):
        text='''Disassembly of section .text:
 00000000 <func>:
   0: 27bdffd8 addiu sp,sp,-40
   4: 3c028000 lui v0,0x8000
       4: R_MIPS_HI16 DATA
   8: 0c000000 jal 0
       8: R_MIPS_26 CALLBACK
'''
        self.assertEqual(mod.parse_objdump(text,0,12),[(0x27bdffd8,None),(0x3c028000,'HI16'),(0x0c000000,'26')])

    def test_objdump_truncated_and_unknown_reloc_rejected(self):
        text='Disassembly of section .text:\n  0: 27bdffd8 addiu sp,sp,-40\n'
        with self.assertRaisesRegex(ValueError,'incomplete'):
            mod.parse_objdump(text,0,8)
        with self.assertRaisesRegex(ValueError,'unsupported'):
            mod.parse_objdump(text+'  0: R_MIPS_TLS_DTPREL32 SOMETHING\n',0,4)

    def test_duplicate_disassembly_address_rejected(self):
        text=('Disassembly of section .text:\n'
              '  0: 27bdffd8 addiu sp,sp,-40\n'
              '  0: 27bdffd4 addiu sp,sp,-44\n')
        with self.assertRaisesRegex(ValueError, 'duplicate disassembled'):
            mod.parse_objdump(text, 0, 4)

    def test_same_symbol_size_does_not_imply_match(self):
        a=[(0x27bdffd8,None),(0x3c028000,'HI16'),(0x0c004000,'26')]
        b=[(0x27bdffd8,None),(0x3c028001,'HI16'),(0x0c000000,'26')]
        self.assertTrue(mod.comparison(a,b)['isolated_structural_match_only'])
        b[1]=(0x3c038001,'HI16')
        c=mod.comparison(a,b)
        self.assertFalse(c['isolated_structural_match_only'])
        self.assertEqual(c['matching_nonreloc_words'],1)
        self.assertEqual(c['relocation_layout_differences'],0)
        self.assertEqual(c['first_mismatches'],['+0x4'])
        b[1]=(0x3c028000,None)
        self.assertEqual(mod.comparison(a,b)['relocation_layout_differences'],1)

    def test_reference_hash_and_original_bytes_required(self):
        content = bytes.fromhex('27bdffd8 3c028000 0c004000')
        with tempfile.TemporaryDirectory() as d:
            rom=Path(d)/'reference.z64'
            rom.write_bytes(content)
            rows=[(int.from_bytes(content[i:i+4],'big'),None) for i in range(0,len(content),4)]
            with patch.object(mod,'ROM_SIZE',len(content)), patch.object(mod,'ROM_SHA1',hashlib.sha1(content).hexdigest()):
                mod.verify_rom(rom,0,rows)
                bad = list(rows);bad[1]=(0x3c038000,None)
                with self.assertRaisesRegex(ValueError,'instruction words'):
                    mod.verify_rom(rom,0,bad)
                rom.write_bytes(content[:-1]+b'\x01')
                with self.assertRaisesRegex(ValueError,'size/SHA-1'):
                    mod.verify_rom(rom,0,rows)

if __name__=='__main__':
    unittest.main()

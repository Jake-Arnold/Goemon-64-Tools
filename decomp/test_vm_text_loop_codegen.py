"""Unit tests for the isolated IDO VM text-loop instruction comparison tool."""
import unittest

from probe_vm_text_loop_codegen import parse_hexdump, parse_relocations, parse_symbol_size


class TestVmCodegenProbe(unittest.TestCase):
    def test_symbol_size(self):
        table = '   2: 00000000   472 FUNC    GLOBAL DEFAULT    4 func_8003DBEC_3E7EC\n'
        self.assertEqual(parse_symbol_size(table), (0, 472))
        with self.assertRaises(ValueError):
            parse_symbol_size(table.replace('FUNC', 'NOTYPE'))

    def test_original_word_hexdump(self):
        lines = ('Hex dump of section .text:\n'
                 '  0x00000000 27bdffb0 3c0e0000 afb00018 ....<...\n'
                 '  0x0000000c 24020001                            $...\n')
        self.assertEqual(parse_hexdump(lines),
                         {0: 0x27BDFFB0, 4: 0x3C0E0000, 8: 0xAFB00018, 12: 0x24020001})

    def test_relocation_offsets(self):
        lines = ('Relocation section .rel.text:\n'
                 '00000004  00000405 R_MIPS_HI16       00000000   foo\n'
                 '00000008  00000406 R_MIPS_LO16       00000000   foo\n'
                 '00000078  00000204 R_MIPS_26         00000000   bar\n')
        self.assertEqual(parse_relocations(lines), {4, 8, 0x78})


if __name__ == '__main__':
    unittest.main()

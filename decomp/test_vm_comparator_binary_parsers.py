"""Host-only unit and negative controls for the isolated comparator gate."""
import unittest

from test_vm_comparator_binary import read_symbol, read_text_words


class ComparatorGateParsing(unittest.TestCase):
    def test_elf_symbol(self):
        row = '  2: 00000000   340 FUNC    GLOBAL DEFAULT    4 func_8003D9B8_3E5B8'
        self.assertEqual(read_symbol(row), (0, 340))
        with self.assertRaises(ValueError):
            read_symbol(row.replace('FUNC', 'NOTYPE'))

    def test_undefined_symbol_rejected(self):
        row = '  2: 00000000   340 FUNC    GLOBAL DEFAULT  UND func_8003D9B8_3E5B8'
        with self.assertRaisesRegex(ValueError, 'defined in an ELF section'):
            read_symbol(row)

    def test_duplicate_symbol_rejected(self):
        row = '  2: 00000000   340 FUNC    GLOBAL DEFAULT    4 func_8003D9B8_3E5B8'
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            read_symbol(row + '\n' + row)

    def test_text_dump_discard_ascii(self):
        text = ('Hex dump of section .text:\n'
                '  0x00000000 34018002 14810005 00001825 14a6004f 4..........%...O\n'
                '  0x00000010 00000000 03e00008 24020001 34018003 ........$...4...\n')
        self.assertEqual(read_text_words(text), bytes.fromhex(
            '34018002148100050000182514a6004f0000000003e000082402000134018003'))

    def test_text_dump_gap_rejected(self):
        text = '  0x00000000 34018002\n  0x00000008 00000000\n'
        with self.assertRaisesRegex(ValueError, 'Discontinuous'):
            read_text_words(text)

    def test_text_dump_missing_rejected(self):
        with self.assertRaisesRegex(ValueError, 'No .text'):
            read_text_words('There are no instructions')


if __name__ == '__main__':
    unittest.main()

"""Synthetic negative controls for VM-loader original-address guard."""
import unittest
from test_vm_loader_original import EXPECTED, check, instruction_rows


class VmLoaderOriginalParser(unittest.TestCase):
    def test_duplicate_addresses_rejected(self):
        line = '/* 3E080 8003D480 00000000 */ bnez $t6, .L8003D490_3E090'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            instruction_rows(f'{line}\n{line}\n')

    def test_no_assembly_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'missing original instruction'):
            check('')

    def test_wrong_branch_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'expected'):
            check('/* 3E080 8003D480 00000000 */ beqz $t6, .L8003D490_3E090')

    def test_guards_unique(self):
        self.assertEqual(len(EXPECTED), len(set(EXPECTED)))
        self.assertIn(0x8003D4CC, EXPECTED)
        self.assertIn(0x8003D60C, EXPECTED)


if __name__ == '__main__':
    unittest.main()

"""ROM-free tests for independent Japanese ELF inventory and ownership."""
from __future__ import annotations
import copy
import unittest
from decomp import japan_inventory as inventory
from decomp import region_verify

F = '''80000400 g     F .entry 00000038 func_80000400_1000
80000400 g     O .entry 00000038 func_80000400_1000.NON_MATCHING
08000040 g     F .ipl3 00000fc0 __ipl3_textbin
08000040 g     O .ipl3 00000001 __ipl3_textbin.NON_MATCHING
80012160 g     F .main 00000020 func_80012160_12D60
80012f70 g     F .main 00000020 func_80012F70_13B70
800161f0 g     F .main 00000024 func_800161F0_16DF0
80016214 g     F .main 00000028 func_80016214_16E14
8001623c g     F .main 00000034 func_8001623C_16E3C
80036cd0 g     F .main 00000010 func_80036CD0_378D0
80036ce0 g     F .main 00000010 func_80036CE0_378E0
80036cf0 g     F .main 00000010 func_80036CF0_378F0
80036d00 g     F .main 00000020 func_80036D00_37900
80036c70 g     F .main 00000060 func_80036C70_37870
80036d20 g     F .main 00000038 func_80036D20_37920
80036f58 g     F .main 00000034 func_80036F58_37B58
8003704c g     F .main 00000038 func_8003704C_37C4C
80037084 g     F .main 00000034 func_80037084_37C84
800370b8 g     F .main 00000028 func_800370B8_37CB8
800370e0 g     F .main 0000003c func_800370E0_37CE0
8003711c g     F .main 00000040 func_8003711C_37D1C
80037a20 g     F .main 00000008 func_80037A20_38620
801d0000 g     F .file_11 00000028 func_801D0000_100000
801d0000 g     O .file_11 00000028 func_801D0000_100000.NON_MATCHING
801d0000 g     F .file_12 00000028 func_801D0000_200000
801d0000 g     O .file_12 00000028 func_801D0000_200000.NON_MATCHING
801d0000 g     O .file_12 00000001 D_801D0000_200000.NON_MATCHING
'''


class JapaneseInventoryTests(unittest.TestCase):
    def setUp(self):
        self.manifest = region_verify.load_manifest()

    def test_counts_claimed_c_and_asm_by_section_not_vma(self):
        result = inventory.summarize_symbols(F, self.manifest)
        self.assertEqual(result['identified_positive_size_elf_entries'], 22)
        self.assertEqual(result['assembly_marked_entries'], 4)
        self.assertEqual(result['reviewed_matching_c_entries'], 18)
        self.assertEqual(result['section_count'], 5)
        self.assertEqual(result['same_section_address_size_aliases'], 0)
        self.assertEqual(result['nonfunction_NON_MATCHING_markers_excluded'], 1)
        self.assertEqual(result['reviewed_matching_c_bytes'], 756)

    def test_refuses_extra_unmarked_function(self):
        with self.assertRaisesRegex(ValueError, 'ownership differs'):
            inventory.summarize_symbols(F + '80042000 g     F .main 00000008 extra\n', self.manifest)

    def test_refuses_false_matching_c_or_incorrect_extent(self):
        with self.assertRaisesRegex(ValueError, 'ownership differs'):
            inventory.summarize_symbols(F + '800161f0 g     O .main 00000024 func_800161F0_16DF0.NON_MATCHING\n', self.manifest)
        with self.assertRaisesRegex(ValueError, 'extent'):
            inventory.summarize_symbols(F.replace('00000034 func_8001623C_16E3C', '00000030 func_8001623C_16E3C'), self.manifest)

    def test_duplicates_and_missing_functions_fail(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            inventory.summarize_symbols(F + '800161f0 g     F .main 00000024 func_800161F0_16DF0\n', self.manifest)
        with self.assertRaisesRegex(ValueError, 'No executable'):
            inventory.summarize_symbols('', self.manifest)

    def test_mismatched_asm_marker_and_same_vma_overlay(self):
        with self.assertRaisesRegex(ValueError, 'ASM marker'):
            inventory.summarize_symbols(F.replace('801d0000 g     O .file_12', '801d0004 g     O .file_12', 1), self.manifest)
        self.assertTrue(inventory.is_executable_section('.file_1024'))
        self.assertFalse(inventory.is_executable_section('.file_data'))


if __name__ == '__main__':
    unittest.main()

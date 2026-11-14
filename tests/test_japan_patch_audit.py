"""ROM-free tests for the isolated JP audio patch audit."""
import struct
import unittest
from unittest.mock import patch

from decomp import japan_patch_audit as a
from decomp.japan_function_map import MAIN_END, MAIN_START, MAIN_VRAM


def synthetic_roms():
    usa = bytearray(MAIN_END['usa'] + 64)
    japan = bytearray(MAIN_END['japan_0'] + 64)
    uspos = MAIN_START + a.USA_ENTRYPOINT - MAIN_VRAM
    jppos = MAIN_START + 0x80037E80 - MAIN_VRAM
    count = a.USA_SIZE // 4
    for n in range(count):
        inst = (0x23 << 26) | (((n % 11) + 1) << 21) | (((n*3 % 19) + 1) << 16) | (n+5)
        struct.pack_into('>I', usa, uspos + 4*n, inst)
        struct.pack_into('>I', japan, jppos + 4*n, (inst & 0xFFFF0000) | (n+11))
    struct.pack_into('>I', usa, uspos+a.USA_PATCH-a.USA_ENTRYPOINT, a.EXPECTED_OLD)
    struct.pack_into('>I', japan, jppos+a.USA_PATCH-a.USA_ENTRYPOINT, a.EXPECTED_OLD)
    return usa, japan, uspos, jppos


class PatchAuditTests(unittest.TestCase):
    def test_patches_identical_expected_instruction_with_complete_shape(self):
        usa, jp, _, _ = synthetic_roms()
        report = a.audit_patch(bytes(usa), bytes(jp))
        self.assertEqual(report['japan_function_vram'], '0x80037E80')
        self.assertEqual(report['japan_patch_vram'], '0x80037F00')
        self.assertEqual(report['structurally_equal_words'], 109)

    def test_rejects_bad_us_original_opcode(self):
        usa, jp, pos, _ = synthetic_roms()
        struct.pack_into('>I', usa, pos + 0x80, 0)
        with self.assertRaisesRegex(ValueError, 'USA original'):
            a.audit_patch(bytes(usa), bytes(jp))

    def test_rejects_wrong_japanese_opcode(self):
        usa, jp, _, pos = synthetic_roms()
        struct.pack_into('>I', jp, pos + 0x80, 0x00E3082A)
        with self.assertRaisesRegex(ValueError, 'Japanese original'):
            a.audit_patch(bytes(usa), bytes(jp))

    def test_rejects_changed_opcode_in_long_function(self):
        usa, jp, _, pos = synthetic_roms()
        struct.pack_into('>I', jp, pos + 0xA0, 0xFFFFFFFF)
        with self.assertRaisesRegex(ValueError, 'complete normalized'):
            a.audit_patch(bytes(usa), bytes(jp))

    def test_rejects_duplicate_japanese_entrypoint(self):
        usa, jp, _, pos = synthetic_roms()
        words=bytes(jp[pos:pos+64])
        jp[0x12000:0x12040]=words
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            a.audit_patch(bytes(usa), bytes(jp))


if __name__=='__main__':
    unittest.main()

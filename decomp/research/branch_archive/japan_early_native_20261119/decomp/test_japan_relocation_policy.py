"""Synthetic exact-relocation tests; no game content required."""
from __future__ import annotations
import unittest
from decomp.japan_relocation_policy import (MODE_RELOCATIONS, MODE_SOURCE, WARP_RELOCATIONS,
                                             WARP_SOURCE, verify_text_relocations)


class JapaneseRelocationPolicyTests(unittest.TestCase):
    def setUp(self):
        self.dump = "\n".join(
            f"{addr} {kind} {symbol}" for addr, kind, symbol in MODE_RELOCATIONS
        )

    def test_six_reviewed_g_system_relocations(self):
        self.assertEqual(verify_text_relocations(MODE_SOURCE, self.dump), 6)

    def test_one_reviewed_warp_call_relocation(self):
        call = "00000008 R_MIPS_26 func_8000364C_424C"
        self.assertEqual(verify_text_relocations(WARP_SOURCE, call), 1)
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(WARP_SOURCE, call.replace("424C", "424D"))
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(MODE_SOURCE, call)

    def test_old_japanese_c_still_forbids_any_relocations(self):
        self.assertEqual(verify_text_relocations("japan_matching/jp_bit_array.c", ""), 0)
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations("japan_matching/jp_camera_13B70.c", self.dump)

    def test_target_symbol_address_and_reloc_order_must_match(self):
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(MODE_SOURCE, self.dump.replace("g_system", "g_other", 1))
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(MODE_SOURCE, self.dump.replace("0000000c", "00000010", 1))
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(MODE_SOURCE, self.dump.replace("R_MIPS_LO16", "R_MIPS_26", 1))
        with self.assertRaisesRegex(ValueError, "Unreviewed"):
            verify_text_relocations(MODE_SOURCE, self.dump + "\n00000030 R_MIPS_LO16 g_system")

    def test_no_silent_unparsed_records(self):
        with self.assertRaisesRegex(ValueError, "Unparsed"):
            verify_text_relocations(MODE_SOURCE, "RELOCATION RECORDS FOR [.text]:\nundecodable")


if __name__ == "__main__":
    unittest.main()

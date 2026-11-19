"""ROM-free metadata checks for the independent USA file11 next-eight native scratch."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "decomp/research/file11_next8_group.c"
PROOF = ROOT / "decomp/results/file11_next8_scratch_proof_20261116.json"

class NextEightScratchTests(unittest.TestCase):
    def test_source_hash_and_exact_functions(self):
        data = SRC.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), "7919d61ac0453f342629d51186b1ddf16f3716f527b411c93716815941122d60")
        src = data.decode("utf-8")
        self.assertNotIn("GLOBAL_ASM", src)
        self.assertNotIn("#include", src)
        found = re.findall(r"^void (func_[0-9A-F]+_[0-9A-F]+)\(", src, re.M)
        expected = [
            f"func_{0x801EB020 + 44*i:08X}_{0x5A6F30 + 44*i:X}"
            for i in range(8)
        ]
        self.assertEqual(found, expected)
        for i in range(8):
            self.assertIn(f"func_801EB180_5A7090(actor, event, {i % 4});", src)

    def test_scope_and_original_contiguous_offsets(self):
        p = json.loads(PROOF.read_text(encoding="utf-8"))
        self.assertEqual(p["status"], "NATIVE_SCRATCH_VERIFIED_NOT_CENTRAL")
        self.assertEqual(p["production_baseline_matching_c"], 315)
        self.assertEqual(p["prospective_usa_matching_c_after_full_gates"], 323)
        self.assertEqual(p["candidate_new_instruction_bytes"], 352)
        rows = p["candidate_functions"]
        self.assertEqual(len(rows), 8)
        self.assertEqual([x["rom_offset"] for x in rows], [0x5A6F30 + 44*i for i in range(8)])
        self.assertEqual([x["size"] for x in rows], [44]*8)
        self.assertEqual([x["vma"] for x in rows], [0x801EB020 + 44*i for i in range(8)])
        self.assertEqual(rows[-1]["rom_offset"]+rows[-1]["size"], 0x5A7090)
        self.assertTrue(p["scratch_native_build"]["complete_rom_byte_equal"])
        self.assertTrue(p["scratch_native_build"]["site_type_symbol_relocation_multisets_equal"])
        self.assertEqual(p["scratch_native_build"]["original_file11_relocations"], 8825)

if __name__ == "__main__":
    unittest.main()

"""Regression tests for the standalone original-USA camera reset C candidate."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "decomp/research/camera_reset_usa_5b56e4.c"
EVIDENCE = ROOT / "decomp/results/camera_reset_136_native_research_20261116.json"


class CameraResetCMatchTests(unittest.TestCase):
    def test_fixture_source_hash_and_scope(self) -> None:
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        text = SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(text).hexdigest(), evidence["source_sha256"])
        self.assertNotIn(b"GLOBAL_ASM", text)
        self.assertNotIn(b"__asm", text)
        self.assertEqual(evidence["rom_range"], ["0x5B56E4", "0x5B576C"])
        self.assertEqual(evidence["size"], 136)
        self.assertEqual(evidence["production_status"], "research_only")

    def test_original_field_widths_and_loop(self) -> None:
        source = SOURCE.read_text(encoding="utf-8")
        self.assertIn("extern ROOT D_800BCCC0_BD8C0;", source)
        self.assertIn("extern u8 D_8008CCC0_8D8C0[];", source)
        self.assertIn("i = (u16)(i+1)", source)
        self.assertIn("i*0x28 + 0x38000", source)
        for offset in (0x2E50, 0x2E54, 0x2E58, 0x2E5C, 0x2E60,
                       0x2E64, 0x2E68, 0x2E6C, 0x2E70, 0x2E74):
            self.assertIn("p+0x" + f"{offset:04X}", source)

    def test_optional_authenticated_original_rom_native_gate(self) -> None:
        names = ("GOEMON_USA_DECOMPRESSED_ROM", "GOEMON_IDO_CC",
                 "GOEMON_MIPS_LD", "GOEMON_MIPS_OBJCOPY")
        if not all(os.environ.get(k) for k in names):
            self.skipTest("Requires ROM and supplied original IDO/MIPS toolchain paths")
        from decomp.research.camera_reset_136_probe import prove
        result = prove(*(Path(os.environ[k]) for k in names), SOURCE)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["matching_code_bytes"], 136)
        self.assertEqual(result["matching_instructions"], 34)


if __name__ == "__main__":
    unittest.main()

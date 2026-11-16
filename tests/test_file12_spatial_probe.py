"""ROM-free tests for the static original-USA file_12 opcode probe."""
import unittest
from decomp.file12_spatial_probe import (
    FILE12_ROM_CODE_END, FILE12_ROM_START, FILE12_VRAM_START,
    I_ANCHORS, JAL_ANCHORS, audit, check_anchors, file12_offset,
)


class SpatialProbeTests(unittest.TestCase):
    def test_rom_vram_address_translation(self):
        self.assertEqual(file12_offset(0x80218AF4), 0x5D3FC4)
        self.assertEqual(file12_offset(0x8021A4B8), 0x5D5988)
        with self.assertRaises(ValueError):
            file12_offset(FILE12_VRAM_START - 4)
        with self.assertRaises(ValueError):
            file12_offset(FILE12_VRAM_START + FILE12_ROM_CODE_END - FILE12_ROM_START)
        with self.assertRaises(ValueError):
            file12_offset(0x80218AF5)

    @staticmethod
    def fake_rom():
        # Synthesised instructions from declared field patterns; no original ROM data.
        buf = bytearray(FILE12_ROM_CODE_END)
        for pc, op, rs, rt, imm, _ in I_ANCHORS:
            code = (op << 26) | (rs << 21) | (rt << 16) | imm
            start = file12_offset(pc)
            buf[start:start + 4] = code.to_bytes(4, "big")
        for pc, target, _ in JAL_ANCHORS:
            code = (3 << 26) | ((target & 0x0FFFFFFF) >> 2)
            start = file12_offset(pc)
            buf[start:start + 4] = code.to_bytes(4, "big")
        return buf

    def test_synthetic_anchor_matrix(self):
        self.assertEqual(check_anchors(self.fake_rom()), [])

    def test_detect_modified_opcode(self):
        buf = self.fake_rom()
        offset = file12_offset(0x8021A4B8)
        buf[offset] ^= 4
        self.assertTrue(any("0x8021A4B8" in message for message in check_anchors(buf)))

    def test_wrong_rom_rejected(self):
        with self.assertRaisesRegex(ValueError, "verified original"):
            audit(bytes(32))


if __name__ == "__main__":
    unittest.main()

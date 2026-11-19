"""ROM-free direct-JAL overlay anchor tests."""
from pathlib import Path
import struct
import tempfile
import unittest
import yaml

from decomp import japan_overlay_entrypoints as mod
from decomp.japan_function_map import SHA1


def code_words():
    return tuple((0x23 << 26) | (((i % 13) + 1) << 21) |
                 (((i * 3 % 17) + 1) << 16) | (i + 1) for i in range(24))


def make_splat(path: Path, region: str, section: str, start: int, vram: int):
    path.write_text(yaml.safe_dump({
        'sha1': SHA1[region],
        'segments': [{'name': section, 'type': 'code', 'start': start, 'vram': vram,
                      'subsegments': [[start, 'asm'], [start + 256, 'data']]}]
    }))


class JALOverlayTests(unittest.TestCase):
    def test_jump_high_nibble_is_pc_relative(self):
        # MIPS PC+4 high nibble, important for 0x08000000 region overlays.
        self.assertEqual(mod.jal_target(0x0E000004, 0x08000100), 0x08000010)
        self.assertEqual(mod.jal_target(0x0C000004, 0x80000100), 0x80000010)
        self.assertIsNone(mod.jal_target(0x08000004, 0x08000100))

    def test_call_target_is_unique_within_section(self):
        base = 0x801D0B90
        word = 0x0C000000 | (((base + 12 * 4) >> 2) & 0x03FFFFFF)
        words = [0] * 48
        words[0] = words[2] = word
        positions, calls = mod.direct_targets(tuple(words), base)
        self.assertEqual(positions, {12})
        self.assertEqual(calls, 2)

    def test_overlay_mapping_keeps_section_identity(self):
        a, b = bytearray(0x4000), bytearray(0x4000)
        us_start, jp_start, vram = 0x1000, 0x1800, 0x08000000
        src_offset, dest_offset = 0x20, 0x50
        words = code_words()
        for i, ins in enumerate(words):
            struct.pack_into('>I', a, us_start + src_offset + 4*i, ins)
            struct.pack_into('>I', b, jp_start + dest_offset + 4*i,
                             (ins & 0xFFFF0000) | (0xFEE0 + i))
        jal = 0x0C000000 | (((vram + src_offset) >> 2) & 0x03FFFFFF)
        struct.pack_into('>I', a, us_start, jal)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            us, jp = root/'us.yaml', root/'jp.yaml'
            make_splat(us, 'usa', 'file_24', us_start, vram)
            make_splat(jp, 'japan_0', 'file_24', jp_start, vram)
            report = mod.map_jal_overlays(bytes(a), bytes(b), us, jp)
        self.assertEqual(len(report['mappings']), 1)
        match = report['mappings'][0]
        self.assertEqual(match['section'], '.file_24')
        self.assertEqual(match['usa_vram'], f'0x{vram+src_offset:08X}')
        self.assertEqual(match['japan_vram'], f'0x{vram+dest_offset:08X}')
        self.assertEqual(report['totals']['unambiguous_starts'], 1)
        self.assertEqual(match['exact_words'], 0)

    def test_ambiguous_japanese_anchor_rejected(self):
        a, b = bytearray(0x4000), bytearray(0x4000)
        us_start, jp_start, vram = 0x1000, 0x1800, 0x08000000
        words = code_words()
        for i, ins in enumerate(words):
            struct.pack_into('>I', a, us_start + 0x20 + 4*i, ins)
            for offset in (0x10, 0x80):
                struct.pack_into('>I', b, jp_start + offset + 4*i, ins)
        struct.pack_into('>I', a, us_start,
                         0x0C000000 | (((vram+0x20) >> 2) & 0x03FFFFFF))
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            us,jp=root/'us.yaml',root/'jp.yaml'
            make_splat(us,'usa','file_24',us_start,vram)
            make_splat(jp,'japan_0','file_24',jp_start,vram)
            report=mod.map_jal_overlays(bytes(a),bytes(b),us,jp)
        self.assertEqual(report['mappings'], [])
        self.assertGreaterEqual(report['totals'].get('ambiguous_or_absent', 0),1)


if __name__=='__main__':
    unittest.main()

"""ROM-free tests for Splat executable section and overlay function mapping."""
from pathlib import Path
import struct
import tempfile
import unittest

from decomp import japan_overlay_map as mapping
from decomp import japan_function_map as base


def splat(path: Path, region: str, start: int, vram: int):
    path.write_text(f"""name: synthetic
sha1: {base.SHA1[region]}
segments:
- name: file_13
  type: code
  start: {start}
  vram: {vram}
  overlay: yes
  subsegments:
  - [{start}, asm]
  - [{start+256}, data]
- name: file_24
  type: code
  start: {start+256}
  vram: 0x08000000
  subsegments:
  - [{start+256}, databin]
""")


class TestJapanOverlayMap(unittest.TestCase):
    def test_splat_code_filter_and_sha(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/"jp.yaml"
            splat(path, "japan_0", 0x1000, 0x801D0B90)
            sections = mapping.splat_text_sections(path, "japan_0")
            self.assertEqual(list(sections), [".file_13"])
            self.assertEqual((sections[".file_13"].rom, sections[".file_13"].end),
                             (0x1000, 0x1100))
            path.write_text(path.read_text().replace(base.SHA1["japan_0"], "0"*40))
            with self.assertRaisesRegex(ValueError, "SHA-1"):
                mapping.splat_text_sections(path, "japan_0")

    def test_full_overlay_instruction_shape(self):
        usa, japan = bytearray(0x3000), bytearray(0x3000)
        us_rom, jp_rom, vram = 0x1000, 0x1800, 0x801D0B90
        code = [(0x23<<26)|(((i%30)+1)<<21)|(((i*3%30)+1)<<16)|(i*2+1)
                for i in range(32)]
        for i, word in enumerate(code):
            struct.pack_into(">I", usa, us_rom+i*4, word)
            struct.pack_into(">I", japan, jp_rom+0x20+i*4,
                             (word & 0xFFFF0000) | 0xEEEE)
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            us, jp, syms = folder/"us.yaml", folder/"jp.yaml", folder/"us.toml"
            splat(us, "usa", us_rom, vram)
            splat(jp, "japan_0", jp_rom, vram)
            syms.write_text(f"""[[section]]
name = ".file_13"
rom = {us_rom}
vram = {vram}
size = 256
functions = [{{name = "original", vram = {vram}, size = {len(code)*4}}}]
""")
            result = mapping.map_sections(bytes(usa), bytes(japan), us, jp, syms)
        self.assertEqual(result["totals"]["unambiguous_full_shape_matches"], 1)
        self.assertEqual(result["mappings"][0]["japan_rom"], f"0x{jp_rom+0x20:X}")
        self.assertEqual(result["mappings"][0]["exact_instruction_words"], 0)

    def test_splat_symbol_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            us, jp, syms = folder/"us.yaml", folder/"jp.yaml", folder/"us.toml"
            splat(us, "usa", 0x1000, 0x801D0B90)
            splat(jp, "japan_0", 0x1800, 0x801D0B90)
            syms.write_text("""[[section]]
name = ".file_13"
rom = 0x9999
vram = 0x801D0B90
functions = []
""")
            with self.assertRaisesRegex(ValueError, "disagreement"):
                mapping.map_sections(bytes(0x3000), bytes(0x3000), us, jp, syms)


if __name__ == "__main__":
    unittest.main()

"""ROM-free synthetic tests for candidate Japanese MIPS function mapping."""
from pathlib import Path
import hashlib
import struct
import tempfile
import unittest
from unittest.mock import patch

from decomp import japan_function_map as mapping


def shape_words():
    words = []
    for i in range(48):
        op = 0x23 if i % 2 else 0x2B
        rs, rt = (i % 13)+1, ((i*5) % 29)+1
        words.append((op << 26) | (rs << 21) | (rt << 16) | (0x100+i))
    return tuple(words)


class TestJapanFunctionMap(unittest.TestCase):
    def test_mips_normalisation(self):
        self.assertEqual(mapping.normalized_instruction(0x0C010123),
                         mapping.normalized_instruction(0x0C01FFFF))
        self.assertEqual(mapping.normalized_instruction(0x24080001),
                         mapping.normalized_instruction(0x2408ABCD))
        self.assertEqual(mapping.normalized_instruction(0x03E00008), 0x03E00008)
        self.assertNotEqual(mapping.normalized_instruction(0x24080001),
                            mapping.normalized_instruction(0x24090001))

    def test_direct_jal_targets_only(self):
        target = mapping.MAIN_VRAM + 5*4
        jal = 0x0C000000 | ((target >> 2) & 0x03FFFFFF)
        self.assertEqual(mapping.jal_entrypoints((jal, jal, 0, 0)), [])
        data = [0]*32
        data[0] = data[3] = jal
        self.assertEqual(mapping.jal_entrypoints(tuple(data)), [5])

    def test_unique_immediate_insensitive_anchor(self):
        us = shape_words()
        jp = list(us)
        jp[4] = (jp[4] & 0xFFFF0000) | 0xFEE0
        sig = mapping._signature(us, 4)
        self.assertTrue(mapping._informative(sig))
        self.assertEqual(mapping.japan_signature_index(tuple(jp))[sig], [4])

    def test_exact_rom_hash_required(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"wrong.z64"
            p.write_bytes(b"wrong")
            with self.assertRaisesRegex(ValueError, "32 MiB"):
                mapping.read_verified_rom(p, "usa")
            with self.assertRaisesRegex(ValueError, "Unsupported"):
                mapping.read_verified_rom(p, "unknown")

    def test_original_us_symbols(self):
        text = '''[[section]]
name = ".entry"
functions = [{name = "entry", vram = 0x80000400, size = 0x38}]
[[section]]
name = ".main"
functions = [
{name = "hello", vram = 0x80001000, size = 0x50},
{name = "outside", vram = 0x80090000, size = 0x40},
]
'''
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"us.toml"
            p.write_text(text)
            self.assertEqual(mapping.symbol_entrypoints(p),
                             [((0x80001000-mapping.MAIN_VRAM)//4, 20, "hello")])

    def test_complete_shape_mapped_across_immediate_changes(self):
        usa, japan = bytearray(mapping.ROM_SIZE), bytearray(mapping.ROM_SIZE)
        words = shape_words()
        source, target = mapping.MAIN_START+0x100, mapping.MAIN_START+0x200
        for i, word in enumerate(words):
            struct.pack_into(">I", usa, source+i*4, word)
            struct.pack_into(">I", japan, target+i*4, (word & 0xFFFF0000) | 0x9A9A)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"syms.toml"
            p.write_text(f'''[[section]]
name = ".main"
functions = [{{name = "f", vram = {mapping.MAIN_VRAM+0x100}, size = {len(words)*4}}}]
''')
            result = mapping.compare_main_code(bytes(usa), bytes(japan), p)
        self.assertEqual(len(result["mappings"]), 1)
        self.assertEqual(result["mappings"][0]["kind"], "full_structure_match")
        self.assertEqual(result["mappings"][0]["japan_rom"], f"0x{target:X}")
        self.assertEqual(result["mappings"][0]["exact_instructions"], 0)


if __name__ == "__main__":
    unittest.main()

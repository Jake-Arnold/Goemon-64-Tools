"""ROM-free contract checks for pinned USA file_11 mixed C/ASM staging."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from decomp import overlay_file11 as mod


class OverlayFile11Tests(unittest.TestCase):
    def setUp(self):
        self.clean = (
            '  - name: file_11\n    type: code\n    start: 0x587370\n'
            '    vram: 0x801CB460\n    subalign: 16\n    subsegments:\n'
            '    - [0x587370, asm]\n    - [0x5B8500, data]\n'
            '  - name: file_12\n    type: code\n'
        )

    def test_expected_thirteen_functions_cover_620_bytes(self):
        self.assertEqual(len(mod.FUNCTIONS), 13)
        self.assertEqual(sum(f[2] for f in mod.FUNCTIONS), 620)
        self.assertEqual(len({f[0] for f in mod.FUNCTIONS}), 13)
        self.assertEqual([f[1] for f in mod.FUNCTIONS], sorted(f[1] for f in mod.FUNCTIONS))

    def test_exact_8_chunk_layout_maintains_selector_assembly(self):
        self.assertEqual(len(mod.CHUNKS), 8)
        self.assertEqual(sum(c[3] for c in mod.CHUNKS), mod.TEXT_END - mod.ROM_START)
        for x, y in zip(mod.CHUNKS, mod.CHUNKS[1:]):
            self.assertEqual(x[2] + x[3], y[2])
        self.assertEqual(mod.CHUNKS[2], ('asm', '59941C', 0x59941C, 0xB4))

    def test_splat_stage_exact_and_reject_double_stage(self):
        patched = mod.stage_config(self.clean)
        self.assertEqual(patched.count('    - [0x599918, c, character_switch_wrappers]'), 1)
        self.assertIn('    - [0x59941C, asm]', patched)
        with self.assertRaises(ValueError):
            mod.stage_config(patched)

    def test_splat_stage_rejects_modified_original(self):
        with self.assertRaises(ValueError):
            mod.stage_config(self.clean.replace('0x801CB460', '0x801CB464'))

    def test_splat_stage_rejects_overlay_reordering(self):
        with self.assertRaises(ValueError):
            mod.stage_config(self.clean.replace('file_12', 'file_13'))

    def test_stage_sources_fails_without_original_rom_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / 'src').mkdir()
            (home / 'config/usa').mkdir(parents=True)
            config = home / 'config/usa/splat.yaml'
            config.write_text(self.clean)
            with self.assertRaisesRegex(ValueError, 'ROM identity'):
                mod.stage_sources(home, home / 'nothing', b'bad')
            self.assertEqual(config.read_text(), self.clean)

    def test_staged_objects_reject_missing_inputs_before_linker_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / '.splat/usa').mkdir(parents=True)
            link = home / '.splat/usa/mnsg.ld'
            link.write_text(mod.LINKER_OLD)
            with self.assertRaises(FileNotFoundError):
                mod.prepare_objects(home)
            self.assertEqual(link.read_text(), mod.LINKER_OLD)

    def test_full_rom_gate_refuses_modified_or_wrong_reference(self):
        with self.assertRaisesRegex(ValueError, 'ROM gate'):
            mod.verify_linked_stage(b'corrupt', b'corrupt', b'', b'', Path('/'), Path('/'))

    def test_lf_c_sources_match_pins(self):
        root = Path(__file__).resolve().parents[1] / 'decomp/research'
        for file, _, digest, _ in mod.SOURCE_SPECS:
            self.assertEqual(hashlib.sha256((root/file).read_bytes().replace(b'\r\n', b'\n')).hexdigest(), digest)


if __name__ == '__main__':
    unittest.main()
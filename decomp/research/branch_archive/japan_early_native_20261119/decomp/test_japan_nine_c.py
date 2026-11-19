"""ROM-free regression cases for the seven-through-nine Japanese C promotions."""
from __future__ import annotations
from pathlib import Path
import tempfile
import unittest

from decomp import japan_nine_c as nine


class NineJapaneseCTests(unittest.TestCase):
    def test_only_reviewed_six_c_stage_accepted(self):
        original = ("    - [0x37870, asm, main_37870]\n"
                    "    - [0x12D60, c, jp_motion_12D60]\n"
                    "    - [0x13B70, c, jp_camera_13B70]\n"
                    "    - [0x16DF0, c, jp_bit_array]\n"
                    "    - [0x38620, c, jp_main_38620]\n")
        staged = nine.render_config(original)
        self.assertIn("[0x378D0, c, jp_mode_flags]", staged)
        self.assertIn("[0x37900, asm, main_37900]", staged)
        with self.assertRaisesRegex(ValueError, "already staged"):
            nine.render_config(staged)
        with self.assertRaisesRegex(ValueError, "baseline"):
            nine.render_config(original.replace("[0x13B70, c, jp_camera_13B70]", ""))

    def test_source_install_safeguards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / nine.SOURCE_FILE
            target.parent.mkdir(parents=True)
            target.write_text('#include "common.h"\n' + "\n".join(
                '#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_mode_flags/' + row[0] + '.s")'
                for row in nine.FUNCTIONS))
            nine.install_source(root)
            self.assertEqual(target.read_bytes(), nine.SOURCE_LOCAL.read_bytes())
            nine.install_source(root)
            target.write_text("void user_edit(void) {}")
            with self.assertRaises(FileExistsError):
                nine.install_source(root)

    def test_function_bounds_and_section_are_contiguous(self):
        self.assertEqual([row[1] for row in nine.FUNCTIONS], [0x378D0, 0x378E0, 0x378F0])
        self.assertEqual(sum(row[3] for row in nine.FUNCTIONS), 48)


if __name__ == "__main__":
    unittest.main()

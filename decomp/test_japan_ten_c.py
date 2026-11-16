"""ROM-free Japanese tenth exact matching-C function regression tests."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from decomp import japan_ten_c as ten

class JapaneseTenthCTests(unittest.TestCase):
    def setUp(self):
        self.base = ("\n".join((
            "[0x12D60, c, jp_motion_12D60]",
            "[0x13B70, c, jp_camera_13B70]",
            "[0x16DF0, c, jp_bit_array]",
            "[0x378D0, c, jp_mode_flags]",
            "[0x38620, c, jp_main_38620]",
            ten.BEFORE)) + "\n")

    def test_original_region_splat_bounds_and_idempotence(self):
        actual = ten.render_config(self.base)
        self.assertIn("[0x37900, c, jp_warp_call_37900]", actual)
        self.assertIn("[0x37920, asm, main_37920]", actual)
        self.assertEqual(actual.count("[0x378D0, c, jp_mode_flags]"), 1)
        with self.assertRaisesRegex(ValueError, "already inserted"):
            ten.render_config(actual)
        with self.assertRaisesRegex(ValueError, "Missing previously"):
            ten.render_config(self.base.replace("jp_mode_flags", "not_a_mode"))

    def test_rejects_modified_existing_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / ten.SOURCE_FILE
            target.parent.mkdir(parents=True)
            target.write_text('#include "common.h"\n'
                              '#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/'
                              'jp_warp_call_37900/func_80036D00_37900.s")\n')
            ten.install_source(root)
            self.assertEqual(target.read_bytes(), ten.SOURCE_LOCAL.read_bytes())
            ten.install_source(root)
            target.write_text("void user_modified(void) {}")
            with self.assertRaises(FileExistsError):
                ten.install_source(root)

    def test_fails_closed_on_mismatched_generated_splat(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / ten.SPLAT_CONFIG
            path.parent.mkdir(parents=True)
            path.write_text("modified")
            parent = root / "nine.yaml"
            parent.write_text(self.base)
            with patch.object(ten.nine, "stage_config", return_value=parent):
                with self.assertRaises(FileExistsError):
                    ten.stage_config(root)

    def test_original_offset_vma_and_extent(self):
        self.assertEqual((ten.ROM_OFFSET, ten.VMA, ten.SIZE), (0x37900, 0x80036D00, 32))
        self.assertEqual(ten.VMA - ten.ROM_OFFSET, 0x7FFFF400)

if __name__ == "__main__":
    unittest.main()

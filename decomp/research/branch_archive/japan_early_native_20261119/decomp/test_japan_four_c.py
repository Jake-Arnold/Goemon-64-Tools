"""ROM-free regression tests for Japan 4-function exact C Splat port."""
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from decomp import japan_four_c as port


class FourJapaneseCTests(unittest.TestCase):
    def test_split_inserts_exact_region_and_preserves_first_c(self):
        source = ("sha1: " + port.baseline.JAPAN_EXPANDED_SHA1 + "\n"
                  "    - [0x15500, asm, main_15500]\n"
                  "    - [0x16E70, asm, main_16E70]\n"
                  "    - [0x38620, c, jp_main_38620]\n")
        rendered = port.render_config(source)
        self.assertEqual(rendered.count("[0x16DF0, c, jp_bit_array]"), 1)
        self.assertIn("[0x38620, c, jp_main_38620]", rendered)
        with self.assertRaisesRegex(ValueError, "already been inserted"):
            port.render_config(rendered)
        with self.assertRaisesRegex(ValueError, "first-C"):
            port.render_config(source.replace("[0x38620, c, jp_main_38620]", ""))

    def test_install_from_generated_stub_and_refuse_user_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / port.SOURCE_FILE
            target.parent.mkdir(parents=True)
            target.write_text('#include "common.h"\n\n' + "\n".join(
                '#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_bit_array/' + name + '.s")'
                for name, _, _ in port.FUNCTIONS), encoding="utf-8")
            port.install_source(root)
            self.assertEqual(target.read_text(), port.SOURCE_LOCAL.read_text())
            port.install_source(root)
            target.write_text("void user_modified(void) {}")
            with self.assertRaises(FileExistsError):
                port.install_source(root)

    def test_all_function_extents_contiguous_and_total_128_bytes(self):
        self.assertEqual(sum(f[2] for f in port.FUNCTIONS), port.SECTION_SIZE)
        self.assertEqual([port.ROM_OFFSET + sum(f[2] for f in port.FUNCTIONS[:i])
                          for i in range(len(port.FUNCTIONS))], [0x16DF0, 0x16E14, 0x16E3C])

    def test_missing_object_rejected_without_running_binutils(self):
        with tempfile.TemporaryDirectory() as temp, \
             mock.patch.object(port.first, "verify", return_value={}), \
             mock.patch.object(port.subprocess, "run") as fake:
            with self.assertRaises(FileNotFoundError):
                port.verify(Path(temp), Path(temp) / "retail.z64")
            fake.assert_not_called()


if __name__ == "__main__":
    unittest.main()

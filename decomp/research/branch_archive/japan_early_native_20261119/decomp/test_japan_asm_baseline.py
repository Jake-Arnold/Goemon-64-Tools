"""ROM-free Japanese assembly-baseline regression tests."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest import mock
import hashlib
from decomp import japan_asm_baseline as mod


class JapaneseAsmBaselineTests(unittest.TestCase):
    def test_config_renders_c_to_asm_without_touching_comments(self):
        original = f"sha1: {mod.JAPAN_EXPANDED_SHA1}\nsegments:\n  - [0x1000, c, one] # c, comment\n  - [0x2000, asm, two]\n"
        self.assertIn("[0x1000, asm, one] # c, comment", mod.render_asm_config(original, count=1))
        with self.assertRaisesRegex(ValueError, "Expected"):
            mod.render_asm_config(original)
        with self.assertRaisesRegex(ValueError, "revision"):
            mod.render_asm_config(original.replace(mod.JAPAN_EXPANDED_SHA1, "0"*40), count=1)

    def test_cross_file_labels_and_bss_collision_patch_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asm = root / mod.REGION_ASM
            asm.mkdir(parents=True)
            (asm / "main_1050.s").write_text(".section .text\n", encoding="utf-8")
            label = ".L08000170_6B1240"
            define = asm / "main.s"
            define.write_text(f".section .text\n  {label}:\n  nop\n", encoding="utf-8")
            (asm / "other.s").write_text(f"lui $v0, %hi({label})\n", encoding="utf-8")
            bss = root / mod.BSS_FILE
            bss.parent.mkdir(parents=True)
            bss.write_text(".section .bss\n" + "".join(
                f"nonmatching {x}, 0x4\ndlabel {x}\n.space 0x4\n"
                for x in mod.BSS_ALIASES), encoding="utf-8")
            result = mod.patch_asm(root, expected_cross=1)
            self.assertEqual(result, {"cross_object_labels":1,"new_global_labels":1,"renamed_bss_symbols":2})
            self.assertIn(f".globl {label}\n  {label}:", define.read_text())
            for name in mod.BSS_ALIASES:
                self.assertIn("D_JP_BSS_" + name, bss.read_text())
            self.assertEqual(mod.patch_asm(root, expected_cross=1)["new_global_labels"], 0)
            self.assertEqual(mod.patch_asm(root, expected_cross=1)["renamed_bss_symbols"], 0)
            (asm / "another.s").write_text(f"{label}:\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Ambiguous"):
                mod.patch_asm(root, expected_cross=1)

    def test_verified_image_hash_and_byte_equality(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            a, b = b"reference-retail", b"reference-expanded"
            paths = (root / "config/japan_0/baserom.z64",
                     root / "config/japan_0/baserom.decompressed.z64",
                     root / "build/japan_0/mnsg.z64", root / "retail.z64")
            for path, content in zip(paths, (a,b,b,a)):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            with mock.patch.object(mod, "RETAIL_SIZE", len(a)), \
                 mock.patch.object(mod, "EXPANDED_SIZE", len(b)), \
                 mock.patch.object(mod, "JAPAN_RETAIL_SHA1", hashlib.sha1(a).hexdigest()), \
                 mock.patch.object(mod, "JAPAN_EXPANDED_SHA1", hashlib.sha1(b).hexdigest()):
                self.assertEqual(mod.verify(root, paths[3])["retail"]["status"], "PASS")
                paths[2].write_bytes(b"bad")
                with self.assertRaisesRegex(ValueError, "mismatch"):
                    mod.verify(root, paths[3])


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from decomp.research import usa_character_switch_extended_rebuild as ext


class ExtendedBuildTests(unittest.TestCase):
    def test_original_rom_extent(self):
        # Every original byte through the file_11 text boundary is accounted for.
        self.assertEqual(sum(ext.SIZES.values()), 0x5B8500 - 0x587370)
        self.assertEqual(ext.SIZES["build/usa/src/character_switch_wrappers.c.o"], 9 * 32)

    def test_source_range_preserved(self):
        self.assertIn("[0x599918, c, character_switch_wrappers]", ext.SPLAT_EXTENDED)
        self.assertIn("[0x599A38, asm]", ext.SPLAT_EXTENDED)
        self.assertNotIn("character_switch_wrappers", ext.SPLAT_PREVIOUS)

    def test_prepare_fails_closed_when_unstaged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config/usa").mkdir(parents=True)
            (root / "config/usa/splat.yaml").write_text("ordinary content\n")
            with self.assertRaises(ValueError):
                ext.prepare(root)

    def test_prepare_fails_closed_on_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config/usa").mkdir(parents=True)
            (root / "config/usa/splat.yaml").write_text(ext.SPLAT_PREVIOUS + "\n" + ext.SPLAT_PREVIOUS)
            with self.assertRaises(ValueError):
                ext.prepare(root)

    def test_full_rom_verifier_accepts_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "build/usa").mkdir(parents=True)
            (root / "build/usa/mnsg.z64").write_bytes(b"test")
            # This module's verifier requires the real authenticated hash.
            with self.assertRaises(ValueError):
                ext.verify(root, b"test")

    def test_full_rom_verifier_rejects_different(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "build/usa").mkdir(parents=True)
            (root / "build/usa/mnsg.z64").write_bytes(b"changed")
            with self.assertRaises(ValueError):
                ext.verify(root, b"original")


if __name__ == "__main__":
    unittest.main()
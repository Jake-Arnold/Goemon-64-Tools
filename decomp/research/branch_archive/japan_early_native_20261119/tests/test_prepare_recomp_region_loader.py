"""Synthetic tests; source preparation does not start Goemon64Recomp."""
from pathlib import Path
import tempfile
import unittest

from decomp import prepare_recomp_region_loader as loader


def original_source():
    return ("#include \"goemon_game.h\"\n" + loader.BEFORE_CONSTANTS + "\n" +
            "void test() {\n" + loader.BEFORE_HEADER + "\n" +
            loader.BEFORE_EXPAND + "\n" + loader.BEFORE_CRC + "\n}\n")


class Tests(unittest.TestCase):
    def test_region_parameters_and_source_replacement(self):
        result = loader.render(original_source())
        for expected in (
            "GOEMON_USA", "GOEMON_JAPAN_0", "0x57FD8", "0x58258",
            "0x9CC11F4B", "0x673A3EDC", "0xFCBCCB21", "0x832C168B",
            "variant->file_table_offset", "variant->decompressed_crc1",
        ):
            self.assertIn(expected, result)
        self.assertNotIn(loader.BEFORE_CRC, result)
        self.assertNotIn(loader.BEFORE_HEADER, result)

    def test_unknown_and_already_patched_files_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "anchor"):
            loader.render(original_source().replace("0x57FD8", "0xDEAD"))
        with self.assertRaisesRegex(ValueError, "already patched"):
            loader.render(loader.render(original_source()))

    def test_dry_run_and_isolated_atomic_patch(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / loader.RELATIVE
            source.parent.mkdir(parents=True)
            source.write_text(original_source())
            loader.prepare(root, dry_run=True)
            self.assertEqual(source.read_text(), original_source())
            loader.prepare(root)
            self.assertIn("GOEMON_JAPAN_0", source.read_text())


if __name__ == "__main__":
    unittest.main()

"""ROM-free tests for strict Goemon version identification."""
from dataclasses import replace
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from practice.game_versions import (ROM_SIZE, VERSIONS, identify_rom,
                                    selected_version, verify_selected_rom)


def synthetic_rom(game_code: bytes) -> bytes:
    rom = bytearray(ROM_SIZE)
    rom[:4] = bytes.fromhex("80371240")
    rom[0x3B:0x3F] = game_code
    return bytes(rom)


class GameVersionsTests(unittest.TestCase):
    def test_default_capability_is_usa_only(self):
        self.assertTrue(selected_version("usa").live_memory_supported)
        self.assertFalse(selected_version("japan").live_memory_supported)
        with self.assertRaises(ValueError):
            selected_version("other")

    def test_original_sha1_fingerprints(self):
        self.assertEqual(VERSIONS["usa"].sha1, "df8083a54296b8c151917c5333e1c85f014a2a66")
        self.assertEqual(VERSIONS["japan"].sha1, "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b")

    def test_identifies_all_n64_byte_orders(self):
        rom = synthetic_rom(b"NG5J")
        patched = replace(VERSIONS["japan"], sha1=hashlib.sha1(rom).hexdigest())
        swapped16 = b"".join(rom[i:i+2][::-1] for i in range(0, len(rom), 2))
        swapped32 = b"".join(rom[i:i+4][::-1] for i in range(0, len(rom), 4))
        with patch.dict(VERSIONS, {"japan": patched}):
            for data in (rom, swapped16, swapped32):
                with self.subTest(header=data[:4]):
                    self.assertEqual(identify_rom(data), patched)

    def test_rejects_wrong_size_bad_hash_and_header(self):
        with self.assertRaises(ValueError):
            identify_rom(b"hello")
        with self.assertRaises(ValueError):
            identify_rom(synthetic_rom(b"NG5E"))
        rom = synthetic_rom(b"NG5E")
        wrong_header = replace(VERSIONS["usa"], sha1=hashlib.sha1(rom).hexdigest(), game_code=b"NG5J")
        with patch.dict(VERSIONS, {"usa": wrong_header}):
            with self.assertRaises(ValueError):
                identify_rom(rom)

    def test_selection_rejects_verified_other_region(self):
        rom = synthetic_rom(b"NG5E")
        usa = replace(VERSIONS["usa"], sha1=hashlib.sha1(rom).hexdigest())
        with tempfile.TemporaryDirectory() as folder, patch.dict(VERSIONS, {"usa": usa}):
            path = Path(folder, "test.z64")
            path.write_bytes(rom)
            self.assertEqual(verify_selected_rom(path, "usa"), usa)
            with self.assertRaisesRegex(ValueError, "Selected Japan"):
                verify_selected_rom(path, "japan")


if __name__ == "__main__":
    unittest.main()

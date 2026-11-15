import unittest

from decomp.research import character_switch_actor_native_probe as native


class ActorNativeCompareTests(unittest.TestCase):
    def test_usa_registry(self):
        info = native.REGIONS["usa"]
        self.assertEqual(info["vma"], 0x801DDA08)
        self.assertEqual(info["offset"], 0x599918)
        self.assertEqual(len(info["functions"]), 9)
        self.assertEqual(info["functions"][-1], "func_801DDB08_599A18")

    def test_japan_registry(self):
        info = native.REGIONS["japan"]
        self.assertEqual(info["vma"], 0x801E2DB8)
        self.assertEqual(info["offset"], 0x59ED88)
        self.assertEqual(info["functions"][-1], "func_801E2EB8_59EE88")

    def test_exact_all(self):
        ref = bytes([23]) * 0x600000
        compiled = bytes([23]) * native.TOTAL
        for region in native.REGIONS:
            result = native.compare(ref, compiled, region)
            self.assertTrue(result["all_exact"])
            self.assertEqual(result["matched_bytes"], 288)
            self.assertEqual(len(result["functions"]), 9)
            self.assertTrue(all(f["word_matches"] == 8 for f in result["functions"]))

    def test_detect_one_different_instruction(self):
        ref = bytes([1]) * 0x600000
        compiled = bytearray([1] * native.TOTAL)
        compiled[32 * 5 + 4] = 2
        result = native.compare(ref, compiled, "usa")
        self.assertFalse(result["all_exact"])
        self.assertEqual(result["matched_bytes"], 8 * 32)
        self.assertFalse(result["functions"][5]["exact"])
        self.assertEqual(result["functions"][5]["word_matches"], 7)

    def test_reject_long_compiler_output(self):
        with self.assertRaises(ValueError):
            native.compare(bytes([0]) * 0x600000, bytes([0]) * 304, "usa")

    def test_reject_short_compiler_output(self):
        with self.assertRaises(ValueError):
            native.compare(bytes([0]) * 0x600000, bytes([0]) * 280, "japan")

    def test_reject_bad_rom_size(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            path = Path(directory) / "rom.z64"
            path.write_bytes(b"short")
            with self.assertRaises(ValueError):
                native.check_original_rom(path, "usa")


if __name__ == "__main__":
    unittest.main()
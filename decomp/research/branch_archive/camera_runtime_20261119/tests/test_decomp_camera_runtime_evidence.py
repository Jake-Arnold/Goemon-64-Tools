"""Source-only regression checks for pinned USA camera trace; no ROM required."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "decomp/results/usa_camera_runtime_trace_20261116.json"

def addr(s: str) -> int:
    return int(s, 16)

class CameraRuntimeTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_original_function_coverage_and_map(self) -> None:
        source = self.data["source"]
        rom_base, vma_base = addr(source["file11_rom_start"]), addr(source["file11_vma_start"])
        spans = []
        for fn in self.data["original_functions"]:
            start, end = addr(fn["rom_start"]), addr(fn["rom_end_exclusive"])
            self.assertEqual(end - start, fn["size"])
            self.assertEqual(vma_base + start - rom_base, addr(fn["vma_start"]))
            self.assertEqual(fn["ownership"], "assembly in canonical 152-C file11 stage")
            spans.append((start, end))
        self.assertEqual(len(spans), 2)
        self.assertLessEqual(spans[0][1], spans[1][0])
        for insn in self.data["instructions"]:
            off = addr(insn["rom_offset"])
            self.assertEqual(vma_base + off - rom_base, addr(insn["pc"]))
            self.assertTrue(any(start <= off < end for start, end in spans))

    def test_table_and_field_addressing(self) -> None:
        runtime = self.data["runtime"]
        table = self.data["region_table"]
        pointer = addr(runtime["camera_task_pointer_observed"])
        self.assertEqual(pointer + addr(runtime["task_mode_offset"]), 0x8016A128)
        self.assertEqual(addr(runtime["global_default_mode"]), 0x800C7B00)
        self.assertEqual(addr(table["base"]), 0x800C7B10)
        self.assertEqual(table["entry_stride"], 0x28)
        self.assertEqual(table["entry_count_scanned"], 10)
        self.assertEqual([addr(x) for x in table["bounds_i32_offsets"]], [4, 8, 12, 16, 20, 24])
        self.assertEqual([addr(x) for x in table["position_override_i32_offsets"]], [28, 32, 36])

    def test_pinned_rom_slices_when_supplied(self) -> None:
        supplied = os.environ.get("GOEMON_USA_DECOMPRESSED_ROM")
        if not supplied:
            self.skipTest("Set GOEMON_USA_DECOMPRESSED_ROM to run optional authentic ROM check")
        rom = Path(supplied).read_bytes()
        self.assertEqual(len(rom), 33554432)
        self.assertEqual(hashlib.sha1(rom).hexdigest(), self.data["source"]["decompressed_sha1"])
        for fn in self.data["original_functions"]:
            got = hashlib.sha256(rom[addr(fn["rom_start"]):addr(fn["rom_end_exclusive"])]).hexdigest()
            self.assertEqual(got, fn["sha256"], fn["name"])

if __name__ == "__main__":
    unittest.main()

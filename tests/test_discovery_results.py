"""Read-only shared discovery result and watch engine tests (no GUI/ROM)."""
from __future__ import annotations

from pathlib import Path
import struct
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from practice.custom_watches import load_watches, make_watch
from practice.discovery_results import (
    canonical_type, read_live_candidates, add_research_watches,
)


class GuestRam:
    def __init__(self, size=512):
        self.data = bytearray(size)
        self.calls = []
        self.writes = 0

    def read_guest(self, address, width):
        offset = address - 0x80000000
        if not 0 <= offset <= len(self.data) - width:
            raise OSError("Out of guest memory")
        self.calls.append((address, width))
        return bytes(self.data[offset:offset + width])


class DiscoveryResultTests(unittest.TestCase):
    def test_live_type_mapping_is_not_semantic_confirmation(self):
        self.assertEqual(canonical_type("saved event flag candidate"), "u8")
        self.assertEqual(canonical_type("one-bit candidate"), "u8")
        self.assertEqual(canonical_type("f32 candidate"), "f32")
        self.assertEqual(canonical_type("XYZ triple candidate"), "xyz")
        self.assertEqual(canonical_type("u16"), "u16")
        self.assertIsNone(canonical_type("text/Shift-JIS"))
        self.assertIsNone(canonical_type("unsupported"))

    def test_batched_big_endian_live_values_and_no_writes(self):
        ram = GuestRam()
        ram.data[8:10] = (950).to_bytes(2, "big")
        ram.data[24:28] = struct.pack(">f", 13.5)
        rows = [
            dict(id="a", address="0x80000008", type="u16"),
            dict(id="b", address="0x80000018", type="f32"),
            dict(id="c", address="0x80000020", type="text/UTF-8"),
        ]
        values = read_live_candidates(ram, rows)
        self.assertEqual(values["a"], ("950", "0x03B6"))
        self.assertEqual(values["b"], ("13.5", "0x41580000"))
        self.assertEqual(values["c"][0], "Unsupported type")
        self.assertEqual(len(ram.calls), 1)
        self.assertEqual(ram.writes, 0)

    def test_xyz_is_live_triple_and_three_watches(self):
        ram = GuestRam()
        ram.data[16:28] = struct.pack(">fff", 10.0, 20.5, -30.0)
        values = read_live_candidates(
            ram, [dict(id="xyz", address="0x80000010",
                       type="XYZ triple candidate")])
        self.assertIn("10", values["xyz"][0])
        self.assertIn("20.5", values["xyz"][0])
        self.assertIn("-30", values["xyz"][0])
        with TemporaryDirectory() as tmp:
            owner = self._owner("japan", Path(tmp) / "jp.json")
            count, existing = add_research_watches(
                owner, [{"address": "0x80000010",
                         "type": "XYZ triple candidate"}],
                label="JP XYZ candidate")
            self.assertEqual((count, existing), (3, 0))
            self.assertEqual(
                {w.address for w in owner.jp_custom_watches},
                {0x80000010, 0x80000014, 0x80000018})
            self.assertTrue(all(w.kind == "f32"
                                for w in owner.jp_custom_watches))
            self.assertEqual(len(load_watches(owner.jp_watch_path)), 3)

    @staticmethod
    def _owner(region, path):
        owner = SimpleNamespace(
            active_version=SimpleNamespace(key=region),
            jp_watch_path=path, jp_custom_watches=[],
            custom_watches=[],
            _jp_insert_custom_watch=Mock(),
            _jp_reset_comparison=Mock(),
            refresh_japan_fields=Mock(),
            refresh_inspector=Mock(),
            current={}, last_inspect_at=123.0,
        )
        return owner

    def test_japan_and_usa_watches_stay_isolated_and_deduplicate(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            owner = self._owner("japan", root / "japan.json")
            rows = [{"address": "0x80000018", "type": "u16"},
                    {"address": "0x80000024", "type": "u8"}]
            self.assertEqual(add_research_watches(
                owner, rows, label="Flag research"), (2, 0))
            self.assertEqual(add_research_watches(
                owner, rows, label="Flag research"), (0, 2))
            self.assertEqual(len(owner.jp_custom_watches), 2)
            self.assertEqual(len(owner.custom_watches), 0)
            self.assertEqual(len(load_watches(owner.jp_watch_path)), 2)

            owner.active_version.key = "usa"
            with patch("practice.ui_extension.CUSTOM_WATCHES_PATH",
                       root / "usa.json"):
                self.assertEqual(add_research_watches(
                    owner, rows, label="Damage candidate"), (2, 0))
            self.assertEqual(len(owner.jp_custom_watches), 2)
            self.assertEqual(len(owner.custom_watches), 2)
            self.assertEqual(len(load_watches(root / "usa.json")), 2)

    def test_invalid_selection_never_persists_partial_batch(self):
        with TemporaryDirectory() as tmp:
            owner = self._owner("japan", Path(tmp) / "jp.json")
            good = {"address": "0x80000010", "type": "u8"}
            bad = {"address": "0x80800000", "type": "u32"}
            with self.assertRaises(ValueError):
                add_research_watches(owner, [good, bad], label="Research")
            self.assertFalse(owner.jp_watch_path.exists())
            self.assertEqual(owner.jp_custom_watches, [])
            with self.assertRaises(ValueError):
                add_research_watches(owner, [good, {
                    "address": "0x80000018", "type": "text/ASCII"
                }], label="Research")
            self.assertFalse(owner.jp_watch_path.exists())

    def test_read_errors_do_not_look_like_valid_values(self):
        ram = GuestRam(size=8)
        rows = [{"id": "beyond", "address": "0x80000030", "type": "u32"},
                {"id": "bad", "address": "abc", "type": "u8"}]
        values = read_live_candidates(ram, rows)
        self.assertTrue(values["beyond"][0].startswith("Read failed"))
        self.assertEqual(values["bad"][0], "Invalid address")


if __name__ == "__main__":
    unittest.main()

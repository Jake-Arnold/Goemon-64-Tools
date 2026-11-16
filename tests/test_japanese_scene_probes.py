"""Source-only Japanese scene hypotheses, no emulator memory writes."""
import unittest
import json
from pathlib import Path

from practice.japanese_fields import JAPAN_FIELDS, JapanFieldReading
from practice.japanese_scene_probes import (
    JAPAN_SCENE_PROBES, RUNTIME_OBSERVED_SCENE_KEYS, RUNTIME_OBSERVATION_STATUS,
    compare_guest_readings, read_japan_scene_probes,
)


class Ram:
    def __init__(self, values=None, bad=None):
        self.values = values or {}
        self.bad = bad
        self.reads = []

    def read_guest(self, address, width):
        self.reads.append((address, width))
        if self.bad == address:
            raise OSError("denied")
        return self.values.get((address, width), bytes(width))


class JapaneseSceneProbeTests(unittest.TestCase):
    def test_ten_individually_documented_offset_hypotheses(self):
        self.assertEqual(len(JAPAN_SCENE_PROBES), 10)
        self.assertTrue(all(x.address - x.usa_reference == 0x57F0
                            for x in JAPAN_SCENE_PROBES))
        self.assertEqual({x.key for x in JAPAN_SCENE_PROBES}.__len__(), 10)
        self.assertFalse({x.address for x in JAPAN_SCENE_PROBES} &
                         {x.address for x in JAPAN_FIELDS})

    def test_scene_and_character_candidates(self):
        v = {
            (0x800CD2A2, 2): bytes.fromhex("012C"),  # candidate scene 300
            (0x80161DCC, 4): bytes.fromhex("00000003"),
        }
        ram = Ram(v)
        out = read_japan_scene_probes(ram)
        self.assertEqual(out["scene_map"].raw, "012C")
        self.assertEqual(out["scene_map"].value, "300 / 0x12C — Kai Highway")
        self.assertEqual(out["scene_character"].value, "Yae (3) — name candidate")
        self.assertTrue(out["scene_character"].status.startswith("UNVERIFIED"))
        self.assertTrue(out["scene_map"].status.startswith("OBSERVED"))
        self.assertEqual(len(ram.reads), 10)
        self.assertFalse(hasattr(ram, "write_guest"))

    def test_single_observation_status_is_limited_to_four_fields(self):
        self.assertEqual(RUNTIME_OBSERVED_SCENE_KEYS, {
            "scene_map", "scene_previous", "scene_pending",
            "scene_submode", "scene_character"})
        self.assertIn("two JP", RUNTIME_OBSERVATION_STATUS["scene_previous"])
        self.assertIn("both directions", RUNTIME_OBSERVATION_STATUS["scene_character"])
        out = read_japan_scene_probes(Ram({
            (0x800CD2A2, 2): bytes.fromhex("0163"),
            (0x800CD2AC, 2): bytes.fromhex("012C"),
            (0x800CD490, 2): bytes.fromhex("0163"),
            (0x800CD294, 1): bytes.fromhex("02"),
        }))
        self.assertEqual(out["scene_map"].value, "355 / 0x163 — Oedo Town (Northwest)")
        self.assertEqual(out["scene_previous"].value, "300 / 0x12C — Kai Highway")
        self.assertEqual(out["scene_pending"].raw, "0163")
        self.assertEqual(out["scene_submode"].value, "2 — town (candidate)")
        for key in ("scene_map", "scene_previous", "scene_pending", "scene_submode"):
            self.assertTrue(out[key].status.startswith("OBSERVED"))
        self.assertTrue(out["scene_character"].status.startswith("CONFIRMED"))
        self.assertTrue(out["scene_phase"].status.startswith("UNVERIFIED"))

    def test_character_both_directions_and_untested_2_3(self):
        addr = 0x80161DCC
        goemon = read_japan_scene_probes(Ram({
            (addr, 4): bytes.fromhex("00000000")}))["scene_character"]
        ebisumaru = read_japan_scene_probes(Ram({
            (addr, 4): bytes.fromhex("00000001")}))["scene_character"]
        sasuke = read_japan_scene_probes(Ram({
            (addr, 4): bytes.fromhex("00000002")}))["scene_character"]
        self.assertEqual(goemon.value, "Goemon (0)")
        self.assertEqual(ebisumaru.value, "Ebisumaru (1)")
        self.assertTrue(goemon.status.startswith("CONFIRMED"))
        self.assertTrue(ebisumaru.status.startswith("CONFIRMED"))
        self.assertTrue(sasuke.status.startswith("UNVERIFIED"))
        self.assertIn("name candidate", sasuke.value)

    def test_second_trace_preserved_verbatim(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "research" /
            "japan_scene_character_runtime_2026-11-15.json").read_text(encoding="utf-8"))
        self.assertEqual(data["region"], "japan-0")
        events = {x["id"]: x for x in data["observations"]}
        self.assertEqual(set(events), {
            "goemon-to-ebisumaru", "oedo-north-to-castle-bridge",
            "ebisumaru-to-goemon"})
        forward = {x["key"]: x for x in events["goemon-to-ebisumaru"]["changes"]}
        reverse = {x["key"]: x for x in events["ebisumaru-to-goemon"]["changes"]}
        oedo = {x["key"]: x for x in events["oedo-north-to-castle-bridge"]["changes"]}
        self.assertEqual((forward["scene_character"]["before"],
                          forward["scene_character"]["after"]),
                         ("00000000", "00000001"))
        self.assertEqual((reverse["scene_character"]["before"],
                          reverse["scene_character"]["after"]),
                         ("00000001", "00000000"))
        self.assertEqual((oedo["scene_map"]["before"], oedo["scene_map"]["after"]),
                         ("0160", "0162"))
        self.assertEqual((oedo["scene_previous"]["before"],
                          oedo["scene_previous"]["after"]), ("0161", "0160"))
        self.assertEqual((oedo["scene_pending"]["before"],
                          oedo["scene_pending"]["after"]), ("0160", "0162"))
        for event, expected_delta in (
            ("goemon-to-ebisumaru", 2),
            ("oedo-north-to-castle-bridge", 15),
            ("ebisumaru-to-goemon", 2),
        ):
            counter = next(x for x in events[event]["changes"]
                           if x["key"] == "total_time_raw")
            self.assertEqual(counter["raw_delta"], expected_delta)
            self.assertEqual(
                int(counter["after"], 16) - int(counter["before"], 16),
                expected_delta)

    def test_runtime_evidence_archive_exact_bytes(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "research" /
            "japan_scene_runtime_2026-11-15.json").read_text(encoding="utf-8"))
        self.assertEqual(data["evidence_class"], "runtime-observed-single-trial")
        self.assertEqual(data["region"], "japan-0")
        evidence = {x["key"]: x for x in data["observations"]}
        self.assertEqual(set(evidence), {
            "total_time_raw", "scene_map", "scene_submode",
            "scene_previous", "scene_pending"})
        self.assertEqual((evidence["scene_map"]["before"],
                          evidence["scene_map"]["after"]), ("012C", "0163"))
        self.assertEqual((evidence["scene_previous"]["before"],
                          evidence["scene_previous"]["after"]), ("0163", "012C"))
        self.assertEqual(evidence["scene_pending"]["after"], "0163")
        self.assertEqual(evidence["scene_submode"]["after"], "02")
        self.assertEqual(evidence["total_time_raw"]["raw_delta"], 6)

    def test_unusual_scene_or_character_values_not_hidden(self):
        ram = Ram({
            (0x800CD2A2, 2): bytes.fromhex("F000"),
            (0x80161DCC, 4): bytes.fromhex("DEADBEEF"),
        })
        out = read_japan_scene_probes(ram)
        self.assertTrue(out["scene_map"].status.startswith("CHECK"))
        self.assertTrue(out["scene_character"].status.startswith("CHECK"))
        self.assertEqual(out["scene_character"].raw, "DEADBEEF")

    def test_probe_read_errors_are_isolated(self):
        ram = Ram(bad=0x800CD2A2)
        out = read_japan_scene_probes(ram)
        self.assertEqual(out["scene_map"].value, "—")
        self.assertIn("READ ERROR", out["scene_map"].status)
        self.assertFalse(out["scene_phase"].status.startswith("READ ERROR"))

    def test_compare_uses_raw_bytes_and_skips_read_errors(self):
        b = {
            "map": JapanFieldReading("Old", "0002", "UNVERIFIED"),
            "ryo": JapanFieldReading("12", "000C", "External lead"),
            "bad": JapanFieldReading("—", "—", "READ ERROR"),
        }
        a = {
            "map": JapanFieldReading("Scene 300", "012C", "UNVERIFIED"),
            "ryo": JapanFieldReading("12 displayed differently", "000C", "External lead"),
            "bad": JapanFieldReading("3", "03", "UNVERIFIED"),
        }
        self.assertEqual(compare_guest_readings(b, a, ("map", "ryo", "bad")),
                         (("map", "0002", "012C"),))


if __name__ == "__main__":
    unittest.main()

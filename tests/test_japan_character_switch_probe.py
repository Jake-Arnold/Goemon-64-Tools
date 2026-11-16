"""ROM-free instruction-identity tests for the Project64 character trace probe."""
import struct
import unittest

from decomp.japan_character_switch_probe import (
    JP_SHA1, EXPECTED, TRACE_START, Overlay, candidate_overlays, probe,
)

BASE = 0x801D0B90


def layout():
    def segment(name, rom):
        return {"name": name, "type": "code", "overlay": "yes", "start": rom,
                "vram": BASE, "subsegments": [[rom, "asm"], [rom + 0x13000, "data"]]}
    return {"sha1": JP_SHA1,
            "segments": [segment("file_11", 0x100), segment("file_13", 0x20000),
                         {"name": "main", "type": "code", "start": 0,
                          "vram": 0x80000450, "subsegments": [[0, "asm"], [100, "data"]]}]}


def populated_rom():
    rom = bytearray(0x40000)
    overlay = Overlay("file_11", 0x100, BASE, 0x13100)
    for addr, word in EXPECTED.items():
        struct.pack_into(">I", rom, overlay.offset(addr), word)
    return rom


class JapanSwitchProbeTests(unittest.TestCase):
    def test_known_jal_encoding_targets_callee(self):
        jal = EXPECTED[0x801E2950]
        self.assertEqual(jal >> 26, 3)
        self.assertEqual(((0x801E2950 + 4) & 0xF0000000) | ((jal & 0x3FFFFFF) << 2),
                         0x801E2970)

    def test_overlapping_virtual_addresses_retained_as_candidates(self):
        self.assertEqual([c.name for c in candidate_overlays(layout())], ["file_11", "file_13"])

    def test_unique_full_trace_match_resolves_one_overlay(self):
        result = probe(populated_rom(), layout())
        self.assertTrue(result["identified_uniquely"])
        self.assertEqual(result["matching_overlays"], ["file_11"])
        self.assertEqual(result["candidate_overlays"][0]["matching_words"], len(EXPECTED))
        self.assertEqual(result["candidate_overlays"][1]["matching_words"], 0)

    def test_mutated_single_word_rejects_candidate(self):
        rom = populated_rom()
        overlay = candidate_overlays(layout())[0]
        struct.pack_into(">I", rom, overlay.offset(0x801E299C), 0)
        result = probe(rom, layout())
        self.assertFalse(result["identified_uniquely"])
        self.assertEqual(result["candidate_overlays"][0]["matching_words"], len(EXPECTED) - 1)

    def test_wrong_layout_sha_rejected(self):
        doc = layout()
        doc["sha1"] = "0" * 40
        with self.assertRaises(ValueError):
            candidate_overlays(doc)

    def test_trace_does_not_guess_unobserved_gap(self):
        self.assertFalse(any(0x801E2958 <= pc < 0x801E2970 for pc in EXPECTED))


if __name__ == "__main__":
    unittest.main()
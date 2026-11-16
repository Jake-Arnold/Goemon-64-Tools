"""ROM-free pinned offset reconciliation for independent USA file_11 research.

Wave 101 documents 16 wrappers only by their inclusive ROM range, so their
identities are explicitly range-inferred rather than source-archive verified.
No production function claim may follow directly from this audit.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
REVIEW=ROOT/"results/file11_crossbranch_overlap_v2_20261116.json"
WAVE1=ROOT/"results/file11_expansion_native_20261116.json"
ADJ=ROOT/"research/file11_adjacent_sources.json"
WAVE2=ROOT/"research/file11_adjacent_wave2_sources.json"
WAVE3=ROOT/"research/file11_adjacent_wave3_sources.json"
WAVE5=ROOT/"research/file11_adjacent_wave5_sources.json"
WAVE4=(0x599CCC,0x59E82C,0x5B1808,0x5B186C,0x5B18A8)
EXPECTED_EXTRA={0x5B4DEC:48,0x5B64B8:44,0x5B71B4:44,0x5B7180:52}
EXPECTED_WRAPPERS=(0x5B2004,0x5B202C,0x5B2054,0x5B2080,
   0x5B225C,0x5B2284,0x5B22A8,0x5B22C8,0x5B22F0,0x5B2314,
   0x5B2578,0x5B25A4,0x5B25D0,0x5B25FC,0x5B2628,0x5B2654)

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

class File11CrossbranchDedupTests(unittest.TestCase):
    def test_expansion_207_original_addresses_are_disjoint(self):
        sets=[load(WAVE1)["functions"],load(ADJ)["functions"],
              load(WAVE2)["functions"],load(WAVE3)["functions"],
              [f for f in load(WAVE5)["functions"] if f["new_wave5"]]]
        offsets=[f["rom_offset"] for group in sets for f in group]
        offsets+=list(WAVE4)
        self.assertEqual(len(offsets),207)
        self.assertEqual(len(set(offsets)),207)

    def test_reconstructed_alternate_54_is_distinct(self):
        review=load(REVIEW)
        buckets=review["alternate_54_reconstructed"]
        offsets=[int(s,16) for group in buckets for s in group["offsets"]]
        self.assertEqual(len(offsets),54)
        self.assertEqual(len(set(offsets)),54)
        self.assertEqual({x["wave"]:len(x["offsets"]) for x in buckets},
            {"52":2,"73_paired":6,"73_noops":15,
             "101_wrappers":16,"101_helpers":12,"104":3})

    def test_wrapper_range_is_explicitly_uncertain(self):
        review=load(REVIEW)
        groups={b["wave"]:b for b in review["alternate_54_reconstructed"]}
        wrappers=tuple(int(s,16) for s in groups["101_wrappers"]["offsets"])
        self.assertEqual(wrappers,EXPECTED_WRAPPERS)
        self.assertEqual(groups["101_wrappers"]["provenance"],
            "inferred_all_16_captures_in_documented_offset_range")
        self.assertIs(review["full_identity_54_verified_from_original_source_archive"],False)

    def test_overlap_and_four_distinct_offsets(self):
        review=load(REVIEW)
        pools=[load(WAVE1)["functions"],load(ADJ)["functions"],
               load(WAVE2)["functions"],load(WAVE3)["functions"],
               [f for f in load(WAVE5)["functions"] if f["new_wave5"]]]
        expansion={f["rom_offset"] for group in pools for f in group}|set(WAVE4)
        alternate={int(s,16) for group in review["alternate_54_reconstructed"] for s in group["offsets"]}
        self.assertEqual(len(expansion & alternate),50)
        self.assertEqual(alternate-expansion,set(EXPECTED_EXTRA))
        self.assertEqual({int(x["rom_offset"],16):x["size"] for x in review["not_in_expansion"]},EXPECTED_EXTRA)
        self.assertEqual(sum(EXPECTED_EXTRA.values()),188)
        self.assertEqual(len(expansion|alternate),211)

    def test_no_central_promotion_is_claimed(self):
        review=load(REVIEW)
        self.assertFalse(review["canonical_210_plus_candidates_rom_gate_completed"])
        self.assertEqual(review["production_function_claims_added"],0)
        self.assertEqual(review["union_unpromoted_candidates_provisional"],211)

if __name__=="__main__":unittest.main()

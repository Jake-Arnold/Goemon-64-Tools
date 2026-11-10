"""Pure synthetic regression checks for combined translation-unit proof boundaries."""
import hashlib
import unittest
if __package__:
    from .prove_integrated_units import compare_unit, SPECS
else:
    from prove_integrated_units import compare_unit, SPECS


class IntegratedUnitProofTests(unittest.TestCase):
    def setUp(self):
        self.original = bytes(range(16))
        self.spec = {
            "unit": "synthetic",
            "offset": 0,
            "size": 16,
            "sha256": hashlib.sha256(self.original).hexdigest(),
            "symbols": (("first", 0, 8), ("second", 8, 8)),
        }

    def test_exact_whole_unit(self):
        report = compare_unit(self.original, self.original, self.spec)
        self.assertTrue(report["exact_original_bytes"])
        self.assertTrue(all(f["exact_original_bytes"] for f in report["functions"]))

    def test_middle_of_second_function_detected(self):
        wrong = self.original[:10] + b"\xff" + self.original[11:]
        report = compare_unit(wrong, self.original, self.spec)
        self.assertFalse(report["exact_original_bytes"])
        self.assertEqual(report["mismatched_offsets"], ["0xa"])
        self.assertTrue(report["functions"][0]["exact_original_bytes"])
        self.assertFalse(report["functions"][1]["exact_original_bytes"])

    def test_wrong_reference_sha_rejected(self):
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            compare_unit(self.original, self.original[::-1], self.spec)

    def test_short_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError, "length"):
            compare_unit(self.original[:-1], self.original, self.spec)

    def test_long_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError, "length"):
            compare_unit(self.original+b"\0", self.original, self.spec)

    def test_known_units_do_not_overlap_and_symbols_cover_every_byte(self):
        ranges = []
        for spec in SPECS:
            self.assertEqual(sum(x[2] for x in spec["symbols"]), spec["size"])
            self.assertEqual([x[1] for x in spec["symbols"]],
                             [sum(y[2] for y in spec["symbols"][:i])
                              for i in range(len(spec["symbols"]))])
            ranges.append((spec["offset"], spec["offset"]+spec["size"]))
        for i, (start,end) in enumerate(ranges):
            for j,(other_start,other_end) in enumerate(ranges):
                if i!=j:
                    self.assertTrue(end<=other_start or other_end<=start)


if __name__ == "__main__":
    unittest.main()

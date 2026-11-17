"""ROM-free safety and symmetry tests for future memory-discovery proposals."""
import unittest

from practice.region_crosswalk_agent import propose_other_region


class AgentCrosswalkTests(unittest.TestCase):
    def test_usa_to_jp_benkei_mask(self):
        rows = propose_other_region("usa", 0x8015C60C, mask=0x20)
        self.assertTrue(any(p.key == "event:benkei_encounter" for p in rows))
        target = next(p for p in rows if p.key == "event:benkei_encounter")
        self.assertEqual(target.target_address, "0x80161DFC")
        self.assertEqual(target.status, "user-confirmed")

    def test_jp_to_usa_benkei_mask(self):
        rows = propose_other_region("japan", 0x80161DFC, mask=0x20)
        self.assertIn("0x8015C60C", {p.target_address for p in rows})

    def test_snowflake_known_exception_beats_subtraction(self):
        rows = propose_other_region("japan", 0x80162057)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].target_address, "0x8015C866")
        self.assertIn("exception", rows[0].note)

    def test_disputed_pause_stays_disputed(self):
        self.assertEqual(
            propose_other_region("japan", 0x800CD2D6)[0].status, "disputed")

    def test_unlisted_requires_classification(self):
        with self.assertRaisesRegex(ValueError, "classify"):
            propose_other_region("usa", 0x8015C777)

    def test_reverse_and_forward_proposals_are_candidates(self):
        jp = propose_other_region("usa", 0x8015C777, kind="saved-event", mask=0x08)[0]
        self.assertEqual(jp.target_address, "0x80161F67")
        self.assertEqual(jp.status, "offset-candidate")
        usa = propose_other_region("japan", 0x80161F67, kind="saved-event", mask=0x08)[0]
        self.assertEqual(usa.target_address, "0x8015C777")
        self.assertEqual(usa.status, "offset-candidate")

    def test_reject_dynamic_or_overlay_addresses_even_with_kind(self):
        for region, address in [
            ("usa", 0x801FC60C), ("usa", 0x801C77E0),
            ("usa", 0x802F7060), ("japan", 0x80151B10)]:
            with self.subTest(region=region, address=address):
                with self.assertRaisesRegex(ValueError, "do not offset"):
                    propose_other_region(region, address, kind="static-global")

    def test_known_unequal_width_is_reported(self):
        results = propose_other_region("japan", 0x80161DDA)
        ryo = next(p for p in results if p.key == "static:ryo_low16")
        self.assertEqual(ryo.target_address, "0x8015C5EA")
        self.assertEqual(ryo.width_bytes, 2)

    def test_no_automatic_writable_promotion(self):
        p = propose_other_region("usa", 0x8015C777, kind="static-global")[0]
        self.assertEqual(p.status, "offset-candidate")
        self.assertNotIn("verified", p.key)


if __name__ == "__main__":
    unittest.main()

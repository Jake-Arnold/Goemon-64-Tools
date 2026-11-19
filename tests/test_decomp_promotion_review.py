"""Fail-closed checks for original-address promotion candidates, without ROM assets."""
import copy
import json
from pathlib import Path
import unittest

from decomp import promotion_review as review

ROOT = Path(__file__).resolve().parent.parent


class PromotionReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.queue = json.loads(review.QUEUE_PATH.read_text())

    def test_queue_is_research_only_and_no_candidate_was_previously_accepted(self):
        result = review.validate(self.queue, ROOT)
        self.assertEqual(result['review_candidates'], 0)
        self.assertEqual(result['review_instruction_bytes'], 0)
        self.assertEqual(result['blocked_not_ready'], 1)
        self.assertEqual(result['by_segment'], {})

    def test_duplicate_rejected(self):
        changed = copy.deepcopy(self.queue)
        changed['blocked_not_promotion_ready'].append(copy.deepcopy(changed['blocked_not_promotion_ready'][0]))
        with self.assertRaisesRegex(review.ReviewError, 'duplicate'):
            review.validate(changed, ROOT)

    def test_false_promotion_rejected(self):
        changed = copy.deepcopy(self.queue)
        changed['blocked_not_promotion_ready'][0]['canonical_g2'] = 'PASSED_G2'
        with self.assertRaisesRegex(review.ReviewError, 'unverified promotion'):
            review.validate(changed, ROOT)

    def test_tampered_source_provenance_rejected(self):
        changed = copy.deepcopy(self.queue)
        changed['blocked_not_promotion_ready'][0]['source']['git_blob_sha'] = 'unknown'
        with self.assertRaisesRegex(review.ReviewError, 'source provenance'):
            review.validate(changed, ROOT)

    def test_blocked_candidate_cannot_be_counted_as_ready(self):
        changed = copy.deepcopy(self.queue)
        changed['blocked_not_promotion_ready'][0]['review_state'] = 'PROMOTION_CANDIDATE'
        with self.assertRaisesRegex(review.ReviewError, 'blocked research'):
            review.validate(changed, ROOT)

    def test_source_blob_verification_works_for_local_graphics(self):
        # The former five graphics sources are now accepted. Validate their archived blob pins.
        historical=json.loads((ROOT/'decomp/data/promotion_candidates_1225_before_graphics5_20261118.json').read_text())
        row=next(x for x in historical['candidates'] if x['segment']=='main')
        f = ROOT / row['source']['path']
        self.assertTrue(f.is_file())
        self.assertEqual(review.git_blob_sha(f.read_bytes()), row['source']['git_blob_sha'])

    def test_wrong_original_rom_rejected(self):
        with self.assertRaisesRegex(review.ReviewError, 'wrong original USA'):
            review.validate(self.queue, ROOT, rom=b'not a rom')


if __name__ == '__main__':
    unittest.main()

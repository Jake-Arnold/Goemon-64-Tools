"""No-ROM regression for compact task context and proof consistency."""
import unittest
from decomp import skill_context as sc


class TaskBriefTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sc.load()

    def test_records_are_consistent(self):
        self.assertEqual(sc.validate(self.data), [])

    def test_bounded_brief(self):
        result = sc.task_brief(self.data, "G64-031")
        self.assertEqual(result["task"], "G64-031")
        self.assertNotIn("steps", result)
        self.assertIn("focus_files", result)

    def test_detailed_packet_is_opt_in(self):
        self.assertTrue(sc.task_brief(self.data, "G64-031", True)["steps"])

    def test_corrupted_count_rejected(self):
        bad = {**self.data, "proof": {**self.data["proof"],
                                     "matched": self.data["proof"]["matched"] - 1}}
        self.assertTrue(sc.validate(bad))

    def test_unknown_task_rejected(self):
        with self.assertRaises(ValueError):
            sc.task_brief(self.data, "G64-999")

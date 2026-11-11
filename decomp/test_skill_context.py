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

    def test_architect_v2_is_visible_without_full_task_packet(self):
        b = sc.task_brief(self.data, "G64-035")
        self.assertEqual(b["architect_override_v2"]["wave"], "A")
        self.assertIn("220B", b["architect_override_v2"]["directive"])
        self.assertEqual(sc.task_brief(self.data, "G64-071")["architect_override_v2"]["wave"], "B")

    def test_current_task_status_and_next_task_dependencies(self):
        tasks = sc.load()["tasks"]
        self.assertEqual(tasks[33]["status"], "RESEARCH_ONLY")
        self.assertEqual(tasks[34]["id"], "G64-035")
        self.assertEqual(tasks[34]["status"], "RESEARCH_ONLY")
        self.assertEqual(tasks[35]["id"], "G64-036")
        self.assertEqual(tasks[35]["status"], "RESEARCH_ONLY")
        self.assertEqual(tasks[36]["id"], "G64-037")
        self.assertEqual(tasks[36]["status"], "PLANNED")
        self.assertEqual(tasks[36]["depends_on"], ["G64-021"])
        self.assertNotIn("architect_override_v2", tasks[33])

    def test_detailed_packet_is_opt_in(self):
        self.assertTrue(sc.task_brief(self.data, "G64-031", True)["steps"])

    def test_corrupted_count_rejected(self):
        bad = {**self.data, "proof": {**self.data["proof"],
                                     "matched": self.data["proof"]["matched"] - 1}}
        self.assertTrue(sc.validate(bad))

    def test_unknown_task_rejected(self):
        with self.assertRaises(ValueError):
            sc.task_brief(self.data, "G64-999")

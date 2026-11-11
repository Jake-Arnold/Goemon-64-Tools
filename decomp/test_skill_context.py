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

    def test_plan_structure_and_execution_evidence_are_consistent(self):
        tasks = self.data["tasks"]
        self.assertEqual(sc.validate(self.data), [])
        self.assertLessEqual({task["status"] for task in tasks}, sc.TASK_STATUSES)
        self.assertTrue(all(task.get("evidence_requirements") for task in tasks))
        self.assertTrue(self.data["execution_records"])

    def test_unknown_status_is_rejected(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[0]["status"] = "DONE"
        self.assertTrue(any("Invalid task status" in error
                            for error in sc.validate({**self.data, "tasks": tasks})))

    def test_malformed_status_type_is_rejected_without_crashing(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[0]["status"] = []
        self.assertTrue(any("Invalid task status" in error
                            for error in sc.validate({**self.data, "tasks": tasks})))

    def test_execution_evidence_includes_current_task_status(self):
        records = [dict(record) for record in self.data["execution_records"]]
        task_id = records[0]["task_id"]
        for record in records:
            if record["task_id"] == task_id:
                record["status"] = "PLANNED" if record["status"] != "PLANNED" else "DOC_ONLY"
        self.assertTrue(any("no report for current task status" in error
                            for error in sc.validate({**self.data, "execution_records": records})))

    def test_status_progress_is_valid_when_evidence_tracks_it(self):
        # Validation follows the ledger's status/evidence relationship instead
        # of pinning whichever task happened to be active when tests were written.
        tasks = [dict(task) for task in self.data["tasks"]]
        records = [dict(record) for record in self.data["execution_records"]]
        task_id = records[0]["task_id"]
        current = next(task for task in tasks if task["id"] == task_id)["status"]
        changed = next(status for status in sorted(sc.TASK_STATUSES)
                       if status != current)
        next(task for task in tasks if task["id"] == task_id)["status"] = changed
        for record in records:
            if record["task_id"] == task_id:
                record["status"] = changed
        self.assertEqual(sc.validate({**self.data, "tasks": tasks,
                                      "execution_records": records}), [])

    def test_duplicate_task_id_is_rejected(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[1]["id"] = tasks[0]["id"]
        self.assertTrue(sc.validate({**self.data, "tasks": tasks}))

    def test_task_dependency_must_point_to_an_earlier_task(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[1]["depends_on"] = [tasks[1]["id"]]
        self.assertTrue(any("Invalid dependency" in error
                            for error in sc.validate({**self.data, "tasks": tasks})))

    def test_task_ordinal_must_match_ledger_position(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[0]["ordinal"] = 2
        self.assertTrue(any("ordinal" in error
                            for error in sc.validate({**self.data, "tasks": tasks})))

    def test_task_evidence_requirements_must_be_present(self):
        tasks = [dict(task) for task in self.data["tasks"]]
        tasks[0]["evidence_requirements"] = []
        self.assertTrue(any("evidence requirements" in error
                            for error in sc.validate({**self.data, "tasks": tasks})))

    def test_detailed_packet_is_opt_in(self):
        self.assertTrue(sc.task_brief(self.data, "G64-031", True)["steps"])

    def test_corrupted_count_rejected(self):
        bad = {**self.data, "proof": {**self.data["proof"],
                                     "matched": self.data["proof"]["matched"] - 1}}
        self.assertTrue(sc.validate(bad))

    def test_unknown_task_rejected(self):
        with self.assertRaises(ValueError):
            sc.task_brief(self.data, "G64-999")

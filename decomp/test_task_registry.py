"""ROM-free task registry regression coverage."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from decomp import task_registry as r


class TaskRegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = r.read_registry()

    def test_checked_in_registry_valid(self):
        self.assertEqual(r.validate(self.data), [])
        self.assertGreaterEqual(len(self.data["tasks"]), 10)
        self.assertEqual(self.data["branch"], "chatgptweb/decomp")

    def test_distinct_and_actionable(self):
        ids = {t["id"] for t in self.data["tasks"]}
        self.assertIn("GQ-CRIGHT-001", ids)
        self.assertIn("GQ-USA-001", ids)
        self.assertIn("GQ-JP-001", ids)
        self.assertIn("GQ-MAINT-001", ids)
        self.assertTrue(any(t["status"] == "blocked_external" for t in self.data["tasks"]))
        self.assertTrue(any(t["status"] == "blocked_rebase" for t in self.data["tasks"]))

    def test_order_and_filter(self):
        all_tasks = r.ordered(self.data)
        self.assertEqual(all_tasks, sorted(all_tasks, key=lambda t: (t["priority"], t["id"])))
        self.assertTrue(all(t["status"] in r.ACTIVE for t in all_tasks))
        self.assertTrue(all(t["region"] in ("usa", "both") for t in r.ordered(self.data, region="usa")))
        self.assertTrue(all(t["status"] == "pending" for t in r.ordered(self.data, status="pending")))
        d = copy.deepcopy(self.data)
        d["tasks"][0]["status"] = "superseded"
        self.assertNotIn(d["tasks"][0], r.ordered(d))
        self.assertIn(d["tasks"][0], r.ordered(d, status="superseded"))

    def test_bad_inputs_fail_closed(self):
        d = copy.deepcopy(self.data)
        d["tasks"][1]["id"] = d["tasks"][0]["id"]
        self.assertTrue(any("duplicate ID" in e for e in r.validate(d)))
        d = copy.deepcopy(self.data)
        d["tasks"][0]["conflicts_with"] = ["GQ-UNKNOWN-999"]
        self.assertTrue(any("invalid conflict" in e for e in r.validate(d)))
        d = copy.deepcopy(self.data)
        d["tasks"][0]["status"] = "done"
        self.assertTrue(any("completion_proof" in e for e in r.validate(d)))

    def test_malformed_json_returns_schema_errors_not_tracebacks(self):
        """Invalid JSON value types must fail closed, including through the CLI."""
        malformed = [None, [], 23]
        for label, mutate in (
            ("head_type", lambda d: d.update(reconciled_head=[])),
            ("non_object_task", lambda d: d["tasks"].append(None)),
            ("id_type", lambda d: d["tasks"][0].update(id=[])),
            ("status_type", lambda d: d["tasks"][0].update(status=[])),
            ("workstream_type", lambda d: d["tasks"][0].update(workstream={})),
            ("conflict_type", lambda d: d["tasks"][0].update(conflicts_with=[[]])),
        ):
            d = copy.deepcopy(self.data)
            mutate(d)
            malformed.append(d)
        for bad in malformed:
            with self.subTest(value=repr(bad)[:100]):
                self.assertTrue(r.validate(bad))
        with tempfile.TemporaryDirectory() as work:
            target = Path(work) / "bad_registry.json"
            target.write_text(json.dumps({"format": "goemon-task-registry-v1",
                                          "tasks": [None]}), encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as stream:
                self.assertEqual(r.main(["--registry", str(target), "validate"]), 2)
            self.assertIn("INVALID:", stream.getvalue())

    def test_checkpoint_sha_and_history(self):
        with tempfile.TemporaryDirectory() as work:
            target = Path(work) / "registry.json"
            target.write_text(json.dumps(self.data) + "\n", encoding="utf-8")
            original = r.digest(target)
            with self.assertRaisesRegex(ValueError, "changed since fingerprint"):
                r.write_checkpoint(target, r.read_registry(target), "GQ-CRIGHT-001",
                                   status="blocked_external", note="still remote", next_step=None,
                                   evidence=[], expected="0" * 64)
            self.assertEqual(r.digest(target), original)
            with self.assertRaisesRegex(ValueError, "done requires"):
                r.write_checkpoint(target, r.read_registry(target), "GQ-CRIGHT-001",
                                   status="done", note="pretend", next_step=None,
                                   evidence=[], expected=original)
            changed = r.read_registry(target)
            r.write_checkpoint(target, changed, "GQ-CRIGHT-001", status="blocked_external",
                               note="Remote tester unavailable; read-only capture pending",
                               next_step="Wait for real Project64 JSONL", evidence=[], expected=original)
            result = r.read_registry(target)
            t = r.get_task(result, "GQ-CRIGHT-001")
            self.assertEqual(t["history"][-1]["note"], "Remote tester unavailable; read-only capture pending")
            self.assertEqual(t["next_step"], "Wait for real Project64 JSONL")
            self.assertNotEqual(original, r.digest(target))
            self.assertEqual(r.validate(result), [])

    def test_cli_list_resume_and_validation(self):
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(r.main(["list", "--workstream", "japan-glitch"]), 0)
        self.assertIn("GQ-CRIGHT-001", stream.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(r.main(["resume", "GQ-CRIGHT-001"]), 0)
        self.assertIn("HANDOFF:", stream.getvalue())
        self.assertIn("BLOCKED:", stream.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(r.main(["validate"]), 0)
        self.assertIn("VALID:", stream.getvalue())

    def test_unknown_task_is_error_not_new_task(self):
        with contextlib.redirect_stderr(io.StringIO()) as stream:
            self.assertEqual(r.main(["show", "GQ-NONE-999"]), 2)
        self.assertIn("Unknown task", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
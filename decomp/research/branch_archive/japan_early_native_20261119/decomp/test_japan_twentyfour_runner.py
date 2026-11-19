"""ROM-free guardrails for the canonical Japanese 24-C build entrypoint.

The canonical runner must never invoke the earlier 18-function stage while
requesting a 24-C Splat layout. That mismatch can silently invalidate the
complete-ROM verification workflow.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "build_japan_twentyfour_c.sh"
VERIFIER = ROOT / "japan_twentyfour_verify.py"


class Japanese24CRunnerTests(unittest.TestCase):
    def test_all_stage_steps_use_the_twentyfour_module(self):
        body = RUNNER.read_text(encoding="utf-8")
        for operation in ("stage", "install", "layout"):
            with self.subTest(operation=operation):
                statement = "run_module decomp.japan_twentyfour_c " + operation
                self.assertEqual(body.count(statement), 1)
                self.assertNotIn(
                    "run_module decomp.japan_eighteen_c " + operation, body
                )

    def test_config_sources_and_verifier_are_from_same_revision(self):
        body = RUNNER.read_text(encoding="utf-8")
        self.assertIn("Usage: build_japan_twentyfour_c.sh", body)
        self.assertIn("splat_twentyfour_c.local.yaml", body)
        self.assertIn("run_module decomp.japan_twentyfour_verify", body)
        self.assertIn("build/japan_0/twentyfour-layout-proof.json", body)
        self.assertIn("build/japan_0/twentyfour-proof.json", body)
        self.assertIn("mnsg.twentyfour-c.retail.z64", body)
        self.assertNotIn("eighteen_c", body)
        self.assertEqual(body.count("src/jp_"), 20)

    def test_verifier_reports_correct_accepted_revision(self):
        body = VERIFIER.read_text(encoding="utf-8")
        self.assertIn("JAPAN 24-C PASS:", body)
        self.assertNotIn("JAPAN 18-C PASS:", body)


if __name__ == "__main__":
    unittest.main()

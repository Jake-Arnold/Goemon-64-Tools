"""Tests for ROM-free local CI orchestration (no compiler or private ROM needed)."""

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from decomp import local_ci


class LocalCITests(unittest.TestCase):
    def test_default_runs_python_validation_then_host_sanitizers(self):
        with tempfile.TemporaryDirectory() as directory:
            steps = local_ci.build_steps(Path(directory) / "host")
        self.assertEqual(len(steps), 11)
        self.assertTrue(any(path.endswith("test_host132.c") for path in steps[9][1]))
        self.assertEqual(sum(path.endswith(".c") and "usa_wide132_promotion_20261118/host_sources" in path for path in steps[9][1]), 9)
        self.assertEqual(len(steps[10][1]), 1)
        self.assertIn("test_*.py", steps[0][1])
        self.assertIn("test_decomp_*.py", steps[1][1])
        self.assertEqual(steps[2][1][-1], "--validate")
        self.assertIn("-fsanitize=address,undefined", steps[3][1])
        self.assertEqual(len(steps[4][1]), 1)
        self.assertTrue(any(path.endswith("test_actual87.c") for path in steps[5][1]))
        self.assertEqual(len(steps[6][1]), 1)
        self.assertTrue(any(path.endswith("file27_adjacent21_20261117/test_adjacent27.c") for path in steps[7][1]))
        self.assertEqual(sum(path.endswith(".c") and "file27_promotion_20261118/sources" in path for path in steps[7][1]), 21)
        self.assertEqual(len(steps[8][1]), 1)

    def test_quick_runs_all_python_gates_without_native_compile(self):
        with tempfile.TemporaryDirectory() as directory:
            steps = local_ci.build_steps(Path(directory) / "host", quick=True)
        self.assertEqual(len(steps), 3)
        self.assertTrue(all("cc" not in step[0].lower() for step in steps))

    @patch.object(local_ci.subprocess, "run")
    def test_fails_closed_on_first_nonzero_exit(self, run):
        run.side_effect = [subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 9)]
        self.assertEqual(local_ci.main(["--quick"]), 9)
        self.assertEqual(run.call_count, 2)

    @patch.object(local_ci.subprocess, "run")
    def test_success_is_not_stealth_full_rom_proof(self, run):
        run.return_value = subprocess.CompletedProcess([], 0)
        self.assertEqual(local_ci.main(["--quick"]), 0)
        self.assertEqual(run.call_count, 3)

    @patch.object(local_ci.subprocess, "run", side_effect=FileNotFoundError("compiler missing"))
    def test_missing_executable_fails(self, run):
        self.assertEqual(local_ci.main(["--quick"]), 127)


if __name__ == "__main__":
    unittest.main()

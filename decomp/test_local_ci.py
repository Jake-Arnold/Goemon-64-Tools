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
        self.assertEqual(len(steps), 47)
        self.assertIn("Native100 original-C 1000-case host sanitizer test", [name for name, _ in steps])
        self.assertEqual(steps[30][0], "USA 92F0 A18C/A548/A5C4/AAE8/AB30/108BC actual-source sanitizer build")
        self.assertTrue(any(path.endswith("test_usa_92f0_a18c_aae8.c") for path in steps[30][1]))
        self.assertIn("-fsanitize=address,undefined", steps[30][1])
        self.assertIn("-Wno-pointer-to-int-cast", steps[30][1])
        self.assertEqual(steps[31][0], "USA 92F0 A18C/A548/A5C4/AAE8/AB30/108BC actual-source sanitizer test")
        self.assertEqual(steps[32][0], "Mini reset 148B original-source sanitizer build")
        self.assertEqual(steps[33][0], "Mini reset 148B original-source sanitizer test")
        self.assertEqual(steps[34][0], "Speed ease 220B original-source sanitizer build")
        self.assertEqual(steps[35][0], "Speed ease 220B original-source sanitizer test")
        # Eight new build/test gates exercise all eleven *actual* native C bodies.
        for idx,label in ((36,'seven'),(38,'conditional'),(40,'pair'),(42,'selector')):
            self.assertEqual(steps[idx][0],f'USA Mini11 {label} actual C ASan/UBSan host build')
            self.assertEqual(steps[idx+1][0],f'USA Mini11 {label} actual C ASan/UBSan host regression')
            self.assertIn('-fsanitize=address,undefined',steps[idx][1])
            self.assertEqual(len(steps[idx+1][1]),1)
        self.assertTrue(any(x.endswith('mini_selector.c') for x in steps[42][1]))
        self.assertEqual(steps[44][0], "Resumable task registry validation")
        self.assertEqual(steps[44][1][-2:], ["decomp.task_registry", "validate"])
        self.assertEqual(steps[45][0], "C-Right live-trace comparator tests")
        self.assertIn("decomp/tasks/cright_live_trace", steps[45][1])
        self.assertEqual(steps[46][0], "Canonical promotion integrity (manifest+G2+inventory)")
        self.assertEqual(steps[46][1][-2:], ["decomp.promotion_integrity", "--validate"])

        self.assertTrue(any(path.endswith("test_actual109.c") for path in steps[11][1]))
        self.assertEqual(sum(path.endswith(".c") and "usa_wide109_promotion_20261118/sources" in path for path in steps[11][1]), 68)
        self.assertEqual(len(steps[12][1]), 1)
        self.assertTrue(any(path.endswith('test_actual_file18_callbacks.c') for path in steps[13][1]))
        self.assertEqual(sum(path.endswith('.c') and 'pending_file18_53_20261118/sources' in path for path in steps[13][1]), 50)
        self.assertEqual(sum(path.endswith('.c') and 'pending_callbacks10_20261118/sources' in path for path in steps[13][1]), 3)
        self.assertEqual(len(steps[14][1]), 1)
        self.assertTrue(any(path.endswith("test_actual_tiny9.c") for path in steps[15][1]))
        self.assertEqual(sum(path.endswith(".c") and "pending_tiny9_20261119/sources" in path for path in steps[15][1]), 7)
        self.assertEqual(len(steps[16][1]), 1)
        self.assertTrue(any(path.endswith('test_actual_menu2.c') for path in steps[17][1]))
        self.assertEqual(sum(path.endswith('.c') and 'pending_menu2_20261119/sources' in path for path in steps[17][1]), 2)
        self.assertEqual(len(steps[18][1]), 1)
        self.assertTrue(any(path.endswith('test_actual_archive22.c') for path in steps[19][1]))
        self.assertEqual(sum(path.endswith('.c') and 'pending_archive22_20261119/sources' in path for path in steps[19][1]), 22)
        self.assertIn('-fsanitize=address,undefined',steps[19][1])
        self.assertEqual(len(steps[20][1]), 1)
        self.assertTrue(any(path.endswith('test_actual_archive33.c') for path in steps[21][1]))
        self.assertEqual(sum(path.endswith('.c') and 'pending_archive33_20261120/sources' in path for path in steps[21][1]),33)
        self.assertIn('-fsanitize=address,undefined', steps[21][1])
        self.assertEqual(len(steps[22][1]),1)
        self.assertIn('test_actual_sources',steps[23][1][-1])
        self.assertTrue(any(path.endswith('test_actual_checkpoint500.c') for path in steps[24][1]))
        self.assertEqual(sum(path.endswith('checkpoint500_000.c') for path in steps[24][1]),1)
        self.assertIn('-fsanitize=address,undefined',steps[24][1])
        self.assertEqual(len(steps[25][1]),1)
        self.assertTrue(any(path.endswith("test_actual_rediscovery5.c") for path in steps[26][1]))
        self.assertEqual(sum("/sources/rediscovery5_" in path and path.endswith(".c") for path in steps[26][1]),5)
        self.assertEqual(len(steps[27][1]),1)
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
        self.assertEqual(len(steps), 6)
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
        self.assertEqual(run.call_count, 6)

    @patch.object(local_ci.subprocess, "run", side_effect=FileNotFoundError("compiler missing"))
    def test_missing_executable_fails(self, run):
        self.assertEqual(local_ci.main(["--quick"]), 127)


if __name__ == "__main__":
    unittest.main()

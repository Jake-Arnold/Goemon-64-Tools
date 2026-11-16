"""Linux native speed-channel interoperability with a synthetic C++ host."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from speed.live_control import SpeedUnavailable, read_speed, request_speed

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(sys.platform == "linux", "Native Linux only")
class LinuxSpeedChannelTests(unittest.TestCase):
    def test_patched_host_acknowledges_exact_rate(self):
        compiler = shutil.which("g++") or shutil.which("clang++")
        if not compiler:
            self.skipTest("C++ compiler missing")
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "speed-host"
            subprocess.run([compiler, "-std=c++17", "-O1", "-Wall", "-Wextra",
                            "-Werror", "-pthread", "-Ispeed",
                            "speed/test_linux_speed_channel.cpp", "-o", str(binary)],
                           cwd=ROOT, check=True, timeout=30, capture_output=True)
            process = subprocess.Popen([str(binary)], cwd=ROOT)
            try:
                deadline = time.monotonic() + 4
                initial = None
                while time.monotonic() < deadline:
                    try:
                        initial = read_speed(process.pid)
                        break
                    except SpeedUnavailable:
                        if process.poll() is not None:
                            break
                        time.sleep(.02)
                self.assertIsNotNone(initial, "Synthetic native host never exposed a valid channel")
                self.assertEqual((initial.requested, initial.applied), (1, 1))
                request_speed(process.pid, 4)
                applied = None
                while time.monotonic() < deadline:
                    try:
                        applied = read_speed(process.pid).applied
                    except SpeedUnavailable:
                        break
                    if applied == 4:
                        break
                    time.sleep(.02)
                self.assertEqual(applied, 4)
                self.assertEqual(process.wait(timeout=5), 0)
            finally:
                if process.poll() is None:
                    process.terminate()
                process.wait(timeout=5)
                # Terminated hosts may not run atexit; only remove our own
                # test process's IPC name, never an unrelated user's channel.
                leftover = Path(f"/dev/shm/goemon64speed_{process.pid}")
                if leftover.is_file() and leftover.stat().st_uid == os.geteuid():
                    leftover.unlink()

    def test_unpatched_process_does_not_expose_speed_control(self):
        with self.assertRaises(SpeedUnavailable):
            read_speed(os.getpid())


if __name__ == "__main__":
    unittest.main()

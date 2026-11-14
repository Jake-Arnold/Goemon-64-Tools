"""Linux native process tests. No ROM, game or unsafe external PID required."""
from __future__ import annotations

import subprocess
import sys
import unittest

from autosplitter.linux_process import LinuxProcess


class LinuxProcessTests(unittest.TestCase):
    def test_readable_maps_only(self):
        lines = [
            "00400000-00401000 r-xp 0000 00:01 0 /test\n",
            "00401000-00402000 ---p 0000 00:01 0\n",
            "00402000-00403000 rw-p 0000 00:01 0\n",
            "broken\n",
        ]
        self.assertEqual(list(LinuxProcess._iter_readable_maps(lines)),
                         [(0x400000, 0x1000), (0x402000, 0x1000)])

    @unittest.skipUnless(sys.platform == "linux", "Linux-only")
    def test_invalid_pid(self):
        with self.assertRaises(ValueError):
            LinuxProcess(0)
        with self.assertRaises(ValueError):
            LinuxProcess(True)

    @unittest.skipUnless(sys.platform == "linux", "Linux-only")
    def test_child_read_and_explicit_write(self):
        child_code = """import ctypes, time
b = ctypes.create_string_buffer(b'goemon-native-ram')
print(ctypes.addressof(b), flush=True)
time.sleep(30)
"""
        child = subprocess.Popen([sys.executable, "-c", child_code],
                                 stdout=subprocess.PIPE, text=True)
        try:
            address = int(child.stdout.readline().strip())
            proc = LinuxProcess(child.pid)
            self.assertEqual(proc.read(address, 17), b"goemon-native-ram")
            with self.assertRaises(PermissionError):
                proc.write(address, b"W")
            self.assertTrue(any(start <= address < start + length
                                for start, length in proc.regions()))
            proc.close()
            with self.assertRaises(OSError):
                proc.read(address, 1)
            writer = LinuxProcess(child.pid, writable=True)
            writer.write(address, b"Goemon")
            self.assertEqual(writer.read(address, 17), b"Goemon-native-ram")
            writer.close()
        finally:
            child.terminate()
            child.wait(timeout=5)
            child.stdout.close()

    @unittest.skipUnless(sys.platform == "linux", "Linux-only")
    def test_toolkit_writes_default_and_explicit_read_only(self):
        from practice.toolkit import parse_args
        normal=parse_args([])
        self.assertFalse(normal.read_only)
        self.assertTrue(normal.enable_hex_edit)
        self.assertTrue(normal.enable_teleport)
        self.assertFalse(parse_args(["--linux-enable-writes"]).read_only)
        limited=parse_args(["--linux-enable-writes","--read-only"])
        self.assertTrue(limited.read_only)
        self.assertFalse(limited.enable_hex_edit)


if __name__ == "__main__":
    unittest.main()

"""Synthetic directory tests for the pinned MIPS binutils runtime bootstrap."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from prepare_mips_binutils import BINUTILS_LIBRARIES, TOOLS, configure


class BinutilsBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'archive'
        self.bin = self.root / 'usr/bin'
        self.lib = self.root / 'usr/lib/x86_64-linux-gnu'
        self.runtime = Path(self.tmp.name) / 'runtime'
        self.bin.mkdir(parents=True)
        self.lib.mkdir(parents=True)
        for tool in TOOLS:
            exe = self.bin / f'mips-linux-gnu-{tool}'
            exe.write_text('#!/bin/sh\necho GNU Binutils 2.45.90.20260125\n')
            exe.chmod(0o755)
        for name in BINUTILS_LIBRARIES:
            (self.lib / name).write_bytes(b'test DSO')
        (self.lib / 'libc.so.6').write_bytes(b'incompatible glibc')

    def test_curated_libs_exclude_glibc_and_support_repeated_setup(self):
        first = configure(self.root, self.runtime)
        second = configure(self.root, self.runtime)
        self.assertEqual(first['LD_LIBRARY_PATH'], second['LD_LIBRARY_PATH'])
        self.assertEqual({p.name for p in self.runtime.iterdir()}, set(BINUTILS_LIBRARIES))
        self.assertFalse((self.runtime / 'libc.so.6').exists())
        self.assertTrue(first['PATH'].startswith(str(self.bin)))

    def test_missing_library_fails(self):
        (self.lib / BINUTILS_LIBRARIES[0]).unlink()
        with self.assertRaisesRegex(ValueError, 'Missing pinned'):
            configure(self.root, self.runtime)

    def test_unexpected_library_in_runtime_fails(self):
        self.runtime.mkdir()
        (self.runtime / 'libc.so.6').write_bytes(b'wrong')
        with self.assertRaisesRegex(ValueError, 'only pinned'):
            configure(self.root, self.runtime)

    def test_refuses_to_replace_unrelated_symlink(self):
        self.runtime.mkdir()
        (self.runtime / BINUTILS_LIBRARIES[0]).symlink_to(self.lib / 'libc.so.6')
        with self.assertRaisesRegex(ValueError, 'different symlink'):
            configure(self.root, self.runtime)

    def test_version_mismatch_fails(self):
        exe = self.bin / 'mips-linux-gnu-ld'
        exe.write_text('#!/bin/sh\necho wrong\n')
        with self.assertRaisesRegex(RuntimeError, 'failed version'):
            configure(self.root, self.runtime)


if __name__ == '__main__':
    unittest.main()

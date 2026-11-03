import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from speed.prepare_runtime import PIN, prepare_runtime


class PrepareRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / 'ultramodern' / 'src'
        self.src.mkdir(parents=True)
        self.timer = self.src / 'timer.cpp'
        self.original = ('#include "ultramodern/ultra64.h"\n'
                         'constexpr uint32_t speed_multiplier = 1;\n'
                         "constexpr uint32_t counter_per_ms = 46'875 * speed_multiplier;\n")
        self.timer.write_text(self.original, encoding='utf-8')
        self.header = self.src / 'goemon_startup_multiplier.h'

    def git(self, revision=PIN, dirty=''):
        return patch('speed.prepare_runtime.subprocess.check_output', side_effect=[revision+'\n', dirty])

    def test_prepare_writes_only_expected_timing_changes(self):
        with self.git(): prepare_runtime(self.root)
        content = self.timer.read_text(encoding='utf-8')
        self.assertIn('#include "goemon_startup_multiplier.h"', content)
        self.assertIn('const uint32_t speed_multiplier = goemon_speed::startup_multiplier();', content)
        self.assertIn("const uint32_t counter_per_ms = 46'875 * speed_multiplier;", content)
        self.assertTrue(self.header.is_file())
        with self.git():
            with self.assertRaises(ValueError): prepare_runtime(self.root)

    def test_dirty_or_wrong_revision_refused_without_mutation(self):
        for revision, dirty in [('0'*40, ''), (PIN, ' M some_file\n')]:
            with self.git(revision,dirty):
                with self.assertRaises(ValueError): prepare_runtime(self.root)
            self.assertEqual(self.timer.read_text(encoding='utf-8'),self.original)
            self.assertFalse(self.header.exists())

    def test_unknown_layout_and_existing_header_are_preserved(self):
        self.timer.write_text('different', encoding='utf-8')
        with self.git():
            with self.assertRaises(ValueError): prepare_runtime(self.root)
        self.assertEqual(self.timer.read_text(encoding='utf-8'),'different')
        self.timer.write_text(self.original, encoding='utf-8')
        self.header.write_text('existing', encoding='utf-8')
        with self.git():
            with self.assertRaises(ValueError): prepare_runtime(self.root)
        self.assertEqual(self.header.read_text(encoding='utf-8'),'existing')
        self.assertEqual(self.timer.read_text(encoding='utf-8'),self.original)

    def test_failed_atomic_replace_keeps_original(self):
        with self.git(), patch('speed.prepare_runtime.os.replace', side_effect=OSError('failure')):
            with self.assertRaises(OSError): prepare_runtime(self.root)
        self.assertEqual(self.timer.read_text(encoding='utf-8'),self.original)
        self.assertFalse(self.header.exists())
        self.assertEqual(sorted(p.name for p in self.src.iterdir()),['timer.cpp'])

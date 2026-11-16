"""Keep the toolkit's release version consistent across documentation and UI."""
from pathlib import Path
import re
import unittest

from practice.version import VERSION, DISPLAY_VERSION


ROOT = Path(__file__).resolve().parents[1]


class ToolkitVersionTests(unittest.TestCase):
    def test_version_is_semver_and_display_is_derived(self):
        self.assertRegex(VERSION, r'^\d+\.\d+\.\d+$')
        self.assertEqual(DISPLAY_VERSION, 'v' + VERSION)

    def test_release_heading_and_progress_reference_current_version(self):
        heading = (ROOT / 'README.md').read_text(encoding='utf-8').splitlines()[0]
        self.assertTrue(heading.startswith(
            '# Goemon Speedrun Tools ' + DISPLAY_VERSION), heading)
        self.assertIn(DISPLAY_VERSION, (
            ROOT / 'PROGRESS.md').read_text(encoding='utf-8')[:2800])

    def test_toolkit_window_uses_canonical_version(self):
        source = (ROOT / 'practice' / 'toolkit.py').read_text(encoding='utf-8')
        self.assertIn('from practice.version import DISPLAY_VERSION', source)
        self.assertIn('Goemon Practice Toolkit {DISPLAY_VERSION}', source)
        self.assertIn('{DISPLAY_VERSION}  |', source)
        launcher = (ROOT / 'Run.bat').read_text(encoding='utf-8')
        self.assertIn('GOEMON_VERSION', launcher)
        self.assertIn('from practice.version import DISPLAY_VERSION', launcher)
        self.assertNotIn('v0.11.17', launcher)
        linux = (ROOT / 'Run-Linux.sh').read_text(encoding='utf-8')
        self.assertIn('python -m practice.toolkit', linux)
        self.assertNotIn('--game-version', linux)
        self.assertNotIn('--read-only', linux)
        self.assertNotRegex(source, r'Goemon Practice Toolkit v\d+\.\d+\.\d+')


if __name__ == '__main__':
    unittest.main()

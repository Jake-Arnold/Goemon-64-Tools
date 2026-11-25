"""Packaging contract tests; Windows executable build itself requires Windows."""
from __future__ import annotations
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from practice import paths
from goemon_app import DEFAULT_PRACTICE_FLAGS

ROOT = Path(__file__).resolve().parents[1]


class TestWindowsPackaging(unittest.TestCase):
    def test_assets_available_for_bundling(self):
        self.assertTrue((ROOT / 'assets/goemon_tools_logo.ico').is_file())
        self.assertTrue((ROOT / 'assets/goemon_tools_logo.png').is_file())
        self.assertTrue((ROOT / 'assets/goemon_tools_logo_small.png').is_file())
        self.assertTrue((ROOT / 'docs/images/actual-dashboard.webp').is_file())
        self.assertTrue((ROOT / 'docs/images/readme-showcase.webp').is_file())
        self.assertGreater((ROOT / 'assets/goemon_tools_logo.ico').stat().st_size, 100)

    def test_source_files_remain_in_old_location(self):
        self.assertFalse(paths.is_frozen())
        self.assertEqual(paths.practice_data_dir(), ROOT / 'practice')
        self.assertEqual(paths.resource_root(), ROOT)

    def test_process_backends_are_in_the_practice_package(self):
        from practice.backends import linux_process, memory, process_discovery
        for module in (linux_process, memory, process_discovery):
            self.assertEqual(Path(module.__file__).parent, ROOT / 'practice' / 'backends')
        self.assertFalse((ROOT / 'autosplitter').exists())

    def test_packaged_paths_use_user_folder_and_temp_resources(self):
        import sys
        with tempfile.TemporaryDirectory() as root:
            with patch.object(sys, 'frozen', True, create=True), patch.object(sys, '_MEIPASS', root, create=True), patch.dict('os.environ', {'LOCALAPPDATA': root}):
                self.assertEqual(paths.resource_root(), Path(root))
                self.assertEqual(paths.practice_data_dir(), Path(root) / 'GoemonSpeedrunTools')
                self.assertEqual(paths.diagnostics_dir(), Path(root) / 'GoemonSpeedrunTools' / 'diagnostics')

    def test_entrypoint_matches_run_bat_flags(self):
        launcher = (ROOT / 'Run.bat').read_text()
        self.assertEqual(DEFAULT_PRACTICE_FLAGS, [])
        self.assertIn('%*',launcher)  # Run.bat --read-only reaches shared parser.
        self.assertNotIn('--enable-',launcher)
        self.assertIn('main(sys.argv[1:])',(ROOT / 'goemon_app.py').read_text())

    def test_build_script_embeds_icon_and_app_assets(self):
        script = (ROOT / 'build/Build-Windows.ps1').read_text()
        self.assertIn('PyInstaller', script)
        self.assertIn('--onefile --windowed', script)
        self.assertIn('--icon $Icon', script)
        self.assertIn('goemon_app.py', script)
        self.assertIn('goemon_tools_logo_small.png', script)
        self.assertIn('--collect-data practice', script)
        self.assertIn('--collect-all tkinterdnd2', script)


if __name__ == '__main__':
    unittest.main()

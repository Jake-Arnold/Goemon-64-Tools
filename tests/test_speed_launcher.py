import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from speed.launch_recomp import launch


class LaunchRecompTests(unittest.TestCase):
    def test_launch_passes_rate_in_child_environment_only(self):
        with tempfile.TemporaryDirectory() as temp:
            exe = Path(temp) / 'Goemon64Recompiled.exe'
            exe.write_bytes(b'test fixture')
            original = os.environ.get('GOEMON_SPEED_MULTIPLIER')
            with patch('speed.launch_recomp.subprocess.Popen') as spawn:
                launch(exe, 3)
            args, kwargs = spawn.call_args
            self.assertEqual(args[0], [str(exe.resolve())])
            self.assertEqual(kwargs['cwd'], str(exe.parent.resolve()))
            self.assertEqual(kwargs['env']['GOEMON_SPEED_MULTIPLIER'], '3')
            self.assertNotIn('shell', kwargs)
            self.assertEqual(os.environ.get('GOEMON_SPEED_MULTIPLIER'), original)

    def test_invalid_rates_and_paths_never_spawn(self):
        with tempfile.TemporaryDirectory() as temp:
            exe = Path(temp) / 'game.exe'
            exe.touch()
            with patch('speed.launch_recomp.subprocess.Popen') as spawn:
                for invalid in (0, 5, 1.5, 2.0, True, '2'):
                    with self.assertRaises(ValueError): launch(exe, invalid)
                with self.assertRaises(ValueError): launch(Path(temp), 2)
                with self.assertRaises(FileNotFoundError): launch(Path(temp) / 'missing.exe', 2)
                spawn.assert_not_called()

"""OS access controls are explicit, testable and never implicitly run on Connect."""
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from practice.linux_pid_access import ptrace_scope, external_pid_hint, change_ptrace_scope


class LinuxPIDAccessTests(unittest.TestCase):
    def test_scope_diagnostics(self):
        with TemporaryDirectory() as tmp:
            setting=Path(tmp)/'scope'
            self.assertIsNone(ptrace_scope(setting))
            setting.write_text('1\\n')
            self.assertEqual(ptrace_scope(setting),1)
            self.assertIn('ptrace_scope=1',external_pid_hint(123,scope=1))
            self.assertIn('same-user',external_pid_hint(123,scope=0))

    def test_explicit_polkit_invocation(self):
        proc=subprocess.CompletedProcess([],0,stdout='kernel.yama.ptrace_scope = 0\\n',stderr='')
        with patch('practice.linux_pid_access.shutil.which',side_effect=['/usr/bin/pkexec','/usr/sbin/sysctl']), \
             patch('practice.linux_pid_access.subprocess.run',return_value=proc) as run, \
             patch('practice.linux_pid_access.ptrace_scope',return_value=0):
            self.assertEqual(change_ptrace_scope(0),0)
        cmd=run.call_args.args[0]
        self.assertEqual(cmd[:2],['/usr/bin/pkexec','/usr/sbin/sysctl'])
        self.assertEqual(cmd[-2:],['-w','kernel.yama.ptrace_scope=0'])
        self.assertEqual(run.call_count,1)

    def test_no_privileged_call_for_invalid_value(self):
        with patch('practice.linux_pid_access.subprocess.run') as run:
            with self.assertRaises(ValueError):
                change_ptrace_scope(3)
        run.assert_not_called()

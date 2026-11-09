"""Tests pinned cross-binutils environment propagation into formal build children."""
import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from verify import build_tool_environment, run_build


class StopAtFirstBuild(Exception):
    """Stop before cloning or compiling; capture actual child invocation."""


class VerifyBinutilsRuntimeTests(unittest.TestCase):
    def test_passthrough_without_archive_does_not_mutate_process(self):
        parent = dict(os.environ)
        env = build_tool_environment(None, Path('/unused'))
        self.assertEqual(env, parent)
        self.assertIsNot(env, os.environ)

    def test_selected_root_uses_curated_runtime_and_isolated_env(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = dict(os.environ)
            root = Path(temp)/'pinned'
            runtime = Path(temp)/'runtime'
            child = {'PATH': '/pinned/tools', 'LD_LIBRARY_PATH': '/curated'}
            with patch('verify.configure_binutils', return_value=child) as configure:
                self.assertEqual(build_tool_environment(root, runtime), child)
                configure.assert_called_once_with(root, runtime)
            self.assertEqual(dict(os.environ), parent)

    def test_build_subprocesses_inherit_curated_env(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            rom = base/'rom.z64'
            rom.write_bytes(b'synthetic retail bytes')
            args = SimpleNamespace(upstream=base, workdir=base/'new_work', retail_rom=rom,
                                   binutils_root=base/'cross', uv='uv', jobs=1)
            manifest = {'retail_sha1':hashlib.sha1(rom.read_bytes()).hexdigest(),
                        'upstream_commit':'test-upstream-sha'}
            env = {'PATH': '/bin', 'LD_LIBRARY_PATH': '/curated-only'}
            report = {}
            with patch('verify.configure_binutils', return_value=env) as configure, \
                 patch('verify.subprocess.check_output',return_value='test-upstream-sha') as check_output, \
                 patch('verify.shutil.which',return_value='/bin/true') as which, \
                 patch('verify.subprocess.run',side_effect=StopAtFirstBuild) as run:
                with self.assertRaises(StopAtFirstBuild):
                    run_build(args,manifest,report)
            configure.assert_called_once_with(args.binutils_root, args.workdir/'.binutils-runtime')
            self.assertEqual(report['binutils_runtime'],'pinned_curated')
            self.assertTrue(all(call.kwargs.get('path') == env['PATH'] for call in which.call_args_list))
            # The pinned upstream Git revision is checked before activation.
            # Every subsequent version/build lookup uses the curated env.
            self.assertNotEqual(check_output.call_args_list[0].kwargs['env'], env)
            self.assertTrue(all(call.kwargs['env'] == env for call in check_output.call_args_list[1:]))
            self.assertEqual(run.call_args.kwargs['env'],env)

    def test_failing_archive_configuration_stops_before_make(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            rom=base/'retail'
            rom.write_bytes(b'synthetic')
            args=SimpleNamespace(upstream=base,workdir=base/'new_work',retail_rom=rom,
                                 binutils_root=base/'missing')
            manifest={'retail_sha1':hashlib.sha1(rom.read_bytes()).hexdigest(),
                      'upstream_commit':'test-upstream-sha'}
            with patch('verify.subprocess.check_output',return_value='test-upstream-sha'), \
                 patch('verify.configure_binutils',side_effect=ValueError('bad root')), \
                 patch('verify.subprocess.run') as run:
                with self.assertRaisesRegex(ValueError,'bad root'):
                    run_build(args,manifest,{})
                run.assert_not_called()


if __name__=='__main__':
    unittest.main()

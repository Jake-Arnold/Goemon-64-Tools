"""Local-only Git regression tests for fast-forward toolkit auto-update."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from practice.updater import (
    UpdateError, check_for_updates, install_update, _trusted_origin,
)


@unittest.skipUnless(shutil.which('git'), 'Git command required')
class GitUpdaterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='goemon-updater-')
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.bare = base / 'remote.git'
        self.main = base / 'main-clone'
        self.other = base / 'other-clone'
        self.run_git(base, 'init', '--bare', str(self.bare))
        self.run_git(base, 'init', '-b', 'main', str(self.main))
        self._identity(self.main)
        (self.main / 'hello.txt').write_text('original\n', encoding='utf-8')
        self.run_git(self.main, 'add', 'hello.txt')
        self.run_git(self.main, 'commit', '-m', 'initial')
        self.run_git(self.main, 'remote', 'add', 'origin', str(self.bare))
        self.run_git(self.main, 'push', '-u', 'origin', 'main')
        self.run_git(base, 'clone', '--branch', 'main',
                     str(self.bare), str(self.other))
        self._identity(self.other)
        # Test-only local bare origin. Production requires canonical GitHub.
        trust = patch('practice.updater._trusted_origin', return_value=True)
        trust.start()
        self.addCleanup(trust.stop)

    def run_git(self, root, *args):
        r = subprocess.run(
            ['git', '-C', str(root), *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            encoding='utf-8', errors='replace', timeout=20)
        if r.returncode:
            self.fail('Git test setup failed: ' + r.stderr)
        return r.stdout.strip()

    def _identity(self, folder):
        self.run_git(folder, 'config', 'user.name', 'Local test')
        self.run_git(folder, 'config', 'user.email', 'local@test.invalid')

    def _push_change(self, text='new version\n'):
        (self.other / 'hello.txt').write_text(text, encoding='utf-8')
        self.run_git(self.other, 'add', 'hello.txt')
        self.run_git(self.other, 'commit', '-m', 'advance upstream')
        self.run_git(self.other, 'push', 'origin', 'main')

    def test_check_and_auto_install_fast_forward_only(self):
        self.assertEqual(check_for_updates(self.main).state, 'current')
        self._push_change()
        status = check_for_updates(self.main)
        self.assertEqual(status.state, 'available')
        self.assertEqual((self.main / 'hello.txt').read_text(), 'original\n')
        updated = install_update(self.main, status)
        self.assertEqual(updated, status.remote_sha)
        self.assertEqual((self.main / 'hello.txt').read_text(), 'new version\n')
        self.assertEqual(check_for_updates(self.main).state, 'current')

    def test_local_modified_tracked_file_blocks_update(self):
        self._push_change()
        (self.main / 'hello.txt').write_text('mine\n', encoding='utf-8')
        with self.assertRaisesRegex(UpdateError, 'local changes'):
            check_for_updates(self.main)
        self.assertEqual((self.main / 'hello.txt').read_text(), 'mine\n')

    def test_toolkit_development_branch_updates_only_itself(self):
        self.run_git(self.main, 'checkout', '-b', 'toolkit/experiment')
        self.run_git(self.main, 'push', '-u', 'origin', 'toolkit/experiment')
        self.run_git(self.other, 'fetch', 'origin', 'toolkit/experiment')
        self.run_git(self.other, 'checkout', '-b', 'toolkit/experiment',
                     'origin/toolkit/experiment')
        self._push_change('feature improvement\n')
        status = check_for_updates(self.main)
        self.assertEqual(status.state, 'available')
        self.assertEqual(status.branch, 'toolkit/experiment')
        install_update(self.main, status)
        self.assertEqual(self.run_git(self.main, 'branch', '--show-current'),
                         'toolkit/experiment')
        self.assertEqual((self.main / 'hello.txt').read_text(),
                         'feature improvement\n')

    def test_decomp_branch_is_not_switched_or_updated(self):
        self.run_git(self.main, 'checkout', '-b', 'chatgptweb/decomp')
        with self.assertRaisesRegex(UpdateError, 'other development branches'):
            check_for_updates(self.main)
        self.assertEqual(self.run_git(self.main, 'branch', '--show-current'),
                         'chatgptweb/decomp')

    def test_divergent_commits_are_never_reset(self):
        self._push_change()
        (self.main / 'hello.txt').write_text('local commit\n', encoding='utf-8')
        self.run_git(self.main, 'commit', '-am', 'local fork')
        local = self.run_git(self.main, 'rev-parse', 'HEAD')
        with self.assertRaisesRegex(UpdateError, 'ahead or diverged'):
            check_for_updates(self.main)
        self.assertEqual(self.run_git(self.main, 'rev-parse', 'HEAD'), local)

    def test_changed_upstream_requires_fresh_check(self):
        self._push_change('upstream one\n')
        status = check_for_updates(self.main)
        self._push_change('upstream two\n')
        with self.assertRaisesRegex(UpdateError, 'changed since the check'):
            install_update(self.main, status)
        self.assertEqual((self.main / 'hello.txt').read_text(), 'original\n')

    def test_untracked_file_is_preserved(self):
        self._push_change()
        notes = self.main / 'personal-notes.txt'
        notes.write_text('keep me\n', encoding='utf-8')
        checked = check_for_updates(self.main)
        install_update(self.main, checked)
        self.assertEqual(notes.read_text(), 'keep me\n')


class OriginValidationTests(unittest.TestCase):
    def test_canonical_https_ssh_origins_only(self):
        self.assertTrue(_trusted_origin(
            'https://github.com/Jake-Arnold/Goemon-64-Tools.git'))
        self.assertTrue(_trusted_origin(
            'git@github.com:Jake-Arnold/Goemon-64-Tools.git'))
        self.assertTrue(_trusted_origin(
            'ssh://git@github.com/Jake-Arnold/Goemon-64-Tools'))
        for url in (
            'https://github.com/someone-else/Goemon-64-Tools.git',
            'https://github.com/Jake-Arnold/Goemon-64-Tools-malware',
            'https://evil.test/Jake-Arnold/Goemon-64-Tools.git',
            'file:///tmp/test.git',
        ):
            self.assertFalse(_trusted_origin(url), url)


if __name__ == '__main__':
    unittest.main()

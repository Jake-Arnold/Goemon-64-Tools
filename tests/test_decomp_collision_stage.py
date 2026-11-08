"""Synthetic source staging tests; no game assets or original ROM bytes."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp.collision_stage import main, stage_collision_gate


class CollisionStageTests(unittest.TestCase):
    def test_stages_exact_bytes_without_overwriting_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            upstream, candidate, output = (root / name for name in ('original.c', 'candidate.c', 'staged.c'))
            upstream.write_bytes(b'original\n')
            candidate.write_bytes(b'candidate\n')
            with patch('decomp.collision_stage.prepare_collision_gate', return_value='staged\n') as prepare:
                self.assertEqual(main(['--upstream', str(upstream), '--candidate', str(candidate),
                                       '--output', str(output)]), 0)
                prepare.assert_called_once_with('original\n', 'candidate\n')
            self.assertEqual(output.read_bytes(), b'staged\n')
            self.assertEqual(upstream.read_bytes(), b'original\n')
            self.assertEqual(candidate.read_bytes(), b'candidate\n')
            with patch('decomp.collision_stage.prepare_collision_gate', return_value='changed\n'):
                with self.assertRaises(FileExistsError):
                    stage_collision_gate(upstream, candidate, output)
            self.assertEqual(output.read_bytes(), b'staged\n')

    def test_invalid_source_never_creates_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            upstream, candidate, output = (root / name for name in ('original.c', 'candidate.c', 'staged.c'))
            upstream.write_bytes(b'original\n')
            candidate.write_bytes(b'candidate\n')
            with patch('decomp.collision_stage.prepare_collision_gate', side_effect=ValueError('bad source')):
                with self.assertRaisesRegex(ValueError, 'bad source'):
                    stage_collision_gate(upstream, candidate, output)
            self.assertFalse(output.exists())
            with patch('decomp.collision_stage.prepare_collision_gate') as prepare:
                with self.assertRaisesRegex(ValueError, 'Output must differ'):
                    stage_collision_gate(upstream, candidate, upstream)
                with self.assertRaisesRegex(ValueError, 'Output must differ'):
                    stage_collision_gate(upstream, candidate, candidate)
                prepare.assert_not_called()
            upstream.write_bytes(b'\xff')
            with self.assertRaises(UnicodeDecodeError):
                stage_collision_gate(upstream, candidate, output)
            self.assertFalse(output.exists())

    def test_crlf_is_not_normalized(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            upstream, candidate, output = (root / name for name in ('original.c', 'candidate.c', 'staged.c'))
            upstream.write_bytes(b'line\r\n')
            candidate.write_bytes(b'candidate\n')
            with patch('decomp.collision_stage.prepare_collision_gate', side_effect=ValueError('LF-only source')) as prepare:
                with self.assertRaisesRegex(ValueError, 'LF-only'):
                    stage_collision_gate(upstream, candidate, output)
                prepare.assert_called_once_with('line\r\n', 'candidate\n')
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()

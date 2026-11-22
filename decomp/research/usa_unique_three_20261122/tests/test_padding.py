"""Fail-closed synthetic tests for Splat/asm-processor original non-FUNC NOP padding."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'verify_original_unit.py'
_spec = importlib.util.spec_from_file_location('verify_original_unit', MODULE)
_m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_m)


class AlignmentBoundaryTest(unittest.TestCase):
    def test_removes_exactly_two_unowned_nops(self):
        with TemporaryDirectory() as directory:
            p = Path(directory) / 'synthetic.s'
            p.write_text('glabel func_8000AFA8_BBA8\n'
                         'endlabel func_8000AFA8_BBA8\n'
                         '    /* BE98 8000B298 00000000 */  nop\n'
                         '    /* BE9C 8000B29C 00000000 */  nop\n')
            evidence = _m.remove_unowned_padding(p)
            self.assertEqual(evidence['trailing_padding_bytes'], 8)
            self.assertEqual(p.read_text().count('nop'), 0)
            self.assertTrue(p.read_text().endswith('endlabel func_8000AFA8_BBA8\n'))

    def test_rejects_non_nop_code_and_changes(self):
        with TemporaryDirectory() as directory:
            p = Path(directory) / 'synthetic.s'
            cases = [
                '    /* BE98 8000B298 00000000 */  nop\n',
                '    /* BE98 8000B298 00000000 */  nop\n'
                '    /* BE9C 8000B29C FFFFFE00 */  addiu $sp, $sp, -512\n',
                '    /* BE9C 8000B29C 00000000 */  nop\n'
                '    /* BE98 8000B298 00000000 */  nop\n',
                '    /* BE98 8000B298 00000000 */  nop\n'
                '    /* BE9C 8000B29C 00000000 */  nop\n'
                '    /* BEA0 8000B2A0 00000000 */  nop\n',
                '',
            ]
            for tail in cases:
                with self.subTest(tail=tail):
                    content = 'glabel func_8000AFA8_BBA8\nendlabel func_8000AFA8_BBA8\n' + tail
                    p.write_text(content)
                    with self.assertRaises(AssertionError):
                        _m.remove_unowned_padding(p)
                    self.assertEqual(p.read_text(), content)

    def test_rejects_duplicate_endlabels(self):
        with TemporaryDirectory() as directory:
            p = Path(directory) / 'synthetic.s'
            p.write_text('endlabel func_8000AFA8_BBA8\nendlabel func_8000AFA8_BBA8\n')
            with self.assertRaises(AssertionError):
                _m.remove_unowned_padding(p)


if __name__ == '__main__':
    unittest.main()

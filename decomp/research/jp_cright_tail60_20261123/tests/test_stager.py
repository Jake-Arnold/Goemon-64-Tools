import importlib.util
from pathlib import Path
import sys
import unittest

MODULE=Path(__file__).resolve().parents[1]/'verify_original.py'
S=importlib.util.spec_from_file_location('tailverify',MODULE)
M=importlib.util.module_from_spec(S)
S.loader.exec_module(M)

class TestStager(unittest.TestCase):
    def test_native_source_hash_pinned(self):M.check_source()
    def test_source_layout_has_callback_calls(self):
        s=M.SOURCE.read_text()
        self.assertIn('g_system_ptr = g_system;',s)
        self.assertLess(s.index('func_80004170_4D70();'),s.index('func_8000339C_3F9C();'))
    def test_unique_asm_splice(self):
        original='sha1: '+M.ROM_SHA+'\n'+('    - [0x100, c, a]\n'*189)+M.SPLAT_INSERT+'\n'
        candidate=M.render_candidate(original)
        self.assertEqual(candidate.count(M.SPLAT_REPLACEMENT),1)
        self.assertEqual(candidate.count('c, jp_cright_tail60'),1)
        self.assertEqual(candidate.count('asm, a'),189)
    def test_reject_nonunique_splice(self):
        raw='sha1: '+M.ROM_SHA+'\n'+('    - [0x100, c, a]\n'*189)+M.SPLAT_INSERT+'\n'+M.SPLAT_INSERT+'\n'
        with self.assertRaises(ValueError):M.render_candidate(raw)
    def test_reject_unpinned_splat(self):
        with self.assertRaises(ValueError):M.render_candidate(('    - [0x100, c, a]\n'*189)+M.SPLAT_INSERT)
    def test_reject_wrong_source(self):
        original=M.SRC_SHA
        try:
            M.SRC_SHA='00'*32
            with self.assertRaises(ValueError):M.check_source()
        finally:M.SRC_SHA=original

if __name__=='__main__':unittest.main()

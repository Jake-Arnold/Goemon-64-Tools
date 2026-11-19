"""ROM-free regression gates for the first Japanese exact C match."""
from __future__ import annotations
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from decomp import japan_first_c as j

class FirstJapaneseCTest(unittest.TestCase):
    def test_splat_segment_selection(self):
        self.assertEqual(j.render_config('x '+j.SEGMENT_OLD+' y'), 'x '+j.SEGMENT_NEW+' y')
        with self.assertRaisesRegex(ValueError,'exactly one'):
            j.render_config('absent')

    def test_source_installation_does_not_override_user_code(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            target=root/j.SOURCE_FILE
            target.parent.mkdir(parents=True)
            target.write_text('#include "common.h"\n\n#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_main_38620/func_80037A20_38620.s")\n')
            j.install_source(root)
            self.assertEqual(target.read_text(),j.SOURCE_LOCAL.read_text())
            j.install_source(root)
            target.write_text('void mine(void) {}\n')
            with self.assertRaises(FileExistsError):
                j.install_source(root)

    def test_verify_rejects_unexpected_c_object(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with mock.patch.object(j.baseline,'verify',return_value={}),\
                 mock.patch.object(j.subprocess,'run') as run:
                with self.assertRaises(FileNotFoundError):
                    j.verify(root,root/'retail')
                run.assert_not_called()

if __name__=='__main__':
    unittest.main()

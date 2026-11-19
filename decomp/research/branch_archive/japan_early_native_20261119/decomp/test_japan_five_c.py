"""ROM-free exact fifth-Japanese-C placement and source-integrity tests."""
from __future__ import annotations
from pathlib import Path
import tempfile
import unittest
from decomp import japan_five_c as m


class FifthJapaneseC(unittest.TestCase):
    def test_splat_original_boundary_and_region(self):
        base='\n'.join((m.BEFORE, '    - [0x16DF0, c, jp_bit_array]', '    - [0x38620, c, jp_main_38620]'))
        rendered=m.render_config(base)
        self.assertIn('    - [0x12D60, c, jp_motion_12D60]', rendered)
        self.assertIn('    - [0x12D80, asm, main_12D80]', rendered)
        with self.assertRaisesRegex(ValueError, 'already inserted'):
            m.render_config(rendered)
        with self.assertRaisesRegex(ValueError, 'existing|absent'):
            m.render_config(base.replace('jp_main_38620','other_source'))

    def test_safe_source_staging_and_refuse_modification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            target=root/m.SOURCE_FILE
            target.parent.mkdir(parents=True)
            target.write_text('#include "common.h"\n#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_motion_12D60/func_80012160_12D60.s")\n')
            m.install_source(root)
            self.assertEqual(target.read_bytes(), m.SOURCE_LOCAL.read_bytes())
            m.install_source(root)
            target.write_text('void changed(void) {}')
            with self.assertRaises(FileExistsError):
                m.install_source(root)

    def test_fixed_original_function_contract(self):
        self.assertEqual((m.ROM_OFFSET,m.VMA,m.SIZE),(0x12D60,0x80012160,32))
        self.assertTrue(m.SPLAT_CONFIG.name.endswith('.local.yaml'))


if __name__ == '__main__':unittest.main()

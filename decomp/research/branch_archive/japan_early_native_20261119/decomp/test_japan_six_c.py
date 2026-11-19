"""ROM-free tests for sixth Japanese region-C split and guarded source ownership."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp import japan_six_c as six


class SixthJapaneseCTest(unittest.TestCase):
    def setUp(self):
        self.base = ('    - [0x12D60, c, jp_motion_12D60]\n'
                     '    - [0x16DF0, c, jp_bit_array]\n'
                     '    - [0x38620, c, jp_main_38620]\n' + six.BEFORE + '\n')

    def test_insert_exact_original_boundaries_and_preserve_previous(self):
        actual = six.render_config(self.base)
        self.assertIn('[0x13B70, c, jp_camera_13B70]', actual)
        self.assertIn('[0x13B90, asm, main_13B90]', actual)
        self.assertIn('[0x12D60, c, jp_motion_12D60]', actual)
        self.assertIn('[0x38620, c, jp_main_38620]', actual)
        self.assertEqual(self.base.count('[0x13B70,'), 0)
        with self.assertRaisesRegex(ValueError, 'already been inserted'):
            six.render_config(actual)

    def test_unrecognised_base_cannot_stage(self):
        with self.assertRaisesRegex(ValueError, 'missing'):
            six.render_config(self.base.replace('jp_bit_array', 'unknown'))
        with self.assertRaisesRegex(ValueError, 'unique'):
            six.render_config(self.base.replace(six.BEFORE, ''))

    def test_source_staging_refuses_modified_contents(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout = Path(folder)
            dest = checkout / six.SOURCE_FILE
            dest.parent.mkdir(parents=True)
            dest.write_bytes(b'#include "common.h"\n#pragma GLOBAL_ASM("asm/japan_0/nonmatchings/jp_camera_13B70/func_80012F70_13B70.s")\n')
            six.install_source(checkout)
            self.assertEqual(dest.read_bytes(), six.SOURCE_LOCAL.read_bytes())
            six.install_source(checkout)
            dest.write_text('void user_override(void) {}')
            with self.assertRaises(FileExistsError):
                six.install_source(checkout)

    def test_stage_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout = Path(folder)
            path = checkout / six.SPLAT_CONFIG
            path.parent.mkdir(parents=True)
            path.write_text('changed')
            with patch.object(six.five, 'stage_config', return_value=checkout / 'five.yaml'):
                (checkout / 'five.yaml').write_text(self.base)
                with self.assertRaises(FileExistsError):
                    six.stage_config(checkout)

    def test_original_guest_addresses_and_size(self):
        self.assertEqual((six.ROM_OFFSET, six.VMA, six.SIZE), (0x13B70, 0x80012F70, 32))
        self.assertEqual(six.VMA - six.ROM_OFFSET, 0x7FFFF400)


if __name__ == '__main__':
    unittest.main()

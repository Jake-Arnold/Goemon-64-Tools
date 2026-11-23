"""ROM-free fail-closed Japanese C-Right source/identity contract checks."""
import hashlib
import unittest
from unittest import mock
from pathlib import Path
from decomp import japan_cright_promotion as cr

class JapanCRightContract(unittest.TestCase):
    def test_frozen_production_c(self):
        raw=cr.SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),cr.SRC_SHA)
        text=raw.decode()
        self.assertEqual(text.count('void func_80212514_5CDAA4('),1)
        self.assertIn('g_system_ptr+0x3B07A',text)
        self.assertIn('& 1',text)
        self.assertIn('& 8',text)
    def test_original_region_and_boundaries(self):
        self.assertEqual((cr.ROM_OFF,cr.VMA,cr.SIZE),(0x5CDAA4,0x80212514,396))
        self.assertEqual(cr.SIZE%4,0)
        self.assertEqual(cr.BASE_C+1,2370)
        self.assertEqual(cr.BASE_BYTES+cr.SIZE,127008)
    def test_no_relocation_waiver_allowed(self):
        path=Path(cr.__file__)
        s=path.read_text()
        self.assertIn('if removed or added or n0!=n1 or h0!=h1:',s)
        self.assertIn('raise ValueError(f\'FAILED_RELOC:',s)
    def test_clean_preflight_rejects_bad_rom(self):
        with self.assertRaises(FileNotFoundError):
            cr.original(Path('/this-path-does-not-exist'))

if __name__=='__main__':unittest.main()

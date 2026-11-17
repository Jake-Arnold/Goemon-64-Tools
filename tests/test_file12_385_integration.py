"""ROM-free guard tests for adjacent USA file12 original-ROM C reconstruction."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / 'decomp/research/file12_spatial/integrate_385.py'
spec = importlib.util.spec_from_file_location('file12_385', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ExpandedFile12Tests(unittest.TestCase):
    def test_original_spatial_code_ownership_is_complete(self):
        self.assertEqual(mod.WRAPPER_COUNT, 374)
        self.assertEqual(mod.WRAPPER_BYTES, 13464)
        self.assertEqual(len(mod.SPECS), 12)
        self.assertEqual(374+len(mod.SPECS)-1, 385)
        self.assertEqual(sum(row[3] for row in mod.SPECS), 14212)

    def test_source_extents_are_disjoint(self):
        self.assertTrue(all(a[2]+a[3]<=b[2] for a,b in zip(mod.SPECS,mod.SPECS[1:])))
        self.assertEqual(mod.SPECS[0][2],0x5C9310)
        self.assertEqual(mod.SPECS[-1][2]+mod.SPECS[-1][3],0x5D5D28)

    def test_missing_wrapper_count_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete 374-wrapper'):
            mod.generate_wrapper_source('')

    def test_pinned_source_hashes(self):
        self.assertEqual(len({row[1] for row in mod.SPECS}),len(mod.SPECS))
        self.assertTrue(all(len(row[4])==64 for row in mod.SPECS))
        self.assertEqual(mod.SPECS[0][4],'046af7d8140efca107fd45b79ea7a08cd8562ad857b9dcbde9323754a6aa639a')

    def test_new_sources_are_byte_pinned(self):
        for name,_,_,_,sha in mod.SPECS[1:]:
            path = mod.ROOT / (name+'.c')
            if not path.is_file():path=mod.ROOT/'adjacent'/(name+'.c')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)

    def test_bad_c_input_rejected_before_staging(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            for name,_,_,_,_ in mod.SPECS:
                (root/(name+'.c')).write_text('void fake(void){}')
            with self.assertRaisesRegex(ValueError,'Pinned C input'):
                mod.build_layout(root)


if __name__=='__main__':unittest.main()

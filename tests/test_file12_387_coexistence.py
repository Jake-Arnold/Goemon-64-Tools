"""ROM-free original-USA 385+2 file12 coexistence guardrail tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'decomp/research/file12_spatial/integrate_387.py'
spec = importlib.util.spec_from_file_location('file12_387_test', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TwoCanonicalFile12Callbacks(unittest.TestCase):
    def test_new_ranges_do_not_overlap(self):
        ranges = [(f[2], f[2] + f[3]) for f in mod.BASE_SPECS + mod.CANONICAL_STAGES]
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:])))
        self.assertEqual(374 + len(ranges) - 1, 387)
        self.assertEqual(sum(e-s for s,e in ranges), 14268)

    def test_two_sources_are_exact(self):
        src = Path(__file__).resolve().parents[1] / 'decomp/candidates'
        self.assertEqual(len(mod.validate_canonical_source_inputs(src)), 2)

    def test_wrong_c_source_hash_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                mod.validate_canonical_source_inputs(Path(t))

    def test_incorrect_canonical_proof_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'combined.json'
            p.write_text(json.dumps({'status':'matched','comparison':{'matched_functions':342}}))
            with self.assertRaisesRegex(ValueError, 'canonical 342-function'):
                mod.audit_canonical_comparison(p)

    def test_overlapping_canonical_proof_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'combined.json'
            funcs = [{'name':'canonical_'+str(i),'rom_offset':'0x249F0','size':4}
                     for i in range(342)]
            funcs[0].update(name='overlap', rom_offset='0x5C9310', size=36)
            p.write_text(json.dumps({'status':'matched','comparison':{'full_rom_match':True,
                'claimed_functions':342,'matched_functions':342,
                'matched_function_bytes':17568,'functions':funcs}}))
            with self.assertRaisesRegex(ValueError, 'overlaps'):
                mod.audit_canonical_comparison(p)

if __name__ == '__main__':
    unittest.main()

"""ROM-free fail-closed source/checkpoint tests for 145 Japanese G2 functions."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from decomp import japan_short145_promotion as promotion

class Short145Tests(unittest.TestCase):
    def test_145_source_hashes_and_unique_original_offsets(self):
        candidates=promotion.load_sources(promotion.DEFAULT_BUNDLES)
        self.assertEqual(len(candidates),145)
        self.assertEqual(len({row['name'] for row in candidates}),145)
        self.assertEqual(len({row['off'] for row in candidates}),145)
        self.assertEqual(sum(row['size'] for row in candidates),8952)
        self.assertTrue(all(row['size']%4==0 and row['size']>0 for row in candidates))
        self.assertEqual({r['batch'] for r in candidates},{'batch101','batch44'})
        self.assertFalse({r['name'] for r in candidates}&{'func_8003CC10_3D810','func_8003E2C4_3EEC4'})

    def test_source_mutation_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for key in promotion.BUNDLES:
                root=p/key;root.mkdir()
                source=promotion.DEFAULT_BUNDLES/key
                (root/'manifest.json').write_bytes((source/'manifest.json').read_bytes())
                (root/'sources').mkdir()
                for f in (source/'sources').glob('*.c'):
                    (root/'sources'/f.name).write_bytes(f.read_bytes())
            x=p/'batch101/sources/func_8001116C_11D6C.c'
            x.write_bytes(x.read_bytes()+b'\n/* deliberate integrity failure */\n')
            with self.assertRaisesRegex(ValueError,'Research source integrity failure'):
                promotion.load_sources(p)

    def test_wrong_rom_never_stages(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                promotion.original(Path(tmp))

    def test_all_original_offsets_have_consistent_labels(self):
        for r in promotion.load_sources(promotion.DEFAULT_BUNDLES):
            parts=r['name'].rsplit('_',1)
            if r['name'].startswith('func_'):
                self.assertEqual(int(parts[-1],16),r['off'])

if __name__=='__main__':unittest.main()

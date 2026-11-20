"""ROM-free research batch identity and canonical deduplication tests."""
from __future__ import annotations
import unittest
from decomp import japan_1686_promotion as p

class Japan1686BatchTests(unittest.TestCase):
    def test_complete_source_set(self):
        rows = p.candidates()
        self.assertEqual(len(rows), 1686)
        self.assertEqual(sum(int(r['size_bytes']) for r in rows), 101448)
        self.assertEqual(len(p.code_sources(rows)), 1663)

    def test_original_coordinate_and_interval_identity(self):
        rows=p.candidates()
        self.assertTrue(all(r['vma'] == int(r['function'].split('_')[1],16) for r in rows))
        self.assertTrue(all(r['off'] == int(r['function'].split('_')[2],16) for r in rows))
        spans=sorted((r['off'],r['end']) for r in rows)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])))

    def test_two_original_relocations_preserved(self):
        self.assertEqual(p.OMIT,{'func_08001228_6B3168','func_080012AC_6B51AC'})
        rows=p.candidates()
        self.assertTrue(p.OMIT.isdisjoint({r['function'] for r in rows}))

    def test_frozen_japanese_432_canon_disjoint(self):
        accepted={int(s,16) for s in (p.BATCH/'canonical_jp432_offsets.txt').read_text().split()}
        self.assertEqual(len(accepted),432)
        self.assertFalse(accepted & {r['off'] for r in p.candidates()})

if __name__=='__main__':unittest.main()

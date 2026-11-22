"""ROM-free guard tests for the USA Mini1 -> Cross48 additive promotion stages."""
import json
import unittest
from pathlib import Path
from decomp import mini_ebisumaru_1_g2_promotion as mini
from decomp import usa_crossregion48_g2_promotion as cross
from decomp import verify

class TestUSA49ResearchSourceGuards(unittest.TestCase):
    def test_miniebi_one_original_identity(self):
        f = mini.fixture()['functions']
        self.assertEqual(len(f),1)
        self.assertEqual(sum(e['size'] for e in f),224)
        self.assertEqual({e['name'] for e in f}, {e[0] for e in mini.EXPECTED})
        self.assertEqual(sum(sum(x['count'] for x in e['original_symbolic_relocations']) for e in f),12)

    def test_cross48_original_identities(self):
        f=cross.fixture()['functions']
        self.assertEqual(len(f),48)
        self.assertEqual(sum(e['size'] for e in f),3028)
        self.assertEqual(sum(len(e['original_symbolic_relocations']) for e in f),130)
        self.assertEqual(len({e['source'] for e in f}),48)

    def test_disjoint_new_original_address_ranges(self):
        entries=mini.fixture()['functions']+cross.fixture()['functions']
        for i,a in enumerate(entries):
            self.assertGreaterEqual(a['size'],8)
            self.assertEqual(a['size']%4,0)
            for b in entries[i+1:]:
                self.assertNotEqual(a['name'],b['name'])
                self.assertTrue(a['rom_offset']+a['size']<=b['rom_offset'] or b['rom_offset']+b['size']<=a['rom_offset'],(a['name'],b['name']))

    def test_only_prior_canonical_overlap_is_the_promoted_menu_helper(self):
        # This test checks overlap as it existed before this research was
        # canonically reconciled. The full current 2072-C accepted set is
        # guarded separately by promotion_integrity.
        manifest=verify.load_manifest(verify.ROOT/'manifest.json')
        manifest.pop('overlay_reconcile108_stage',None)
        manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
        existing={x['name'] for x in verify.claimed_functions(manifest)}
        names={x['name'] for x in mini.fixture()['functions']+cross.fixture()['functions']}
        self.assertEqual(names&existing,{'func_800108BC_114BC'})
        self.assertEqual(len(names-existing),48)

    def test_never_invent_acceptance_without_G2(self):
        self.assertEqual(mini.fixture()['status'],'PENDING_FULL_G2')
        self.assertEqual(cross.fixture()['status'],'PENDING_FULL_G2')

if __name__=='__main__':unittest.main()

"""ROM-free semantic metadata invariants; no new matching-C claims."""
import copy
import unittest

from decomp import semantic_inventory as si


class SemanticInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = si.build()
        cls.index = {(r['region'], r['name']): r for r in cls.rows}

    def test_canonical_coverage(self):
        self.assertEqual(len(self.index), len(self.rows))
        for region, stats in si.summary(self.rows).items():
            count, size, _ = si.batches.expected_totals(region, si.ROOT)
            self.assertEqual((stats['functions'], stats['bytes']), (count, size))
            self.assertEqual(sum(stats['confidence'].values()), count)
        for row in self.rows:
            self.assertIn(row['confidence'], si.LEVELS)
            self.assertTrue(row['identity_evidence'])
            if row['confidence'] != 'Unknown':
                self.assertTrue(row['evidence'] and row['behavior'])
            else:
                self.assertIsNone(row['semantic_alias'])

    def test_purpose_and_behavior_independent(self):
        for row in self.rows:
            self.assertEqual(row['behavior_confidence'], row['confidence'])
            self.assertIn(row['role_confidence'], si.LEVELS)
            if row['role_confidence'] == 'Unknown':
                self.assertEqual(row['role_scope'], 'unknown')
            else:
                self.assertTrue(row['role_evidence'])
                self.assertTrue(all((si.ROOT/p).is_file() for p in row['role_evidence']))
            if row['subsystem'] == 'empty_callback':
                self.assertEqual(row['role_confidence'], 'Unknown')
            if row['subsystem'] == 'resource_registration':
                self.assertEqual(row['role_scope'], 'resource_family')
            for lead in row['dependency_leads']:
                self.assertIn(lead['name'], row['callees'])
                self.assertEqual(self.index[row['region'],lead['name']]['semantic_alias'], lead['alias'])
        for region, stats in si.summary(self.rows).items():
            self.assertEqual(sum(stats['role_confidence'].values()), stats['functions'])
            self.assertEqual(sum(stats['role_scope'].values()), stats['functions'])

    def test_refined_examples(self):
        row = self.index['usa','func_80003728_4328']
        self.assertEqual(row['role_confidence'], 'Confirmed')
        self.assertEqual(row['counterpart']['name'], 'func_8000364C_424C')
        self.assertIn('3ADD4', row['behavior'])
        row = self.index['japan_0','func_08000174_711DE4']
        self.assertEqual(row['semantic_alias'], 'saved_flag0_dependent_actor_update')
        self.assertEqual(row['role_confidence'], 'High')
        self.assertIn('identity unknown', row['behavior'])

    def test_reciprocal_edges(self):
        for row in self.rows:
            key = row['region'], row['name']
            for field in ('counterpart', 'counterpart_candidate'):
                peer = row[field]
                if peer:
                    other = self.index[peer['region'], peer['name']]
                    back = other[field]
                    self.assertEqual((back['region'], back['name']), key)
                    if field == 'counterpart_candidate':
                        for k in ('size', 'owner', 'original_sha256'):
                            self.assertEqual(row[k], other[k])
            for name in row['callers']:
                self.assertIn(row['name'], self.index[row['region'], name]['callees'])

    def test_curated_examples(self):
        row = self.index['usa', 'func_801CBAF8_587A08']
        self.assertEqual(row['semantic_alias'], 'player_post_update')
        self.assertEqual(row['counterpart']['name'], 'func_801D1228_58D1F8')
        self.assertIn('0x8000', row['counterpart']['regional_difference'])
        row = self.index['japan_0', 'func_80023AB0_246B0']
        self.assertEqual(row['semantic_alias'], 'set_flag_bank_a')

    def test_unknown_is_not_promoted_by_complex_syntax(self):
        self.assertEqual(si.classify_body('if (x) { f(); }', 'usa')[0], 'Unknown')
        self.assertEqual(si.classify_body('return 3;', 'usa')[0], 'Medium')

    def test_reject_invalid_annotations(self):
        original = si.read(si.ROOT/'semantics/annotations.json')
        for change in ('stale', 'duplicate', 'field'):
            data = copy.deepcopy(original)
            rows = data['groups'][0]['functions']
            if change == 'stale':
                rows[0]['usa'] = 'not_a_canonical_function'
            elif change == 'duplicate':
                rows.append(copy.deepcopy(rows[0]))
            else:
                rows[0]['fields'] = ['nonexistent.+0x123']
            with self.assertRaises(ValueError):
                si.apply_annotations(copy.deepcopy(self.index), data, si.ROOT)


if __name__ == '__main__':
    unittest.main()

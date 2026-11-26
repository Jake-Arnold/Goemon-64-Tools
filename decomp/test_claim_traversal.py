"""A traversal memo is not a persisted manifest or source certification."""
import copy
import unittest
from unittest.mock import patch

from decomp import verify
from decomp import usa_script_vm440_promotion as vm440


class ClaimTraversalTests(unittest.TestCase):
    def test_identical_projection_once_per_invocation_and_isolated_results(self):
        calls = []

        def traverse(manifest):
            calls.append(copy.deepcopy(manifest))
            if manifest.get('root'):
                a = verify.claimed_functions({'leaf': [1]})
                a[0]['size'] = 99
                b = verify.claimed_functions({'leaf': [1]})
                return b + verify.claimed_functions({'leaf': [2]})
            return [{'name': 'test', 'size': manifest['leaf'][0]}]

        with patch.object(verify, '_claimed_functions', side_effect=traverse):
            for i in range(2):
                self.assertEqual(verify.claimed_functions({'root': True}),
                                 [{'name': 'test', 'size': 1},
                                  {'name': 'test', 'size': 2}])
                self.assertEqual(len(calls), (i + 1) * 3)
                self.assertIsNone(verify._CLAIM_TRAVERSAL.get())

    def test_different_types_and_changed_content_are_not_interchangeable(self):
        key = verify._claim_traversal_key
        self.assertNotEqual(key({'x': True}), key({'x': 1}))
        self.assertNotEqual(key({'x': [1]}), key({'x': [2]}))
        with self.assertRaises(TypeError):
            key({'x': (1,)})
        with self.assertRaises(TypeError):
            key({1: 'x'})

    def test_failed_traversal_is_never_retained(self):
        with patch.object(verify, '_claimed_functions',
                          side_effect=[ValueError('source drift'), []]) as fn:
            with self.assertRaisesRegex(ValueError, 'source drift'):
                verify.claimed_functions({'x': 1})
            self.assertIsNone(verify._CLAIM_TRAVERSAL.get())
            self.assertEqual(verify.claimed_functions({'x': 1}), [])
            self.assertEqual(fn.call_count, 2)

    def test_canonical_source_is_revalidated_after_a_successful_call(self):
        manifest = verify.load_manifest(verify.ROOT / 'manifest.json')
        claims = verify.claimed_functions(manifest)
        self.assertEqual((len(claims), sum(row['size'] for row in claims)),
                         (3056, 209088))
        with patch.object(vm440, 'SOURCE_SHA', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'VM440 C source drift'):
                verify.claimed_functions(manifest)
            with self.assertRaisesRegex(ValueError, 'VM440 C source drift'):
                verify.load_manifest(verify.ROOT / 'manifest.json')
        self.assertIsNone(verify._CLAIM_TRAVERSAL.get())
        self.assertEqual(verify.claimed_functions(manifest), claims)

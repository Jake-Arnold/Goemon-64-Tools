"""ROM-free guardrails for the all-at-once Japanese research promotion gate."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from decomp import japan_jp55_promotion as jp55


class JapanJP55PromotionTests(unittest.TestCase):
    def test_authenticated_research_manifest_and_sources(self):
        rows = jp55.load_sources(jp55.DEFAULT_BUNDLES)
        self.assertEqual(len(rows), 55)
        self.assertEqual(len(set(x['name'] for x in rows)), 55)
        self.assertEqual(len(set(x['off'] for x in rows)), 55)
        self.assertEqual(sum(x['size'] for x in rows), 3376)
        self.assertTrue(all(x['size'] % 4 == 0 for x in rows))
        self.assertTrue(all(x['source'].is_file() for x in rows))

    def test_prior_accepted_duplicate_is_excluded(self):
        manifest=json.loads((jp55.DEFAULT_BUNDLES/'manifest.json').read_text())
        excluded={x['name'] for x in manifest['excluded_historical_accepted']}
        self.assertEqual(excluded, {'func_801E818C_5A415C'})
        self.assertTrue(excluded.isdisjoint(x['name'] for x in jp55.load_sources(jp55.DEFAULT_BUNDLES)))

    def test_main_toolkit_readme_entry_points(self):
        repo = Path(__file__).resolve().parent.parent
        readme = (repo/'README.md').read_text()
        self.assertIn('git clone --branch stable/toolkit --single-branch', readme)
        self.assertIn('bash Run-Linux.sh', readme)
        self.assertIn('.\\Run.bat', readme)
        self.assertIn('--read-only', readme)

    def test_promotion_proof_never_uses_only_isolated_result(self):
        import inspect
        source=inspect.getsource(jp55.verify)
        self.assertIn('all_semantic_relocations', source)
        self.assertIn('7376', source)
        self.assertIn('80747', source)
        self.assertIn('original(co)', source)
        self.assertIn('classified', source)


if __name__=='__main__':
    unittest.main()

"""ROM-free tests preventing false claims in the historical research index."""
import json
import tempfile
import unittest
from pathlib import Path

from decomp.research.historical_audit_20261117 import audit
from decomp.research.historical_audit_20261117 import recheck_graphics

ROOT = Path(__file__).resolve().parents[1]


class HistoricalAuditTests(unittest.TestCase):
    def test_fresh_index_preserves_all_historical_evidence(self):
        with tempfile.TemporaryDirectory(prefix='goemon-audit-test-') as folder:
            output = Path(folder) / 'index.json'
            audit.main(ROOT, output)
            data = json.loads(output.read_text())
        self.assertEqual(len(data['task_catalog']), 100)
        self.assertGreaterEqual(len(data['execution_evidence']), 77)
        self.assertGreaterEqual(len(data['archived_research_reports']), 84)
        self.assertGreaterEqual(len(data['historic_branch_refs']), 45)
        self.assertEqual(data['reconciliation']['old_registry_now_accepted'], 87)
        self.assertGreaterEqual(data['canonical_production']['usa_matching_c'], 864)
        self.assertGreaterEqual(data['canonical_production']['japan_matching_c'], 39)

    def test_names_extracted_only_from_declared_target_fields(self):
        name='func_8003DE80_3EA80'
        self.assertEqual(audit.names_from({'name':name}),[name])
        self.assertEqual(audit.names_from({'body':name}),[])
        self.assertEqual(audit.names_from('arbitrary '+name),[])

    def test_no_private_rom_or_production_claim(self):
        leads=json.loads((ROOT/'decomp/research/historical_audit_20261117/LIVE_LEADS.json').read_text())
        self.assertTrue(leads['groups'])
        self.assertTrue(all(x['status'] in ('RESEARCH_ONLY','FAILED_NATIVE') for x in leads['groups']))
        self.assertNotIn('PASSED_G2', {x['status'] for x in leads['groups']})
        self.assertEqual(sum(x[4] for x in recheck_graphics.FUNCTIONS),284)
        self.assertEqual(len(recheck_graphics.FUNCTIONS),5)
        self.assertTrue(all(len(x)==40 for x in recheck_graphics.SOURCE_SHA1.values()))

    def test_source_blob_hash_function(self):
        path=ROOT/'decomp/research/historical_audit_20261117/audit.py'
        self.assertEqual(audit.blob_sha(path),__import__('subprocess').check_output(
            ['git','hash-object',str(path)],text=True).strip())


if __name__=='__main__':
    unittest.main()

"""Audit the consolidated read-only address metadata import."""
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / 'practice' / 'data'


class AddressCatalogueConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((DATA/'address_catalogue_audit.json').read_text())
        cls.catalogue = json.loads((DATA/'address_catalogue_v1.json').read_text())
        cls.discoveries = json.loads((DATA/'address_discoveries_v1.json').read_text())

    def test_exact_catalogue_size_and_audit(self):
        self.assertEqual(self.audit['total_records'],549)
        self.assertEqual(len(self.catalogue['entries']),549)
        self.assertEqual(len(self.discoveries['entries']),25)
        self.assertEqual(self.audit['live_readable']+self.audit['research_only'],549)

    def test_discovery_ids_unique_and_have_source_revision(self):
        ids=[row['id'] for row in self.discoveries['entries']]
        self.assertEqual(len(ids),len(set(ids)))
        for item in self.discoveries['entries']:
            if item['id'].startswith(('decomp:','research:')):
                self.assertRegex(item['source_revision'],r'^[0-9a-f]{40}$')


if __name__=='__main__':
    unittest.main()

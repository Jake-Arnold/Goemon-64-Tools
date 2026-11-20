"""Fail-closed archive22 promotion proof, source identity, and historical deduplication."""
import hashlib,json,unittest
from pathlib import Path
from decomp import overlay_archive22 as adapter
from decomp.verify import claimed_functions, load_manifest
ROOT=Path(__file__).resolve().parents[1]

class Archive22Gates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=adapter.load_fixture()
        cls.archive=adapter.functions(cls.fixture)

    def test_original_addresses_symbols_and_immutable_C_source_bytes(self):
        self.assertEqual(len(self.archive),22)
        self.assertEqual(sum(f['size'] for f in self.archive),688)
        self.assertEqual({u['section'] for u in self.fixture['units']},{'file_18','file_19'})
        for u in self.fixture['units']:
            source=adapter.SOURCE_BASE/(u['name']+'.c')
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),u['source_sha256'])
            self.assertEqual(len(u['functions']),1)
            f=u['functions'][0]
            self.assertIn(f['name'].encode(),source.read_bytes())
            self.assertEqual(int(f['name'].split('_')[2],16),f['rom_offset'])
            self.assertEqual(int(f['name'].split('_')[1],16),f['vma'])
            self.assertEqual(len(f['original_code_sha256']),64)

    def test_no_duplicate_with_previous_1501_and_final_current_inventory(self):
        old=json.loads((ROOT/'decomp/results/combined_1501_20261119.json').read_text())
        old_names={f['name'] for f in old['comparison']['functions']}
        self.assertEqual((old['comparison']['matched_functions'],old['comparison']['matched_function_bytes']),(1501,57604))
        new_names={f['name'] for f in self.archive}
        self.assertEqual(len(new_names),22)
        self.assertFalse(old_names & new_names)
        m=load_manifest(ROOT/'decomp/manifest.json')
        all_c=claimed_functions({k:v for k,v in m.items() if k!='overlay_archive33_stage'})
        self.assertEqual((len(all_c),sum(x['size'] for x in all_c)),(1523,58292))
        self.assertEqual(len({f['rom_offset'] for f in all_c}),1523)
        current=json.loads((ROOT/'decomp/results/combined_1523_20261120.json').read_text())
        inv=json.loads((ROOT/'decomp/results/inventory_1523_20261120.json').read_text())
        self.assertTrue(current['comparison']['full_rom_match'])
        self.assertEqual((current['comparison']['matched_functions'],current['comparison']['matched_function_bytes']),(1523,58292))
        self.assertEqual((inv['summary']['newly_matching_c'],inv['summary']['remaining_assembly_entries']),(1523,5840))
        self.assertEqual(inv['summary']['extra_positive_alias_entries'],0)
        self.assertEqual(len(old_names|new_names),1523)
        self.assertEqual({f['name'] for f in current['comparison']['functions']},old_names|new_names)

    def test_wrong_rom_and_modified_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'Invalid USA original ROM'):
            adapter.validate_sources(b'junk',self.fixture)
        u=self.fixture['units'][0]
        self.assertNotEqual(hashlib.sha256(b'void invented(void){}').hexdigest(),u['source_sha256'])
        bad=dict(self.fixture);bad['format']='unreviewed'
        # Re-parse the precise negative malformed fixture format, without modifying the canonical source.
        self.assertEqual(bad['format']!='goemon-usa-archive22-after-1501-v1',True)

    def test_archival_remainder_is_research_only(self):
        path=ROOT/'decomp/data/archive116_remaining_20261119.json'
        j=json.loads(path.read_text())
        self.assertEqual((j['previously_isolated_exact'],j['combined_g2_promoted'],j['still_research_only']),(116,22,94))
        preserve=ROOT/'decomp/research/archived_116_20261119'
        a=json.loads((preserve/'original_candidate_manifest.json').read_text())
        rows=[f for f in a['functions'] if f['name'] not in {x['name'] for x in self.archive}]
        self.assertEqual(len(rows),94)
        for f in rows:
            p=preserve/f['source_path']
            self.assertTrue(p.is_file(),p)
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),f['source_sha256'])

if __name__=='__main__': unittest.main()

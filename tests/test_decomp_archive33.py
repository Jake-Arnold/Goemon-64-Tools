"""Read-only, fail-closed second-wave 33 original native source acceptance checks."""
import hashlib,json,unittest
from pathlib import Path
from decomp import overlay_archive33 as archive33
from decomp.verify import claimed_functions,load_manifest
ROOT=Path(__file__).resolve().parents[1]

class Archive33Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=archive33.load_fixture()
        cls.functions=archive33.functions(cls.fixture)
        cls.previous=json.loads((ROOT/'decomp/results/combined_1523_20261120.json').read_text())
        cls.current=json.loads((ROOT/'decomp/results/combined_1556_20261120.json').read_text())
        cls.inventory=json.loads((ROOT/'decomp/results/inventory_1556_20261120.json').read_text())
        cls.proof=json.loads((ROOT/'decomp/results/usa_archive33_1556_promotion_20261120.json').read_text())

    def test_original_address_extent_zero_relocation_and_sha256_pinned(self):
        self.assertEqual((len(self.functions),sum(f['size'] for f in self.functions)),(33,1260))
        self.assertEqual(len(self.fixture['units']),33)
        self.assertEqual(self.fixture['archive_verified_native_relocations'],0)
        self.assertEqual(len({f['rom_offset'] for f in self.functions}),33)
        for u in self.fixture['units']:
            raw=(archive33.SOURCE_BASE/(u['name']+'.c')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),u['source_sha256'])
            self.assertEqual(len(u['functions']),1)
            f=u['functions'][0]
            self.assertIn(f['name'].encode(),raw)
            self.assertEqual(f['rom_offset'],int(f['name'].rsplit('_',1)[1],16))
            self.assertEqual(f['vma'],int(f['name'].split('_')[1],16))
            self.assertEqual(f['size']%4,0)

    def test_accepted_c_exact_and_disjoint_from_1523(self):
        older=self.previous['comparison']['functions']
        oldnames={f['name'] for f in older}
        newnames={f['name'] for f in self.functions}
        self.assertEqual((len(oldnames),self.previous['comparison']['matched_function_bytes']),(1523,58292))
        self.assertFalse(oldnames & newnames)
        self.assertEqual((self.current['comparison']['matched_functions'],self.current['comparison']['matched_function_bytes']),(1556,59552))
        self.assertTrue(self.current['comparison']['full_rom_match'])
        self.assertEqual(self.current['comparison']['candidate_sha1'],'6ea0ed71032ce08fc2745f412d84936382197494')
        self.assertEqual({f['name'] for f in self.current['comparison']['functions']},oldnames|newnames)
        m=load_manifest(ROOT/'decomp/manifest.json');accepted=claimed_functions({k:v for k,v in m.items() if k not in ('overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage','overlay_native49_stage','overlay_native51_stage','overlay_isolated233_stage')})
        self.assertEqual((len(accepted),sum(f['size'] for f in accepted)),(1556,59552))
        self.assertEqual(len({f['rom_offset'] for f in accepted}),1556)

    def test_original_elf_relocation_and_strict_inventory(self):
        proof=self.current['overlay_archive33_stage']
        self.assertEqual((proof['status'],proof['count'],proof['original_instruction_bytes']),('PASS',33,1260))
        self.assertEqual(proof['matched_ROM_bytes'],33554432)
        self.assertEqual(proof['identical_accepted_ELF_FUNC_identities'],7376)
        self.assertEqual(len(proof['identical_accepted_semantic_relocations']),70)
        inv=self.inventory['summary']
        self.assertEqual((inv['identified_function_entries'],inv['newly_matching_c'],inv['remaining_assembly_entries']),(7376,1556,5807))
        self.assertEqual(inv['extra_positive_alias_entries'],0)
        self.assertEqual(len(inv['size_annotation_differences']),2)

    def test_historical_stage_retained_and_research_only_count(self):
        self.assertEqual((self.proof['after_1523_accepted']['functions'],self.proof['after_1556_accepted']['functions']),(1523,1556))
        self.assertEqual(self.proof['remaining_archive_116_research_only'],61)
        ledger=json.loads((ROOT/'decomp/data/archive116_second33_stage_20261120.json').read_text())
        self.assertEqual((ledger['previously_isolated_exact'],ledger['combined_g2_promoted'],ledger['still_research_only']),(116,55,61))
        self.assertEqual(len(ledger['candidate33_names']),33)
        self.assertNotIn('alFilterNew',ledger['candidate33_names'])
        archive=json.loads((ROOT/'decomp/research/archived_116_20261119/original_candidate_manifest.json').read_text())
        self.assertEqual(len(archive['functions']),116)
        remaining={f['name'] for f in archive['functions']}-{f['name'] for f in self.current['comparison']['functions']}
        self.assertEqual(len(remaining),61)

    def test_negative_modified_source_and_wrong_rom_rejected(self):
        with self.assertRaisesRegex(ValueError,'Invalid USA original ROM'):
            archive33.validate_sources(b'wrong',self.fixture)
        u=self.fixture['units'][0]
        self.assertNotEqual(hashlib.sha256(b'void forged(void){}').hexdigest(),u['source_sha256'])
        self.assertNotEqual(self.fixture['format'],'goemon-usa-unreviewed-v1')

if __name__=='__main__':unittest.main()

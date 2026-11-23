#!/usr/bin/env python3
"""ROM-free negative/metadata ownership checks; never substitute for native IDO or original-ROM G2."""
import hashlib,json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class TestResearchManifest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=json.loads((ROOT/'manifest.json').read_text());cls.rows=cls.m['candidates']
    def test_pinned_base(self):
        self.assertEqual(self.m['stable_decomp_sha'],'838e9f87c3a860973e9d168b58fcf88bd456bfb4')
        self.assertEqual(self.m['published_c_baseline'],{'usa':2164,'japan_0':2398})
        self.assertEqual(self.m['new_accepted_c_claims'],0)
    def test_region_and_original_ownership(self):
        self.assertEqual(len(self.rows),101)
        self.assertEqual(sum(x['region']=='usa' for x in self.rows),47)
        self.assertEqual(sum(x['region']=='japan_0' for x in self.rows),54)
        self.assertEqual(len({(x['region'],x['name']) for x in self.rows}),101)
        self.assertEqual(len({(x['region'],x['rom_offset']) for x in self.rows}),101)
        for x in self.rows:
            self.assertTrue(0<x['original_bytes']<100 and x['original_bytes']%4==0,x['name'])
            self.assertTrue(re.fullmatch(r'[a-f0-9]{64}',x['code_sha256']))
            self.assertFalse('..' in Path(x['owner']).parts)
    def test_src_and_neg_hashes(self):
        for e in self.rows:
            for name,h in [('source','source_sha256'),('negative_source','negative_sha256')]:
                p=ROOT/e[name]
                self.assertTrue(p.is_file(),p)
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),e[h],p)
            original=(ROOT/e['source']).read_text();mut=(ROOT/e['negative_source']).read_text()
            self.assertNotEqual(original,mut)
            self.assertIn('volatile unsigned int __native_negative_control',mut)
    def test_no_canonical_proof(self):
        self.assertEqual(self.m['complete_original_rom_gate'],'NOT_RUN')
        self.assertEqual(self.m['full_local_ci_on_added_sources'],'NOT_RUN')
        self.assertEqual(self.m['unit_elf_reloc_inventory_gate'],'NOT_RUN')
        self.assertTrue(all(x['canonical_promotion']=='NOT_RUN' for x in self.rows))
    def test_tamper_negative(self):
        e=self.rows[0]
        invalid=(ROOT/e['source']).read_bytes()+b'\n/* modified */\n'
        self.assertNotEqual(hashlib.sha256(invalid).hexdigest(),e['source_sha256'])
    def test_parallel_research_overlap_exclusion(self):
        claimed={'__freeParam','__osGetActiveQueue','func_08000AAC_70AE1C','func_08001454_734ED4','func_8004054C_4114C','osGetThreadPri','osSyncPrintf'}
        self.assertFalse(claimed.intersection({x['name'] for x in self.rows}))
if __name__=='__main__':unittest.main()

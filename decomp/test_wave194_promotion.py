"""Fail closed on missing original reference, source or ownership proof."""
import copy, unittest
from unittest.mock import patch
from decomp import wave194_promotion as w, verify, promotion_integrity

class Wave194Tests(unittest.TestCase):
    def test_current_ownership(self):
        m=verify.load_manifest(w.ROOT/'manifest.json');c=verify.claimed_functions(m)
        self.assertEqual(c,w.predecessor(m)+w.claims())
        self.assertEqual((len(c),sum(f['size'] for f in c)),(2657,156672))
        self.assertEqual(promotion_integrity.audit()['status'],'PASS')
        self.assertEqual(w.validate_jp()['accepted_C'],2757)

    def test_negative_and_proof_identity(self):
        for r in w.REGIONS:
            p=w.read(w.proof_path(r));w.validate_native(r,p)
            for k,v in [('retail_exact',False),('expanded_rom_exact',False),('candidate_elf_sha256','0'*64),('semantic_relocations_after',0),('observed_new_ownership',0),('source_manifest_sha256','0'*64)]:
                with self.subTest(r=r,k=k),self.assertRaises(ValueError):
                    q=copy.deepcopy(p);q[k]=v;w.validate_native(r,q)
            for k in ['native_exact','negative_rejected']:
                q=copy.deepcopy(p);q['native'][0][k]=False
                with self.assertRaises(ValueError):w.validate_native(r,q)
            q=copy.deepcopy(p);q['strict_inventory']['upstream_unmarked_names'].pop()
            with self.assertRaises(ValueError):w.validate_native(r,q)

    def test_jp_reference_negative_controls(self):
        p=w.read(w.proof_path('japan_0'))
        for field in ['full_rom_exact','full_relocations_exact','function_identities_exact','stable_globals_exact','label_identity_exact']:
            for i in range(2):
                q=copy.deepcopy(p);q['independent_original_reference']['reference_links'][i][field]=False
                with self.assertRaises(ValueError):w.validate_native('japan_0',q)
        for field in ['native_relocation_records_unmodified','no_alias_link_negative_rejected']:
            q=copy.deepcopy(p);q['independent_original_reference'][field]=False
            with self.assertRaises(ValueError):w.validate_native('japan_0',q)
        q=copy.deepcopy(p);q['relocations_removed']=[]
        with self.assertRaises(ValueError):w.validate_native('japan_0',q)
        q=copy.deepcopy(p);q['preserved_original_labels'][0]['identity_exact']=False
        with self.assertRaises(ValueError):w.validate_native('japan_0',q)

    def test_predecessor_and_source_drift(self):
        m=verify.load_manifest(w.ROOT/'manifest.json');m[w.KEY]['format']='unreviewed'
        with self.assertRaises(ValueError):w.predecessor(m)
        with patch.dict(w.REGIONS['usa'],{'manifest':'0'*64}):
            with self.assertRaises(ValueError):w.rows('usa')
        m=w.read(w.ROOT/'regions/japan_0.json');m[w.JP_KEY]['asm_remaining']-=1
        with self.assertRaises(ValueError):w.master_predecessor(m)

    def test_inventory_tamper(self):
        m=w.read(w.ROOT/'manifest.json');p=w.read(w.ROOT/'results/combined.json');i=w.read(w.ROOT/'results/inventory.json');i['summary']['newly_matching_c']+=1
        self.assertEqual(w.audit_usa(w.ROOT,m,p,i)['status'],'FAIL')

    def test_historical_compiler_ledger_and_research_provenance(self):
        self.assertEqual(w.sha((w.ROOT/'COMPILER_QUIRKS.md').read_bytes()[:66321]),'3a6b131e31ec91c17163210e2e76c432ec7b1f58d0a39811a52c2da32576b84c')
        b=w.ROOT/w.BATCH;doc=w.read(b/'research-provenance.json');matches={(x['region'],x['name']):x for x in doc['matches']}
        self.assertEqual(len(matches),194)
        for region,expected in [('usa',580),('japan_0',522)]:
            rows=w.rows(region);self.assertEqual(sum(x['relocation_count'] for x in rows),expected)
            for f in rows:
                p=matches[region,f['name']]
                self.assertEqual((p['source_sha256'],p['negative']['source_sha256'],p['original_sha256'],p['native_relocations'],p['expected_relocations']),(f['source_sha256'],f['negative_sha256'],f['code_sha256'],f['relocation_count'],f['relocation_count']))
                self.assertEqual(p['replay_status'],'PASS')
        q=matches['usa','func_802121EC_5CD6BC'];self.assertEqual(w.sha((b/'line_grouping_control.c').read_bytes()),q['baseline']['source_sha256'])

"""Negative mutation tests: field-offset provenance never silences true losses."""
import unittest
from collections import Counter
from unittest.mock import patch
import hashlib
from decomp import japan_cright_relocation_provenance as p

class FailClosedCRightProvenance(unittest.TestCase):
    def setUp(self):
        self.base=Counter({('other',0x80001234,'R_MIPS_26',0x80002000,'actual_func'): 1})+p.EXPECTED_LOST
        self.cand=Counter({('other',0x80001234,'R_MIPS_26',0x80002000,'actual_func'): 1})
        self.auto='D_3B07A = 0x3B07A;\n'
        self.explicit=['D_80001234 = 0x80001234;\n']

    def test_expected_first_pair_exact(self):
        self.assertEqual(self.base-self.cand,p.EXPECTED_LOST)
        self.assertEqual(p._check_splat_provenance(self.auto,self.explicit),None)
        self.assertEqual(len(p.SITE_WORDS),6)
    def test_bad_provenance_missing(self):
        with self.assertRaisesRegex(ValueError,'generated'):
            p._check_splat_provenance('',self.explicit)
    def test_bad_provenance_wrong_value(self):
        with self.assertRaisesRegex(ValueError,'generated'):
            p._check_splat_provenance('D_3B07A = 0x3B07B;\n',self.explicit)
    def test_bad_provenance_duplicate(self):
        with self.assertRaisesRegex(ValueError,'generated'):
            p._check_splat_provenance(self.auto+self.auto,self.explicit)
    def test_bad_provenance_explicit(self):
        with self.assertRaisesRegex(ValueError,'explicitly authored'):
            p._check_splat_provenance(self.auto,self.explicit+['D_3B07A = 0x3B07A;'])
    def test_bad_provenance_no_explicit_map(self):
        with self.assertRaisesRegex(ValueError,'unavailable'):
            p._check_splat_provenance(self.auto,[])
    def test_missing_true_relocation_always_rejected(self):
        genuine=('other',0x80001234,'R_MIPS_26',0x80002000,'actual_func')
        self.assertNotEqual(self.base-(self.cand-Counter({genuine:1})),p.EXPECTED_LOST)
    def test_extra_relocation_always_rejected(self):
        extra=('other',0x80002348,'R_MIPS_HI16',0x80002000,'actual_data')
        self.assertNotEqual((self.cand+Counter({extra:1}))-self.base,Counter())
    def test_missing_half_pair_always_rejected(self):
        row=next(iter(p.EXPECTED_LOST))
        self.assertNotEqual(self.base-(self.cand+Counter({row:1})),p.EXPECTED_LOST)
    def test_wrong_symbol_always_rejected(self):
        a=next(iter(p.EXPECTED_LOST))
        fake=(a[0],a[1],a[2],a[3],'D_3B07B')
        changed=self.base-Counter({a:1})+Counter({fake:1})
        self.assertNotEqual(changed-self.cand,p.EXPECTED_LOST)
    def test_wrong_section_always_rejected(self):
        a=next(iter(p.EXPECTED_LOST))
        fake=('.rel.main',a[1],a[2],a[3],a[4])
        changed=self.base-Counter({a:1})+Counter({fake:1})
        self.assertNotEqual(changed-self.cand,p.EXPECTED_LOST)
    def _run_policy_on_synthetic_rom(self, *, baseline=None, candidate=None,
                                      candidate_rom=None, auto_symbols=None,
                                      explicit_symbols=None, old_hash=None,
                                      new_hash=None):
        """Exercise the *actual* validator with authenticated synthetic bytes."""
        zero=bytes(33554432)
        with patch.object(p,'ORIGINAL_SHA1',hashlib.sha1(zero).hexdigest()), \
             patch.object(p,'ORIGINAL_CODE_SHA256',hashlib.sha256(bytes(396)).hexdigest()), \
             patch.object(p,'SITE_WORDS',{site:0 for site in p.SITE_WORDS}):
            return p.reconcile_research(
                baseline if baseline is not None else self.full_base,
                candidate if candidate is not None else self.full_cand,
                original_rom=zero,candidate_rom=candidate_rom if candidate_rom is not None else zero,
                auto_symbols=auto_symbols if auto_symbols is not None else self.auto,
                explicit_symbols=explicit_symbols if explicit_symbols is not None else self.explicit,
                original_reloc_sha256=old_hash if old_hash is not None else p.BASELINE_RELOC_SHA256,
                candidate_reloc_sha256=new_hash if new_hash is not None else p.CANDIDATE_RELOC_SHA256,
            )
    @property
    def genuine(self):
        return ('other',0x80001234,'R_MIPS_26',0x80002000,'actual_func')
    @property
    def full_base(self):
        return Counter({self.genuine:80745})+p.EXPECTED_LOST
    @property
    def full_cand(self):
        return Counter({self.genuine:80745})
    def test_full_policy_accepts_only_expected_synthetic_delta(self):
        proof=self._run_policy_on_synthetic_rom()
        self.assertEqual(proof['status'],'RESEARCH_PROVENANCE_RECONCILED_NOT_G2')
        self.assertTrue(proof['all_other_relocation_records_preserved'])
        self.assertEqual(proof['promotion_status'],'BLOCKED_RELOCATION_POLICY_REVIEW')
    def test_full_policy_rejects_shifted_generated_relocation(self):
        row=next(iter(p.EXPECTED_LOST)); shifted=(row[0],row[1]+4,row[2],row[3],row[4])
        changed=self.full_base-Counter({row:1})+Counter({shifted:1})
        with self.assertRaisesRegex(ValueError,'unexpected loss/addition'):
            self._run_policy_on_synthetic_rom(baseline=changed)
    def test_full_policy_rejects_removed_genuine_with_compensating_extra(self):
        extra=('other',0x80001235,'R_MIPS_26',0x80002000,'actual_func')
        changed=self.full_cand-Counter({self.genuine:1})+Counter({extra:1})
        with self.assertRaisesRegex(ValueError,'unexpected loss/addition'):
            self._run_policy_on_synthetic_rom(candidate=changed)
    def test_full_policy_rejects_relocation_fingerprint_drift(self):
        with self.assertRaisesRegex(ValueError,'fingerprint drift'):
            self._run_policy_on_synthetic_rom(new_hash='deadbeef')
    def test_full_policy_rejects_rom_difference_even_with_same_relocations(self):
        different=bytes(33554431)+b'\x01'
        with self.assertRaisesRegex(ValueError,'candidate differs'):
            self._run_policy_on_synthetic_rom(candidate_rom=different)
    def test_full_policy_rejects_forged_explicit_symbol(self):
        with self.assertRaisesRegex(ValueError,'explicitly authored'):
            self._run_policy_on_synthetic_rom(explicit_symbols=['D_3B07A = 0x3B07A;'])

    def test_invalid_relocation_hash_rejected_early(self):
        # Calling the policy on wrong ROM must never treat mock data as native proof.
        with self.assertRaisesRegex(ValueError,'unauthenticated'):
            p.reconcile_research(self.base,self.cand,original_rom=b'',candidate_rom=b'',auto_symbols=self.auto,
                 explicit_symbols=self.explicit,original_reloc_sha256=p.BASELINE_RELOC_SHA256,
                 candidate_reloc_sha256=p.CANDIDATE_RELOC_SHA256)

if __name__=='__main__':unittest.main()

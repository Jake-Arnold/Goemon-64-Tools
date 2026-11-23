"""Fail-closed source syntax and relocation-triple rules; no native mock proof."""
from collections import Counter
import unittest
from unittest.mock import patch
from decomp import japan_cright_dual_reference as d

class DualOriginalReferenceTests(unittest.TestCase):
    def setUp(self):
        self.real=('other',0x80001234,'R_MIPS_26',0x80002000,'actual_func')
        self.original=Counter({self.real:80745})+d.SYNTHETIC_PAIR
        self.normalized=Counter({self.real:80745})
    def invoke(self, original=None,normalized=None,candidate=None,hash0=None,hash1=None,hash2=None,
               count0=80747,count1=80745,count2=80745):
        return d.check_relocation_triplet(
            original if original is not None else self.original,
            normalized if normalized is not None else self.normalized,
            candidate if candidate is not None else self.normalized,
            count0,count1,count2,
            hash0 if hash0 is not None else d.BASELINE_HASH,
            hash1 if hash1 is not None else d.NORMALIZED_HASH,
            hash2 if hash2 is not None else d.NORMALIZED_HASH)
    def test_exact_pair_only(self):
        p=self.invoke()
        self.assertEqual(p['compiled_c_relocation_count'],80745)
        self.assertTrue(p['real_relocations_exact_in_independent_reference'])
    def test_unexpected_genuine_loss(self):
        with self.assertRaisesRegex(ValueError,'FAILED_RELOC'):
            self.invoke(candidate=self.normalized-Counter({self.real:1}))
    def test_fake_compensating_genuine_relocation(self):
        fake=('other',0x80001238,'R_MIPS_26',0x80002000,'actual_func')
        with self.assertRaisesRegex(ValueError,'FAILED_RELOC'):
            self.invoke(candidate=self.normalized-Counter({self.real:1})+Counter({fake:1}))
    def test_missing_first_asm_reference(self):
        k=next(iter(d.SYNTHETIC_PAIR))
        with self.assertRaisesRegex(ValueError,'FAILED_RELOC'):
            self.invoke(original=self.original-Counter({k:1}))
    def test_unexpected_asm_reference(self):
        fake=('.rel.file_12',0x80212554,'R_MIPS_HI16',0x3B07A,'D_3B07A')
        with self.assertRaisesRegex(ValueError,'FAILED_RELOC'):
            self.invoke(original=self.original+Counter({fake:1}))
    def test_source_name_wrong(self):
        with self.assertRaises(ValueError):
            d.normalize_original_asm('not the real ASM')
    def test_source_single_pair_wrong(self):
        src=''.join((d.BEFORE+'\n') for _ in range(2))+d.BEFORE_LO
        with self.assertRaises(ValueError):
            d.normalize_original_asm(src)
    def test_total_wrong(self):
        with self.assertRaisesRegex(ValueError,'counts'):
            self.invoke(count2=80747)
    def test_fingerprint_wrong(self):
        with self.assertRaisesRegex(ValueError,'fingerprints'):
            self.invoke(hash2='0'*64)
    def test_input_type_wrong(self):
        with self.assertRaises(TypeError):
            self.invoke(candidate={self.real:80745})
    def test_second_reloc_must_survive(self):
        fake=('.rel.file_12',0x80212660,'R_MIPS_HI16',0x3B07A,'D_3B07A')
        changed=self.normalized-Counter({self.real:1})+Counter({fake:1})
        with self.assertRaisesRegex(ValueError,'FAILED_RELOC'):
            self.invoke(candidate=changed)

if __name__=='__main__': unittest.main()

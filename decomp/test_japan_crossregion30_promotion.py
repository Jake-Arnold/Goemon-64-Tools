"""Negative and positive ROM-free source provenance and original-reference integrity tests."""
import unittest,json,hashlib
from pathlib import Path
from decomp import japan_crossregion30_promotion as jp
from decomp import japan_crossregion30_integrity as integrity

class CrossRegion30ProofTests(unittest.TestCase):
    def test_all_30_nonoverlapping(self):
        rows=jp.rows();self.assertEqual(len(rows),30)
        self.assertEqual(sum(f['size'] for f in rows),1280)
        extents=sorted((r['rom_offset'],r['rom_offset']+r['size']) for r in rows)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(extents,extents[1:])))

    def test_three_original_asm_unpromoted(self):
        self.assertEqual(jp.RETAIN_ASM_ABS_RELOCS,{'osAiGetLength','__osSpGetStatus','__osSpSetStatus'})
        self.assertFalse({r['name'] for r in jp.rows()} & jp.RETAIN_ASM_ABS_RELOCS)

    def test_native_compiler_source_integrity(self):
        self.assertEqual(len(jp.CANONICAL_VARIANTS),7)
        for name,digest in jp.CANONICAL_VARIANTS.items():
            p=jp.PACKAGE/'canonical_variants'/f'{name}.c'
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),digest)

    def test_frozen_native_source_bundle(self):
        self.assertEqual(hashlib.sha256(jp.MANIFEST.read_bytes()).hexdigest(),jp.MANIFEST_SHA)
        rows=jp.rows();self.assertEqual(len(rows),30)

    def test_full_reference_relocations_source_provenance(self):
        self.assertEqual(jp.BASE_RELOCS,80745)
        self.assertEqual(jp.BASE_RELOC_HASH,'43a133b21ac2b18d8e1d00f8c4e5718776b001a1f45c54e807dae12165e797c0')

    def test_original_C_not_double_counted(self):
        old=json.loads((integrity.ROOT/'regions/japan_0_short28_2398.json').read_text())
        oldnames={f['name'] for f in old['functions']}
        self.assertFalse(oldnames & {r['name'] for r in jp.rows()})

    def test_native_variant_negative_controls(self):
        data=json.loads((jp.PACKAGE/'canonical_variants/native_negative_evidence.json').read_text())
        self.assertEqual(len(data['negative_controls']),4)
        for neg in data['negative_controls']:
            self.assertEqual(neg['original_IDO_native_negative'],'PASS_DIFFERENT_CODE')
            self.assertNotEqual(neg['canonical_positive_sha256'],neg['negative_sha256'])

    def test_complete_stored_regional_integrity(self):
        self.assertEqual(integrity.validate()['accepted_C'],2428)

if __name__=='__main__':unittest.main()

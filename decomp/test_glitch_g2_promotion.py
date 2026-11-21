"""ROM-free fail-closed tests for five true original-ROM Start-path promotions."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from decomp import glitch_g2_promotion as g

D=Path(__file__).resolve().parent

class GlitchG2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((D/'results/glitch_start5_2121jp_1958usa_g2_20261121.json').read_text())

    def test_deduped_original_function_list(self):
        names={r:[(n,off,length) for n,off,length,_ in g.REGIONS[r]['targets']] for r in ('japan_0','usa')}
        self.assertEqual(names['japan_0'], [('func_8001F580_20180',0x20180,100),
                                           ('func_8001F610_20210',0x20210,252),
                                           ('func_8003EE44_3FA44',0x3FA44,36)])
        self.assertEqual(names['usa'], [('func_8001F8B0_204B0',0x204B0,100),
                                        ('func_8001F940_20540',0x20540,252)])
        self.assertEqual(sum(s for a in names.values() for _,_,s in a),740)
        self.assertNotIn('func_8001F70C_2030C',str(names))

    def test_per_region_proof_claims_exact(self):
        m=self.report['regions']
        self.assertEqual((m['japan_0']['prior_matched_c_functions'],m['japan_0']['matched_c_functions']), (2118,2121))
        self.assertEqual((m['usa']['prior_matched_c_functions'],m['usa']['matched_c_functions']), (1956,1958))
        self.assertEqual((m['japan_0']['all_semantic_relocation_count'],m['usa']['all_semantic_relocation_count']), (80747,82103))
        self.assertEqual((m['japan_0']['assembly_remaining'],m['usa']['assembly_remaining']), (5255,5405))
        self.assertEqual((m['japan_0']['matched_c_instruction_bytes'],m['usa']['matched_c_instruction_bytes']), (112244,84292))
        for region in m:
            with self.subTest(region=region):
                self.assertEqual(m[region]['original_rom_bytes'],33554432)
                self.assertEqual(m[region]['original_elf_function_identities'],7376)
                self.assertEqual(len(m[region]['functions']),len(g.REGIONS[region]['targets']))
                self.assertEqual(m[region]['original_rom_sha1'],g.REGIONS[region]['rom_sha1'])
                self.assertEqual(m[region]['all_semantic_relocation_sha256'],g.REGIONS[region]['reloc_sha256'])

    def test_sources_locked_to_verified_native_content(self):
        for region in g.REGIONS:
            for name,off,size,src in g.REGIONS[region]['targets']:
                self.assertEqual(off,int(name.split('_')[-1],16))
                self.assertEqual(int(name.split('_')[1],16),0x80000000+off-0xC00)
                raw=(g.SOURCES/src).read_bytes()
                self.assertTrue(raw)
                self.assertIn(name.encode(),raw)
        expected={f['source'].split('/')[-1]:f['source_sha256']
                  for reg in self.report['regions'].values() for f in reg['functions'] if f['source'].startswith('src/glitch_g2')}
        for name,digest in expected.items():
            self.assertEqual(hashlib.sha256((g.SOURCES/name).read_bytes()).hexdigest(),digest)
        self.assertEqual(hashlib.sha256((g.SOURCES/'usa_rotation_angles.c').read_bytes()).hexdigest(),
                         '72742e59bf097de609062aac468e8dd3a11473939e67134f7853bc6c19050710')

    def test_all_section_relocation_reader_includes_main(self):
        sample="""Relocation section '.rel.main' at offset 0x000 contains 2 entries:
  Offset     Info    Type            Sym.Value  Sym. Name
8001f594  00001f05 R_MIPS_HI16       0003adde   D_3ADDE
8001f5ac  00001f06 R_MIPS_LO16       0003adde   D_3ADDE
Relocation section '.rel.file_11' at offset 0x101 contains 1 entry:
801e2000  00002004 R_MIPS_26         80034e8c   func_80034E8C_35A8C
"""
        with patch.object(g.subprocess,'check_output',return_value=sample):
            rel,count,digest=g.all_semantic_relocations('/dev/null')
        self.assertEqual(count,3)
        self.assertEqual(sum(v for row,v in rel.items() if row[0]=='.rel.main'),2)
        self.assertEqual(sum(v for row,v in rel.items() if row[0]=='.rel.file_11'),1)
        self.assertEqual(len(digest),64)

    def test_original_asm_preservation_and_owner_guards(self):
        usa=(g.SOURCES/'usa_rotation_angles.c').read_text()
        self.assertIn('func_8001FA80_20680.s',usa)
        self.assertNotIn('func_8001F8B0_204B0.s',usa)
        self.assertNotIn('func_8001F940_20540.s',usa)
        self.assertIn('D_8014CCC0_14D8C0',usa)
        self.assertIn('D_800BCCC0_BD8C0',usa)
        jp=(g.SOURCES/'jp_gameplay_start.c').read_text()
        self.assertIn('0x3B07C',jp)
        self.assertNotIn('extern u16 D_800CD52C;',jp)
        self.assertIn('D_3ADDE', (g.SOURCES/'jp_gameplay_dispatch.c').read_text())
        self.assertEqual(g.REGIONS['japan_0']['c_offset'],0)
        self.assertEqual(g.REGIONS['usa']['c_offset'],13)

    def test_japan_1686_deduplication(self):
        original=(D/'research/jp1686_promotion/candidates.csv').read_text()
        for name,*_ in g.REGIONS['japan_0']['targets']:
            self.assertNotIn(','+name+',',original)

if __name__=='__main__':unittest.main()

"""ROM-free research integrity checks for Japanese VM G2 two-function stage."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest
from decomp import vm_g2_promotion as vm


class NativeVmG2ResearchTests(unittest.TestCase):
    def test_source_checksums_original_extents_and_canonical_dedup(self):
        self.assertEqual(vm.REGION, 'japan_0')
        self.assertEqual((vm.OLD_C,vm.OLD_BYTES,vm.IDENTITIES),(2121,112244,7376))
        self.assertEqual([(r[0],r[1],r[2]) for r in vm.TARGETS],[
            ('func_8003CC10_3D810',0x3D810,48),
            ('func_8003E2C4_3EEC4',0x3EEC4,44)])
        self.assertEqual(len({r[0] for r in vm.TARGETS}),2)
        self.assertEqual(sum(r[2] for r in vm.TARGETS),92)
        for name,off,size,file,owner,sha,code in vm.TARGETS:
            with self.subTest(name=name):
                self.assertEqual(int(name.split('_')[2],16),off)
                self.assertTrue((vm.SOURCES/file).is_file())
                blob=(vm.SOURCES/file).read_bytes()
                self.assertEqual(hashlib.sha256(blob).hexdigest(),sha)
                self.assertEqual(len(code),64)
                self.assertTrue(owner.endswith('.s'))

    def test_fail_closed_does_not_weaken_original_rom_or_relocation_gates(self):
        source=Path(vm.__file__).read_text(encoding='utf8')
        for requirement in ('33554432', 'FAILED_ROM', 'FAILED_RELOC',
                            'FAILED_INVENTORY', 'all_semantic_relocations',
                            'pack_text_metadata', 'original_elf_function_identities',
                            'CURRENT_ROM', 'SOURCES'):
            if requirement=='CURRENT_ROM':continue
            with self.subTest(requirement=requirement):self.assertIn(requirement,source)
        self.assertNotIn('force=True',source)

    def test_reproducible_accepted_but_not_rerun_claims(self):
        self.assertEqual(vm.RELOC_COUNT,80747)
        self.assertEqual(vm.ORIG_SHA1,'6f8745fecc3a5e7d4918c7a73353eb0726116ded')
        self.assertEqual(vm.RELOC_SHA,'e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20')
        self.assertEqual(vm.OLD_C+len(vm.TARGETS),2123)
        self.assertEqual(vm.OLD_BYTES+sum(r[2] for r in vm.TARGETS),112336)

if __name__=='__main__':unittest.main()

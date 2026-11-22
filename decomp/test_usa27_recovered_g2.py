"""Fail-closed provenance guards for independently recovered 27 USA C functions.

This ROM-free guard does not replace native compiler, full-ROM and ELF G2.
"""
from __future__ import annotations
import unittest
from pathlib import Path
from decomp import usa_crossregion51_recovered27_g2_promotion as recovery
from decomp import overlay_isolated233 as isolation

class Recovery27Guards(unittest.TestCase):
    def test_identity_source_hash_and_27_relocations(self):
        m=recovery.fixture()
        self.assertEqual(len(m['functions']),27)
        self.assertEqual(sum(x['size'] for x in m['functions']),1904)
        self.assertEqual(sum(len(x['original_symbolic_relocations']) for x in m['functions']),77)
        self.assertEqual(len({x['rom_offset'] for x in m['functions']}),27)

    def test_live_original_names_and_rom_offsets(self):
        m=recovery.fixture()
        for f in m['functions']:
            self.assertEqual(f['name'].split('_')[-1].upper(),format(f['rom_offset'],'X'))
            self.assertTrue((recovery.DIR/'sources'/(f['source']+'.c')).is_file())

    def test_embedded_ownership_exact(self):
        m=recovery.fixture()
        embedded=[x for x in m['functions'] if x['name'] in recovery.EMBEDDED_27]
        self.assertEqual(len(embedded),10)
        self.assertEqual(sum(x['size'] for x in embedded),580)

    def test_no_global_adapter_mutation(self):
        self.assertFalse(recovery.EMBEDDED_27.intersection(isolation.EMBEDDED))
        fn=isolation.embed_original
        with recovery.scoped_embedded():
            self.assertEqual(len(recovery.EMBEDDED_27.intersection(isolation.EMBEDDED)),10)
            self.assertIs(isolation.embed_original,recovery.embed_recovered_dialogue)
        self.assertFalse(recovery.EMBEDDED_27.intersection(isolation.EMBEDDED))
        self.assertIs(isolation.embed_original,fn)

if __name__=='__main__':unittest.main()

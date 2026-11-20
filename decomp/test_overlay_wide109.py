"""ROM-free regression gates for USA wide109's 106 unique production functions.

Historical PR #74 carried 109 researched C functions; three were already
accepted at canonical 1119 and must never be re-promoted.
"""
import hashlib
import json
from pathlib import Path
import unittest
from decomp import overlay_wide109 as wide
from decomp.verify import claimed_functions,load_manifest,wide109_stage


class Wide109PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=wide.load_fixture()
        cls.manifest=load_manifest(Path(__file__).with_name('manifest.json'))

    def test_exact_source_pins(self):
        u=self.fixture['units']
        self.assertEqual(len(u),68)
        for entry in u:
            with self.subTest(unit=entry['name']):
                path=wide.SOURCE_BASE/(entry['name']+'.c')
                self.assertTrue(path.is_file())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),entry['source_sha256'])
                self.assertEqual(sum(f['size'] for f in entry['functions']),entry['size'])

    def test_unique_original_addresses_and_unit_grouping(self):
        fs=wide.functions(self.fixture)
        self.assertEqual(len(fs),106)
        self.assertEqual(sum(x['size'] for x in fs),1200)
        self.assertEqual(len({f['name'] for f in fs}),106)
        self.assertEqual(len({f['rom_offset'] for f in fs}),106)
        self.assertEqual({u['section'] for u in self.fixture['units']},wide.SECTIONS)
        for unit in self.fixture['units']:
            cursor=unit['rom_offset']
            for f in unit['functions']:
                self.assertEqual(f['rom_offset'],cursor)
                self.assertEqual(int(f['name'].split('_')[1],16),f['vma'])
                self.assertEqual(int(f['name'].split('_')[2],16),f['rom_offset'])
                cursor+=f['size']
            self.assertEqual(cursor-unit['rom_offset'],unit['size'])

    def test_no_duplicate_promotion_and_complete_accepted_inventory(self):
        # Historical 1225-C checkpoint; later original-address stages are excluded.
        production=claimed_functions({k:v for k,v in self.manifest.items() if k not in ('overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage' )})
        self.assertEqual((len(production),sum(x['size'] for x in production)),(1225,52028))
        self.assertEqual(len({f['name'] for f in production}),1225)
        spans=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in production)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])))
        previous=claimed_functions({k:v for k,v in self.manifest.items() if k not in ('overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage')})
        self.assertEqual((len(previous),sum(x['size'] for x in previous)),(1119,50828))
        prev_names={f['name'] for f in previous}
        self.assertFalse(prev_names&{f['name'] for f in wide.functions(self.fixture)})
        self.assertEqual({f['name'] for f in previous if f['rom_offset'] in (0x5d42c8,0x5d57d8,0x5d59ac)},
                         {'func_80218DF8_5D42C8','func_8021A308_5D57D8','func_8021A4DC_5D59AC'})

    def test_stage_contract_rejects_unknown_format(self):
        with self.assertRaisesRegex(ValueError,'Unreviewed wide109'):
            wide109_stage({'overlay_wide109_stage':{'format':'experimental'}})

    def test_1119_original_proofs_retained(self):
        root=Path(__file__).parent/'results'
        combined=json.loads((root/'combined_1119_before_wide109_20261118.json').read_text())
        inv=json.loads((root/'inventory_1119_before_wide109_20261118.json').read_text())
        self.assertEqual(combined['comparison']['matched_functions'],1119)
        self.assertEqual(combined['comparison']['matched_function_bytes'],50828)
        self.assertTrue(combined['comparison']['full_rom_match'])
        self.assertEqual(inv['summary']['remaining_assembly_entries'],6244)

if __name__=='__main__':unittest.main()

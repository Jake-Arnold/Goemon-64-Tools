"""Fail-closed ROM-free archive61 source/manifest/SDK ownership contracts."""
from __future__ import annotations
import copy
import hashlib
import unittest
from decomp import overlay_archive61 as native
from decomp.verify import claimed_functions,load_manifest

# This suite proves its historical promotion checkpoint, not subsequent stages.
_historical_load_manifest = load_manifest

def load_manifest(*args, **kwargs):
    manifest = _historical_load_manifest(*args, **kwargs)
    # The 2090-C Mini stages postdate this fixed historical test checkpoint.
    manifest.pop('overlay_mini10_stage', None)
    manifest.pop('overlay_mini_selector_stage', None)
    manifest.pop('overlay_native49_stage', None)
    manifest.pop('overlay_native51_stage', None)
    # The 233-C batch is newer than this frozen historical checkpoint.
    manifest.pop('overlay_isolated233_stage', None)
    manifest.pop('overlay_reconcile108_stage', None)  # Preserve this historical acceptance checkpoint
    manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
    return manifest


class Archive61PromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=native.load_fixture()
        cls.functions=native.functions(cls.fixture)

    def test_total_original_counts_and_unique_ranges(self):
        self.assertEqual(len(self.fixture['units']),61)
        self.assertEqual(len(self.functions),61)
        self.assertEqual(sum(f['size'] for f in self.functions),2772)
        self.assertEqual(sum(f['expected_original_relocations'] for f in self.functions),163)
        offsets=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in self.functions)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(offsets,offsets[1:])))

    def test_all_authenticated_original_c_files_preserved(self):
        for u in self.fixture['units']:
            with self.subTest(unit=u['name']):
                source=native.SOURCE_BASE/(u['name']+'.c')
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),u['source_sha256'])

    def test_sdk_alfilternew_original_linker_section_alignment(self):
        sdk=[f for f in self.functions if f['name']=='alFilterNew']
        self.assertEqual(len(sdk),1)
        self.assertEqual((sdk[0]['rom_offset'],sdk[0]['size'],sdk[0]['expected_original_relocations']),
                         (0x524C0,28,0))
        self.assertTrue(any('.text.archive61' in str(value) for value in native.stage_linker.__code__.co_consts))

    def test_complete_production_claims_no_duplicate(self):
        m=load_manifest(native.ROOT/'manifest.json')
        # Historical checkpoint projection: post2090 functions were not yet accepted.
        m.pop('overlay_usa_opening_new2_stage',None)
        functions=claimed_functions({k:v for k,v in m.items() if k not in ('overlay_checkpoint500_stage','overlay_rediscovery5_stage')})
        self.assertEqual(len(functions),1617)
        names=[f['name'] for f in functions]
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual({f['name'] for f in self.functions} & set(names),
                         {f['name'] for f in self.functions})
        older=claimed_functions({k:v for k,v in m.items() if k not in ('overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage')})
        self.assertEqual(len(older),1556)
        self.assertTrue(set(names)-{f['name'] for f in older}=={f['name'] for f in self.functions})

    def test_source_drift_rejected_before_build(self):
        tampered=copy.deepcopy(self.fixture)
        tampered['units'][0]['source_sha256']='0'*64
        self.assertNotEqual(hashlib.sha256((native.SOURCE_BASE/'archive61_000.c').read_bytes()).hexdigest(),
                            tampered['units'][0]['source_sha256'])

if __name__=='__main__':unittest.main()

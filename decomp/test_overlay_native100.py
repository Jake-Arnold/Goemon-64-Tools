"""USA 100 source-backed C promotion: current and historical manifest guards."""
from __future__ import annotations

import hashlib
from pathlib import Path
import unittest
from decomp.verify import load_manifest, claimed_functions
from decomp import overlay_native49 as stage49, overlay_native51 as stage51

ROOT=Path(__file__).resolve().parent

class Native100ExactC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=load_manifest(ROOT/'manifest.json')
        # Historical checkpoint projection: post2090 functions were not yet accepted.
        cls.manifest.pop('overlay_usa_opening_new2_stage',None)
        cls.manifest.pop('overlay_usa_short72_stage',None)
        cls.manifest.pop('overlay_mini_selector_stage',None)  # Later canonical USA2090
        cls.manifest.pop('overlay_mini10_stage',None)  # Later canonical USA2089
        cls.manifest.pop('overlay_reconcile108_stage', None)  # Historical native100 stage
        cls.manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
        # Retain the frozen 1623 -> 1723 proof projection.
        cls.manifest.pop('overlay_isolated233_stage',None)
        cls.a=stage49.load_fixture()
        cls.b=stage51.load_fixture()

    def test_pinned_prior_and_current_function_counts(self):
        base=claimed_functions({k:v for k,v in self.manifest.items() if k not in ('overlay_native49_stage','overlay_native51_stage')})
        midway=claimed_functions({k:v for k,v in self.manifest.items() if k!='overlay_native51_stage'})
        full=claimed_functions(self.manifest)
        self.assertEqual((len(base),sum(f['size'] for f in base)),(1623,62504))
        self.assertEqual((len(midway),sum(f['size'] for f in midway)),(1672,64920))
        self.assertEqual((len(full),sum(f['size'] for f in full)),(1723,69344))
        self.assertEqual(len({f['name'] for f in full}),1723)
        ordered=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in full)
        self.assertTrue(all(p[1] <= n[0] for p,n in zip(ordered,ordered[1:])))

    def test_original_research_sources_pinned_and_distinct(self):
        old={f['name'] for f in claimed_functions({k:v for k,v in self.manifest.items() if k not in ('overlay_native49_stage','overlay_native51_stage')})}
        names=set()
        for mod,fixture,total,bytes_ in ((stage49,self.a,49,2416),(stage51,self.b,51,4424)):
            self.assertEqual(len(fixture['units']),total)
            self.assertEqual(sum(u['size'] for u in fixture['units']),bytes_)
            self.assertEqual(fixture['original_rom_sha1'],'6ea0ed71032ce08fc2745f412d84936382197494')
            for u in fixture['units']:
                path=mod.SOURCE_BASE/(u['name']+'.c')
                with self.subTest(source=str(path)):
                    data=path.read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(),u['source_sha256'])
                    self.assertNotIn(b'GLOBAL_ASM',data)
                for f in u['functions']:
                    self.assertNotIn(f['name'],old)
                    self.assertNotIn(f['name'],names)
                    self.assertEqual(len(f['original_code_sha256']),64)
                    self.assertEqual(f['vma'],int(f['name'].split('_')[1],16))
                    self.assertEqual(f['rom_offset'],int(f['name'].split('_')[2],16))
                    names.add(f['name'])
        self.assertEqual(len(names),100)

if __name__=='__main__':unittest.main()

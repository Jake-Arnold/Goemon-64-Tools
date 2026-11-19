"""Fail-closed native-source and ownership tests for USA tiny9 stage."""
import copy,hashlib,json,unittest
from pathlib import Path
from decomp import overlay_tiny9
from decomp.verify import load_manifest,claimed_functions

class Tiny9NativePromotionTests(unittest.TestCase):
    def setUp(self):
        self.manifest=load_manifest(Path(__file__).with_name('manifest.json'))
        self.fixture=overlay_tiny9.load_fixture()

    def test_original_function_identity_source_sha_and_boundaries(self):
        units=self.fixture['units'];entries=overlay_tiny9.functions(self.fixture)
        self.assertEqual(len(units),7)
        self.assertEqual((len(entries),sum(f['size'] for f in entries)),(9,72))
        self.assertEqual(len({f['name'] for f in entries}),9)
        for unit in units:
            src=overlay_tiny9.SOURCE_BASE/(unit['name']+'.c')
            self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),unit['source_sha256'])
            self.assertEqual(sum(f['size'] for f in unit['functions']),unit['size'])
            self.assertEqual(unit['functions'][0]['rom_offset'],unit['rom_offset'])
            for f in unit['functions']:
                self.assertEqual(int(f['name'].split('_')[1],16),f['vma'])
                self.assertEqual(int(f['name'].rsplit('_',1)[1],16),f['rom_offset'])
                self.assertEqual(f['size'],8)

    def test_disjoint_previous_1452_claims(self):
        before=claimed_functions({k:v for k,v in self.manifest.items() if k not in ('overlay_tiny9_stage','overlay_micro2_stage')})
        after=claimed_functions({k:v for k,v in self.manifest.items() if k!='overlay_micro2_stage'})
        self.assertEqual((len(before),sum(f['size'] for f in before)),(1452,56744))
        self.assertEqual((len(after),sum(f['size'] for f in after)),(1461,56816))
        self.assertEqual(len(set(f['name'] for f in after)),1461)
        spans=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in after)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])))

    def test_unreviewed_stage_contract_rejected(self):
        doc=copy.deepcopy(self.manifest)
        doc['overlay_tiny9_stage']['format']='unreviewed'
        with self.assertRaises(ValueError):claimed_functions(doc)

    def test_unauthenticated_rom_fails_closed(self):
        with self.assertRaises(ValueError):overlay_tiny9.validate_sources(b'bad',self.fixture)

if __name__=='__main__':unittest.main()

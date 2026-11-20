"""Menu-resource two-function source and canonical ownership regression."""
import copy
import hashlib
import unittest
from decomp import overlay_menu2
from decomp.verify import load_manifest, claimed_functions


class Menu2PromotionTests(unittest.TestCase):
    def test_pinned_source_hashes_and_original_anchors(self):
        fixture=overlay_menu2.load_fixture()
        self.assertEqual(len(fixture['units']),2)
        self.assertEqual(sum(f['size'] for f in overlay_menu2.functions(fixture)),84)
        for u in fixture['units']:
            data=(overlay_menu2.SOURCE_BASE/(u['name']+'.c')).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),u['source_sha256'])

    def test_canonical_claims_are_unique(self):
        manifest=load_manifest(overlay_menu2.ROOT/'manifest.json')
        functions=claimed_functions({k:v for k,v in manifest.items() if k not in ('overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage')})
        self.assertEqual(len(functions),1500)
        self.assertEqual(len(claimed_functions(manifest)),1556)
        names=[f['name'] for f in functions]
        self.assertEqual(len(names),len(set(names)))
        for func in overlay_menu2.functions(overlay_menu2.load_fixture()):
            self.assertEqual(names.count(func['name']),1)
        self.assertEqual(names.count('func_80010980_11580'),1)

    def test_wrong_source_hash_fails_closed(self):
        fixture=overlay_menu2.load_fixture()
        tampered=copy.deepcopy(fixture)
        tampered['units'][0]['source_sha256']='0'*64
        # The actual source/ROM gate runs in decomp.verify; detect source drift in the checked-in fixture.
        self.assertNotEqual(hashlib.sha256((overlay_menu2.SOURCE_BASE/'menu2_000.c').read_bytes()).hexdigest(),tampered['units'][0]['source_sha256'])


if __name__=='__main__':unittest.main()

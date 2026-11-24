"""C-Right4 additive transaction and fail-closed source/range controls."""
import copy,unittest
from unittest.mock import patch
from decomp import usa_cright4_promotion as stage,verify
class CRight4Tests(unittest.TestCase):
    def test_claims(self):
        m=verify.load_manifest(verify.ROOT/'manifest.json');c=verify.claimed_functions(m)
        self.assertEqual((len(c),sum(f['size'] for f in c)),(2323,111736))
        self.assertEqual(len({f['name'] for f in c}),len(c))
        self.assertEqual(len(stage.claims()),4)
    def test_unreviewed_stage(self):
        m=verify.load_manifest(verify.ROOT/'manifest.json');m[stage.KEY]={'format':'wrong'}
        with self.assertRaisesRegex(ValueError,'unreviewed stage'):stage.validate_predecessor(m)
    def test_reject_source_hash(self):
        m=verify.load_manifest(verify.ROOT/'manifest.json');r=stage.rows('usa');r[0]['source_sha256']='0'*64
        with patch.object(stage,'rows',return_value=r):
            with self.assertRaisesRegex(ValueError,'native source drift'):stage.validate_predecessor(m)
    def test_reject_existing_owner(self):
        m=verify.load_manifest(verify.ROOT/'manifest.json');r=stage.rows('usa');r[0]['rom_offset']=verify.claimed_functions({k:v for k,v in m.items() if k!=stage.KEY})[0]['rom_offset']
        with patch.object(stage,'rows',return_value=r):
            with self.assertRaisesRegex(ValueError,'duplicate original owner'):stage.validate_predecessor(m)
if __name__=='__main__':unittest.main()

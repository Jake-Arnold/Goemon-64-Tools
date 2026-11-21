"""ROM-free checks for immutable native scheduler insertion wrapper source."""
import hashlib
import unittest
from pathlib import Path
from decomp import scheduler5_g2_promotion as stage

class Scheduler5StageTests(unittest.TestCase):
    def test_original_identity(self):
        fixture=stage.fixture()
        f=fixture['functions'][0]
        self.assertEqual((f['name'],f['rom_offset'],f['vma'],f['size']),('func_80034B24_35724',0x35724,0x80034B24,52))
        self.assertEqual(f['original_code_sha256'],'0eab8ac0d64b399e5bbb84096877a33a3347d5f7542bf22c8828f60e2319a1a3')

    def test_source_hash_and_abi(self):
        f=stage.fixture()['functions'][0]
        s=(stage.BASE/'sources'/f['source']).read_bytes()
        self.assertEqual(hashlib.sha256(s).hexdigest(),f['source_sha256'])
        self.assertIn(b'func_80034B58_35758',s)
        self.assertIn(b'D_8016DAB4_16E6B4',s)

    def test_fixture_refuses_mutation(self):
        f=stage.fixture()['functions'][0]
        self.assertEqual(len(f['source_sha256']),64)
        self.assertEqual(stage.ORIGINAL_SHA1,'6ea0ed71032ce08fc2745f412d84936382197494')

if __name__=='__main__': unittest.main()

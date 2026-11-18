"""ROM-free fail-closed authenticity checks for file26 original-address C."""
import copy
import unittest
from pathlib import Path
from decomp import overlay_highbyte26 as stage
from decomp.verify import load_manifest, claimed_functions, highbyte26_stage

class File26HighbyteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=stage.load_fixture()
        cls.manifest=load_manifest(Path(__file__).with_name('manifest.json'))

    def test_only_fifteen_original_address_sources(self):
        entries=self.fixture['functions']
        self.assertEqual((len(entries), sum(x['size'] for x in entries)),(15,2508))
        self.assertEqual(len(set(x['name'] for x in entries)),15)
        self.assertEqual(len(set(x['rom_offset'] for x in entries)),15)
        for x in entries:
            with self.subTest(symbol=x['name']):
                self.assertEqual(stage.sha256((stage.SOURCE_BASE/(x['name']+'.c')).read_bytes()),x['source_sha256'])
                self.assertEqual(x['vma'],int(x['name'].split('_')[1],16))
                self.assertEqual(x['rom_offset'],int(x['name'].split('_')[2],16))

    def test_manifest_canonical_increment_without_double_claim(self):
        original={k:v for k,v in self.manifest.items() if k not in ('overlay_highbyte26_stage','overlay_file27_stage','overlay_wide132_stage','overlay_wide109_stage')}
        existing={k:v for k,v in self.manifest.items() if k not in ('overlay_file27_stage','overlay_wide132_stage','overlay_wide109_stage')}
        old=claimed_functions(original);new=claimed_functions(existing)
        self.assertEqual((len(old),sum(x['size'] for x in old)),(951,38816))
        self.assertEqual((len(new),sum(x['size'] for x in new)),(966,41324))
        self.assertEqual(len({x['name'] for x in new}),966)
        self.assertEqual(len(highbyte26_stage(self.manifest)['functions']),15)

    def test_wrong_manifest_format_rejected(self):
        bad=copy.deepcopy(self.manifest)
        bad['overlay_highbyte26_stage']['format']='unknown'
        with self.assertRaises(ValueError):highbyte26_stage(bad)

    def test_mutated_source_rejected_before_rom(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            source=Path(tmp)
            for original in stage.SOURCE_BASE.glob('*.c'):
                (source/original.name).write_bytes(original.read_bytes())
            name=self.fixture['functions'][0]['name']
            (source/(name+'.c')).write_text('malicious source mutation')
            with self.assertRaisesRegex(ValueError,'source modified'):
                stage.validate_sources(b'not-a-rom',self.fixture,source)

    def test_bad_original_rom_rejected(self):
        with self.assertRaisesRegex(ValueError,'Not original'):
            stage.validate_sources(b'invalid',self.fixture)

if __name__=='__main__':unittest.main()

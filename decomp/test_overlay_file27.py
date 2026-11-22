"""Fail-closed original C, ROM and no-double-count checks for file27."""
import copy
import unittest
from pathlib import Path
from decomp import overlay_file27 as stage
from decomp.verify import load_manifest, claimed_functions, file27_stage

# This suite proves its historical promotion checkpoint, not subsequent stages.
_historical_load_manifest = load_manifest

def load_manifest(*args, **kwargs):
    manifest = _historical_load_manifest(*args, **kwargs)
    manifest.pop('overlay_native49_stage', None)
    manifest.pop('overlay_native51_stage', None)
    # The 233-C batch is newer than this frozen historical checkpoint.
    manifest.pop('overlay_isolated233_stage', None)
    manifest.pop('overlay_reconcile108_stage', None)  # Preserve this historical acceptance checkpoint
    manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
    return manifest


class File27StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=stage.load_fixture()
        cls.manifest=load_manifest(Path(__file__).with_name('manifest.json'))

    def test_pinned_address_source_and_extent(self):
        rows=self.fixture['functions']
        self.assertEqual((len(rows),sum(x['size'] for x in rows)),(21,1316))
        self.assertEqual(len({x['name'] for x in rows}),21)
        offsets=[]
        for x in rows:
            with self.subTest(symbol=x['name']):
                self.assertEqual(stage.sha256((stage.SOURCE_BASE/(x['name']+'.c')).read_bytes()),x['source_sha256'])
                self.assertEqual(int(x['name'].split('_')[1],16),x['vma'])
                self.assertEqual(int(x['name'].split('_')[2],16),x['rom_offset'])
                offsets.append((x['rom_offset'],x['rom_offset']+x['size']))
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(offsets,offsets[1:])))

    def test_increment_is_21_not_a_duplicate(self):
        prior={k:v for k,v in self.manifest.items() if k not in ('overlay_file27_stage','overlay_wide132_stage','overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage')}
        file27_view={k:v for k,v in self.manifest.items() if k not in ('overlay_wide132_stage','overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage')}
        old=claimed_functions(prior);new=claimed_functions(file27_view)
        self.assertEqual((len(old),sum(x['size'] for x in old)),(966,41324))
        self.assertEqual((len(new),sum(x['size'] for x in new)),(987,42640))
        self.assertEqual(len({x['name'] for x in new}),987)

    def test_invalid_stage_format_fails(self):
        bad=copy.deepcopy(self.manifest)
        bad['overlay_file27_stage']['format']='other'
        with self.assertRaisesRegex(ValueError,'Unreviewed'):
            file27_stage(bad)

    def test_changed_source_fails_before_private_rom(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as path:
            tmp=Path(path)
            for src in stage.SOURCE_BASE.glob('*.c'):(tmp/src.name).write_bytes(src.read_bytes())
            name=self.fixture['functions'][0]['name']
            (tmp/(name+'.c')).write_text('tampered source')
            with self.assertRaisesRegex(ValueError,'source modified'):
                stage.validate_sources(b'not-a-ROM',self.fixture,tmp)

    def test_wrong_original_rom_fails(self):
        with self.assertRaisesRegex(ValueError,'Not original'):
            stage.validate_sources(b'bad',self.fixture)

if __name__=='__main__':unittest.main()

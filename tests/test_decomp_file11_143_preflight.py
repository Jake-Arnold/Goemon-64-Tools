"""Fail-closed ROM-free acceptance of the opt-in file_11 143-C preflight.

The existing 210-function manifest remains the sole production source of truth.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from decomp import file11_143_preflight as mod
from decomp.verify import load_manifest


class File11143PreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(mod.ROOT / 'manifest.json')
        # Explicit historical 210-C projection: strip precisely the current
        # 143-C file_11 stage, the two Impact stages and the 36-byte dialogue C.
        cls.manifest = copy.deepcopy(cls.manifest)
        # Historical 210-C projection omits the separately reviewed 47-C stage.
        cls.manifest.pop('overlay_crossregion47_stage', None)
        cls.manifest.pop('overlay_native87_stage', None)
        cls.manifest.pop('overlay_file27_stage', None)
        cls.manifest.pop('overlay_highbyte26_stage', None)
        cls.manifest.pop('overlay_wide132_stage', None)
        cls.manifest.pop('overlay_wide109_stage', None)
        cls.manifest.pop('overlay_resource140_stage', None)
        cls.manifest.pop('overlay_graphics5_stage', None)
        cls.manifest.pop('overlay_file18_53_stage', None)
        cls.manifest.pop('overlay_callbacks10_stage', None)
        cls.manifest.pop('overlay_main19_stage', None)
        cls.manifest.pop('overlay_tiny9_stage', None)
        cls.manifest.pop('overlay_micro2_stage', None)
        cls.manifest.pop('overlay_micro15_stage', None)
        cls.manifest['overlay_file11_stage'] = {'format': 'goemon-file11-character-switch-50-v2'}
        cls.manifest['overlay_file12_stages'] = [
            x for x in cls.manifest['overlay_file12_stages']
            if x['format'] != 'goemon-file12-registration-374-v1'
            and x['function']['name'] not in {
                f['name'] for f in json.loads((mod.ROOT/'results/usa_file12_spatial_11_promotion_20261117.json').read_text())['functions']
            }
        ]
        del cls.manifest['overlay_file13_stages']
        cls.manifest['support_headers'].remove('impact_controller.h')
        dialogue = next(u for u in cls.manifest['units'] if u['source']=='dialogue_window.c')
        added = next(f for f in dialogue['functions'] if f['name']=='func_8000C430_D030')
        dialogue['functions'].remove(added)
        dialogue['assembly_functions'].insert(2,added['name'])
        cls.fixture = json.loads(mod.FIXTURE.read_text(encoding='utf-8'))

    def checked(self, fixture=None, manifest=None, rom=None):
        return mod.validate(manifest or self.manifest, fixture or self.fixture, rom)

    def test_canonical_210_plus_93_is_not_promoted(self):
        plan = self.checked()
        self.assertEqual((plan['baseline_usa_c'], plan['existing_file11_c'],
                          plan['additional_research_c'], plan['prospective_usa_c']),
                         (210, 50, 93, 303))
        self.assertEqual((plan['file11_c_total'], plan['file11_c_instruction_bytes']), (143, 3908))
        self.assertEqual((plan['c_units'], plan['asm_slices']), (44, 44))
        self.assertFalse(plan['central_g2_verified'])
        self.assertFalse(plan['eligible_for_manifest_promotion'])
        self.assertFalse(plan['rom_verified'])

    def test_reject_changed_research_source(self):
        f = copy.deepcopy(self.fixture)
        next(x for x in f['chunks'] if x['kind'] == 'c')['source'] += '\nint extra;'
        with self.assertRaises(ValueError):
            self.checked(f)

    def test_reject_duplicate_or_moved_original_function(self):
        f = copy.deepcopy(self.fixture)
        c = [x for x in f['chunks'] if x['kind'] == 'c']
        c[-1]['functions'][-1]['name'] = c[0]['functions'][0]['name']
        with self.assertRaises(ValueError):
            self.checked(f)
        f = copy.deepcopy(self.fixture)
        next(x for x in f['chunks'] if x['kind'] == 'c')['functions'][0]['vma'] += 4
        with self.assertRaises(ValueError):
            self.checked(f)

    def test_reject_original_overlay_gap_and_changed_chunk_digest(self):
        f = copy.deepcopy(self.fixture)
        f['chunks'][1]['rom_start'] += 4
        with self.assertRaises(ValueError):
            self.checked(f)
        f = copy.deepcopy(self.fixture)
        f['chunks'][0]['original_sha256'] = 'x' * 64
        with self.assertRaises(ValueError):
            self.checked(f)

    def test_reject_unreviewed_stage_or_claim(self):
        m = copy.deepcopy(self.manifest)
        m['overlay_file11_stage'] = {'format': 'goemon-file11-143-central-stage'}
        with self.assertRaises(ValueError):
            self.checked(manifest=m)
        f = copy.deepcopy(self.fixture)
        f['production_promotion_count'] = 93
        with self.assertRaises(ValueError):
            self.checked(f)

    def test_reject_wrong_original_rom(self):
        with self.assertRaises(ValueError):
            self.checked(rom=b'invalid')

    def test_emit_creates_44_sources_and_88_segments_exclusively(self):
        plan = self.checked()
        with tempfile.TemporaryDirectory(prefix='file11-143-contract-') as root:
            output = Path(root) / 'fresh'
            mod.emit(plan, output)
            self.assertEqual(len(list((output / 'src').glob('*.c'))), 44)
            seg = (output / 'file11-subsegments.txt').read_text().splitlines()
            self.assertEqual(len(seg), 88)
            self.assertEqual(seg[0], '    - [0x587370, asm]')
            self.assertIn('    - [0x5993E8, c, character_switch_entry]', seg)
            report = json.loads((output / 'preflight.json').read_text())
            self.assertFalse(report['eligible_for_manifest_promotion'])
            self.assertNotIn('c_sources', report)
            with self.assertRaises(FileExistsError):
                mod.emit(plan, output)

    def test_refuse_staging_into_repository_source_tree(self):
        for destination in (mod.ROOT / 'never-write-stage-here',
                            mod.ROOT.parent / 'also-never-write-here'):
            with self.subTest(destination=destination):
                with self.assertRaises(ValueError):
                    mod.emit(self.checked(), destination)


if __name__ == '__main__':
    unittest.main()

"""ROM-free checks for the opt-in, noncanonical USA 143-C central stage."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from decomp import file11_143_stage as stage
from decomp import verify


ROOT = Path(__file__).resolve().parents[1]


class File11143CentralStageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = verify.load_manifest(ROOT / 'decomp/manifest.json')

    def opt_in(self):
        manifest = copy.deepcopy(self.base)
        manifest['overlay_file11_stage'] = {'format': stage.STAGE_FORMAT}
        return manifest

    def test_canonical_315_includes_152_file11(self):
        self.assertEqual(verify.file11_stage_mode(self.base), 152)
        self.assertEqual(len(verify.claimed_functions(self.base)), 315)
        self.assertEqual(self.base['overlay_file11_stage']['format'],
                         'goemon-file11-152-central-v1')

    def test_canonical_143_claims_coexist_with_impact(self):
        candidate = self.opt_in()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'review-manifest.json'
            path.write_text(json.dumps(candidate), encoding='utf-8')
            loaded = verify.load_manifest(path)
        self.assertEqual(verify.file11_stage_mode(loaded), 143)
        claims = verify.claimed_functions(loaded)
        self.assertEqual(len(claims), 306)
        self.assertEqual(len({x['name'] for x in claims}), 306)
        self.assertEqual(sum(x['size'] for x in claims), 16292)
        plan = stage.reviewed_plan(loaded)
        self.assertEqual((plan['existing_file11_c'], plan['additional_research_c']),
                         (50, 93))
        self.assertFalse(plan['eligible_for_manifest_promotion'])
        self.assertFalse(plan['central_g2_verified'])

    def test_stage_has_complete_44_c_and_44_assembly_objects(self):
        objects = stage.source_objects()
        self.assertEqual(len(objects), 88)
        self.assertEqual(len(stage.object_targets()), 88)
        self.assertEqual(len(set(stage.object_targets())), 88)
        self.assertEqual(sum(size for _, size, _ in objects), 0x5B8500 - 0x587370)
        self.assertEqual(
            sum(size for _, size, chunk in objects if chunk['kind'] == 'c'), 3908)
        self.assertEqual(sum(chunk['kind'] == 'c' for _, _, chunk in objects), 44)

    def test_splat_stage_preserves_exact_original_neighbors(self):
        original = (
            '  - name: file_11\n'
            '    type: code\n'
            '    start: 0x587370\n'
            '    vram: 0x801CB460\n'
            '    subalign: 16\n'
            '    subsegments:\n'
            '    - [0x587370, asm]\n'
            '    - [0x5B8500, data]\n'
            '  - name: file_12\n'
            '    type: code\n'
        )
        output = stage.stage_splat(original, stage.reviewed_plan(self.opt_in()))
        self.assertEqual(output.count('  - name: file_11'), 1)
        self.assertIn('    - [0x5B8500, data]', output)
        self.assertEqual(output.count(', c, '), 44)
        self.assertEqual(output.count(', asm]'), 44)
        self.assertIn('  - name: file_12\n    type: code', output)
        with self.assertRaises(ValueError):
            stage.stage_splat(output, stage.reviewed_plan(self.opt_in()))

    def test_reject_unreviewed_function_count_or_source(self):
        candidate = self.opt_in()
        del candidate['overlay_file11_stage']
        with self.assertRaises(ValueError):
            stage.reviewed_plan(candidate)
        candidate = self.opt_in()
        candidate['overlay_file11_stage'] = {'format': 'unreviewed'}
        with self.assertRaises(ValueError):
            stage.reviewed_plan(candidate)

    def test_source_payloads_must_not_replace_existing_source(self):
        plan = stage.reviewed_plan(self.opt_in())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'src').mkdir()
            files = stage.source_payloads(root, plan)
            self.assertEqual(len(files), 44)
            first, _source = files[0]
            first.write_text('unrelated user source', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                stage.source_payloads(root, plan)


if __name__ == '__main__':
    unittest.main()

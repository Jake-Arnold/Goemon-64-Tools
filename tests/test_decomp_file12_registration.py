"""ROM-free fail-closed tests for the versioned USA 374-wrapper C island."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from decomp import file12_registration as reg
from decomp import overlay_file12
from decomp.verify import claimed_functions, load_manifest, manifest_file12_stages, validate_file12_stage_definition

ROOT = Path(__file__).resolve().parents[1]


class RegistrationStageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(ROOT / 'decomp/manifest.json')
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
        cls.manifest.pop('overlay_micro20_stage', None)
        cls.manifest.pop('overlay_menu2_stage', None)
        cls.manifest.pop('overlay_statecopy1_stage', None)
        cls.manifest.pop('overlay_archive22_stage', None); cls.manifest.pop('overlay_archive33_stage', None); cls.manifest.pop('overlay_archive61_stage', None); cls.manifest.pop('overlay_checkpoint500_stage', None); cls.manifest.pop('overlay_rediscovery5_stage', None)
        cls.group = manifest_file12_stages(cls.manifest)[0]

    def test_pinned_source_has_all_374_original_function_identities(self):
        source = (ROOT / 'decomp' / reg.SOURCE_NAME).read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(), reg.SOURCE_SHA256)
        text = source.decode('utf-8')
        self.assertNotIn('GLOBAL_ASM', text)
        self.assertEqual(text.count('void func_802'), reg.COUNT)
        self.assertEqual(len(reg.functions()), reg.COUNT)
        self.assertEqual(sum(row['size'] for row in reg.functions()), reg.TOTAL_BYTES)
        self.assertEqual(reg.functions()[0]['rom_offset'], reg.ROM_START)
        self.assertEqual(reg.functions()[-1]['rom_offset'] + reg.FUNCTION_BYTES,
                         reg.ROM_START + reg.TOTAL_BYTES)
        for index, fn in enumerate(reg.functions()):
            self.assertEqual(fn['name'],
                f'func_{reg.VMA_START+index*reg.FUNCTION_BYTES:08X}_{reg.ROM_START+index*reg.FUNCTION_BYTES:X}')
            self.assertEqual(text.count('void ' + fn['name'] + '(void)'), 1)

    def test_stage_claims_374_real_functions_not_group_marker(self):
        staged = manifest_file12_stages(self.manifest)
        self.assertEqual(len(staged), 14)
        self.assertEqual(validate_file12_stage_definition(staged[0]), Path(reg.SOURCE_NAME))
        claims = claimed_functions(self.manifest)
        self.assertEqual(len(claims), 987)
        self.assertEqual(len({row['name'] for row in claims}), 987)
        self.assertNotIn(reg.GROUP_NAME, {row['name'] for row in claims})
        expected = {row['name'] for row in reg.functions()}
        self.assertEqual(expected & {row['name'] for row in claims}, expected)

    def test_group_stage_rejects_any_changed_contract(self):
        for key, value in (
            ('source_sha256', '0' * 64),
            ('object_sha256', '1' * 64),
            ('compiler_object_sha256', '2' * 64),
            ('source', '../escaped.c'),
        ):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.group)
                changed[key] = value
                with self.assertRaises(ValueError):
                    validate_file12_stage_definition(changed)
        altered = copy.deepcopy(self.group)
        altered['function']['size'] += 4
        with self.assertRaises(ValueError):
            validate_file12_stage_definition(altered)

    def test_file12_stage_split_places_group_before_existing_callbacks(self):
        from decomp.verify import _file12_stages_layout
        layout = _file12_stages_layout(manifest_file12_stages(self.manifest))
        self.assertEqual(layout['assembly'][0], 'file_12_before_5C9310')
        self.assertEqual(layout['assembly'][1], 'file_12_gap_5CC7A8_5D424C')
        self.assertEqual(layout['assembly'][-1], 'file_12_after_5DD65C')
        self.assertIn('    - [0x5C9310, c, file12_reg374]', layout['lines'])

    def test_unrecognized_group_or_missing_compiler_object_is_not_accepted(self):
        with self.assertRaises(ValueError):
            reg.validate_object(b'not an ELF', staged=True)
        with self.assertRaises(ValueError):
            reg.pack(b'not the pinned IDO 5.3 object')
        self.assertFalse(reg.is_group({'format': 'unreviewed-file12-stage'}))

    def test_old_file12_callback_reference_hashes_unchanged(self):
        for name in overlay_file12.FUNCTIONS:
            self.assertNotIn(name, {r['name'] for r in reg.functions()})
        self.assertEqual(len(overlay_file12.FUNCTIONS), 13)
        self.assertTrue({'func_80222034_5DD504', 'func_80222168_5DD638'}
                        <= set(overlay_file12.FUNCTIONS))


if __name__ == '__main__':
    unittest.main()

"""ROM-free region selection, manifest integrity and Japanese ownership tests."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from types import ModuleType
import sys
import tempfile
import unittest
from unittest.mock import patch

from decomp import region_verify as rv


class JapaneseRegionManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = rv.load_manifest()

    def assert_invalid(self, modify, phrase):
        manifest = copy.deepcopy(self.original)
        modify(manifest)
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'japan.json'
            dest.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, phrase):
                rv.load_manifest(dest)

    def test_pinned_region_and_source_revision(self):
        self.assertEqual(self.original['region'], 'japan_0')
        self.assert_invalid(lambda m: m.__setitem__('region', 'usa'), 'Unsupported region')
        self.assert_invalid(lambda m: m.__setitem__('upstream_commit', '0'*40), 'revision')

    def test_rejects_cross_region_rom_and_unsupported_revision(self):
        self.assert_invalid(lambda m: m['retail'].__setitem__('sha1', '0'*40), 'retail reference')
        self.assert_invalid(lambda m: m['expanded'].__setitem__('size', 16), 'expanded reference')

    def test_function_original_address_and_bounds(self):
        self.assert_invalid(lambda m: m['units'][0]['functions'][1].__setitem__('vram', 0x80010000), 'extent/name')
        self.assert_invalid(lambda m: m['units'][0]['functions'][0].__setitem__('name', 'func_800161F0_17260'), 'extent/name')
        self.assert_invalid(lambda m: m['units'][0].__setitem__('section_size', 160), 'gap or overlap')

    def test_rejects_missing_and_duplicate_source_ownership(self):
        self.assert_invalid(lambda m: m['units'][0].__setitem__('source', '../secret.c'), 'prefix|Unsafe')
        self.assert_invalid(lambda m: m['units'][0].__setitem__('object', 'build/usa/src/x.o'), 'prefix')
        self.assert_invalid(lambda m: m['units'].append(copy.deepcopy(m['units'][0])), 'Duplicate')

    def test_verified_manifest_accounts_for_eighteen_distinct_functions(self):
        items = [f for unit in self.original['units'] for f in unit['functions']]
        self.assertEqual(len(items), 18)
        self.assertEqual(sum(f['size'] for f in items), 756)
        self.assertEqual(len({f['name'] for f in items}), 18)


class JapaneseRegionObjectTests(unittest.TestCase):
    def test_link_map_exact_extent_and_guest_function_addresses(self):
        unit = rv.load_manifest()['units'][0]
        body = f' .text          0x{unit["vram"]:x}       0x80 {unit["object"]}\n'
        for fn in unit['functions']:
            body += f'                0x{fn["vram"]:x}                {fn["name"]}\n'
        rv._map_section(body, unit)
        with self.assertRaisesRegex(ValueError, 'wrong guest address'):
            rv._map_section(body.replace(f'0x{unit["vram"]:x}', '0x80001234', 1), unit)
        with self.assertRaisesRegex(ValueError, 'missing or repeated'):
            rv._map_section(body.replace(unit['object'], 'wrong/source.c.o'), unit)

    def test_object_symbols_require_exact_function_names_sizes(self):
        text = '''00000000 l    d  .text  00000080 .text
00000000 g     F .text  00000024 func_800161F0_16DF0
00000024 g     F .text  00000028 func_80016214_16E14
0000004c g     F .text  00000034 func_8001623C_16E3C
'''
        with patch.object(rv.subprocess, 'run') as run:
            run.return_value.stdout = text
            result = rv._object_symbols('mips-linux-gnu-objdump', Path('/tmp/bit-array.o'))
        self.assertEqual(result['func_80016214_16E14'], (36, 40))
        self.assertEqual(len(result), 3)

    def test_japanese_splat_config_must_match_original_and_two_c_units(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = root / rv.japan_asm_baseline.PINNED_CONFIG
            original.parent.mkdir(parents=True)
            original.write_text('sha1: ' + rv.japan_asm_baseline.JAPAN_EXPANDED_SHA1)
            candidate = root / rv.japan_four_c.SPLAT_CONFIG
            candidate.write_text('different')
            with patch.object(rv.japan_asm_baseline, 'render_asm_config', return_value='a'), \
                 patch.object(rv.japan_first_c, 'render_config', return_value='b'), \
                 patch.object(rv.japan_four_c, 'render_config', return_value='expected'):
                with self.assertRaisesRegex(ValueError, 'Splat split'):
                    rv._verify_stage(root)
                candidate.write_text('expected')
                rv._verify_stage(root)

    def test_identity_failure_before_any_rom_data_accepted(self):
        manifest = rv.load_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'dummy-retail.z64').write_bytes(b'not-a-rom')
            with patch.object(rv.subprocess, 'check_output', return_value='wrong sha\n'):
                with self.assertRaisesRegex(ValueError, 'not pinned'):
                    rv.verify_japan(root, root / 'dummy-retail.z64', manifest, source_dir=root)


class RegionEntryPointTests(unittest.TestCase):
    def test_usa_default_delegates_to_unchanged_verifier(self):
        verify = ModuleType('decomp.verify')
        original_args = ['--upstream', '/tmp/pinned', '--workdir', '/tmp/new', '--retail-rom', '/tmp/us.z64', '--report', '/tmp/report.json']
        with patch.dict(sys.modules, {'decomp.verify':verify}), patch.object(verify, 'main', create=True, return_value=7) as forwarded:
            self.assertEqual(rv.main(original_args), 7)
            forwarded.assert_called_once_with(original_args)
            self.assertEqual(rv.main(['--region', 'usa', *original_args]), 7)
            forwarded.assert_called_with(original_args)

    def test_report_refuses_overwrite_before_native_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / 'existing.json'
            report.write_text('do not destroy')
            with self.assertRaises(SystemExit) as err:
                rv.main(['--region', 'japan_0', '--checkout', tmp, '--retail-output', tmp+'/retail.z64', '--report', str(report)])
            self.assertEqual(err.exception.code, 2)
            self.assertEqual(report.read_text(), 'do not destroy')


if __name__ == '__main__':
    unittest.main()

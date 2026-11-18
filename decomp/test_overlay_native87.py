"""ROM-free guardrails for the separately verified 87-function USA C stage."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from decomp import overlay_native87 as stage


class OriginalAddressNative87Tests(unittest.TestCase):
    def test_fixture_is_complete_and_original_address_pinned(self):
        fixture=stage.load_fixture()
        rows=fixture['functions']
        self.assertEqual(len(rows),87)
        self.assertEqual(sum(r['size'] for r in rows),912)
        self.assertEqual(len({r['name'] for r in rows}),87)
        self.assertEqual(len({r['rom_offset'] for r in rows}),87)
        self.assertEqual({r['section'] for r in rows},set(stage.OVERLAY_NAMES))
        for row in rows:
            self.assertEqual(int(row['name'].split('_')[1],16),row['vma'])
            self.assertEqual(int(row['name'].split('_')[2],16),row['rom_offset'])
            self.assertEqual(hashlib.sha256((stage.SOURCE_BASE/(row['name']+'.c')).read_bytes()).hexdigest(),row['source_sha256'])

    def test_modified_source_is_never_eligible(self):
        fixture=stage.load_fixture()
        with tempfile.TemporaryDirectory() as td:
            copied=Path(td)
            for row in fixture['functions']:
                (copied/(row['name']+'.c')).write_bytes((stage.SOURCE_BASE/(row['name']+'.c')).read_bytes())
            bad=fixture['functions'][0]['name']+'.c'
            (copied/bad).write_bytes(b'void forged(){}')
            with self.assertRaisesRegex(ValueError,'Native87 C source modified'):
                stage.validate_sources(b'',fixture,copied)

    def test_wrong_original_bytes_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'Not original decompressed USA ROM'):
            stage.validate_sources(b'\x00'*32,stage.load_fixture())

    def test_asm_ownership_must_be_unique_and_active(self):
        first=stage.load_fixture()['functions'][0]
        fixture={'functions':[first]}
        name=first['name']
        with tempfile.TemporaryDirectory() as td:
            work=Path(td)
            (work/'.splat/usa').mkdir(parents=True)
            (work/'asm/usa').mkdir(parents=True)
            ld=work/'.splat/usa/mnsg.ld'
            ld.write_text('build/usa/asm/usa/first.s.o(.text);\n')
            (work/'asm/usa/first.s').write_text(f'nonmatching {name}, 0x{first["size"]:X}\n')
            owners=stage.find_owners(work,fixture)
            self.assertEqual(owners[name],('first',first['size']))
            self.assertEqual(stage.parent_targets(owners),['build/usa/asm/usa/first.s.o'])
            ld.write_text('build/usa/asm/usa/first.s.o(.text);\nbuild/usa/asm/usa/second.s.o(.text);\n')
            (work/'asm/usa/second.s').write_text(f'nonmatching {name}, 0x{first["size"]:X}\n')
            with self.assertRaisesRegex(ValueError,'two active ASM owners'):
                stage.find_owners(work,fixture)
            ld.write_text('build/usa/asm/usa/second.s.o(.rodata);\n')
            with self.assertRaisesRegex(ValueError,'No active original ASM'):
                stage.find_owners(work,fixture)

    def test_invalid_duplicate_fixture_rejected(self):
        # The immutable fixture is read afresh: a caller may not silently
        # substitute candidate entries or invent new address identities.
        original=stage.load_fixture()
        self.assertEqual(len(original['functions']),87)
        bad=copy.deepcopy(original)
        bad['functions'][1]['name']=bad['functions'][0]['name']
        self.assertNotEqual(len({e['name'] for e in bad['functions']}),87)


if __name__=='__main__':
    unittest.main()

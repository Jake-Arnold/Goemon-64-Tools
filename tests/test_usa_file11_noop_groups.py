"""ROM-free contract tests for two native-matching callback clusters."""
import re
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from decomp.research import usa_file11_noop_groups as mod
from decomp import overlay_file11


class TestFile11NoopGroups(unittest.TestCase):
    def test_groups_are_37_distinct_functions(self):
        functions=mod.entries()
        self.assertEqual(len(functions),37)
        self.assertEqual(len(set(x[0] for x in functions)),37)
        self.assertEqual(len(set(x[1] for x in functions)),37)
        self.assertTrue(all(name.split('_')[-1]==f'{offset:X}' for name,offset in functions))
        self.assertEqual(len(set(x[0] for x in functions)&set(x[0] for x in overlay_file11.FUNCTIONS)),0)

    def test_12_chunk_extents_are_consecutive(self):
        chunks=mod.CHUNKS
        self.assertEqual(len(chunks),12)
        self.assertEqual(chunks[0][2],overlay_file11.ROM_START)
        self.assertEqual(chunks[-1][2]+chunks[-1][3],overlay_file11.TEXT_END)
        self.assertEqual(sum(item[3] for item in chunks),overlay_file11.TEXT_END-overlay_file11.ROM_START)
        self.assertTrue(all(a[2]+a[3]==b[2] for a,b in zip(chunks,chunks[1:])))
        self.assertEqual(sum(c[3] for c in chunks if c[0]=='c'),1064)
        self.assertEqual(len(mod.objects()),len(chunks))

    def test_exact_empty_callbacks_c(self):
        root=Path(__file__).resolve().parents[1]/'decomp/research'
        for start,count,name in mod.GROUPS:
            code=mod.render(name,count,start)
            self.assertEqual((root/(name+'.c')).read_text(),code)
            self.assertEqual(code.count('{}'),count)
            self.assertEqual(len(re.findall(r'(?m)^void func_[0-9A-F]{8}_[0-9A-F]+\(',code)),count)

    def test_original_pattern_is_exact_three_instruction_words(self):
        self.assertEqual(mod.ORIGINAL_NOOP.hex().upper(),'AFA4000003E00008AFA50004')
        self.assertEqual(len(mod.ORIGINAL_NOOP),12)

    def test_all_native_object_hashes_are_pinned(self):
        self.assertEqual(set(mod.TRIMMED_C_OBJECT_SHA256),{item[2] for item in mod.GROUPS})
        self.assertTrue(all(re.fullmatch('[0-9a-f]{64}',v) for v in mod.TRIMMED_C_OBJECT_SHA256.values()))

    def test_refuses_wrong_rom_without_source_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            with self.assertRaisesRegex(ValueError,'ROM identity'):
                mod.prepare(home,b'no rom')
            self.assertFalse((home/'src').exists())

    def test_trim_refuses_missing_elf_without_linker_modification(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            (home/'.splat/usa').mkdir(parents=True)
            linker=home/'.splat/usa/mnsg.ld'
            linker.write_text(mod.LINKER_OLD)
            with self.assertRaises(FileNotFoundError):
                mod.trim(home)
            self.assertEqual(linker.read_text(),mod.LINKER_OLD)

    def test_verify_fails_on_wrong_reference_before_touching_elf(self):
        with self.assertRaisesRegex(ValueError,'ROM identity'):
            mod.verify(Path('/invalid'),b'wrong',Path('/invalid'))


    def test_v2_splat_extension_rejects_repeat(self):
        s='  - name: file_11\n    - [0x599918, c, character_switch_wrappers]\n'+mod.SPLAT_OLD+'\n  - name: file_12\n'
        converted=mod.stage_splat(s)
        self.assertIn('    - [0x59D0C0, c, callback_noops_a]',converted)
        self.assertIn('    - [0x59D38C, c, callback_noops_b]',converted)
        with self.assertRaisesRegex(ValueError,'Expected pristine'):
            mod.stage_splat(converted)

    def test_exact_v2_stage_contract(self):
        self.assertEqual(mod.STAGE_FORMAT,'goemon-file11-character-switch-50-v2')
        self.assertEqual(len(mod.object_targets()),12)
        self.assertEqual(mod.object_targets()[8],'build/usa/src/callback_noops_a.c.o')
        self.assertEqual(mod.object_targets()[10],'build/usa/src/callback_noops_b.c.o')

    def test_c_source_copies_have_pinned_hashes(self):
        root=Path(__file__).resolve().parents[1]/'decomp/research'
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            (home/'src').mkdir()
            with mock.patch.object(mod,'validate_reference',return_value=None):
                staged=mod.checked_source_copies(home,root,b'')
            self.assertEqual(len(staged),2)
            for source,dest in staged:
                self.assertTrue(source.is_file())
                self.assertFalse(dest.exists())
                self.assertEqual(mod.sha256(source.read_bytes()),mod.PINNED_SOURCE_SHA256[dest.stem])

    def test_c_source_collision_rejected_before_copy(self):
        root=Path(__file__).resolve().parents[1]/'decomp/research'
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            (home/'src').mkdir()
            (home/'src/callback_noops_b.c').write_text('collision')
            with mock.patch.object(mod,'validate_reference',return_value=None):
                with self.assertRaisesRegex(ValueError,'colliding'):
                    mod.checked_source_copies(home,root,b'')
            self.assertFalse((home/'src/callback_noops_a.c').exists())


if __name__=='__main__':unittest.main()
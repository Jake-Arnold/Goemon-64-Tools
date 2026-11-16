"""Fail-closed offline contract tests for the file_11 143-C candidate."""
from __future__ import annotations
import copy
import json
import os
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import verify_file11_143 as probe

class File11Production143Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads(probe.FIXTURE.read_text())
        location=os.environ.get('GOEMON_PINNED_UPSTREAM')
        if not location:raise unittest.SkipTest('Set GOEMON_PINNED_UPSTREAM to the pristine USA baseline checkout')
        cls.original=Path(location)
        cls.rom=(cls.original/'config/usa/baserom.decompressed.z64').read_bytes()
        cls.elf=cls.original/'build/usa/mnsg.elf'
        cls.asm=cls.original/'asm/usa/587370.s'

    def checked(self,fixture=None):
        # The fixture is read from its pinned path; use temporary replacement
        # entirely in memory by intercepting Path.read_text, not the filesystem.
        target=probe.FIXTURE
        orig=Path.read_text
        def read_text(path,*args,**kwargs):
            if path==target and fixture is not None:
                return json.dumps(fixture)
            return orig(path,*args,**kwargs)
        from unittest.mock import patch
        with patch.object(Path,'read_text',read_text):
            return probe.checked_fixture(self.rom,self.elf,self.asm)

    def test_authentic_manifest_contract(self):
        f,functions=self.checked()
        self.assertEqual(len(functions),143)
        self.assertEqual(sum(c['size'] for c in f['chunks'] if c['kind']=='c'),3908)
        self.assertEqual(len([c for c in f['chunks'] if c['kind']=='c']),44)
        self.assertEqual(f['new_covered_functions_beyond_existing_50'],93)

    def test_reject_altered_ROM_chunk_hash(self):
        f=copy.deepcopy(self.fixture);f['chunks'][0]['original_sha256']='0'*64
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_relocated_C_fragment(self):
        f=copy.deepcopy(self.fixture)
        next(c for c in f['chunks'] if c['kind']=='c')['rom_start']+=4
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_changed_C_source(self):
        f=copy.deepcopy(self.fixture)
        next(c for c in f['chunks'] if c['kind']=='c')['source']+='\nint foreign=1;'
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_duplicate_function_identity(self):
        f=copy.deepcopy(self.fixture)
        first=next(c for c in f['chunks'] if c['kind']=='c')['functions'][0]['name']
        last=next(c for c in reversed(f['chunks']) if c['kind']=='c')
        last['functions'][-1]['name']=first
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_source_with_assembly(self):
        f=copy.deepcopy(self.fixture)
        next(c for c in f['chunks'] if c['kind']=='c')['source']='GLOBAL_ASM("unsafe");'
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_candidate_promotion_claim(self):
        f=copy.deepcopy(self.fixture);f['production_promotion_count']=93
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_original_symbol_identity_change(self):
        f=copy.deepcopy(self.fixture)
        next(c for c in f['chunks'] if c['kind']=='c')['functions'][0]['vma']+=4
        with self.assertRaises(ValueError):self.checked(f)

    def test_reject_original_assembly_changed(self):
        with self.assertRaises(ValueError):
            probe.checked_fixture(self.rom,self.elf,Path(__file__))

if __name__=='__main__':unittest.main()

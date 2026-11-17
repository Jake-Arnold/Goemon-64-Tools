"""ROM-free negative controls for the opt-in 47-C production overlay stage."""
from __future__ import annotations
import copy
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

try:
    from decomp import overlay_crossregion47 as stage
except ImportError:
    import overlay_crossregion47 as stage


class OverlayCrossregion47Tests(unittest.TestCase):
    def setUp(self):
        self.fixture=stage.load_fixture()

    def test_exact_reviewed_original_function_bounds(self):
        entries=self.fixture['functions']
        self.assertEqual(len(entries),47)
        self.assertEqual(sum(e['size'] for e in entries),2220)
        self.assertEqual(len({e['name'] for e in entries}),47)
        self.assertEqual({x['section'] for x in entries},set(stage.OVERLAYS))

    @staticmethod
    def _original_rom():
        """Optional user-owned ROM; never assume a developer-local filesystem."""
        supplied = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM', '')
        return Path(supplied) if supplied else None

    def test_committed_source_hashes_match_manifest(self):
        for entry in self.fixture['functions']:
            raw = (stage.SOURCE_BASE / (entry['name'] + '.c')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),
                             entry['source_sha256'], entry['name'])

    def test_fail_closed_on_source_sha_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)
            for e in self.fixture['functions']:
                (src/(e['name']+'.c')).write_bytes((stage.SOURCE_BASE/(e['name']+'.c')).read_bytes())
            name=self.fixture['functions'][0]['name']
            (src/(name+'.c')).write_bytes(b'void changed(void) {}\n')
            original=self._original_rom()
            if original is None or not original.is_file():
                self.skipTest('Original ROM not provided in GOEMON_USA_DECOMPRESSED_ROM')
            with self.assertRaisesRegex(ValueError,'Source SHA'):
                stage.validate_sources(original.read_bytes(),self.fixture,src)

    def test_rejects_wrong_original_rom(self):
        with self.assertRaisesRegex(ValueError,'original 32MiB'):
            stage.validate_sources(b'not original',self.fixture)

    def test_rejects_duplicate_names(self):
        modified=copy.deepcopy(self.fixture)
        modified['functions'][1]['name']=modified['functions'][0]['name']
        import json
        with tempfile.TemporaryDirectory() as tmp:
            fixture=Path(tmp)/'fixture.json'
            fixture.write_text(json.dumps(modified))
            with patch.object(stage,'FIXTURE',fixture),self.assertRaisesRegex(ValueError,'Unsafe/duplicate'):
                stage.load_fixture()

    def test_rejects_bad_original_symbol_offset(self):
        modified=copy.deepcopy(self.fixture)
        modified['functions'][0]['rom_offset']+=4
        import json
        with tempfile.TemporaryDirectory() as tmp:
            fixture=Path(tmp)/'fixture.json'
            fixture.write_text(json.dumps(modified))
            with patch.object(stage,'FIXTURE',fixture),self.assertRaisesRegex(ValueError,'Unsafe/duplicate'):
                stage.load_fixture()

    def test_source_and_original_code_sha256(self):
        original=self._original_rom()
        if original is None or not original.is_file():
            self.skipTest('Original ROM not provided in GOEMON_USA_DECOMPRESSED_ROM')
        stage.validate_sources(original.read_bytes(),self.fixture)


if __name__=='__main__':
    unittest.main()

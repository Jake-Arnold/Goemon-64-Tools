"""ROM-free original-source provenance and fail-closed Japanese short28 tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib,json,unittest
from unittest.mock import patch
from decomp import japan_short28_promotion as jp28

class JPShort28Tests(unittest.TestCase):
    def test_original_source_hashes_and_coverage(self):
        data=jp28.rows()
        self.assertEqual(len(data),28)
        self.assertEqual(sum(f['size'] for f in data),1980)
        self.assertEqual(sum(f['native_relocation_count'] for f in data),124)
        self.assertEqual(len(set(f['name'] for f in data)),28)
        self.assertEqual(len(set(f['rom_offset'] for f in data)),28)
        self.assertEqual(len(set(f['original_asm_owner'] for f in data)),13)
    def test_research_negative_controls_preserved(self):
        for item in jp28.rows():
            good=(jp28.PACKAGE/item['source']).read_bytes()
            bad=(jp28.PACKAGE/item['negative_source']).read_bytes()
            self.assertNotEqual(good,bad,item['name'])
            self.assertEqual(hashlib.sha256(bad).hexdigest(),item['negative_sha256'])
    def test_reference_count_is_immutable(self):
        self.assertEqual((jp28.BASE_C,jp28.BASE_BYTES,jp28.BASE_RELOCS),(2370,127008,80745))
    def test_reject_duplicate_rom_identity(self):
        with TemporaryDirectory() as tmp:
            modified=json.loads(jp28.MANIFEST.read_text())
            modified['functions'][1]['rom_offset']=modified['functions'][0]['rom_offset']
            file=Path(tmp)/'manifest.json';file.write_text(json.dumps(modified))
            with patch.object(jp28,'MANIFEST',file),patch.object(jp28,'MANIFEST_SHA',hashlib.sha256(file.read_bytes()).hexdigest()):
                with self.assertRaises(ValueError):jp28.rows()
    def test_fail_closed_original_rom_absent(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):jp28.original(Path(tmp))

if __name__=='__main__':unittest.main()

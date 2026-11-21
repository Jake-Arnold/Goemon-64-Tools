"""ROM-free, native-source hash and actual C host-regression checks for scheduler4."""
from __future__ import annotations
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from decomp import scheduler4_g2_promotion as stage

class SchedulerFourStageTests(unittest.TestCase):
    def test_fixture_four_original_addresses_and_192_bytes(self):
        data=stage.load_fixture()
        self.assertEqual(len(data['functions']),4)
        self.assertEqual(sum(r['size'] for r in data['functions']),192)
        self.assertEqual([r['rom_offset'] for r in data['functions']], [0x359D8,0x35A08,0x35A38,0x35A68])
        self.assertEqual(len({r['name'] for r in data['functions']}),4)

    def test_source_hashes_are_pinned(self):
        for entry in stage.load_fixture()['functions']:
            content=(stage.SOURCE/entry['source']).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(),entry['source_sha256'])
            self.assertIn(entry['name'].encode(),content)

    def test_original_symbol_offsets_are_region_specific(self):
        for entry in stage.load_fixture()['functions']:
            self.assertEqual(entry['vma']-entry['rom_offset'],0x7FFFF400)
            self.assertEqual(int(entry['name'].split('_')[1],16),entry['vma'])
            self.assertEqual(int(entry['name'].split('_')[2],16),entry['rom_offset'])

    @unittest.skipUnless(shutil.which('gcc'), 'Requires GCC for sanitizer compile')
    def test_actual_native_c_host_sanitizers(self):
        source=stage.SOURCE/'scheduler_neighbors_verified.c'
        tests=stage.SOURCE.parent/'tests'
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'scheduler4-host'
            subprocess.run(['gcc','-std=c11','-O1','-g','-Wall','-Wextra','-Werror',
                            '-fsanitize=address,undefined','-fno-omit-frame-pointer',
                            '-I'+str(tests/'stubs'),str(source),str(tests/'test_scheduler_neighbors.c'),'-o',str(out)],check=True,capture_output=True)
            result=subprocess.run([str(out)],check=True,capture_output=True,text=True)
            self.assertIn('1024 call chains',result.stdout)

if __name__=='__main__':unittest.main()

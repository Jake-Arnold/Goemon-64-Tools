import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from decomp.verify import load_manifest

ROOT=Path(__file__).resolve().parents[1]


class KeySpawnGateTests(unittest.TestCase):
    def test_isolated_proof_binds_source_and_stays_outside_full_rom_count(self):
        proof=json.loads((ROOT/'decomp/results/key_spawn_gate_candidate.json').read_text())
        source=ROOT/'decomp'/proof['source']
        digest=hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        self.assertEqual(proof['source_sha256_lf'],digest)
        self.assertEqual(proof['status'],'linked_match')
        self.assertEqual(proof['comparison']['expected_size'],96)
        self.assertEqual(proof['comparison']['actual_size'],96)
        self.assertEqual(proof['comparison']['byte_differences'],0)
        self.assertEqual(proof['comparison']['expected_sha256'],proof['comparison']['actual_sha256'])
        self.assertFalse(proof['full_rom_verified'])
        self.assertEqual(proof['claimed_verified_functions'],0)
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertNotIn(proof['function'],{f['name'] for u in manifest['units'] for f in u['functions']})

    @unittest.skipUnless(os.name=='posix' and shutil.which('gcc'),'Requires Linux GCC')
    def test_host_control_flow_field_offset_and_no_state_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            executable=Path(folder)/'key-gate-test'
            subprocess.run(['gcc','-std=c11','-Wall','-Wextra','-Werror','-Idecomp/test_support',
                            'decomp/test_key_spawn_gate.c','-o',str(executable)],cwd=ROOT,check=True,capture_output=True)
            subprocess.run([str(executable)],check=True,capture_output=True)

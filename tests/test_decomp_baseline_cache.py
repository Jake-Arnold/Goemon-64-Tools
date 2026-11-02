import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from decomp.verify import certify_baseline, validate_baseline_cache


class BaselineCacheTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.root=Path(self.folder.name)
        for name in ('config/usa','build/usa','tools/ido-5.3','.venv/bin'):
            (self.root/name).mkdir(parents=True)
        self.image=b'synthetic reference image'
        for name in ('config/usa/baserom.decompressed.z64','build/usa/mnsg.z64'):
            (self.root/name).write_bytes(self.image)
        (self.root/'build/usa/mnsg.elf').write_bytes(b'synthetic ELF identity')
        (self.root/'tools/ido-5.3/cc').write_bytes(b'synthetic compiler')
        (self.root/'uv.lock').write_bytes(b'locked dependencies')
        (self.root/'.venv/bin/python').write_bytes(b'environment marker')
        self.pin='1'*40
        self.dirty=''
        self.manifest={'upstream_commit':self.pin,'decompressed_sha1':hashlib.sha1(self.image).hexdigest()}
        def capture(command,**kwargs):return self.pin+'\n' if command[1]=='rev-parse' else self.dirty
        self.mock=patch('decomp.verify.subprocess.check_output',side_effect=capture)
        self.mock.start()

    def tearDown(self):
        self.mock.stop();self.folder.cleanup()

    def test_cache_is_exclusive_and_validation_is_read_only(self):
        proof=certify_baseline(self.root,self.manifest)
        before={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(validate_baseline_cache(self.root,self.manifest),proof)
        after={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
        with self.assertRaises(FileExistsError):certify_baseline(self.root,self.manifest)

    def test_changed_compiler_elf_lock_and_rom_are_rejected(self):
        certify_baseline(self.root,self.manifest)
        for name in ('tools/ido-5.3/cc','build/usa/mnsg.elf','uv.lock','build/usa/mnsg.z64','config/usa/baserom.decompressed.z64'):
            path=self.root/name;before=path.read_bytes();path.write_bytes(before+b'changed')
            with self.subTest(name=name):
                with self.assertRaises(ValueError):validate_baseline_cache(self.root,self.manifest)
            path.write_bytes(before)

    def test_missing_or_changed_provenance_and_environment_fail_closed(self):
        with self.assertRaises(FileNotFoundError):validate_baseline_cache(self.root,self.manifest)
        certify_baseline(self.root,self.manifest)
        proof_path=self.root/'build/goemon-baseline-proof.json'
        before=proof_path.read_text();proof=json.loads(before);proof['elf_sha256']='0'*64
        proof_path.write_text(json.dumps(proof))
        with self.assertRaises(ValueError):validate_baseline_cache(self.root,self.manifest)
        proof_path.write_text(before)
        (self.root/'.venv/bin/python').unlink()
        with self.assertRaises(ValueError):validate_baseline_cache(self.root,self.manifest)

    def test_source_pin_and_tracked_changes_are_rejected(self):
        certify_baseline(self.root,self.manifest)
        self.dirty='src/changed.c\n'
        with self.assertRaises(ValueError):validate_baseline_cache(self.root,self.manifest)
        self.dirty='';self.pin='2'*40
        with self.assertRaises(ValueError):validate_baseline_cache(self.root,self.manifest)

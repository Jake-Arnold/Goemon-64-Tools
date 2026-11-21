"""ROM-free validation of the original-address USA 0x2C40 dispatcher stage."""
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import tempfile

from decomp import usa_dispatcher_g2_promotion as stage

class TestDispatcherStage(unittest.TestCase):
    def test_reviewed_original_identity_and_source_hash(self):
        m=stage.fixture()
        self.assertEqual(m['function']['name'],'func_80002040_2C40')
        self.assertEqual(m['function']['rom_offset'],0x2c40)
        self.assertEqual(m['function']['vma'],0x80002040)
        self.assertEqual(m['function']['size'],120)
        self.assertEqual(hashlib.sha256(stage.SOURCE.read_bytes()).hexdigest(),m['function']['source_sha256'])
    def test_safety_and_original_abi(self):
        src=stage.SOURCE.read_text()
        self.assertIn('D_8015C5C8_15D1C8[STATE_OFFSET]',src)
        self.assertIn('D_3ADD4',src)
        self.assertIn('callbacks[18]',src)
        self.assertIn('volatile int unused[2]',src)
        self.assertNotIn('asm(',src)
        self.assertNotIn('__asm__',src)
    def test_fails_closed_on_bad_source(self):
        orig=stage.SOURCE
        self.assertTrue(orig.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            changed=Path(tmp)/'tampered.c'
            changed.write_bytes(orig.read_bytes()+b'\n')
            with patch.object(stage,'SOURCE',changed):
                with self.assertRaisesRegex(ValueError,'source hash changed'):
                    stage.fixture()
    def test_reloc_and_identity_thresholds(self):
        m=stage.fixture()
        self.assertEqual(m['expected_rom_bytes'],33554432)
        self.assertEqual(m['expected_elf_functions'],7376)
        self.assertEqual(m['expected_relocations'],82103)
        self.assertEqual(m['accepted_prior_count'],1965)

if __name__=='__main__':unittest.main()

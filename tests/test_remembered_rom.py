"""Remember Japan-0 ROM selection without weakening exact ROM verification."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from practice.game_versions import VERSIONS
from practice.remembered_rom import (
    FORMAT, remember_verified_rom, load_remembered_rom,
)


class RememberedRomTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.rom = self.root / 'japan game.z64'
        self.rom.write_bytes(b'original-japan-rom-test')
        self.store = self.root / 'settings' / 'verified_rom_paths.json'

    @staticmethod
    def verified(path, version_key):
        if Path(path).read_bytes() != b'original-japan-rom-test':
            raise ValueError('ROM bytes changed since verification')
        if version_key != 'japan':
            raise ValueError('Wrong region')
        return VERSIONS['japan']

    def test_remember_and_recheck_same_file_next_session(self):
        with patch('practice.remembered_rom.verify_selected_rom',
                   side_effect=self.verified) as verify:
            path = remember_verified_rom(self.rom, 'japan', store=self.store)
            self.assertEqual(path, self.rom.resolve())
            self.assertEqual(load_remembered_rom('japan', store=self.store), path)
        self.assertEqual(verify.call_count, 2)
        data = json.loads(self.store.read_text(encoding='utf-8'))
        self.assertEqual(data['format'], FORMAT)
        self.assertEqual(data['versions']['japan']['canonical_sha1'],
                         VERSIONS['japan'].sha1)
        self.assertEqual(data['versions']['japan']['path'], str(self.rom.resolve()))
        self.assertNotIn('original-japan-rom-test', self.store.read_text())

    def test_edit_or_remove_rom_fails_closed_without_cached_trust(self):
        with patch('practice.remembered_rom.verify_selected_rom',
                   side_effect=self.verified):
            remember_verified_rom(self.rom, 'japan', store=self.store)
            self.rom.write_bytes(b'modified')
            self.assertIsNone(load_remembered_rom('japan', store=self.store))
            self.rom.unlink()
            self.assertIsNone(load_remembered_rom('japan', store=self.store))
        self.assertTrue(self.store.exists())

    def test_corrupt_registry_and_spoofed_digest_rejected(self):
        self.assertIsNone(load_remembered_rom('japan', store=self.store))
        self.store.parent.mkdir(parents=True)
        self.store.write_text('{invalid', encoding='utf-8')
        self.assertIsNone(load_remembered_rom('japan', store=self.store))
        self.store.write_text(json.dumps({
            'format': FORMAT, 'versions': {
                'japan': {'path': str(self.rom), 'canonical_sha1': '0' * 40}
            }}), encoding='utf-8')
        with patch('practice.remembered_rom.verify_selected_rom') as verifier:
            self.assertIsNone(load_remembered_rom('japan', store=self.store))
        verifier.assert_not_called()

    def test_wrong_region_never_stored(self):
        with patch('practice.remembered_rom.verify_selected_rom',
                   side_effect=self.verified):
            with self.assertRaises(ValueError):
                remember_verified_rom(self.rom, 'usa', store=self.store)
            self.assertFalse(self.store.exists())


if __name__ == '__main__':
    unittest.main()

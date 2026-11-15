"""Synthetic Japan-0 position control tests; no real emulator or ROM writes."""
import struct
import unittest

from practice.japanese_position import (
    JAPAN_PLAYER_XYZ, JAPAN_PLAYER_XYZ_START, JAPAN_SCENE_INDEX,
    JAPAN_CHARACTER_INDEX, JAPAN_OEDO_SOUTH_ENTRANCE,
    checked_japan_xyz, read_japan_position, move_japan_goemon_oedo_south,
)
from tests.test_japanese_party_unlock import Process


def ram(endian='wordswapped'):
    p = Process(endian)
    p.set_guest(JAPAN_SCENE_INDEX, (0x161).to_bytes(2, 'big'))
    p.set_guest(JAPAN_CHARACTER_INDEX, (0).to_bytes(4, 'big'))
    p.set_guest(JAPAN_PLAYER_XYZ_START, struct.pack('>fff', -174.5, 0.0, -142.0))
    p.writes.clear()
    return p


class JapanesePositionTests(unittest.TestCase):
    def test_confirmed_guest_offsets_and_oedo_entrance(self):
        self.assertEqual(JAPAN_PLAYER_XYZ, (
            0x80151B10, 0x80151B14, 0x80151B18))
        self.assertEqual(struct.pack('>fff', *JAPAN_OEDO_SOUTH_ENTRANCE).hex(),
                         'c390800000000000c3270000')
        self.assertEqual(struct.pack('>f', 52.0).hex(), '42500000')

    def test_goemon_oedo_12_byte_write_word_swapped_and_big(self):
        for endian in ('wordswapped', 'big'):
            with self.subTest(endian=endian):
                p = ram(endian)
                reader = p.rdram()
                old = reader.read_guest(JAPAN_PLAYER_XYZ_START, 12)
                res = move_japan_goemon_oedo_south(
                    reader, JAPAN_OEDO_SOUTH_ENTRANCE, expected_before=old)
                self.assertTrue(res.changed)
                self.assertEqual(read_japan_position(reader),
                                 JAPAN_OEDO_SOUTH_ENTRANCE)
                self.assertEqual(
                    reader.read_guest(JAPAN_PLAYER_XYZ_START, 12),
                    bytes.fromhex('c390800000000000c3270000'))
                self.assertEqual(len(p.writes), 1)
                self.assertEqual(p.writes[0][1],
                                 (bytes.fromhex('008090c300000000000027c3')
                                  if endian == 'wordswapped'
                                  else bytes.fromhex('c390800000000000c3270000')))
                self.assertEqual(reader.read_guest(JAPAN_CHARACTER_INDEX, 4),
                                 bytes(4))

    def test_invalid_decimal_or_overrange_never_writes(self):
        invalid = (
            (float('nan'), 0, 0), (0, float('inf'), 0),
            ('bad', 0, 0), (True, 0, 0), (10001, 0, 0),
            (1, 2), '1,2,3',
        )
        for values in invalid:
            p = ram()
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    move_japan_goemon_oedo_south(
                        p.rdram(), values,
                        expected_before=p.rdram().read_guest(
                            JAPAN_PLAYER_XYZ_START, 12))
                self.assertEqual(p.writes, [])

    def test_wrong_character_or_scene_never_writes(self):
        for scene, char in ((0x1D1, 0), (0x161, 1),
                            (0x161, 2), (0x000, 0)):
            p = ram()
            p.set_guest(JAPAN_SCENE_INDEX, scene.to_bytes(2, 'big'))
            p.set_guest(JAPAN_CHARACTER_INDEX, char.to_bytes(4, 'big'))
            with self.subTest(scene=scene, char=char):
                with self.assertRaisesRegex(RuntimeError, 'only for Goemon'):
                    move_japan_goemon_oedo_south(
                        p.rdram(), (0.0, 0.0, 0.0),
                        expected_before=p.rdram().read_guest(
                            JAPAN_PLAYER_XYZ_START, 12))
                self.assertEqual(p.writes, [])

    def test_stale_before_and_noop(self):
        p = ram()
        guest = p.rdram()
        with self.assertRaisesRegex(RuntimeError, 'after confirmation'):
            move_japan_goemon_oedo_south(
                guest, (0, 0, 0), expected_before=bytes(12))
        self.assertEqual(p.writes, [])
        result = move_japan_goemon_oedo_south(
            guest, read_japan_position(guest),
            expected_before=guest.read_guest(JAPAN_PLAYER_XYZ_START, 12))
        self.assertFalse(result.changed)
        self.assertEqual(p.writes, [])

    def test_readonly_handle_does_not_write(self):
        p = ram()
        p.writable = False
        with self.assertRaises(PermissionError):
            move_japan_goemon_oedo_south(
                p.rdram(), (0, 0, 0),
                expected_before=p.rdram().read_guest(JAPAN_PLAYER_XYZ_START, 12))
        self.assertEqual(p.writes, [])


if __name__ == '__main__':
    unittest.main()

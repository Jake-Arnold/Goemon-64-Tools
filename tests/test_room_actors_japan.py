import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from practice.room_actors import (
    JP_CODE_RAM, JP_ROOM_POINTERS, JP_RETAIL_SHA1, JP_SCHEMA,
    JapanRomFiles, actor_names, actors_for_stage, digest, extract_actors,
    save_actors, load_actors, validate_actors,
)
from tests.test_room_actors import room_fixture


class JapanActorTests(unittest.TestCase):
    def test_japan_independent_overlay_pointer_table(self):
        room, start, footer, ending = room_fixture()
        code = bytearray(JP_ROOM_POINTERS+4*484)
        # JP overlay offset is region-specific; never use USA's ROM pointer.
        meta_offset = 0x23000
        struct.pack_into('>I', code, JP_ROOM_POINTERS+353*4, 0x80000000+JP_CODE_RAM+meta_offset)
        struct.pack_into('>HHHHHHH', code, meta_offset+8,
                         0x800, start, 0x800, ending, 0x800, footer, 0)
        struct.pack_into('>H', code, meta_offset+20, 0x40B)

        class FakeJapanFiles:
            sha1 = JP_RETAIL_SHA1
            def file(self, index):
                return bytes(code) if index == 12 else room
        with patch('practice.room_actors.JapanRomFiles', return_value=FakeJapanFiles()):
            atlas = extract_actors(b'fake',region='japan_0')
        self.assertEqual(atlas['payload']['region'],'japan_0')
        self.assertEqual(atlas['payload']['format'],JP_SCHEMA)
        self.assertEqual(len(actors_for_stage(atlas,353)),4)
        validate_actors(atlas)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'actors.json'
            save_actors(path,atlas)
            self.assertEqual(load_actors(path),atlas)

    def test_wrong_region_and_unverified_usa_names(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):extract_actors(b'bad',region='japan_1')
        with self.assertRaisesRegex(ValueError,'Japanese actor extraction requires'):JapanRomFiles(bytes.fromhex('8037124011223344'))
        with self.assertRaises(ValueError):extract_actors(bytes.fromhex('8037124011223344'),region='usa')
        names=actor_names(region='japan_0')
        self.assertEqual(names[0x08C][1],'USA ID label / Japan unverified')
        with self.assertRaises(ValueError):actor_names(region='japan_1')


if __name__=='__main__':unittest.main()

"""ROM-free tests for opt-in Japanese party unlock writes."""
import unittest

from practice.backends.memory import Rdram
from practice.japanese_party_unlock import (
    PARTY_FLAGS, CHARACTER_INDEX_ADDR, SCENE_ID_ADDR,
    unlock_japan_party_member,
)


class Process:
    def __init__(self, endian="wordswapped", writable=True):
        self.writable = writable
        self.endian = endian
        self.mem = bytearray(0x800000)
        self.writes = []
        self.set_guest(CHARACTER_INDEX_ADDR, (0).to_bytes(4, "big"))
        self.set_guest(SCENE_ID_ADDR, (352).to_bytes(2, "big"))
        for _, address in PARTY_FLAGS.values():
            self.set_guest(address - 3, bytes(4))
        self.writes.clear()

    def set_guest(self, address, data):
        start = address & 0x1FFFFFFF
        for pos, byte in enumerate(data):
            offset = start + pos
            if self.endian == "wordswapped":
                offset ^= 3
            elif self.endian == "byteswapped":
                offset ^= 1
            self.mem[offset] = byte

    def read(self, address, length):
        return bytes(self.mem[address:address+length])

    def write(self, address, data):
        if not self.writable:
            raise PermissionError("Read-only process")
        self.mem[address:address+len(data)] = data
        self.writes.append((address, bytes(data)))

    def rdram(self):
        return Rdram(self, 0, self.endian)


class JapanesePartyUnlockTests(unittest.TestCase):
    def test_only_sasuke_yae_allowlisted(self):
        ram = Process().rdram()
        for value in (-1, 0, 1, 4, True, "2"):
            with self.assertRaises(ValueError):
                unlock_japan_party_member(ram, value)
        self.assertEqual(PARTY_FLAGS[2], ("Sasuke", 0x80161E97))
        self.assertEqual(PARTY_FLAGS[3], ("Yae", 0x80161E9B))

    def test_sasuke_unlock_single_low_byte_big_endian(self):
        p = Process("big")
        out = unlock_japan_party_member(p.rdram(), 2)
        self.assertEqual((out.before, out.after), (bytes(4), b"\x00\x00\x00\x01"))
        self.assertTrue(out.changed)
        self.assertEqual(p.rdram().read_guest(0x80161E94, 4), b"\x00\x00\x00\x01")
        self.assertEqual(p.rdram().read_guest(CHARACTER_INDEX_ADDR, 4), bytes(4))
        self.assertEqual(p.writes, [(0x161E97, b"\x01")])

    def test_yae_unlock_word_swapped_preserves_neighbours(self):
        p = Process("wordswapped")
        out = unlock_japan_party_member(p.rdram(), 3)
        self.assertEqual(out.address, 0x80161E9B)
        self.assertTrue(out.changed)
        self.assertEqual(p.rdram().read_guest(0x80161E98, 4), b"\x00\x00\x00\x01")
        self.assertEqual(p.writes, [(0x161E98, b"\x01\x00\x00\x00")])
        self.assertEqual(p.rdram().read_guest(0x80161DCC, 4), bytes(4))

    def test_no_write_if_already_unlocked(self):
        p = Process()
        p.set_guest(0x80161E94, b"\x00\x00\x00\x01")
        result = unlock_japan_party_member(p.rdram(), 2)
        self.assertFalse(result.changed)
        self.assertEqual(p.writes, [])

    def test_no_write_if_member_word_unusual(self):
        p = Process()
        p.set_guest(0x80161E94, b"\x02\x00\x00\x00")
        with self.assertRaisesRegex(RuntimeError, "expected 00000000"):
            unlock_japan_party_member(p.rdram(), 2)
        self.assertEqual(p.writes, [])

    def test_no_write_if_forced_character_index(self):
        p = Process()
        p.set_guest(CHARACTER_INDEX_ADDR, b"\x00\x00\x00\x02")
        with self.assertRaisesRegex(RuntimeError, "Goemon or Ebisumaru"):
            unlock_japan_party_member(p.rdram(), 3)
        self.assertEqual(p.writes, [])

    def test_no_write_if_no_game_scene(self):
        p = Process()
        p.set_guest(SCENE_ID_ADDR, b"\x00\x00")
        with self.assertRaisesRegex(RuntimeError, "gameplay scene"):
            unlock_japan_party_member(p.rdram(), 2)
        self.assertEqual(p.writes, [])

    def test_read_only_process_must_not_be_bypassed(self):
        p = Process(writable=False)
        with self.assertRaises(PermissionError):
            unlock_japan_party_member(p.rdram(), 2)
        self.assertEqual(p.writes, [])

    def test_yae_after_sasuke_with_goemon_active(self):
        p = Process()
        unlock_japan_party_member(p.rdram(), 2)
        unlock_japan_party_member(p.rdram(), 3)
        self.assertEqual(p.rdram().read_guest(0x80161E94, 4), b"\x00\x00\x00\x01")
        self.assertEqual(p.rdram().read_guest(0x80161E98, 4), b"\x00\x00\x00\x01")
        self.assertEqual(p.rdram().read_guest(CHARACTER_INDEX_ADDR, 4), bytes(4))

if __name__ == "__main__":
    unittest.main()

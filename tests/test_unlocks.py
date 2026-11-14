"""Writable unlock values tested on fake N64 RAM, not a running game."""
from __future__ import annotations
import unittest
from practice.unlocks import UNLOCKS, GROUPS, BY_ADDRESS, read_unlock, write_unlock, validate_unlocks, unlock_all_known


class FakeRAM:
    def __init__(self):
        self.bytes = {0x800C7A94: 13}
        self.writes = []
    def u8(self, address):
        return self.read_guest(address, 1)[0]
    def read_guest(self, address, length):
        return bytes(self.bytes.get(address + i, 0) for i in range(length))
    def write_guest(self, address, value):
        self.writes.append((address, value))
        for i, b in enumerate(value):
            self.bytes[address + i] = b


class TestUnlocks(unittest.TestCase):
    def test_mappings_match_inspector(self):
        validate_unlocks()
        self.assertEqual(len(UNLOCKS), 34)
        self.assertEqual(len(set(x.address for x in UNLOCKS)), len(UNLOCKS))
        self.assertEqual({x.group for x in UNLOCKS}, set(GROUPS))

    def test_binary_toggle_and_neighbor_bytes(self):
        ram = FakeRAM()
        ram.bytes[0x8015C6BE] = 0x54
        ram.bytes[0x8015C6C0] = 0x6A
        chain = BY_ADDRESS[0x8015C6BF]
        self.assertEqual(chain.values, (0, 2))
        self.assertTrue(write_unlock(ram, chain, 2))
        self.assertEqual(read_unlock(ram, chain), 2)
        self.assertEqual(ram.read_guest(0x8015C6BE,3), bytes((0x54,2,0x6A)))
        self.assertTrue(write_unlock(ram, chain, 0))
        self.assertEqual(read_unlock(ram, chain), 0)

    def test_weapon_level_has_three_stages(self):
        ram = FakeRAM()
        upgrade = BY_ADDRESS[0x8015C6AF]
        self.assertEqual(upgrade.values, (0, 1, 2))
        self.assertTrue(write_unlock(ram, upgrade, 1))
        self.assertTrue(write_unlock(ram, upgrade, 2))
        self.assertEqual(read_unlock(ram, upgrade), 2)

    def test_noop_and_no_extra_write(self):
        ram = FakeRAM()
        item = BY_ADDRESS[0x8015C6C3]
        self.assertFalse(write_unlock(ram, item, 0))
        self.assertEqual(ram.writes, [])

    def test_invalid_value_never_writes(self):
        ram = FakeRAM()
        with self.assertRaises(ValueError):
            write_unlock(ram, BY_ADDRESS[0x8015C6C3], 2)
        with self.assertRaises(ValueError):
            write_unlock(ram, BY_ADDRESS[0x8015C6BF], 1)
        self.assertEqual(ram.writes, [])

    def test_fish_are_counts_not_binary(self):
        ram=FakeRAM()
        expected_caps={0x8015C71B:8, 0x8015C723:3, 0x8015C71F:5}
        for address,cap in expected_caps.items():
            field=BY_ADDRESS[address]
            self.assertTrue(field.quantity)
            self.assertEqual(field.max_value, cap)
            self.assertTrue(write_unlock(ram,field,0xFE))
            self.assertEqual(read_unlock(ram,field),cap)
            self.assertTrue(write_unlock(ram,field,0))
            with self.assertRaises(ValueError):write_unlock(ram,field,256)

    def test_miracle_flags_and_candidate_item_slots(self):
        ram=FakeRAM()
        for address in (0x8015C85B,0x8015C85F,0x8015C863,0x8015C866,
                        0x8015C703,0x8015C707,0x8015C70F):
            self.assertIn(address,BY_ADDRESS)
            self.assertTrue(write_unlock(ram,BY_ADDRESS[address],1))
            self.assertEqual(read_unlock(ram,BY_ADDRESS[address]),1)

    def test_sasuke_battery_1_preserves_other_event_flags(self):
        addr=0x8015C609
        field=BY_ADDRESS[addr]
        self.assertEqual(field.bit_mask,0x20)
        self.assertNotIn(0x8015C70B,BY_ADDRESS)
        ram=FakeRAM()
        ram.bytes[addr]=0x85
        self.assertEqual(read_unlock(ram,field),0)
        self.assertTrue(write_unlock(ram,field,1))
        self.assertEqual(ram.bytes[addr],0xA5)
        self.assertEqual(read_unlock(ram,field),1)
        self.assertFalse(write_unlock(ram,field,1))
        self.assertTrue(write_unlock(ram,field,0))
        self.assertEqual(ram.bytes[addr],0x85)
        self.assertEqual(len(ram.writes),2)
        with self.assertRaises(ValueError):write_unlock(ram,field,0x20)

    def test_unlock_all_known_one_shot_and_packed_flag_preserved(self):
        from tests.test_checkpoint import TestCheckpoint
        _, ram = TestCheckpoint().sample()
        ram.write_guest(0x8015C609,b'\x85')
        changed, total = unlock_all_known(ram)
        self.assertEqual(total,len(UNLOCKS))
        self.assertGreater(changed,0)
        self.assertEqual(ram.u8(0x8015C609),0xA5)
        self.assertEqual(ram.u8(0x8015C6AF),2)
        self.assertEqual(ram.u8(0x8015C6BF),2)
        self.assertEqual(ram.u8(0x8015C71B),8)
        self.assertEqual(ram.u8(0x8015C723),3)
        self.assertEqual(ram.u8(0x8015C71F),5)
        self.assertEqual(unlock_all_known(ram),(0,total))

    def test_unlock_all_refuses_non_gameplay_without_writes(self):
        from tests.test_checkpoint import TestCheckpoint
        _, ram = TestCheckpoint().sample()
        ram.write_guest(0x800C7A94,b'\x04')
        with self.assertRaises(ValueError):
            unlock_all_known(ram)
        self.assertEqual(ram.u8(0x8015C6AF),0)

    def test_transition_blocks_flag_write(self):
        ram = FakeRAM()
        ram.bytes[0x800C7A94] = 4
        with self.assertRaises(RuntimeError):
            write_unlock(ram, BY_ADDRESS[0x8015C6C7], 1)
        self.assertEqual(ram.writes, [])



    def test_doll_progress_control_keeps_all_quarter_states(self):
        field=BY_ADDRESS[0x8015C707];ram=FakeRAM()
        self.assertEqual(field.values,(0,1,2,3,4))
        for value in field.values:
            write_unlock(ram,field,value)
            self.assertEqual(read_unlock(ram,field),value)
        self.assertEqual(field.levels[2],'1/2')
        self.assertEqual(field.levels[3],'3/4')

if __name__ == '__main__':
    unittest.main()

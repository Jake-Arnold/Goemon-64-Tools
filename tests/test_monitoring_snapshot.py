"""Read-only snapshot survives special modes without trusting a stale player."""
import unittest

from autosplitter.memory import (
    Rdram, SYS_POINTER_ADDR, PLAYER_OBJECT_PTR_ADDR, PLAYER_TASK_PTR_ADDR,
    CHARACTER_ID_ADDR, LOADING_FLAG_ADDR, discover_rdram,
)
from tests.test_tools import BASE, Tests, write_u8, write_u32


class MonitoringSnapshotTests(unittest.TestCase):
    def sample(self):
        proc = Tests().sample()
        write_u8(proc, 0x800C7A94, 13)
        write_u8(proc, 0x800C7A9E, 1)
        return proc, Rdram(proc, BASE)

    def test_valid_normal_player_unchanged(self):
        proc, ram = self.sample()
        strict = ram.snapshot()
        monitored = ram.snapshot_for_monitoring()
        self.assertEqual(monitored, strict)
        self.assertAlmostEqual(monitored["x"], 125.25)

    def test_impact_invalid_player_pointer_does_not_disconnect(self):
        proc, ram = self.sample()
        write_u32(proc, PLAYER_OBJECT_PTR_ADDR, 0xA4600014)
        with self.assertRaisesRegex(ValueError, "Invalid player object pointer"):
            ram.snapshot()
        monitored = ram.snapshot_for_monitoring()
        self.assertIsNone(monitored["player_ptr"])
        self.assertIsNone(monitored["task_ptr"])
        self.assertIsNone(monitored["character"])
        self.assertIsNone(monitored["x"])
        self.assertIsNone(monitored["action"])
        self.assertIn("0xA4600014", monitored["player_unavailable_reason"])
        self.assertEqual(monitored["loading"], 0)
        # A unique known RDRAM mapping should be discoverable with no player.
        self.assertEqual(discover_rdram(proc), (BASE, "wordswapped"))

    def test_title_screen_invalid_player_pointer_is_also_tolerated(self):
        proc, ram = self.sample()
        write_u8(proc, 0x800C7A94, 6)
        write_u32(proc, PLAYER_OBJECT_PTR_ADDR, 0xA4600014)
        self.assertIsNone(ram.snapshot_for_monitoring()["x"])
        self.assertEqual(discover_rdram(proc), (BASE, "wordswapped"))

    def test_missing_player_task_is_not_exposed_to_writes(self):
        proc, ram = self.sample()
        write_u32(proc, PLAYER_TASK_PTR_ADDR, 0)
        monitored = ram.snapshot_for_monitoring()
        self.assertIsNone(monitored["player_ptr"])
        self.assertIsNone(monitored["task_ptr"])
        self.assertIsNone(monitored["action"])

    def test_unknown_character_with_stale_player_is_tolerated(self):
        proc, ram = self.sample()
        write_u32(proc, CHARACTER_ID_ADDR, 0xFFFFFFFF)
        self.assertIsNone(ram.snapshot_for_monitoring()["character"])

    def test_recovery_without_reconnection(self):
        proc, ram = self.sample()
        write_u32(proc, PLAYER_OBJECT_PTR_ADDR, 0xA4600014)
        self.assertIsNone(ram.snapshot_for_monitoring()["player_ptr"])
        write_u32(proc, PLAYER_OBJECT_PTR_ADDR, 0x801A0000)
        monitored = ram.snapshot_for_monitoring()
        self.assertEqual(monitored["player_ptr"], 0x801A0000)
        self.assertAlmostEqual(monitored["x"], 125.25)

    def test_invalid_global_system_pointer_still_fails(self):
        proc, ram = self.sample()
        write_u32(proc, SYS_POINTER_ADDR, 0xDEADBEEF)
        with self.assertRaisesRegex(ValueError, "Invalid system pointer"):
            ram.snapshot_for_monitoring()

    def test_invalid_global_loading_flag_still_fails(self):
        proc, ram = self.sample()
        write_u8(proc, LOADING_FLAG_ADDR, 200)
        with self.assertRaisesRegex(ValueError, "Invalid loading flag"):
            ram.snapshot_for_monitoring()


if __name__ == "__main__":
    unittest.main()

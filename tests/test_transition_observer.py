"""Synthetic RAM tests for the read-only scene context helper."""
import unittest
from practice.transition_observer import read_transition_observation, format_transition_observation


class FakeRam:
    def __init__(self):
        self.reads = []
    def u16(self, address):
        self.reads.append(("u16", address))
        return 353
    def u32(self, address):
        self.reads.append(("u32", address))
        if address == 0x801C77E0:
            raise OSError("unmapped")
        return address
    def read_guest(self, address, size):
        self.reads.append(("read", address, size))
        return b"\xff"


class SceneContextTests(unittest.TestCase):
    def test_reads_without_player_pointer_and_handles_partial_failure(self):
        ram = FakeRam()
        observation = read_transition_observation(ram)
        self.assertEqual(observation["Map ID"], 353)
        self.assertIsNone(observation["VM state"])
        self.assertEqual(observation["VM pause byte"], -1)
        self.assertEqual(len(ram.reads), 5)
        self.assertNotIn("write_guest", str(ram.reads))

    def test_labels_are_cautious(self):
        text = format_transition_observation(read_transition_observation(FakeRam()))
        self.assertIn("VM cursor", text)
        self.assertIn("unavailable", text)
        self.assertIn("does not prove scene activation", text)


if __name__ == "__main__":
    unittest.main()

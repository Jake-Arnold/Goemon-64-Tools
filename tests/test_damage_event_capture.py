"""Synthetic damage-event recording tests; no game or process access required."""
import unittest

from practice.damage_event_capture import (
    DamageRecorder, DamageCaptureError, HP, CHARACTER, MAP, LOADING,
    TASK_POINTER, OBJECT_POINTER, candidate_report, event_timeline, export_report,
)


class FakeMemory:
    def __init__(self):
        self.data = {}
        self.read_count = 0
        self.write_count = 0
        self.put(LOADING, 0, 1)
        self.put(CHARACTER, 1, 4)
        self.put(MAP, 40, 2)
        self.put(HP, 12, 4)
        self.put(TASK_POINTER, 0x80169FA0, 4)
        self.put(OBJECT_POINTER, 0x80169A00, 4)

    def put(self, address, value, width):
        for i, byte in enumerate(value.to_bytes(width, "big")):
            self.data[address + i] = byte

    def read_guest(self, address, size):
        self.read_count += 1
        return bytes(self.data.get(address + i, 0) for i in range(size))

    def u8(self, address):
        return int.from_bytes(self.read_guest(address, 1), "big")

    def u16(self, address):
        return int.from_bytes(self.read_guest(address, 2), "big")

    def u32(self, address):
        return int.from_bytes(self.read_guest(address, 4), "big")


def take_hit(recorder, mem, start):
    for i in range(8):
        recorder.sample(start + i * 0.04)
    mem.put(HP, mem.u32(HP) - 1, 4)
    flag = 0x80169FA0 + 0x30
    mem.put(flag, 1, 1)
    recorder.sample(start + 0.35)
    for i in range(1, 96):
        if i == 55:
            mem.put(flag, 0, 1)
        recorder.sample(start + 0.35 + i * 0.04)


class DamageEventCaptureTests(unittest.TestCase):
    def test_repeatable_temporary_flag_ranked_and_health_excluded(self):
        mem = FakeMemory()
        rec = DamageRecorder(mem)
        take_hit(rec, mem, 0)
        self.assertEqual(len(rec.events), 1)
        self.assertTrue(rec.events[0].complete)
        take_hit(rec, mem, 10)
        ranked = candidate_report(rec.events)
        row = next(r for r in ranked if
                   r["address"] == "0x80169FD0" and r["type"] == "u8")
        self.assertEqual((row["hits"], row["returns"]), (2, 2))
        self.assertFalse(any(r["address"] == "0x8015C5E4" for r in ranked))
        timeline = event_timeline(rec.events[0], row)
        self.assertEqual(timeline[0]["value"], 0)
        self.assertTrue(any(v["value"] == 1 for v in timeline))
        exported = export_report(rec)
        self.assertEqual(exported["complete_events"], 2)
        self.assertTrue(exported["read_only"])
        self.assertGreater(mem.read_count, 0)
        self.assertEqual(mem.write_count, 0)

    def test_map_change_stops_recording(self):
        mem = FakeMemory()
        rec = DamageRecorder(mem)
        rec.sample(0)
        mem.put(MAP, 41, 2)
        with self.assertRaises(DamageCaptureError):
            rec.sample(0.04)
        self.assertTrue(rec.stopped)

    def test_character_or_pointer_change_stops_recording(self):
        mem = FakeMemory()
        rec = DamageRecorder(mem)
        rec.sample(0)
        mem.put(TASK_POINTER, 0x8016A000, 4)
        with self.assertRaises(DamageCaptureError):
            rec.sample(0.04)
        self.assertTrue(rec.stopped)

    def test_incomplete_hit_excluded_from_ranking(self):
        mem = FakeMemory()
        rec = DamageRecorder(mem)
        for i in range(5):
            rec.sample(i * 0.04)
        mem.put(HP, 11, 4)
        mem.put(0x80169FD0, 1, 1)
        rec.sample(0.21)
        rec.stop()
        self.assertEqual(len(rec.events), 1)
        self.assertFalse(rec.events[0].complete)
        self.assertEqual(candidate_report(rec.events), [])

    def test_loading_and_bad_pointer_refused(self):
        mem = FakeMemory()
        mem.put(LOADING, 1, 1)
        with self.assertRaises(DamageCaptureError):
            DamageRecorder(mem).sample(0)
        mem.put(LOADING, 0, 1)
        mem.put(TASK_POINTER, 0, 4)
        with self.assertRaises(DamageCaptureError):
            DamageRecorder(mem).sample(0)

    def test_maximum_event_count_stops_cleanly(self):
        mem = FakeMemory()
        rec = DamageRecorder(mem, max_events=1)
        take_hit(rec, mem, 0)
        self.assertTrue(rec.stopped)
        self.assertFalse(rec.sample(10))


if __name__ == "__main__":
    unittest.main()

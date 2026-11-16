"""Synthetic JP damage capture: uses native HP and scene with no task ptr."""
import unittest
from tests.test_japan_party_controller import Writer
from practice.japan_damage_capture import JapanDamageRecorder, JAPAN_HP_BYTE
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_LOADING, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER,
)
from practice.damage_event_capture import candidate_report, DamageCaptureError


class JapanDamageCaptureTests(unittest.TestCase):
    def setUp(self):
        self.writer=Writer()
        self.writer.set_guest(0x800CD000,bytes(0x600))
        self.writer.set_guest(0x80161D80,bytes(0x700))
        self.writer.set_guest(JAPAN_DEBUG_ENGINE_MODE,b'\x0d')
        self.writer.set_guest(JAPAN_DEBUG_LOADING,bytes(4))
        self.writer.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('0161'))
        self.writer.set_guest(JAPAN_DEBUG_CHARACTER,bytes(4))
        self.writer.set_guest(JAPAN_HP_BYTE,b'\x20')

    def test_japan_health_drop_records_event_without_us_pointers(self):
        rec=JapanDamageRecorder(
            self.writer.rdram(),post_seconds=0.25,max_events=1)
        self.assertTrue(rec.sample(now=0.0))
        self.assertTrue(rec.sample(now=0.04))
        self.writer.set_guest(JAPAN_HP_BYTE,b'\x1e')
        self.assertTrue(rec.sample(now=0.08))
        self.assertTrue(rec.sample(now=0.40))
        self.assertEqual(rec.samples,4)
        self.assertTrue(rec.stopped)
        self.assertEqual(len(rec.events),1)
        event=rec.events[0]
        self.assertEqual(event.baseline.hp,32)
        self.assertEqual(event.after[0].hp,30)
        self.assertEqual(event.before[-1].map_id,0x161)
        self.assertEqual(event.before[-1].pointers,(0,0))
        self.assertEqual(event.baseline.regions[1][1],0x80161D80)
        self.assertFalse(any(
            r['address']==f'0x{JAPAN_HP_BYTE:08X}'
            for r in candidate_report(rec.events)))

    def test_scene_or_loading_rejects_mixed_sample(self):
        rec=JapanDamageRecorder(self.writer.rdram())
        rec.sample(now=0.0)
        self.writer.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('0162'))
        with self.assertRaisesRegex(DamageCaptureError,'Scene, character'):
            rec.sample(now=0.1)
        other=JapanDamageRecorder(self.writer.rdram())
        self.writer.set_guest(JAPAN_DEBUG_LOADING,(1).to_bytes(4,'big'))
        with self.assertRaisesRegex(DamageCaptureError,'not in stable'):
            other.sample(now=0.2)


if __name__=='__main__':
    unittest.main()

"""Japanese Event Sessions reuse USA trial/ranking UI with JP evidence only."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from practice.event_sessions import (
    EVENT_START, JAPAN_CANDIDATE_START, capture_japan_event, new_session,
    with_trial, rank_bits, save_session, load_session,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
    JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
)
from tests.test_japan_party_controller import Writer


class JapanEventSessionsTests(unittest.TestCase):
    def setUp(self):
        self.writer=Writer()
        self.writer.set_guest(JAPAN_DEBUG_ENGINE_MODE,b'\x0d')
        self.writer.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('0161'))
        self.writer.set_guest(JAPAN_DEBUG_CHARACTER,bytes(4))
        self.writer.set_guest(JAPAN_DEBUG_LOADING,bytes(4))
        self.writer.set_guest(JAPAN_CANDIDATE_START,bytes(0x64))
        self.writer.writes.clear()

    def test_japan_capture_uses_own_source_and_no_usa_pointer(self):
        capture=capture_japan_event(self.writer.rdram())
        self.assertEqual(capture['context'],{
            'map_id':0x161,'character':0,'player_ptr':0,'task_ptr':0})
        self.assertEqual(len(capture['bytes_hex']),200)
        self.assertEqual(self.writer.writes,[])

    def test_japanese_bit_rank_address_and_roundtrip(self):
        ram=self.writer.rdram()
        a=capture_japan_event(ram)
        self.writer.set_guest(JAPAN_CANDIDATE_START,b'\x08')
        b=capture_japan_event(ram)
        session=new_session('Oedo dialogue','project64',
                            region='japan',event_start=JAPAN_CANDIDATE_START)
        session=with_trial(session,'event','A/B',{'A':a,'B':b})
        report=rank_bits(session)
        self.assertEqual(report['region'],'japan')
        self.assertEqual(report['event_start'],'0x80161D80')
        self.assertEqual(report['candidates'][0]['address'],'0x80161D80')
        self.assertEqual(report['candidates'][0]['mask'],'08')
        self.assertFalse(report['candidates'][0]['confirmed'])
        with TemporaryDirectory() as temp:
            path=Path(temp)/'japan_event.json'
            save_session(path,session)
            self.assertEqual(load_session(path),session)
        self.assertEqual(self.writer.writes,[])

    def test_region_cannot_reinterpret_us_bank_or_cross_read(self):
        with self.assertRaisesRegex(ValueError,'fixed'):
            new_session('USA', 'project64', region='usa',
                        event_start=JAPAN_CANDIDATE_START)
        with self.assertRaisesRegex(ValueError,'unsupported'):
            new_session('USA','mupen64plus',region='usa')
        with self.assertRaisesRegex(ValueError,'Invalid'):
            capture_japan_event(self.writer.rdram(),
                                event_start=0x807FFFE0)
        self.writer.set_guest(JAPAN_DEBUG_LOADING,b'\x00\x00\x00\x01')
        with self.assertRaisesRegex(ValueError,'stable gameplay'):
            capture_japan_event(self.writer.rdram())
        self.assertEqual(self.writer.writes,[])


if __name__=='__main__':
    unittest.main()

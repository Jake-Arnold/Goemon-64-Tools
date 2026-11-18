"""The shared session must never expose the inactive game's RAM reader."""
import unittest
from types import SimpleNamespace

from practice.region_session import RegionSession, active_session


class RegionSessionTests(unittest.TestCase):
    def test_selected_region_is_only_reader(self):
        usa = object()
        japan = object()
        app = SimpleNamespace(
            active_version=SimpleNamespace(key='usa'),
            mem=usa, jp_rdram=japan, game_pid=321,
            connection_target=SimpleNamespace(get=lambda: 'recomp'),
            jp_backend='project64')
        session = active_session(app)
        self.assertIs(session.reader, usa)
        self.assertEqual((session.region, session.backend), ('usa', 'recomp'))
        app.active_version.key = 'japan'
        session = active_session(app)
        self.assertIs(session.reader, japan)
        self.assertEqual((session.region, session.backend), ('japan', 'project64'))

    def test_disconnected_is_read_only(self):
        session = RegionSession('usa', None, None, None)
        self.assertFalse(session.connected)
        self.assertFalse(hasattr(session, 'write_guest'))
        with self.assertRaises(RuntimeError):
            session.read_guest(0x80000000, 1)

    def test_active_session_rejects_unknown_region(self):
        app = SimpleNamespace(active_version=SimpleNamespace(key='other'))
        with self.assertRaises(ValueError):
            active_session(app)


if __name__ == '__main__':
    unittest.main()

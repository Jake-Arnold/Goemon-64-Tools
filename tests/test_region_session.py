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

    def test_native_current_scene_uses_only_selected_region_global(self):
        class Reader:
            def __init__(self, values):
                self.values = values
                self.calls = []
            def read_guest(self, address, length):
                self.calls.append((address, length))
                return self.values[(address, length)]
        usa = Reader({(0x800C7AB2, 2): b'\x01\x61'})
        japan = Reader({(0x800CD2A2, 2): b'\x01\x61'})
        app = SimpleNamespace(
            active_version=SimpleNamespace(key='usa'),
            mem=usa, jp_rdram=japan, game_pid=1,
            connection_target=SimpleNamespace(get=lambda: 'recomp'),
            jp_backend='project64')
        session = active_session(app)
        self.assertEqual(session.read_current_scene(), 0x161)
        self.assertEqual(usa.calls, [(0x800C7AB2, 2)])
        self.assertEqual(japan.calls, [])
        app.active_version.key = 'japan'
        self.assertEqual(active_session(app).read_current_scene(), 0x161)
        self.assertEqual(japan.calls, [(0x800CD2A2, 2)])

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

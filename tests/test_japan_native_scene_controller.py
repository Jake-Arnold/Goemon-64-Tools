"""Synthetic shared-browser Japanese native warp sequence, no live emulator."""
import struct
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit
from practice.japan_native_scene_warp import (
    JAPAN_MENU_CATEGORY, JAPAN_MENU_STAGE_INDEX,
)
from practice.japanese_debug_warp import (
    JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
)
from practice.japanese_position import JAPAN_PLAYER_XYZ_START
from tests.test_japan_debug_menu_controller import screen
from tests.test_japan_party_controller import Writer, Label


def make_controller():
    writer = Writer()
    source = screen(writer, scene=0x161)
    app = object.__new__(Toolkit)
    app.__dict__.update(source.__dict__)
    app.jp_auto_warp = None
    app.jp_native_key_release = None
    app.jp_warp_a_key = SimpleNamespace(get=lambda: 'X')
    app.selected_japan_debug_scene = lambda: 0x1D1
    app._japan_native_warp_writer = lambda: (writer, writer.rdram())
    app.scene_status = Label()
    scheduled = []
    app.root = SimpleNamespace(
        after=lambda ms, callback: scheduled.append((ms, callback)))
    return app, writer, scheduled


class JapanFullNativeSceneControllerTests(unittest.TestCase):
    def test_browser_target_auto_stages_and_sends_a_then_observes_loaded_map(self):
        app, writer, scheduled = make_controller()
        pressed = []
        with patch('practice.toolkit.press_project64_native_a',
                   side_effect=lambda pid, key: (
                       pressed.append((pid, key)) or
                       (lambda: pressed.append(('release', key))))):
            app.start_japan_native_scene_warp(destination=0x1D1)
            self.assertIsNotNone(app.jp_auto_warp)
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE,1), b'\x0a')
            # No direct scene write. Actual game still reports source map.
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_DEBUG_SCENE,2),
                bytes.fromhex('0161'))
            app.jp_auto_warp['started'] = time.monotonic() - 2
            app.poll_japan_native_scene_warp(time.monotonic())
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_MENU_CATEGORY,1), b'\x04')
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_MENU_STAGE_INDEX,2),
                bytes.fromhex('0041'))
            app.poll_japan_native_scene_warp(time.monotonic() + 0.6)
            self.assertEqual(pressed, [(959604, 'X')])
            self.assertEqual(len(scheduled),1)
            app._release_japan_native_key()
            self.assertEqual(pressed[-1], ('release','X'))
            # Simulate engine-owned load into requested map and valid XYZ.
            writer.set_guest(JAPAN_DEBUG_ENGINE_MODE,b'\x0d')
            writer.set_guest(JAPAN_DEBUG_SCENE,bytes.fromhex('01d1'))
            writer.set_guest(
                JAPAN_PLAYER_XYZ_START,
                struct.pack('>fff', 5.0, 0.0, -10.0))
            for _ in range(3):
                app.poll_japan_native_scene_warp(time.monotonic()+0.8)
            self.assertIsNone(app.jp_auto_warp)
            self.assertIn('Native scene warp loaded',app.scene_status.value)

    def test_stale_menu_selection_suppresses_a(self):
        app, writer, _scheduled = make_controller()
        with patch('practice.toolkit.press_project64_native_a') as press:
            app.start_japan_native_scene_warp(destination=0x1D1)
            app.jp_auto_warp['started'] = time.monotonic()-2
            app.poll_japan_native_scene_warp(time.monotonic())
            writer.set_guest(JAPAN_MENU_STAGE_INDEX,bytes.fromhex('0000'))
            app.poll_japan_native_scene_warp(time.monotonic()+0.6)
        press.assert_not_called()
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('overwrote',app.scene_status.value)

    def test_start_failure_has_no_pending_warp_or_scene_change(self):
        app, writer, _scheduled=make_controller()
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE,b'\x0a')
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('refused',app.scene_status.value)
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_SCENE,2),
            bytes.fromhex('0161'))


if __name__=='__main__':
    unittest.main()

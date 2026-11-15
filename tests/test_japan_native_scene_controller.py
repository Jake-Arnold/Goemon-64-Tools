"""Synthetic shared Scene Browser instant Japan 0x0C reload controller tests."""
import struct
import time
from unittest.mock import patch
import unittest

from practice.toolkit import Toolkit
from practice.japan_direct_scene_reload import JAPAN_PENDING_MAP
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
    app.selected_japan_debug_scene = lambda: 0x1D1
    app._japan_native_warp_writer = lambda: (writer, writer.rdram())
    app.scene_status = Label()
    return app, writer


class JapanFullNativeSceneControllerTests(unittest.TestCase):
    def test_doubleclick_requests_immediate_0x0c_without_menu_or_a(self):
        app, writer = make_controller()
        with patch('practice.toolkit.enter_japan_native_debug_menu') as menu, \
             patch('practice.japan_project64_input.press_project64_native_a') as press:
            app.start_japan_native_scene_warp(destination=0x1D1)
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_PENDING_MAP, 2),
                bytes.fromhex('01D1'))
            self.assertEqual(
                writer.rdram().read_guest(JAPAN_DEBUG_SCENE, 2),
                bytes.fromhex('0161'))
            self.assertIsNotNone(app.jp_auto_warp)
            self.assertIn('instant reload', app.scene_status.value)
            menu.assert_not_called()
            press.assert_not_called()
        self.assertEqual(writer.close_count, 1)

        # A fast game can complete the 0x0C state before a 170ms Tk tick.
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE, b'\x0d')
        writer.set_guest(JAPAN_DEBUG_SCENE, bytes.fromhex('01d1'))
        writer.set_guest(
            JAPAN_PLAYER_XYZ_START,
            struct.pack('>fff', 5.0, 0.0, -10.0))
        for _ in range(3):
            app.poll_japan_native_scene_warp(time.monotonic())
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('Japan scene reload reached', app.scene_status.value)

    def test_pending_warp_never_opens_native_menu_or_injects_a(self):
        app, writer = make_controller()
        app.start_japan_native_scene_warp(destination=0x1D1)
        app.poll_japan_native_scene_warp(time.monotonic())
        self.assertTrue(app.jp_auto_warp['seen_reload'])
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')
        app.start_japan_native_scene_warp(destination=0x161)
        self.assertIn('pending', app.scene_status.value)

    def test_direct_reload_entrance_when_unique_source_route_exists(self):
        app, writer = make_controller()
        app.entrance_atlas = {'payload': {'entries': [{
            'id': '161:001', 'kind': 'exit', 'source_map': 0x161,
            'destination': 0x1D1, 'position': [4, 8, -10],
            'heading': 512, 'mode': 0x10, 'exit_id': 1,
        }]}}
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertEqual(app.jp_auto_warp['spawn'].position, (4, 8, -10))
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_PENDING_MAP, 12),
            app.jp_auto_warp['spawn'].pending_bytes())
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')

    def test_start_failure_has_no_pending_warp_or_scene_change(self):
        app, writer = make_controller()
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE, b'\x0a')
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('refused', app.scene_status.value)
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_SCENE, 2),
            bytes.fromhex('0161'))

    def test_explicit_original_debug_menu_remains_separate(self):
        app, writer = make_controller()
        with patch('practice.toolkit.enter_japan_native_debug_menu') as menu:
            app.start_japan_native_scene_warp(destination=0x1D1)
        menu.assert_not_called()
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')


if __name__ == '__main__':
    unittest.main()

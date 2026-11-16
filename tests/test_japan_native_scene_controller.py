"""Synthetic shared Scene Browser instant Japan 0x0C reload controller tests."""
import struct
from types import SimpleNamespace
import time
from unittest.mock import patch
import unittest

from practice.toolkit import Toolkit
from practice.japan_direct_scene_reload import JAPAN_PENDING_MAP
from practice.entrances import Spawn
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
    app.jp_warp_spawns = {}
    app.selected_scene_spawn = lambda destination: Spawn(
        destination, (4, 8, -10), heading=512, mode=0x10,
        label='Original USA entrance', entrance_id='usa:shared')
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
        self.assertIn('USA entrance usa:shared', app.scene_status.value)

    def test_japan_character_selection_stages_yae_before_reload(self):
        app, writer = make_controller()
        app.scene_character = SimpleNamespace(current=lambda: 4)  # JP selector index
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertEqual(
            writer.rdram().read_guest(0x80161DCC, 4),
            bytes.fromhex('00000003'))
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1),
            bytes((12,)))
        self.assertEqual(app.jp_auto_warp['target_character'], 3)
        self.assertIn('Target character 3 staged', app.scene_status.value)

    def test_pending_warp_never_opens_native_menu_or_injects_a(self):
        app, writer = make_controller()
        app.start_japan_native_scene_warp(destination=0x1D1)
        app.poll_japan_native_scene_warp(time.monotonic())
        self.assertTrue(app.jp_auto_warp['seen_reload'])
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')
        app.start_japan_native_scene_warp(destination=0x161)
        self.assertIn('pending', app.scene_status.value)

    def test_japan_warp_stages_exact_selected_usa_entrance(self):
        app, writer = make_controller()
        selected = Spawn(
            0x1D1, (40, 8, -10), heading=512, mode=0x20,
            label='USA selected from 161', entrance_id='usa:161:exit:1')
        app.selected_scene_spawn = lambda dest: selected
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertEqual(app.jp_auto_warp['spawn'], selected)
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_PENDING_MAP, 12),
            selected.pending_bytes())
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1),
            bytes((12,)))
        self.assertIn('Shared USA entrance', app.scene_status.value)
        self.assertIn('USA entrance', app.scene_status.value)

    def test_japan_postload_places_exact_usa_xyz_once(self):
        app, writer = make_controller()
        selected = Spawn(
            0x1D1, (100, 5, 200), label='USA same coords',
            entrance_id='usa:shared')
        app.selected_scene_spawn = lambda dest: selected
        app.start_japan_native_scene_warp(destination=0x1D1)
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE, bytes((13,)))
        writer.set_guest(JAPAN_DEBUG_SCENE, bytes.fromhex('01D1'))
        writer.set_guest(
            JAPAN_PLAYER_XYZ_START,
            struct.pack('>fff', 5.0, 0.0, -10.0))
        writer.writes.clear()
        for _ in range(3):
            app.poll_japan_native_scene_warp(time.monotonic())
        self.assertIsNone(app.jp_auto_warp)
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_PLAYER_XYZ_START, 12),
            struct.pack('>fff', *selected.position))
        self.assertEqual(len(writer.writes), 1)
        self.assertIn('USA entrance usa:shared', app.scene_status.value)
        self.assertIn('JP actual (100.0, 5.0, 200.0)', app.scene_status.value)

    def test_japan_warp_refuses_if_selected_usa_entrance_is_missing(self):
        app, writer = make_controller()
        def missing(_destination):
            raise ValueError('Load original USA ROM entrance data first')
        app.selected_scene_spawn = missing
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('Load original USA ROM', app.scene_status.value)
        self.assertEqual(writer.writes, [])

    def test_other_character_does_not_write_unmapped_japanese_xyz(self):
        app, writer = make_controller()
        app.start_japan_native_scene_warp(destination=0x1D1)
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE, bytes((13,)))
        writer.set_guest(JAPAN_DEBUG_SCENE, bytes.fromhex('01D1'))
        writer.set_guest(0x80161DCC, (3).to_bytes(4, 'big'))
        writer.set_guest(
            JAPAN_PLAYER_XYZ_START,
            struct.pack('>fff', 500.0, 0.0, 200.0))
        writer.writes.clear()
        for _ in range(3):
            app.poll_japan_native_scene_warp(time.monotonic())
        self.assertIsNone(app.jp_auto_warp)
        self.assertEqual(writer.writes, [])
        self.assertIn('not Goemon', app.scene_status.value)

    def test_capture_current_japan_xyz_persists_without_game_writes(self):
        app, writer = make_controller()
        writer.set_guest(
            JAPAN_PLAYER_XYZ_START,
            struct.pack('>fff', -289.0, 0.0, -167.0))
        writer.writes.clear()
        with patch('practice.toolkit.save_japan_spawn') as save:
            app.capture_japan_warp_spawn()
        save.assert_called_once()
        self.assertEqual(
            app.jp_warp_spawns[0x161].position, (-289.0, 0.0, -167.0))
        self.assertEqual(writer.writes, [])
        self.assertIn('Captured JP scene', app.scene_status.value)


    def test_start_failure_has_no_pending_warp_or_scene_change(self):
        app, writer = make_controller()
        writer.set_guest(JAPAN_DEBUG_ENGINE_MODE, b'\x0a')
        app.start_japan_native_scene_warp(destination=0x1D1)
        self.assertIsNone(app.jp_auto_warp)
        self.assertIn('refused', app.scene_status.value)
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_SCENE, 2),
            bytes.fromhex('0161'))

    def test_new_scene_only_optin_allows_revalidated_writer(self):
        from unittest.mock import patch
        app, writer = make_controller()
        app.args.enable_japan_debug_menu_writes = False
        app.args.enable_japan_scene_writes = True
        # Exercise the actual live-writer guard, not the synthetic shortcut.
        del app._japan_native_warp_writer
        with patch('practice.toolkit.sys.platform', 'win32'), \
             patch('practice.toolkit.verified_emulator_pid',
                   return_value=(959604, 'project64')), \
             patch('practice.toolkit.verified_japan_probes',
                   return_value=('verified',)), \
             patch('practice.toolkit.HostProcess',
                   return_value=writer), \
             patch('practice.toolkit.validate_rdram_base',
                   return_value=writer.rdram()):
            handle, verified = Toolkit._japan_native_warp_writer(app)
        self.assertIs(handle, writer)
        self.assertEqual(verified.read_guest(JAPAN_DEBUG_ENGINE_MODE,1),
                         b'\x0d')
        handle.close()
        self.assertEqual(writer.close_count,1)
        self.assertEqual(writer.writes,[])

    def test_new_scene_optin_refuses_readonly(self):
        app, writer = make_controller()
        app.args.enable_japan_scene_writes = True
        app.args.enable_japan_debug_menu_writes = False
        app.args.read_only = True
        del app._japan_native_warp_writer
        with patch('practice.toolkit.HostProcess') as handle:
            with self.assertRaisesRegex(RuntimeError, 'requires'):
                Toolkit._japan_native_warp_writer(app)
        handle.assert_not_called()

    def test_explicit_original_debug_menu_remains_separate(self):
        app, writer = make_controller()
        with patch('practice.toolkit.enter_japan_native_debug_menu') as menu:
            app.start_japan_native_scene_warp(destination=0x1D1)
        menu.assert_not_called()
        self.assertEqual(
            writer.rdram().read_guest(JAPAN_DEBUG_ENGINE_MODE, 1), b'\x0c')


if __name__ == '__main__':
    unittest.main()

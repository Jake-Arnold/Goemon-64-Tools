"""Game-version read models: same navigation, distinct source-backed RAM."""
import struct
from types import SimpleNamespace
import unittest

from practice.region_views import (
    japan_live_watches, japan_unlock_fields, japan_story_fields,
)
from practice.entrance_ui import EntranceMixin
from practice.scenes import SCENES
from practice.ui_extension import InspectorMixin
from tests.test_japanese_fields import FakeRam


class Message:
    def __init__(self):
        self.value = ''
    def set(self, value):
        self.value = value


class SelectedList:
    def curselection(self):
        return (0,)


class RegionReadTests(unittest.TestCase):
    def test_shared_live_memory_reads_japanese_guest_addresses_not_usa(self):
        ram = FakeRam({
            (0x80161DDA, 2): bytes.fromhex('04d2'),
            (0x800CD2A2, 2): bytes.fromhex('0161'),
            (0x80151B10, 12): struct.pack('>fff', -289.0, 0.0, -167.0),
        })
        rows = japan_live_watches(ram)
        ryo = next(r for r in rows if r.addr == 0x80161DDA)
        self.assertEqual(ryo.value, '1234')
        self.assertEqual(ryo.raw, '04D2')
        xyz = [r for r in rows if r.name.startswith('Player position')]
        self.assertEqual([r.addr for r in xyz],
                         [0x80151B10, 0x80151B14, 0x80151B18])
        self.assertEqual([r.value for r in xyz],
                         ['-289.0000', '0.0000', '-167.0000'])
        self.assertNotIn((0x8015C5DC, 4), ram.reads)
        self.assertNotIn((0x8015C6A7, 1), ram.reads)

    def test_unlock_and_story_use_japan_field_catalogue(self):
        unlocks = {r.key: r.address for r in japan_unlock_fields()}
        story = {r.key: r.address for r in japan_story_fields()}
        self.assertEqual(unlocks['sasuke_party'], 0x80161E97)
        self.assertEqual(unlocks['yae_party'], 0x80161E9B)
        self.assertEqual(unlocks['ryo'], 0x80161DDA)
        self.assertEqual(story['world_map_access'], 0x80162063)
        self.assertNotIn(0x8015C6A7, unlocks.values())
        self.assertNotIn(0x80168E90, story.values())

    def test_japan_scene_catalog_ignores_usa_only_atlas_entries(self):
        host = SimpleNamespace(
            active_version=SimpleNamespace(key='japan'),
            entrance_atlas={'payload': {'rooms': [0x7F1]}})
        catalog = EntranceMixin.scene_catalog(host)
        self.assertEqual(catalog, SCENES)
        host.active_version.key = 'usa'
        self.assertIn(0x7F1, EntranceMixin.scene_catalog(host))

    def test_shared_scene_doubleclick_uses_native_japan_warp_not_manual_menu(self):
        commands = []
        host = SimpleNamespace(
            active_version=SimpleNamespace(key='japan'),
            scene_list=SelectedList(),
            scene_options=[(0x1D1, "Goemon's House")],
            scene_status=Message(),
            start_japan_native_scene_warp=lambda destination:
                commands.append(('warp', destination)),
        )
        InspectorMixin.try_reload_warp(host)
        self.assertEqual(commands, [('warp', 0x1D1)])
        # The manual debug button is a different command.
        host.open_japan_debug_for_selected_scene = (
            lambda: commands.append(('manual', None)))
        InspectorMixin.enter_debug_menu(host)
        self.assertEqual(commands[-1], ('manual', None))

    def test_usa_scene_reload_path_remains_separate(self):
        calls=[]
        host=SimpleNamespace(
            active_version=SimpleNamespace(key='usa'),
            scene_list=SelectedList(),
            scene_options=[(0x161, 'Oedo Town South')],
            scene_status=Message(),
            try_reload_warp=lambda: calls.append('usa reload'),
        )
        InspectorMixin.request_direct_scene(host, 0x161, 'Oedo Town South')
        self.assertEqual(calls, ['usa reload'])


if __name__ == '__main__':
    unittest.main()

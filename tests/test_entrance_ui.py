import copy
import tempfile
from pathlib import Path
import tkinter as tk
import unittest
from unittest.mock import patch

from practice.toolkit import Toolkit,parse_args
from practice.entrances import digest,Spawn
from practice.checkpoints import MAP_ADDR,STATE_ADDR
import tests.test_checkpoint as checkpoint_fixture
from tests.test_entrances import atlas_fixture


class EntranceUITests(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk();self.root.withdraw()
        with patch('practice.entrance_ui.load_atlas',return_value=atlas_fixture()):
            self.app=Toolkit(self.root,parse_args(['--game-version','usa']))
        self.process,self.app.mem=checkpoint_fixture.TestCheckpoint().sample()
        self.app.mem.write_guest(MAP_ADDR,(1).to_bytes(2,'big'))
        self.app.current=self.app.mem.snapshot()
        self.app.scene_options=[(2,'Synthetic destination')]
        self.app.scene_list.delete(0,'end');self.app.scene_list.insert('end','2: Synthetic destination');self.app.scene_list.selection_set(0)
        self.app.refresh_entrance_choices(2)

    def tearDown(self):
        for callback in self.root.tk.call('after','info'):
            try:self.root.after_cancel(callback)
            except tk.TclError:pass
        self.root.destroy()

    def test_unique_origin_entry_is_selected_and_request_stages_xyz(self):
        self.assertEqual(self.app.entrance_choice.current(),0)
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):self.app.try_reload_warp()
        self.assertEqual(self.app.mem.u8(STATE_ADDR),12)
        self.assertEqual(self.app.mem.read_guest(0x800C7CA4,6),b'\xff\xf6\x00\x14\x00\x1e')
        pending=self.app.pending_direct_warp
        self.app.entrance_choice.set('')
        self.assertEqual(pending['placement'].spawn.position,(-10,20,30))
        self.app.mem.write_guest(MAP_ADDR,b'\x00\x02');self.app.mem.write_guest(STATE_ADDR,b'\x0D')
        with patch.object(self.app,'_save_direct_warp_diagnostics',return_value='synthetic report'):
            self.app.poll_direct_warp(pending['start_at']+.2);self.app.poll_direct_warp(pending['start_at']+.4)
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertEqual(tuple(self.app.mem.snapshot()[k] for k in ('x','y','z')),(-10,20,30))

    def test_ambiguous_unrelated_entry_requires_explicit_choice(self):
        atlas=copy.deepcopy(atlas_fixture());row=copy.deepcopy(atlas['payload']['entries'][0]);row['id']='other';row['position']=[1,2,3]
        atlas['payload']['entries'].append(row);atlas['sha256']=digest(atlas['payload'])
        self.app.entrance_atlas=atlas;self.app.entrance_choice.set('');self.app.mem.write_guest(MAP_ADDR,b'\x00\x23')
        self.app.refresh_entrance_choices(2)
        self.assertEqual(self.app.entrance_choice.current(),-1)
        with patch.object(self.process,'write',side_effect=AssertionError('No game writes')):self.app.try_reload_warp()
        self.assertIsNone(self.app.pending_direct_warp)
        self.assertIn('Choose',self.app.scene_status.get())

    def test_missing_atlas_and_disabled_position_restoration_do_not_request_reload(self):
        self.app.entrance_atlas=None
        with patch.object(self.process,'write',side_effect=AssertionError('No writes')):self.app.try_reload_warp()
        self.assertIn('Load original',self.app.scene_status.get())
        self.app.args.enable_teleport=False
        with patch.object(self.process,'write',side_effect=AssertionError('No writes')):self.app.try_reload_warp()
        self.assertIn('disabled',self.app.scene_status.get())

    def test_native_manual_request_also_places_after_actual_load(self):
        self.app.debug_shortcut_confirmed=True
        with patch('practice.ui_extension.calibrated_for_direct_warp',return_value=False), \
             patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):
            self.app.open_debug_for_selected_scene()
        self.assertEqual(self.app.mem.u8(STATE_ADDR),10)
        pending=self.app.pending_native_warp;self.assertTrue(pending['manual'])
        self.app.poll_native_warp_menu(pending['start_at'])
        self.app.mem.write_guest(MAP_ADDR,b'\x00\x02');self.app.mem.write_guest(STATE_ADDR,b'\x0D')
        self.app.poll_native_warp_menu(pending['start_at']+.2);self.app.poll_native_warp_menu(pending['start_at']+.4)
        self.assertIsNone(self.app.pending_native_warp)
        self.assertEqual(self.app.mem.snapshot()['x'],-10)

    def test_cancel_and_read_only_pending_requests_cannot_place(self):
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):self.app.try_reload_warp()
        self.app.cancel_scene_request();self.assertIsNone(self.app.pending_direct_warp)
        self.assertIsNone(self.app.pending_native_warp)
        self.app.args.read_only=True
        self.app.pending_direct_warp={'anything':'not accessed'}
        with patch.object(self.process,'write',side_effect=AssertionError('No writes')):self.app.poll_direct_warp(1)
        self.assertIsNone(self.app.pending_direct_warp)

    def test_known_oedo_coordinates_work_without_any_rom_in_both_regions(self):
        from practice.game_versions import VERSIONS
        self.app.entrance_atlas = None
        self.app.entrance_choice.set('')
        self.app.refresh_entrance_choices(0x161)
        usa = self.app.selected_scene_spawn(0x161)
        self.assertEqual(usa.position, (-289.0, 0.0, -167.0))
        self.assertIn('Staged before reload', self.app.entrance_note.get())

        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.refresh_entrance_choices(0x161)
        japan = self.app.selected_scene_spawn(0x161)
        self.assertEqual(japan.pending_bytes(), usa.pending_bytes())
        self.assertEqual(japan.entrance_id, usa.entrance_id)

    def test_validated_legacy_atlas_migrates_to_durable_user_settings(self):
        from practice.entrance_ui import EntranceMixin
        from practice.entrances import load_atlas, save_atlas
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            legacy = folder / 'entrances.json'
            persistent = folder / 'xdg-config' / 'entrance-coordinates.json'
            atlas = atlas_fixture()
            save_atlas(legacy, atlas)
            with patch('practice.entrance_ui.stored_entrance_atlas_path',
                       return_value=persistent), \
                 patch('practice.entrance_ui.repository_entrance_atlas_path',
                       return_value=folder / 'missing-bundled.json'), \
                 patch('practice.entrance_ui.practice_data_dir',
                       return_value=folder):
                first = EntranceMixin()
                first.init_entrances()
                self.assertEqual(first.entrance_atlas, atlas)
                self.assertEqual(load_atlas(persistent), atlas)
                legacy.unlink()
                second = EntranceMixin()
                second.init_entrances()
                self.assertEqual(second.entrance_atlas, atlas)

    def test_repository_bundled_entrance_table_wins_over_local_cache(self):
        from practice.entrance_ui import EntranceMixin
        from practice.entrances import save_atlas
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bundled = folder / 'repo' / 'entrance-coordinates.json'
            local = folder / 'xdg' / 'entrance-coordinates.json'
            atlas = atlas_fixture()
            save_atlas(bundled, atlas)
            changed = copy.deepcopy(atlas)
            changed['payload']['entries'][0]['position'] = [7, 8, 9]
            changed['sha256'] = digest(changed['payload'])
            save_atlas(local, changed)
            with patch('practice.entrance_ui.repository_entrance_atlas_path',
                       return_value=bundled), \
                 patch('practice.entrance_ui.stored_entrance_atlas_path',
                       return_value=local), \
                 patch('practice.entrance_ui.practice_data_dir',
                       return_value=folder):
                host = EntranceMixin()
                host.init_entrances()
                self.assertEqual(host.entrance_atlas, atlas)
                self.assertEqual(host.entrance_atlas_source, 'repository')

    def test_invalid_checked_in_entrance_table_falls_back_to_valid_user_cache(self):
        from practice.entrance_ui import EntranceMixin
        from practice.entrances import save_atlas
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bundled = folder / 'repo' / 'entrance-coordinates.json'
            bundled.parent.mkdir()
            bundled.write_text('invalid file', encoding='utf-8')
            local = folder / 'xdg' / 'entrance-coordinates.json'
            atlas = atlas_fixture()
            save_atlas(local, atlas)
            with patch('practice.entrance_ui.repository_entrance_atlas_path',
                       return_value=bundled), \
                 patch('practice.entrance_ui.stored_entrance_atlas_path',
                       return_value=local), \
                 patch('practice.entrance_ui.practice_data_dir',
                       return_value=folder):
                host = EntranceMixin()
                host.init_entrances()
                self.assertEqual(host.entrance_atlas, atlas)
                self.assertEqual(host.entrance_atlas_source,
                                 'persistent user cache')

    def test_failed_rom_load_preserves_previous_atlas(self):
        old=self.app.entrance_atlas
        self.app.entrance_results.put(('error','incorrect ROM'))
        self.app.poll_entrance_rom()
        self.assertIs(self.app.entrance_atlas,old)
        self.assertIn('incorrect ROM',self.app.entrance_note.get())

    def test_japan_uses_same_usa_entrance_for_matching_source_scene(self):
        from practice.game_versions import VERSIONS
        from tests.test_japanese_fields import FakeRam
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.entrance_atlas=atlas_fixture()
        self.app.jp_rdram=FakeRam({
            (0x800CD2A2,2): (1).to_bytes(2,'big')})
        self.app.refresh_entrance_choices(2)
        spawn=self.app.selected_scene_spawn(2)
        self.assertEqual(spawn.position,(-10,20,30))
        self.assertEqual(spawn.pending_bytes(),
                         Spawn(2,(-10,20,30),spawn.heading,spawn.mode).pending_bytes())
        self.assertNotEqual(self.app.entrance_box.winfo_manager(),'')

    def test_japan_uses_same_default_fallback_when_source_unrelated(self):
        from practice.game_versions import VERSIONS
        from tests.test_japanese_fields import FakeRam
        atlas=copy.deepcopy(atlas_fixture())
        row=copy.deepcopy(atlas['payload']['entries'][0])
        row.update(id='default:2',kind='default',source_map=None,
                   source_file=None,position=[40,50,60])
        atlas['payload']['entries'].append(row)
        atlas['sha256']=digest(atlas['payload'])
        self.app.game_version_choice.set(VERSIONS['japan'].label)
        self.app.on_game_version_changed()
        self.app.entrance_atlas=atlas
        self.app.jp_rdram=FakeRam({
            (0x800CD2A2,2):(0x23).to_bytes(2,'big')})
        self.app.refresh_entrance_choices(2)
        self.assertEqual(self.app.selected_scene_spawn(2).position,
                         (40,50,60))

    def test_native_default_is_used_when_origin_has_no_unique_route(self):
        atlas=copy.deepcopy(atlas_fixture());row=copy.deepcopy(atlas['payload']['entries'][0])
        row.update(id='default:2',kind='default',source_map=None,source_file=None,position=[40,50,60])
        atlas['payload']['entries'].append(row);atlas['sha256']=digest(atlas['payload'])
        self.app.entrance_atlas=atlas;self.app.entrance_choice.set('');self.app.mem.write_guest(MAP_ADDR,b'\x00\x23')
        self.app.refresh_entrance_choices(2)
        self.assertEqual(self.app.selected_scene_spawn(2).position,(40,50,60))

    def test_scene_request_blocks_overlapping_checkpoint_restore(self):
        from practice.checkpoints import capture_checkpoint
        checkpoint=capture_checkpoint(self.app.mem,'Before reload')
        self.app.checkpoints=[checkpoint];self.app.checkpoints_box['values']=['Before reload'];self.app.checkpoints_box.current(0)
        with patch('practice.ui_extension.messagebox.askyesno',side_effect=AssertionError('No confirmation expected')):self.app.try_reload_warp()
        # An unexpected failure to stage the USA warp must fail fast rather
        # than display a hidden Tk modal under Xvfb and hang the whole suite.
        self.assertIsNotNone(self.app.pending_direct_warp,
                             'Expected USA warp; check selected test region')
        with patch.object(self.process,'write',side_effect=AssertionError('No second transition')), \
             patch('practice.toolkit.messagebox.askyesno',
                   side_effect=AssertionError('Hidden checkpoint modal forbidden')):
            self.app.restore_full_checkpoint()
        self.assertIn('scene request',self.app.status.get())

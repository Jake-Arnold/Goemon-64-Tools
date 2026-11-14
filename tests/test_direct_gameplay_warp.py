"""Regression tests: v0.9.7's exit flag must never be written for warp."""
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from practice.ui_extension import InspectorMixin
from practice.scene_controls import (request_scene_warp, PENDING_MAP_ADDR, EXIT_REQUEST_ADDR)
from practice.checkpoints import MAP_ADDR, STATE_ADDR
from tests.test_scene_warp import TestWarp

class Display:
    def __init__(self):self.text=''
    def set(self,text):self.text=text

class TestGameplayDirectWarp(unittest.TestCase):
    def test_exit_path_blocked_with_no_writes(self):
        ram=TestWarp().make()
        addresses=[(PENDING_MAP_ADDR,2),(EXIT_REQUEST_ADDR,1),(MAP_ADDR,2),(STATE_ADDR,1)]
        before=[ram.read_guest(a,n) for a,n in addresses]
        with patch.object(ram, 'write_guest', wraps=ram.write_guest) as write_guest:
            with self.assertRaisesRegex(RuntimeError,'Direct warp disabled'):
                request_scene_warp(ram,465,{465:'House'})
            write_guest.assert_not_called()
        self.assertEqual(before,[ram.read_guest(a,n) for a,n in addresses])

    def test_ui_double_click_does_not_write(self):
        ram=TestWarp().make()
        addresses=[(PENDING_MAP_ADDR,2),(EXIT_REQUEST_ADDR,1),(MAP_ADDR,2),(STATE_ADDR,1)]
        before=[ram.read_guest(a,n) for a,n in addresses]
        ui=SimpleNamespace(mem=ram,scene_status=Display())
        with patch.object(ram, 'write_guest', wraps=ram.write_guest) as write_guest:
            InspectorMixin.request_direct_scene(ui,465,'House')
            write_guest.assert_not_called()
        self.assertIn('DISABLED',ui.scene_status.text)
        self.assertEqual(before,[ram.read_guest(a,n) for a,n in addresses])

if __name__=='__main__':unittest.main()

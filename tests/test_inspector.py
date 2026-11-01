import unittest
from autosplitter.memory import Rdram
from tests.test_checkpoint import TestCheckpoint
from practice.inspector import get_watches, checkpoint_differences
from practice.checkpoints import capture_checkpoint, MAP_ADDR, PHASE_ADDR, GAMEDATA_ADDR
from practice.scenes import SCENES, scene_label
from practice.scene_controls import open_native_debug_menu


class TestInspector(unittest.TestCase):
    def sample(self):
        return TestCheckpoint().sample()

    def test_live_resources_and_inventory(self):
        proc, ram=self.sample()
        ram.write_guest(0x8015C6BF, b'\x01')
        ram.write_guest(0x8015C5F3, b'\x03')
        rows={r.name:r for r in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(rows['Ryo'].raw,'0x00000064')
        self.assertEqual(rows['Lives'].value,'3')
        self.assertEqual(rows['Chain Pipe'].raw,'0x01')
        self.assertEqual(rows['Item slot 1 code'].value,'3')
        self.assertEqual(rows['Selected item (currently equipped)'].status,'UNKNOWN')
        self.assertEqual(rows['Map ID'].raw,'0x0023')

    def test_invalid_resource_flags_not_silently_accepted(self):
        _, ram=self.sample()
        ram.write_guest(0x8015C5E8,(12000).to_bytes(4,'big'))
        ram.write_guest(0x8015C69F,b'\xAA')
        watches={w.name:w for w in get_watches(ram,ram.snapshot(),SCENES)}
        self.assertEqual(watches['Ryo'].status,'CHECK')
        self.assertEqual(watches['Goemon in party'].status,'CHECK')

    def test_checkpoint_differences_and_stale_mirror(self):
        _,ram=self.sample()
        checkpoint=capture_checkpoint(ram,'test')
        ram.write_guest(GAMEDATA_ADDR + 0x70,b'\x11') # stale mirror, ignored
        comparison=checkpoint_differences(ram,checkpoint)
        self.assertEqual(comparison['total'],0)
        ram.write_guest(GAMEDATA_ADDR+0x140,b'\xAA')
        comparison=checkpoint_differences(ram,checkpoint)
        self.assertEqual(comparison['counts']['gamedata'],1)
        self.assertEqual(comparison['rows'][0][1],f'0x{GAMEDATA_ADDR+0x140:08X}')
        ram.write_guest(MAP_ADDR,b'\x00\x24')
        self.assertFalse(checkpoint_differences(ram,checkpoint)['map_matches'])

    def test_native_debug_state_write_only_when_safe(self):
        _,ram=self.sample()
        self.assertEqual(open_native_debug_menu(ram),10)
        self.assertEqual(ram.u8(0x800C7A94),10)
        self.assertEqual(ram.u16(MAP_ADDR),0x23) # map is never overwritten
        with self.assertRaises(ValueError):
            open_native_debug_menu(ram)

    def test_scene_labels_are_grounded(self):
        self.assertEqual(SCENES[465],"South Oedo - Goemon's House")
        self.assertIn('Unknown',scene_label(0x777))

if __name__=='__main__':unittest.main()

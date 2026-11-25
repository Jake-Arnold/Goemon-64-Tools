"""The character ID must never be directly written to trigger a swap."""
import unittest
import tests.test_checkpoint as checkpoint_fixture
from practice.native_character import (
    prepare_character_swap, undo_character_preparation, ready_after_native_swap,
    PARTY_OFFSET, CHARACTER_TASK_OFFSET, ready_for_scene_character, ready_for_scene_spawn, scene_character_unlocked,
)
from practice.checkpoints import GAMEDATA_ADDR, MAP_ADDR
from practice.backends.memory import CHARACTER_ID_ADDR

class TestNativeCharacter(unittest.TestCase):
    def sample(self):
        # Create a coherent stage where saved char=3 and currently char=0.
        p, ram = checkpoint_fixture.TestCheckpoint().sample()
        ram.write_guest(CHARACTER_ID_ADDR,(3).to_bytes(4,'big'))
        ram.write_guest(GAMEDATA_ADDR+PARTY_OFFSET+4*3, (1).to_bytes(4,'big'))
        cp=__import__('practice.checkpoints',fromlist=['capture_checkpoint']).capture_checkpoint(ram,'Yae test')
        ram.write_guest(CHARACTER_ID_ADDR, (0).to_bytes(4,'big'))
        ram.write_guest(0x801B0000+CHARACTER_TASK_OFFSET,b'\x00')
        ram.write_guest(0x801B0000+0xCC,b'\x00')
        return ram,cp

    def test_already_unlocked_does_not_write(self):
        ram,cp=self.sample()
        patch=prepare_character_swap(ram,cp)
        self.assertIsNone(patch)
        self.assertEqual(ram.u32(CHARACTER_ID_ADDR),0)

    def test_stages_one_party_entry_and_rolls_back(self):
        ram,cp=self.sample()
        addr=GAMEDATA_ADDR+PARTY_OFFSET+4*3
        ram.write_guest(addr,b'\x00'*4)
        patch=prepare_character_swap(ram,cp)
        self.assertIsNotNone(patch)
        self.assertEqual(ram.read_guest(addr,4),b'\x00\x00\x00\x01')
        self.assertEqual(ram.u32(CHARACTER_ID_ADDR),0)
        self.assertIn('reverted',undo_character_preparation(ram,patch,3))
        self.assertEqual(ram.read_guest(addr,4),b'\x00'*4)

    def test_cannot_clear_availability_of_active_character(self):
        ram,cp=self.sample()
        addr=GAMEDATA_ADDR+PARTY_OFFSET+4*3
        ram.write_guest(addr,b'\x00'*4)
        patch=prepare_character_swap(ram,cp)
        ram.write_guest(CHARACTER_ID_ADDR,(3).to_bytes(4,'big'))
        self.assertIn('kept',undo_character_preparation(ram,patch,3))
        self.assertEqual(ram.u32(addr),1)

    def test_ready_only_after_native_character_task_finishes(self):
        ram,cp=self.sample()
        self.assertFalse(ready_after_native_swap(ram,cp))
        ram.write_guest(CHARACTER_ID_ADDR,(3).to_bytes(4,'big'))
        ram.write_guest(0x801B0000+CHARACTER_TASK_OFFSET,b'\x03')
        ram.write_guest(0x801B0000+0xCC,b'\xBA')
        self.assertFalse(ready_after_native_swap(ram,cp))
        ram.write_guest(0x801B0000+0xCC,b'\x00')
        self.assertTrue(ready_after_native_swap(ram,cp))
        ram.write_guest(0x801B0000+CHARACTER_TASK_OFFSET,b'\x01')
        self.assertFalse(ready_after_native_swap(ram,cp))

    def test_scene_character_ready_checks_map_task_and_loading(self):
        ram,_=self.sample()
        base=ram.snapshot()['task_ptr']
        ram.write_guest(base+0xCC,b'\x00')
        ram.write_guest(base+CHARACTER_TASK_OFFSET,b'\x00')
        current_map=ram.u16(MAP_ADDR)
        self.assertTrue(scene_character_unlocked(ram,0))
        self.assertTrue(ready_for_scene_character(ram,current_map,0))
        self.assertFalse(ready_for_scene_character(ram,current_map+1,0))
        ram.write_guest(base+CHARACTER_TASK_OFFSET,b'\x01')
        self.assertFalse(ready_for_scene_character(ram,current_map,0))
        ram.write_guest(base+CHARACTER_TASK_OFFSET,b'\x00')
        ram.write_guest(base+0xCC,b'\xBA')
        self.assertFalse(ready_for_scene_character(ram,current_map,0))

    def test_spawn_verification_requires_correct_character_model_and_map(self):
        ram,_=self.sample()
        snap=ram.snapshot()
        character=snap['character']
        self.assertTrue(ready_for_scene_spawn(ram,ram.u16(MAP_ADDR),character,snap))
        self.assertFalse(ready_for_scene_spawn(ram,ram.u16(MAP_ADDR)+1,character,snap))
        self.assertFalse(ready_for_scene_spawn(ram,ram.u16(MAP_ADDR),(character+1)%4,snap))

    def test_wrong_map_never_prepares(self):
        ram,cp=self.sample()
        ram.write_guest(MAP_ADDR,b'\x00\x12')
        with self.assertRaisesRegex(ValueError,'map differs'):
            prepare_character_swap(ram,cp)

if __name__=='__main__':unittest.main()

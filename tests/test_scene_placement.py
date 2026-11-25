import struct
import unittest
from unittest.mock import patch
from practice.entrances import Spawn
from practice.scene_placement import SpawnPlacement,apply_spawn_position
from practice.experimental_controls import stage_reload_trial,ACTIVE_CHARACTER_ADDR
from practice.checkpoints import MAP_ADDR,STATE_ADDR,SCRIPT_VM_ADDR,SCRIPT_LOCK_ADDR,TRANSITION_ADDR,PHASE_ADDR,PAUSE_ADDR
from practice.scene_controls import PENDING_MAP_ADDR
import tests.test_checkpoint as checkpoint_fixture


class SpawnPlacementTests(unittest.TestCase):
    def sample(self):
        _,ram=checkpoint_fixture.TestCheckpoint().sample();return ram

    def target_ready(self,ram):
        ram.write_guest(MAP_ADDR,(353).to_bytes(2,'big'));ram.write_guest(STATE_ADDR,b'\x0D')

    def placement(self,ram):
        snap=ram.snapshot()
        return SpawnPlacement(ram,Spawn(353,(95,0,-350),0x300,0x10,'Test entrance','161:002'),0,35,snap['player_ptr'],snap['task_ptr'],0)

    def test_stages_complete_native_spawn_before_reload_without_touching_source_player(self):
        ram=self.sample();before=ram.read_guest(ram.snapshot()['player_ptr']+8,12)
        writes=[];original=ram.write_guest
        def write(address,data):writes.append((address,data));original(address,data)
        ram.write_guest=write
        spawn=self.placement(ram).spawn
        result=stage_reload_trial(ram,353,{353:'Destination'},spawn=spawn)
        self.assertEqual(writes,[(PENDING_MAP_ADDR,spawn.pending_bytes()),(STATE_ADDR,b'\x0C')])
        self.assertEqual(ram.read_guest(ram.snapshot()['player_ptr']+8,12),before)
        self.assertEqual(result['staged_spawn']['position'],[95,0,-350])

    def test_invalid_spawn_or_active_script_makes_no_reload_writes(self):
        for address,data in ((SCRIPT_VM_ADDR,(1).to_bytes(4,'big')),(SCRIPT_LOCK_ADDR,b'\x01'),(TRANSITION_ADDR,b'\x01'),(PAUSE_ADDR,b'\x01')):
            ram=self.sample();ram.write_guest(address,data)
            with patch.object(ram,'write_guest',side_effect=AssertionError('No writes')):
                with self.assertRaises(ValueError):stage_reload_trial(ram,353,{353:'Target'},spawn=Spawn(353,(1,2,3)))
        ram=self.sample()
        with patch.object(ram,'write_guest',side_effect=AssertionError('No writes')):
            with self.assertRaises(ValueError):stage_reload_trial(ram,353,{353:'Target'},spawn=Spawn(354,(1,2,3)))

    def test_full_pending_record_rolls_back_on_failed_character_staging(self):
        ram=self.sample();before=bytes(range(12));ram.write_guest(PENDING_MAP_ADDR,before)
        original=ram.write_guest
        def fail(address,data):
            if address==ACTIVE_CHARACTER_ADDR:raise OSError('character failed')
            original(address,data)
        ram.write_guest=fail
        with self.assertRaises(OSError):stage_reload_trial(ram,353,{353:'Target'},spawn_character=2,spawn=Spawn(353,(1,2,3)))
        self.assertEqual(ram.read_guest(PENDING_MAP_ADDR,12),before)
        self.assertEqual(ram.u8(STATE_ADDR),13)

    def test_places_once_after_destination_and_stable_character(self):
        ram=self.sample();placement=self.placement(ram)
        with patch.object(ram,'write_guest',side_effect=AssertionError('Still source')):self.assertEqual(placement.poll(ram,.1)['status'],'waiting')
        self.target_ready(ram)
        self.assertEqual(placement.poll(ram,.2)['status'],'waiting')
        result=placement.poll(ram,.4)
        self.assertEqual(result['status'],'placed')
        self.assertEqual(tuple(ram.snapshot()[k] for k in ('x','y','z')),(95,0,-350))
        with self.assertRaises(RuntimeError):placement.poll(ram,.5)

    def test_loading_scripts_wrong_character_and_pointer_changes_reset_readiness(self):
        ram=self.sample();placement=self.placement(ram);self.target_ready(ram)
        ram.write_guest(SCRIPT_LOCK_ADDR,b'\x01')
        self.assertEqual(placement.poll(ram,.1)['status'],'waiting');ram.write_guest(SCRIPT_LOCK_ADDR,b'\0')
        ram.write_guest(ram.snapshot()['task_ptr']+0x60,b'\x02')
        self.assertEqual(placement.poll(ram,.2)['reason'],'character');ram.write_guest(ram.snapshot()['task_ptr']+0x60,b'\0')
        self.assertEqual(placement.poll(ram,.3)['status'],'waiting')
        ram.write_guest(0x801FC60C,(0x801A1000).to_bytes(4,'big'))
        self.assertEqual(placement.poll(ram,.4)['status'],'waiting')
        self.assertEqual(placement.poll(ram,.5)['status'],'placed')

    def test_wrong_map_disconnect_timeout_and_menu_cancel_never_place(self):
        ram=self.sample();placement=self.placement(ram)
        ram.write_guest(MAP_ADDR,(354).to_bytes(2,'big'))
        with patch.object(ram,'write_guest',side_effect=AssertionError('Wrong map')):
            with self.assertRaises(RuntimeError):placement.poll(ram,.1)
        with self.assertRaises(RuntimeError):placement.poll(self.sample(),.1)
        ram=self.sample();placement=self.placement(ram)
        with self.assertRaises(RuntimeError):placement.poll(ram,16)
        placement.spawn=Spawn(35,(1,2,3));ram.write_guest(STATE_ADDR,b'\x0A')
        self.assertEqual(placement.poll(ram,.1)['status'],'waiting');ram.write_guest(STATE_ADDR,b'\x0D')
        for time in (.2,.4,.6):self.assertEqual(placement.poll(ram,time)['reason'],'same_stage_reload')

    def test_single_vector_write_preserves_neighbors_and_is_not_retried_after_failure(self):
        ram=self.sample();placement=self.placement(ram);self.target_ready(ram);player=ram.snapshot()['player_ptr']
        before=ram.read_guest(player,8);after=ram.read_guest(player+20,12)
        writes=[];original=ram.write_guest
        def fail(address,data):writes.append((address,data));original(address,data);raise OSError('partial write uncertain')
        placement.poll(ram,.1);ram.write_guest=fail
        with self.assertRaises(OSError):placement.poll(ram,.3)
        with self.assertRaises(RuntimeError):placement.poll(ram,.4)
        self.assertEqual(writes,[(player+8,struct.pack('>fff',95,0,-350))])
        self.assertEqual(ram.read_guest(player,8),before);self.assertEqual(ram.read_guest(player+20,12),after)

    def test_big_endian_host_stages_and_places_canonical_values(self):
        from practice.backends.memory import Rdram
        from tests.test_checkpoint import BASE
        ram=self.sample();memory=ram.process.mem;converted=bytearray(len(memory))
        for index in range(4):converted[index::4]=memory[3-index::4]
        ram.process.mem=converted;ram=Rdram(ram.process,BASE,'big')
        placement=self.placement(ram)
        stage_reload_trial(ram,353,{353:'Target'},spawn=placement.spawn)
        self.assertEqual(ram.read_guest(PENDING_MAP_ADDR,12),placement.spawn.pending_bytes())
        self.target_ready(ram)
        placement.poll(ram,.1);self.assertEqual(placement.poll(ram,.3)['status'],'placed')
        self.assertEqual(tuple(ram.snapshot()[k] for k in ('x','y','z')),(95,0,-350))

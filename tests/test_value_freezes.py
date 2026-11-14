import unittest
from unittest.mock import patch
from practice.value_freezes import ValueFreezes,HEALTH,MAX_HEALTH
from practice.checkpoints import STATE_ADDR,PAUSE_ADDR
from tests import test_checkpoint


class ValueFreezeTests(unittest.TestCase):
    def setUp(self):
        self.process,self.ram=test_checkpoint.TestCheckpoint().sample()
        self.freezes=ValueFreezes();self.token=(123,456)

    def poll(self,**kw):
        return self.freezes.poll(self.ram,self.token,writable=kw.get('writable',True))

    def test_raw_reasserts_changed_value_skips_unchanged_and_preserves_neighbors(self):
        addr=0x8015C63B
        self.ram.write_guest(addr-1,b'\xA1\x02\xB2')
        self.freezes.add(self.token,addr,b'\x10')
        self.assertIn('Active',self.poll())
        self.assertEqual(self.ram.read_guest(addr-1,3),b'\xA1\x10\xB2')
        with patch.object(self.process,'write',side_effect=AssertionError('Already matches')):self.poll()
        self.ram.write_guest(addr,b'\x00');self.poll()
        self.assertEqual(self.ram.u8(addr),0x10)

    def test_max_health_tracks_maximum_and_does_not_change_maximum(self):
        self.freezes.enable_health(self.token);self.poll()
        self.assertEqual(self.ram.u32(HEALTH),10)
        self.ram.write_guest(MAX_HEALTH,(12).to_bytes(4,'big'));self.poll()
        self.assertEqual(self.ram.u32(HEALTH),12)
        self.assertEqual(self.ram.u32(MAX_HEALTH),12)
        self.ram.write_guest(MAX_HEALTH,bytes(4))
        self.assertIn('stopped after failure',self.poll())
        self.assertFalse(self.freezes.keep_health)

    def test_no_writes_during_pause_scripts_or_transition_then_resumes(self):
        self.freezes.add(self.token,0x8015C63B,b'\x10')
        for address,value in ((PAUSE_ADDR,1),(STATE_ADDR,12),(0x80077858,1)):
            self.ram.write_guest(address,bytes([value]))
            with patch.object(self.process,'write',side_effect=AssertionError('Paused')):
                self.assertIn('paused',self.poll())
            self.ram.write_guest(address,bytes([13 if address==STATE_ADDR else 0]))
        self.poll();self.assertEqual(self.ram.u8(0x8015C63B),16)

    def test_disconnect_reconnect_permissions_and_failure_stop_without_retry(self):
        for reason in ('disconnect','token','read_only','failure'):
            self.freezes.add(self.token,0x8015C63B,b'\x10')
            with patch.object(self.process,'write',side_effect=OSError('write denied')):
                if reason=='disconnect':result=self.freezes.poll(None,self.token,writable=True)
                elif reason=='token':result=self.freezes.poll(self.ram,(999,456),writable=True)
                elif reason=='read_only':result=self.poll(writable=False)
                else:result=self.poll()
            self.assertIn('stopped',result);self.assertEqual(self.freezes.locks,{})
            with patch.object(self.process,'write',side_effect=AssertionError('No retry')):self.poll()
            self.ram.write_guest(0x8015C63B,b'\x00')

    def test_overlap_bounds_and_health_conflicts(self):
        for address,value in ((0x7FFFFFFF,b'1'),(0x807FFFFF,b'12'),(0x80150000,b'123')):
            with self.assertRaises(ValueError):self.freezes.add(self.token,address,value)
        self.freezes.add(self.token,0x8015C63A,b'12')
        with self.assertRaisesRegex(ValueError,'overlaps'):self.freezes.add(self.token,0x8015C63B,b'1')
        self.freezes.clear();self.freezes.enable_health(self.token)
        with self.assertRaises(ValueError):self.freezes.add(self.token,HEALTH,b'1234')
        self.freezes.clear();self.freezes.add(self.token,HEALTH,b'1234')
        with self.assertRaises(ValueError):self.freezes.enable_health(self.token)


    def test_enemy_pass_through_follows_live_player_task(self):
        from practice.value_freezes import ENEMY_PASS_THROUGH_OFFSET
        from autosplitter.memory import PLAYER_TASK_PTR_ADDR
        first = self.ram.u32(PLAYER_TASK_PTR_ADDR)
        self.assertTrue(self.ram.is_ram_pointer(first + ENEMY_PASS_THROUGH_OFFSET))
        self.freezes.enable_enemy_pass_through(self.token)
        self.assertTrue(self.freezes.active())
        self.assertIn('enemy pass-through', self.poll())
        self.assertEqual(self.ram.u8(first + ENEMY_PASS_THROUGH_OFFSET), 6)
        # Repoint the task in the very same gameplay session: no fixed lock
        # may keep writing the old task's +0x30 state.
        second = first + 0x400
        self.ram.write_guest(PLAYER_TASK_PTR_ADDR, second.to_bytes(4, 'big'))
        self.ram.write_guest(first + ENEMY_PASS_THROUGH_OFFSET, b'\x03')
        self.ram.write_guest(second + ENEMY_PASS_THROUGH_OFFSET, b'\x03')
        self.assertIn('enemy pass-through', self.poll())
        self.assertEqual(self.ram.u8(first + ENEMY_PASS_THROUGH_OFFSET), 3)
        self.assertEqual(self.ram.u8(second + ENEMY_PASS_THROUGH_OFFSET), 6)
        self.freezes.disable_enemy_pass_through()
        self.assertFalse(self.freezes.active())
        self.ram.write_guest(second + ENEMY_PASS_THROUGH_OFFSET, b'\x03')
        with patch.object(self.process, 'write', side_effect=AssertionError('Disabled')):
            self.poll()

    def test_enemy_pass_through_pause_and_session_loss(self):
        from practice.value_freezes import ENEMY_PASS_THROUGH_OFFSET
        from autosplitter.memory import PLAYER_TASK_PTR_ADDR
        address = self.ram.u32(PLAYER_TASK_PTR_ADDR) + ENEMY_PASS_THROUGH_OFFSET
        self.freezes.enable_enemy_pass_through(self.token)
        self.ram.write_guest(PAUSE_ADDR, b'\x01')
        with patch.object(self.process, 'write', side_effect=AssertionError('Paused')):
            self.assertIn('paused', self.poll())
        self.ram.write_guest(PAUSE_ADDR, b'\x00')
        self.poll()
        self.assertEqual(self.ram.u8(address), 6)
        with patch.object(self.process, 'write', side_effect=AssertionError('New session')):
            self.assertIn('stopped', self.freezes.poll(self.ram, ('different',), writable=True))
        self.assertFalse(self.freezes.enemy_pass_through)
        self.freezes.enable_enemy_pass_through(self.token)
        with patch.object(self.process, 'write', side_effect=AssertionError('Read-only')):
            self.assertIn('stopped', self.freezes.poll(self.ram, self.token, writable=False))
        self.assertFalse(self.freezes.enemy_pass_through)

    def test_enemy_pass_through_respects_pointer_change_before_write(self):
        from practice.value_freezes import ENEMY_PASS_THROUGH_OFFSET
        from autosplitter.memory import PLAYER_TASK_PTR_ADDR
        old = self.ram.u32(PLAYER_TASK_PTR_ADDR)
        new = old + 0x400
        self.freezes.enable_enemy_pass_through(self.token)
        original_read = self.ram.read_guest
        shifted = False
        def switch_on_target_read(addr, width):
            nonlocal shifted
            if addr == old + ENEMY_PASS_THROUGH_OFFSET and not shifted:
                shifted = True
                self.ram.write_guest(PLAYER_TASK_PTR_ADDR, new.to_bytes(4, 'big'))
            return original_read(addr, width)
        original_write = self.ram.write_guest
        def reject_old_target(addr, value):
            if addr == old + ENEMY_PASS_THROUGH_OFFSET:
                raise AssertionError('Stale player-task write')
            return original_write(addr, value)
        with patch.object(self.ram, 'read_guest', side_effect=switch_on_target_read), \
             patch.object(self.ram, 'write_guest', side_effect=reject_old_target):
            self.assertIn('paused', self.poll())
        self.assertTrue(shifted)

    def test_enemy_pass_through_conflicting_fixed_lock_fails_closed(self):
        from practice.value_freezes import ENEMY_PASS_THROUGH_OFFSET
        from autosplitter.memory import PLAYER_TASK_PTR_ADDR
        target = self.ram.u32(PLAYER_TASK_PTR_ADDR) + ENEMY_PASS_THROUGH_OFFSET
        self.freezes.add(self.token, target, b'\x03')
        self.freezes.enable_enemy_pass_through(self.token)
        with patch.object(self.process, 'write', side_effect=AssertionError('Conflicting writes')):
            self.assertIn('overlaps', self.poll())
        self.assertFalse(self.freezes.active())

    def test_god_mode_resources_enforce_and_uncheck_is_not_revert(self):
        self.ram.write_guest(HEALTH,(2).to_bytes(4,'big'))
        self.ram.write_guest(0x8015C5E8,(5).to_bytes(4,'big'))
        self.ram.write_guest(0x8015C5EC,(1).to_bytes(4,'big'))
        self.freezes.enable_god_mode(self.token)
        self.assertIn('God Mode on',self.poll())
        self.assertEqual(self.ram.u32(HEALTH),10)
        self.assertEqual(self.ram.u32(0x8015C5E8),9999)
        self.assertEqual(self.ram.u32(0x8015C5EC),99)
        self.freezes.disable_god_mode()
        self.assertFalse(self.freezes.active())
        self.ram.write_guest(0x8015C5E8,(10).to_bytes(4,'big'))
        with patch.object(self.process,'write',side_effect=AssertionError('No writes after off')):
            self.poll()
        self.assertEqual(self.ram.u32(0x8015C5E8),10)

    def test_god_mode_conflict_and_disconnect(self):
        self.freezes.add(self.token,HEALTH,b'\x00\x00\x00\x05')
        with self.assertRaisesRegex(ValueError,'conflicting'):
            self.freezes.enable_god_mode(self.token)
        self.freezes.clear()
        self.freezes.enable_god_mode(self.token)
        with self.assertRaisesRegex(ValueError,'conflicts'):
            self.freezes.add(self.token,0x8015C5E9,b'\x01')
        self.assertIn('stopped',self.freezes.poll(None,self.token,writable=True))
        self.assertFalse(self.freezes.god_mode)

    def test_readback_failure_clears_all_locks(self):
        self.freezes.add(self.token,0x8015C63B,b'\x10')
        with patch.object(self.process,'write',return_value=None):
            self.assertIn('failure',self.poll())
        self.assertFalse(self.freezes.locks)

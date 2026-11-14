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

    def test_readback_failure_clears_all_locks(self):
        self.freezes.add(self.token,0x8015C63B,b'\x10')
        with patch.object(self.process,'write',return_value=None):
            self.assertIn('failure',self.poll())
        self.assertFalse(self.freezes.locks)

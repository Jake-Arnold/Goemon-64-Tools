"""Regression checks for high-frequency freezes without Tk callbacks."""
import queue
import threading
import time
import unittest

from practice.value_freezes import ValueFreezes, FastFreezeWorker, FREEZE_INTERVAL_SECONDS
from tests.test_checkpoint import TestCheckpoint


class FastFreezeTests(unittest.TestCase):
    def setUp(self):
        self.process, self.ram = TestCheckpoint().sample()
        self.freezes = ValueFreezes()
        self.token = (123, 456)

    def test_independent_worker_corrects_value_without_tk_event_loop(self):
        addr=0x8015C63B
        self.freezes.add(self.token,addr,b'\x10')
        messages=queue.SimpleQueue()
        worker=FastFreezeWorker(self.freezes,
                                 lambda:(self.ram,self.token,True),messages,interval=0.005)
        try:
            worker.start()
            self.ram.write_guest(addr,b'\x01')
            deadline=time.monotonic()+1.0
            while self.ram.u8(addr)!=16 and time.monotonic()<deadline:
                time.sleep(0.005)
            self.assertEqual(self.ram.u8(addr),16)
            self.assertFalse(messages.empty())
        finally:
            worker.stop()

    def test_remove_lock_and_rename_are_thread_safe(self):
        addr=0x8015C63B
        self.freezes.add(self.token,addr,b'\x10',label='Old')
        worker=FastFreezeWorker(self.freezes,lambda:(self.ram,self.token,True),interval=0.005)
        try:
            worker.start()
            self.freezes.rename_lock(addr,'Old','Renamed')
            self.assertEqual(self.freezes.get(addr).label,'Renamed')
            self.freezes.remove(addr)
            self.assertFalse(self.freezes.active())
            self.ram.write_guest(addr,b'\x00')
            time.sleep(0.025)
            self.assertEqual(self.ram.u8(addr),0)
        finally:
            worker.stop()

    def test_worker_stops_and_clears_on_connection_change(self):
        addr=0x8015C63B
        self.freezes.add(self.token,addr,b'\x10')
        worker=FastFreezeWorker(self.freezes,
                                 lambda:(self.ram,('new', 'connection'),True),interval=0.005)
        try:
            worker.start()
            deadline=time.monotonic()+1.0
            while self.freezes.active() and time.monotonic()<deadline:
                time.sleep(0.005)
            self.assertFalse(self.freezes.active())
        finally:
            worker.stop()

    def test_default_interval_is_ten_milliseconds(self):
        self.assertEqual(FREEZE_INTERVAL_SECONDS,0.010)
        with self.assertRaises(ValueError):
            FastFreezeWorker(self.freezes,lambda:(self.ram,self.token,True),interval=0.001)


if __name__=='__main__':
    unittest.main()

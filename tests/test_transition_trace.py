import unittest
from practice.transition_trace import read_transition_sample, TransitionTrace

class Ram:
    def __init__(self):self.data={}
    def read_guest(self,addr,n):return bytes(self.data.get(addr+i,0) for i in range(n))
    def set(self,addr,num,width):
        for i,b in enumerate(num.to_bytes(width,'big')):self.data[addr+i]=b

class TestTrace(unittest.TestCase):
    def test_reads_pending_previous_and_exit_separately(self):
        r=Ram()
        r.set(0x800C7A94,13,1)
        r.set(0x800C7A9E,1,1)
        r.set(0x800C7A9F,0,1)
        r.set(0x800C7AB2,90,2)
        r.set(0x800C7ABC,91,2)
        r.set(0x800C7CA0,96,2)
        r.set(0x8015C5DC,2,4)
        got=read_transition_sample(r)
        self.assertEqual((got['state'],got['phase'],got['exit_request']), (13,1,0))
        self.assertEqual((got['current_map'],got['previous_map'],got['pending_map']),(90,91,96))
        self.assertEqual(got['active_character'],2)
    def test_trace_stops_and_exports(self):
        r=Ram()
        r.set(0x800C7AB2,90,2)
        rec=TransitionTrace(r,duration=.1,interval=.005)
        rec.start();rec.thread.join(timeout=1)
        self.assertFalse(rec.thread.is_alive())
        data=rec.report()
        self.assertEqual(data['format'],'mnsg-usa-in-game-transition-trace-v1')
        self.assertGreater(data['samples'],1)
        self.assertEqual(data['events'][0]['values']['current_map'],90)
        self.assertIsNone(data['error'])
if __name__=='__main__':unittest.main()

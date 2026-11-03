import unittest
from contextlib import contextmanager
from unittest.mock import patch
from speed.live_control import MAGIC,VERSION,SpeedStatus,SpeedUnavailable,read_speed,request_speed

class FakeChannel:
    def __init__(self, words):self.words=words;self.writes=[]
    def read(self):return self.words
    def request(self,value):self.writes.append(value)

@contextmanager
def opened(channel):yield channel

class LiveSpeedControlTests(unittest.TestCase):
    def test_read_and_request_preserve_applied_until_host_acknowledges(self):
        channel=FakeChannel((MAGIC,VERSION,55,1,1,1234))
        with patch('speed.live_control._open_channel',return_value=opened(channel)):
            self.assertEqual(read_speed(55),SpeedStatus(1,1,1234))
        with patch('speed.live_control._open_channel',return_value=opened(channel)):
            self.assertEqual(request_speed(55,2),SpeedStatus(1,1,1234))
        self.assertEqual(channel.writes,[2])

    def test_invalid_identity_or_rate_never_writes(self):
        for words in ((0,VERSION,55,1,1,0),(MAGIC,VERSION,56,1,1,0),
                      (MAGIC,VERSION,55,0,1,0),(MAGIC,VERSION,55,1,9,0)):
            channel=FakeChannel(words)
            with patch('speed.live_control._open_channel',return_value=opened(channel)):
                with self.assertRaises(SpeedUnavailable):request_speed(55,2)
            self.assertEqual(channel.writes,[])
        with patch('speed.live_control._open_channel') as opener:
            for value in (0,5,2.0,True,'2'):
                with self.assertRaises(ValueError):request_speed(55,value)
            opener.assert_not_called()

    def test_millis_wrap_is_reported_unsigned(self):
        channel=FakeChannel((MAGIC,VERSION,55,1,1,-1))
        with patch('speed.live_control._open_channel',return_value=opened(channel)):
            self.assertEqual(read_speed(55).guest_millis,0xFFFFFFFF)

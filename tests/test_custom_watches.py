"""Tests for custom watch parsing and guest-memory interpretation."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from practice.custom_watches import make_watch, append_watch, save_watches, load_watches, read_watch

class FakeRAM:
    def __init__(self, data=b'\x01\x02\xA0\xB0\x3F\x80\x00\x00'):
        self.data=data
    def read_guest(self, address, width):
        index=address-0x8015C574
        return self.data[index:index+width]

class CustomWatchTests(unittest.TestCase):
    def test_endian_decode(self):
        ram=FakeRAM()
        self.assertEqual(read_watch(ram,make_watch('Map','8015C574','u8')).raw,'0x01')
        self.assertEqual(read_watch(ram,make_watch('Counter','8015C574','u16')).value,'258')
        self.assertEqual(read_watch(ram,make_watch('Float','8015C578','f32')).value,'1')
        self.assertEqual(read_watch(ram,make_watch('Raw','8015C574','hex8')).raw,'0x0102A0B03F800000')

    def test_save_reload_and_reject_duplicates(self):
        with TemporaryDirectory() as d:
            path=Path(d)/'custom_watches.json'
            entries=append_watch([],make_watch('Map','0x8015C574','u8'))
            save_watches(path,entries)
            self.assertEqual(load_watches(path),entries)
            with self.assertRaises(ValueError):append_watch(entries,make_watch('map','8015C575','u8'))

    def test_invalid_ranges(self):
        for value in ('garbage','0x00000000','0x90000000'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                make_watch('Bad',value,'u8')
        with self.assertRaises(ValueError):
            make_watch('Out of range','0x807FFFFF','f64')

    def test_read_failure_is_isolated(self):
        class Bad:
            def read_guest(self,*args):raise OSError('not mapped')
        self.assertEqual(read_watch(Bad(),make_watch('Bad','8015C574','u8')).status,'ERROR')

if __name__ == '__main__': unittest.main()

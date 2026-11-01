import unittest
from practice.hex_edit import POLICIES, parse_hex, checked_write, get_policy
from tests.test_checkpoint import TestCheckpoint

class TestHexEdit(unittest.TestCase):
    def test_canonical_parse_and_bounds(self):
        self.assertEqual(parse_hex('0x00ff',2),b'\x00\xff')
        self.assertEqual(parse_hex('a',1),b'\x0a')
        for bad in ('', '0x','0xG1','0x100','-1'):
            with self.subTest(bad=bad),self.assertRaises(ValueError):parse_hex(bad,1)
    def test_safe_resource_write(self):
        _,ram=TestCheckpoint().sample()
        addr=0x8015C5E8
        old=ram.read_guest(addr,4)
        self.assertTrue(checked_write(ram,addr,old,parse_hex('0x0000022B',4)))
        self.assertEqual(ram.u32(addr),555)
        with self.assertRaises(RuntimeError):checked_write(ram,addr,old,parse_hex('A0',4))
    def test_dangerous_engine_fields_require_unlock(self):
        _,ram=TestCheckpoint().sample()
        address=0x800C7A9F
        before=ram.read_guest(address,1)
        with self.assertRaises(PermissionError):checked_write(ram,address,before,b'\x01')
        self.assertEqual(ram.read_guest(address,1),before)
        self.assertTrue(get_policy(address).advanced)
    def test_wrong_width_and_protected_unknown(self):
        _,ram=TestCheckpoint().sample()
        with self.assertRaises(ValueError):checked_write(ram,0x8015C5E8,b'\x00',b'\x01')
        with self.assertRaises(ValueError):checked_write(ram,0x80123456,b'\x00',b'\x01')
        with self.assertRaises(ValueError):checked_write(ram,0x8015C5E8,ram.read_guest(0x8015C5E8,4),parse_hex('0xFFFFFF',4))
    def test_stable_state_only(self):
        _,ram=TestCheckpoint().sample()
        ram.write_guest(0x800C7A94,b'\x03')
        addr=0x8015C5E8
        with self.assertRaises(RuntimeError):checked_write(ram,addr,ram.read_guest(addr,4),b'\x00\x00\x00\x02')
    def test_unsafe_raw_override_allows_unrestricted_values(self):
        _,ram=TestCheckpoint().sample()
        addr=0x8015C5E8  # ordinary resource has max_value 9999
        old=ram.read_guest(addr,4)
        raw=parse_hex('DEADBEEF',4)
        with self.assertRaises(ValueError):checked_write(ram,addr,old,raw)
        with self.assertRaises(PermissionError):checked_write(ram,addr,old,raw,raw_override=True)
        self.assertTrue(checked_write(ram,addr,old,raw,allow_advanced=True,raw_override=True))
        self.assertEqual(ram.read_guest(addr,4),raw)

    def test_unsafe_raw_override_accepts_unknown_address_and_checks_width(self):
        _,ram=TestCheckpoint().sample()
        address=0x8015C70B
        before=ram.read_guest(address,1)
        self.assertTrue(checked_write(ram,address,before,b'\xFE',allow_advanced=True,raw_override=True))
        with self.assertRaises(ValueError):checked_write(ram,0x807FFFFF,b'\x00\x00',b'\x00\x01',allow_advanced=True,raw_override=True)
        with self.assertRaises(RuntimeError):checked_write(ram,address,before,b'\x44',allow_advanced=True,raw_override=True)

    def test_known_field_widths(self):
        self.assertEqual(POLICIES[0x800C7CA0].width,2)
        self.assertEqual(POLICIES[0x800C7E60].width,4)
        self.assertEqual(POLICIES[0x8015C5D4].width,4)

if __name__=='__main__':unittest.main()

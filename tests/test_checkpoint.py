"""Self-contained USA RAM fixtures for checkpoint and value-freeze tests.

Keep these tests independent of the removed LiveSplit/autosplitter bridge
and route engine. The shared RDRAM reader remains production code.
"""
import unittest
import struct
from autosplitter.memory import (
    Rdram, SYS_POINTER_ADDR, SYS_EXPECTED_PTR, PLAYER_OBJECT_PTR_ADDR,
    PLAYER_TASK_PTR_ADDR, CHARACTER_ID_ADDR, LOADING_FLAG_ADDR,
)

BASE = 0x10000000


class FakeProcess:
    def __init__(self):
        self.mem = bytearray(0x800000)

    def read(self, addr, size):
        offset = addr - BASE
        if offset < 0 or offset + size > len(self.mem):
            raise OSError("bad read")
        return bytes(self.mem[offset:offset + size])

    def write(self, addr, value):
        offset = addr - BASE
        if offset < 0 or offset + len(value) > len(self.mem):
            raise OSError("bad write")
        self.mem[offset:offset + len(value)] = value

    def regions(self):
        return [(BASE, len(self.mem))]


def write_u32(process, address, value):
    process.write(BASE + (address & 0x1FFFFFFF), struct.pack("<I", value))


def write_u8(process, address, value):
    process.write(BASE + ((address & 0x1FFFFFFF) ^ 3), bytes([value]))


def sample_process():
    process = FakeProcess()
    write_u32(process, SYS_POINTER_ADDR, SYS_EXPECTED_PTR)
    write_u32(process, PLAYER_OBJECT_PTR_ADDR, 0x801A0000)
    write_u32(process, PLAYER_TASK_PTR_ADDR, 0x801B0000)
    write_u32(process, CHARACTER_ID_ADDR, 3)
    write_u8(process, LOADING_FLAG_ADDR, 0)
    write_u8(process, 0x801B0000 + 0xCC, 4)
    for index, value in enumerate((125.25, -5.5, 700.5)):
        process.write(
            BASE + (0x801A0008 & 0x1FFFFFFF) + index * 4,
            struct.pack("<f", value),
        )
    return process
from practice.checkpoints import (capture_checkpoint, restore_checkpoint,
                                  validate_checkpoint, LIVE_ADDR, GAMEDATA_ADDR,
                                  HEADER_ADDR, SHADOW_ADDR, MAP_ADDR, STATE_ADDR,
                                  PHASE_ADDR, SUBMODE_ADDR)


class TestCheckpoint(unittest.TestCase):
    def sample(self, endian="wordswapped"):
        if endian != "wordswapped":
            raise NotImplementedError
        p = sample_process()
        ram = Rdram(p, BASE, endian)
        write_u8(p, STATE_ADDR, 13)
        write_u8(p, PHASE_ADDR, 1)
        write_u8(p, SUBMODE_ADDR, 0)
        ram.write_guest(MAP_ADDR, (0x23).to_bytes(2, "big"))
        ram.write_guest(GAMEDATA_ADDR, bytes((i*7) % 256 for i in range(0x304)))
        ram.write_guest(HEADER_ADDR, bytes(range(12)))
        ram.write_guest(LIVE_ADDR, b"\x00" * 0x30)
        for off, v in ((8, 10), (12, 8), (16, 100), (20, 3)):
            ram.write_guest(LIVE_ADDR + off, struct.pack(">I", v))
        ram.write_guest(0x801A0014, b"\x00\x01\x00\x02\x00\x03")
        return p, ram

    def test_guest_read_write_misaligned(self):
        p, ram = self.sample()
        ram.write_guest(0x801A0051, bytes(range(11)))
        self.assertEqual(ram.read_guest(0x801A0051, 11), bytes(range(11)))
        self.assertEqual(ram.u16(0x801A0053), 0x0203)
        self.assertEqual(ram.read_guest(0x801A004F, 2), b"\x00\x00")
        self.assertEqual(ram.read_guest(0x801A005C, 1), b"\x00")

    def test_capture_and_restore_progress_and_resources(self):
        p, ram = self.sample()
        cp = capture_checkpoint(ram, "Sakura practice")
        data = cp["payload"]
        self.assertEqual(data["summary"], {"max_health":10, "health":8, "ryo":100, "lives":3})
        self.assertEqual(data['map_id'],35)
        self.assertEqual(len(data['position']),3)
        self.assertAlmostEqual(data['position'][0],125.25)
        self.assertIn('rotation_b64',data)
        self.assertEqual(set(data['regions']),{'live','gamedata','header'})
        ram.write_guest(LIVE_ADDR + 12, struct.pack(">I",1))
        ram.write_guest(LIVE_ADDR + 16, struct.pack(">I",777))
        ram.write_guest(GAMEDATA_ADDR + 0x138, b"\xFE\xED\xBE\xEF")
        ram.write_guest(GAMEDATA_ADDR + 0x20, b"\xAA")
        ram.write_guest(HEADER_ADDR, b"Z"*12)
        ram.write_f32(0x801A0008, 993.0)
        r=restore_checkpoint(ram, cp)
        self.assertEqual(r["health"], 8)
        self.assertEqual(ram.u32(LIVE_ADDR+12), 8)
        self.assertEqual(ram.u32(LIVE_ADDR+16), 100)
        self.assertEqual(ram.read_guest(GAMEDATA_ADDR+0x138,4), bytes((0x138+i)*7%256 for i in range(4)))
        self.assertEqual(ram.read_guest(GAMEDATA_ADDR+0x20,1), bytes([0x20*7 % 256]))
        self.assertEqual(ram.read_guest(HEADER_ADDR,12), bytes(range(12)))
        self.assertAlmostEqual(ram.snapshot()["x"],125.25)
        self.assertEqual(ram.read_guest(GAMEDATA_ADDR+0x64,0x30), ram.read_guest(LIVE_ADDR,0x30))
        self.assertEqual(ram.read_guest(SHADOW_ADDR,0x304), ram.read_guest(GAMEDATA_ADDR,0x304))

    def test_refuses_cross_scene_and_character(self):
        p, ram=self.sample()
        cp=capture_checkpoint(ram, "Check")
        ram.write_guest(MAP_ADDR,b"\x00\x24")
        with self.assertRaisesRegex(ValueError,"map differs"):
            restore_checkpoint(ram,cp)
        ram.write_guest(MAP_ADDR,b"\x00\x23")
        write_u32(p,0x8015C5DC,2)
        with self.assertRaisesRegex(ValueError,"character differs"):
            restore_checkpoint(ram,cp)

    def test_refuses_unstable_gameplay_and_corruption(self):
        p, ram=self.sample()
        cp=capture_checkpoint(ram,"Check")
        cp["payload"]["summary"]["health"] = 999
        with self.assertRaisesRegex(ValueError,"checksum"):
            validate_checkpoint(cp)
        cp=capture_checkpoint(ram,"Check")
        write_u8(p,SUBMODE_ADDR,3)
        with self.assertRaisesRegex(ValueError,"Unsafe game submode"):
            restore_checkpoint(ram,cp)
        write_u8(p,PHASE_ADDR,2)
        with self.assertRaisesRegex(ValueError,"outside ordinary gameplay"):
            capture_checkpoint(ram,"blocked")

if __name__ == "__main__":
    unittest.main()

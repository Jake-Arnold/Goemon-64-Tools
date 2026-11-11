"""No-private-binary tests for REA feasibility classification."""
import struct
import tempfile
import unittest
from pathlib import Path

from rea_pilot_preflight import classify_header, inspect


def elf(arch: int, *, e_type: int = 2, e_machine: int = 8, endian: str = "big") -> bytes:
    prefix = ">" if endian == "big" else "<"
    result = bytearray(52)
    result[:6] = b"\x7fELF\x01" + (b"\x02" if endian == "big" else b"\x01")
    result[6] = 1
    struct.pack_into(prefix + "HH", result, 16, e_type, e_machine)
    struct.pack_into(prefix + "I", result, 36, arch)
    struct.pack_into(prefix + "H", result, 40, 52)
    return bytes(result)


class REAPreflightTests(unittest.TestCase):
    def check(self, data, state):
        self.assertEqual(classify_header(data[:64], len(data))["rea_mips_lane"], state)

    def test_raw_rom_is_not_mips_elf(self):
        self.check(b"\x80\x37\x12\x40" + b"\0" * 60, "NOT_APPLICABLE")

    def test_mips_ii_is_refused(self):
        self.check(elf(0x10000000), "UNSUPPORTED_DECLARED_ISA")

    def test_mips_iii_is_refused(self):
        self.check(elf(0x20000000), "UNSUPPORTED_DECLARED_ISA")

    def test_mips_32r2_requires_real_provider(self):
        self.check(elf(0x70000000), "POSSIBLE_REQUIRES_OFFICIAL_REA_ADMISSION")

    def test_legacy_mips_i_requires_real_provider(self):
        self.check(elf(0), "POSSIBLE_REQUIRES_OFFICIAL_REA_ADMISSION")

    def test_little_endian(self):
        self.assertEqual(classify_header(elf(0x50000000, endian="little"), 52)["byte_order"], "little")

    def test_wrong_machine(self):
        self.check(elf(0x70000000, e_machine=3), "NOT_MIPS")

    def test_wrong_type(self):
        self.check(elf(0x70000000, e_type=3), "UNSUPPORTED_ELF_TYPE")

    def test_missing_elf_bytes(self):
        self.check(b"\x7fELF\x01\x02", "MALFORMED")

    def test_unsupported_elf64(self):
        b = bytearray(elf(0x70000000)); b[4] = 2
        self.check(bytes(b), "UNSUPPORTED_ELF_CLASS")

    def test_declared_section_beyond_eof(self):
        b = bytearray(elf(0x70000000)); struct.pack_into(">I", b, 32, 4096); struct.pack_into(">H", b, 48, 40); struct.pack_into(">H", b, 50, 1)
        self.check(bytes(b), "MALFORMED")

    def test_only_private_file_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.elf"
            path.write_bytes(elf(0x10000000))
            result = inspect(path)
            self.assertFalse(result["provider_executed"])
            self.assertFalse(result["full_rom_verification"])
            self.assertFalse(result["private_data_exported"])
            self.assertNotIn(directory, str(result))
            self.assertEqual(result["size_bytes"], 52)


if __name__ == "__main__":
    unittest.main()

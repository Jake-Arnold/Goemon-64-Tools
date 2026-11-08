"""Synthetic ELF32 MIPS test object; no original game assets or source data."""
from pathlib import Path
import struct
import tempfile
import unittest

from decomp.elf_layout import pack_heap_noop_text, pack_heap_noop_file


def fixture():
    names = b'\0.text\0.options\0.reginfo\0.symtab\0.strtab\0.shstrtab\0'
    symbols = b'\0func_80035D84_36984\0'
    data = bytearray(52)
    sections = [(0,) * 10]

    def section(name, kind, flags, payload, link=0, align=4, entsize=0):
        offset = len(data)
        data.extend(payload)
        sections.append((names.index(name + b'\0'), kind, flags, 0,
                         offset, len(payload), link, 0, align, entsize))

    section(b'.text', 1, 6, bytes.fromhex('03E0000800000000') + bytes(8), align=16)
    section(b'.options', 0x7000000D, 0, bytes(32), align=8)
    section(b'.reginfo', 0x70000006, 2, bytes(24), align=4)
    entries = (bytes(16) + struct.pack('>IIIBBH', 0, 0, 16, 3, 0, 1) +
               struct.pack('>IIIBBH', 1, 0, 8, 0x12, 0, 1))
    section(b'.symtab', 2, 0, entries, link=5, align=4, entsize=16)
    section(b'.strtab', 3, 0, symbols, align=1)
    section(b'.shstrtab', 3, 0, names, align=1)
    shoff = len(data)
    for header in sections:
        data.extend(struct.pack('>10I', *header))
    data[:16] = b'\x7fELF\x01\x02\x01' + bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH', data, 16, 1, 8, 1, 0, 0, shoff,
                     0, 52, 0, 0, 40, len(sections), len(sections) - 1)
    return bytes(data), sections, shoff


class HeapNoopLayoutTests(unittest.TestCase):
    def test_metadata_only_no_payload_or_instruction_changes(self):
        original, sections, shoff = fixture()
        modified, evidence = pack_heap_noop_text(original)
        self.assertEqual(len(original), len(modified))
        self.assertEqual(evidence['payload_bytes_changed'], 0)
        self.assertEqual((evidence['old_size'], evidence['new_size']), (16, 8))
        allowed = set(range(shoff + 40 + 20, shoff + 40 + 24)) | set(
            range(shoff + 40 + 32, shoff + 40 + 36))
        self.assertTrue(all(a == b or i in allowed for i, (a, b) in enumerate(zip(original, modified))))
        self.assertEqual(original[sections[1][4]:sections[1][4] + 16],
                         modified[sections[1][4]:sections[1][4] + 16])
        self.assertEqual(struct.unpack_from('>I', modified, shoff + 40 + 20)[0], 8)
        self.assertEqual(struct.unpack_from('>I', modified, shoff + 40 + 32)[0], 4)
        with self.assertRaises(ValueError):
            pack_heap_noop_text(modified)

    def test_wrong_symbol_and_padding_and_allocated_data_rejected(self):
        original, sections, shoff = fixture()
        mutations = (
            (sections[1][4] + 8, b'\x01'),
            (sections[1][4], b'\x01'),
            (shoff + 40 + 20, struct.pack('>I', 8)),
            (shoff + 40 + 32, struct.pack('>I', 4)),
            (sections[4][4] + 32 + 8, struct.pack('>I', 16)),
            (sections[4][4] + 32 + 12, b'\x13'),
            (shoff + 2 * 40 + 8, struct.pack('>I', 2)),
            (shoff + 3 * 40 + 4, struct.pack('>I', 9)),
        )
        for offset, replacement in mutations:
            with self.subTest(offset=offset, replacement=replacement):
                changed = bytearray(original)
                changed[offset:offset + len(replacement)] = replacement
                with self.assertRaises(ValueError):
                    pack_heap_noop_text(bytes(changed))
        for bad in (b'', original[:30], original[:-1]):
            with self.assertRaises(ValueError):
                pack_heap_noop_text(bad)

    def test_exclusive_backup_and_validation_before_writes(self):
        original, _, _ = fixture()
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'synthetic.o'
            target.write_bytes(original)
            pack_heap_noop_file(target)
            backup = target.with_name(target.name + '.before-heap-noop-layout')
            self.assertEqual(backup.read_bytes(), original)
            target.write_bytes(original)
            with self.assertRaises(FileExistsError):
                pack_heap_noop_file(target)
            self.assertEqual(target.read_bytes(), original)
            target.write_bytes(b'corrupted')
            with self.assertRaises(ValueError):
                pack_heap_noop_file(target)
            self.assertEqual(target.read_bytes(), b'corrupted')


if __name__ == '__main__':
    unittest.main()

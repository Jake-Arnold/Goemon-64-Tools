import struct
import unittest

from decomp import vm_dialogue as vm


class DialogueTest(unittest.TestCase):
    def test_command_to_decoded_text(self):
        base = 0x08000000
        resource = struct.pack(">II9h", 0x8010, base + 8,
                               33, 0, 90, -60, 17, 1, -33, 0x7FFF, -1)
        offset = vm.text_operand(resource, base, 0)
        self.assertEqual(offset, 8)
        self.assertEqual(vm.format_tokens(vm.read_tokens(resource, offset)),
                         "A z\n1!<token:-33><token:32767>")

    def test_controls_keep_page_and_window_events_distinct(self):
        self.assertEqual(vm.format_tokens((-70, -63, -61, -62, -71)),
                         "<open-window><clear-glyphs><state-3><state-4><close-window>")
        self.assertEqual(vm.read_tokens(b"\xff\xff\x00\x21", 0), ())

    def test_resource_ids_are_one_based_and_reject_compressed_rows(self):
        rom = bytearray(vm.SOURCE_TABLE + 16)
        rom[0x100:0x106] = b"sample"
        struct.pack_into(">II", rom, vm.SOURCE_TABLE + 4, 0x100, 0x106)
        struct.pack_into(">II", rom, vm.VIRTUAL_TABLE + 8, 0x08000000, 0x08000006)
        self.assertEqual(vm.resource_data(rom, 2), (0x100, 0x08000000, b"sample"))
        for resource_id in (0, 1, 3, vm.MAX_RESOURCE_ID + 1):
            with self.subTest(resource_id=resource_id), self.assertRaises(ValueError):
                vm.resource_data(rom, resource_id)
        struct.pack_into(">I", rom, vm.SOURCE_TABLE + 4, 0x80000100)
        with self.assertRaises(ValueError):
            vm.resource_data(rom, 2)

    def test_command_rejects_bad_opcode_alignment_and_target(self):
        base = 0x08000000
        for opcode, operand, offset in (
            (0x8011, base, 0), (0x8010, base, -4), (0x8010, base, 2),
            (0x8010, base + 1, 0), (0x8010, base + 8, 0),
            (0x8010, base - 2, 0), (0x8010, 0x80000000, 0),
        ):
            with self.subTest(opcode=opcode, operand=operand, offset=offset), self.assertRaises(ValueError):
                vm.text_operand(struct.pack(">II", opcode, operand), base, offset)

    def test_token_walker_is_bounded_by_resource_and_limit(self):
        record = struct.pack(">3h", 33, 34, -1)
        self.assertEqual(vm.read_tokens(record, 0, limit=3), (33, 34))
        for data, offset, limit in (
            (record[:-1], 0, 3), (record, 0, 2), (record, 1, 3),
            (record, -2, 3), (record, 6, 3), (record, 0, 0),
        ):
            with self.subTest(data=data, offset=offset, limit=limit), self.assertRaises(ValueError):
                vm.read_tokens(data, offset, limit=limit)

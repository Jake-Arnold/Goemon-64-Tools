"""Safe long/short Goemon USA dialogue relocation and 16 MiB retail repacking."""
from __future__ import annotations

import hashlib
import os
import struct
import tempfile
import unittest
from pathlib import Path

from practice.dialogue_rom import (
    MAX_RESOURCE_GROWTH, RESOURCE_TABLE, ROM_SIZE, VIRTUAL_TABLE,
    DialogueRecord, decode_tokens, extract_dialogue, load_usa_image,
    patch_image, save_patched_image, validate_flexible_replacement,
)
from practice.dialogue_repack import (
    USA_RETAIL_SHA1, load_usa_retail, repack_usa_retail, save_retail_rom,
)


class FlexibleEncodingTests(unittest.TestCase):
    def test_longer_and_shorter_preserve_controls(self):
        record = DialogueRecord(96, 2, 0x750000, (40, -60, 65, -61), (0x10,))
        self.assertEqual(validate_flexible_replacement(record, 'I love N64\na<state-3>')[-3:],
                         (-60, 65, -61))
        self.assertEqual(validate_flexible_replacement(record, 'I\na<state-3>'),
                         (41, -60, 65, -61))
        for invalid in ('Ian<state-3>', 'I\naa', 'I\na<state-4>', 'I\na<state-3>\n'):
            with self.assertRaises(ValueError):
                validate_flexible_replacement(record, invalid)

    def test_reject_too_many_tokens(self):
        record = DialogueRecord(96, 2, 0x750000, (33,), (0x10,))
        with self.assertRaisesRegex(ValueError, 'maximum'):
            validate_flexible_replacement(record, 'A' * 4097)


class OriginalVariableRomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        if not path:
            raise unittest.SkipTest('Set GOEMON_USA_DECOMPRESSED_ROM for ROM-backed tests')
        cls.source = Path(path)
        cls.image = load_usa_image(path)
        cls.records = extract_dialogue(cls.image)
        cls.long = next(r for r in cls.records if r.resource_id == 97 and r.text_offset == 4)
        cls.short = next(r for r in cls.records if r.resource_id == 96 and r.text_offset == 0x1CC0)

    def _resource(self, image, id):
        start, end = struct.unpack_from('>II', image, RESOURCE_TABLE + (id - 1) * 4)
        base, upper = struct.unpack_from('>II', image, VIRTUAL_TABLE + (id - 1) * 8)
        return start, end, base, upper

    def test_longer_edit_moves_record_and_all_known_refs(self):
        r = self.long
        replacement = r.text.replace('Yae:', 'People of the world! Yae:', 1)
        image = patch_image(self.image, self.records, {r.key: replacement})
        start, end, virtual, upper = self._resource(self.image, r.resource_id)
        new_start, new_end, new_virtual, new_upper = self._resource(image, r.resource_id)
        self.assertEqual(new_start, start)
        self.assertEqual(new_virtual, virtual)
        self.assertGreater(new_end, end)
        self.assertEqual(new_end - end, new_upper - upper)
        self.assertEqual(image[start+r.text_offset:start+r.text_offset+(len(r.tokens)+1)*2],
                         self.image[start+r.text_offset:start+r.text_offset+(len(r.tokens)+1)*2])
        operands = set()
        for ref in r.references:
            opcode, operand = struct.unpack_from('>II', image, start+ref)
            self.assertEqual(opcode, 0x8010)
            self.assertGreater(operand, virtual+r.text_offset)
            operands.add(operand)
        self.assertEqual(len(operands), 1)
        relocated = next(iter(operands)) - virtual
        found = []
        for o in range(relocated, new_end-new_start, 2):
            token = struct.unpack_from('>h', image, new_start+o)[0]
            if token == -1:
                break
            found.append(token)
        self.assertEqual(decode_tokens(tuple(found)), replacement)
        self.assertEqual(len(image), ROM_SIZE)
        # Resource 98 content is unchanged though its physical location shifted.
        after = self._resource(image, r.resource_id+1)
        before = self._resource(self.image, r.resource_id+1)
        self.assertEqual(image[after[0]:after[1]], self.image[before[0]:before[1]])

    def test_two_resource_edits_relocate_independently(self):
        a, b = self.long, self.short
        edits = {a.key: a.text + 'Extra!', b.key: b.text.replace('UFO', 'U', 1)}
        # b may contain control codes; removing two spaces is allowed.
        output = patch_image(self.image, self.records, edits)
        for r in (a, b):
            before = self._resource(self.image, r.resource_id)
            after = self._resource(output, r.resource_id)
            self.assertGreater(after[3] - before[3], 0)
            self.assertEqual(after[1] - after[0] - (before[1] - before[0]),
                             after[3] - before[3])
        self.assertEqual(len(output), ROM_SIZE)
        self.assertEqual(output[:0x10], self.image[:0x10])

    def test_large_growth_rejected(self):
        r = self.long
        text = 'A' * (MAX_RESOURCE_GROWTH // 2 + 50)
        with self.assertRaises(ValueError):
            patch_image(self.image, self.records, {r.key: text})

    def test_expanded_decompressed_output_has_correct_header_crc(self):
        r = self.long
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'expanded.decompressed.z64'
            digest = save_patched_image(self.source, dest, self.records,
                                        {r.key: r.text + ' Here is longer text.'})
            output = dest.read_bytes()
            self.assertEqual(hashlib.sha1(output).hexdigest(), digest)
            self.assertEqual(len(output), ROM_SIZE)
            from practice.dialogue_repack import _update_usa_crc
            verify = bytearray(output)
            _update_usa_crc(verify)
            self.assertEqual(bytes(verify), output)
            self.assertNotEqual(output[0x10:0x18], self.image[0x10:0x18])

    def test_retail_rebuild_reproduces_original(self):
        retail_path = os.environ.get('GOEMON_USA_RETAIL_ROM')
        if not retail_path:
            self.skipTest('Set GOEMON_USA_RETAIL_ROM')
        try:
            import lzkn64
        except ImportError:
            self.skipTest('lzkn64 not installed')
        original = load_usa_retail(retail_path)
        output = repack_usa_retail(self.image, original)
        self.assertEqual(hashlib.sha1(output).hexdigest(), USA_RETAIL_SHA1)
        self.assertEqual(output, original)

    def test_repacked_changed_resource_decompresses_identically(self):
        retail_path = os.environ.get('GOEMON_USA_RETAIL_ROM')
        if not retail_path:
            self.skipTest('Set GOEMON_USA_RETAIL_ROM')
        try:
            import lzkn64
        except ImportError:
            self.skipTest('lzkn64 not installed')
        original = load_usa_retail(retail_path)
        r = self.long
        patched = patch_image(self.image, self.records, {r.key: r.text + ' Secret new words.'})
        built = repack_usa_retail(patched, original)
        self.assertEqual(len(built), 16 * 1024 * 1024)
        row = RESOURCE_TABLE + (r.resource_id - 1) * 4
        compressed_start, compressed_end = struct.unpack_from('>II', built, row)
        self.assertTrue(compressed_start & 0x80000000)
        compressed_start &= 0x7FFFFFFF
        compressed_end &= 0x7FFFFFFF
        decomp_start, decomp_end = struct.unpack_from('>II', patched, row)
        self.assertEqual(lzkn64.decompress(built[compressed_start:compressed_end]),
                         patched[decomp_start:decomp_end])
        self.assertNotEqual(built, original)

    def test_retail_build_refuses_source_overwrite(self):
        retail_path = os.environ.get('GOEMON_USA_RETAIL_ROM')
        if not retail_path:
            self.skipTest('Set GOEMON_USA_RETAIL_ROM')
        with self.assertRaises(ValueError):
            save_retail_rom(self.source, retail_path, self.source,
                            self.records, {self.long.key: self.long.text + ' Hi'})
        with self.assertRaises(ValueError):
            save_retail_rom(self.source, retail_path, retail_path,
                            self.records, {self.long.key: self.long.text + ' Hi'})


if __name__ == '__main__':
    unittest.main()

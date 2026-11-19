"""ROM-free contract regressions for original-VMA USA file_11 callback discovery."""
from __future__ import annotations

import json
import struct
import unittest
from pathlib import Path
from unittest.mock import patch

from decomp.research import file11_expansion_probe as probe
from decomp.overlay_file11 import ROM_START, VMA_START


class File11ExpansionTests(unittest.TestCase):
    def original_shape(self, delay=0xAFA5001C, target=0x801E3AC0):
        return struct.pack('>8I', *probe.PREFIX,
                           0x0C000000 | ((target >> 2) & 0x3FFFFFF), delay,
                           *probe.SUFFIX)

    def test_second_arg_spill(self):
        actual = probe.identify_direct_wrapper(self.original_shape())
        self.assertEqual(actual, {'target_vma': 0x801E3AC0,
                                  'mode': 'two_arg', 'constant': None})

    def test_one_arg_nop_delay(self):
        self.assertEqual(probe.identify_direct_wrapper(self.original_shape(0))['mode'], 'one_arg')

    def test_numeric_event_arguments(self):
        for num in (12, 13, 14, 15, 16, 18):
            item = probe.identify_direct_wrapper(self.original_shape(0x24050000 | num))
            self.assertEqual((item['mode'], item['constant']), ('constant_arg', num))

    def test_null_argument_requires_zero_arg_c_function(self):
        item = probe.identify_direct_wrapper(self.original_shape(0x00002025))
        src = probe.render_wrapper(dict(name='func_801FA6C4_5B65D4', **item))
        self.assertIn('(void)', src)
        self.assertIn('handler((void *)0)', src)

    def test_reject_wrong_instruction_extent(self):
        self.assertIsNone(probe.identify_direct_wrapper(self.original_shape()[:28]))

    def test_reject_non_jal_or_modified_prologue(self):
        b = bytearray(self.original_shape())
        b[8:12] = bytes.fromhex('00000000')
        self.assertIsNone(probe.identify_direct_wrapper(bytes(b)))
        b = bytearray(self.original_shape())
        b[0] = 0
        self.assertIsNone(probe.identify_direct_wrapper(bytes(b)))

    def test_reject_unknown_delay_slot(self):
        self.assertIsNone(probe.identify_direct_wrapper(self.original_shape(0x24040003)))

    def test_discovery_excludes_promoted_wrappers_and_noops(self):
        rom = bytearray(probe.TEXT_END + 4)
        name, _, _, _ = next(x for x in probe.PROMOTED_CHARACTER_FUNCTIONS if x[2] == 32)
        vma = int(name.split('_')[1], 16)
        off = probe.ROM_START + vma - probe.VMA_START
        rom[off:off+32] = self.original_shape()
        eligible = probe.ROM_START + 0x1200
        rom[eligible:eligible+32] = self.original_shape()
        nop = eligible + 0x80
        rom[nop:nop+12] = probe.ORIGINAL_NOOP
        promoted_nop, promoted_off = probe.PROMOTED_NOOP_ENTRIES()[0]
        rom[promoted_off:promoted_off+12] = probe.ORIGINAL_NOOP
        class Elf:
            def symbols(self_inner):
                return [
                    (name, vma, 32, 2, 1),
                    (f'func_{probe.VMA_START+eligible-probe.ROM_START:08X}_{eligible:X}',
                     probe.VMA_START+eligible-probe.ROM_START, 32, 2, 1),
                    (f'func_{probe.VMA_START+nop-probe.ROM_START:08X}_{nop:X}',
                     probe.VMA_START+nop-probe.ROM_START, 12, 2, 1),
                    (promoted_nop, probe.VMA_START+promoted_off-probe.ROM_START, 12, 2, 1),
                    ('data', probe.VMA_START+eligible+0x40-probe.ROM_START, 32, 1, 1),
                ]
        wrappers, noops = probe.discover(bytes(rom), Elf())
        self.assertEqual(len(wrappers), 1)
        self.assertEqual(len(noops), 1)
        self.assertEqual(wrappers[0]['rom_offset'], eligible)
        self.assertEqual(noops[0]['rom_offset'], nop)

    def test_noop_template_exact(self):
        item = {'name': 'func_801CB5C4_5874D4'}
        self.assertEqual(probe.render_noop(item),
                         'void func_801CB5C4_5874D4(void *a0, void *a1) {}\n')

    def test_float_reset_source_has_two_distinct_original_functions(self):
        self.assertEqual(probe.FLOAT_RESET_SOURCE.count('0.0f'), 4)
        for name, off in probe.FLOAT_RESET_NAMES:
            self.assertIn(name, probe.FLOAT_RESET_SOURCE)

    def test_wrong_rom_and_elf_fail_closed(self):
        with self.assertRaises(ValueError):
            probe.checked_inputs(b'not a ROM', b'not an ELF')
        with patch.object(probe.hashlib, 'sha1') as fake:
            fake.return_value.hexdigest.return_value = probe.ROM_SHA1
            with self.assertRaises(ValueError):
                probe.checked_inputs(bytes(probe.ROM_LENGTH), b'not a valid baseline')

    def test_native_probe_rejects_compiled_shorter_than_original(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            with patch.object(probe.subprocess, 'run') as command:
                def output(_cmd, **_kw):
                    (Path(tmp) / 'candidate.bin').write_bytes(b'\x00' * 4)
                command.side_effect = output
                with self.assertRaises(ValueError):
                    probe.native_probe('void foo(void) {}', 0x801E0000, {},
                                       Path('cc'), Path('ld'), Path('objcopy'),
                                       Path(tmp), b'\0'*32, {})


if __name__ == '__main__':
    unittest.main()

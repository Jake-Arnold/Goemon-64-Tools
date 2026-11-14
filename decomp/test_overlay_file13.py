"""Fail-closed file_13 staging and IDO object-layout tests."""
from unittest import TestCase

from decomp import overlay_file13
from decomp.elf_layout import pack_overlay_function_text
from decomp.test_overlay_file12 import relocatable_file12_callback
from decomp.verify import stage_file13_splat


FUNCTION = 'func_801D3954_5FED34'
RELOCATIONS = (
    (0, 5, 'D_8020EED0_63A2B0'),
    (4, 6, 'D_8020EED0_63A2B0'),
)
SYMBOL_SHAPES = {'D_8020EED0_63A2B0': (1, 4)}


def pinned_splat():
    return f"""sha1: {overlay_file13.ROM_SHA1}
segments:
  - name: file_13
    type: code
    start: 0x5F6840
    vram: 0x801CB460
    bss_size: 0x80
    subalign: 16
    overlay: yes
    exclusive_ram_id: static_overlay_1
    subsegments:
    - [0x5F6840, asm]
    - [0x634E30, data]
  - name: file_14
    type: code
    start: 0x63A2B0
"""


def stage_record():
    function = overlay_file13.FUNCTIONS[FUNCTION]
    return {
        'format': 'goemon-file13-c-stage-v1',
        'source': 'impact_hp_clamp.c',
        'source_sha256': '0' * 64,
        'compiler_object_sha256': '1' * 64,
        'object_sha256': '2' * 64,
        'function': {
            'name': FUNCTION,
            'vma': function[0],
            'rom_offset': function[1],
            'size': function[2],
        },
    }


class OverlayFile13Tests(TestCase):
    def test_layout_pins_file_table_boundary_and_overlay_window(self):
        layout = overlay_file13.validate_layout(pinned_splat())
        self.assertEqual(layout['rom_start'], 0x5F6840)
        self.assertEqual(layout['rom_end'], 0x63A2B0)
        self.assertEqual(layout['vma_start'], 0x801CB460)
        with self.assertRaisesRegex(ValueError, 'file_14'):
            overlay_file13.validate_layout(pinned_splat().replace(
                'start: 0x63A2B0', 'start: 0x63A2B4'))

    def test_splat_split_places_only_reviewed_function_in_c_segment(self):
        updated, before, after = stage_file13_splat(pinned_splat(), stage_record())
        self.assertEqual(before, 'file_13_before_5FED34')
        self.assertEqual(after, 'file_13_after_5FED5C')
        self.assertIn('subalign: null', updated)
        self.assertIn('- [0x5FED34, c, impact_hp_clamp]', updated)
        self.assertIn('- [0x5FED5C, asm, file_13_after_5FED5C]', updated)
        self.assertIn('- [0x634E30, data]', updated)

    def test_ido_overlay_object_packing_trims_only_eight_zero_bytes(self):
        code = bytes(range(40))
        original, _ = relocatable_file12_callback(
            code, tail=bytes(8), function_name=FUNCTION,
            relocations=RELOCATIONS, symbol_shapes=SYMBOL_SHAPES,
        )
        packed, evidence = pack_overlay_function_text(
            original, FUNCTION, 40, 8, RELOCATIONS, SYMBOL_SHAPES,
            'file_13 HP clamp', 'file13_hp_clamp',
        )
        self.assertEqual(evidence['zero_padding_bytes'], 8)
        self.assertEqual(evidence['payload_bytes_changed'], 0)
        self.assertEqual(evidence['new_size'], 40)
        self.assertEqual(len(packed), len(original))

    def test_ido_overlay_object_packing_rejects_nonzero_tail(self):
        original, _ = relocatable_file12_callback(
            bytes(range(40)), tail=bytes(7) + b'\x01',
            function_name=FUNCTION, relocations=RELOCATIONS,
            symbol_shapes=SYMBOL_SHAPES,
        )
        with self.assertRaisesRegex(ValueError, 'padding'):
            pack_overlay_function_text(
                original, FUNCTION, 40, 8, RELOCATIONS, SYMBOL_SHAPES,
                'file_13 HP clamp', 'file13_hp_clamp',
            )

    def test_relocation_check_allows_only_named_elf_symbol_type_upgrades(self):
        original = (
            (0x801D3954, 5, 'D_8020EED0_63A2B0', 0x8020EED0,
             0, 0, 1, 0xFFF1, None),
            (0x801D3958, 6, 'D_8020EED0_63A2B0', 0x8020EED0,
             0, 0, 1, 0xFFF1, None),
        )
        candidate = tuple(row[:5] + (1,) + row[6:] for row in original)
        proof = overlay_file13.normalize_relocation_metadata(original, candidate)
        self.assertEqual(proof['symbol_kind_upgrades'], {'D_8020EED0_63A2B0': 2})
        wrong = (candidate[0], candidate[1][:2] + ('unrelated',) + candidate[1][3:])
        with self.assertRaisesRegex(ValueError, 'target changed'):
            overlay_file13.normalize_relocation_metadata(original, wrong)

        function_alias = (
            (0x801DDE00, 5, '.L0800AD60_6BE000', 0x0800AD60,
             0, 0, 1, 70, None),
        )
        function_alias_candidate = (
            (0x801DDE00, 5, '.L0800AD60_6BE000', 0x0800AD60,
             0, 2, 1, 70, None),
        )
        alias_proof = overlay_file13.normalize_relocation_metadata(
            function_alias, function_alias_candidate)
        self.assertEqual(alias_proof['symbol_kind_upgrades'], {
            '.L0800AD60_6BE000': 1,
        })

"""Original USA Object structure offset tests; no emulator required."""
import struct
import tkinter as tk
import unittest
from practice.model_object_probe import (
    GRAPHICS_1_OFFSET, GRAPHICS_2_OFFSET, OVERLAY_INFO_OFFSET,
    OBJECT_HEADER_BYTES, interpret_usa_object_graphics, parse_snapshot_hex,
)
from practice.model_object_probe_ui import ModelObjectProbeDialog


def make_snapshot():
    b=bytearray(OBJECT_HEADER_BYTES)
    struct.pack_into('>I',b,GRAPHICS_1_OFFSET,0x08001234)
    struct.pack_into('>I',b,GRAPHICS_2_OFFSET,0x09005678)
    # Last overlay ends at +0x64, followed by unknown_64 flags.
    for i in range(6):
        struct.pack_into('>HHI',b,OVERLAY_INFO_OFFSET+i*8,
                         [0x120,0x124,0,0xFFFF,0x12B,0x12C][i],
                         0x55AA,0x80300000+0x1000*i)
    b[0x64:0x68]=b'\x9A\xBC\xDE\xF0'
    return bytes(b)


class ObjectStructureTests(unittest.TestCase):
    def test_source_offsets_and_big_endian_metadata(self):
        self.assertEqual((GRAPHICS_1_OFFSET,GRAPHICS_2_OFFSET,OVERLAY_INFO_OFFSET),(0x2C,0x30,0x34))
        self.assertEqual(OVERLAY_INFO_OFFSET+6*8,0x64)
        result=interpret_usa_object_graphics(make_snapshot())
        self.assertEqual(result['region'],'usa')
        self.assertEqual(result['graphics_1'],'0x08001234')
        self.assertEqual(result['graphics_2'],'0x09005678')
        self.assertEqual(result['overlays'][0]['file_id'],0x120)
        self.assertEqual(result['overlays'][1]['vram_addr'],'0x80301000')
        self.assertFalse(result['overlays'][3]['plausible_rom_file_id'])
        self.assertEqual(result['overlays'][5]['file_id'],0x12C)
        self.assertIn('not authenticated',result['evidence'])

    def test_hex_formats_and_no_address_columns(self):
        b=make_snapshot()
        self.assertEqual(parse_snapshot_hex(b.hex()),b)
        self.assertEqual(parse_snapshot_hex('0x'+b.hex()),b)
        self.assertEqual(parse_snapshot_hex(' '.join(f'{v:02X}' for v in b)),b)
        for input_value in ('', '0x11','80 00 11', '80000000: 00 10',
                            ' '.join(['80']*103),b.hex()+'00', ' '.join(['GG']*104)):
            with self.subTest(input_value=input_value[:25]):
                with self.assertRaises(ValueError):parse_snapshot_hex(input_value)
        with self.assertRaises(ValueError):interpret_usa_object_graphics(b[:12])

    def test_headless_dialog(self):
        root=tk.Tk();root.withdraw()
        try:
            dlg=ModelObjectProbeDialog(root)
            dlg.raw.insert('1.0',make_snapshot().hex())
            dlg.decode()
            self.assertIn('0x08001234',dlg.result.get('1.0','end'))
            self.assertIn('0x80305000',dlg.result.get('1.0','end'))
            self.assertIn('no snapshot persisted',dlg.status.get())
            dlg.raw.delete('1.0','end')
            dlg.decode()
            self.assertIn('Invalid input:',dlg.status.get())
            dlg.window.destroy()
        finally:root.destroy()


if __name__ == '__main__':unittest.main()

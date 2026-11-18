"""Synthetic original-overlay resource table and real-ROM optional regressions."""
from __future__ import annotations
import os
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from practice.model_research import (
    EXPECTED_GRAPHICS_IDS, PLAYER_FRAGMENT_SPANS, PLAYER_TABLE_OFFSETS,
    decode_geometry, extract_player_fragment, player_graphics_resources,
)


def make_fake_files(region, slot=0):
    table = bytearray(PLAYER_TABLE_OFFSETS[region] + 16)
    struct.pack_into('>8H', table, PLAYER_TABLE_OFFSETS[region], *EXPECTED_GRAPHICS_IDS)
    start, stop = PLAYER_FRAGMENT_SPANS[region][slot]
    meshdata = bytearray(max(stop + 8, 0x3000))
    for i, coords in enumerate(((0,0,0), (12,0,0), (0,12,0))):
        struct.pack_into('>hhhHhhBBBB', meshdata, 0x80 + i*16, *coords, 0,0,0,60,100,140,255)
    struct.pack_into('>II', meshdata, start, 0x04000C00, 0x09000080)
    struct.pack_into('>II', meshdata, start+8, 0xBF000000, (2<<17)|(1<<9)|(0<<1))
    struct.pack_into('>II', meshdata, start+16, 0xB8000000, 0)
    class FakeFiles:
        sha1 = 'synthetic-sha1'
        def file(self, file_id):
            return bytes(table if file_id == 11 else meshdata)
    return FakeFiles()


class PlayerResourcesTests(unittest.TestCase):
    def test_four_source_confirmed_ids_and_separate_region_offsets(self):
        for region in ('usa', 'japan_0'):
            with self.subTest(region=region):
                result = player_graphics_resources(make_fake_files(region), region)
                self.assertEqual([r['file_id'] for r in result], [0x120,0x124,0x128,0x12C])
                self.assertEqual([r['adjacent_file_id'] for r in result], [0x123,0x127,0x12B,0x12F])
                self.assertEqual([r['segment'] for r in result], [9]*4)
                self.assertEqual([r['slot'] for r in result], list(range(4)))

    def test_region_and_hash_gate_reject_layout_mismatch(self):
        for region in ('usa', 'japan_0'):
            fake=make_fake_files(region)
            with self.subTest(region=region):
                with patch('practice.model_research.RomFiles' if region=='usa' else 'practice.model_research.JapanRomFiles', return_value=fake):
                    report, mesh=extract_player_fragment(b'test', region, 0)
                self.assertEqual(report['file_id'],0x120)
                self.assertEqual(report['segment'],9)
                self.assertEqual(report['slot'],0)
                self.assertEqual(mesh.triangle_count,1)
                self.assertTrue(mesh.ended)
                self.assertIn('partial',report['limitations'])
        for bad in (-1, 4, 0.0, True):
            with self.assertRaises(ValueError):extract_player_fragment(b'', 'usa',bad)
        with self.assertRaises(ValueError):extract_player_fragment(b'', 'japan_1',0)
        with self.assertRaises(ValueError):player_graphics_resources(make_fake_files('usa'),'japan_1')

    def test_rejects_drifted_table_instead_of_guessing(self):
        fake=make_fake_files('usa')
        class Drift:
            def file(self, file_id):
                data=bytearray(fake.file(file_id))
                if file_id==11:data[PLAYER_TABLE_OFFSETS['usa']]=0
                return data
        with self.assertRaisesRegex(ValueError,'does not match'):
            player_graphics_resources(Drift(),'usa')

    def test_segment_nine_mesh_and_eight_backward_compat(self):
        fake=make_fake_files('usa')
        start,end=PLAYER_FRAGMENT_SPANS['usa'][0]
        mesh=decode_geometry(fake.file(0x120),start,end,segment=9)
        self.assertEqual(mesh.triangles[0],((0,12,0),(12,0,0),(0,0,0)))
        with self.assertRaisesRegex(ValueError,'segment-08'):
            decode_geometry(fake.file(0x120),start,end,segment=8)
        with self.assertRaisesRegex(ValueError,'Unsupported'):
            decode_geometry(fake.file(0x120),start,end,segment=7)

    def test_real_original_roms_when_supplied(self):
        # Tests can run anywhere without proprietary ROM inputs. Local original
        # ROM validation becomes exhaustive when the user supplies both paths.
        paths={
            'usa':os.environ.get('GOEMON_TEST_USA_ROM'),
            'japan_0':os.environ.get('GOEMON_TEST_JP_ROM'),
        }
        if not all(paths.values()):
            self.skipTest('GOEMON_TEST_USA_ROM and GOEMON_TEST_JP_ROM are not set')
        expected=(90,52,12,25)
        for region, path in paths.items():
            rom=Path(path).read_bytes()
            for slot, count in enumerate(expected):
                with self.subTest(region=region,slot=slot):
                    report, mesh=extract_player_fragment(rom,region,slot)
                    self.assertTrue(mesh.ended)
                    self.assertEqual(mesh.triangle_count,count)
                    self.assertEqual(report['segment'],9)
                    self.assertEqual(len([w for w in mesh.warnings if 'not loaded' in w]),0)


if __name__=='__main__':
    unittest.main()

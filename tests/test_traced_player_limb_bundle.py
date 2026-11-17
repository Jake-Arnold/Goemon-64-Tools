"""Captured PJ64 USA four-list graphics bundle, source-authenticated in both ROMs."""
import os
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from practice.model_research import (
    EXPECTED_GRAPHICS_IDS, PLAYER_TABLE_OFFSETS,
    PJ64_CAPTURED_LIMB_ROOTS_USA, PJ64_CAPTURED_LIMB_ROOTS_DELTA,
    PJ64_CAPTURED_LIMB_FACES, PJ64_CAPTURED_TEXTURE_REFS_USA,
    extract_traced_player_limb_bundle, inspect_traced_skeleton_records,
)


def synthetic_files(region, altered=None):
    # A minimal stream with the same proven display-list structure but entirely
    # synthetic vertex/tri data. No ROM or original assets are embedded.
    code = bytearray(PLAYER_TABLE_OFFSETS[region]+32)
    struct.pack_into('>8H', code, PLAYER_TABLE_OFFSETS[region], *EXPECTED_GRAPHICS_IDS)
    data = bytearray(0x9000)
    for i,coords in enumerate(((0,0,0),(12,0,0),(0,12,0))):
        struct.pack_into('>hhhHhhBBBB',data,0x8000+16*i,*coords,0,0,0,50,80,110,255)
    for index, base_root in enumerate(PJ64_CAPTURED_LIMB_ROOTS_USA):
        root=base_root+PJ64_CAPTURED_LIMB_ROOTS_DELTA[region]
        texture=PJ64_CAPTURED_TEXTURE_REFS_USA[index]+PJ64_CAPTURED_LIMB_ROOTS_DELTA[region]
        struct.pack_into('>II',data,root,0xE7000000,0)
        struct.pack_into('>II',data,root+8,0xFD100000,texture)
        struct.pack_into('>II',data,root+16,0x04000C00,0x09008000)
        for j in range(PJ64_CAPTURED_LIMB_FACES[index]//2):
            tri=(0<<17)|(1<<9)|(2<<1)
            struct.pack_into('>II',data,root+24+j*8,0xB1000000|tri,tri)
        struct.pack_into('>II',data,root+24+(PJ64_CAPTURED_LIMB_FACES[index]//2)*8,0xB8000000,0)
    if altered:
        byte_offset,new_value=altered
        struct.pack_into('>I',data,byte_offset,new_value)
    class FakeFiles:
        sha1='synthetic-fake-sha'
        def file(self,num):
            return bytes(code if num==11 else data)
    return FakeFiles()


class TracedPlayerTests(unittest.TestCase):
    def test_synthetic_four_part_bundles_and_region_translation(self):
        for region in ('usa','japan_0'):
            with self.subTest(region=region):
                with patch('practice.model_research.RomFiles' if region=='usa' else
                           'practice.model_research.JapanRomFiles',return_value=synthetic_files(region)):
                    report,mesh=extract_traced_player_limb_bundle(b'synthetic',region)
                self.assertEqual(report['triangles'],84)
                self.assertEqual(len(report['parts']),4)
                self.assertEqual([x['triangles'] for x in report['parts']],[20,20,22,22])
                self.assertTrue(mesh.ended)
                self.assertEqual(report['segment'],9)
                self.assertEqual(len(set(mesh.rgb)),4)
                self.assertIn('not original', ' '.join(mesh.warnings))

    def test_rejects_corrupted_list_and_out_of_region(self):
        with self.assertRaises(ValueError):extract_traced_player_limb_bundle(b'', 'japan_1')
        for position,value in [(0x47f8,0),(0x47f8+12,0x0900FFFF)]:
            with self.subTest(position=position):
                with patch('practice.model_research.RomFiles',return_value=synthetic_files('usa',(position,value))):
                    with self.assertRaisesRegex(ValueError,'prologue|texture pointer'):
                        extract_traced_player_limb_bundle(b'synthetic','usa')

    def test_synthetic_file_without_screenshot_is_not_claimed_exact(self):
        for region in ('usa','japan_0'):
            with patch('practice.model_research.RomFiles' if region=='usa' else
                       'practice.model_research.JapanRomFiles', return_value=synthetic_files(region)):
                result=inspect_traced_skeleton_records(b'synthetic',region)
            self.assertEqual(result['candidate_record_count'],0)
            self.assertFalse(result['screenshot_match'])
            self.assertIsNone(result['screenshot_index'])

    def test_real_original_roms(self):
        paths={
          'usa':os.environ.get('GOEMON_TEST_USA_ROM'),
          'japan_0':os.environ.get('GOEMON_TEST_JP_ROM'),
        }
        if not all(paths.values()):self.skipTest('Original USA/Japan ROM environment paths not supplied')
        for region,path in paths.items():
            with self.subTest(region=region):
                report,mesh=extract_traced_player_limb_bundle(Path(path).read_bytes(),region)
                self.assertEqual(report['triangles'],84)
                self.assertEqual([p['triangles'] for p in report['parts']],[20,20,22,22])
                self.assertEqual(report['file_id'],0x120)
                self.assertEqual(len(report['roots']),4)
                self.assertEqual(mesh.bounds,((-17,-39,-21),(21,9,34)))
                summary=report['skeleton_records']
                self.assertTrue(summary['screenshot_match'])
                self.assertEqual(summary['candidate_record_count'],122)
                self.assertEqual(summary['screenshot_offset'],0x2A530)
                self.assertEqual(summary['screenshot_index'],109)
                self.assertEqual(summary['file_id'],0x123)
                self.assertEqual(summary['candidate_offsets'][109],0x2A530)


if __name__=='__main__':unittest.main()

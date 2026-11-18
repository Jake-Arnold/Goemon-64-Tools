"""Source-backed, read-only hierarchy and encoded-channel regressions."""
import os
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from practice.model_research import EXPECTED_GRAPHICS_IDS, PLAYER_TABLE_OFFSETS
from practice.skeleton_rig import (
    RIG_WRAPPER_OFFSET,RIG_ROOT_OFFSET,encoded_channel,reconstruct_traced_rig,
)


class SkeletonRigTests(unittest.TestCase):
    def test_immediate_channel_meaning_from_original_mips(self):
        result=encoded_channel(0xB100,'scale')
        self.assertEqual(result['kind'],'immediate')
        self.assertEqual(result['raw_value'],256)
        self.assertEqual(result['value'],1.0)
        self.assertEqual(encoded_channel(0xB000,'translation')['value'],0.0)
        self.assertEqual(encoded_channel(0xB040,'translation')['value'],2.0)
        self.assertEqual(encoded_channel(0xAFFF,'translation')['value'],-1/32)
        self.assertEqual(encoded_channel(0xB020,'rotation')['raw_value'],32)
        indirect=encoded_channel(0x06C8,'rotation')
        self.assertEqual(indirect['kind'],'animation_channel')
        self.assertEqual(indirect['offset'],0x6c8)
        self.assertNotIn('value',indirect)
        self.assertTrue(encoded_channel(0xF100,'scale')['special_bit'])

    def test_rejects_invalid_channel_values_and_unknown_regions(self):
        for invalid in (True,-1,0x10000,0.5):
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):
                encoded_channel(invalid,'scale')
        with self.assertRaises(ValueError):encoded_channel(0xB100,'quaternion')
        with self.assertRaises(ValueError):reconstruct_traced_rig(b'', 'japan_1')

    def synthetic_files(self, *,root_child=1,child_back=-1,flags=0x80000125,invalid_gfx=False):
        code=bytearray(PLAYER_TABLE_OFFSETS['usa']+32)
        struct.pack_into('>8H',code,PLAYER_TABLE_OFFSETS['usa'],*EXPECTED_GRAPHICS_IDS)
        animation=bytearray(RIG_WRAPPER_OFFSET+0x20)
        struct.pack_into('>III',animation,RIG_WRAPPER_OFFSET,flags,0x07029980,0x0702A518)
        # Synthetic cycle: a root whose child points back at it. No proprietary assets.
        struct.pack_into('>Ibb9h',animation,RIG_ROOT_OFFSET,
                         0x08000000 if invalid_gfx else 0,root_child,0,*([0xB100-0x10000]*9))
        struct.pack_into('>Ibb9h',animation,RIG_ROOT_OFFSET+0x18,
                         0,0,child_back,*([0xB100-0x10000]*9))
        class Files:
            sha1='synthetic'
            def file(self,file_id):
                return bytes(code if file_id==11 else animation if file_id==0x123 else bytearray(0x9000))
        return Files()

    def test_cyclic_links_and_wrapper_drift_fail_closed(self):
        with patch('practice.skeleton_rig.RomFiles',return_value=self.synthetic_files()):
            with self.assertRaisesRegex(ValueError,'cycle'):
                reconstruct_traced_rig(b'synthetic','usa')
        with patch('practice.skeleton_rig.RomFiles',return_value=self.synthetic_files(flags=0)):
            with self.assertRaisesRegex(ValueError,'wrapper flags'):
                reconstruct_traced_rig(b'synthetic','usa')
        with patch('practice.skeleton_rig.RomFiles',return_value=self.synthetic_files(root_child=50)):
            with self.assertRaisesRegex(ValueError,'source node array'):
                reconstruct_traced_rig(b'synthetic','usa')

    def test_verified_original_usa_japanese_source_rigs(self):
        paths={'usa':os.environ.get('GOEMON_TEST_USA_ROM'),
               'japan_0':os.environ.get('GOEMON_TEST_JP_ROM')}
        if not all(paths.values()): self.skipTest('Original retail ROM paths not provided')
        for region,path in paths.items():
            with self.subTest(region=region):
                info,mesh=reconstruct_traced_rig(Path(path).read_bytes(),region)
                self.assertEqual(info['node_count'],14)
                self.assertEqual(info['mesh_node_count'],13)
                self.assertEqual(info['triangles'],460)
                self.assertEqual(mesh.triangle_count,460)
                self.assertEqual(info['root_offset'],0x2A518)
                self.assertEqual(info['animation_stream_offset'],0x29980)
                self.assertEqual(info['immediate_scale_count'],42)
                self.assertTrue(info['all_immediate_scales_one'])
                self.assertEqual(info['unresolved_rotation_channels'],39)
                self.assertEqual(info['unresolved_translation_channels'],27)
                self.assertEqual(len(info['nodes']),14)
                self.assertTrue(all(node['source_offset']%24==RIG_ROOT_OFFSET%24 for node in info['nodes']))
                self.assertEqual(sum(node['triangles'] for node in info['nodes']),460)
                self.assertIn('no character-body identification',info['preview_status'])
                offset = 0 if region=='usa' else -0x60
                expected = {f'0x09{v+offset:06X}' for v in (0x47F8,0x4BB0,0x4930,0x4CD0)}
                self.assertTrue(expected.issubset({node['graphics_pointer'] for node in info['nodes']}))

if __name__=='__main__':unittest.main()

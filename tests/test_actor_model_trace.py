"""Synthetic-only JP actor/draw trace tests; no ROM or emulator needed."""
import json
import struct
import tempfile
import unittest
from pathlib import Path

from practice.actor_model_trace import (SCHEMA, INIT_AFTER_PC, DRAW_ENTRY_PC, analyze, load_capture)


def actor_event(frame=20, actor=0x80150000, obj=0x80300000, aid=0xFB, mid=0xFB, pc=INIT_AFTER_PC):
    header=bytearray(0x60)
    struct.pack_into('>I',header,0x18,obj)
    struct.pack_into('>HH',header,0x5C,aid,mid)
    return {'kind':'actor','frame':frame,'pc':f'0x{pc:08X}',
            'actor_ptr':f'0x{actor:08X}','header_hex':header.hex()}


def draw_event(frame=20,obj=0x80300000):
    header=bytearray(0x68)
    struct.pack_into('>II',header,0x2C,0x790047F8,0x09000580)
    struct.pack_into('>HHI',header,0x34,0x0123,0,0x80304000)
    return {'kind':'draw','frame':frame,'pc':f'0x{DRAW_ENTRY_PC:08X}','a0':f'0x{obj:08X}',
            'header_hex':header.hex()}


def trace(*rows):
    return {'schema':SCHEMA,'region':'japan_0','map_id':3,'captures':list(rows)}


class ModelBindingTests(unittest.TestCase):
    def test_same_frame_exact_pointer_correlates_model_with_draw(self):
        result=analyze(trace(actor_event(),draw_event()))
        self.assertTrue(result['target_actor_seen'])
        self.assertEqual(result['matches'][0]['actor_id'],'0x00FB')
        self.assertEqual(result['matches'][0]['model_id'],'0x00FB')
        self.assertEqual(result['matches'][0]['graphics_payload'],'0x090047F8')
        self.assertEqual(result['matches'][0]['overlays'][0]['file_id'],0x123)
        self.assertIn('provisional',result['matches'][0]['binding_status'])
        self.assertNotIn('header_hex',json.dumps(result))
        self.assertNotIn('80304000',str(result['actor_ids_seen']))

    def test_no_match_without_exact_pointer_or_matching_frame(self):
        for row in (draw_event(obj=0x80300020),draw_event(frame=21)):
            with self.subTest(row=row['frame']):
                result=analyze(trace(actor_event(),row))
                self.assertFalse(result['matches'])
                self.assertEqual(len(result['unmatched_draws']),1)

    def test_different_actor_does_not_claim_robot(self):
        result=analyze(trace(actor_event(aid=0x00FF),draw_event()))
        self.assertFalse(result['target_actor_seen'])
        self.assertEqual(result['matches'][0]['actor_id'],'0x00FF')

    def test_draw_pause_without_initializer_is_unlinked(self):
        result=analyze(trace(actor_event(pc=DRAW_ENTRY_PC),draw_event()))
        self.assertEqual(result['matches'],[])

    def test_model_override_is_not_silently_forced_to_id(self):
        result=analyze(trace(actor_event(frame=19),actor_event(frame=20,mid=0x0150,pc=DRAW_ENTRY_PC),draw_event()))
        self.assertEqual(result['matches'][0]['model_id'],'0x0150')
        self.assertEqual(result['matches'][0]['initial_model_id'],'0x00FB')
        self.assertTrue(result['matches'][0]['model_changed_after_init'])

    def test_rejects_conflicting_actor_identity(self):
        with self.assertRaisesRegex(ValueError,'conflicting actor captures'):
            analyze(trace(actor_event(),actor_event(frame=21,obj=0x80300004)))

    def test_rejects_bad_region_pc_address_and_snapshots(self):
        for field,change in [('region',{'region':'usa'}),('map_id',{'map_id':4})]:
            with self.subTest(field=field):
                data=trace(actor_event())
                data.update(change)
                with self.assertRaises(ValueError):analyze(data)
        bads=[]
        e=actor_event();e['pc']='0x8021DE00';bads.append(e)
        e=actor_event();e['pc']='0x8021DE70';bads.append(e)
        e=actor_event();e['actor_ptr']='0x80150001';bads.append(e)
        e=actor_event();e['header_hex']=e['header_hex'][:-2];bads.append(e)
        e=actor_event();e['header_hex']='GG'*(0x60);bads.append(e)
        e=draw_event();e['pc']='0x80016C44';bads.append(e)
        for e in bads:
            with self.subTest(e=e):
                with self.assertRaises(ValueError):analyze(trace(e))

    def test_good_bad_hash_evidence(self):
        def frame(n,label,gbi,matrix='b',texture='c',fb='d'):
            return {'kind':'frame','frame':n,'label':label,
                    'guest_gbi_sha256':gbi*64,'guest_matrices_sha256':matrix*64,
                    'guest_textures_sha256':texture*64,'framebuffer_sha256':fb*64}
        result=analyze(trace(frame(12,'good','a'),frame(13,'bad','a',fb='e')))
        self.assertEqual(result['frame_comparison']['status'],'compared')
        self.assertEqual(result['frame_comparison']['changed_inputs'],[])
        self.assertIn('RT64',result['frame_comparison']['interpretation'])
        result=analyze(trace(frame(12,'good','a'),frame(13,'bad','f',fb='e')))
        self.assertIn('guest_gbi_sha256',result['frame_comparison']['changed_inputs'])
        with self.assertRaisesRegex(ValueError,'SHA-256'):
            analyze(trace({'kind':'frame','frame':12,'label':'good','guest_gbi_sha256':'abc'}))

    def test_file_load_size_cap(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'trace.json'
            path.write_text(json.dumps(trace(actor_event())),encoding='utf-8')
            self.assertEqual(load_capture(path)['schema'],SCHEMA)
            path.write_bytes(b'X'* (256*1024+1))
            with self.assertRaisesRegex(ValueError,'cap'):load_capture(path)


if __name__=='__main__':unittest.main()
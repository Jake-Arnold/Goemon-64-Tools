"""Original-only USA/JP source regression; never checks in any game bytes."""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from practice.dialogue_japan import (
    load_japan_image, normalise_japan_retail, extract_japan_dialogue,
    decode_japan_tokens, encode_japan_text, validate_japan_replacement,
    patch_japan_image, repack_japan_retail, save_japan_retail_rom,
    JP_RETAIL_SHA1,JP_DECOMPRESSED_SHA1)
from practice.dialogue_store import (identify_original_rom, import_rom,
    verify_stored, decompress_original, drop_paths, open_directory,build_directory)


class EncodingTests(unittest.TestCase):
    def test_japan_numeric_token_identity(self):
        raw=(13,13,123,-33,395,-32,-60,23,-61)
        s=decode_japan_tokens(raw)
        self.assertEqual(encode_japan_text(s),raw)
        with self.assertRaises(ValueError):encode_japan_text('未確認')
        with self.assertRaises(ValueError):encode_japan_text('<token:999>')
        with self.assertRaises(ValueError):encode_japan_text('<token:-1>')

    def test_controls_must_remain(self):
        from practice.dialogue_japan import JapanDialogueRecord
        r=JapanDialogueRecord(82,4,0x500000,(13,-33,20,-32,-60),(8,))
        self.assertEqual(validate_japan_replacement(r,' <token:-33><token:21><token:-32>\n'),
                         (13,-33,21,-32,-60))
        with self.assertRaises(ValueError):validate_japan_replacement(r,' <token:21>\n')
        with self.assertRaises(ValueError):validate_japan_replacement(r,' <token:-33><token:21><token:-32>\n\n')

    def test_drop_paths_with_braces(self):
        class MockTcl:
            @staticmethod
            def splitlist(text):
                import tkinter as tk
                return tk.Tcl().splitlist(text)
        class MockRoot:tk=MockTcl()
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'original Japanese ROM.n64'
            path.write_bytes(b'0')
            self.assertEqual(drop_paths(MockRoot(),'{'+str(path)+'}'),path)
            with self.assertRaises(ValueError):drop_paths(MockRoot(),'{'+str(path)+'} {'+str(path)+'}')

    def test_open_build_directory(self):
        with tempfile.TemporaryDirectory() as tmp, patch('practice.dialogue_store.subprocess.Popen') as popen:
            with patch('practice.dialogue_store.sys.platform','linux'):
                folder=build_directory(tmp)
                self.assertEqual(open_directory(folder),folder)
                popen.assert_called_once_with(['xdg-open',str(folder)],close_fds=True)


class OriginalSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        jp=os.environ.get('GOEMON_JP_DECOMPRESSED_ROM')
        us=os.environ.get('GOEMON_USA_DECOMPRESSED_ROM')
        jp_ret=os.environ.get('GOEMON_JP_RETAIL_ROM')
        us_ret=os.environ.get('GOEMON_USA_RETAIL_ROM')
        if not all((jp,us,jp_ret,us_ret)):
            raise unittest.SkipTest('Set all four GOEMON_*_ROM environment paths')
        cls.jp=Path(jp).read_bytes()
        cls.us=Path(us).read_bytes()
        cls.jp_raw=Path(jp_ret).read_bytes()
        cls.us_raw=Path(us_ret).read_bytes()
        cls.records=extract_japan_dialogue(cls.jp)

    def test_known_pinned_images(self):
        self.assertEqual(hashlib.sha1(self.jp).hexdigest(),JP_DECOMPRESSED_SHA1)
        self.assertEqual(len(self.records),5039)
        self.assertEqual(len({r.resource_id for r in self.records}),42)
        self.assertEqual(sum(map(lambda r:len(r.references),self.records)),5694)

    def test_byte_swap(self):
        normalized=normalise_japan_retail(self.jp_raw)
        self.assertEqual(hashlib.sha1(normalized).hexdigest(),JP_RETAIL_SHA1)
        self.assertEqual(identify_original_rom(self.jp_raw)[:2],('japan','retail'))
        self.assertEqual(identify_original_rom(self.us_raw)[:2],('usa','retail'))
        self.assertEqual(identify_original_rom(self.us)[:2],('usa','decompressed'))
        self.assertEqual(identify_original_rom(self.jp)[:2],('japan','decompressed'))
        with self.assertRaises(ValueError):identify_original_rom(self.us_raw[:500])

    def test_import_once_stores_both_roms_and_reverifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            jp_input=folder/'Japanese Original.n64'
            jp_input.write_bytes(self.jp_raw)
            region,kind,output=import_rom(jp_input,root=folder/'library')
            self.assertEqual((region,kind),('japan','retail'))
            self.assertEqual(output.read_bytes(),self.jp)
            retail=verify_stored('japan','retail',root=folder/'library')
            self.assertIsNotNone(retail)
            self.assertEqual(retail.read_bytes(),normalise_japan_retail(self.jp_raw))
            output.write_bytes(b'corrupted')
            self.assertIsNone(verify_stored('japan','decompressed',root=folder/'library'))
            self.assertEqual(hashlib.sha1(jp_input.read_bytes()).hexdigest(),
                             hashlib.sha1(self.jp_raw).hexdigest())

    def test_auto_decompress_usa_japan(self):
        self.assertEqual(decompress_original(self.us_raw,'usa'),self.us)
        self.assertEqual(decompress_original(normalise_japan_retail(self.jp_raw),'japan'),self.jp)

    def test_japan_index_no_usa_glyph_assumption(self):
        r=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x18)
        self.assertIn('かいどう',r.text)
        self.assertEqual(encode_japan_text(r.text),r.tokens)
        self.assertEqual(r.as_dict()['region'],'japan_0')


    def test_kai_screenshot_matches_original_rom_and_roundtrips(self):
        # The screenshot aligns both *adjacent* JP resource-82 records.
        title=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x4)
        road=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x18)
        self.assertEqual(title.tokens, (13,13,292,-33,99,95,-32,293,-60))
        self.assertEqual(road.tokens, (13,13,13,13,13,19,15,78,16))
        self.assertEqual(title.text, '  【<token:-33>カイ<token:-32>】\n')
        self.assertEqual(road.text, '     かいどう')
        self.assertEqual(encode_japan_text(title.text),title.tokens)
        self.assertEqual(encode_japan_text(road.text),road.tokens)

    def test_known_character_edit_preserves_controls(self):
        title=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x4)
        # It is now possible to type confirmed Unicode glyphs directly.
        changed=title.text.replace('カイ','イカ')
        edited=validate_japan_replacement(title,changed)
        self.assertEqual(edited,(13,13,292,-33,95,99,-32,293,-60))
        self.assertEqual(encode_japan_text(decode_japan_tokens(edited)),edited)
        with self.assertRaises(ValueError):
            validate_japan_replacement(title,changed.replace('<token:-32>',''))

    def test_japan_same_length_patch_and_header(self):
        r=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x18)
        edited=r.text.replace('か','<token:29>',1)
        out=patch_japan_image(self.jp,self.records,{r.key:edited})
        self.assertNotEqual(out,self.jp)
        self.assertEqual(struct.unpack_from('>h',out,r.image_offset+5*2)[0],29)
        self.assertEqual(out[:r.image_offset],self.jp[:r.image_offset])
        self.assertEqual(out[r.image_offset+len(r.tokens)*2:],self.jp[r.image_offset+len(r.tokens)*2:])

    def test_japan_original_retail_repacks_byte_exact(self):
        normalized=normalise_japan_retail(self.jp_raw)
        self.assertEqual(repack_japan_retail(self.jp,normalized),normalized)

    def test_japan_variable_length_relocation(self):
        r=next(r for r in self.records if r.resource_id==82 and r.text_offset==0x18)
        edited=r.text+'<token:23>'
        patched=patch_japan_image(self.jp,self.records,{r.key:edited})
        self.assertNotEqual(patched,self.jp)
        old_ref=r.references[0]
        old_op=struct.unpack_from('>I',self.jp,r.image_offset-r.text_offset+old_ref+4)[0]
        new_op=struct.unpack_from('>I',patched,r.image_offset-r.text_offset+old_ref+4)[0]
        self.assertGreater(new_op,old_op)
        packed=repack_japan_retail(patched,normalise_japan_retail(self.jp_raw))
        self.assertEqual(len(packed),16*1024*1024)
        self.assertEqual(packed[:4],b'\x80\x37\x12\x40')

    def test_save_never_overwrites_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            jp_src=Path(tmp)/'jp_decomp.z64'
            retail_src=Path(tmp)/'jp_original.n64'
            jp_src.write_bytes(self.jp)
            retail_src.write_bytes(self.jp_raw)
            rec=self.records[0]
            with self.assertRaises(ValueError):
                save_japan_retail_rom(jp_src,retail_src,jp_src,self.records,{rec.key:rec.text})
            with self.assertRaises(ValueError):
                save_japan_retail_rom(jp_src,retail_src,retail_src,self.records,{rec.key:rec.text})

if __name__=='__main__':unittest.main()

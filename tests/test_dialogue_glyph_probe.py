"""Project64 glyph-probe planner and safe-output tests. No ROM assets committed."""
from collections import Counter
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from practice.dialogue_glyph_probe import (
    COLUMNS, PER_PAGE, SUSPECT_NON_GLYPHS, _html_guide,
    build_probe_suite, make_probe_pages, unknown_token_counts)
from practice.dialogue_japan import JapanDialogueRecord, encode_japan_text


class ProbePlannerTests(unittest.TestCase):
    def test_unknown_glyphs_only_not_kana_spaces_or_vm_controls(self):
        record = JapanDialogueRecord(82,0x18,0x1000,
            (13,-60,-33,14,186,226,295,11,390,395), (8,))
        result=unknown_token_counts([record,record])
        self.assertEqual(result,Counter({226:2,11:2,390:2,395:2}))
        self.assertIn(11,SUSPECT_NON_GLYPHS)

    def test_111_unknown_ids_fit_in_four_labelled_pages(self):
        ids=list(range(250,361))
        pages=make_probe_pages(ids)
        self.assertEqual([len(p.ids) for p in pages],[28,28,28,27])
        self.assertEqual(len(pages),4)
        self.assertEqual(pages[0].rows[0],tuple(ids[:COLUMNS]))
        self.assertEqual(len(pages[0].rows),4)
        self.assertEqual(encode_japan_text(pages[0].text).count(-60),3)
        flattened=[tid for p in pages for row in p.rows for tid in row]
        self.assertEqual(flattened,ids)
        for page in pages:
            self.assertTrue(page.text.startswith(f'<token:{page.ids[0]}>'))
            self.assertNotIn('<token:-',page.text)

    def test_reject_invalid_or_duplicate_ids(self):
        for ids in ([],[11,11],[-60],[396],[1.5]):
            with self.subTest(ids=ids),self.assertRaises(ValueError):
                make_probe_pages(ids)
        with self.assertRaises(ValueError):make_probe_pages([226],rows=5)

    def test_build_suite_from_pinned_loader_uses_original_renderer_and_manifest(self):
        record=JapanDialogueRecord(82,0x18,0x742358,(19,15,78,16),(0x50,))
        counts=Counter({i:1 for i in range(250,362)})
        counts[11]=1
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=root/'sources'/'original.decompressed.z64'
            retail=root/'sources'/'original.retail.z64'
            destination=root/'probe-results'
            source.parent.mkdir()
            source.write_bytes(b'original-decompressed')
            retail.write_bytes(b'original-retail')
            called=[]
            def fake_save(src,ret,out,records,changes):
                self.assertEqual(Path(src),source)
                self.assertEqual(Path(ret),retail)
                self.assertEqual(list(changes),[record.key])
                encoded=encode_japan_text(changes[record.key])
                called.append(tuple(v for v in encoded if v>=0 and v!=13))
                Path(out).write_bytes(b'FAKE PROBE; no actual ROM data')
                return 'f'*40
            with (patch('practice.dialogue_glyph_probe.load_japan_image',return_value=b'fake'),
                  patch('practice.dialogue_glyph_probe.load_japan_retail',return_value=b'fake'),
                  patch('practice.dialogue_glyph_probe.extract_japan_dialogue',return_value=[record]),
                  patch('practice.dialogue_glyph_probe.unknown_token_counts',return_value=counts),
                  patch('practice.dialogue_glyph_probe.save_japan_retail_rom',side_effect=fake_save)):
                manifest=build_probe_suite(source,retail,destination)
            self.assertEqual(manifest['unknown_ids_in_index'],113)
            self.assertEqual(manifest['emitted_probe_ids'],112)
            self.assertEqual(manifest['excluded_suspect_ids'],[11])
            self.assertEqual([len(v) for v in called],[28,28,28,28])
            self.assertEqual(len(manifest['pages']),4)
            self.assertEqual([x for row in manifest['pages'][0]['rows'] for x in row][0]['id'],250)
            guide=(destination/'jp-glyph-probe-guide.html').read_text()
            self.assertIn('token 250',guide)
            self.assertIn('token 361',guide)
            self.assertIn('suspect non-glyph token IDs: 11',guide)
            self.assertEqual(len(list(destination.glob('*.z64'))),4)
            self.assertEqual(source.read_bytes(),b'original-decompressed')
            self.assertEqual(retail.read_bytes(),b'original-retail')
            with self.assertRaises(FileExistsError):
                with (patch('practice.dialogue_glyph_probe.load_japan_image',return_value=b'fake'),
                      patch('practice.dialogue_glyph_probe.load_japan_retail',return_value=b'fake'),
                      patch('practice.dialogue_glyph_probe.extract_japan_dialogue',return_value=[record]),
                      patch('practice.dialogue_glyph_probe.unknown_token_counts',return_value=counts)):
                    build_probe_suite(source,retail,destination)

    def test_failure_writes_no_partial_published_probe_files(self):
        record=JapanDialogueRecord(82,0x18,0x742358,(19,15,78,16),(0x50,))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.bin';retail=root/'retail.bin';output=root/'different-folder'
            with (patch('practice.dialogue_glyph_probe.load_japan_image',return_value=b'fake'),
                  patch('practice.dialogue_glyph_probe.load_japan_retail',return_value=b'fake'),
                  patch('practice.dialogue_glyph_probe.extract_japan_dialogue',return_value=[record]),
                  patch('practice.dialogue_glyph_probe.unknown_token_counts',return_value=Counter(range(100,135))),
                  patch('practice.dialogue_glyph_probe.save_japan_retail_rom',side_effect=ValueError('repack stopped'))):
                with self.assertRaisesRegex(ValueError,'repack stopped'):
                    build_probe_suite(source,retail,output)
            self.assertEqual(list(output.iterdir()),[])

if __name__=='__main__':unittest.main()

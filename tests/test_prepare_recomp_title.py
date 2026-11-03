import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from speed.prepare_recomp_title import PIN, prepare_title, render_main

class RecompTitleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.source=self.root/'src/main/main.cpp'
        self.source.parent.mkdir(parents=True)
        self.original='void create() {\n    SDL_SysWMinfo wmInfo;\n}\n'
        self.source.write_text(self.original,encoding='utf-8')
    def outputs(self, cmd, **kwargs):
        if 'rev-parse' in cmd:return PIN+'\n'
        if 'status' in cmd:return ''
        if 'show' in cmd:return self.original
        raise AssertionError(cmd)
    def test_exact_source_gets_label_once(self):
        with patch('speed.prepare_recomp_title.subprocess.check_output',side_effect=self.outputs):prepare_title(self.root)
        self.assertEqual(self.source.read_text(encoding='utf-8'),render_main(self.original))
        with self.assertRaises(ValueError):render_main(self.source.read_text(encoding='utf-8'))
    def test_dirty_or_unexpected_source_is_preserved(self):
        self.source.write_text('other',encoding='utf-8')
        with patch('speed.prepare_recomp_title.subprocess.check_output',side_effect=self.outputs):
            with self.assertRaises(ValueError):prepare_title(self.root)
        self.assertEqual(self.source.read_text(encoding='utf-8'),'other')

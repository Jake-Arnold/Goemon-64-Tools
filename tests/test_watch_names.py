"""Unit tests for persistent, presentation-only Live Memory aliases."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from practice.watch_names import (
    FORMAT_ID, load_watch_names, save_watch_names, validate_watch_label,
)


class WatchNamesTests(unittest.TestCase):
    def test_atomic_save_and_reload_of_unicode_labels(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/'user'/'watch_names.json'
            self.assertEqual(load_watch_names(path),{})
            save_watch_names(path,{'Ryo':'Cash','Lives':'  Extra lives  '})
            self.assertEqual(load_watch_names(path),{'Ryo':'Cash','Lives':'Extra lives'})
            self.assertEqual(json.loads(path.read_text())['format'],FORMAT_ID)
            self.assertFalse(path.with_name(path.name+'.tmp').exists())

    def test_bad_names_do_not_overwrite_saved_data(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/'names.json'
            save_watch_names(path,{'Ryo':'Cash'})
            previous=path.read_bytes()
            for name in ('   ','Bad\nname','a'*65):
                with self.subTest(name=name),self.assertRaises(ValueError):
                    save_watch_names(path,{'Ryo':name})
                self.assertEqual(path.read_bytes(),previous)

    def test_corrupt_file_is_rejected(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/'names.json'
            path.write_text('{"format":"unexpected","names":{}}')
            with self.assertRaises(ValueError):
                load_watch_names(path)
            path.write_text(json.dumps({'format':FORMAT_ID,'names':{'Ryo':None}}))
            with self.assertRaises(ValueError):
                load_watch_names(path)


if __name__=='__main__':
    unittest.main()

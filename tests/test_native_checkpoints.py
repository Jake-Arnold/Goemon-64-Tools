"""Named native savestate metadata is scoped and never contains game bytes."""
import json
import tempfile
import unittest
from pathlib import Path

from practice.native_checkpoints import (
    FORMAT, load_named_checkpoints, make_named_checkpoint,
    save_named_checkpoints, upsert_named_checkpoint, label_named_checkpoint,
)


class NamedNativeCheckpointsTests(unittest.TestCase):
    def test_create_and_replace_one_region_backend_slot(self):
        a=make_named_checkpoint('Oedo entry', 'japan', 'project64', 2,
                                scene=0x161, character=0, xyz=(1.2, 3.4, 5.6))
        b=make_named_checkpoint('Oedo redo', 'japan', 'project64', 2,
                                scene=0x161, character=1)
        other=make_named_checkpoint('USA slot 2', 'usa', 'project64', 2)
        items=upsert_named_checkpoint([a, other], b)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Oedo redo')
        self.assertEqual(items[1]['region'], 'usa')
        self.assertIn('scene 0x161', label_named_checkpoint(items[0]))
        self.assertIsNone(items[0]['xyz'])

    def test_roundtrip_atomic_file_is_metadata_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'native-state-bookmarks.json'
            self.assertEqual(load_named_checkpoints(path), [])
            entry=make_named_checkpoint(
                'All items', 'japan', 'mupen64plus', 9, scene=4,
                character=3, xyz=[12, 13, 14])
            save_named_checkpoints(path, [entry])
            self.assertEqual(load_named_checkpoints(path), [entry])
            data=path.read_text(encoding='utf-8')
            self.assertIn(FORMAT, data)
            self.assertNotIn('rdram', data.lower())
            self.assertNotIn('base64', data.lower())

    def test_invalid_slot_region_and_xyz_rejected(self):
        for override in (
                {'slot': 10}, {'slot': True}, {'region': 'unknown'},
                {'backend': 'recomp'}, {'xyz': (float('nan'), 0, 0)},
                {'character': 4}, {'scene': 0x1000}):
            values = dict(name='Name', region='japan', backend='project64',
                          slot=0, xyz=None)
            values.update(override)
            with self.subTest(override=override), self.assertRaises(ValueError):
                make_named_checkpoint(**values)

    def test_invalid_json_does_not_get_treated_as_a_savestate(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'meta.json'
            path.write_text(json.dumps({'format': FORMAT,'entries':[{'name':'bad'}]}),
                            encoding='utf-8')
            with self.assertRaises(ValueError):
                load_named_checkpoints(path)


if __name__ == '__main__':
    unittest.main()

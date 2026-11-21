from pathlib import Path
import json
import os
import unittest
from verify_static_atlas import (check_atlas, jal_target, loads_a0_literal, USA_SHA1)

DIR = Path(__file__).resolve().parent
ATLAS = json.loads((DIR/'state_atlas.json').read_text())

class StateAtlasTests(unittest.TestCase):
    def test_partition(self):
        self.assertEqual(len(ATLAS['states']), 18)
        self.assertEqual([s['state'] for s in ATLAS['states']], list(range(18)))
        self.assertEqual(len({s['handler_vma'] for s in ATLAS['states']}), 18)
        self.assertEqual(sum(len(s['direct_setter_calls']) for s in ATLAS['states']), 20)
        self.assertEqual(sum(len(s['increment_helper_calls']) for s in ATLAS['states']), 4)
        self.assertEqual(len(ATLAS['state15_dispatch']['entry_vmas']), 5)
        self.assertEqual(len(ATLAS['file22_dispatch']['entries']), 2)

    def test_edge_provenance_distinct(self):
        calls = [e['call_rom_offset'] for s in ATLAS['states'] for e in s['direct_setter_calls']]
        self.assertEqual(len(calls), len(set(calls)))
        self.assertEqual({e['target_state'] for e in ATLAS['states'][16]['direct_setter_calls']}, {17})
        self.assertEqual({e['target_state'] for e in ATLAS['states'][15]['direct_setter_calls']}, {5})
        self.assertFalse(ATLAS['states'][3]['direct_setter_calls'])
        self.assertEqual(ATLAS['overlay_direct_write']['outer_state'], 4)
        self.assertEqual(ATLAS['file22_dispatch']['entries'][1], 'func_801CB53C_69E15C')

    def test_mips_properties(self):
        word = (3 << 26) | (0x3728 // 4)
        self.assertEqual(jal_target(word, 0x8000303C), 0x80003728)
        self.assertIsNone(jal_target(0, 0x8000303C))
        self.assertTrue(loads_a0_literal((9 << 26) | (4 << 16) | 15, 15))
        self.assertFalse(loads_a0_literal((9 << 26) | (5 << 16) | 15, 15))

    def test_short_input_rejected(self):
        with self.assertRaisesRegex(ValueError, '33554432'):
            check_atlas(b'not a ROM', ATLAS)

    def test_real_private_original_rom_if_supplied(self):
        rom_path = os.environ.get('GOEMON_DECOMPRESSED_ROM')
        if not rom_path:
            self.skipTest('private expanded USA ROM not configured')
        res = check_atlas(Path(rom_path).read_bytes(), ATLAS)
        self.assertEqual(res['rom_sha1'], USA_SHA1)
        self.assertEqual(res['checks'], 68)
        self.assertEqual(res['direct_setter_sites'], 20)

if __name__=='__main__':
    unittest.main()

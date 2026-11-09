"""One-source-shape regression for unpromoted resource-index volatile probe."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'candidates/vm_resource_halfword_probe.c'
PROBE = ROOT / 'candidates/vm_resource_halfword_volatile_probe.c'
ORIGINAL = '    s32 half, out, entry;'
UPDATED = '    volatile s32 half; s32 out, entry;'


def change(base):
    if base.count(ORIGINAL) != 1:
        raise ValueError('canonical resource candidate changed unexpectedly')
    return base.replace(ORIGINAL, UPDATED)


class ResourceIndexVolatileTests(unittest.TestCase):
    def test_only_one_declaration_change(self):
        baseline = BASE.read_text(encoding='utf-8')
        candidate = PROBE.read_text(encoding='utf-8')
        self.assertEqual(change(baseline[baseline.index('typedef signed int s32;'):]),
                         candidate[candidate.index('typedef signed int s32;'):])

    def test_signed_half_index_and_recovery_preserved(self):
        source = PROBE.read_text(encoding='utf-8')
        self.assertIn('volatile s32 half;', source)
        self.assertIn('half = arg / 2;', source)
        self.assertIn('entry = VM_F038_TABLE[half];', source)
        self.assertIn('if (out == -1) func_80013B14_14714((u16)entry);', source)
        self.assertIn('if (half < 4)', source)

    def test_missing_original_declaration_rejected(self):
        with self.assertRaisesRegex(ValueError, 'canonical resource candidate changed'):
            change(BASE.read_text(encoding='utf-8').replace(ORIGINAL, '    s32 half, entry;'))


if __name__ == '__main__':
    unittest.main()

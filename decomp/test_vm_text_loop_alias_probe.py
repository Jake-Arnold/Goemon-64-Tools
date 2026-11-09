"""Structural guard for unpromoted VM text-loop aliasing/codegen research."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def alias_body(source):
    """One reviewed load/store alias-shape change, no loop/control-flow edits."""
    start = source.index('typedef signed int s32;')
    result = source[start:]
    changes = (
        ('VmWork *work = &D_801C77E8_1C83E8;',
         'volatile VmWork *work = &D_801C77E8_1C83E8;'),
        ('s32 state;\nretry:', 's32 state;\n        s32 script_arg;\nretry:'),
        ('D_801C77E8_1C83E8.script_word = func_8003DE80_3EA80(D_801C7754_1C8354, work->script_word);',
         'script_arg = work->script_word;\n'
         '        work->script_word = func_8003DE80_3EA80(D_801C7754_1C8354, script_arg);'),
    )
    for before, after in changes:
        if result.count(before) != 1:
            raise ValueError(f'Original VM candidate changed: {before}')
        result = result.replace(before, after)
    return result


class AliasProbeStructureTests(unittest.TestCase):
    def test_only_reviewed_load_store_aliasing_change(self):
        baseline = (ROOT/'candidates/vm_text_loop.c').read_text()
        probe = (ROOT/'candidates/vm_text_loop_alias_probe.c').read_text()
        self.assertEqual(alias_body(baseline), probe[probe.index('typedef signed int s32;'):])

    def test_unambiguous_function_and_unsigned_halfword_fields(self):
        probe = (ROOT/'candidates/vm_text_loop_alias_probe.c').read_text()
        self.assertEqual(probe.count('void func_8003DBEC_3E7EC(void) {'), 1)
        self.assertIn('u16 gate_halfword;', probe)
        self.assertIn('typedef struct {u16 status, held, pressed;} Controller;', probe)
        self.assertIn('if (outer_count >= D_801C77D8_1C83D8 || retry_count >= 3) break;', probe)

    def test_fails_closed_if_original_call_changes(self):
        base = (ROOT/'candidates/vm_text_loop.c').read_text()
        with self.assertRaisesRegex(ValueError, 'Original VM candidate changed'):
            alias_body(base.replace('func_8003DE80_3EA80(D_801C7754_1C8354, work->script_word)',
                                    'func_8003DE80_3EA80(D_801C7754_1C8354, 0)'))


if __name__ == '__main__':
    unittest.main()

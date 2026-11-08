"""Synthetic upstream fixtures only, no original ROM or upstream game source."""
import unittest
from decomp.collision_patch import prepare_collision_gate

CANDIDATE = '''#include "common.h"\n\ns32 func_8002A168_2AD68(f32, f32, f32);\ns32 func_8003266C_3326C(f32, f32);\n\ns32 func_80029E08_2AA08(f32 arg0, f32 arg1, f32 arg2) {\n    if (func_8003266C_3326C(arg0, arg1) == 0x7FFF) {\n        return 0x7FFF;\n    }\n    return func_8002A168_2AD68(arg0, arg1, arg2);\n}\n'''
UPSTREAM = '#include "common.h"\n/* prior */\n#pragma GLOBAL_ASM("asm/nonmatchings/27FE0/func_80029E08_2AA08.s")\ns32 func_80029E58_2AA58(void) { return 7; }\n'

class CollisionPatchTests(unittest.TestCase):
    def test_preserves_surrounding_source_and_inserts_candidate(self):
        out = prepare_collision_gate(UPSTREAM, CANDIDATE)
        self.assertTrue(out.startswith('#include "common.h"\n/* prior */\n'))
        self.assertTrue(out.endswith('s32 func_80029E58_2AA58(void) { return 7; }\n'))
        self.assertEqual(out.count('s32 func_80029E08_2AA08('), 1)
        self.assertNotIn('#pragma GLOBAL_ASM', out)
        self.assertEqual(out.count('#include "common.h"'), 1)

    def test_compatible_later_definition_matches_pinned_source_layout(self):
        extra = """
s32 func_8002A168_2AD68(f32 origin_x, f32 origin_y, f32 origin_z) {
    return 17;
}
"""
        result = prepare_collision_gate(UPSTREAM + extra, CANDIDATE)
        self.assertEqual(result.count('s32 func_8002A168_2AD68('), 2)
        self.assertTrue(result.endswith(extra))

    def test_conflicting_later_definition_or_prototype_rejected(self):
        variants = (
            's32 func_8002A168_2AD68(f32 first, s32 second, f32 third) { return 0; }\n',
            's32 func_8002A168_2AD68(f32, f32, f32);\n',
            's32 func_8002A168_2AD68(f32 x, f32 y, f32 z) { return 0; }\n'
            's32 func_8002A168_2AD68(f32 x, f32 y, f32 z) { return 1; }\n',
        )
        for added in variants:
            with self.subTest(added=added), self.assertRaisesRegex(ValueError, 'interface review'):
                prepare_collision_gate(UPSTREAM + added, CANDIDATE)

    def test_callee_defined_before_gate_rejected(self):
        early = 's32 func_8002A168_2AD68(f32 x, f32 y, f32 z) { return 0; }\n'
        with self.assertRaisesRegex(ValueError, 'interface review'):
            prepare_collision_gate(early + UPSTREAM, CANDIDATE)

    def test_missing_duplicate_or_ambiguous_anchor_rejected(self):
        for source in (UPSTREAM.replace('#pragma GLOBAL_ASM', '// #pragma GLOBAL_ASM'),
                       UPSTREAM.replace('s32 func_80029E58_2AA58', 's32 other'),
                       UPSTREAM.replace('s32 func_80029E58', '#pragma GLOBAL_ASM("asm/func_80029E08_2AA08.s")\ns32 func_80029E58'),
                       UPSTREAM + 's32 func_80029E08_2AA08(void);\n'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                prepare_collision_gate(source, CANDIDATE)

    def test_modified_candidate_or_existing_callee_rejected(self):
        with self.assertRaisesRegex(ValueError, 'reviewed isolated probe'):
            prepare_collision_gate(UPSTREAM, CANDIDATE.replace('0x7FFF', '0x7FFE'))
        with self.assertRaisesRegex(ValueError, 'interface review'):
            prepare_collision_gate(UPSTREAM + 's32 func_8003266C_3326C(f32, f32);\n', CANDIDATE)
        with self.assertRaisesRegex(ValueError, 'LF-only'):
            prepare_collision_gate(UPSTREAM.replace('\n', '\r\n'), CANDIDATE)


    def test_anchor_before_pragma_rejected(self):
        moved = UPSTREAM.replace('s32 func_80029E58_2AA58(void) { return 7; }\n', '')
        moved = 's32 func_80029E58_2AA58(void) { return 7; }\n' + moved
        with self.assertRaisesRegex(ValueError, 'following upstream'):
            prepare_collision_gate(moved, CANDIDATE)

    def test_duplicate_following_anchor_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unique following'):
            prepare_collision_gate(UPSTREAM + 's32 func_80029E58_2AA58(void);\n', CANDIDATE)

    def test_intervening_assembly_rejected(self):
        modified = UPSTREAM.replace('s32 func_80029E58', '#pragma GLOBAL_ASM("asm/other.s")\ns32 func_80029E58')
        with self.assertRaisesRegex(ValueError, 'Unexpected assembly'):
            prepare_collision_gate(modified, CANDIDATE)

if __name__ == '__main__': unittest.main()

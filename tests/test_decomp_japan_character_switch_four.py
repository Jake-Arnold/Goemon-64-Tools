"""ROM-free source/provenance checks for JP original-address switch C promotion."""
import hashlib
import unittest

from decomp import japan_character_switch_four as switch
from decomp import japan_noop_port as jp329


class JapaneseSwitchFour(unittest.TestCase):
    def test_native_exact_original_offsets(self):
        expected={
            'func_801E2888_59E858':(0x59E858,40),
            'func_801E28B0_59E880':(0x59E880,12),
            'func_801E2970_59E940':(0x59E940,148),
            'func_801E2A04_59E9D4':(0x59E9D4,132),
        }
        self.assertEqual({n:(offset,size) for n,offset,size,_ in switch.RECORDS},expected)
        self.assertEqual(sum(sz for _,_,sz,_ in switch.RECORDS),332)
        self.assertEqual(len({selection for _,_,_,selection in switch.RECORDS}),4)
        self.assertEqual(len(switch.EXPECTED_SHA256),4)
        self.assertEqual({n for n,*_ in switch.RECORDS},switch.EXPECTED_NAMES)

    def test_no_double_counting_prior_japan_functions(self):
        base=__import__('json').loads((switch.HERE/'regions/japan_0.json').read_text())
        old={f['name'] for unit in base['units'] for f in unit['functions']}
        prior={name for parent in jp329.load_manifest()['parents'] for name,_ in parent['c']}
        self.assertEqual((len(old),len(prior)),(39,290))
        self.assertFalse(old & prior)
        self.assertFalse(old & switch.EXPECTED_NAMES)
        self.assertFalse(prior & switch.EXPECTED_NAMES)
        self.assertEqual(39+290+len(switch.EXPECTED_NAMES),333)

    def test_usa_provenance_is_exact_archived_source(self):
        original=switch.SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(),switch.SOURCE_SHA256)
        self.assertIn(b'#elif defined(REGION_USA)',original)
        self.assertIn(b'#if defined(REGION_JAPAN)',original)
        for _,_,_,form in switch.RECORDS:
            self.assertIn(f'#elif defined({form})'.encode(),original+b'#elif defined(SELECT_READER)') if form not in ('SELECT_READER',) else self.assertIn(b'#if defined(SELECT_READER)',original)

    def test_generated_source_selects_only_one_original_function(self):
        for name,_,_,selector in switch.RECORDS:
            body=switch.source_text(name,selector)
            self.assertIn('#define REGION_JAPAN 1',body)
            self.assertIn(f'#define {selector} 1',body)
            self.assertIn('#include "src/jp_switch/jp_switch_verified_shared.h"',body)
            self.assertNotIn('GLOBAL_ASM',body)
            self.assertEqual(body.count('#define SELECT_'),1)

    def test_original_parent_is_bounded(self):
        self.assertEqual(switch.ORIGINAL_PARENT,'59DA50.s')
        self.assertEqual(switch.ORIGINAL_SIZE,0x1010)
        prev=0x59DA50
        for _,off,size,_ in switch.RECORDS:
            self.assertGreaterEqual(off,prev)
            self.assertLessEqual(off+size,0x59DA50+switch.ORIGINAL_SIZE)
            self.assertEqual(len(switch.EXPECTED_SHA256[next(n for n,o,_,_ in switch.RECORDS if o==off)]),64)
            prev=off+size

if __name__=='__main__':unittest.main()

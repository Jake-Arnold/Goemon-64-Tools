"""Synthetic targeted character cursor discovery tests: no game assets or process writes."""
import json
import unittest
from practice.native_character_cursor_scan import (
    ORDER, CHARACTERS, CursorCapture, menu_context,
    capture_cursor, find_cursor_candidates, make_cursor_report,
    validate_sequence, SCAN_BASE, SCAN_SIZE,
)

TEST_BASE = SCAN_BASE
TEST_SIZE = 1024


def captures(*, unstable=False, changed_context=False):
    data=[]
    for n,char in enumerate(ORDER):
        b=bytearray(TEST_SIZE)
        b[128]=char                             # 0,1,2,3
        b[132]=char+1                           # 1,2,3,4
        b[136:138]=(0x1230+4*char).to_bytes(2,'big')
        b[140:144]=(0x80214580+24*char).to_bytes(4,'big')
        b[144]=[2,7,4,9][char]                # non-linear encoded highlight
        b[164]=n                             # time-linked, not the char
        c=bytearray(b)
        if unstable: c[200]=n+1              # volatile pixel/counter
        context={'state':10,'category':0 if not changed_context or n==0 else 1,'stage_offset':90,
                 'absolute_map':90,'active_character':0}
        data.append(CursorCapture(char,bytes(b),bytes(c),context))
    return data


class FakeMenuRam:
    def __init__(self):
        self.state=10
        self.calls=[]
    def u8(self,addr):return 10 if addr==0x800C7A94 else 0
    def u16(self,addr):return 90
    def u32(self,addr):return 0
    def read_guest(self,addr,length):
        self.calls.append((addr,length))
        return b'\x11'*length


class TestCursorScan(unittest.TestCase):
    def test_exact_offsets_reverse_and_encodings(self):
        result=find_cursor_candidates(captures(),base=TEST_BASE)
        found={(c['addr'],c['width']):c for c in result}
        self.assertEqual(found[(f'0x{TEST_BASE+128:08X}',1)]['encoding'],'zero_based')
        self.assertEqual(found[(f'0x{TEST_BASE+132:08X}',1)]['encoding'],'one_based')
        self.assertEqual(found[(f'0x{TEST_BASE+136:08X}',2)]['encoding'],'linear')
        self.assertEqual(found[(f'0x{TEST_BASE+140:08X}',4)]['values'],[0x80214580+24*i for i in range(4)])
        self.assertEqual(found[(f'0x{TEST_BASE+144:08X}',1)]['encoding'],'lookup')
        self.assertFalse(any(c['addr']==f'0x{TEST_BASE+164:08X}' for c in result))
        self.assertEqual(result[0]['encoding'],'zero_based')
        self.assertTrue(all(c['verified_samples']==8 for c in result))

    def test_volatile_bytes_are_not_candidates(self):
        result=find_cursor_candidates(captures(unstable=True),base=TEST_BASE)
        self.assertFalse(any(c['addr']==f'0x{TEST_BASE+200:08X}' for c in result))

    def test_context_change_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Category|state|changed'):
            find_cursor_candidates(captures(changed_context=True),base=TEST_BASE)

    def test_wrong_order_is_rejected(self):
        a=captures()
        a[1],a[2]=a[2],a[1]
        with self.assertRaisesRegex(ValueError,'Expected'):
            validate_sequence(a)

    def test_report_has_all_candidates_without_ram(self):
        caps=captures(); cs=find_cursor_candidates(caps,base=TEST_BASE)
        report=make_cursor_report(caps,cs,base=TEST_BASE)
        self.assertEqual(report['total_candidates'],len(cs))
        self.assertEqual(len(report['capture_order']),8)
        self.assertEqual(report['game_context']['category'],0)
        self.assertNotIn('first',json.dumps(report))
        self.assertNotIn('second',json.dumps(report))
        self.assertTrue(all('addr' in c for c in report['candidates']))

    def test_capture_does_not_write_memory_and_checks_stability(self):
        ram=FakeMenuRam()
        captured=capture_cursor(ram,1,base=TEST_BASE,size=TEST_SIZE,delay=0,sleeper=lambda s:None)
        self.assertEqual(captured.character,1)
        self.assertEqual(ram.calls,[(TEST_BASE,TEST_SIZE),(TEST_BASE,TEST_SIZE)])
        self.assertEqual(captured.context['state'],10)
        ram.state=13
        ram.u8=lambda addr:ram.state if addr==0x800C7A94 else 0
        with self.assertRaisesRegex(ValueError,'debug menu'):
            capture_cursor(ram,0,base=TEST_BASE,size=TEST_SIZE,delay=0,sleeper=lambda s:None)

    def test_overlay_included(self):
        self.assertGreater(SCAN_BASE+SCAN_SIZE,0x80220000)

if __name__=='__main__': unittest.main()

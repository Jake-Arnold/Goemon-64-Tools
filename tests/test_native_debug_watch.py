import unittest
from practice.native_debug_watch import FIELDS, read_fields, changed_fields, make_change_event, can_mark_state, decode_hover_pointer


class MockRam:
    def __init__(self):
        self.bytes = bytearray(0x200000)
        for i, field in enumerate(FIELDS):
            offset = field.address - 0x80000000
            self.bytes[offset:offset+field.width] = (i+1).to_bytes(field.width,'big')

    def read_guest(self,address,width):
        o=address-0x80000000
        return self.bytes[o:o+width]


class WatchTests(unittest.TestCase):
    def test_reads_original_n64_memory_endian_and_width(self):
        memory=MockRam()
        self.assertEqual(read_fields(memory),{field.key:i+1 for i,field in enumerate(FIELDS)})

    def test_changes_report_only_changed_watches(self):
        memory=MockRam()
        before=read_fields(memory)
        field=next(f for f in FIELDS if f.key=='scene_candidate')
        off=field.address-0x80000000
        memory.bytes[off:off+2]=(96).to_bytes(2,'big')
        after=read_fields(memory)
        self.assertEqual(changed_fields(before,after),{'scene_candidate':(2,96)})

    def test_all_watches_are_guest_addresses_and_read_only(self):
        self.assertEqual(len(FIELDS),len({f.address for f in FIELDS}))
        self.assertTrue(all(0x80000000 <= f.address < 0x80400000 for f in FIELDS))
        self.assertEqual({f.key for f in FIELDS},
                         {'state','scene_candidate','character_candidate','submode','live_map','live_character','phase','exit_request','pending_map','hover_pointer'})


class GameplayTransitionWatchTests(unittest.TestCase):
    def test_export_preserves_menu_to_gameplay_transition(self):
        before={'state':10,'scene_candidate':96,'live_map':96}
        after={'state':13,'scene_candidate':96,'live_map':96}
        event=make_change_event(before,after,'2026-11-01T12:00:00+00:00')
        self.assertEqual(event['changed'],{'state':[10,13]})
        self.assertEqual(event['values']['state'],13)

    def test_export_preserves_gameplay_to_menu_transition(self):
        before={'state':13,'live_map':90,'live_character':0}
        after={'state':10,'live_map':91,'live_character':0}
        event=make_change_event(before,after,'2026-11-01T12:00:00+00:00')
        self.assertEqual(event['changed']['state'],[13,10])
        self.assertEqual(event['changed']['live_map'],[90,91])

    def test_change_event_returns_none_when_same(self):
        before={'state':13,'live_map':90}
        self.assertIsNone(make_change_event(before,dict(before),'now'))

    def test_marking_allowed_only_in_gameplay_or_menu(self):
        for st in (10,13):
            self.assertTrue(can_mark_state(st))
        for st in (0,7,8,9,12,14):
            self.assertFalse(can_mark_state(st))


class CharacterHoverPointerTests(unittest.TestCase):
    def test_exact_four_original_menu_entries(self):
        for n,addr in zip(('Goemon','Ebisumaru','Sasuke','Yae'),
                          (0x8007BAD0,0x8007BADC,0x8007BAE8,0x8007BAF4)):
            self.assertEqual(decode_hover_pointer(addr),n)

    def test_unknown_and_nearby_addresses_not_misidentified(self):
        for invalid in (0x8007BACF, 0x8007BAD1, 0x8007BB00, 0, -1,
                        0x8015C5DC, None, True, '0x8007BAD0'):
            self.assertIsNone(decode_hover_pointer(invalid))

    def test_live_watch_includes_candidate_pointer(self):
        f = next(f for f in FIELDS if f.key=='hover_pointer')
        self.assertEqual((f.address,f.width),(0x800C7E60,4))
        self.assertIn('READ ONLY',f.confidence)
        memory=MockRam()
        off=f.address-0x80000000
        memory.bytes[off:off+4]=bytes.fromhex('8007BAE8')
        self.assertEqual(decode_hover_pointer(read_fields(memory)['hover_pointer']), 'Sasuke')

"""Synthetic guest-RAM tests for native-menu selector discovery/validation."""
import unittest
import json
from practice.native_debug_trace import (
    BASE,SIZE,PROFILE_FORMAT,Observation,candidates_for_pair,find_candidates,
    validate_profile,calibrated_for_direct_warp,stage_menu_selection,selection_values,
    Candidate,candidate_report,display_candidate_indices
)
from practice.checkpoints import STATE_ADDR, MAP_ADDR

MENU_SCENE=0x80210000
MENU_CHARACTER=0x80210140
MENU_CATEGORY=0x80210204


def obs(map_id,character,unstable=False):
    d=bytearray(SIZE)
    d[MENU_SCENE-BASE:MENU_SCENE-BASE+2]=map_id.to_bytes(2,'big')
    d[MENU_CHARACTER-BASE]=character
    d[MENU_CATEGORY-BASE]=selection_values(map_id)['category_index']
    e=bytearray(d)
    if unstable:e[0x2801]=0xA4
    return Observation(map_id,character,bytes(d),bytes(e))

class FakeRam:
    def __init__(self):
        self.b=bytearray(SIZE)
        self.b[STATE_ADDR-BASE]=10
    def u8(self,addr):return self.b[addr-BASE]
    def read_guest(self,addr,n):return bytes(self.b[addr-BASE:addr-BASE+n])
    def write_guest(self,addr,value):self.b[addr-BASE:addr-BASE+len(value)]=value

class TestNativeDebugTrace(unittest.TestCase):
    def test_diff_identifies_two_native_menu_fields_not_volatile_memory(self):
        a=obs(353,0,unstable=True);b=obs(354,0,unstable=True);c=obs(353,1,unstable=True)
        sc=candidates_for_pair(a,b,'scene','map_id')
        ch=candidates_for_pair(a,c,'character','character_id')
        self.assertTrue(any(x.addr==MENU_SCENE and x.width==2 for x in sc))
        self.assertTrue(any(x.addr==MENU_CHARACTER and x.width==1 for x in ch))
        self.assertTrue(all(x.addr!=BASE+0x2801 for x in sc+ch))
        cs=find_candidates([a,b,c])
        self.assertTrue(any(x.role=='scene' and x.addr==MENU_SCENE for x in cs))
        self.assertTrue(any(x.role=='character' and x.addr==MENU_CHARACTER for x in cs))

    def test_unknown_native_addresses_block_direct_warp(self):
        self.assertFalse(calibrated_for_direct_warp({'format':PROFILE_FORMAT,'fields':{}}))
        ram=FakeRam()
        with self.assertRaises(ValueError):stage_menu_selection(ram,{'format':PROFILE_FORMAT,'fields':{}},353,2)
        self.assertEqual(ram.read_guest(MENU_SCENE,2),b'\0\0')

    def test_ready_when_direct_scene_and_character_are_calibrated(self):
        profile={'format':PROFILE_FORMAT,'fields':{
            'scene':{'addr':hex(MENU_SCENE),'width':2,'method':'map_id','pairs':2},
            'character':{'addr':hex(MENU_CHARACTER),'width':1,'method':'character_id','pairs':2},
        }}
        self.assertTrue(calibrated_for_direct_warp(profile))
        ram=FakeRam()
        result=stage_menu_selection(ram,profile,353,2)
        self.assertEqual(result['status'],'staged_not_confirmed')
        self.assertEqual(ram.read_guest(MENU_SCENE,2),b'\x01\x61')
        self.assertEqual(ram.u8(MENU_CHARACTER),2)
        self.assertEqual(ram.u8(STATE_ADDR),10)
        ram.write_guest(STATE_ADDR,b'\x0d')
        with self.assertRaises(ValueError):stage_menu_selection(ram,profile,354,3)

    def test_stage_index_requires_category_field(self):
        profile={'format':PROFILE_FORMAT,'fields':{
            'scene':{'addr':hex(MENU_SCENE),'width':2,'method':'stage_index','pairs':2},
            'character':{'addr':hex(MENU_CHARACTER),'width':1,'method':'character_id','pairs':2},
        }}
        self.assertFalse(calibrated_for_direct_warp(profile))
        profile['fields']['category']={'addr':hex(MENU_CATEGORY),'width':1,'method':'category_index','pairs':2}
        self.assertTrue(calibrated_for_direct_warp(profile))
        ram=FakeRam();stage_menu_selection(ram,profile,353,3)
        self.assertEqual(ram.read_guest(MENU_SCENE,2),b'\0\x03')
        self.assertEqual(ram.u8(MENU_CATEGORY),2)
        self.assertEqual(ram.u8(MENU_CHARACTER),3)

    def test_rejects_conflicting_fields_and_known_gameplay_addresses(self):
        profile={'format':PROFILE_FORMAT,'fields':{
            'scene':{'addr':hex(MAP_ADDR),'width':2,'method':'map_id'},
        }}
        with self.assertRaises(ValueError):validate_profile(profile)
        profile={'format':PROFILE_FORMAT,'fields':{
            'scene':{'addr':hex(MENU_SCENE),'width':2,'method':'map_id','pairs':2},
            'character':{'addr':hex(MENU_SCENE+1),'width':1,'method':'character_id'},
        }}
        with self.assertRaises(ValueError):validate_profile(profile)

    def test_only_repeated_independent_comparisons_unlock_direct_warp(self):
        profile={'format':PROFILE_FORMAT,'fields':{
            'scene':{'addr':hex(MENU_SCENE),'width':2,'method':'map_id','pairs':1},
            'character':{'addr':hex(MENU_CHARACTER),'width':1,'method':'character_id','pairs':1},
        }}
        self.assertFalse(calibrated_for_direct_warp(profile))
        profile['fields']['scene']['pairs']=2
        profile['fields']['character']['pairs']=2
        self.assertTrue(calibrated_for_direct_warp(profile))

    def test_scanner_includes_swappable_level_select_overlay(self):
        self.assertGreater(SIZE, 0x00210000)
        aa=obs(90,0)
        bb=obs(96,0)
        self.assertTrue(any(c.addr==MENU_SCENE for c in candidates_for_pair(aa,bb,'scene','map_id')))

    def test_alignment_and_executable_code_are_not_cursor_fields(self):
        from practice.native_debug_trace import _valid_address
        self.assertFalse(_valid_address(0x8006CFB8,4))  # .main text
        self.assertFalse(_valid_address(0x80210201,2))  # MIPS halfword misalignment
        self.assertFalse(_valid_address(0x80210202,4))  # MIPS word misalignment
        self.assertTrue(_valid_address(0x80210204,4))

    def test_full_export_includes_more_than_400_and_counts_every_role(self):
        candidates = [Candidate('category', 'category_index', BASE + 0x1000 + i, 1, 2, 0, 1)
                      for i in range(620)]
        candidates.extend([
            Candidate('scene','map_id',BASE + 0x3000,2,1,90,96),
            Candidate('character','character_id',BASE + 0x3004,1,1,0,1),
        ])
        source = [obs(90,0),obs(96,0),obs(90,1)]
        report = candidate_report(source,candidates,{'format':PROFILE_FORMAT,'fields':{}})
        encoded = json.dumps(report)
        imported = json.loads(encoded)
        self.assertEqual(imported['total_candidates'],622)
        self.assertEqual(imported['scan_range']['end_exclusive'],'0x80400000')
        self.assertEqual(len(imported['candidates']),622)
        self.assertEqual(imported['candidate_counts']['category']['category_index'],620)
        self.assertEqual(imported['candidate_counts']['scene']['map_id'],1)
        self.assertEqual(imported['candidate_counts']['character']['character_id'],1)
        self.assertEqual(len(imported['observations']),3)
        self.assertNotIn('first',encoded)
        self.assertNotIn('second',encoded)

    def test_bounded_display_preserves_scene_and_character_candidates(self):
        candidates = [Candidate('category','category_index',BASE + 0x1000 + i,1,2,0,1)
                      for i in range(620)]
        candidates.append(Candidate('scene','map_id',BASE+0x3000,2,1,90,96))
        candidates.append(Candidate('character','character_id',BASE+0x3004,1,1,0,1))
        display = display_candidate_indices(candidates,400)
        self.assertEqual(len(display),400)
        self.assertEqual(len(set(display)),400)
        self.assertIn(620,display)
        self.assertIn(621,display)
        self.assertEqual(len(display_candidate_indices(candidates[:7],400)),7)

if __name__=='__main__':unittest.main()

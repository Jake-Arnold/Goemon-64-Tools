import unittest
from unittest.mock import patch
from practice.story_progress import FLAGS,CURATED_FLAGS,EXTERNAL_FLAGS,SAVED_BASE,BANK_A,BANK_B,read_story_state,story_rows,story_edit_options,write_story_value,STORY_SECTIONS,story_section_for_key,validate_story_catalog
from tests.test_unlocks import FakeRAM


class StoryProgressTests(unittest.TestCase):
    def sample(self,d=0,e=0,c=0,mini=0,heel=0):
        ram=FakeRAM()
        ram.write_guest(0x8015C60C,bytes([c,d,e]))
        ram.write_guest(0x8015C6F0,mini.to_bytes(4,'big'))
        ram.write_guest(0x8015C70C,heel.to_bytes(4,'big'))
        ram.writes.clear()
        return ram

    def test_edit_flags_preserves_other_bits_and_validates_observed_bytes(self):
        ram=self.sample(d=0x85)
        self.assertEqual(story_edit_options('ushi_intro'),('Clear','Set'))
        self.assertTrue(write_story_value(ram,'ushi_intro','Set',b'\x85'))
        self.assertEqual(ram.bytes[0x8015C60D],0xA5)
        self.assertTrue(write_story_value(ram,'ushi_intro','Clear',b'\xA5'))
        self.assertEqual(ram.bytes[0x8015C60D],0x85)
        writes=len(ram.writes)
        with self.assertRaises(RuntimeError):write_story_value(ram,'ushi_intro','Set',b'\x00')
        self.assertEqual(len(ram.writes),writes)
        ram.bytes[0x800C7A94]=12
        with self.assertRaises(RuntimeError):write_story_value(ram,'ushi_intro','Set',b'\x85')
        self.assertEqual(len(ram.writes),writes)

    def test_edit_inventory_words_and_disallow_aggregate_rows(self):
        ram=self.sample()
        self.assertEqual(story_edit_options('mini'),('Absent','Present'))
        self.assertTrue(write_story_value(ram,'mini','Present',b'\x00'*4))
        self.assertEqual(ram.read_guest(0x8015C6F0,4),b'\x00\x00\x00\x01')
        self.assertTrue(write_story_value(ram,'mini','Absent',b'\x00\x00\x00\x01'))
        self.assertEqual(story_edit_options('bank_a'),())
        with self.assertRaises(ValueError):write_story_value(ram,'bank_a','Set',b'\x00')
        with self.assertRaises(ValueError):write_story_value(ram,'mini','Set',b'\x00'*4)

    def test_plasma_priority_bits_are_independent_and_all_sources_are_labelled(self):
        ram=self.sample(); ram.bytes[0x8015C60A]=0; ram.bytes[0x8015C608]=0
        self.assertTrue(write_story_value(ram,'external_super_pass','Set',b'\x00'))
        rows={r['key']:r for r in story_rows(read_story_state(ram))}
        self.assertEqual(rows['external_chain_pipe']['value'],'Clear')
        self.assertEqual(rows['external_super_pass']['value'],'Set')
        self.assertIn('user force-tested',rows['external_super_pass']['source'])
        self.assertTrue(write_story_value(ram,'external_chain_pipe','Set',b'\x00'))
        rows={r['key']:r for r in story_rows(read_story_state(ram))}
        self.assertEqual(rows['external_chain_pipe']['value'],'Set')
        self.assertEqual(rows['external_super_pass']['value'],'Set')
        self.assertIn('mn64rando',rows['plasma_sudden_advice']['source'])

    def test_oedo_dialogue_cycle_flags_and_existing_omitsu_annotation(self):
        ram=self.sample();ram.bytes[0x8015C608]=0x84;ram.bytes[0x8015C609]=0x01
        rows={r['key']:r for r in story_rows(read_story_state(ram))}
        for key in ('oedo_old_man_dialogue_cycle','external_omitsu_ufo','oedo_coffee_man_dialogue_cycle'):
            self.assertEqual(rows[key]['value'],'Set')
        self.assertIn('map 432',rows['external_omitsu_ufo']['source'])
        self.assertTrue(write_story_value(ram,'oedo_old_man_dialogue_cycle','Clear',b'\x84'))
        self.assertEqual(ram.bytes[0x8015C608],0x80)
        self.assertEqual(ram.bytes[0x8015C609],0x01)
        self.assertTrue(write_story_value(ram,'oedo_coffee_man_dialogue_cycle','Clear',b'\x01'))
        self.assertEqual(ram.bytes[0x8015C608],0x80)
        self.assertEqual(ram.bytes[0x8015C609],0x00)

    def test_masked_stages_with_cumulative_values(self):
        stages={0:'Introduction not recorded',0x20:'Introduction seen',0x30:'Three blue',
                0x38:'Five yellow',0x3C:'Eight red',0x3E:'Fish-sequence',0x3F:'Golden Temple',
                0x7F:'Training passed',0xBF:'training failed'}
        for value,expected in stages.items():
            state=read_story_state(self.sample(value))
            self.assertIn(expected.lower(),state['ushiwaka'].lower())
            self.assertEqual(state['values']['ushi_intro'],bool(value&0x20))
        state=read_story_state(self.sample(0xFF,2,mini=1,heel=1))
        self.assertTrue(state['values']['training_failed'])
        self.assertTrue(state['values']['training_passed'])
        self.assertIn('Training passed',state['ushiwaka'])  # Original success-reader priority.
        self.assertFalse(state['advisories'])

    def test_decline_precedes_failure_and_referral_precedes_boss(self):
        self.assertIn('declined',read_story_state(self.sample(0xBF,1))['ushiwaka'])
        self.assertIn('Later Miracle',read_story_state(self.sample(e=4))['benkei'])
        self.assertIn('referral',read_story_state(self.sample(e=4,c=8))['benkei'])
        self.assertIn('Fight completed',read_story_state(self.sample(e=8))['benkei'])
        self.assertIn('First dialogue completed',read_story_state(self.sample(e=0x10))['benkei'])

    def test_inventory_and_recorded_flags_are_separate(self):
        state=read_story_state(self.sample(0x3E,2))
        self.assertTrue(any('reward branch may be skipped' in n for n in state['advisories']))
        self.assertTrue(any("Heel reward is recorded" in n for n in state['advisories']))
        state=read_story_state(self.sample(mini=1,heel=1))
        self.assertTrue(any('grant flag is clear' in n for n in state['advisories']))
        self.assertTrue(any('progression flag is clear' in n for n in state['advisories']))
        state=read_story_state(self.sample(mini=0x101))
        self.assertTrue(any('unexpected value' in n for n in state['advisories']))

    def test_bank_namespaces_and_evidence_rows(self):
        ram=self.sample();ram.write_guest(BANK_A,b'\xFF\xFF');ram.write_guest(BANK_B,b'\x55\xAA')
        rows={r['key']:r for r in story_rows(read_story_state(ram))}
        self.assertEqual(rows['bank_a']['raw'],'0xFFFF')
        self.assertEqual(rows['bank_b']['raw'],'0x55AA')
        self.assertEqual(rows['ushi_intro']['value'],'Clear')
        self.assertEqual(rows['ushi_intro']['address'],0x8015C60D)
        self.assertEqual(rows['ushi_intro']['mask'],'0x20')
        self.assertIn('lifecycle',rows['bank_a']['source'])
        self.assertTrue(all(f.evidence and SAVED_BASE<=f.address<SAVED_BASE+0x64 for f in FLAGS))
        self.assertEqual(len({f.key for f in FLAGS}),len(FLAGS))

    def test_catalog_categories_and_unique_ids(self):
        validate_story_catalog()
        self.assertEqual(len({f.flag_id for f in FLAGS}),len(FLAGS))
        self.assertIn('Fortune Dolls',STORY_SECTIONS)
        for key in ('silver_doll_356','placed_gold_doll_0f2','turtle_rock_doll_reward',
                    'fortune_doll_quarters','fortune_doll_total'):
            self.assertEqual(story_section_for_key(key),'Fortune Dolls')
        self.assertEqual(story_section_for_key('oedo_silver_key_1f'),'Keys & Locks')
        self.assertEqual(story_section_for_key('training_passed'),'Ushiwaka & Training')
        self.assertEqual(story_section_for_key('bank_a'),'Diagnostics')

    def test_fortune_counters_are_read_only_story_rows(self):
        ram=self.sample()
        ram.write_guest(0x8015C704,(2).to_bytes(4,'big'))
        ram.write_guest(0x8015C708,(12).to_bytes(4,'big'))
        rows={row['key']:row for row in story_rows(read_story_state(ram))}
        self.assertEqual(rows['fortune_doll_quarters']['value'],'2')
        self.assertEqual(rows['fortune_doll_total']['raw'],'0x0000000C')
        self.assertEqual(story_edit_options('fortune_doll_total'),())

    def test_partial_failures_are_unknown_without_false_inventory_advisory(self):
        ram=self.sample(mini=1,heel=1);read=ram.read_guest
        def partial(addr,size):return b'\x00'*(size-1) if addr==SAVED_BASE else read(addr,size)
        with patch.object(ram,'read_guest',side_effect=partial):state=read_story_state(ram)
        self.assertIsNone(state['values']['mini_recorded'])
        self.assertEqual(state['ushiwaka'],'Unavailable')
        self.assertEqual(state['mini'],1)
        self.assertFalse(state['advisories'])
        self.assertIn('saved',state['errors'])
        self.assertTrue(all(r['value']=='Unavailable' for r in story_rows(state) if r['bank']=='Saved event data'))

    def test_bank_failure_does_not_hide_saved_progress_and_no_writes(self):
        ram=self.sample(0x38);read=ram.read_guest;total=0
        def sampled(addr,size):
            nonlocal total
            total+=size
            if addr==BANK_A:raise OSError('Bank A unavailable')
            return read(addr,size)
        with patch.object(ram,'read_guest',side_effect=sampled),patch.object(ram,'write_guest',side_effect=AssertionError('Read-only')):
            state=read_story_state(ram);story_rows(state)
        self.assertEqual(total,120)  # 100 event bytes, 4 bank bytes, 8 ownership bytes and 8 doll-counter bytes.
        self.assertIn('Five yellow',state['ushiwaka'])
        self.assertIn('bank_a',state['errors'])

    def test_disconnected_values_never_look_clear(self):
        state=read_story_state(None)
        self.assertTrue(all(value is None for value in state['values'].values()))
        self.assertTrue(all(r['raw']=='—' for r in story_rows(state)))

    def test_external_entries_have_distinct_ids_and_explicit_evidence_limits(self):
        self.assertEqual(len(EXTERNAL_FLAGS),37)
        self.assertFalse({f.flag_id for f in EXTERNAL_FLAGS}&{f.flag_id for f in CURATED_FLAGS})
        self.assertEqual(len({f.flag_id for f in FLAGS}),len(FLAGS))
        for flag in EXTERNAL_FLAGS:
            self.assertTrue(flag.external)
            self.assertIn('not locally gameplay-verified',flag.evidence)
            self.assertGreater(flag.reference_count,0)
            self.assertTrue(flag.reference_example.startswith('0x'))
        rows={r['key']:r for r in story_rows(read_story_state(self.sample()))}
        self.assertIn('External annotation',rows['external_koryuta_freed']['source'])
        self.assertIn('opcode-pattern leads',rows['external_koryuta_freed']['source'])

    def test_external_boss_magic_and_travel_masks_decode_independently(self):
        ram=self.sample()
        examples={'external_koryuta_freed':(0x8015C60A,0x10),
                  'external_dharmanyo_defeated':(0x8015C60B,0x01),
                  'external_sudden_granted':(0x8015C60B,0x10),
                  'external_super_jump_granted':(0x8015C60C,0x01),
                  'external_yae_recruited':(0x8015C60F,0x04),
                  'external_tsurami_defeated':(0x8015C610,0x01),
                  'external_super_jump_passed':(0x8015C614,0x02),
                  'external_outer_space':(0x8015C615,0x08)}
        specs={f.key:f for f in EXTERNAL_FLAGS}
        for key,(address,mask) in examples.items():
            self.assertEqual((specs[key].address,specs[key].mask),(address,mask))
            ram.bytes[address]=ram.bytes.get(address,0)|mask
        state=read_story_state(ram)
        self.assertTrue(all(state['values'][key] for key in examples))
        self.assertFalse(state['values']['ushi_intro'])

    def test_congo_candidates_outside_original_prefix_decode_only_their_bits(self):
        ram=self.sample()
        ram.write_guest(0x8015C61C,b'\x90')
        ram.write_guest(0x8015C62E,b'\xF8')
        with patch.object(ram,'write_guest',side_effect=AssertionError('Read only')):
            state=read_story_state(ram)
            rows={r['key']:r for r in story_rows(state)}
        self.assertTrue(state['values']['congo_moon_collected'])
        self.assertFalse(state['values']['congo_state_candidate'])
        self.assertEqual(rows['congo_moon_collected']['address'],0x8015C61C)
        self.assertEqual(rows['congo_moon_collected']['mask'],'0x10')
        self.assertEqual(rows['congo_state_candidate']['address'],0x8015C62E)
        self.assertEqual(rows['congo_state_candidate']['mask'],'0x04')
        self.assertIn('not confirmed',rows['congo_state_candidate']['source'])
        ram.write_guest(0x8015C61C,b'\x80')
        ram.write_guest(0x8015C62E,b'\xFC')
        state=read_story_state(ram)
        self.assertFalse(state['values']['congo_moon_collected'])
        self.assertTrue(state['values']['congo_state_candidate'])

    def test_lord_event_gate_masks_are_independent_of_adjacent_boss_bits(self):
        ram=self.sample()
        ram.write_guest(0x8015C62D,b'\xDF')  # Every bit except the activation gate.
        ram.write_guest(0x8015C61A,b'\x7F')  # Completion gate clear.
        state=read_story_state(ram)
        self.assertFalse(state['values']['lord_event_enabled'])
        self.assertFalse(state['values']['lord_event_completed'])
        ram.write_guest(0x8015C62D,b'\xFF')
        ram.write_guest(0x8015C61A,b'\xFF')
        rows={r['key']:r for r in story_rows(read_story_state(ram))}
        self.assertEqual(rows['lord_event_enabled']['address'],0x8015C62D)
        self.assertEqual(rows['lord_event_enabled']['mask'],'0x20')
        self.assertEqual(rows['lord_event_enabled']['value'],'Set')
        self.assertEqual(rows['lord_event_completed']['address'],0x8015C61A)
        self.assertEqual(rows['lord_event_completed']['mask'],'0x80')
        self.assertEqual(rows['lord_event_completed']['value'],'Set')
        self.assertIn('rejects set',rows['lord_event_completed']['source'])

    def test_ghost_toys_torch_bits_and_door_latch_decode_independently(self):
        ram=self.sample()
        keys=('ghost_torch_04','ghost_torch_08','ghost_entrance_unlocked')
        for value,expected in ((0x02,(False,False,False)),(0x06,(True,False,False)),
                               (0x0A,(False,True,False)),(0x1E,(True,True,True)),
                               (0x10,(False,False,True)),(0xE2,(False,False,False))):
            ram.write_guest(0x8015C63B,bytes([value]))
            state=read_story_state(ram)
            self.assertEqual(tuple(state['values'][key] for key in keys),expected)
        rows={r['key']:r for r in story_rows(state)}
        self.assertEqual([rows[k]['mask'] for k in keys],['0x04','0x08','0x10'])
        self.assertTrue(all(rows[k]['address']==0x8015C63B for k in keys))

    def test_castle_map_pickups_are_separate_masked_flags(self):
        ram=self.sample()
        cases=(('oedo_elly_collected',0x8015C627,0x80,0x0FF),
               ('ghost_arrow_collected',0x8015C628,0x20,0x105),
               ('musical_arrow_collected',0x8015C629,0x01,0x108))
        specs={f.key:f for f in FLAGS}
        for key,address,mask,flag_id in cases:
            self.assertEqual(specs[key].flag_id,flag_id)
            ram.write_guest(address,bytes([255^mask]))
        state=read_story_state(ram)
        self.assertTrue(all(state['values'][key] is False for key,_,_,_ in cases))
        for key,address,mask,_ in cases:
            ram.write_guest(address,b'\xFF')
        state=read_story_state(ram);rows={r['key']:r for r in story_rows(state)}
        for key,address,mask,_ in cases:
            self.assertTrue(state['values'][key])
            self.assertEqual(rows[key]['address'],address)
            self.assertEqual(rows[key]['mask'],f'0x{mask:02X}')
            self.assertIn('User',rows[key]['source'])

    def test_kegon_hint_mask_preserves_adjacent_story_bits(self):
        ram=self.sample()
        ram.write_guest(0x8015C610,b'\x04')
        self.assertFalse(read_story_state(ram)['values']['kegon_plasma_hint'])
        ram.write_guest(0x8015C610,b'\x14')
        state=read_story_state(ram);row=next(r for r in story_rows(state) if r['key']=='kegon_plasma_hint')
        self.assertTrue(state['values']['kegon_plasma_hint'])
        self.assertEqual(row['address'],0x8015C610)
        self.assertEqual(row['mask'],'0x10')
        self.assertIn('access not established',row['source'])
        self.assertEqual(ram.u8(0x8015C610),0x14)

    def test_oedo_silver_keys_keep_collection_bits_when_lock_opens(self):
        ram=self.sample()
        names=('oedo_silver_key_1f','oedo_silver_key_2f','oedo_silver_lock_2f')
        for value,expected in ((0,(False,False,False)),(1,(True,False,False)),
                               (0x11,(True,True,False)),(0x19,(True,True,True))):
            ram.write_guest(0x8015C62A,bytes([value]))
            state=read_story_state(ram)
            self.assertEqual(tuple(state['values'][key] for key in names),expected)
        rows={r['key']:r for r in story_rows(state)}
        self.assertEqual([rows[k]['mask'] for k in names],['0x01','0x10','0x08'])
        self.assertTrue(all(rows[k]['address']==0x8015C62A for k in names))
        self.assertIn('not current key count',rows[names[1]]['source'])

    def test_oedo_first_lock_keeps_pickup_history_and_separate_arrow_bit(self):
        ram=self.sample();ram.write_guest(0x8015C62A,b'\x19')
        ram.write_guest(0x8015C629,b'\x01')
        self.assertFalse(read_story_state(ram)['values']['oedo_silver_lock_1f'])
        ram.write_guest(0x8015C629,b'\x81')
        state=read_story_state(ram)
        self.assertTrue(state['values']['oedo_silver_lock_1f'])
        self.assertTrue(state['values']['musical_arrow_collected'])
        self.assertTrue(state['values']['oedo_silver_key_1f'])
        self.assertTrue(state['values']['oedo_silver_key_2f'])
        self.assertTrue(state['values']['oedo_silver_lock_2f'])
        row=next(r for r in story_rows(state) if r['key']=='oedo_silver_lock_1f')
        self.assertEqual((row['address'],row['mask']),(0x8015C629,'0x80'))
        self.assertIn('1 to 0',row['source'])

    def test_gourmet_key_is_separate_from_bazooka_room_event(self):
        ram=self.sample();ram.write_guest(0x8015C63C,b'\x20')
        self.assertFalse(read_story_state(ram)['values']['gourmet_silver_key_129'])
        ram.write_guest(0x8015C637,b'\x08')
        state=read_story_state(ram);row=next(r for r in story_rows(state) if r['key']=='gourmet_silver_key_129')
        self.assertTrue(state['values']['gourmet_silver_key_129'])
        self.assertEqual((row['address'],row['mask']),(0x8015C637,'0x08'))
        self.assertEqual(ram.u8(0x8015C63C),0x20)

    def test_silver_doll_instance_flags_are_separate_from_strength_flag(self):
        ram=self.sample();ram.write_guest(0x8015C611,b'\x40')
        keys=(('silver_doll_356',0x8015C625,0x20),('silver_doll_381',0x8015C626,0x02),('silver_doll_fuji',0x8015C623,0x08))
        self.assertTrue(read_story_state(ram)['values']['strength_gauge_condition'])
        for key,addr,mask in keys:
            self.assertFalse(read_story_state(ram)['values'][key])
            ram.write_guest(addr,bytes([mask]))
        state=read_story_state(ram)
        self.assertTrue(all(state['values'][k] for k,_,_ in keys))
        self.assertTrue(state['values']['strength_gauge_condition'])

import unittest
from unittest.mock import patch
from practice.story_progress import FLAGS,CURATED_FLAGS,EXTERNAL_FLAGS,SAVED_BASE,BANK_A,BANK_B,read_story_state,story_rows
from tests.test_unlocks import FakeRAM


class StoryProgressTests(unittest.TestCase):
    def sample(self,d=0,e=0,c=0,mini=0,heel=0):
        ram=FakeRAM()
        ram.write_guest(0x8015C60C,bytes([c,d,e]))
        ram.write_guest(0x8015C6F0,mini.to_bytes(4,'big'))
        ram.write_guest(0x8015C70C,heel.to_bytes(4,'big'))
        ram.writes.clear()
        return ram

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
        self.assertEqual(total,112)  # Full 100-byte events plus two banks and inventory words.
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
        self.assertTrue(state['values']['congo_defeat_candidate'])
        self.assertFalse(state['values']['congo_state_candidate'])
        self.assertEqual(rows['congo_defeat_candidate']['address'],0x8015C61C)
        self.assertEqual(rows['congo_defeat_candidate']['mask'],'0x10')
        self.assertEqual(rows['congo_state_candidate']['address'],0x8015C62E)
        self.assertEqual(rows['congo_state_candidate']['mask'],'0x04')
        self.assertIn('not confirmed',rows['congo_state_candidate']['source'])
        ram.write_guest(0x8015C61C,b'\x80')
        ram.write_guest(0x8015C62E,b'\xFC')
        state=read_story_state(ram)
        self.assertFalse(state['values']['congo_defeat_candidate'])
        self.assertTrue(state['values']['congo_state_candidate'])

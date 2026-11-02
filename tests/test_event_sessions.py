import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from practice.event_sessions import (EVENT_START,EVENT_SIZE,capture_event,new_session,
    with_trial,rank_bits,save_session,load_session,validate_session)
from tests import test_checkpoint


class EventSessionTests(unittest.TestCase):
    def setUp(self):
        self.process,self.ram=test_checkpoint.TestCheckpoint().sample()
        self.ram.write_guest(EVENT_START,bytes(EVENT_SIZE))

    def trial(self,a,b,c=None):
        captures={}
        for stage,value in (('A',a),('B',b),('C',c)):
            if value is not None:
                self.ram.write_guest(EVENT_START,bytes([value])+bytes(EVENT_SIZE-1))
                captures[stage]=capture_event(self.ram)
        return captures

    def test_repeat_noise_opposites_absence_and_bit_reversal(self):
        session=new_session('Talk','project64')
        first=self.trial(0,0x23,0x01)
        session=with_trial(session,'event','first',first)
        session=with_trial(session,'event','repeat',self.trial(0,0x23))
        session=with_trial(session,'idle','timer',self.trial(0,0x02))
        session=with_trial(session,'control','item only',self.trial(0,0x01))
        rows=rank_bits(session)['candidates']
        self.assertEqual(rows[0]['mask'],'20')
        self.assertEqual(len(rows[0]['support']),2)
        self.assertEqual(rows[0]['reverted'],[session['trials'][0]['id']])
        noisy=next(r for r in rows if r['mask']=='01')
        self.assertEqual(noisy['control_overlap'],[session['trials'][3]['id']])
        self.assertEqual(noisy['not_reverted'],[session['trials'][0]['id']])
        session=with_trial(session,'event','opposite',self.trial(0x20,0))
        session=with_trial(session,'event','unchanged',self.trial(0,0))
        row=next(r for r in rank_bits(session)['candidates'] if r['mask']=='20' and r['direction']=='set')
        self.assertEqual(len(row['opposite']),1);self.assertEqual(len(row['absent']),1)
        self.assertFalse(row['confirmed'])
        self.assertEqual(rank_bits(session),rank_bits(session))

    def test_all_event_bytes_analysed_and_no_ui_truncation(self):
        caps=self.trial(0,0)
        self.ram.write_guest(EVENT_START+EVENT_SIZE-1,b'\x80')
        caps['B']=capture_event(self.ram)
        session=with_trial(new_session('Last byte','recomp'),'event','',caps)
        self.assertEqual(rank_bits(session)['candidates'][0]['address'],'0x8015C66B')

    def test_capture_is_read_only_bounded_and_rejects_partial_read(self):
        original=self.ram.read_guest;total=0
        def counted(address,length):
            nonlocal total
            total+=length;return original(address,length)
        with patch.object(self.ram,'write_guest',side_effect=AssertionError('No writes')):
            with patch.object(self.ram,'read_guest',side_effect=counted):capture_event(self.ram)
        self.assertLess(total,256)
        def partial(address,length):
            return b'' if address==EVENT_START else original(address,length)
        with patch.object(self.ram,'read_guest',side_effect=partial):
            with self.assertRaisesRegex(OSError,'Incomplete'):capture_event(self.ram)

    def test_context_changes_between_captures_allowed_but_mid_capture_and_scripts_rejected(self):
        caps=self.trial(0,1)
        for key in ('map_id','character','player_ptr','task_ptr'):
            changed=copy.deepcopy(caps);changed['B']['context'][key]+=1
            session=with_trial(new_session('Talk','recomp'),'event','',changed)
            report=rank_bits(session)
            self.assertEqual(report['context_changes'][session['trials'][0]['id']],[key])
            self.assertEqual(report['candidates'][0]['mask'],'01')
        self.ram.write_guest(0x80077858,b'\x01')
        with self.assertRaisesRegex(ValueError,'scripts'):capture_event(self.ram)
        self.ram.write_guest(0x80077858,b'\x00')
        original=self.ram.read_guest
        def transition(address,length):
            result=original(address,length)
            if address==EVENT_START:self.ram.write_guest(0x800C7AB2,b'\x00\x24')
            return result
        with patch.object(self.ram,'read_guest',side_effect=transition):
            with self.assertRaisesRegex(ValueError,'context changed'):capture_event(self.ram)

    def test_trial_order_mixed_context_and_input_copy(self):
        session=new_session('Talk','project64');caps=self.trial(0,1)
        changed=copy.deepcopy(caps);changed['A'],changed['B']=changed['B'],changed['A']
        with self.assertRaisesRegex(ValueError,'time order'):with_trial(session,'event','',changed)
        recorded=with_trial(session,'event','',caps)
        caps['A']['context']['map_id']=99
        self.assertNotEqual(recorded['trials'][0]['captures']['A']['context']['map_id'],99)
        changed=self.trial(0,1)
        for capture in changed.values():capture['context']['map_id']=99
        recorded=with_trial(recorded,'event','another source map',changed)
        self.assertEqual(len(recorded['trials']),2)
        self.assertEqual(rank_bits(recorded)['candidates'][0]['support'],[t['id'] for t in recorded['trials']])

    def test_atomic_roundtrip_unknown_schema_and_failed_save(self):
        session=with_trial(new_session('Talk','project64'),'idle','',self.trial(0,0))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'session.json';save_session(path,session)
            self.assertEqual(load_session(path),session)
            before=path.read_bytes()
            with patch('practice.event_sessions.os.replace',side_effect=OSError('disk failure')):
                with self.assertRaises(OSError):save_session(path,session)
            self.assertEqual(path.read_bytes(),before)
            self.assertEqual(list(Path(folder).glob('*.tmp')),[])
            bad=copy.deepcopy(session);bad['format']='future-v2'
            with self.assertRaisesRegex(ValueError,'Unsupported'):save_session(path,bad)
            self.assertEqual(path.read_bytes(),before)
            path.write_text('{broken')
            with self.assertRaises(ValueError):load_session(path)

    def test_validation_duplicate_ids_bad_encoding_and_unverified_rom(self):
        session=with_trial(new_session('Talk','recomp','a'*40),'event','',self.trial(0,1))
        self.assertFalse(rank_bits(session)['rom_identity_verified'])
        for mutation in ('duplicate','encoding','role'):
            bad=copy.deepcopy(session)
            if mutation=='duplicate':bad['trials'].append(copy.deepcopy(bad['trials'][0]))
            elif mutation=='encoding':bad['trials'][0]['captures']['A']['bytes_hex']='00'
            else:bad['trials'][0]['role']='guess'
            with self.assertRaises(ValueError):validate_session(bad)

    def test_cross_room_trial_context_roundtrip_and_invalid_context_rejection(self):
        caps=self.trial(0,0x10,0)
        caps['B']['context'].update(map_id=99,character=1,player_ptr=0x801B0000,task_ptr=0x801B0100)
        session=with_trial(new_session('Post-boss chat','recomp'),'event','room transition',caps)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'trial.json';save_session(path,session)
            self.assertEqual(load_session(path),session)
        report=rank_bits(session)
        self.assertEqual(len(report['context_changes'][session['trials'][0]['id']]),4)
        self.assertEqual(report['candidates'][0]['reverted'],[session['trials'][0]['id']])
        bad=copy.deepcopy(session);bad['trials'][0]['captures']['B']['context']['player_ptr']=0
        with self.assertRaisesRegex(ValueError,'player_ptr'):validate_session(bad)

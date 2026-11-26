import threading
import unittest
from types import SimpleNamespace
from practice.native_state_control import run_state_job, state_complete, LOAD, SAVE, ADVANCE


class FakeInspector:
    def __init__(self):
        self.cv=threading.Condition();self.state=3;self.recording=self.stepping=self.finished=False
        self.state_job_expected=self.state_job_result=None;self.state_job_notice='';self.serial=0
        self.rows=[dict(frame=1)];self.watches=[dict(name='a')];self.last=self.rows[0]
        self.player_base=42;self.player_text='x';self.player_watches_suspended=False;self.watch_errors={};self.error='';self.unlock_result=None
        self.core=SimpleNamespace(core_version=0x020600,queue_state=self.queue_state,cmd=self.cmd,locate_japan_player=lambda:42)
        self.calls=[];self.result=1
    def set_input(self,v):self.calls.append(('input',v.copy()))
    def queue_state(self,op,slot):self.calls.append(('queue',op,slot));self.parameter=op
    def cmd(self,op):
        self.calls.append(('advance',op));self.serial+=1
        state_complete(self,self.parameter,self.result)
    def wait(self,predicate,timeout):assert predicate()


class NativeStateControlTests(unittest.TestCase):
    def test_save_keeps_trace_and_uses_neutral_boundary(self):
        i=FakeInspector();run_state_job(i,'save_state',2)
        self.assertEqual(i.calls,[('input',dict(buttons=0,x=0,y=0)),('queue',SAVE,2),('advance',ADVANCE)])
        self.assertEqual(i.rows,[dict(frame=1)]);self.assertIsNone(i.state_job_expected)
        self.assertIn('Saved slot 2',i.state_job_notice)
    def test_load_requires_confirmation_then_preserves_watches(self):
        i=FakeInspector()
        with self.assertRaisesRegex(RuntimeError,'confirmation'):run_state_job(i,'load_state',0)
        self.assertEqual(i.calls,[])
        run_state_job(i,'load_state',0,True)
        self.assertEqual(i.rows,[]);self.assertEqual(i.watches,[dict(name='a')]);self.assertEqual(i.player_base,42)
        self.assertIsNone(i.last);self.assertFalse(i.player_watches_suspended);self.assertEqual(i.player_text,'x')
        self.assertIn('Loaded slot 0',i.state_job_notice);self.assertIsNone(i.state_job_expected)
    def test_manual_watch_retention_and_located_identity_change(self):
        i=FakeInspector();i.player_base=None;i.player_text=None
        i.core.locate_japan_player=lambda: self.fail('manual watches must not trigger locator')
        run_state_job(i,'load_state',0,True)
        self.assertEqual(i.watches,[dict(name='a')]);self.assertFalse(i.player_watches_suspended)
        i=FakeInspector();i.core.locate_japan_player=lambda:43
        run_state_job(i,'load_state',0,True)
        self.assertTrue(i.player_watches_suspended);self.assertEqual(i.player_base,42)
        self.assertEqual(i.watches,[dict(name='a')]);self.assertIn('Locate Player again',i.state_job_notice)
        i=FakeInspector();i.core.locate_japan_player=lambda: (_ for _ in ()).throw(RuntimeError('ambiguous'))
        run_state_job(i,'load_state',0,True)
        self.assertTrue(i.player_watches_suspended);self.assertEqual(i.watches,[dict(name='a')])
    def test_bad_slot_running_and_core_rejected(self):
        i=FakeInspector()
        for slot in (-1,10,True,'0'):
            with self.assertRaises(ValueError):run_state_job(i,'save_state',slot)
        i.state=2
        with self.assertRaises(RuntimeError):run_state_job(i,'save_state',0)
        i.state=3;i.core.core_version=0x020500
        with self.assertRaises(RuntimeError):run_state_job(i,'save_state',0)
        self.assertEqual(i.calls,[])
    def test_acknowledged_failure_and_unresolved_job(self):
        i=FakeInspector();i.result=0
        with self.assertRaisesRegex(RuntimeError,'failed'):run_state_job(i,'load_state',0,True)
        self.assertIsNone(i.state_job_expected);self.assertEqual(i.watches,[dict(name='a')]);self.assertTrue(i.player_watches_suspended)
        i=FakeInspector();i.core.cmd=lambda _: (_ for _ in ()).throw(RuntimeError('interrupted'))
        with self.assertRaisesRegex(RuntimeError,'interrupted'):run_state_job(i,'save_state',0)
        self.assertEqual(i.state_job_expected,SAVE)
        with self.assertRaises(RuntimeError):run_state_job(i,'save_state',0)
        state_complete(i,LOAD,1);self.assertIsNone(i.state_job_result)

if __name__=='__main__':unittest.main()

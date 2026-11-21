"""ROM-free tests of the declarative tracer; no live game required."""
import json
import unittest
from copy import deepcopy

from practice.scripted_trace import (SCRIPT_FORMAT, PRESETS, ScriptedTracer,
                                     parse_script)


class RAM:
    def __init__(self):
        self.bytes={};self.reads=0;self.writes=0;self.fail=False
    def write_guest(self,address,data):
        self.writes+=1
        for i,b in enumerate(data):self.bytes[address+i]=b
    def read_guest(self,address,size):
        if self.fail:raise OSError('process disappeared')
        self.reads+=1
        return bytes(self.bytes.get(address+i,0) for i in range(size))


def script(watches=None,triggers=None,**kwargs):
    d={'format':SCRIPT_FORMAT,'name':'test','sample_ms':100,'max_events':64,
       'log_changes':True,
       'watches':watches or [{'name':'flag','address':'0x80001000','type':'u8'}],
       'triggers':triggers if triggers is not None else []}
    d.update(kwargs)
    return d


class TracerTests(unittest.TestCase):
    def test_presets_and_required_fields(self):
        self.assertEqual(set(PRESETS),{'Script VM / dialogue','Scene transitions'})
        for s in PRESETS.values():
            spec=parse_script(s)
            self.assertTrue(spec.watches and spec.triggers)
            self.assertEqual(spec.source,s)

    def test_reject_arbitrary_execution_unknown_keys_and_malformed_formats(self):
        for payload in (
            {'format':'unknown','name':'a','watches':[]},
            script(command='exec("rm")'),
            script(watches=[{'name':'flag','address':'0xBFC00000','type':'u8'}]),
            script(watches=[{'name':'flag','address':'0x80001000','type':'u32'}],triggers=[{'name':'x','watch':'flag','op':'call_function'}]),
            script(watches=[{'name':'flag','address':'0x80001001','type':'u32'}]),
            script(watches=[{'name':'flag','address':'0x80001000','type':'u8'}]*2),
            script(sample_ms=10),
            script(max_events=True),
            script(triggers=[{'name':'foo','watch':'missing','op':'changed'}]),
            script(triggers=[{'name':'foo','watch':'flag','op':'eq','value':True}]),
            script(triggers=[{'name':'foo','watch':'flag','op':'bit_set','mask':'0x100'}]),
            script(watches=[{'name':['bad'],'address':'0x80001000','type':'u8'}]),
            script(watches=[{'name':'flag','address':'0x80001000','type':[]}]),
            script(triggers=[{'name':'x','watch':[],'op':'changed'}]),
            script(triggers=[{'name':'x','watch':'flag','op':[]}]),
            script(triggers=[{'name':'x','watch':'flag','op':'changed','capture':[{}]}]),
        ):
            with self.subTest(payload=payload),self.assertRaises(ValueError):parse_script(payload)
        with self.assertRaises(ValueError):parse_script('x'*70000)

    def test_priming_sample_throttling_and_detect_changes(self):
        ram=RAM();t=ScriptedTracer();t.start(ram,parse_script(script()),now=10.0)
        self.assertEqual(t.sample_count,1)
        self.assertEqual(t.events,[])
        ram.write_guest(0x80001000,b'\x04')
        self.assertEqual(t.poll(now=10.05),[])
        changes=t.poll(now=10.11)
        self.assertEqual(len(changes),1)
        self.assertEqual(changes[0]['before'],'00')
        self.assertEqual(changes[0]['after'],'04')
        self.assertEqual(changes[0]['after_value'],4)
        self.assertEqual(t.sample_count,2)
        self.assertEqual(t.events[0]['kind'],'change')
        self.assertEqual(t.jsonl().count('\n'),2)
        self.assertEqual(ram.writes,1)  # game writes only; tracer never writes

    def test_snapshot_pre_and_post_ordering_with_complete_marker(self):
        trig=[{'name':'flag_change','watch':'flag','op':'changed','pre_samples':2,
               'post_samples':2,'capture':['flag']}]
        ram=RAM();t=ScriptedTracer();t.start(ram,parse_script(script(triggers=trig,log_changes=False)),now=0)
        t.poll(now=.11)
        ram.write_guest(0x80001000,b'\x01')
        entries=t.poll(now=.22)
        self.assertEqual(len(entries),1)
        e=entries[0]
        self.assertEqual(e['kind'],'trigger')
        self.assertEqual([x['sample'] for x in e['before']],[1,2])
        self.assertEqual(e['observed']['sample'],3)
        self.assertEqual(e['after'],[])
        self.assertFalse(e['complete'])
        t.poll(now=.33)
        self.assertEqual([x['sample'] for x in e['after']],[4])
        t.poll(now=.44)
        self.assertEqual([x['sample'] for x in e['after']],[4,5])
        self.assertTrue(e['complete'])
        self.assertEqual(list(e['before'][0]['values']),['flag'])
        self.assertEqual(ram.reads,5)

    def test_bit_rise_fall_comparison_and_cooldown(self):
        triggers=[
            {'name':'set','watch':'flag','op':'bit_set','mask':'0x04','post_samples':0},
            {'name':'clear','watch':'flag','op':'bit_clear','mask':4,'post_samples':0},
            {'name':'target','watch':'flag','op':'eq','value':4,'cooldown_ms':500,'post_samples':0},
        ]
        ram=RAM();t=ScriptedTracer();t.start(ram,parse_script(script(triggers=triggers,log_changes=False)),now=0)
        ram.write_guest(0x80001000,b'\x04')
        self.assertEqual([e['trigger'] for e in t.poll(now=.11)],['set','target'])
        self.assertEqual(t.poll(now=.22),[])
        ram.write_guest(0x80001000,b'\x00')
        self.assertEqual([e['trigger'] for e in t.poll(now=.33)],['clear'])
        ram.write_guest(0x80001000,b'\x04')
        self.assertEqual([e['trigger'] for e in t.poll(now=.44)],['set'])
        self.assertEqual(t.poll(now=.55),[])
        ram.write_guest(0x80001000,b'\x00');t.poll(now=.66)
        ram.write_guest(0x80001000,b'\x04')
        self.assertEqual([e['trigger'] for e in t.poll(now=.77)],['set','target'])

    def test_once_and_increased_decreased(self):
        triggers=[{'name':'increase','watch':'flag','op':'increased','once':True,'post_samples':0},
                  {'name':'decrease','watch':'flag','op':'decreased','post_samples':0}]
        r=RAM();t=ScriptedTracer();t.start(r,parse_script(script(triggers=triggers,log_changes=False)),now=0)
        for n,v in enumerate((1,2,1,2),1):
            r.write_guest(0x80001000,bytes([v]));t.poll(now=n*.2)
        self.assertEqual([e['trigger'] for e in t.events],['increase','decrease'])

    def test_event_limits_marker_and_jsonl_structured(self):
        r=RAM();t=ScriptedTracer();t.start(r,parse_script(script(max_events=2)),now=0)
        for i in range(1,6):
            r.write_guest(0x80001000,bytes([i]));t.poll(now=i*.2)
        self.assertEqual(len(t.events),2)
        t.mark('Start cutscene')
        self.assertEqual(len(t.events),2)
        self.assertEqual(t.events[-1]['kind'],'marker')
        records=[json.loads(line) for line in t.jsonl().splitlines()]
        self.assertEqual(records[0]['record'],'session')
        self.assertEqual(records[0]['format'],'goemon-scripted-trace-session-v1')
        self.assertEqual(records[-1]['record'],'event')
        self.assertIn('Host-polled',records[0]['observation'])
        t.stop();self.assertFalse(t.running)
        self.assertEqual(t.document()['status'],'stopped')

    def test_reconnect_fail_closed_and_evidence_retained(self):
        r=RAM();t=ScriptedTracer();t.start(r,parse_script(script()),now=0)
        r.write_guest(0x80001000,b'\x01');t.poll(now=.2)
        r.fail=True
        with self.assertRaisesRegex(OSError,'Trace stopped'):
            t.poll(now=.4)
        self.assertFalse(t.running)
        self.assertEqual(len(t.events),1)
        self.assertEqual(t.document()['event_count'],1)
        self.assertIsNone(t.ram)

    def test_signed_and_float_canonical_big_endian(self):
        watches=[{'name':'signed','address':'0x80002000','type':'s16'},
                 {'name':'float','address':'0x80002004','type':'f32'}]
        r=RAM();r.write_guest(0x80002000,(-5).to_bytes(2,'big',signed=True));r.write_guest(0x80002004,bytes.fromhex('3FC00000'))
        spec=parse_script(script(watches=watches,triggers=[{'name':'negative','watch':'signed','op':'lt','value':-3}]))
        t=ScriptedTracer();t.start(r,spec,now=0)
        self.assertEqual(t._last_frame['values']['signed']['value'],-5)
        self.assertEqual(t._last_frame['values']['float']['value'],1.5)
        r.write_guest(0x80002000,(-2).to_bytes(2,'big',signed=True))
        t.poll(now=.2)
        self.assertEqual([e['kind'] for e in t.events],['change'])

    def test_trace_on_guest_alias_and_no_native_hook_claim(self):
        spec=parse_script(script(watches=[{'name':'alias','address':'0xA0001000','type':'u32'}]))
        self.assertEqual(spec.watches[0].address,0xA0001000)
        r=RAM();t=ScriptedTracer();t.start(r,spec,now=0)
        self.assertNotIn('pc',t.document())
        self.assertNotIn('callstack',t.document())


class UiTests(unittest.TestCase):
    def test_scripted_tab_start_mark_and_stop(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from practice.pj64_debugger_ui import PJ64DebuggerMixin
        try:root=tk.Tk()
        except tk.TclError as exc:self.skipTest('No Tk display: '+str(exc))
        try:
            class App(PJ64DebuggerMixin):pass
            app=App();app.root=root;app.args=Namespace(enable_hex_edit=False)
            app.mem=RAM();app.game_pid=123
            app.notebook=ttk.Notebook(root);app.notebook.pack()
            app.build_pj64_debugger_tab(app.notebook)
            self.assertEqual(app.debug_pages.tab(app.scripted_trace_tab,'text'),'Scripted tracer')
            app.scripted_trace_start()
            self.assertTrue(app.scripted_tracer.running)
            app.scripted_trace_add_mark()
            self.assertEqual(app.scripted_tracer.events[-1]['kind'],'marker')
            app.scripted_trace_stop()
            self.assertFalse(app.scripted_tracer.running)
            app.scripted_trace_start()
            app.mem=RAM()
            app.poll_pj64_debugger(99.0)
            self.assertFalse(app.scripted_tracer.running)
            self.assertIn('disconnect/reconnect',app.scripted_trace_status.get())
        finally:root.destroy()


if __name__=='__main__':unittest.main()

"""Synthetic native API tests. No live emulator or retail ROM is used."""
import ctypes as C
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from practice.mupen_native import (Inspector, NativeCore, PAUSED, RUNNING, ADVANCE, PAUSE, RESUME, STOP,
    NEUTRAL, parse_watches, valid_input, write_trace)
from practice.pj64_frame_control import controller_input

ROOT=Path(__file__).resolve().parents[1]


class MockCore:
    def __init__(self, ins):
        self.ins=ins; self.word=1; self.input=dict(NEUTRAL); self.extra=False; self.no_polls=False
    def set_input(self, buttons, x, y, /): self.input=dict(buttons=buttons,x=x,y=y); return True
    def polls(self): return 0 if self.no_polls else 1
    def read_watch(self,w): return self.word
    def cmd(self, op):
        if op==PAUSE: self.ins.state_changed(PAUSED)
        if op==RESUME: self.ins.state_changed(RUNNING)
        if op==STOP: self.ins.state_changed(1)
        if op==ADVANCE:
            self.ins.state_changed(RUNNING); self.word+=1
            self.ins.frame(self.word)
            if self.extra:self.ins.frame(self.word+1)
            self.ins.state_changed(PAUSED)


class NativeInspectorTests(unittest.TestCase):
    def setup_inspector(self):
        i=Inspector(parse_watches('action u16 80001002','japan'),'japan'); i.core=MockCore(i);i.state_changed(PAUSED);return i
    def test_watches_validate_and_resolve_region(self):
        with patch('practice.mupen_native.guest_address',return_value=0x80000100) as resolve:
            self.assertEqual(parse_watches('action u16 @test','japan')[0]['address'],0x80000100)
            resolve.assert_called_once_with('test',region='japan',width=2)
        for value in ('action u16 80001001','frame u32 80001000','a f32 80400000','a u16 80000000\na u8 80000000'):
            with self.assertRaises(ValueError):parse_watches(value,'usa')
        with self.assertRaises(ValueError):valid_input(dict(buttons=64,x=0,y=0))
        with self.assertRaises(ValueError):valid_input(dict(buttons=0,x=81,y=0))
    def test_live_schema_is_atomic_and_paused_only(self):
        i=self.setup_inspector(); i.control(dict(op='step',inputs=[NEUTRAL]))
        old=i.report(); command=dict(op='watches',text='new s16 80001004')
        with self.assertRaisesRegex(RuntimeError,'Export and clear'):i.control(command)
        with self.assertRaises(ValueError):i.control(dict(op='watches',text='bad f32 80001001',replace_trace=True))
        self.assertEqual(i.report(),old)
        i.control(dict(op='record'))
        with self.assertRaises(RuntimeError):i.control(dict(command,replace_trace=True))
        i.control(dict(op='record')); i.control(dict(op='resume'))
        with self.assertRaises(RuntimeError):i.control(dict(command,replace_trace=True))
        i.control(dict(op='pause'));r=i.control(dict(command,replace_trace=True))
        self.assertEqual(r['watches'][0]['name'],'new');self.assertEqual(r['rows'],[]);self.assertIsNone(r['last'])
        self.assertEqual(r['serial'],old['serial']); self.assertEqual(r['state'],PAUSED)
        r=i.control(dict(op='step',inputs=[NEUTRAL]));self.assertIn('new',r['rows'][0]);self.assertNotIn('action',r['rows'][0])
        self.assertEqual(i.control(command)['rows'],r['rows'])
    def test_pointer_chains_follow_relocation_and_reject_invalid(self):
        c=object.__new__(NativeCore);c.debugger=True; reads=[]
        mem={0x80001000:0x80002000,0x8000205c:0x80003000,0x80003020:0x3f333333,0x80004020:0x3f800000}
        c.readers={4:lambda addr:(reads.append(addr),mem.get(addr,0))[1]}
        c.mem_info=lambda typ,addr:2 if typ==1 else 1
        w=parse_watches('history f32 80001000->5C->20','japan')[0]
        self.assertAlmostEqual(c.read_watch(w),.7,places=6)
        mem[0x8000205c]=0x80004000;self.assertEqual(c.read_watch(w),1.0)
        for value in (0,0x80400000,0xA0002000,0x80002001,0xFFFFFFFF,0x803FFFFC):
            mem[0x80001000]=value;reads.clear();self.assertIsNone(c.read_watch(w));self.assertEqual(reads,[0x80001000])
        for bad in ('bad u32 80001000->','bad u32 80001000->-1','bad u32 80001000->400000','bad u32 80001000->0->0->0->0->0','bad u16 80001002->0'):
            with self.assertRaises(ValueError):parse_watches(bad,'japan')
    def test_signed_native_reads_and_preset(self):
        c=object.__new__(NativeCore);c.debugger=False
        buf=(C.c_uint32*1)(0xFFB7FF80);c.rdram_pointer=lambda n:C.addressof(buf)
        self.assertEqual(c.read_watch(dict(kind='s16',address=0x80000000)),-73)
        self.assertEqual(c.read_watch(dict(kind='s8',address=0x80000003)),-128)
        self.assertEqual(c.read_watch(dict(kind='s32',address=0x80000000)),C.c_int32(0xFFB7FF80).value)
        from practice.mupen_native_ui import JP_CONTROLLER_WATCHES
        w=parse_watches(JP_CONTROLLER_WATCHES,'japan')
        self.assertEqual(len(w),10);self.assertEqual(w[0],dict(name='raw_x',kind='s16',address=0x800CD52E))
        self.assertEqual(w[2]['address'],0x800CD534)
        with self.assertRaises(ValueError):parse_watches(JP_CONTROLLER_WATCHES,'usa')
    def test_ctypes_input_uses_positional_arguments(self):
        i=self.setup_inspector();calls=[]
        i.core.set_input=C.CFUNCTYPE(C.c_int,C.c_uint,C.c_int,C.c_int)(lambda b,x,y:(calls.append((b,x,y)),1)[1])
        i.set_input(dict(buttons=8,x=-80,y=40));self.assertEqual(calls,[(8,-80,40)])
    def test_step_capture_and_neutral_release(self):
        i=self.setup_inspector(); x=controller_input(['CU'],80,-80)
        r=i.control(dict(op='step',inputs=[x,NEUTRAL]))
        self.assertEqual([row['action'] for row in r['rows']],[2,3]);self.assertEqual(r['rows'][0]['buttons'],8)
        self.assertEqual(i.core.input,NEUTRAL);self.assertEqual(r['state'],PAUSED)
        self.assertFalse(r['capabilities']['logic_updates']);self.assertFalse(r['capabilities']['ram_writes'])
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'trace.json';b=Path(d)/'trace.csv';write_trace(a,r);write_trace(b,r)
            self.assertEqual(json.loads(a.read_text())['rows'],r['rows']);self.assertIn('core-frame',b.read_text())
    def test_running_and_multiple_callback_rejected(self):
        i=self.setup_inspector();i.control(dict(op='resume'))
        with self.assertRaises(RuntimeError):i.control(dict(op='step',inputs=[NEUTRAL]))
        i.control(dict(op='pause'));i.core.extra=True
        with self.assertRaisesRegex(RuntimeError,'Multiple core callbacks'):i.control(dict(op='step',inputs=[NEUTRAL]))
        self.assertEqual(i.core.input,NEUTRAL)
    def test_trace_bound_and_record(self):
        i=self.setup_inspector();i.control(dict(op='record'))
        for n in range(601):i.frame(n)
        self.assertEqual(len(i.rows),600);self.assertFalse(i.recording);self.assertIn('limit',i.error)
        with self.assertRaises(ValueError):i.control(dict(op='step',inputs=[NEUTRAL]))
        i.control(dict(op='clear'));self.assertEqual(i.rows,[])
    def test_mini_unlock_native_word_and_negative_controls(self):
        c=object.__new__(NativeCore);c.region='japan';c.core_version=0x020600;c.debugger=False
        ram=(C.c_uint32*(0x400000//4))();c.rdram_pointer=lambda n:C.addressof(ram)
        idx=(0x80161EE0-0x80000000)//4
        ram[idx-1]=0xdeadbeef;ram[idx+1]=0x12345678
        self.assertEqual(c.unlock_mini_ebisumaru(),dict(before=0,after=1,changed=True))
        self.assertEqual(list(ram[idx-1:idx+2]),[0xdeadbeef,1,0x12345678])
        self.assertFalse(c.unlock_mini_ebisumaru()['changed'])
        ram[idx]=0x100;self.assertRaises(RuntimeError,c.unlock_mini_ebisumaru);self.assertEqual(ram[idx],0x100)
        ram[idx]=0;c.region='usa';self.assertRaises(RuntimeError,c.unlock_mini_ebisumaru);self.assertEqual(ram[idx],0)
        c.region='japan';c.core_version=0x020500;self.assertRaises(RuntimeError,c.unlock_mini_ebisumaru)
        c.core_version=0x020600;c.rdram_pointer=lambda n:None;self.assertRaises(RuntimeError,c.unlock_mini_ebisumaru)
        c.rdram_pointer=lambda n:C.addressof(ram)
        with patch('practice.mupen_native.guest_address',side_effect=[0x80161EE7,0x80161EE4]):
            self.assertRaises(RuntimeError,c.unlock_mini_ebisumaru)
        self.assertEqual(ram[idx],0);self.assertEqual(ram[idx+1],0x12345678)
    def test_mini_unlock_requires_paused_confirmed_empty_trace_and_callback(self):
        i=self.setup_inspector();i.core.core_version=0x020600;calls=[]
        def grant():
            calls.append((i.state,i.serial,i.input));return dict(before=0,after=1,changed=True)
        i.core.unlock_mini_ebisumaru=grant
        self.assertTrue(i.report()['capabilities']['mini_unlock'])
        with self.assertRaises(RuntimeError):i.control(dict(op='unlock_mini'))
        cmd=dict(op='unlock_mini',confirm=True)
        i.control(dict(op='resume'))
        with self.assertRaises(RuntimeError):i.control(cmd)
        i.control(dict(op='pause'));i.control(dict(op='record'))
        with self.assertRaises(RuntimeError):i.control(cmd)
        i.control(dict(op='record'));i.control(dict(op='step',inputs=[NEUTRAL]))
        with self.assertRaises(RuntimeError):i.control(cmd)
        self.assertEqual(calls,[]);i.control(dict(op='clear'))
        before=i.serial;r=i.control(cmd)
        self.assertEqual(calls,[(RUNNING,before+1,NEUTRAL)])
        self.assertEqual(r['state'],PAUSED);self.assertEqual(r['rows'],[])
        self.assertTrue(r['mini_unlock']['changed']);self.assertFalse(r['capabilities']['ram_writes'])
        i.region='usa'
        with self.assertRaises(RuntimeError):i.control(cmd)
        self.assertEqual(len(calls),1)
    def test_mini_unlock_failure_disarms_request(self):
        i=self.setup_inspector();i.core.core_version=0x020600
        def fail():raise RuntimeError('grant rejected')
        i.core.unlock_mini_ebisumaru=fail
        with self.assertRaisesRegex(RuntimeError,'grant rejected'):i.control(dict(op='unlock_mini',confirm=True))
        self.assertFalse(i.unlock_pending);self.assertIsNone(i.unlock_result);self.assertEqual(i.state,PAUSED)

    def test_zero_polls_visible_not_fabricated(self):
        i=self.setup_inspector();i.core.no_polls=True;r=i.control(dict(op='step',inputs=[NEUTRAL]))
        self.assertEqual(r['rows'][0]['polls'],0)
    def test_raw_core_words_native_endian(self):
        c=object.__new__(NativeCore);c.debugger=False
        buf=(C.c_uint32*2)(0x12345678,0x3f333333);c.rdram_pointer=lambda n:C.addressof(buf)
        for kind,offset,want in [('u8',1,0x34),('u16',2,0x5678),('u32',0,0x12345678)]:
            self.assertEqual(c.read_watch(dict(kind=kind,address=0x80000000+offset)),want)
        self.assertAlmostEqual(c.read_watch(dict(kind='f32',address=0x80000004)),.7,places=6)
        c.rdram_pointer=lambda n:None;self.assertIsNone(c.read_watch(dict(kind='u32',address=0x80000000)))
    def test_debugger_reads_must_be_ram_and_readable(self):
        c=object.__new__(NativeCore);c.debugger=True;c.readers={4:lambda addr:0x12345678}
        c.mem_info=lambda typ,addr:2 if typ==1 else 1
        self.assertEqual(c.read_watch(dict(kind='u32',address=0x80000000)),0x12345678)
        c.mem_info=lambda typ,addr:0
        self.assertIsNone(c.read_watch(dict(kind='u32',address=0x80000000)))

    @unittest.skipUnless(shutil.which('cc') and sys.platform in ('linux','darwin'),'C11 compiler / POSIX required')
    def test_scripted_input_plugin_with_abi_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            lib=Path(d)/('input.dylib' if sys.platform=='darwin' else 'input.so')
            supplied=os.environ.get('GOEMON_NATIVE_INPUT_LIBRARY')
            if supplied: lib=Path(supplied).resolve()
            else:
                subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',*(['-dynamiclib'] if sys.platform=='darwin' else ['-shared','-fPIC']),'-I',str(ROOT/'tests/fixtures/mupen_native'),str(ROOT/'native/goemon_mupen_input.c'),'-o',str(lib)],check=True)
            p=C.CDLL(str(lib));p.PluginStartup.argtypes=[C.c_void_p]*3;p.GoemonSetInput.argtypes=[C.c_uint,C.c_int,C.c_int]
            p.GetKeys.argtypes=[C.c_int,C.POINTER(C.c_uint32)];p.GoemonTakePolls.restype=C.c_uint32
            self.assertEqual(p.PluginStartup(None,None,None),0)
            self.assertEqual(p.GoemonSetInput(0x8008,-80,80),1)
            keys=C.c_uint32();p.GetKeys(0,C.byref(keys))
            self.assertEqual(keys.value,0x50B00880);self.assertEqual(p.GoemonTakePolls(),1);self.assertEqual(p.GoemonTakePolls(),0)
            p.GetKeys(1,C.byref(keys));self.assertEqual(keys.value,0);self.assertEqual(p.GoemonTakePolls(),0)
            self.assertEqual(p.GoemonSetInput(0xC0,0,0),0);self.assertEqual(p.GoemonSetInput(0,81,0),0)
            p.RomClosed();p.GetKeys(0,C.byref(keys));self.assertEqual(keys.value,0)
            self.assertEqual(p.PluginShutdown(),0)

if __name__=='__main__':unittest.main()

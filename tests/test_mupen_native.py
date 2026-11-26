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
    def test_physical_play_then_exclusive_scripted_step(self):
        i=self.setup_inspector(); i.core.physical_available=True
        with patch.object(i.core,'use_physical',return_value=True,create=True) as physical:
            r=i.control(dict(op='physical'))
            self.assertEqual(r['state'],RUNNING);self.assertEqual(r['input_mode'],'physical')
            self.assertTrue(r['capabilities']['physical_input']);physical.assert_called_once()
            i.frame(10);self.assertIsNone(i.last['buttons']);self.assertEqual(i.rows,[])
            with self.assertRaisesRegex(RuntimeError,'scripted'):i.control(dict(op='record'))
            i.control(dict(op='pause'))
            r=i.control(dict(op='step',inputs=[dict(NEUTRAL,x=80),NEUTRAL]))
            self.assertEqual(r['input_mode'],'scripted');self.assertEqual(r['state'],PAUSED)
            self.assertEqual([x['x'] for x in r['rows']],[80,0]);self.assertEqual(i.core.input,NEUTRAL)
            i.control(dict(op='record'))
            with self.assertRaisesRegex(RuntimeError,'recording'):i.control(dict(op='physical'))
        i.control(dict(op='record'));i.core.physical_available=False
        with self.assertRaisesRegex(RuntimeError,'unavailable'):i.control(dict(op='physical'))

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
                subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',*(['-dynamiclib'] if sys.platform=='darwin' else ['-shared','-fPIC']),'-I',str(ROOT/'tests/fixtures/mupen_native'),str(ROOT/'native/goemon_mupen_input.c'),'-o',str(lib),*(['-ldl'] if sys.platform=='linux' else [])],check=True)
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

    def test_stock_provider_passthrough_and_script_override(self):
        if sys.platform not in ('linux','darwin') or not shutil.which('cc'):
            self.skipTest('requires native C compiler')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);suffix='.dylib' if sys.platform=='darwin' else '.so'
            fixture=p/'provider.c';provider=p/('provider'+suffix);lib=p/('bridge'+suffix)
            fixture.write_text(r'''#include <m64p_plugin.h>
static int keys_down;
EXPORT m64p_error CALL PluginGetVersion(m64p_plugin_type *kind,int *v,int *api,const char **n,int *c) {
    (void)v;(void)n;(void)c;*kind=M64PLUGIN_INPUT;*api=0x020100;return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginStartup(m64p_dynlib_handle c,void *x,void (*l)(void*,int,const char*)) {
    (void)c;(void)x;(void)l;keys_down=0;return M64ERR_SUCCESS;
}
EXPORT m64p_error CALL PluginShutdown(void){return M64ERR_SUCCESS;}
EXPORT void CALL InitiateControllers(CONTROL_INFO i){(void)i;}
EXPORT void CALL GetKeys(int i,BUTTONS *k){(void)i;k->Value=0;k->X_AXIS=-42;k->Y_AXIS=31;k->A_BUTTON=!!keys_down;}
EXPORT int CALL RomOpen(void){return 1;}
EXPORT void CALL RomClosed(void){}
EXPORT void CALL SDL_KeyDown(int m,int k){(void)m;(void)k;keys_down=1;}
EXPORT void CALL SDL_KeyUp(int m,int k){(void)m;(void)k;keys_down=0;}
''')
            flags=['-dynamiclib'] if sys.platform=='darwin' else ['-shared','-fPIC']
            cmd=['cc','-std=c11','-Wall','-Wextra','-Werror',*flags,'-I',str(ROOT/'tests/fixtures/mupen_native')]
            subprocess.run([*cmd,str(fixture),'-o',str(provider)],check=True)
            supplied=os.environ.get('GOEMON_NATIVE_INPUT_LIBRARY')
            if supplied:lib=Path(supplied).resolve()
            else:subprocess.run([*cmd,str(ROOT/'native/goemon_mupen_input.c'),'-o',str(lib),*(['-ldl'] if sys.platform=='linux' else [])],check=True)
            bridge=C.CDLL(str(lib));bridge.GoemonConfigurePhysical.argtypes=[C.c_char_p]
            bridge.PluginStartup.argtypes=[C.c_void_p]*3;bridge.GetKeys.argtypes=[C.c_int,C.POINTER(C.c_uint32)]
            bridge.GoemonSetInput.argtypes=[C.c_uint,C.c_int,C.c_int]
            self.assertEqual(bridge.GoemonConfigurePhysical(os.fsencode(lib)),0)
            self.assertEqual(bridge.GoemonConfigurePhysical(os.fsencode(provider)),1)
            self.assertEqual(bridge.PluginStartup(None,None,None),0)
            try:
                self.assertEqual(bridge.RomOpen(),1);self.assertEqual(bridge.GoemonUsePhysical(),1)
                k=C.c_uint32();bridge.SDL_KeyDown(0,0);bridge.GetKeys(0,C.byref(k))
                self.assertEqual(k.value,0x1FD60080);self.assertEqual(bridge.GoemonTakePolls(),1)
                bridge.SDL_KeyUp(0,0);bridge.GetKeys(0,C.byref(k));self.assertEqual(k.value,0x1FD60000)
                self.assertEqual(bridge.GoemonSetInput(8,80,-80),1)
                bridge.GetKeys(0,C.byref(k));self.assertEqual(k.value,0xB0500800)
                bridge.GetKeys(1,C.byref(k));self.assertEqual(k.value,0)
                self.assertEqual(bridge.GoemonUsePhysical(),1);bridge.GetKeys(0,C.byref(k));self.assertEqual(k.value,0x1FD60000)
                bridge.RomClosed()
            finally:self.assertEqual(bridge.PluginShutdown(),0)

class NativeInputBuildTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform in ('linux','darwin'), 'native source build only')
    def test_missing_current_stale_and_failed_build(self):
        if not shutil.which('cc') or not shutil.which('bash'):
            self.skipTest('requires native C compiler and bash')
        from practice.mupen_input_build import default_input_path
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'scripts').mkdir();(root/'native').mkdir()
            for rel in ('scripts/build_mupen_input.sh','native/goemon_mupen_input.c'):
                shutil.copyfile(ROOT/rel,root/rel)
            sdk=str(ROOT/'tests/fixtures/mupen_native')
            cmd=['bash','scripts/build_mupen_input.sh','--if-needed',sdk]
            out=default_input_path(root)
            env=dict(os.environ,CC='cc')
            run=lambda e:subprocess.run(cmd,cwd=root,env=e,capture_output=True,text=True,timeout=30)
            self.assertFalse(out.exists())
            first=run(env);self.assertEqual(first.returncode,0,first.stderr)
            self.assertTrue(out.is_file());original=out.read_bytes()
            # Cached build skips even a deliberately failing compiler.
            current=run(dict(env,CC='false'));self.assertEqual(current.returncode,0,current.stderr)
            self.assertIn('Current',current.stdout)
            with (root/'native/goemon_mupen_input.c').open('a') as f:f.write('\n/* changed source */\n')
            failed=run(dict(env,CC='false'));self.assertNotEqual(failed.returncode,0)
            self.assertEqual(out.read_bytes(),original)
            rebuilt=run(env);self.assertEqual(rebuilt.returncode,0,rebuilt.stderr);self.assertIn('Built',rebuilt.stdout)
            out.unlink();self.assertEqual(run(env).returncode,0)

    def test_background_request_is_shared_and_failure_retry_is_explicit(self):
        from practice import mupen_input_build as b
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'plugin.so';out.touch()
            with patch.object(b,'_future',None),patch.object(b,'build_default_input',side_effect=[RuntimeError('SDK missing'),out]) as build:
                f=b.request_input_build()
                with self.assertRaisesRegex(RuntimeError,'SDK missing'):f.result(timeout=5)
                self.assertIs(f,b.request_input_build());self.assertEqual(build.call_count,1)
                g=b.request_input_build(retry=True);self.assertEqual(g.result(timeout=5),out)
                self.assertIs(g,b.request_input_build());self.assertEqual(build.call_count,2)


@unittest.skipUnless(sys.platform=='linux','Linux managed child memory')
class ManagedNativeRamTests(unittest.TestCase):
    def test_toolkit_manual_writer_and_freeze_guards(self):
        from types import SimpleNamespace
        from practice.managed_native_ram import ManagedNativeRam
        from practice.toolkit import Toolkit
        from practice.value_freezes_ui import ValueFreezesMixin
        managed=object.__new__(ManagedNativeRam);managed.owner=object()
        sentinel=object()
        ui=SimpleNamespace(process=managed.owner,manual_edits_paused=lambda:False)
        screen=SimpleNamespace(process=managed,native_frame_ui=ui,active_version=SimpleNamespace(key='japan'),
                               jp_rdram=SimpleNamespace(process=managed),game_pid=123,jp_backend='mupen64plus',
                               _connecting=False,args=SimpleNamespace(read_only=False,enable_hex_edit=True),freeze_token=lambda:'token')
        with patch.object(managed,'writer',return_value=sentinel) as writer:
            with self.assertRaisesRegex(RuntimeError,'Pause native inspector'):Toolkit._open_japan_manual_writer(screen)
            writer.assert_not_called();ui.manual_edits_paused=lambda:True
            self.assertIs(Toolkit._open_japan_manual_writer(screen),sentinel)
            writer.assert_called_once();ui.process=object()
            with self.assertRaisesRegex(RuntimeError,'Pause native inspector'):Toolkit._open_japan_manual_writer(screen)
        with self.assertRaisesRegex(PermissionError,'Continuous freezes'):
            ValueFreezesMixin.require_freeze_access(screen,raw=True)
        self.assertFalse(ValueFreezesMixin._freeze_worker_connection(screen)[2])

    def test_owned_child_probe_edit_bounds_and_exit(self):
        from practice.managed_native_ram import connect_managed_japan, ManagedNativeRam, SIZE
        # Synthetic buffer owned by this test process; no emulator or ROM.
        child_code="""import ctypes as C,sys
ram=(C.c_uint32*(0x400000//4))()
for off in (0x450,0x600,0x2400,0x3000):ram[off//4]=0x11223344
print(C.addressof(ram),flush=True)
sys.stdin.readline()
"""
        child=subprocess.Popen([sys.executable,'-c',child_code],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
        host=None
        try:
            base=int(child.stdout.readline())
            probes=tuple((off,bytes.fromhex('11223344')) for off in (0x450,0x600,0x2400))
            with patch('practice.managed_native_ram.verified_japan_probes',return_value=probes):
                try:host,reader,endian=connect_managed_japan(child,base,'synthetic')
                except PermissionError as exc:self.skipTest(f'owned-child procfs denied: {exc}')
                self.assertEqual(reader.rdram_size,SIZE)
                self.assertEqual(reader.read_guest(0x80003000,4),bytes.fromhex('11223344'))
                with self.assertRaises(PermissionError):host.write(base,b'\x00')
                with self.assertRaises(OSError):host.read(base-1,1)
                with self.assertRaises(OSError):host.read(base+SIZE,1)
                with self.assertRaises(ValueError):connect_managed_japan(child,base+16,'synthetic')
                writer=host.writer()
                try:
                    from practice.backends.memory import Rdram
                    view=Rdram(writer,base,endian);view.rdram_size=SIZE
                    view.write_guest(0x80003001,b'\x99')
                    self.assertEqual(reader.read_guest(0x80003000,4),bytes.fromhex('11993344'))
                    with self.assertRaises(OSError):writer.write(base+SIZE,b'\x00')
                finally:writer.close()
            child.stdin.close();child.wait(timeout=5)
            with self.assertRaises(OSError):host.read(base,4)
            with self.assertRaises(OSError):host.writer()
        finally:
            if host:host.close()
            if not child.stdin.closed:child.stdin.close()
            if child.poll() is None:child.kill();child.wait(timeout=5)
            child.stdout.close()


if __name__=='__main__':unittest.main()

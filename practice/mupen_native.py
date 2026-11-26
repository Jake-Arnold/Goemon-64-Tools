"""Experimental native Mupen64Plus research frontend (managed child session).

Core execution stays on the process main thread for SDL/macOS. Only the
public core API and a purpose-built P1 input plugin are used. A core frame
callback is NOT a Goemon logic-update callback.
"""
from __future__ import annotations
import argparse
import ctypes as C
import csv
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import threading
import time

from practice.address_registry import guest_address
from practice.game_versions import identify_rom
from practice.entrances import canonical_rom
from practice.pj64_frame_control import controller_input, parse_inputs
from practice.native_trace_wire import PREFIX, TraceWriter, private_stdout, checkpoint
from practice.native_state_control import SET_SLOT, LOAD_COMPLETE, run_state_job, state_complete

_wire = None
_emit_lock = threading.Lock()
STOPPED, RUNNING, PAUSED = 1, 2, 3
ROM_OPEN, ROM_CLOSE, EXECUTE, STOP, PAUSE, RESUME, QUERY = 1, 2, 5, 6, 7, 8, 9
FRAME_CALLBACK, ADVANCE = 15, 20
WIDTHS = {'u8': 1, 's8': 1, 'u16': 2, 's16': 2, 'u32': 4, 's32': 4, 'f32': 4}
MAX_WATCHES = 24
MAX_POINTER_HOPS = 4
MAX_NATIVE_STEPS = 600
MAX_TRACE_ROWS = 3600
# Original Japan-0 task registration and scheduler evidence (PR #272).
JP_PRE, JP_POST = 0x801D0F54, 0x801D1228
GUEST_BASE, RAM_SIZE = 0x80000000, 0x400000

def ram_address(address, width):
    return width in (1,2,4) and type(address) is int and 0x80000000 <= address <= 0x80400000-width and address % width == 0
NEUTRAL = {'buttons': 0, 'x': 0, 'y': 0}
DebugCB = C.CFUNCTYPE(None, C.c_void_p, C.c_int, C.c_char_p)
StateCB = C.CFUNCTYPE(None, C.c_void_p, C.c_int, C.c_int)
FrameCB = C.CFUNCTYPE(None, C.c_uint)


def checked(code, operation):
    if code:
        raise RuntimeError(f'{operation}: Mupen64Plus error {code}')


def bind(lib, name, result, *args):
    f = getattr(lib, name)
    f.restype, f.argtypes = result, list(args)
    return f


def parse_watches(text, region):
    """Fixed addresses or explicit guest-only pointer chains: root->offset->offset."""
    if not isinstance(text, str) or len(text) > 8192:
        raise ValueError('Watch definitions must be text (maximum 8192 characters)')
    result = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        fields = line.split()
        if len(fields) != 3:
            raise ValueError('Expected name type address or root->hex_offset')
        name, kind, raw = fields
        if (not re.fullmatch('[A-Za-z][A-Za-z0-9_]{0,23}', name)
                or name in ('frame', 'serial', 'polls', 'buttons', 'x', 'y')
                or kind not in WIDTHS or len(result) >= MAX_WATCHES or any(w['name']==name for w in result)):
            raise ValueError('Expected up to 24 unique watches: name u8/s8/u16/s16/u32/s32/f32 address')
        root, *hops = raw.split('->')
        if len(hops) > MAX_POINTER_HOPS:
            raise ValueError('Pointer chain exceeds four dereferences')
        width = 4 if hops else WIDTHS[kind]
        if root.startswith('@'):
            try: address = guest_address(root[1:], region=region, width=width)
            except KeyError as exc: raise ValueError(str(exc)) from exc
        else:
            if not re.fullmatch(r'(?:0[xX])?[0-9a-fA-F]{1,8}',root):
                raise ValueError('Expected hexadecimal guest address')
            address = int(root, 16)
        if not ram_address(address, width):
            raise ValueError('Watch root must be aligned within the first 4 MiB of guest RAM')
        watch = dict(name=name, kind=kind, address=address)
        if hops:
            if any(not re.fullmatch(r'(?:0[xX])?[0-9a-fA-F]{1,6}', h) for h in hops):
                raise ValueError('Pointer offsets must be nonnegative hexadecimal values')
            offsets = [int(h,16) for h in hops]
            if any(offset >= 0x400000 for offset in offsets):
                raise ValueError('Pointer offset outside the first 4 MiB')
            watch['offsets'] = offsets
        result.append(watch)
    return result


def valid_input(value):
    if not isinstance(value, dict) or set(value) != {'buttons', 'x', 'y'}:
        raise ValueError('Invalid input fields')
    b,x,y = (value[k] for k in ('buttons','x','y'))
    if any(type(v) is not int for v in (b,x,y)) or not 0<=b<=65535 or b&0xc0 or not -80<=x<=80 or not -80<=y<=80:
        raise ValueError('Invalid N64 controller input')
    return dict(value)


def write_trace(path, report):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        columns = ['serial','frame','polls','buttons','x','y'] + [w['name'] for w in report['watches']]
        with path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['region','boundary']+columns)
            writer.writeheader()
            for row in report['rows']:
                writer.writerow(dict(region=report['region'], boundary=report['boundary'], **row))
    else:
        path.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


def locate_japan_player(snapshot):
    """Find a unique callback-pair candidate, not a permanent player identity."""
    if len(snapshot)!=RAM_SIZE:
        raise ValueError('Expected complete 4 MiB native RDRAM snapshot')
    word=struct.Struct('=I')
    needle=word.pack(JP_PRE)
    candidates=[]; start=0
    while True:
        hit=snapshot.find(needle,start)
        if hit<0: break
        start=hit+1; off=hit-8
        if off<0 or off%4 or off+0xEC>RAM_SIZE: continue
        def u32(rel): return word.unpack_from(snapshot,off+rel)[0]
        if u32(0x10)!=JP_POST: continue
        if not all(ram_address(u32(rel),4) for rel in (0x0C,0x18,0x5C)): continue
        if not ram_address(u32(0x18)+0x10,4) or not ram_address(u32(0x5C)+0x86,2): continue
        if u32(0x60)>>24 not in range(4): continue
        candidates.append(GUEST_BASE+off)
    if len(candidates)!=1:
        detail=', '.join(f'0x{x:08X}' for x in candidates[:8])
        raise RuntimeError(f'Player locator: {len(candidates)} structural candidates'+(f' ({detail})' if detail else '')+'; enter normal gameplay and retry')
    return candidates[0]


def player_watch_text(base):
    # Controller fields use existing region-specific registry entries.
    controller=[f'{name} {kind} @research:controller_japan_{name}' for name,kind in (
        ('raw_x','s16'),('raw_y','s16'),('magnitude','f32'),('held','u16'),('pressed','u16'),('combined_magnitude','f32'))]
    fields=(('pre_callback','u32',8,''),('action_callback','u32',0xC,''),('post_callback','u32',0x10,''),
        ('action_byte0','u8',0xCC,''),('action_byte1','u8',0xCD,''),('character','u8',0x60,''),
        ('context','u32',0x5C,''),('miniature','u16',0x5C,'->86'),('history0','f32',0x5C,'->20'),
        ('history1','f32',0x5C,'->24'),('history2','f32',0x5C,'->28'),('movement_e4','f32',0xE4,''),
        ('movement_e8','f32',0xE8,''),('position_x','f32',0x18,'->08'),('position_y','f32',0x18,'->0C'),
        ('position_z','f32',0x18,'->10'))
    return '\n'.join(controller+[f'{name} {kind} {base+off:08X}{suffix}' for name,kind,off,suffix in fields])


class NativeCore:
    """One isolated native session. Calls validated against the public 2.x API."""
    def __init__(self, args, on_state, on_frame, data=None, on_state_job=None):
        if data is None: data = Path(args.rom).read_bytes()
        self.region = identify_rom(data).key
        self.rom = C.create_string_buffer(canonical_rom(data))
        self.core = C.CDLL(str(Path(args.core).resolve()), mode=getattr(C, 'RTLD_GLOBAL', 0))
        self.plugins = []
        self.physical_available = False
        self.started = self.opened = False
        self.log = DebugCB(lambda ctx, level, msg: print(msg.decode('utf-8', 'replace'), file=sys.stderr) if msg else None)
        def state_callback(ctx, param, value):
            if param == 1: on_state(value)
            elif param in (10, 11) and on_state_job is not None: on_state_job(param, value)
        self.state_cb = StateCB(state_callback)
        self.frame_cb = FrameCB(on_frame)
        self.command = bind(self.core, 'CoreDoCommand', C.c_int, C.c_int, C.c_int, C.c_void_p)
        try:
            kind, version, api, caps = (C.c_int() for _ in range(4))
            name = C.c_char_p()
            getversion = bind(self.core, 'PluginGetVersion', C.c_int, *([C.POINTER(C.c_int)]*3), C.POINTER(C.c_char_p), C.POINTER(C.c_int))
            checked(getversion(C.byref(kind), C.byref(version), C.byref(api), C.byref(name), C.byref(caps)), 'Core version')
            if kind.value != 5 or api.value >> 16 != 2:
                raise RuntimeError('Expected a Mupen64Plus 2.x core library')
            self.debugger = bool(caps.value & 2)
            self.core_version = version.value
            if not self.debugger and version.value != 0x020600:
                raise RuntimeError('For non-debug builds, the native RDRAM layout is verified for core 2.6.0 only')
            # Keep all changes and save data in a dedicated research directory.
            config = Path(args.config).expanduser().resolve() / 'goemon-native-session'; config.mkdir(parents=True, exist_ok=True)
            saves = config / 'research-saves'; saves.mkdir(exist_ok=True)
            startup = bind(self.core,'CoreStartup',C.c_int,C.c_int,C.c_char_p,C.c_char_p,C.c_void_p,DebugCB,C.c_void_p,StateCB)
            checked(startup(0x020001, os.fsencode(config), os.fsencode(Path(args.data).resolve()), None,self.log,None,self.state_cb),'CoreStartup')
            self.started = True
            section = C.c_void_p()
            checked(bind(self.core,'ConfigOpenSection',C.c_int,C.c_char_p,C.POINTER(C.c_void_p))(b'Core',C.byref(section)), 'Core config')
            set_param = bind(self.core,'ConfigSetParameter',C.c_int,C.c_void_p,C.c_char_p,C.c_int,C.c_void_p)
            for key,val in ((b'R4300Emulator',0),(b'EnableDebugger',0),(b'RandomizeInterrupt',0)):
                checked(set_param(section,key,1 if key==b'R4300Emulator' else 3,C.byref(C.c_int(val))),key.decode())
            for key in (b'SaveStatePath',b'SaveSRAMPath'):
                checked(set_param(section,key,4,C.c_char_p(os.fsencode(saves))),key.decode())
            # Keep paused-edit and frame-step boundaries owned by the inspector.
            # In this isolated config only, disable stock hotkeys that could
            # resume, advance, reset or load state behind the parent's back.
            events = C.c_void_p()
            checked(bind(self.core,'ConfigOpenSection',C.c_int,C.c_char_p,C.POINTER(C.c_void_p))(b'CoreEvents',C.byref(events)), 'Core events config')
            for name in (b'Pause', b'Frame Advance', b'Save State', b'Load State', b'Reset', b'Speed Limiter Toggle'):
                key=b'Kbd Mapping '+name
                checked(set_param(events,key,1,C.byref(C.c_int(0))),key.decode())
            for name in (b'Pause', b'Frame Advance', b'Save State', b'Load State', b'Reset'):
                key=b'Joy Mapping '+name
                checked(set_param(events,key,4,C.c_char_p(b'')),key.decode())
            checked(self.command(ROM_OPEN,len(data),C.cast(self.rom,C.c_void_p)), 'ROM_OPEN'); self.opened=True
            for kind,path in ((2,args.gfx),(3,args.audio),(4,args.input),(1,args.rsp)):
                lib = C.CDLL(str(Path(path).resolve()))
                plugtype,pv,pa,pc = (C.c_int() for _ in range(4)); pn=C.c_char_p()
                getver=bind(lib,'PluginGetVersion',C.c_int,*([C.POINTER(C.c_int)]*3),C.POINTER(C.c_char_p),C.POINTER(C.c_int))
                checked(getver(C.byref(plugtype),C.byref(pv),C.byref(pa),C.byref(pn),C.byref(pc)),'PluginGetVersion')
                if plugtype.value != kind or pa.value>>16!=2: raise RuntimeError(f'Wrong plugin type/API: {path}')
                if kind==4:
                    if pa.value != 0x020100: raise RuntimeError('Expected Goemon input plugin API 2.1.0')
                    self.set_input=bind(lib,'GoemonSetInput',C.c_int,C.c_uint,C.c_int,C.c_int)
                    self.polls=bind(lib,'GoemonTakePolls',C.c_uint)
                    physical=getattr(args,'physical_input','')
                    if physical:
                        if not hasattr(lib,'GoemonConfigurePhysical'):
                            raise RuntimeError('Rebuild Goemon input plugin with scripts/build_mupen_input.sh')
                        configure=bind(lib,'GoemonConfigurePhysical',C.c_int,C.c_char_p)
                        self.use_physical=bind(lib,'GoemonUsePhysical',C.c_int)
                        if not configure(os.fsencode(Path(physical).resolve())):
                            raise RuntimeError('Could not load compatible SDL input provider; check setup or leave physical input blank')
                        self.physical_available=True
                start=bind(lib,'PluginStartup',C.c_int,C.c_void_p,C.c_void_p,DebugCB)
                checked(start(self.core._handle,None,self.log),'PluginStartup')
                self.plugins.append((kind,lib,False))
                checked(bind(self.core,'CoreAttachPlugin',C.c_int,C.c_int,C.c_void_p)(kind,lib._handle),'CoreAttachPlugin')
                self.plugins[-1]=(kind,lib,True)
            if self.debugger:
                self.readers = {n:bind(self.core,f'DebugMemRead{n*8}',t,C.c_uint) for n,t in ((1,C.c_uint8),(2,C.c_uint16),(4,C.c_uint32))}
                self.mem_info=bind(self.core,'DebugMemGetMemInfo',C.c_int,C.c_int,C.c_uint)
            if self.core_version == 0x020600:
                self.rdram_pointer=bind(self.core,'DebugMemGetPointer',C.c_void_p,C.c_int)
            checked(self.command(FRAME_CALLBACK,0,C.cast(self.frame_cb,C.c_void_p)),'Set frame callback')
        except BaseException:
            self.close(); raise

    def cmd(self, op):
        checked(self.command(op,0,None), f'Core command {op}')

    def queue_state(self, op, slot):
        checked(self.command(SET_SLOT,slot,None),'Set savestate slot')
        self.cmd(op)

    def read_word(self, addr, width):
        self.read_error = ''
        if not ram_address(addr,width):
            self.read_error = f'Invalid or unaligned guest address {addr!r} (width {width})'
            return None
        # Both debugger and non-debugger builds of 2.6.0 expose the same
        # native word-array RDRAM API. Prefer it: debugger type/flag tables
        # need not be available when EnableDebugger is disabled.
        if getattr(self,'core_version',None)==0x020600 or not self.debugger:
            base=self.rdram_pointer(1)
            if not base or base%4:
                self.read_error = 'Core RDRAM pointer unavailable or unaligned'
                return None
            off=addr-GUEST_BASE
            word=C.c_uint32.from_address(base+(off&~3)).value
            return (word>>((4-width-off%4)*8))&((1<<(8*width))-1)
        memtype, flags = self.mem_info(1,addr), self.mem_info(2,addr)
        if memtype!=2 or not flags&1:
            self.read_error = f'Debugger rejected 0x{addr:08X}: type={memtype}, flags=0x{flags:X}'
            return None
        return self.readers[width](addr)

    def locate_japan_player(self):
        """Only while paused: snapshot this core's first 4 MiB; no external PID access."""
        if self.region!='japan' or self.core_version!=0x020600:
            raise RuntimeError('Locate Player requires Japan-0 and core 2.6.0')
        base=self.rdram_pointer(1)
        if not base or base%4:
            raise RuntimeError('Core RDRAM pointer unavailable or unaligned')
        return locate_japan_player(C.string_at(base,RAM_SIZE))

    def unlock_mini_ebisumaru(self):
        """One explicit Japan-0 grant, on the emulator callback thread only.

        Existing unlock byte and original script grant agree. Never expose a
        general write API; require the reviewed original word and a binary
        value. This does not set the active miniature form or story bits.
        """
        if self.region != 'japan' or self.core_version != 0x020600:
            raise RuntimeError('Mini Ebisumaru unlock requires Japan-0 and core 2.6.0')
        byte = guest_address('crosswalk:japan:unlock:mini_ebisumaru',region='japan',width=1)
        word = guest_address('research:dialogue_grant_mini_ebisu_jp',region='japan',width=4)
        # Pinned review boundary: a catalogue refresh cannot relocate a writer.
        if word != 0x80161EE0 or byte != word+3 or not ram_address(word,4):
            raise RuntimeError('Mini Ebisumaru catalogue no longer matches reviewed grant')
        before=self.read_word(word,4)
        if before not in (0,1):
            raise RuntimeError(f'Unexpected miniature ability word: {before!r}; no write')
        base=self.rdram_pointer(1)
        if not base or base%4:
            raise RuntimeError('Native RDRAM unavailable; no write')
        cell=C.c_uint32.from_address(base+word-0x80000000)
        if cell.value != before:
            raise RuntimeError('Native grant word disagrees with readback; no write')
        if before == 0:
            cell.value=1
        if self.read_word(word,4)!=1 or cell.value!=1:
            raise RuntimeError('Mini Ebisumaru grant readback failed')
        return dict(before=before,after=1,changed=before==0)

    def read_watch(self,w):
        addr=w['address']; width=WIDTHS[w['kind']]
        for offset in w.get('offsets', ()):
            pointer=self.read_word(addr,4)
            # Do not interpret null, host, KSEG1, MMIO, unaligned or stale
            # out-of-range pointers as valid guest memory. No wrapping.
            if not ram_address(pointer,4):
                self.read_error = getattr(self,'read_error','') or f'Invalid guest pointer {pointer!r} at 0x{addr:08X}'
                return None
            addr=pointer+offset
        v=self.read_word(addr,width)
        if v is None: return None
        if w['kind']=='f32':
            f=struct.unpack('>f',v.to_bytes(4,'big'))[0]
            return f if math.isfinite(f) else f'bits:0x{v:08X}'
        if w['kind'].startswith('s') and v & (1<<(width*8-1)):
            return v-(1<<(width*8))
        return v

    def close(self):
        # Called only after EXECUTE returns, or during failed setup.
        for kind,lib,attached in reversed(self.plugins):
            if attached: self.core.CoreDetachPlugin(kind)
            lib.PluginShutdown()
        self.plugins.clear()
        if self.opened: self.command(ROM_CLOSE,0,None); self.opened=False
        if self.started: self.core.CoreShutdown(); self.started=False


class Inspector:
    """Frame callback recorder and bounded control; testable without a ROM/core."""
    def __init__(self, watches, region):
        self.cv=threading.Condition(); self.core=None; self.state=STOPPED
        self.serial=0; self.input=dict(NEUTRAL); self.watches=watches; self.region=region
        self.rows=[]; self.recording=False; self.stepping=False; self.error=''; self.last=None
        self.finished=False; self.operation=threading.Lock()
        self.physical_mode=False; self.managed_base=None
        self.watch_errors={}; self.player_base=None; self.player_text=None
        self.player_watches_suspended=False
        self.unlock_pending=False; self.unlock_result=None; self.unlock_error=None
        self.state_job_expected=None; self.state_job_result=None; self.state_job_notice=''

    def state_job_complete(self,parameter,value):
        state_complete(self,parameter,value)

    def state_changed(self,value):
        with self.cv: self.state=value; self.cv.notify_all()

    def frame(self,index):
        with self.cv:
            try:
                self.serial+=1
                # Load jobs can cross intermediate RAM states; never sample them.
                if self.state_job_expected == LOAD_COMPLETE:
                    self.cv.notify_all(); return
                if (self.managed_base is None and sys.platform == 'linux'
                        and getattr(self.core,'core_version',None)==0x020600
                        and hasattr(self.core,'rdram_pointer')):
                    base=self.core.rdram_pointer(1)
                    if base and base%16==0: self.managed_base=base
                if self.unlock_pending:
                    self.unlock_pending=False
                    try:
                        self.unlock_result=self.core.unlock_mini_ebisumaru()
                    except Exception as exc:
                        self.unlock_error=str(exc)
                row=dict(serial=self.serial,frame=index,polls=self.core.polls(),**(dict(buttons=None,x=None,y=None) if self.physical_mode else self.input))
                self.watch_errors={}
                valid_player=(self.player_base is None or
                    (not self.player_watches_suspended and self.core.read_word(self.player_base+8,4)==JP_PRE and self.core.read_word(self.player_base+0x10,4)==JP_POST))
                for w in self.watches:
                    name=w['name']
                    if not valid_player and self.player_base<=w['address']<self.player_base+0xEC:
                        row[name]=None; self.watch_errors[name]='Player signature changed; pause and locate again'
                    else:
                        row[name]=self.core.read_watch(w)
                        if row[name] is None:
                            self.watch_errors[name]=getattr(self.core,'read_error','') or 'Read unavailable'

                self.last=row
                if self.recording or self.stepping:
                    if len(self.rows)<MAX_TRACE_ROWS: self.rows.append(row)
                    else: self.recording=False; self.error='Trace limit reached; export and clear before continuing'
            except Exception as exc:
                self.error=f'Frame capture failed: {exc}'
            self.cv.notify_all()

    def wait(self,predicate,timeout=10):
        deadline=time.monotonic()+timeout
        with self.cv:
            while not predicate():
                if self.finished or time.monotonic()>=deadline:
                    raise RuntimeError('Core boundary timeout or emulator stopped')
                self.cv.wait(max(0,deadline-time.monotonic()))

    def set_input(self,value):
        value=valid_input(value)
        with self.cv:
            if not self.core.set_input(value['buttons'], value['x'], value['y']): raise RuntimeError('Input plugin rejected sample')
            self.input=value
            self.physical_mode=False

    def report(self):
        with self.cv:
            return dict(region=self.region,boundary='core-frame',input_semantics='last requested input; not proof of game consumption; physical samples not recorded',watches=self.watches,rows=list(self.rows),last=self.last,
                        state=self.state,serial=self.serial,recording=self.recording,error=self.error,
                        watch_errors=dict(self.watch_errors), player_base=self.player_base, player_text=self.player_text,
                        ram_reader='native 2.6.0 words' if getattr(self.core,'core_version',None)==0x020600 else 'debugger API',
                        mini_unlock=self.unlock_result, input_mode='physical' if self.physical_mode else 'scripted',
                        state_job_pending=self.state_job_expected is not None, state_job_notice=self.state_job_notice,
                        capabilities=dict(frame_advance=True,scripted_p1=True,physical_input=bool(getattr(self.core,'physical_available',False)),typed_reads=True,live_watches=True,pointer_watches=True,logic_updates=False,breakpoints=False,ram_writes=False,mini_unlock=self.region=='japan' and getattr(self.core,'core_version',None)==0x020600,savestate_control=getattr(self.core,'core_version',None)==0x020600,core_debugger=bool(getattr(self.core,'debugger',False))))

    def control(self,q, *, progress=None):
        op=q.get('op')
        if op=='status': return self.report()
        if self.finished: raise RuntimeError('Session closed')
        if self.state==STOPPED: raise RuntimeError('Emulator not running')
        if self.state_job_expected is not None and op!='stop':
            raise RuntimeError('Unacknowledged savestate job; stop and relaunch the session')
        self.state_job_notice=''
        if op in ('save_state','load_state'):
            run_state_job(self,op,q.get('slot'),q.get('confirm',False))
        elif op=='pause':
            if self.state!=PAUSED: self.core.cmd(PAUSE); self.wait(lambda:self.state==PAUSED)
        elif op=='resume':
            self.set_input(NEUTRAL); self.core.cmd(RESUME)
        elif op=='physical':
            with self.cv:
                if self.recording or self.stepping:
                    raise RuntimeError('Stop recording before switching to physical input')
                if not getattr(self.core,'physical_available',False) or not self.core.use_physical():
                    raise RuntimeError('Physical input unavailable: configure the stock SDL input plugin and rebuild the Goemon plugin')
                self.physical_mode=True; self.input=dict(NEUTRAL)
            if self.state==PAUSED: self.core.cmd(RESUME)
        elif op=='hold':
            self.set_input(q['input'])
        elif op=='watches':
            new=parse_watches(q.get('text'),self.region)
            with self.cv:
                if self.state!=PAUSED or self.recording or self.stepping:
                    raise RuntimeError('Pause and stop recording before applying watches')
                if new != self.watches:
                    if self.rows and q.get('replace_trace') is not True:
                        raise RuntimeError('Export and clear the old trace before changing watches')
                    # Schema and trace must change atomically. Reads happen only
                    # in the next core callback; never read RAM on the UI thread.
                    self.watches=new; self.rows=[]; self.last=None; self.error=''
                    self.watch_errors={}; self.player_base=None; self.player_text=None
                    self.player_watches_suspended=False
        elif op=='locate_player':
            with self.cv:
                if self.state!=PAUSED or self.recording or self.stepping:
                    raise RuntimeError('Pause and stop recording before locating the player')
                if self.rows and q.get('replace_trace') is not True:
                    raise RuntimeError('Export and clear the old trace before locating the player')
                base=self.core.locate_japan_player()
                text=player_watch_text(base)
                new=parse_watches(text,self.region)
                self.player_base=base; self.player_text=text
                self.player_watches_suspended=False
                self.watches=new; self.rows=[]; self.last=None; self.error=''; self.watch_errors={}
        elif op=='unlock_mini':
            if self.region!='japan' or getattr(self.core,'core_version',None)!=0x020600:
                raise RuntimeError('Mini Ebisumaru unlock requires Japan-0 and core 2.6.0')
            if q.get('confirm') is not True:
                raise RuntimeError('Explicit unlock confirmation required')
            with self.cv:
                if self.state!=PAUSED or self.recording or self.stepping or self.unlock_pending:
                    raise RuntimeError('Pause and stop recording before unlocking')
                if self.rows:
                    raise RuntimeError('Export and clear the trace before unlocking')
                self.unlock_result=None; self.unlock_error=None; self.error=''
                before=self.serial
                self.set_input(NEUTRAL); self.core.polls()
                self.unlock_pending=True
            try:
                # Native frame callback performs the write; never mutate RAM
                # from the UI/command thread while the core may still execute.
                self.core.cmd(ADVANCE)
                self.wait(lambda:self.serial>before and self.state==PAUSED and not self.unlock_pending)
                if self.unlock_error: raise RuntimeError(self.unlock_error)
                if self.serial!=before+1 or self.unlock_result is None or self.error:
                    raise RuntimeError('Unlock frame boundary/capture failed; inspect current ability before retrying')
            finally:
                with self.cv: self.unlock_pending=False
                if not self.finished and self.state==RUNNING:
                    try:self.core.cmd(PAUSE)
                    except RuntimeError:pass
        elif op=='record':
            with self.cv:
                if self.physical_mode: raise RuntimeError('Switch to scripted input before recording')
                self.recording=not self.recording
        elif op=='clear':
            with self.cv: self.rows=[]; self.error=''
        elif op=='step':
            inputs=q.get('inputs')
            if not isinstance(inputs,list) or not 1<=len(inputs)<=MAX_NATIVE_STEPS: raise ValueError(f'Expected 1..{MAX_NATIVE_STEPS} samples')
            inputs=[valid_input(v) for v in inputs]
            if self.state!=PAUSED: raise RuntimeError('Pause before stepping')
            with self.cv:
                if len(self.rows)+len(inputs)>MAX_TRACE_ROWS: raise ValueError('Trace limit; export and clear')
                self.stepping=True; self.error=''
            try:
                deadline=time.monotonic()+max(30,len(inputs)*0.5)
                last_progress=time.monotonic()
                for index,value in enumerate(inputs,1):
                    before=self.serial; self.set_input(value); self.core.polls()
                    self.core.cmd(ADVANCE)
                    self.wait(lambda:self.serial>before and self.state==PAUSED,timeout=min(10,max(0,deadline-time.monotonic())))
                    if self.serial!=before+1 or self.error: raise RuntimeError(self.error or 'Multiple core callbacks during single step')
                    now=time.monotonic()
                    if progress is not None and (index==1 or index==len(inputs) or now-last_progress>=0.5):
                        progress(index,len(inputs)); last_progress=now
            except Exception:
                if not self.finished and self.state==RUNNING:
                    try: self.core.cmd(PAUSE)
                    except RuntimeError: pass
                raise
            finally:
                with self.cv: self.stepping=False
                if not self.finished: self.set_input(NEUTRAL)
        elif op=='stop':
            self.set_input(NEUTRAL); self.core.cmd(STOP)
        else: raise ValueError('Unknown command')
        return self.report()


def emit(value):
    with _emit_lock:
        if _wire is not None: _wire.send(value)
        else: print(PREFIX+json.dumps(value,allow_nan=False),flush=True)


def worker(args):
    data=Path(args.rom).read_bytes()
    region=identify_rom(data).key
    inspector=Inspector(parse_watches(args.watches,region),region)
    core=NativeCore(args,inspector.state_changed,inspector.frame,data=data,on_state_job=inspector.state_job_complete); inspector.core=core
    recovery_path=Path(args.config).expanduser().resolve()/'goemon-native-session'/'research-traces'/f'trace-{os.getpid()}-{time.time_ns()}.json'
    saved_stamp=None; recovery_error=''
    def response(report, **fields):
        nonlocal saved_stamp,recovery_error
        report['recovery_path']=str(recovery_path)
        rows=report['rows']
        if rows:
            stamp=(len(rows),rows[0]['serial'],rows[-1]['serial'])
            if stamp!=saved_stamp:
                try:
                    checkpoint(recovery_path,report)
                    saved_stamp=stamp; recovery_error=''
                except (OSError,ValueError) as exc: recovery_error=str(exc)
        report['recovery_error']=recovery_error
        value=dict(ok=True,report=report,**fields)
        if inspector.managed_base is not None and report['state'] in (RUNNING,PAUSED):
            value['managed_ram']=dict(pid=os.getpid(),base=inspector.managed_base,region=region,size=0x400000)
        return value
    def commands():
        try:
            for line in sys.stdin:
                try:
                    q=json.loads(line)
                    if not isinstance(q,dict): raise ValueError('Expected command object')
                    with inspector.operation:
                        def progress(done,total):
                            emit(response(inspector.report(),progress=dict(done=done,total=total)))
                        emit(response(inspector.control(q, progress=progress)))
                except (ValueError, KeyError, TypeError, RuntimeError) as exc:
                    value=response(inspector.report()); value.update(ok=False,error=str(exc)); emit(value)
        except OSError:
            pass
        finally:
            # EOF may occur before the first RUNNING notification. Wait for
            # startup (or failure), then request normal core shutdown.
            try:
                inspector.wait(lambda:inspector.state!=STOPPED,timeout=30)
                with inspector.operation:
                    if not inspector.finished and inspector.state!=STOPPED:
                        core.cmd(STOP)
            except RuntimeError:
                pass
    t=threading.Thread(target=commands,daemon=True)
    try:
        emit(response(inspector.report())); t.start()
        core.cmd(EXECUTE)
    finally:
        with inspector.cv: inspector.finished=True; inspector.cv.notify_all()
        # Stop worker access before unloading native libraries, even on GUI close.
        # The process exits immediately after EXECUTE; commands are rejected once stopped.
        inspector.state_changed(STOPPED)
        with inspector.operation:
            core.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('rom','core','gfx','audio','input','rsp','data','config'):
        p.add_argument('--'+name,required=True)
    p.add_argument('--physical_input',default='')
    p.add_argument('--watches',default='')
    args=p.parse_args()
    global _wire
    _wire=TraceWriter(private_stdout())
    try: worker(args)
    except Exception as exc: emit(dict(ok=False,error=str(exc))); return 1
    return 0

if __name__=='__main__': raise SystemExit(main())

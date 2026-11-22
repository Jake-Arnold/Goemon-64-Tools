"""Bounded, declarative N64 guest-RAM trace scripts for the native toolkit.

This module observes the existing Rdram.read_guest interface only. It does
NOT run arbitrary Python, alter game memory, pause execution, identify a
writer, or infer a guest PC. Time stamps are host observation times.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
import re
import struct
import time
from typing import Any

from practice.pj64_debugger import guest_address
from practice.address_registry import guest_address as registered_guest_address

SCRIPT_FORMAT = 'goemon-scripted-trace-v1'
SESSION_FORMAT = 'goemon-scripted-trace-session-v1'
MAX_WATCHES = 32
MAX_TRIGGERS = 16
MAX_HISTORY = 32
MAX_POST = 32
MAX_SCRIPT_BYTES = 65536
MAX_LOG_EVENTS = 1500
MAX_TRIGGER_CAPTURE_VALUES = 128
_TYPES = {'u8':(1,False),'u16':(2,False),'u32':(4,False),'u64':(8,False),
          's8':(1,True),'s16':(2,True),'s32':(4,True),'s64':(8,True),'f32':(4,None)}
_SIMPLE = {'changed','increased','decreased'}
_COMPARE = {'eq','ne','gt','lt','ge','le'}
_BITS = {'bit_set','bit_clear'}
_TOKEN = re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,39}\Z')


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')


def _integer(value: Any, label: str, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{label} must be an integer from {low} through {high}')
    return value


def _value(value: Any, label: str) -> int | float:
    """Decimal JSON numbers or explicitly-prefixed hex strings only."""
    if isinstance(value, str):
        if not re.fullmatch(r'0[xX][0-9a-fA-F]{1,16}', value):
            raise ValueError(f'{label} must be a number or 0x-prefixed hex')
        return int(value,16)
    if type(value) not in (int,float) or not math.isfinite(value):
        raise ValueError(f'{label} must be finite numeric value')
    return value


@dataclass(frozen=True)
class TraceWatch:
    name: str
    address: int
    kind: str
    width: int


@dataclass(frozen=True)
class TraceTrigger:
    name: str
    watch: str
    op: str
    value: int | float | None
    mask: int | None
    pre_samples: int
    post_samples: int
    cooldown_ms: int
    once: bool
    capture: tuple[str, ...]


@dataclass(frozen=True)
class TraceScript:
    name: str
    sample_ms: int
    log_changes: bool
    max_events: int
    watches: tuple[TraceWatch, ...]
    triggers: tuple[TraceTrigger, ...]
    source: dict
    region: str | None = None


def parse_script(document: str | dict) -> TraceScript:
    """Strict, side-effect-free validation; rejects unknown keys and commands."""
    if isinstance(document,str):
        if len(document.encode('utf-8')) > MAX_SCRIPT_BYTES:
            raise ValueError('Script exceeds 64 KiB')
        doc=json.loads(document)
    else:
        doc=document
    if not isinstance(doc,dict):raise ValueError('Script must be a JSON object')
    allowed={'format','name','region','sample_ms','log_changes','max_events','watches','triggers'}
    if set(doc)-allowed:raise ValueError('Unsupported script keys: '+', '.join(sorted(set(doc)-allowed)))
    if doc.get('format')!=SCRIPT_FORMAT:raise ValueError('Unsupported trace script format')
    name=doc.get('name')
    if not isinstance(name,str) or not 1<=len(name)<=80 or not name.strip():
        raise ValueError('Script needs a 1..80 character name')
    region=doc.get('region')
    if region not in (None, 'usa', 'japan'):raise ValueError('Region must be usa or japan when specified')
    sample_ms=_integer(doc.get('sample_ms',200),'sample_ms',100,5000)
    max_events=_integer(doc.get('max_events',1000),'max_events',1,MAX_LOG_EVENTS)
    log_changes=doc.get('log_changes',True)
    if type(log_changes) is not bool:raise ValueError('log_changes must be a boolean')
    raw_watches=doc.get('watches')
    if not isinstance(raw_watches,list) or not 1<=len(raw_watches)<=MAX_WATCHES:
        raise ValueError('Specify 1..32 watches')
    watches=[]
    seen=set()
    for row in raw_watches:
        if not isinstance(row,dict) or set(row)!={'name','address','type'}:
            raise ValueError('Watch requires only name, address, type')
        key=row['name']; kind=row['type']
        if not isinstance(key,str) or not _TOKEN.fullmatch(key) or key in seen:
            raise ValueError('Watch names must be unique identifiers up to 40 characters')
        if not isinstance(kind,str) or kind not in _TYPES:raise ValueError(f'Invalid watch type for {key}')
        width=_TYPES[kind][0]
        addr=guest_address(row['address'],width)  # never guess a host pointer
        # Require natural alignment for integer/f32 reads that represent game fields.
        if addr % width:raise ValueError(f'{key} address is misaligned for {kind}')
        watches.append(TraceWatch(key,addr,kind,width));seen.add(key)
    raw_triggers=doc.get('triggers',[])
    if not isinstance(raw_triggers,list) or len(raw_triggers)>MAX_TRIGGERS:
        raise ValueError('Specify at most 16 triggers')
    triggers=[]; trigger_names=set()
    trigger_keys={'name','watch','op','value','mask','pre_samples','post_samples','cooldown_ms','once','capture'}
    for row in raw_triggers:
        if not isinstance(row,dict) or set(row)-trigger_keys:
            raise ValueError('Trigger contains unsupported keys')
        tname=row.get('name'); key=row.get('watch'); op=row.get('op')
        if not isinstance(tname,str) or not _TOKEN.fullmatch(tname) or tname in trigger_names:
            raise ValueError('Trigger names must be unique identifiers')
        if not isinstance(key,str) or key not in seen:raise ValueError(f'Trigger {tname} references missing watch')
        if not isinstance(op,str) or op not in (_SIMPLE|_COMPARE|_BITS):raise ValueError(f'Unknown operation for {tname}')
        kind=next(w.kind for w in watches if w.name==key)
        if kind=='f32' and op in _BITS:raise ValueError('Float watch cannot have bit trigger')
        if op in _COMPARE:
            if 'value' not in row or 'mask' in row:raise ValueError(f'{tname} requires value (not mask)')
            val=_value(row['value'],tname)
        else:
            if 'value' in row:raise ValueError(f'{tname} does not take a value')
            val=None
        if op in _BITS:
            if 'mask' not in row:raise ValueError(f'{tname} requires mask')
            mask=_value(row['mask'],tname+' mask')
            bits=next(w.width for w in watches if w.name==key)*8
            if type(mask) is not int or not 0<mask<(1<<bits):
                raise ValueError(f'{tname} mask out of range')
        else:
            if 'mask' in row:raise ValueError(f'{tname} has unexpected mask')
            mask=None
        pre=_integer(row.get('pre_samples',4),'pre_samples',0,MAX_HISTORY)
        post=_integer(row.get('post_samples',4),'post_samples',0,MAX_POST)
        cooldown=_integer(row.get('cooldown_ms',0),'cooldown_ms',0,600000)
        once=row.get('once',False)
        if type(once) is not bool:raise ValueError('once must be boolean')
        capture=row.get('capture',[w.name for w in watches])
        if (not isinstance(capture,list) or not capture or len(capture)>MAX_WATCHES or
            any(not isinstance(c,str) or c not in seen for c in capture) or len(set(capture))!=len(capture)):
            raise ValueError(f'{tname} capture must reference unique watches')
        if (pre+post+1)*len(capture)>MAX_TRIGGER_CAPTURE_VALUES:
            raise ValueError(f'{tname} capture window exceeds 128 scalar samples; reduce capture or windows')
        triggers.append(TraceTrigger(tname,key,op,val,mask,pre,post,cooldown,once,tuple(capture)))
        trigger_names.add(tname)
    # Reconstruct canonical JSON-compatible values so callers cannot mutate the validated config.
    normalized=json.loads(json.dumps(doc,allow_nan=False))
    return TraceScript(name,sample_ms,log_changes,max_events,tuple(watches),tuple(triggers),normalized,region)


def _decode(data: bytes, kind: str) -> int | float | None:
    if kind=='f32':
        number=struct.unpack('>f',data)[0]
        return number if math.isfinite(number) else None
    return int.from_bytes(data,'big',signed=_TYPES[kind][1])


def _matched(t:TraceTrigger, old:Any, new:Any, changed:bool) -> bool:
    """Edge-trigger level conditions, or compare current to prior sample."""
    if t.op=='changed':return changed
    if old is None or new is None:return False
    if t.op=='increased':return new>old
    if t.op=='decreased':return new<old
    if t.op=='bit_set':return not(old&t.mask) and bool(new&t.mask)
    if t.op=='bit_clear':return bool(old&t.mask) and not(new&t.mask)
    def level(v):
        return {'eq': lambda:v==t.value, 'ne':lambda:v!=t.value,
                'gt':lambda:v>t.value,'lt':lambda:v<t.value,
                'ge':lambda:v>=t.value,'le':lambda:v<=t.value}[t.op]()
    return level(new) and not level(old)


def _project(frame:dict, keys:tuple[str,...]) -> dict:
    return {'sample':frame['sample'],'utc':frame['utc'],
            'values':{key:frame['values'][key] for key in keys}}


class ScriptedTracer:
    """Session-scoped observational engine. poll() must run on its owner thread."""
    def __init__(self):
        self.ram=None
        self.spec:TraceScript|None=None
        self.running=False
        self.events:list[dict]=[]
        self.sample_count=0
        self.last_sample_at:float|None=None
        self.start_utc:str|None=None
        self.end_utc:str|None=None
        self._previous:dict[str,bytes]|None=None
        self._history=deque(maxlen=MAX_HISTORY)
        self._pending:list[tuple[dict,int,tuple[str,...]]]=[]
        self._fired_once:set[str]=set()
        self._fired_at:dict[str,float]={}
        self._last_frame:dict|None=None

    def start(self,ram,spec:TraceScript,*,now:float|None=None):
        if ram is None:raise RuntimeError('Connect to a running game first')
        if not isinstance(spec,TraceScript):raise ValueError('Expected validated TraceScript')
        self.ram=ram;self.spec=spec;self.running=True
        self.events=[];self.sample_count=0;self.last_sample_at=None
        self.start_utc=_utc();self.end_utc=None
        self._previous=None;self._history=deque(maxlen=MAX_HISTORY)
        self._pending=[];self._fired_once=set();self._fired_at={};self._last_frame=None
        self.poll(now=now)

    def stop(self):
        self.running=False
        if self.start_utc is not None:self.end_utc=_utc()
        # Do not discard partial pre/post records; export marks them incomplete.
        self._pending=[]
        self.ram=None

    def _append(self,item:dict):
        self.events.append(item)
        if len(self.events)>self.spec.max_events:
            del self.events[:len(self.events)-self.spec.max_events]

    def mark(self,note:str):
        if not self.running or self._last_frame is None:raise RuntimeError('Trace is not running')
        if not isinstance(note,str) or not 1<=len(note)<=120 or not note.strip():
            raise ValueError('Marker note must contain 1..120 characters')
        self._append({'kind':'marker','utc':_utc(),'sample':self._last_frame['sample'],
                      'note':note.strip()})

    def poll(self,*,now:float|None=None) -> list[dict]:
        if not self.running:return []
        if now is None:now=time.monotonic()
        if self.last_sample_at is not None and (now-self.last_sample_at)*1000<self.spec.sample_ms:
            return []
        if self.ram is None:raise RuntimeError('Trace RAM connection lost')
        raw={};values={}
        try:
            for w in self.spec.watches:
                data=self.ram.read_guest(w.address,w.width)
                if len(data)!=w.width:raise OSError(f'Short read for {w.name}')
                raw[w.name]=data
                values[w.name]={'address':f'0x{w.address:08X}','type':w.kind,
                                'hex':data.hex().upper(),'value':_decode(data,w.kind)}
        except (OSError,ValueError) as exc:
            self.stop()  # never silently mix partial/unstable observations
            raise OSError(f'Trace stopped on guest-RAM read failure: {exc}') from exc
        self.sample_count+=1
        frame={'sample':self.sample_count,'utc':_utc(),'values':values}
        # Append post samples before evaluating new triggers, so the trigger
        # sample is never also its own 'after' observation.
        pending=[]
        for event,remaining,keys in self._pending:
            event['after'].append(_project(frame,keys));remaining-=1
            if remaining:
                pending.append((event,remaining,keys))
            else:event['complete']=True
        self._pending=pending
        emitted=[]
        previous=self._previous
        if previous is not None:
            for w in self.spec.watches:
                prior=previous[w.name];current=raw[w.name]
                if current != prior and self.spec.log_changes:
                    item={'kind':'change','utc':frame['utc'],'sample':frame['sample'],
                          'watch':w.name,'address':values[w.name]['address'],
                          'before':prior.hex().upper(),'after':current.hex().upper(),
                          'before_value':_decode(prior,w.kind),'after_value':values[w.name]['value']}
                    self._append(item);emitted.append(item)
            for t in self.spec.triggers:
                if t.once and t.name in self._fired_once:continue
                w=next(w for w in self.spec.watches if w.name==t.watch)
                previous_value=_decode(previous[t.watch],w.kind)
                current_value=values[t.watch]['value']
                if not _matched(t,previous_value,current_value,raw[t.watch]!=previous[t.watch]):continue
                last=self._fired_at.get(t.name)
                if last is not None and (now-last)*1000<t.cooldown_ms:continue
                item={'kind':'trigger','utc':frame['utc'],'sample':frame['sample'],
                      'trigger':t.name,'watch':t.watch,'op':t.op,
                      'observed':_project(frame,t.capture),
                      'before':[_project(row,t.capture) for row in list(self._history)[-t.pre_samples:]] if t.pre_samples else [],
                      'after':[],'complete':t.post_samples==0}
                self._append(item);emitted.append(item)
                if t.post_samples:
                    self._pending.append((item,t.post_samples,t.capture))
                self._fired_at[t.name]=now
                if t.once:self._fired_once.add(t.name)
        self._history.append(frame)
        self._last_frame=frame
        self._previous=raw
        self.last_sample_at=now
        return emitted

    def document(self) -> dict:
        if self.spec is None:raise RuntimeError('No trace has been started')
        return {'format':SESSION_FORMAT,'script':self.spec.source,
                'started_utc':self.start_utc,'ended_utc':self.end_utc,
                'status':'recording' if self.running else 'stopped',
                'sample_count':self.sample_count,'event_count':len(self.events),
                'observation':'Host-polled N64 guest RAM; event time is observation time, not execution time. '
                              'No original MIPS PC, writer instruction or native function hooks.',
                'events':self.events}

    def jsonl(self) -> str:
        doc=self.document()
        header={k:v for k,v in doc.items() if k!='events'}
        lines=[json.dumps({'record':'session',**header},allow_nan=False)]
        lines.extend(json.dumps({'record':'event',**event},allow_nan=False) for event in self.events)
        return '\n'.join(lines)+'\n'


def _registered_usa(field_id: str, width: int) -> str:
    """Resolve observed original-USA addresses through the canonical registry."""
    return f'0x{registered_guest_address(field_id, region="usa", width=width):08X}'


VM_DIALOGUE_SCRIPT = {
    'format':SCRIPT_FORMAT,'name':'USA script VM dialogue transitions','region':'usa',
    'sample_ms':200,'log_changes':True,'max_events':1500,
    'watches':[
        {'name':'vm_state','address':_registered_usa('research:vm_state',4),'type':'u32'},
        {'name':'script_cursor','address':_registered_usa('research:vm_command_pc',4),'type':'u32'},
        {'name':'resource_id','address':_registered_usa('research:vm_resource_id',4),'type':'u32'},
        {'name':'game_state','address':_registered_usa('crosswalk:usa:static:engine_state',1),'type':'u8'},
        {'name':'submode','address':_registered_usa('crosswalk:usa:static:gameplay_submode',1),'type':'u8'}],
    'triggers':[
        {'name':'vm_state_change','watch':'vm_state','op':'changed','pre_samples':6,'post_samples':6},
        {'name':'cursor_advance','watch':'script_cursor','op':'changed','pre_samples':3,'post_samples':4}]
}

SCENE_TRANSITION_SCRIPT = {
    'format':SCRIPT_FORMAT,'name':'USA scene transition observation','region':'usa',
    'sample_ms':200,'log_changes':True,'max_events':1500,
    'watches':[
        {'name':'game_state','address':_registered_usa('crosswalk:usa:static:engine_state',1),'type':'u8'},
        {'name':'map','address':_registered_usa('crosswalk:usa:static:current_scene',2),'type':'u16'},
        {'name':'previous_map','address':_registered_usa('crosswalk:usa:static:previous_scene',2),'type':'u16'},
        {'name':'submode','address':_registered_usa('crosswalk:usa:static:gameplay_submode',1),'type':'u8'}],
    'triggers':[
        {'name':'state_changed','watch':'game_state','op':'changed','pre_samples':6,'post_samples':8},
        {'name':'map_changed','watch':'map','op':'changed','pre_samples':6,'post_samples':8}]
}

PRESETS={'Script VM / dialogue':VM_DIALOGUE_SCRIPT,'Scene transitions':SCENE_TRANSITION_SCRIPT}

"""Bounded read-only persistent-event experiments; local, versioned evidence."""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import uuid

FORMAT = 'goemon-event-session-v1'
EVENT_START = 0x8015C608
EVENT_SIZE = 0x64
MAX_TRIALS = 500
JAPAN_CANDIDATE_START = 0x80161DF8  # offset-derived saved-event candidate; not gameplay-verified
# Separate battery-research preset includes the unverified 0x80161DF9 & 0x20.
JAPAN_BATTERY_RESEARCH_START = 0x80161DC0
assert JAPAN_BATTERY_RESEARCH_START <= 0x80161DF9 < JAPAN_BATTERY_RESEARCH_START + EVENT_SIZE


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def new_session(label, backend, rom_sha1='', *, region='usa', event_start=None):
    if not isinstance(label,str) or not label.strip() or len(label)>160:
        raise ValueError('Give this experiment a name (1–160 characters)')
    if backend not in ('project64','recomp','mupen64plus'):
        raise ValueError('Select an explicit Project64, Mupen or recomp backend')
    if region not in ('usa', 'japan'):
        raise ValueError('Unsupported event-session region')
    if region == 'usa' and backend == 'mupen64plus':
        raise ValueError('USA Mupen event sessions are not supported')
    address = (EVENT_START if region == 'usa'
               else JAPAN_CANDIDATE_START) if event_start is None else event_start
    if type(address) is not int or not (0x80000000 <= address
             and address + EVENT_SIZE <= 0x80800000):
        raise ValueError('Invalid 100-byte event comparison range')
    if region == 'usa' and address != EVENT_START:
        raise ValueError('USA saved event bank address must remain fixed')
    rom_sha1=rom_sha1.strip().lower()
    if rom_sha1 and not re.fullmatch('[0-9a-f]{40}',rom_sha1):
        raise ValueError('ROM SHA-1 must contain 40 hexadecimal characters, or be blank/unverified')
    return dict(format=FORMAT,id=uuid.uuid4().hex,label=label.strip(),backend=backend,
                rom_sha1=rom_sha1 or None,created_utc=utc_now(),trials=[],
                region=region,event_start=address)


def _context(ram):
    state=ram.snapshot()  # Fresh pointers, never the UI's potentially stale snapshot.
    if state.get('loading') != 0 or not state.get('player_ptr') or not state.get('task_ptr'):
        raise ValueError('Enter stable gameplay with a loaded player')
    def byte(address):
        raw=ram.read_guest(address,1)
        if len(raw)!=1:raise OSError('Incomplete gameplay context read')
        return raw[0]
    if byte(0x800C7A94)!=13 or byte(0x80077858)!=0:
        raise ValueError('Wait for gameplay and dialogue/cutscene scripts to finish')
    return dict(map_id=ram.u16(0x800C7AB2),character=state['character'],
                player_ptr=state['player_ptr'],task_ptr=state['task_ptr'])


def _japan_event_context(ram):
    """Observe Japan runtime fields without imposing speculative gameplay rules.

    Engine mode is known, but the Japanese loading/character/scene offsets
    include candidate mappings. A read-only research snapshot must not be
    rejected simply because a candidate word is nonzero or a dialogue/script
    has changed the engine mode. Preserve exact raw values and check that the
    complete context is unchanged across the bounded 100-byte capture.
    """
    from practice.japanese_debug_warp import (
        JAPAN_DEBUG_ENGINE_MODE, JAPAN_DEBUG_SCENE,
        JAPAN_DEBUG_CHARACTER, JAPAN_DEBUG_LOADING,
    )

    def read_uint(address, width):
        raw = ram.read_guest(address, width)
        if len(raw) != width:
            raise OSError(f'Incomplete Japanese context read at 0x{address:08X}')
        return int.from_bytes(raw, 'big')

    engine = read_uint(JAPAN_DEBUG_ENGINE_MODE, 1)
    loading = read_uint(JAPAN_DEBUG_LOADING, 4)
    scene = read_uint(JAPAN_DEBUG_SCENE, 2)
    character = read_uint(JAPAN_DEBUG_CHARACTER, 4)
    context = dict(map_id=scene, character=character,
                   player_ptr=0, task_ptr=0)
    runtime = dict(engine_mode=engine, loading_word=loading)
    return context, runtime


def capture_japan_event(ram, *, event_start=JAPAN_CANDIDATE_START):
    """Observe exactly 100 Japanese bytes with unchanged runtime context.

    Any readable game state can be captured as evidence, including dialogue
    or cutscenes. No guest write or assumption of a loaded player occurs.
    """
    if type(event_start) is not int or not (
            0x80000000 <= event_start and event_start + EVENT_SIZE <= 0x80800000):
        raise ValueError('Invalid Japanese candidate RAM range')
    started = utc_now()
    before, runtime_before = _japan_event_context(ram)
    data = ram.read_guest(event_start, EVENT_SIZE)
    after, runtime_after = _japan_event_context(ram)
    if len(data) != EVENT_SIZE:
        raise OSError('Incomplete Japanese 100-byte event block; capture discarded')
    if before != after or runtime_before != runtime_after:
        raise ValueError(
            'Japanese scene/character/engine/loading changed during capture; recapture')
    return dict(started_utc=started, ended_utc=utc_now(),
                context=before, runtime=runtime_before, bytes_hex=data.hex())


def capture_event(ram):
    """One 100-byte block, bounded context reads. Not an atomic frame snapshot."""
    started=utc_now()
    before=_context(ram)
    data=ram.read_guest(EVENT_START,EVENT_SIZE)
    after=_context(ram)
    if len(data)!=EVENT_SIZE:raise OSError('Incomplete event block; capture discarded')
    if before!=after:raise ValueError('Gameplay context changed during capture; recapture')
    return dict(started_utc=started,ended_utc=utc_now(),context=before,bytes_hex=data.hex())


def _validate_capture(capture, *, region='usa'):
    if not isinstance(capture,dict):raise ValueError('Invalid capture')
    for field in ('started_utc','ended_utc'):
        stamp=datetime.fromisoformat(capture[field])
        if stamp.tzinfo is None:raise ValueError('Capture timestamp requires timezone')
    if datetime.fromisoformat(capture['started_utc'])>datetime.fromisoformat(capture['ended_utc']):
        raise ValueError('Capture times reversed')
    ctx=capture['context']
    if not isinstance(ctx,dict) or set(ctx)!={'map_id','character','player_ptr','task_ptr'}:
        raise ValueError('Invalid capture context')
    for key,low,high in (('map_id',0,65535),('character',0 if region != 'japan' else 0,
                         3 if region != 'japan' else 0xFFFFFFFF),
                         ('player_ptr',0 if region == 'japan' else 0x80000000,
                          0 if region == 'japan' else 0x807FFFFF),
                         ('task_ptr',0 if region == 'japan' else 0x80000000,
                          0 if region == 'japan' else 0x807FFFFF)):
        if type(ctx[key]) is not int or not low<=ctx[key]<=high:raise ValueError('Invalid '+key)
    runtime = capture.get('runtime')
    if runtime is not None:
        if (region != 'japan' or not isinstance(runtime, dict)
                or set(runtime) != {'engine_mode', 'loading_word'}):
            raise ValueError('Invalid Japanese runtime context')
        for key, maximum in (('engine_mode', 0xFF), ('loading_word', 0xFFFFFFFF)):
            if type(runtime[key]) is not int or not 0 <= runtime[key] <= maximum:
                raise ValueError('Invalid Japanese '+key)
    raw=capture['bytes_hex']
    if not isinstance(raw,str) or not re.fullmatch('[0-9a-fA-F]{200}',raw):
        raise ValueError('Invalid event block length/encoding')


def validate_session(session):
    try:
        if not isinstance(session,dict) or session['format']!=FORMAT:
            raise ValueError('Unsupported event-session format')
        if not re.fullmatch('[0-9a-f]{32}',session['id']):raise ValueError('Invalid session ID')
        region=session.get('region','usa')
        address=session.get('event_start',EVENT_START)
        new_session(session['label'],session['backend'],session['rom_sha1'] or '',
                    region=region,event_start=address)
        if datetime.fromisoformat(session['created_utc']).tzinfo is None:
            raise ValueError('Session timestamp requires timezone')
        trials=session['trials']
        if not isinstance(trials,list) or len(trials)>MAX_TRIALS:raise ValueError('Too many/invalid trials')
        ids=set()
        for trial in trials:
            if not isinstance(trial,dict) or not re.fullmatch('[0-9a-f]{32}',trial['id']) or trial['id'] in ids:
                raise ValueError('Invalid/duplicate trial ID')
            ids.add(trial['id'])
            if trial['role'] not in ('event','idle','control'):raise ValueError('Invalid trial role')
            if not isinstance(trial['note'],str) or len(trial['note'])>500:raise ValueError('Invalid trial note')
            captures=trial['captures']
            if not isinstance(captures,dict) or set(captures) not in ({'A','B'},{'A','B','C'}):
                raise ValueError('Trials need A/B and optional C')
            for capture in captures.values():
                _validate_capture(capture,region=region)
            ordered=[captures[key] for key in ('A','B','C') if key in captures]
            if any(datetime.fromisoformat(a['ended_utc'])>datetime.fromisoformat(b['started_utc'])
                   for a,b in zip(ordered,ordered[1:])):
                raise ValueError('Capture stages are out of time order')
        return session
    except (KeyError,TypeError,AttributeError,OverflowError) as exc:
        raise ValueError('Malformed event session') from exc


def changed_context_fields(captures):
    """Context is provenance for global flags, not a requirement across captures."""
    contexts=[captures[key]['context'] for key in ('A','B','C') if key in captures]
    if not contexts:return []
    return [key for key in ('map_id','character','player_ptr','task_ptr')
            if any(context[key]!=contexts[0][key] for context in contexts[1:])]


def describe_contexts(captures):
    parts=[]
    for stage in ('A','B','C'):
        if stage not in captures:continue
        ctx=captures[stage]['context']
        details = (f'{stage}: map {ctx["map_id"]}, character {ctx["character"]}, '
                   f'player 0x{ctx["player_ptr"]:08X}, task 0x{ctx["task_ptr"]:08X}')
        runtime = captures[stage].get('runtime')
        if runtime is not None:
            details += (f', JP engine {runtime["engine_mode"]}, '
                        f'loading candidate 0x{runtime["loading_word"]:08X}')
        parts.append(details)
    return '; '.join(parts)


def with_trial(session,role,note,captures):
    """Return an independent validated value; failures do not mutate the session."""
    result=json.loads(json.dumps(session))
    result['trials'].append(dict(id=uuid.uuid4().hex,role=role,note=note,
                                 captures=json.loads(json.dumps(captures))))
    return validate_session(result)


def save_session(path,session):
    validate_session(session)
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        with temporary.open('x',encoding='utf-8') as stream:
            json.dump(session,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        temporary.unlink(missing_ok=True)


def load_session(path):
    path=Path(path)
    if path.stat().st_size>2_000_000:raise ValueError('Session file exceeds 2 MB limit')
    try:return validate_session(json.loads(path.read_text(encoding='utf-8')))
    except (UnicodeError,json.JSONDecodeError) as exc:raise ValueError('Invalid session JSON') from exc


def rank_bits(session):
    """Full bit evidence with missing/opposite/control trials; no confidence probability."""
    validate_session(session)
    events=[t for t in session['trials'] if t['role']=='event']
    controls=[t for t in session['trials'] if t['role']!='event']
    blocks={t['id']:{stage:bytes.fromhex(capture['bytes_hex']) for stage,capture in t['captures'].items()}
            for t in session['trials']}
    def transition(trial,index,mask):
        a=blocks[trial['id']]['A'][index]&mask
        b=blocks[trial['id']]['B'][index]&mask
        return 0 if a==b else (1 if b else -1)
    rows=[]
    for index in range(EVENT_SIZE):
        for bit in range(8):
            mask=1<<bit
            for direction in (1,-1):
                support=[t for t in events if transition(t,index,mask)==direction]
                if not support:continue
                opposite=[t['id'] for t in events if transition(t,index,mask)==-direction]
                absent=[t['id'] for t in events if transition(t,index,mask)==0]
                noise=[t['id'] for t in controls if transition(t,index,mask)!=0]
                reverted=[];not_reverted=[]
                for t in support:
                    c=blocks[t['id']]
                    if 'C' in c:
                        destination=reverted if ((c['C'][index]^c['A'][index])&mask)==0 else not_reverted
                        destination.append(t['id'])
                base=session.get('event_start',EVENT_START)
                rows.append(dict(address=f'0x{base+index:08X}',mask=f'{mask:02X}',
                    direction='set' if direction==1 else 'clear',support=[t['id'] for t in support],
                    event_trials=len(events),opposite=opposite,absent=absent,control_overlap=noise,
                    reverted=reverted,not_reverted=not_reverted,confirmed=False))
    rows.sort(key=lambda r:(bool(r['control_overlap']),len(r['opposite'])+len(r['absent']),
                            -len(r['support']),int(r['address'],16),int(r['mask'],16),r['direction']))
    return dict(format='goemon-event-ranking-v1',session_id=session['id'],
                region=session.get('region','usa'),
                event_start=f'0x{session.get("event_start",EVENT_START):08X}',
                rom_identity_verified=False,rom_sha1=session['rom_sha1'],candidates=rows,
                context_changes={t['id']:changed_context_fields(t['captures']) for t in session['trials']
                                 if changed_context_fields(t['captures'])},
                notes='Observations only. ROM hash is user-supplied, not verified against the running game. '
                      'Captures are not atomic; matching context cannot detect all in-frame transitions. '
                      'Japanese engine/loading fields are recorded as observed context, not prerequisites '
                      'or independently verified gameplay-status decoders. '
                      'Room/character/pointer changes between captures are retained as context, not filtered. '
                      'Room transitions may change unrelated global flags. '
                      'A changed bit is not a proven event trigger or write-safe flag.')

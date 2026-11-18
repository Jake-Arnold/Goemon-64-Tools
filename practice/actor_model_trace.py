"""Correlate manually captured Japan-0 actor and draw snapshots without RAM access.

This is evidence analysis, not a graphics hook or a model-ID-to-ROM-file map.
The file contains no ROM or game memory bytes. Source layout:
  ActorTask (recomp patches/types.h): Task.heap_element +0x18,
  actor_id +0x5C, model_id +0x5E.
  Object: graphics_1 +0x2C, graphics_2 +0x30, overlay_info +0x34.
The Object layout is not independently verified for original Japan-0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import struct

SCHEMA = 'goemon-japan-0-actor-model-trace-v1'
INIT_AFTER_PC = 0x8021D834  # Following sh t1,+0x5E(s0) at genuine JP initializer +0x6C.
DRAW_ENTRY_PC = 0x800167D4  # JP counterpart candidate of USA object graphics dispatcher.
MAX_CAPTURE_BYTES = 256 * 1024
MAX_EVENTS = 256
ACTOR_BYTES = 0x60
OBJECT_BYTES = 0x68
HEX_WORD = re.compile(r'0x[0-9a-fA-F]{8}\Z')
HEX_BYTES = re.compile(r'[0-9a-fA-F]+\Z')
HEX_SHA256 = re.compile(r'[0-9a-f]{64}\Z')


def _pointer(value, label, *, allow_null=False):
    if not isinstance(value, str) or not HEX_WORD.fullmatch(value):
        raise ValueError(f'{label} requires 0x followed by eight hex digits')
    number = int(value, 16)
    if allow_null and number == 0:
        return number
    if number & 3 or not 0x80000000 <= number < 0x80800000:
        raise ValueError(f'{label} must be an aligned 8-MiB KSEG0 RAM pointer')
    return number


def _snapshot(value, count, label):
    if not isinstance(value, str) or len(value) != 2 * count or not HEX_BYTES.fullmatch(value):
        raise ValueError(f'{label} must contain exactly {count} big-endian bytes as hex, no address columns')
    return bytes.fromhex(value)


def _frame(value):
    if type(value) is not int or not 0 <= value <= 0x7FFFFFFF:
        raise ValueError('frame must be a nonnegative integer <= 2147483647')
    return value


def _parse_event(row):
    if not isinstance(row, dict):
        raise ValueError('each capture must be an object')
    kind = row.get('kind')
    frame = _frame(row.get('frame'))
    if kind == 'actor':
        pc = _pointer(row.get('pc'), 'actor pc')
        if pc not in (INIT_AFTER_PC, DRAW_ENTRY_PC):
            raise ValueError('actor sample pc must be the JP initializer +0x70 (0x8021D834) or JP draw entry')
        ptr = _pointer(row.get('actor_ptr'), 'actor_ptr')
        blob = _snapshot(row.get('header_hex'), ACTOR_BYTES, 'actor header_hex')
        heap, = struct.unpack_from('>I', blob, 0x18)
        actor_id, model_id = struct.unpack_from('>HH', blob, 0x5C)
        return {'kind':kind,'frame':frame,'actor_ptr':ptr,'object_ptr':heap,
                'site':'init' if pc==INIT_AFTER_PC else 'draw_pause',
                'actor_id':actor_id,'model_id':model_id,
                'valid_object_ptr':heap != 0 and (heap & 3)==0 and 0x80000000 <= heap < 0x80800000}
    if kind == 'draw':
        if _pointer(row.get('pc'), 'draw pc') != DRAW_ENTRY_PC:
            raise ValueError('draw capture must be taken at Japanese dispatcher entry 0x800167D4')
        ptr = _pointer(row.get('a0'), 'draw a0')
        blob = _snapshot(row.get('header_hex'), OBJECT_BYTES, 'draw header_hex')
        graphics_1, graphics_2 = struct.unpack_from('>II', blob, 0x2C)
        overlays = [struct.unpack_from('>HHI', blob, 0x34 + 8*i) for i in range(6)]
        return {'kind':kind,'frame':frame,'object_ptr':ptr,'graphics_1':graphics_1,
                'graphics_2':graphics_2,'object_kind':graphics_1 & 0x70000000,
                'graphics_payload':graphics_1 & 0x8FFFFFFE,
                'overlays':[{'slot':i,'file_id':o[0],'vram_base':f'0x{o[2]:08X}'}
                            for i,o in enumerate(overlays)]}
    if kind == 'frame':
        label = row.get('label')
        if label not in ('good','bad'):
            raise ValueError('frame evidence label must be good or bad')
        digests = {}
        for key in ('guest_gbi_sha256','guest_matrices_sha256','guest_textures_sha256','framebuffer_sha256'):
            value = row.get(key)
            if value is not None:
                if not isinstance(value,str) or not HEX_SHA256.fullmatch(value):
                    raise ValueError(f'{key} must be a lowercase 64-character SHA-256 digest')
                digests[key] = value
        return {'kind':kind,'frame':frame,'label':label,**digests}
    raise ValueError('capture kind must be actor, draw or frame')


def analyze(capture):
    """Return metadata-only evidence; reject ambiguous or unsupported inputs."""
    if not isinstance(capture, dict) or capture.get('schema') != SCHEMA:
        raise ValueError('unsupported trace schema')
    if capture.get('region') != 'japan_0' or capture.get('map_id') != 3:
        raise ValueError('this trace is limited to Japan-0 map 0x0003')
    rows = capture.get('captures')
    if not isinstance(rows,list) or not 1 <= len(rows) <= MAX_EVENTS:
        raise ValueError(f'requires 1..{MAX_EVENTS} capture events')
    events = [_parse_event(row) for row in rows]
    actors = [e for e in events if e['kind']=='actor']
    draws = [e for e in events if e['kind']=='draw']
    frames = [e for e in events if e['kind']=='frame']
    # Require a unique, stable observed heap pointer per captured actor. Reused
    # pointers or time-varying task layouts are not resolved by this format.
    ptr_to_actors = {}
    actor_headers = {}
    for a in actors:
        key=a['actor_ptr']
        identity=(a['object_ptr'],a['actor_id'])
        if key in actor_headers and actor_headers[key] != identity:
            raise ValueError('conflicting actor captures: instance reuse or object rebind requires a generation-aware trace')
        actor_headers[key]=identity
        if a['valid_object_ptr']:
            ptr_to_actors.setdefault(a['object_ptr'],set()).add(key)
    matches=[]
    unmatched=[]
    for d in draws:
        candidates=[a for a in actors if a['actor_ptr'] in ptr_to_actors.get(d['object_ptr'],()) and a['frame'] <= d['frame']]
        candidates={a['actor_ptr']:a for a in candidates}
        # Require same frame: actor header must still correspond to the draw.
        same_frame=[a for a in candidates.values() if a['frame']==d['frame']]
        # A draw-time recheck must be anchored to an earlier initializer
        # observation for the very same task pointer.
        same_frame=[a for a in same_frame if a['site']=='init' or
                    any(i['site']=='init' and i['actor_ptr']==a['actor_ptr']
                        and i['frame']<=a['frame'] for i in actors)]
        if len(same_frame)!=1:
            unmatched.append({'frame':d['frame'],'object_ptr':f"0x{d['object_ptr']:08X}",
                              'reason':'no unique same-frame actor header, anchored to initializer, matching Task.heap_element'})
            continue
        a=same_frame[0]
        initial=next((i for i in actors if i['site']=='init' and
                      i['actor_ptr']==a['actor_ptr'] and i['frame']<=a['frame']),a)
        matches.append({'frame':d['frame'],'actor_ptr':f"0x{a['actor_ptr']:08X}",
                        'actor_id':f"0x{a['actor_id']:04X}",
                        'model_id':f"0x{a['model_id']:04X}",
                        'initial_model_id':f"0x{initial['model_id']:04X}",
                        'model_changed_after_init':a['model_id']!=initial['model_id'],
                        'object_ptr':f"0x{d['object_ptr']:08X}",
                        'graphics_1':f"0x{d['graphics_1']:08X}",
                        'graphics_2':f"0x{d['graphics_2']:08X}",
                        'graphics_payload':f"0x{d['graphics_payload']:08X}",
                        'graphics_kind':f"0x{d['object_kind']:08X}",
                        'overlays':d['overlays'],
                        'binding_status':'observed Task.heap_element == render Object*; Japan graphics field layout still provisional'})
    comparison = {'status':'not_comparable','reason':'a paired good/bad capture with three guest digests and framebuffer hashes is required'}
    goods=[f for f in frames if f['label']=='good']
    bads=[f for f in frames if f['label']=='bad']
    keys=('guest_gbi_sha256','guest_matrices_sha256','guest_textures_sha256')
    for good in goods:
        for bad in bads:
            if abs(good['frame']-bad['frame']) != 1:
                continue
            if not all(k in good and k in bad for k in keys+('framebuffer_sha256',)):
                continue
            same=[k for k in keys if good[k]==bad[k]]
            changed=[k for k in keys if k not in same]
            if good['framebuffer_sha256'] == bad['framebuffer_sha256']:
                verdict='framebuffer digests identical despite visual good/bad labels; capture is inconclusive'
            elif changed:
                verdict='guest draw inputs differ; investigate upstream model/animation or capture conditions before blaming RT64'
            else:
                verdict='captured guest inputs identical; suspect uncaptured GPU state, RT64 interpolation, or rendering state'
            comparison={'status':'compared','good_frame':good['frame'],'bad_frame':bad['frame'],
                        'same_inputs':same,'changed_inputs':changed,'interpretation':verdict}
            break
        if comparison['status']=='compared':break
    return {'schema':SCHEMA,'region':'japan_0','map_id':3,
            'capture_counts':{'actors':len(actors),'draws':len(draws),'frames':len(frames)},
            'actor_ids_seen':sorted({f"0x{a['actor_id']:04X}" for a in actors}),
            'target_actor_seen':any(a['actor_id']==0x00FB for a in actors),
            'matches':matches,'unmatched_draws':unmatched,'frame_comparison':comparison,
            'limitations':['Runtime pointer equality is not proof of a ROM mesh/resource-file mapping.',
                           'The Japan-0 Object graphics layout comes from recomp source; independent live layout verification remains outstanding.',
                           'The Japanese draw entry is a uniquely matched original-ROM instruction prefix; a live debugger trace is still required.',
                           'No display-list contents, RT64 calls or texture data are captured by this tool.']}


def load_capture(path):
    path=Path(path)
    if path.stat().st_size > MAX_CAPTURE_BYTES:
        raise ValueError('trace file exceeds the 256-KiB cap')
    return json.loads(path.read_text(encoding='utf-8'))


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('capture',help='local JSON trace (kept local; never commit RAM snapshots)')
    args=ap.parse_args(argv)
    try:
        print(json.dumps(analyze(load_capture(args.capture)),sort_keys=True,indent=2))
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        ap.exit(2,f'Invalid trace: {exc}\n')


if __name__=='__main__':
    main()
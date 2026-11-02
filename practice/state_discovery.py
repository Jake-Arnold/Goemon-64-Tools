"""Read-only state-difference probes for finding original Goemon N64 RAM fields.

No memory addresses inferred here are automatically promoted into confirmed
settings or written to game memory. Captures record values, not ground truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math
import struct

FOCUSED_RANGES = (
    ('system', 0x800C7800, 0x1000),
    ('game_data', 0x8015C500, 0x900),
)
WIDE_RANGE = ('base_4mb', 0x80000000, 0x400000)
DYNAMIC_RANGES = (('player_task', 'task_ptr', 0xF0), ('player_object', 'player_ptr', 0x98))
PROBE_ACTIONS = {
    'Travel destinations': 'Capture A before visiting a never-before-seen dragon travel stop; B after it is unlocked. Expect persistent bits, not necessarily one byte per destination.',
    'Map displayed': 'Hold still in an outdoor area. Capture A with C-Right map hidden; B with map visible; C after hiding again.',
    'Selected item / weapon': 'Equipped weapon index confirmed at 0x8015C607: 01/02/03 for each character. Compare A/B/C to investigate other item selection and animation fields.',
    'Magic active': 'Capture A before C-Up, B while the magic effect is active, C after it ends. Repeat separately for Goemon, Ebisumaru, Sasuke and Yae.',
    'Player velocity': 'Capture A while stationary, B while moving or jumping and C when stationary again. Player-task float candidates are shown separately; observed XYZ speed is already displayed on Dashboard.',
}


@dataclass(frozen=True)
class RegionData:
    name: str
    address: int
    data: bytes


@dataclass(frozen=True)
class ProbeCapture:
    label: str
    utc: str
    character: int
    map_id: int
    regions: tuple[RegionData, ...]
    scope: str


def capture_state(ram, label: str, *, scope: str = 'focused', snapshot: dict | None = None) -> ProbeCapture:
    if scope not in ('focused', 'wide'):
        raise ValueError('Scope must be focused or wide')
    if not label.strip():
        raise ValueError('Capture label is required')
    snapshot = snapshot if snapshot is not None else ram.snapshot()
    current_map = ram.u16(0x800C7AB2)
    character = ram.u32(0x8015C5DC)
    if character > 3:
        raise ValueError('Invalid current character')
    regions=[]
    for name, addr, size in (FOCUSED_RANGES if scope == 'focused' else (WIDE_RANGE,)):
        data = ram.read_guest(addr, size)
        if len(data) != size:
            raise OSError(f'Incomplete read for {name}')
        regions.append(RegionData(name, addr, data))
    if scope == 'focused':
        for name, ptr_key, size in DYNAMIC_RANGES:
            address=snapshot.get(ptr_key)
            if address:
                data=ram.read_guest(address,size)
                if len(data)!=size:
                    raise OSError(f'Incomplete read for {name}')
                regions.append(RegionData(name,address,data))
    return ProbeCapture(label,datetime.now(timezone.utc).isoformat(),character,current_map,tuple(regions),scope)


def _f32(data: bytes, index: int) -> float | None:
    if index + 4 > len(data):
        return None
    value=struct.unpack_from('>f',data,index)[0]
    return value if math.isfinite(value) and abs(value) < 100000 else None


def compare_captures(before: ProbeCapture, after: ProbeCapture,
                     reverted: ProbeCapture | None = None, *, limit: int = 1200) -> dict:
    """Return changed bytes, bit transitions and plausible player task f32 changes.

    A third snapshot filters to fields that EXACTLY return to A's previous byte.
    Context (character/map) is included so users can distinguish unrelated
    scene transitions and per-character state.
    """
    if before.scope != after.scope or (reverted and before.scope != reverted.scope):
        raise ValueError('Capture scopes differ; recapture all three at the same scope')
    index_b={(r.name,r.address):r for r in after.regions}
    index_c={} if reverted is None else {(r.name,r.address):r for r in reverted.regions}
    rows=[]
    totals={'observed_changes':0,'reverting_changes':0,'regions_compared':0}
    for old in before.regions:
        key=(old.name,old.address)
        nxt=index_b.get(key)
        if nxt is None or len(old.data)!=len(nxt.data):
            continue
        restore=index_c.get(key)
        if reverted and (restore is None or len(restore.data)!=len(old.data)):
            continue
        totals['regions_compared']+=1
        for i,(a,b) in enumerate(zip(old.data,nxt.data)):
            if a==b:
                continue
            totals['observed_changes']+=1
            returned=(restore is not None and restore.data[i]==a)
            if reverted is not None and not returned:
                continue
            if returned:
                totals['reverting_changes']+=1
            mask=a^b
            is_bit=mask.bit_count()==1
            binary=a in (0,1) and b in (0,1)
            score=(50 if returned else 0)+(20 if binary else 0)+(12 if is_bit else 0)
            if old.name in ('game_data','base_4mb') and before.label.lower().startswith('travel'):
                score+=5
            if old.name=='player_task':
                score+=3
            row={'address':f'0x{old.address+i:08X}', 'region':old.name,
                 'before':f'{a:02X}','after':f'{b:02X}',
                 'xor_mask':f'{mask:02X}', 'reverted':returned,
                 'score':score, 'kind':'boolean' if binary else ('one-bit' if is_bit else 'byte'),
                 'width':1}
            rows.append(row)
        if old.name in ('player_task','player_object'):
            for i in range(0,len(old.data)-3,4):
                a=_f32(old.data,i); b=_f32(nxt.data,i)
                if a is None or b is None or a==b:
                    continue
                if restore is not None and _f32(restore.data,i)!=a:
                    continue
                rows.append({'address':f'0x{old.address+i:08X}', 'region':old.name,
                             'before':f'{a:.5g}', 'after':f'{b:.5g}',
                             'xor_mask':'—', 'reverted':restore is not None,
                             'score':75 if restore is not None else 15,
                             'kind':'f32 candidate', 'width':4})
    rows.sort(key=lambda v:(-v['score'],v['region'],int(v['address'],16),v['width']))
    return {
        'format':'goemon-state-difference-v1',
        'capture_A':{'label':before.label,'utc':before.utc,'character':before.character,'map_id':before.map_id},
        'capture_B':{'label':after.label,'utc':after.utc,'character':after.character,'map_id':after.map_id},
        'capture_C':None if reverted is None else {'label':reverted.label,'utc':reverted.utc,'character':reverted.character,'map_id':reverted.map_id},
        'scope':before.scope,
        'counts':{**totals,'reported_candidates':min(limit,len(rows)), 'candidate_count':len(rows)},
        'candidates':rows[:limit],
        'notes':'CANDIDATES ONLY. Field semantics require repeat tests; A→B→A reversibility helps reject changing unrelated RAM. '
                'The player_task float entries are unknown fields, not proven velocity. No writes or full RAM dumps are exported.'
    }


def measured_velocity(current: dict, previous: dict | None, dt: float | None) -> tuple[float,float,float] | None:
    """Observed XYZ displacement in units/sec, NOT game-engine velocity."""
    if previous is None or dt is None or not 0.01 <= dt <= 1.0:
        return None
    if not current.get('player_ptr') or current.get('player_ptr') != previous.get('player_ptr'):
        return None
    if current.get('character') != previous.get('character') or current.get('loading') or previous.get('loading'):
        return None
    if any(current.get(k) is None or previous.get(k) is None for k in ('x','y','z')):
        return None
    return tuple((current[k]-previous[k])/dt for k in ('x','y','z'))

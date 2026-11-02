"""Original MNSG native-debug menu selection reverse-engineering adapter.

This is NOT a known native debug-menu cursor map. The upstream decomp does not
currently expose the menu's selection fields. Observe a user's actual native
menu, compare stable RAM values across different selections, explicitly accept
a candidate, and only then drive the game's menu selection/confirmation.

No host-process pointers are saved; every candidate is a genuine guest N64
address. Usable as a reference for a future ROM-side hook.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json

from practice.scene_controls import NATIVE_DEBUG_CATEGORIES
from practice.checkpoints import STATE_ADDR, MAP_ADDR

BASE = 0x80000000
# The original v0.9-v0.9.1 scanner stopped at 0x801CB460, exactly where
# the swappable native menu/level-select overlays begin. A menu cursor can
# live in an overlay; scan the entire base 4 MiB of N64 RDRAM while the
# native menu is active. This is still original N64 guest memory, not PC state.
SIZE = 0x00400000
NATIVE_STATE = 10
PROFILE_FORMAT = 'mnsg-usa-debug-selection-v1'


@dataclass(frozen=True)
class Observation:
    map_id: int
    character: int
    first: bytes
    second: bytes
    def __post_init__(self):
        if len(self.first) != SIZE or len(self.second) != SIZE:
            raise ValueError('Native menu observation size mismatch')
        if not (0 <= self.character < 4):
            raise ValueError('Invalid character')


@dataclass(frozen=True)
class Candidate:
    role: str
    method: str
    addr: int
    width: int
    examples: int
    before: int
    after: int

    def to_json(self):
        return dict(role=self.role,method=self.method,addr=f'0x{self.addr:08X}',width=self.width,
                    examples=self.examples,before=self.before,after=self.after)


def selection_values(map_id: int) -> dict:
    if not 0 <= map_id <= 0x26C:
        raise ValueError('Invalid map')
    for index, (threshold, _) in enumerate(NATIVE_DEBUG_CATEGORIES):
        if map_id >= threshold:
            return {'map_id': map_id, 'stage_index': map_id-threshold, 'category_index': len(NATIVE_DEBUG_CATEGORIES)-index}
    raise ValueError('Unrecognized map')


def menu_state(ram):
    return ram.u8(STATE_ADDR) == NATIVE_STATE


def take_menu_snapshot(ram):
    if not menu_state(ram):
        raise ValueError('Open the original in-game debug menu before recording a selection')
    data=ram.read_guest(BASE,SIZE)
    if not menu_state(ram):
        raise ValueError('Menu exited during memory capture')
    return data


def _expected(obs: Observation, method: str) -> int:
    return obs.character if method=='character_id' else selection_values(obs.map_id)[method]


def _stable(obs, off, width):
    return obs.first[off:off+width] == obs.second[off:off+width]


def _read(buf: bytes, off: int, width: int):
    return int.from_bytes(buf[off:off+width],'big')


def _valid_address(addr, width):
    # Don't rewrite known game state, live resources, inventory, scene identifier,
    # active overlays, or original system pointers while "calibrating".
    blocked = ((STATE_ADDR, STATE_ADDR+1),
               (MAP_ADDR,MAP_ADDR+2),
               (0x8015C5C0,0x8015CC24),
               (0x800C7A9E,0x800C7AA0))
    # MIPS lw/sw and lh/sh require natural alignment for ordinary globals.
    # Misaligned multi-byte hits result from coincidental byte patterns.
    if addr % width != 0:
        return False
    # This region is the original base game's executable code rather than
    # writable BSS; a purported cursor here is almost certainly coincidental.
    if BASE <= addr < 0x8007E020:
        return False
    return all(addr+width<=a or addr>=b for a,b in blocked)


def candidates_for_pair(a: Observation, b: Observation, role: str, method: str):
    if role not in ('scene','character','category'):
        raise ValueError('Unknown field role')
    if method not in ('map_id','stage_index','category_index','character_id'):
        raise ValueError('Unknown method')
    if (role == 'character') != (method == 'character_id'):
        raise ValueError('Inconsistent field role')
    if role == 'scene' and method not in ('map_id','stage_index'):
        raise ValueError('Invalid scene mapping')
    if role == 'category' and method!='category_index':
        raise ValueError('Invalid category mapping')
    if role=='character' and a.map_id != b.map_id:
        raise ValueError('Change only character when calibrating its field')
    if role in ('scene','category') and a.character != b.character:
        raise ValueError('Change only scene when calibrating its field')
    if role=='scene' and method=='stage_index' and selection_values(a.map_id)['category_index'] != selection_values(b.map_id)['category_index']:
        raise ValueError('Calibrate stage index using two scenes in the same category')
    want_a, want_b = _expected(a,method),_expected(b,method)
    if want_a==want_b:
        raise ValueError('The two selections must differ in the target field')
    # Scan CHANGED bytes only, then check up to four possible starts for each.
    # A candidate is admitted only if both observations were stable, have the
    # expected encoded value, and did change with the menu selection.
    result=[]
    inspected=set()
    for off,(old,new) in enumerate(zip(a.first,b.first)):
        if old==new:
            continue
        for width in (1,2,4):
            if want_a >= (1<<(width*8)) or want_b >= (1<<(width*8)):
                continue
            for start in range(max(0,off-width+1), min(off,SIZE-width)+1):
                key=(start,width)
                if key in inspected:
                    continue
                inspected.add(key)
                addr=BASE+start
                if (not _valid_address(addr,width) or not _stable(a,start,width) or not _stable(b,start,width)):
                    continue
                if _read(a.first,start,width)==want_a and _read(b.first,start,width)==want_b:
                    result.append(Candidate(role,method,addr,width,2,want_a,want_b))
    return sorted(result,key=lambda c:(c.width!=2,c.width!=1,c.addr))


def find_candidates(observations: list[Observation]):
    """Cross-validate same-char scene pairs and same-scene character pairs."""
    scores={}
    for ia,a in enumerate(observations):
        for b in observations[ia+1:]:
            if a.map_id==b.map_id and a.character!=b.character:
                roles=(('character','character_id'),)
            elif a.character==b.character and a.map_id!=b.map_id:
                roles=(('scene','map_id'),('scene','stage_index'),('category','category_index'))
            else:
                continue
            for role,method in roles:
                try:
                    match=candidates_for_pair(a,b,role,method)
                except ValueError:
                    continue
                for c in match:
                    key=(c.role,c.method,c.addr,c.width)
                    if key not in scores:
                        scores[key]=[0,c]
                    scores[key][0]+=1
    return sorted((Candidate(c.role,c.method,c.addr,c.width,pairs,c.before,c.after)
                   for pairs,c in scores.values()),
                  key=lambda c:(-c.examples,c.role,c.addr,c.width))


def validate_profile(profile: dict):
    if profile.get('format')!=PROFILE_FORMAT:
        raise ValueError('Invalid native debug calibration profile')
    fields=profile.get('fields')
    if not isinstance(fields,dict):
        raise ValueError('Missing native debug fields')
    for role,c in fields.items():
        if role not in ('scene','category','character'):
            raise ValueError(f'Unknown field {role}')
        addr=int(c['addr'],16) if isinstance(c['addr'],str) else c['addr']
        width=c.get('width')
        if width not in (1,2,4) or not (BASE<=addr<BASE+SIZE) or not _valid_address(addr,width):
            raise ValueError(f'Invalid guest address/width in {role}')
        method=c.get('method')
        if role=='character' and method!='character_id':
            raise ValueError('Character mapping must use character_id')
        if role=='category' and method!='category_index':
            raise ValueError('Category mapping must use category_index')
        if role=='scene' and method not in ('map_id','stage_index'):
            raise ValueError('Scene mapping must be map_id or stage_index')
    addrs=[(int(v['addr'],16) if isinstance(v['addr'],str) else v['addr'],v['width']) for v in fields.values()]
    for i,(a,n) in enumerate(addrs):
        for b,m in addrs[i+1:]:
            if a < b+m and b < a+n:
                raise ValueError('Menu fields overlap')
    return fields


def calibrated_for_direct_warp(profile: dict):
    fields=validate_profile(profile)
    required = ('character','scene') if fields.get('scene',{}).get('method')=='map_id' else ('character','scene','category')
    # Two matching pair comparisons is still not definitive proof. It is the
    # minimum before enabling high-risk native-menu writes. Field selection
    # must be validated in live gameplay and only with a disposable save.
    return all(role in fields and int(fields[role].get('pairs',0)) >= 2 for role in required)


def stage_menu_selection(ram, profile: dict, map_id: int, character: int):
    """Stage original-menu SELECTED VALUES ONLY; does not trigger scene load.

    The game menu must be active and each address must have been discovered by
    stable user-observed menu samples. This is an experimental menu adapter,
    not a raw gameplay warp or a ROM patch.
    """
    if not menu_state(ram):
        raise ValueError('Native debug menu is not active')
    if not calibrated_for_direct_warp(profile):
        raise ValueError('Native debug-menu selection not calibrated')
    if type(character) is not int or character not in range(4):
        raise ValueError('Choose a character 0–3')
    targets=selection_values(map_id)
    fields=validate_profile(profile)
    # Gather and validate all writes before the first mutation.
    ops=[]
    for role in ('category','scene','character'):
        if role not in fields:continue
        field=fields[role];method=field['method'];width=field['width']
        addr=int(field['addr'],16) if isinstance(field['addr'],str) else field['addr']
        number=character if method=='character_id' else targets[method]
        if number >= (1<<(width*8)):
            raise ValueError(f'{role} value does not fit learned field width')
        original=ram.read_guest(addr,width)
        ops.append((addr,number.to_bytes(width,'big'),original))
    # Verify menu did not exit between snapshot and write; rollback on failure.
    if not menu_state(ram):
        raise ValueError('Menu exited before write')
    changed=[]
    try:
        for addr,data,original in ops:
            ram.write_guest(addr,data)
            changed.append((addr,original))
            if ram.read_guest(addr,len(data))!=data or not menu_state(ram):
                raise RuntimeError('Menu value did not verify or menu exited during staging')
    except Exception:
        if menu_state(ram):
            for addr,old in reversed(changed):
                try: ram.write_guest(addr,old)
                except Exception: pass
        raise
    return {'map_id':map_id,'character':character,'values':{f['method']:(character if f['method']=='character_id' else targets[f['method']]) for f in fields.values()},'status':'staged_not_confirmed'}


def load_profile(path: Path):
    if not path.exists():
        return {'format': PROFILE_FORMAT, 'fields': {}}
    profile=json.loads(path.read_text(encoding='utf-8'))
    validate_profile(profile)
    return profile


def save_profile(path: Path, profile: dict):
    validate_profile(profile)
    path.write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')


def candidate_report(observations: list[Observation], candidates: list[Candidate], profile: dict):
    """Lossless, untruncated export of ALL scored candidate addresses.

    Observations are labelled metadata only: raw guest-RAM snapshots stay in
    memory and are never included in the report.
    """
    counts = Counter((c.role, c.method) for c in candidates)
    return {
        'format': 'mnsg-usa-native-menu-candidates-v2',
        'date': datetime.now(timezone.utc).isoformat(),
        'observations': [
            {'map_id': o.map_id, 'character': o.character} for o in observations
        ],
        'total_candidates': len(candidates),
        'scan_range': {'start': f'0x{BASE:08X}', 'end_exclusive': f'0x{BASE+SIZE:08X}', 'includes_overlay_ram': True},
        'candidate_counts': {
            role: {method: counts[(role, method)]
                   for method in sorted({m for r, m in counts if r == role})}
            for role in ('character', 'scene', 'category')
        },
        'candidates': [c.to_json() for c in candidates],
        'profile': profile,
        'notes': 'All candidates exported without a 400-entry cap. ' +
                 'They are unverified hypotheses derived from user-labelled N64 menu changes; ' +
                 'no raw RAM dump or ROM bytes are included.',
    }


def display_candidate_indices(candidates: list[Candidate], limit: int = 400):
    """Keep the UI bounded but do not hide scene/character behind category hits.

    Full candidate list remains untouched and is always available in export.
    """
    if limit <= 0:
        return []
    if len(candidates) <= limit:
        return list(range(len(candidates)))
    # Reserve slots for the three roles. Ranking within a role is preserved.
    priorities = ('character', 'scene', 'category')
    indices = []
    seen = set()
    for role in priorities:
        quota = max(1, limit // len(priorities))
        taken = 0
        for i, candidate in enumerate(candidates):
            if taken >= quota:
                break
            if candidate.role == role and i not in seen:
                indices.append(i)
                seen.add(i)
                taken += 1
    for i in range(len(candidates)):
        if len(indices) >= limit:
            break
        if i not in seen:
            indices.append(i)
    return indices

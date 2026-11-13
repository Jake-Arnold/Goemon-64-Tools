"""USA original-game memory inspector. Reads only; NO dynamic guessing of offsets.

Resource addresses verified by disassembly in ogdanimal's Goemon64Recomp-Android
reverse-engineering notes. Inventory item offsets come from MetroidMoo's US
GameFAQs GameShark reference and MUST be checked against the game UI.
All offsets are N64 guest addresses, NOT Windows host pointers.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct
import math
from practice import checkpoints as cp
from practice.native_menu_categories import native_menu_category, NATIVE_MENU_CATEGORIES
from practice.story_progress import read_story_state,story_rows

CHARACTERS = ('Goemon', 'Ebisumaru', 'Sasuke', 'Yae')

# User-observed gameplay labels only: not exclusive native enum meanings.
VM_STATE_HINTS = {
    0: "usually idle / no text",
    1: "text rendering observed",
    2: "interactive selection observed",
    3: "A to continue observed",
    4: "A to close observed",
    5: "area-notice lead-in observed; unverified",
    6: "observed briefly; meaning unknown",
    7: "area notice or scripted dialogue observed",
}
GAMEPLAY_SUBMODE_HINTS = {
    0: "dungeon areas observed",
    1: "overworld areas observed",
    2: "towns / villages observed",
    3: "building interiors observed",
    4: "Impact gameplay observed",
    7: "Impact introduction observed",
}


# Each tuple (label, guest_address, width in bytes, accepted_max, meaning)
# Entries explicitly verified by the user in live gameplay are marked confirmed.
# Unverified fields (e.g., suspected Sasuke battery) remain clearly labelled.
INVENTORY = [
    ('Item slot 1 code', 0x8015C5F3, 1, 255, 'confirmed item slot 1 code; not necessarily selected item'),
    ('Item slot 2 code', 0x8015C5F7, 1, 255, 'user verified item slot/quantity address'),
    ('Item slot 2 quantity', 0x8015C5FB, 1, 255, 'user verified item slot/quantity address'),
    ('Item slot 3 code', 0x8015C5FF, 1, 255, 'user verified item slot/quantity address'),
    ('Item slot 3 quantity', 0x8015C603, 1, 255, 'user verified item slot/quantity address'),
    ('Goemon in party', 0x8015C69F, 1, 1, '0=no, 1=yes; community mapping'),
    ('Ebisumaru in party', 0x8015C6A3, 1, 1, '0=no, 1=yes; community mapping'),
    ('Sasuke in party', 0x8015C6A7, 1, 1, '0=no, 1=yes; community mapping'),
    ('Yae in party', 0x8015C6AB, 1, 1, '0=no, 1=yes; community mapping'),
    ('Goemon pipe upgrade', 0x8015C6AF, 1, 2, 'user verified: 0 normal, 1 silver, 2 gold'),
    ('Ebisumaru hammer upgrade', 0x8015C6B3, 1, 2, 'user verified: 0 normal, 1 silver, 2 gold'),
    ('Sasuke kunai upgrade', 0x8015C6B7, 1, 2, 'user verified: 0 normal, 1 double, 2 gold'),
    ('Yae katana upgrade', 0x8015C6BB, 1, 2, 'user verified: 0 normal, 1 silver, 2 gold'),
    ('Chain Pipe', 0x8015C6BF, 1, 2, 'user verified: acquired when nonzero'),
    ('Meat Saw Hammer', 0x8015C6C3, 1, 1, 'user verified: acquired when nonzero'),
    ('Fire Cracker Bomb', 0x8015C6C7, 1, 1, 'user verified: acquired when nonzero'),
    ('Flute', 0x8015C6CB, 1, 1, 'user verified: acquired when nonzero'),
    ('Windup Camera', 0x8015C6D3, 1, 1, 'user verified: acquired when nonzero'),
    ('Ice Kunai', 0x8015C6D7, 1, 1, 'user verified: acquired when nonzero'),
    ('Bazooka', 0x8015C6DB, 1, 1, 'user verified: acquired when nonzero'),
    ('Medal of Flames', 0x8015C6DF, 1, 1, 'user verified: acquired when nonzero'),
    ('Sudden Impact', 0x8015C6EF, 1, 1, 'user verified: acquired when nonzero'),
    ('Mini Ebisumaru', 0x8015C6F3, 1, 1, 'user verified: acquired when nonzero'),
    ('Super Jump', 0x8015C6F7, 1, 1, 'user verified: acquired when nonzero'),
    ('Magic Mermaid', 0x8015C6FB, 1, 1, 'user verified: acquired when nonzero'),
    ('Triton Shell', 0x8015C6FF, 1, 1, 'user verified in-game'),
    ('Unknown brown item (Achilles Heel? candidate)', 0x8015C703, 1, 1, 'item identity NOT confirmed'),
    ('Fortune Doll progress (low byte)', 0x8015C707, 1, 4, 'low byte of 32-bit progress word 0x8015C704; native item renderer handles 1..4, not a boolean'),
    ('Sasuke battery 1 collected', 0x8015C609, 1, 255, 'CONFIRMED: event byte bit 0x20; preserves other flags'),
    ("Achilles' Heel", 0x8015C70F, 1, 1, 'ROM reward script: inventory word 0x8015C70C; user mapping'),
    ('Gold Key', 0x8015C713, 1, 1, 'user verified in-game'),
    ('Cucumber (formerly Blue Sausage)', 0x8015C717, 1, 1, 'item identification tentative, previously Blue Sausage'),
    ('Red fish count', 0x8015C71B, 1, 255, 'count (was Pink Fish); user observed 0x01 displays one'),
    ('Yellow fish count', 0x8015C71F, 1, 255, 'count (was Gold Fish); user observed 0x01 displays one'),
    ('Blue fish count', 0x8015C723, 1, 255, 'count; user observed 0x01 displays one'),
    ('Star', 0x8015C85B, 1, 1, 'Miracle item: star'),
    ('Moon', 0x8015C85F, 1, 1, 'Miracle item: moon'),
    ('Flower', 0x8015C863, 1, 1, 'Miracle item: flower'),
    ('Snowflake', 0x8015C866, 1, 1, 'Miracle item: snowflake; address ends C866'),
]

@dataclass(frozen=True)
class Watch:
    name: str
    addr: int | None
    value: str
    raw: str
    status: str
    source: str = ''


def _read_int(ram, addr, width):
    return int.from_bytes(ram.read_guest(addr, width), 'big')


def get_watches(ram, snapshot, scene_names=None):
    """Return watch records with provenance/validation, not guessed fields."""
    scene_names = scene_names or {}
    watches = []
    def add(name, addr, width, decode=None, validator=None, source='reverse-engineered'):
        try:
            v = _read_int(ram, addr, width)
            valid = validator is None or validator(v)
            decoded = decode(v) if decode else str(v)
            watches.append(Watch(name, addr, str(decoded), f'0x{v:0{width*2}X}',
                                 'OK' if valid else 'CHECK', source))
        except (OSError, ValueError) as e:
            watches.append(Watch(name, addr, f'READ FAILED: {e}', '—', 'ERROR', source))
    add('Character', 0x8015C5DC, 4,
        lambda v: f'{CHARACTERS[v]} ({v})' if v < 4 else f'UNKNOWN ({v})',
        lambda v: v < 4)
    add('Map ID', cp.MAP_ADDR, 2,
        lambda v: f'{v} / 0x{v:03X} — {scene_names.get(v, "Unmapped / verify")}',
        lambda v: v < 0x800)
    add('Current health (units)', 0x8015C5E4, 4, validator=lambda v: v<=127)
    add('Maximum health (units)', 0x8015C5E0, 4, validator=lambda v: 0<v<=127)
    add('Ryo', 0x8015C5E8, 4, validator=lambda v: v<=9999)
    add('Lives', 0x8015C5EC, 4, validator=lambda v: v<=99)
    add('Top-level game state', cp.STATE_ADDR, 1,
        lambda v: f'{v} (reload=12; gameplay=13; debug menu=10)',lambda v:v<18)
    add('Phase', cp.PHASE_ADDR, 1, validator=lambda v:v<3)
    add('Loading flag', 0x8015C5D4, 4, validator=lambda v:v<=1)
    # ROM-backed VM globals from the pinned USA G64-021/027/030 traces.
    # Addresses and access widths are observed; semantic names are inferred.
    add('Script cursor (VM)', cp.SCRIPT_VM_ADDR, 4,
        lambda v: 'Inactive (0)' if v == 0 else f'0x{v:08X} (nonzero)',
        source='ROM-observed 32-bit cursor access; inferred script meaning, not a lock')
    add('Script VM state', 0x801C77E0, 4,
        lambda v: f'{v} — {VM_STATE_HINTS.get(v, "meaning unknown")}',
        source='ROM-observed 32-bit VM state; labels are gameplay observations, not universal semantics')
    add('Script resource ID', 0x801C78E8, 4,
        lambda v: f'{v} / 0x{v:08X}',
        source='ROM-observed current resource word; may be updated by VM setup')
    add('Script VM pause byte', 0x801C78FC, 1,
        lambda v: str(v if v < 128 else v - 256),
        source='ROM-observed signed 8-bit access; pause meaning inferred')
    state=ram.u8(cp.STATE_ADDR)
    if state==10:
        add('Native menu category',cp.SUBMODE_ADDR,1,
            lambda v: f'{v} — {native_menu_category(v)}',
            lambda v: v < len(NATIVE_MENU_CATEGORIES),
            source='user-observed native menu row order; 0 MAIN, 1 SIRO, 2 DOUCHU, 3 MACHI, 4 SHOP')
    else:
        add('Gameplay submode',cp.SUBMODE_ADDR,1,
            lambda v: (f'{v} — {GAMEPLAY_SUBMODE_HINTS.get(v, "unmapped")}' if state == 13
                       else f'{v} — outside ordinary gameplay; meaning unverified'),
            source='same address as menu category; user-observed mode associations, not a decoded enum')
    add('Stage offset',0x800C7AB4,2,source='verified menu stage index; also updates at scene load')
    add('Previous map',0x800C7ABC,2,source='observed door transition: previous map commits with current map')
    add('Pending destination',0x800C7CA0,2,source='observed door transition: updates before the next map loads')
    add('Exit request (not warp)',0x800C7A9F,1,source='0 in observed door transition; writing 1 exited to title')
    add('Native menu entry pointer (state 10 only)',0x800C7E60,4,
        lambda v: f'0x{v:08X} (' +
            (('menu entry ' + str((v-0x8007BAD0)//12)) if state==10 and
             0x8007BAD0<=v<=0x8007BAF4 and (v-0x8007BAD0)%12==0
             else 'STALE/UNKNOWN; do not use as spawn selector') + ')',
        source='read-only; character-linked pointer observed ONLY during live native-menu highlights')
    add('Sasuke battery 2 cutscene finished (observed)',0x8015C609,1,
        lambda v: 'Yes (bit 0x40)' if v & 0x40 else 'No (bit 0x40)',
        source='observed: second battery cutscene ends with 0x20 -> 0x60; cutscene trigger separate')
    for row in story_rows(read_story_state(ram)):
        watches.append(Watch('Story: '+row['name'],row['address'],row['value'],row['raw'],row['status'],
            row['bank']+'; mask '+row['mask']+'; '+row['source']))
    add('Map overlay state (observed)',0x8015C574,1,
        lambda v: f'{v} ({"visible" if v == 1 else "hidden" if v == 0 else "unusual"})',
        validator=lambda v: v in (0,1),
        source='observed 0/1 when toggled by game; external writes may open the map regardless of value')
    obj=snapshot.get('player_ptr')
    if obj:
        watches.extend([
            Watch('X', obj+0x08, f'{snapshot["x"]:.3f}', ram.read_guest(obj+0x08,4).hex().upper(),'OK','player object'),
            Watch('Y', obj+0x0C, f'{snapshot["y"]:.3f}', ram.read_guest(obj+0x0C,4).hex().upper(),'OK','player object'),
            Watch('Z', obj+0x10, f'{snapshot["z"]:.3f}', ram.read_guest(obj+0x10,4).hex().upper(),'OK','player object'),
        ])
    task=snapshot.get('task_ptr')
    if task:
        addr=task+0x68
        try:
            bits=ram.read_guest(addr,4)
            value=struct.unpack('>f',bits)[0]
            watches.append(Watch('Task +0x68 f32 (movement hypothesis)',addr,
                f'{value:.6g}' if math.isfinite(value) else str(value),
                '0x'+bits.hex().upper(), 'CHECK',
                'dynamic player task; manual movement nudge observed, not proven velocity'))
        except (OSError,ValueError,struct.error) as exc:
            watches.append(Watch('Task +0x68 f32 (movement hypothesis)',addr,
                f'READ FAILED: {exc}','—','ERROR','dynamic player task'))
    add('Equipped weapon index',0x8015C607,1,
        lambda v: f'{v} ({"weapon slot" if v in (1,2,3) else "outside normal 1–3; cross-character fallback observed"})',
        validator=lambda v: v in (1,2,3),
        source='confirmed in-game across all four characters; out-of-range entries use unintended weapons')
    add('Fortune Doll progress (quarters)',0x8015C704,4,
        lambda v: ('2/4 (1/2)' if v==2 else f'{v}/4') if v<=4 else f'Unexpected ({v})',
        validator=lambda v:v<=4,source='native item-screen reads saved data +0xFC; renderer handles 1..4; live word 2 matched half icon')
    add('Fortune Dolls obtained (annotated total)',0x8015C708,4,
        source='mn64rando word annotation; live value 2 alongside half icon; full reset/award rules not traced')
    for name,addr,width,maximum,hint in INVENTORY:
        if addr == 0x8015C609:
            add(name,addr,1,lambda v: 'Yes (bit 0x20)' if v & 0x20 else 'No (bit 0x20)',
                source='confirmed by live pre-pickup flag write and subsequent stage progression')
            continue
        confirmed = (name.startswith('Item slot ') or name.startswith('Goemon pipe upgrade')
                     or name.startswith('Ebisumaru hammer upgrade')
                     or name.startswith('Sasuke kunai upgrade')
                     or name.startswith('Yae katana upgrade')
                     or name in {'Chain Pipe', 'Meat Saw Hammer', 'Fire Cracker Bomb', 'Flute',
                                 'Windup Camera', 'Ice Kunai', 'Bazooka', 'Medal of Flames',
                                 'Sudden Impact', 'Mini Ebisumaru', 'Super Jump', 'Magic Mermaid',
                                 'Star', 'Moon', 'Flower', 'Snowflake', 'Fortune Doll progress (low byte)'})
        add(name,addr,width,validator=lambda v, m=maximum: v<=m,
            source=('confirmed: ' if confirmed else 'provisional: ')+hint)
    return watches


def checkpoint_differences(ram, checkpoint, max_rows=200):
    """Compare original-game logical progress in canonical guest byte order.

    Mirror gamedata+0x64:0x94 to LIVE, because the game's saved copy may be
    stale between saves. This comparison is read-only and never resumes a game.
    """
    from practice.checkpoints import validate_checkpoint
    p, blobs = validate_checkpoint(checkpoint)
    current_map=ram.u16(cp.MAP_ADDR)
    current_character=ram.u32(0x8015C5DC)
    regions={
        'live':(cp.LIVE_ADDR,blobs['live']),
        'gamedata':(cp.GAMEDATA_ADDR,blobs['gamedata']),
        'header':(cp.HEADER_ADDR,blobs['header']),
    }
    changes=[]
    counts={}
    total=0
    for name,(addr,old) in regions.items():
        new=ram.read_guest(addr,len(old))
        # Stale save mirror of resources, not independently authoritative.
        if name == 'gamedata':
            indices=[i for i in range(len(old)) if not 0x64<=i<0x94]
        else:
            indices=range(len(old))
        diff=[(i,a,b) for i in indices if (a:=old[i]) != (b:=new[i])]
        counts[name]=len(diff)
        total+=len(diff)
        for offset,a,b in diff[:max(0,max_rows-len(changes))]:
            changes.append((name,f'0x{addr+offset:08X}',f'0x{offset:03X}',f'{a:02X}',f'{b:02X}'))
    return {
        'map_matches':current_map==p['map_id'],
        'map_live':current_map,'map_saved':p['map_id'],
        'character_matches':current_character==p['character'],
        'character_live':current_character,'character_saved':p['character'],
        'counts':counts,'total':total,'rows':changes,'omitted':max(0,total-len(changes)),
    }

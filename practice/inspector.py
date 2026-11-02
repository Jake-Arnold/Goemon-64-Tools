"""USA original-game memory inspector. Reads only; NO dynamic guessing of offsets.

Resource addresses verified by disassembly in ogdanimal's Goemon64Recomp-Android
reverse-engineering notes. Inventory item offsets come from MetroidMoo's US
GameFAQs GameShark reference and MUST be checked against the game UI.
All offsets are N64 guest addresses, NOT Windows host pointers.
"""
from __future__ import annotations
from dataclasses import dataclass
from practice import checkpoints as cp
from practice.native_menu_categories import native_menu_category, NATIVE_MENU_CATEGORIES

CHARACTERS = ('Goemon', 'Ebisumaru', 'Sasuke', 'Yae')

# Each tuple (label, guest_address, width in bytes, accepted_max, meaning)
# Explicitly user-verified mappings are identified as confirmed; uncertain fields remain provisional.
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
    ('Silver Fortune Doll? (candidate)', 0x8015C707, 1, 1, 'old GameShark item name, unverified'),
    ('Sasuke battery? (candidate)', 0x8015C70B, 1, 1, 'inferred unused four-byte item slot, NOT confirmed'),
    ('Round brown item (Achilles Heel? candidate)', 0x8015C70F, 1, 1, 'item identity NOT confirmed'),
    ('Gold Key', 0x8015C713, 1, 1, 'user verified in-game'),
    ('Cucumber (formerly Blue Sausage)', 0x8015C717, 1, 1, 'item identification tentative, previously Blue Sausage'),
    ('Red fish count', 0x8015C71B, 1, 255, 'count (was Pink Fish); user observed 0x01 displays one'),
    ('Yellow fish count', 0x8015C71F, 1, 255, 'count (was Gold Fish); user observed 0x01 displays one'),
    ('Blue fish count', 0x8015C723, 1, 255, 'count; user observed 0x01 displays one'),
    ('Miracle item 1 (identity unknown)', 0x8015C85B, 1, 1, 'four Miracle Items GameShark code; individual symbol unverified'),
    ('Miracle item 2 (identity unknown)', 0x8015C85F, 1, 1, 'four Miracle Items GameShark code; individual symbol unverified'),
    ('Miracle item 3 (identity unknown)', 0x8015C863, 1, 1, 'four Miracle Items GameShark code; individual symbol unverified'),
    ('Miracle item 4 (identity unknown)', 0x8015C866, 1, 1, 'four Miracle Items GameShark code; offset explicitly C866, verify in-game'),
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
        lambda v: f'{v} (normal gameplay=13; debug menu=10)',lambda v:v<18)
    add('Phase', cp.PHASE_ADDR, 1, validator=lambda v:v<3)
    add('Loading flag', 0x8015C5D4, 4, validator=lambda v:v<=1)
    add('Event/script VM lock', cp.SCRIPT_VM_ADDR, 4)
    state=ram.u8(cp.STATE_ADDR)
    if state==10:
        add('Native menu category',cp.SUBMODE_ADDR,1,
            lambda v: f'{v} — {native_menu_category(v)}',
            lambda v: v < len(NATIVE_MENU_CATEGORIES),
            source='user-observed native menu order: MAIN=0, SIRO=1, DOUCHU=2, MACHI=3, SHOP=4')
    else:
        add('Gameplay submode',cp.SUBMODE_ADDR,1,source='same address as menu category; context dependent')
    add('Stage offset',0x800C7AB4,2,source='verified menu stage index; also updates at scene load')
    add('Previous map',0x800C7ABC,2,source='observed door transition: previous map commits with current map')
    add('Pending destination',0x800C7CA0,2,source='observed door transition: updates before the next map loads')
    add('Exit request (not warp)',0x800C7A9F,1,source='0 in observed door transition; writing 1 exited to title')
    add('Native menu entry pointer',0x800C7E60,4,
        lambda v:f'0x{v:08X} (menu entry; not a character ID)',
        source='follows debug-menu highlight; may be used on other menu pages')
    obj=snapshot.get('player_ptr')
    if obj:
        watches.extend([
            Watch('X', obj+0x08, f'{snapshot["x"]:.3f}', ram.read_guest(obj+0x08,4).hex().upper(),'OK','player object'),
            Watch('Y', obj+0x0C, f'{snapshot["y"]:.3f}', ram.read_guest(obj+0x0C,4).hex().upper(),'OK','player object'),
            Watch('Z', obj+0x10, f'{snapshot["z"]:.3f}', ram.read_guest(obj+0x10,4).hex().upper(),'OK','player object'),
        ])
    add('Selected item (currently equipped)', None, 0, source='NOT MAPPED') if False else None
    watches.append(Watch('Selected item (currently equipped)',None,'Not mapped yet', '—','UNKNOWN',
                          'Item slots below are not evidence of current selection'))
    for name,addr,width,maximum,hint in INVENTORY:
        confirmed = (name.startswith('Item slot ') or name.startswith('Goemon pipe upgrade')
                     or name.startswith('Ebisumaru hammer upgrade')
                     or name.startswith('Sasuke kunai upgrade')
                     or name.startswith('Yae katana upgrade')
                     or name in {'Chain Pipe', 'Meat Saw Hammer', 'Fire Cracker Bomb', 'Flute',
                                 'Windup Camera', 'Ice Kunai', 'Bazooka', 'Medal of Flames',
                                 'Sudden Impact', 'Mini Ebisumaru', 'Super Jump', 'Magic Mermaid'})
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

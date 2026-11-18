"""USA original-game debug-mode entry and separate scene experiments.

Source: abyssonym/mn64rando tables/patch_debug_menu_en.txt: the ROM hack
opens its native debug menu by storing 0x0A in 0x800C7A94 after L press.
That does NOT mean simply writing the map ID performs a valid warp.
"""
from practice.checkpoints import STATE_ADDR, MAP_ADDR
DEBUG_MENU_STATE = 10


def open_native_debug_menu(ram):
    """Request the original USA debug menu with one exact 0x0A byte write.

    No player/task pointer, submode, loading state, selected scene or entrance
    is needed. This is not a destination warp; the game's native menu owns
    destination selection and subsequent loading.

    The provided reader must belong to an already verified, write-enabled USA
    connection. Exact-byte writes avoid touching adjacent swapped host bytes.
    """
    current = ram.u8(STATE_ADDR)
    if current != DEBUG_MENU_STATE:
        ram.write_guest_byte_exact(STATE_ADDR, DEBUG_MENU_STATE)
    observed = ram.u8(STATE_ADDR)
    if observed != DEBUG_MENU_STATE:
        raise RuntimeError(
            f'USA debug-menu engine state 0x0A did not verify: '
            f'0x{observed:02X}')
    return observed

# Guest RAM values established in Goemon64Recomp-Android reverse-engineering
# notes. THIS IS AN EXPERIMENTAL HYPOTHESIS ABOUT HOW TO INITIATE A WARP.
# The field 0x800C7CA0 is the pending map; the exit flag is 0x800C7A9F.
# Writing the two is not confirmed to trigger the game's full scene teardown.
# In particular, spawn coordinates/entrance data might remain inconsistent.
# It is intentionally separate from the native debug-menu entry.
PENDING_MAP_ADDR = 0x800C7CA0
EXIT_REQUEST_ADDR = 0x800C7A9F
MAX_US_MAP_ID = 0x26C


def request_scene_warp(ram, destination: int, known_scenes: dict):
    """Disabled: v0.9.7's exit-bit experiment returned to the main menu.

    A pending map and an exit request are NOT sufficient to trigger an area
    load. No direct scene warp writes will be sent until the actual game
    transition mechanism is identified and validated.
    """
    raise RuntimeError(
        "Direct warp disabled: v0.9.7 triggered game exit/title screen, "
        "not a valid scene load. No memory writes made."
    )


def assess_direct_warp(ram, destination: int):
    """Monitor scene and full gameplay state, never conclude success on map alone.

    Debug-menu navigation itself can alter the absolute map before a load.
    A direct request can only count as success with playable state and a valid
    newly loaded player. The caller requires consecutive stable polls too.
    """
    state=ram.u8(STATE_ADDR)
    phase=ram.u8(0x800C7A9E)
    exit_flag=ram.u8(EXIT_REQUEST_ADDR)
    map_id=ram.u16(MAP_ADDR)
    pending_map=ram.u16(PENDING_MAP_ADDR)
    character=ram.u32(0x8015C5DC)
    loading=ram.u32(0x8015C5D4)
    status='waiting'
    if state==13 and phase==1 and exit_flag==0 and not loading and map_id==destination:
        try:
            snap=ram.snapshot()
            if snap['player_ptr'] and snap['task_ptr'] and snap['x'] is not None:
                status='loaded_and_playable'
        except (ValueError,OSError):
            pass
    return dict(status=status,state=state,phase=phase,exit_request=exit_flag,
                map_id=map_id,pending_map=pending_map,character=character,loading=loading)


def assess_scene_warp(ram, destination: int):
    """Read-only post-request observation; never writes the active scene ID."""
    try:
        here = ram.u16(MAP_ADDR)
        if here == destination:
            return 'destination_observed'
        if ram.u8(EXIT_REQUEST_ADDR) != 0 or ram.u8(STATE_ADDR) != 13:
            return 'transition_pending'
        return 'no_change'
    except (OSError, ValueError):
        return 'unreadable'


# The original game's level-select labels have four families, as recorded by
# abyssonym/mn64rando MapCategoryData.DEBUG_WARP_CATEGORIES and debug_index.
# This mapping is a *label*, not an address or an automatic warp command.
NATIVE_DEBUG_CATEGORIES = (
    (0x190, "SHOP"),
    (0x15E, "MACHI"),
    (0x12C, "DOUCHU"),
    (0x000, "SIRO"),
)


def native_debug_selection(map_id: int, known_scenes: dict):
    """Return the original debug-menu selection label for a named USA room.

    The returned label is useful when manually choosing a room in the actual
    N64 menu; it does not claim that modifying that menu's cursor has been
    implemented. Do not truncate IDs to 8 bits, as many rooms are >255.
    """
    if type(map_id) is not int or map_id not in known_scenes:
        raise ValueError("Unknown USA room ID")
    for first_id, category in NATIVE_DEBUG_CATEGORIES:
        if map_id >= first_id:
            return {"map_id": map_id, "room_name": known_scenes[map_id],
                    "category": category, "index": map_id - first_id,
                    "label": f"{category} {map_id - first_id}"}
    raise ValueError("Invalid map ID")


def open_native_debug_for_scene(ram, map_id: int, known_scenes: dict):
    """Open the *actual* game level-select; never request an unverified warp.

    Note: the level-select cursor/commit routine is not decoded yet. The
    destination is a UI hint only; the user must select it in the game.
    """
    target = native_debug_selection(map_id, known_scenes)
    observed_state = open_native_debug_menu(ram)
    return {**target, "menu_state": observed_state, "status": "menu_opened_selection_manual"}

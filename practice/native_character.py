"""Original-game character-change helpers for the US Mystical Ninja game.

The *game* owns character swapping. The Goemon64Recomp adapter below presses
its normal C-Down input; it does not write character IDs, player pointers or
model-loader addresses. Future N64 ROM code can call the original game's swap
entry point instead of using Win32 keyboard injection.

Research: ogdanimal/Goemon64Recomp-Android,
 docs/re-notes/goemon_character_swap_re.md (2026-07-18).
"""
from __future__ import annotations
from dataclasses import dataclass
import os

from practice.checkpoints import GAMEDATA_ADDR, MAP_ADDR, STATE_ADDR, validate_checkpoint, _ensure_capture_safe

PARTY_OFFSET = 0x94
IDLE_ACTIONS = frozenset((0, 1, 0x42))
CHARACTER_TASK_OFFSET = 0x60


def scene_character_unlocked(ram, character: int) -> bool:
    """C-Down cannot select characters missing from the current party."""
    if type(character) is not int or character not in range(4):
        raise ValueError('Expected character 0–3')
    return bool(ram.u32(GAMEDATA_ADDR + PARTY_OFFSET + 4 * character))


def ready_for_scene_character(ram, map_id: int, character: int, snapshot=None) -> bool:
    """Verify global and per-task actor IDs, rather than just a displayed cursor."""
    if type(character) is not int or character not in range(4):
        return False
    if ram.u8(STATE_ADDR) != 13 or ram.u16(MAP_ADDR) != map_id:
        return False
    snap = snapshot if snapshot is not None else ram.snapshot()
    if (snap.get('loading') or snap.get('character') != character
            or snap.get('action') not in IDLE_ACTIONS or not snap.get('task_ptr')):
        return False
    return ram.u8(snap['task_ptr'] + CHARACTER_TASK_OFFSET) == character

@dataclass(frozen=True)
class PartyPatch:
    address: int
    before: bytes
    staged: bytes


def prepare_character_swap(ram, checkpoint):
    """Make the saved character selectable using the original party table.

    Only a *single party entry* is changed, temporarily. The game still
    performs its ordinary character swap (graphics load + task reconstruction).
    Nothing else from the checkpoint is restored until native swap completes.
    On success, the full gamedata snapshot supersedes this temporary entry.
    """
    payload, blobs = validate_checkpoint(checkpoint)
    state = _ensure_capture_safe(ram)
    if ram.u16(MAP_ADDR) != payload['map_id']:
        raise ValueError('Checkpoint map differs; first enter the saved map using Scene browser')
    if state['character'] == payload['character']:
        return None
    selected = payload['character']
    addr = GAMEDATA_ADDR + PARTY_OFFSET + 4*selected
    old = ram.read_guest(addr, 4)
    desired = blobs['gamedata'][PARTY_OFFSET+4*selected:PARTY_OFFSET+4*selected+4]
    if int.from_bytes(desired, 'big') == 0:
        raise ValueError('Saved character is not unlocked in this checkpoint; native swapping is unavailable')
    if int.from_bytes(old, 'big'):
        return None  # Already unlocked; don't touch party inventory.
    # The original game checks the 32-bit entry. Use the checkpoint's exact
    # four bytes, not a guessed in-memory byte offset.
    ram.write_guest(addr, desired)
    if ram.read_guest(addr, 4) != desired:
        ram.write_guest(addr, old)
        raise OSError('Temporary party unlock did not verify')
    return PartyPatch(addr, old, desired)


def undo_character_preparation(ram, patch: PartyPatch | None, target_character: int):
    """Best-effort compare-and-restore. Never lock the currently active avatar.

    If the user is now playing the temporarily unlocked character, removing
    availability could leave the game in an inconsistent state; leave it alone.
    """
    if patch is None:
        return 'nothing to undo'
    if ram.snapshot()['character'] == target_character:
        return 'character now active; kept temporary party unlock'
    if ram.read_guest(patch.address, 4) != patch.staged:
        return 'party changed elsewhere; no rollback attempted'
    ram.write_guest(patch.address, patch.before)
    return 'temporary party unlock reverted'


def ready_after_native_swap(ram, checkpoint) -> bool:
    """Require both global and per-task character IDs plus idle action.

    The model-load state machine runs as action 0xBA for many frames.
    A global-character match in the middle of this work is NOT sufficient.
    """
    payload, _ = validate_checkpoint(checkpoint)
    current = _ensure_capture_safe(ram)
    if current['character'] != payload['character'] or ram.u16(MAP_ADDR) != payload['map_id']:
        return False
    if current['action'] not in IDLE_ACTIONS:
        return False
    if not current['task_ptr'] or ram.u8(current['task_ptr'] + CHARACTER_TASK_OFFSET) != payload['character']:
        return False
    return True


def _game_window(pid: int):
    import ctypes
    from ctypes import wintypes
    u = ctypes.WinDLL('user32', use_last_error=True)
    u.EnumWindows.argtypes = [ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
    u.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    u.IsWindowVisible.argtypes = [wintypes.HWND]
    u.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    u.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    match = []
    cb_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def callback(hwnd, _):
        p = wintypes.DWORD()
        u.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == pid and u.IsWindowVisible(hwnd) and u.GetWindowTextLengthW(hwnd):
            size=u.GetWindowTextLengthW(hwnd)+1
            title=ctypes.create_unicode_buffer(size)
            u.GetWindowTextW(hwnd,title,size)
            if 'goemon' in title.value.lower():
                match.append(hwnd)
        return True
    cb=cb_type(callback)
    u.EnumWindows(cb,0)
    if not match:
        raise RuntimeError('Could not find the Goemon64Recomp game window')
    return u, match[0]


def press_native_c_down(pid: int):
    """Hold the *default* keyboard C-Down binding for 180ms; return key-up.

    Caller MUST schedule the returned release function even on errors. This is
    an optional Windows input adapter, NOT the implementation of the game swap.
    Custom keyboard/controller mappings may require manual in-game C-Down.
    """
    if os.name != 'nt':
        raise OSError('Automatic key press is only supported on Windows; use in-game C-Down')
    from ctypes import wintypes
    import ctypes
    u, hwnd = _game_window(pid)
    u.SetForegroundWindow.argtypes=[wintypes.HWND]
    u.GetForegroundWindow.restype=wintypes.HWND
    u.GetWindowThreadProcessId.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.DWORD)]
    if not u.SetForegroundWindow(hwnd):
        raise RuntimeError('Windows prevented focusing Goemon. Focus the game and press C-Down manually')
    focused = u.GetForegroundWindow()
    owner=wintypes.DWORD()
    u.GetWindowThreadProcessId(focused,ctypes.byref(owner))
    if owner.value != pid:
        raise RuntimeError('Game was not focused; press C-Down manually')
    VK_DOWN=0x28
    KEYEVENTF_EXTENDEDKEY=0x0001
    KEYEVENTF_KEYUP=0x0002
    u.MapVirtualKeyW.argtypes=[wintypes.UINT,wintypes.UINT]
    u.keybd_event.argtypes=[wintypes.BYTE,wintypes.BYTE,wintypes.DWORD,ctypes.c_size_t]
    scan=u.MapVirtualKeyW(VK_DOWN,0)
    u.keybd_event(VK_DOWN,scan,KEYEVENTF_EXTENDEDKEY,0)
    def release():
        u.keybd_event(VK_DOWN,scan,KEYEVENTF_EXTENDEDKEY|KEYEVENTF_KEYUP,0)
    return release


def press_native_debug_accept(pid: int):
    """Press US recomp's DEFAULT N64 A keyboard binding (Space), once.

    This only confirms a native menu selection already staged by the game.
    The release callback must always run. Rebinds require manual confirmation.
    """
    if os.name != 'nt':
        raise OSError('Native debug keyboard shortcut requires Windows')
    import ctypes
    from ctypes import wintypes
    u,hwnd=_game_window(pid)
    u.SetForegroundWindow.argtypes=[wintypes.HWND]
    u.SetForegroundWindow(hwnd)
    u.GetForegroundWindow.restype=wintypes.HWND
    active=u.GetForegroundWindow()
    owner=wintypes.DWORD()
    u.GetWindowThreadProcessId(active,ctypes.byref(owner))
    if owner.value!=pid:
        raise RuntimeError('Could not focus game; press the N64 A button inside the debug menu')
    u.MapVirtualKeyW.argtypes=[wintypes.UINT,wintypes.UINT]
    u.keybd_event.argtypes=[wintypes.BYTE,wintypes.BYTE,wintypes.DWORD,ctypes.c_size_t]
    vk=0x20 # Space, default N64 A in the recomp's source
    scan=u.MapVirtualKeyW(vk,0)
    u.keybd_event(vk,scan,0,0)
    def release():u.keybd_event(vk,scan,2,0)
    return release

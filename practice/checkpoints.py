"""Original-game logical checkpoints for Mystical Ninja Starring Goemon (US).

The data contract deliberately contains *guest* memory and coordinates, not
Windows/Goemon64Recomp host pointers. A future ROM implementation can use the
same addresses and layout. Restore is exploratory and is NOT a native savestate.

Source: ogdanimal/Goemon64Recomp-Android docs/re-notes/goemon_cheats_re.md
and docs/re-notes/goemon_save_re.md, based on original game disassembly.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from practice.address_registry import guest_address

GAME = "mnsg-usa"
FORMAT = "goemon-logical-checkpoint-v1"
LIVE_ADDR, LIVE_LEN = 0x8015C5D8, 0x30
GAMEDATA_ADDR, GAMEDATA_LEN = 0x8015C608, 0x304
SHADOW_ADDR = 0x8015C910
HEADER_ADDR, HEADER_LEN = 0x8015CC18, 0x0C
MAP_ADDR = guest_address("crosswalk:usa:static:current_scene", region="usa", width=2)
STATE_ADDR = guest_address("crosswalk:usa:static:engine_state", region="usa", width=1)
PHASE_ADDR = guest_address("crosswalk:usa:static:scene_phase", region="usa", width=1)
EXIT_ADDR = guest_address("crosswalk:usa:static:exit_request", region="usa", width=1)
PAUSE_ADDR = guest_address("crosswalk:usa:static:pause_byte", region="usa", width=1)
TRANSITION_ADDR = guest_address("crosswalk:usa:static:scene_transition", region="usa", width=1)
SCRIPT_LOCK_ADDR = guest_address("crosswalk:usa:static:script_lock", region="usa", width=1)
SCRIPT_VM_ADDR = guest_address("research:vm_command_pc", region="usa", width=4)
SUBMODE_ADDR = guest_address("crosswalk:usa:static:gameplay_submode", region="usa", width=1)


def _guest_bytes(ram, addr, length):
    """Read canonical N64 byte order regardless of word swapping on PC."""
    return ram.read_guest(addr, length)


def _digest(payload: dict) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _encoded(data):
    return base64.b64encode(data).decode("ascii")


def _decoded(value, expected):
    try:
        data = base64.b64decode(value, validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("Malformed checkpoint base64") from exc
    if len(data) != expected:
        raise ValueError(f"Checkpoint region size {len(data)} differs from {expected}")
    return data


def _u32(data, offset):
    return int.from_bytes(data[offset:offset+4], "big", signed=False)


def _ensure_capture_safe(ram):
    s = ram.snapshot()
    if s["x"] is None or s["loading"] or not s["player_ptr"] or not s["task_ptr"]:
        raise ValueError("Checkpoint requires stable gameplay with a live player")
    if ram.u8(STATE_ADDR) != 0x0D or ram.u8(PHASE_ADDR) != 1:
        raise ValueError("Checkpoint unavailable outside ordinary gameplay")
    if ram.u8(EXIT_ADDR) or ram.u8(PAUSE_ADDR) or ram.u8(TRANSITION_ADDR):
        raise ValueError("Transition/pause/exit in progress; checkpoint rejected")
    if ram.u8(SCRIPT_LOCK_ADDR) or ram.u32(SCRIPT_VM_ADDR):
        raise ValueError("Script/event active; checkpoint rejected")
    return s


def capture_checkpoint(ram, name: str) -> dict:
    """Capture original-game logical progress; never copy the entire 8MB RAM.

    This includes save flags/inventory, resource live block, global unlocks,
    and the avatar's position and orientation. It cannot capture native host
    threads, GPU/audio, other running actors, or every volatile game variable.
    """
    before = _ensure_capture_safe(ram)
    map_id = ram.u16(MAP_ADDR)
    live = _guest_bytes(ram, LIVE_ADDR, LIVE_LEN)
    game_data = _guest_bytes(ram, GAMEDATA_ADDR, GAMEDATA_LEN)
    header = _guest_bytes(ram, HEADER_ADDR, HEADER_LEN)
    obj = before["player_ptr"]
    rotation = _guest_bytes(ram, obj + 0x14, 6)
    after = _ensure_capture_safe(ram)
    if (before["player_ptr"] != after["player_ptr"] or
            before["character"] != after["character"] or
            map_id != ram.u16(MAP_ADDR)):
        raise ValueError("Game scene/character changed during checkpoint capture")
    # Guard against a progress write while capturing. The live values are
    # validated for plausible ranges and require a stable duplicate read.
    if live != _guest_bytes(ram, LIVE_ADDR, LIVE_LEN) or game_data != _guest_bytes(ram, GAMEDATA_ADDR, GAMEDATA_LEN):
        raise ValueError("Game progression changed during checkpoint capture")
    max_hp, hp, ryo, lives = (_u32(live, o) for o in (8, 12, 16, 20))
    if not (0 < max_hp <= 127 and hp <= max_hp and 0 <= ryo <= 9999 and 0 <= lives <= 999):
        raise ValueError("Implausible original-game resource values; checkpoint refused")
    payload = {
        "format": FORMAT, "game": GAME, "name": name.strip() or "Practice checkpoint",
        "created": datetime.now(timezone.utc).isoformat(),
        "map_id": map_id, "character": before["character"],
        "position": [before[k] for k in ("x", "y", "z")],
        "rotation_b64": _encoded(rotation),
        "regions": {"live": _encoded(live), "gamedata": _encoded(game_data), "header": _encoded(header)},
        "summary": {"max_health": max_hp, "health": hp, "ryo": ryo, "lives": lives},
    }
    return {"payload": payload, "sha256": _digest(payload)}


def validate_checkpoint(checkpoint: dict) -> tuple[dict, dict[str, bytes]]:
    if not isinstance(checkpoint, dict) or not isinstance(checkpoint.get("payload"), dict):
        raise ValueError("Invalid checkpoint structure")
    p = checkpoint["payload"]
    if p.get("format") != FORMAT or p.get("game") != GAME:
        raise ValueError("Incorrect checkpoint format or game region")
    if checkpoint.get("sha256") != _digest(p):
        raise ValueError("Checkpoint checksum mismatch")
    if not isinstance(p.get("character"), int) or p["character"] not in range(4):
        raise ValueError("Invalid checkpoint character")
    if not isinstance(p.get("map_id"), int) or p["map_id"] not in range(65536):
        raise ValueError("Invalid checkpoint map")
    xyz = p.get("position")
    if not isinstance(xyz, list) or len(xyz) != 3 or any(not isinstance(x,(float,int)) or not -1e6<x<1e6 for x in xyz):
        raise ValueError("Invalid checkpoint position")
    reg = p.get("regions", {})
    data = {"live": _decoded(reg.get("live"), LIVE_LEN),
            "gamedata": _decoded(reg.get("gamedata"), GAMEDATA_LEN),
            "header": _decoded(reg.get("header"), HEADER_LEN),
            "rotation": _decoded(p.get("rotation_b64"), 6)}
    return p, data


def restore_checkpoint(ram, checkpoint: dict):
    """Experimental in-room restore; no native quicksave feature required.

    Restores original-game save flag blocks, live stats, global header flags,
    position and rotation. It does *not* recover overlay-owned actor state,
    physics/momentum, in-flight scripts, or a different room's live objects.
    """
    p, data = validate_checkpoint(checkpoint)
    before = _ensure_capture_safe(ram)
    if before["character"] != p["character"]:
        raise ValueError("Saved character differs; character-switch runtime is not reconstructed")
    if ram.u16(MAP_ADDR) != p["map_id"]:
        raise ValueError("Checkpoint map differs. Travel to that map before restoration")
    submode = ram.u8(SUBMODE_ADDR)
    if submode >= 4 or submode == 3:
        raise ValueError("Unsafe game submode; restoration refused")
    obj = before["player_ptr"]
    if not ram.is_ram_pointer(obj, 0x1A):
        raise ValueError("Player object unavailable")
    # The game stores a stale save mirror of the 0x30-byte live block at +0x64
    # until a save marshals it. On restoration, synchronize this to the live
    # block so the primary/shadow saved-state data agree.
    game_data = bytearray(data["gamedata"])
    game_data[0x64:0x94] = data["live"]
    locations = [
        (GAMEDATA_ADDR, bytes(game_data)),
        (SHADOW_ADDR, bytes(game_data)),
        (LIVE_ADDR, data["live"]),
        (HEADER_ADDR, data["header"]),
        (obj + 0x14, data["rotation"]),
    ]
    # Avoid mixed-axis writes: all coordinates written in one operation.
    import struct
    coords = b"".join(struct.pack(">f", float(v)) for v in p["position"])
    locations.append((obj + 0x08, coords))
    # Store all original values before first write; no rollback can make
    # concurrent writes atomic, but this can handle a failed partial operation.
    originals = [(addr, ram.read_guest(addr, len(value))) for addr, value in locations]
    try:
        _ensure_capture_safe(ram)
        if ram.u16(MAP_ADDR) != p["map_id"] or ram.snapshot()["player_ptr"] != obj:
            raise ValueError("Game advanced while preparing to restore")
        for addr, value in locations:
            ram.write_guest(addr, value)
        for addr, value in locations:
            if ram.read_guest(addr, len(value)) != value:
                raise OSError(f"Readback mismatch at 0x{addr:08X}")
    except Exception:
        # Best effort only; NEVER assume the game was actually paused.
        for addr, original in reversed(originals):
            try:
                ram.write_guest(addr, original)
            except Exception:
                pass
        raise
    return p["summary"]


def save_checkpoint_file(path: Path, checkpoints: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(checkpoints, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_checkpoint_file(path: Path):
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Checkpoint list must be a JSON array")
    for cp in data:
        validate_checkpoint(cp)
    return data

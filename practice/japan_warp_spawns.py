"""User-observed Japanese warp-point records; never infer JP spawns from USA.

Legacy per-Japanese-room position capture research, retained for inspecting
a game's live entrance record. The shared Scene Browser in v0.11.23 instead
uses the same original-USA ROM entrance atlas and selected entrance for both
regions. These optional saved positions DO NOT override the USA entrance
coordinates on a Japanese scene warp.

Records are user-specific metadata, never ROM bytes or save states. A captured
coordinate is evidence of a position, not proof of safe collision or a door.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import struct
import sys
import tempfile

from practice.entrances import Spawn
from practice.japanese_position import (
    JAPAN_OEDO_SOUTH_ENTRANCE, JAPAN_OEDO_SOUTH_SCENE,
    checked_japan_xyz, read_japan_position,
)
from practice.japanese_debug_warp import get_japan_debug_context, _normal_gameplay
from practice.japan_direct_scene_reload import JAPAN_PENDING_MAP

FORMAT = "goemon-japan-warp-spawns-v1"
MAX_FILE_BYTES = 160_000
MAX_SPAWNS = 600
# This source-backed Oedo South XYZ was user-observed in live Japanese play.
# The default heading and mode are still hypotheses, not JP-proven.
OEDO_EXPERIMENTAL_SPAWN = Spawn(
    JAPAN_OEDO_SOUTH_SCENE, JAPAN_OEDO_SOUTH_ENTRANCE,
    heading=0, mode=0x10, label="JP Oedo South XYZ; heading/mode unverified",
    entrance_id="jp:oedo-south:observed-xyz",
)

def registry_path():
    if sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA")
                    or (Path.home() / "AppData" / "Local"))
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME")
                    or (Path.home() / ".config"))
    return root / "GoemonSpeedrunTools" / "japan-warp-spawns.json"


def _parse_record(text, *, scene_key=None):
    if not isinstance(text, dict):
        raise ValueError("Invalid Japanese spawn record")
    scene = text.get("scene")
    if type(scene) is not int or not 0 < scene < 0x800:
        raise ValueError("Japanese spawn scene out of range")
    if scene_key is not None and scene_key != str(scene):
        raise ValueError("Japanese spawn scene key mismatch")
    if text.get("source") != "user-captured-japan":
        raise ValueError("Unrecognized Japanese spawn origin")
    mode = text.get("mode")
    heading = text.get("heading")
    position = text.get("position")
    if (not isinstance(position, list) or len(position) != 3
            or any(type(v) not in (int, float) for v in position)):
        raise ValueError("Invalid Japanese XYZ")
    if type(mode) is not int or type(heading) is not int:
        raise ValueError("Invalid Japanese heading/mode")
    if text.get("basis") not in ("native-pending", "xyz-only"):
        raise ValueError("Unknown Japanese heading/mode provenance")
    spawn = Spawn(
        scene, tuple(position), heading=heading, mode=mode,
        label=("User-captured Japanese position "
               f"({text['basis']} heading/mode)"),
        entrance_id=f"jp:capture:{scene:03X}",
    ).validate()
    return spawn


def load_japan_spawns(*, store=None):
    path = Path(store) if store is not None else registry_path()
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return {}
        doc = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(doc, dict) or doc.get("format") != FORMAT
                or not isinstance(doc.get("spawns"), dict)
                or len(doc["spawns"]) > MAX_SPAWNS):
            return {}
        return {
            int(key): _parse_record(value, scene_key=key)
            for key, value in doc["spawns"].items()
        }
    except (OSError, ValueError, TypeError, OverflowError, KeyError):
        return {}


def save_japan_spawn(spawn: Spawn, *, basis: str, store=None):
    """Write one *explicit* captured JP destination atomically, not a guess."""
    if basis not in ("native-pending", "xyz-only"):
        raise ValueError("Unexpected Japanese spawn source")
    spawn.validate()
    if not 0 < spawn.destination < 0x800:
        raise ValueError("Unknown Japanese scene")
    dest = Path(store) if store is not None else registry_path()
    existing = load_japan_spawns(store=dest)
    existing[spawn.destination] = spawn
    if len(existing) > MAX_SPAWNS:
        raise ValueError("Too many Japanese warp points")
    prior_records = {}
    try:
        if dest.stat().st_size <= MAX_FILE_BYTES:
            raw = json.loads(dest.read_text(encoding="utf-8"))
            if raw.get("format") == FORMAT and isinstance(raw.get("spawns"), dict):
                prior_records = raw["spawns"]
    except (OSError, ValueError, AttributeError):
        pass
    records = {}
    for scene, point in sorted(existing.items()):
        prior = prior_records.get(str(scene), {})
        previous_basis = (
            prior.get("basis") if isinstance(prior, dict)
            and prior.get("basis") in ("native-pending", "xyz-only")
            else "xyz-only")
        records[str(scene)] = dict(
            scene=scene, position=list(point.position),
            heading=point.heading, mode=point.mode,
            source="user-captured-japan",
            basis=basis if scene == spawn.destination else previous_basis,
        )
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=dest.parent, delete=False,
                prefix=f".{dest.name}.", suffix=".tmp") as stream:
            tmp = Path(stream.name)
            json.dump({"format": FORMAT, "spawns": records}, stream, indent=2)
            stream.write("\n")
        os.replace(tmp, dest)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
    return dest


def capture_current_japan_spawn(reader):
    """Capture *this* scene's Goemon XYZ only during stable Japanese gameplay.

    Preserve native mode/heading if the 12-byte pending block's scene and XYZ
    agree with the live Japanese float32 position. Otherwise use clearly
    labelled USA-derived mode/heading defaults, never call them proven.
    """
    context = get_japan_debug_context(reader)
    _normal_gameplay(context)
    if context[2] != 0:
        raise ValueError(
            "Capturing Japanese warp XYZ is currently limited to Goemon")
    xyz = checked_japan_xyz(read_japan_position(reader))
    if any(abs(v) > 32767 for v in xyz):
        raise ValueError("Live XYZ cannot fit signed native entrance coordinates")
    scene = context[1]
    heading, mode, basis = 0, 0x10, "xyz-only"
    try:
        raw = reader.read_guest(JAPAN_PENDING_MAP, 12)
        pending_scene, pending_mode, x, y, z, pending_heading = struct.unpack(
            ">HHhhhH", raw)
        if (pending_scene == scene
                and all(abs(a - b) <= 32 for a, b in
                        zip((x, y, z), xyz))):
            heading, mode, basis = pending_heading, pending_mode, "native-pending"
    except (OSError, ValueError, struct.error):
        pass
    if get_japan_debug_context(reader) != context:
        raise RuntimeError("Japanese scene changed during XYZ capture")
    if math.dist(xyz, read_japan_position(reader)) > 2:
        raise RuntimeError("Player moved during XYZ capture; retry while idle")
    spawn = Spawn(
        scene, xyz, heading=heading, mode=mode,
        label=("User-captured Japanese Goemon XYZ ("
               + ("native pending mode/heading)" if basis == "native-pending"
                  else "unverified mode/heading)")),
        entrance_id=f"jp:capture:{scene:03X}",
    ).validate()
    return spawn, basis


def destination_spawn(spawns, destination):
    """Never substitute USA-entrance records for a Japanese destination."""
    if destination in spawns:
        return spawns[destination]
    if destination == JAPAN_OEDO_SOUTH_SCENE:
        return OEDO_EXPERIMENTAL_SPAWN
    return None


def position_difference(expected, observed):
    """Report observed Japanese post-load XYZ without claiming collision proof."""
    if len(expected) != 3 or len(observed) != 3:
        raise ValueError("Expected three XYZ components")
    if not all(math.isfinite(v) for v in (*expected, *observed)):
        raise ValueError("Nonfinite Japanese spawn XYZ")
    delta = math.dist(expected, observed)
    return delta

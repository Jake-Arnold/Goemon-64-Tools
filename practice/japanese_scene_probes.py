"""Japanese NG5J scene/transition *candidate* probes. STRICTLY READ ONLY.

The +0x57F0 displacement is verified externally for two nearby debug
variables, NOT as a universal relocation. These ten addresses are individual
hypotheses derived from known USA globals; their meanings must be checked in
a live Japanese game before any scene/writing features are enabled.
"""
from __future__ import annotations

from dataclasses import dataclass
from practice.japanese_fields import JapanFieldReading

TCRF = "https://tcrf.net/Mystical_Ninja_Starring_Goemon_(Nintendo_64)"
GROUP = "Scene research (candidate)"


@dataclass(frozen=True)
class JapanSceneProbe:
    key: str
    label: str
    address: int
    width: int
    usa_reference: int
    group: str = GROUP
    source: str = TCRF

    def __post_init__(self):
        if self.address - self.usa_reference != 0x57F0:
            raise ValueError("Scene probe must retain its explicit USA-to-JP hypothesis")
        if self.width not in (1, 2, 4):
            raise ValueError("Invalid scene probe width")
        if not (0x80000000 <= self.address and self.address + self.width <= 0x80800000):
            raise ValueError("Scene probe outside RDRAM")


# Per-field hypotheses; the nearby JP 0x800CD284 engine/debug byte is
# independently documented and ALREADY present in JAPAN_FIELDS.
JAPAN_SCENE_PROBES = (
    JapanSceneProbe("scene_map", "Current scene ID (candidate)", 0x800CD2A2, 2, 0x800C7AB2),
    JapanSceneProbe("scene_phase", "Scene phase (candidate)", 0x800CD28E, 1, 0x800C7A9E),
    JapanSceneProbe("scene_submode", "Gameplay submode (candidate)", 0x800CD294, 1, 0x800C7AA4),
    JapanSceneProbe("scene_previous", "Previous scene ID (candidate)", 0x800CD2AC, 2, 0x800C7ABC),
    JapanSceneProbe("scene_pending", "Pending scene ID (candidate)", 0x800CD490, 2, 0x800C7CA0),
    JapanSceneProbe("scene_transition", "Transition flag (candidate)", 0x800CD2C6, 1, 0x800C7AD6),
    JapanSceneProbe("scene_exit", "Exit request (candidate)", 0x800CD28F, 1, 0x800C7A9F),
    JapanSceneProbe("scene_pause", "Pause flag (candidate)", 0x800CD2D6, 1, 0x800C7AE6),
    JapanSceneProbe("scene_character", "Character index (candidate)", 0x80161DCC, 4, 0x8015C5DC),
    JapanSceneProbe("scene_loading", "Loading word (candidate)", 0x80161DC4, 4, 0x8015C5D4),
)
assert len(set(x.key for x in JAPAN_SCENE_PROBES)) == len(JAPAN_SCENE_PROBES)
assert len(set(x.address for x in JAPAN_SCENE_PROBES)) == len(JAPAN_SCENE_PROBES)


def read_japan_scene_probes(rdram):
    """Return one result per probe; never write or infer a player pointer."""
    readings = {}
    for probe in JAPAN_SCENE_PROBES:
        try:
            data = rdram.read_guest(probe.address, probe.width)
            if len(data) != probe.width:
                raise OSError("short guest RAM read")
            val = int.from_bytes(data, "big")
            label = str(val)
            if probe.key in ("scene_map", "scene_previous", "scene_pending"):
                label = f"{val} / 0x{val:03X}"
            elif probe.key == "scene_character" and 0 <= val <= 3:
                label = ("Goemon", "Ebisumaru", "Sasuke", "Yae")[val] + f" ({val})"
            status = "UNVERIFIED: regional-offset hypothesis"
            if probe.key == "scene_map" and val > 0x800:
                status = "CHECK: out-of-range scene candidate"
            elif probe.key == "scene_character" and val > 3:
                status = "CHECK: unusual character candidate"
            readings[probe.key] = JapanFieldReading(label, data.hex().upper(), status)
        except (ValueError, OSError, PermissionError) as exc:
            readings[probe.key] = JapanFieldReading("—", "—", f"READ ERROR: {exc}")
    return readings


def compare_guest_readings(before, after, keys):
    """Calculate reproducible *raw-byte* changes; display strings can differ."""
    changes = []
    for key in keys:
        a, b = before.get(key), after.get(key)
        if a is None or b is None or a.raw == "—" or b.raw == "—":
            continue
        if a.raw != b.raw:
            changes.append((key, a.raw, b.raw))
    return tuple(changes)

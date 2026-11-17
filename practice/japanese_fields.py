"""Source-backed, *read-only* Japanese Goemon N64 field candidates.

Only explicit NG5J GameShark addresses and the published JP debug-state code
appear here. No blanket USA->JP RAM offset and no game-memory writes. The
published cheat meanings remain external evidence until checked during play.
"""
from __future__ import annotations

from dataclasses import dataclass
from practice.address_registry import guest_address

JP_CHEATS = "https://gamehacking.org/game/20438"
JP_DEBUG = "https://tcrf.net/Mystical_Ninja_Starring_Goemon_(Nintendo_64)"


@dataclass(frozen=True)
class JapanField:
    key: str
    label: str
    address: int
    width: int
    group: str
    kind: str = "unsigned"
    source: str = JP_CHEATS
    expected_max: int | None = None


def _field(key, label, address, width, group, kind="unsigned", maximum=None,
           source=JP_CHEATS):
    # Reject malformed caller input before consulting the registry; schema
    # tests must still detect invalid guest addresses for unknown field IDs.
    if not 0x80000000 <= address < 0x80800000 or address + width > 0x80800000:
        raise ValueError("JP field outside 8 MiB RDRAM")
    if width not in (1, 2, 4):
        raise ValueError("Unsupported JP read width")
    # All Japanese source-backed fields resolve their actual guest address
    # from the same authoritative catalogue as the shared Live Memory page.
    address = guest_address(
        "japanese:field:" + key, region="japan", width=width)
    if not 0x80000000 <= address < 0x80800000 or address + width > 0x80800000:
        raise ValueError("JP field outside 8 MiB RDRAM")
    if width not in (1, 2, 4):
        raise ValueError("Unsupported JP read width")
    return JapanField(key, label, address, width, group, kind, source, maximum)


_f = [
    _field("max_hp", "Maximum health (low byte)", 0x80161DD3, 1, "Vitals", maximum=127),
    _field("hp", "Current health (low byte)", 0x80161DD7, 1, "Vitals", maximum=127),
    _field("ryo", "Ryo", 0x80161DDA, 2, "Vitals", maximum=9999),
    _field("lives", "Lives (low byte)", 0x80161DDF, 1, "Vitals", maximum=99),
    _field("fish_riceballs", "Fish riceballs", 0x80161DE3, 1, "Vitals"),
    _field("helmet", "Helmet count / level", 0x80161DE7, 1, "Vitals"),
    _field("armour", "Armour count / level", 0x80161DEF, 1, "Vitals"),
    _field("sasuke_party", "Sasuke in party", 0x80161E97, 1, "Party", "flag"),
    _field("yae_party", "Yae in party", 0x80161E9B, 1, "Party", "flag"),
]

# The cheat's GameShark 50-type repeat writes four 8-bit values at +4 bytes.
# These slot names deliberately do not assume unconfirmed individual item IDs.
for prefix, name, first, kind in (
    ("weapon", "Weapon upgrade", 0x80161E9F, "level"),
    ("super_weapon", "Super weapon slot", 0x80161EAF, "flag"),
    ("sub_weapon", "Sub-weapon slot", 0x80161EC3, "flag"),
    ("jutsu", "Jutsu skill slot", 0x80161EDF, "flag"),
):
    for i in range(4):
        _f.append(_field(f"{prefix}_{i+1}", f"{name} {i+1}",
                         first + i * 4, 1, "Weapons and skills", kind))

_f.extend([
    _field("triton_shell", "Triton Shell", 0x80161EEF, 1, "Items", "flag"),
    _field("super_pass", "Super Pass", 0x80161EF3, 1, "Items", "flag"),
    _field("benkei_weakness", "Benkei's weakness", 0x80161EFF, 1, "Items", "flag"),
    _field("cucumber", "Kappa's Cucumber", 0x80161F07, 1, "Items", "flag"),
    _field("red_fish", "Red fish", 0x80161F0B, 1, "Items", maximum=8),
    _field("yellow_fish", "Yellow fish", 0x80161F0F, 1, "Items", maximum=5),
    _field("blue_fish", "Blue fish", 0x80161F13, 1, "Items", maximum=3),
    _field("world_map_access", "World map access", 0x80162063, 1, "World map", "flag"),
])
for i in range(4):
    _f.append(_field(f"treasure_{i+1}", f"Treasure slot {i+1}",
                     0x8016204B + 4*i, 1, "Items", "flag"))
for i in range(16):
    _f.append(_field(f"map_stop_{i+1}", f"World map stop {i+1}",
                     0x8016209F + 4*i, 1, "World map", "flag"))
for i in range(3):
    _f.append(_field(f"extra_mode_{i+1}", f"Bonus mode / song flag {i+1}",
                     0x8016240B + 4*i, 1, "Modes and engine", "flag"))
_f.extend([
    _field("total_time_raw", "Total time (raw counter)", 0x8016205C,
           4, "Modes and engine", "hex"),
    _field("native_debug_state", "Engine mode (debug = 10)", 0x800CD284,
           1, "Modes and engine", "unsigned", source=JP_DEBUG),
])

JAPAN_FIELDS = tuple(_f)
FIELD_GROUPS = tuple(dict.fromkeys(x.group for x in JAPAN_FIELDS))
assert len({x.key for x in JAPAN_FIELDS}) == len(JAPAN_FIELDS)
assert len({(x.address, x.width) for x in JAPAN_FIELDS}) == len(JAPAN_FIELDS)


@dataclass(frozen=True)
class JapanFieldReading:
    value: str
    raw: str
    status: str


def read_japan_field(rdram, field: JapanField) -> JapanFieldReading:
    """Read canonical guest bytes. Never invokes the host process writer."""
    try:
        data = rdram.read_guest(field.address, field.width)
        if len(data) != field.width:
            raise OSError("short guest RAM read")
        value = int.from_bytes(data, "big")
        if field.kind == "hex":
            display = f"0x{value:0{field.width * 2}X}"
        elif field.kind == "flag":
            display = "Yes (1)" if value == 1 else "No (0)" if value == 0 else str(value)
        elif field.kind == "level":
            display = f"{value} (cheat max=2)" if value == 2 else str(value)
        else:
            display = str(value)
        max_value = 1 if field.kind == "flag" else 2 if field.kind == "level" else field.expected_max
        status = "External lead" if max_value is None or value <= max_value else "CHECK: unusual value"
        return JapanFieldReading(display, data.hex().upper(), status)
    except (OSError, ValueError, PermissionError) as exc:
        return JapanFieldReading("—", "—", f"READ ERROR: {exc}")


def read_japan_fields(rdram):
    return {field.key: read_japan_field(rdram, field) for field in JAPAN_FIELDS}

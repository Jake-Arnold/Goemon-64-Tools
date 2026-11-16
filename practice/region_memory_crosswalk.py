"""Read-only USA -> Japan static-global and saved-event crosswalk.

A measured +0x57F0 displacement is evidence for *candidate* Japanese addresses,
not proof that all original globals, overlays or dynamic objects relocate.
The only promotion in this table is explicitly documented original gameplay
evidence. Nothing here is an editor, freeze target, or warp control.
"""
from __future__ import annotations

from dataclasses import dataclass

from practice.region_unlocks import JAPAN_UNLOCK_LEADS, REGION_DELTA
from practice.story_progress import CURATED_FLAGS, PLASMA_FLAGS
from practice.unlocks import UNLOCKS


@dataclass(frozen=True)
class CrossRegionField:
    key: str
    group: str
    label: str
    usa: int
    japan: int
    width: int = 1
    mask: int | None = None
    evidence: str = "offset-candidate"
    note: str = ""

    def __post_init__(self):
        for addr in (self.usa, self.japan):
            if not 0x80000000 <= addr < 0x80800000 or addr + self.width > 0x80800000:
                raise ValueError("Cross-region address outside 8 MiB guest RDRAM")
        if self.width not in (1, 2, 4):
            raise ValueError("Unsupported guest field width")
        if self.mask is not None and not (0 < self.mask < (1 << (8 * self.width))):
            raise ValueError("Invalid bit mask")

    @property
    def predicted_japan(self):
        return self.usa + REGION_DELTA

    @property
    def is_exception(self):
        return self.japan != self.predicted_japan


# Explicitly selected static globals. "user-confirmed" means the user reported
# checking the Japanese field in actual gameplay on 2026-11-16. "observed" is
# prior documented Japan runtime evidence, not an additional test this run.
# "candidate" is NOT safe to edit and may not even have the same semantics.
# The pause byte is retained solely as a NEGATIVE/UNRESOLVED research lead.
_STATIC = (
    ("engine_state", "Engine / scene", "Engine state", 0x800C7A94, 1, "observed", ""),
    ("current_scene", "Engine / scene", "Current scene", 0x800C7AB2, 2, "observed", ""),
    ("pending_scene", "Engine / scene", "Pending scene", 0x800C7CA0, 2, "observed", ""),
    ("previous_scene", "Engine / scene", "Previous scene", 0x800C7ABC, 2, "observed", ""),
    ("gameplay_submode", "Engine / scene", "Gameplay submode", 0x800C7AA4, 1, "user-confirmed", ""),
    ("scene_phase", "Engine / scene", "Scene phase", 0x800C7A9E, 1, "candidate", ""),
    ("scene_transition", "Engine / scene", "Scene transition byte", 0x800C7AD6, 1, "candidate", ""),
    ("exit_request", "Engine / scene", "Exit request", 0x800C7A9F, 1, "candidate", "Do not write as a warp"),
    ("scene_stage_offset", "Engine / scene", "Stage/category offset", 0x800C7AB4, 2, "candidate", ""),
    ("pause_byte", "Engine / scene", "Possible pause byte (NOT verified)", 0x800C7AE6, 1, "disputed", "User reports JP 0x800CD2D6 is probably not pause; do not promote"),
    ("script_lock", "Engine / scene", "Script interaction lock", 0x800C7AE9, 1, "candidate", ""),
    ("menu_pointer", "Engine / scene", "Original debug menu entry pointer", 0x800C7E60, 4, "candidate", "Context-specific; pointer may be stale"),
    ("character_index", "Gameplay / live", "Active character index", 0x8015C5DC, 4, "observed", "JP Goemon/Ebisumaru switching traced"),
    ("loading_word", "Gameplay / live", "Loading word", 0x8015C5D4, 4, "candidate", ""),
    ("weapon_index", "Gameplay / live", "Equipped weapon index", 0x8015C607, 1, "user-confirmed", "JP 01/02/03 tested across cycling"),
    ("map_overlay", "Gameplay / live", "Map overlay observed byte", 0x8015C574, 1, "user-confirmed", "Not a safe on/off toggle"),
    ("max_hp_low", "Gameplay / live", "Maximum HP low byte", 0x8015C5E3, 1, "external-jp", "Low byte of USA u32; JP GameShark byte"),
    ("hp_low", "Gameplay / live", "Current HP low byte", 0x8015C5E7, 1, "external-jp", "Low byte of USA u32; JP GameShark byte"),
    ("ryo_low16", "Gameplay / live", "Ryo low 16 bits", 0x8015C5EA, 2, "external-jp", "JP GameShark u16; USA full value is u32"),
    ("lives_low", "Gameplay / live", "Lives low byte", 0x8015C5EF, 1, "external-jp", "Low byte of USA u32"),
    ("item_slot_1", "Gameplay / live", "USA item slot 1 code (JP role unverified)", 0x8015C5F3, 1, "conflict", "JP code labels this offset fish riceballs; semantic parity unproven"),
    ("item_slot_2", "Gameplay / live", "USA item slot 2 code (JP role unverified)", 0x8015C5F7, 1, "candidate", ""),
    ("item_slot_2_quantity", "Gameplay / live", "USA item slot 2 quantity (JP role unverified)", 0x8015C5FB, 1, "candidate", ""),
    ("item_slot_3", "Gameplay / live", "USA item slot 3 code (JP role unverified)", 0x8015C5FF, 1, "candidate", ""),
    ("item_slot_3_quantity", "Gameplay / live", "USA item slot 3 quantity (JP role unverified)", 0x8015C603, 1, "candidate", ""),
    ("doll_quarters", "Gameplay / live", "Silver Fortune Doll quarter word (candidate)", 0x8015C704, 4, "candidate", "Only JP low-byte progress is separately verified"),
    ("doll_total", "Gameplay / live", "Total Fortune Dolls word (candidate)", 0x8015C708, 4, "candidate", ""),
)


def _build_crosswalk():
    fields = []
    for key, group, label, usa, width, evidence, note in _STATIC:
        fields.append(CrossRegionField(
            "static:" + key, group, label, usa, usa + REGION_DELTA,
            width=width, evidence=evidence, note=note))
    for item in UNLOCKS:
        lead = JAPAN_UNLOCK_LEADS[item.slug]
        evidence = "user-confirmed" if lead.user_verified else "candidate"
        fields.append(CrossRegionField(
            "unlock:" + item.slug, "Inventory / unlocks", item.label,
            item.address, lead.address, width=lead.width,
            mask=item.bit_mask, evidence=evidence,
            note=lead.evidence))
    for flag in CURATED_FLAGS:
        evidence = "user-confirmed" if flag.key == "benkei_encounter" else "candidate"
        fields.append(CrossRegionField(
            "event:" + flag.key, "Persistent story flags", flag.label,
            flag.address, flag.address + REGION_DELTA,
            mask=flag.mask, evidence=evidence,
            note=("USA: " + flag.evidence
                  + "; JP bit semantics still require independent checks"
                  if evidence != "user-confirmed" else
                  "User confirmed JP 0x80161DFC, bit 0x20 on 2026-11-16")))
    for flag in PLASMA_FLAGS:
        fields.append(CrossRegionField(
            "plasma:" + flag.key, "Plasma advice flags", flag.label,
            flag.address, flag.address + REGION_DELTA,
            mask=flag.mask, evidence="candidate",
            note="USA original script/annotation: " + flag.evidence))
    return tuple(fields)


CROSS_REGION_FIELDS = _build_crosswalk()
CROSS_REGION_BY_KEY = {field.key: field for field in CROSS_REGION_FIELDS}
assert len(CROSS_REGION_FIELDS) == len(CROSS_REGION_BY_KEY)
assert CROSS_REGION_BY_KEY["static:weapon_index"].japan == 0x80161DF7
assert CROSS_REGION_BY_KEY["static:gameplay_submode"].japan == 0x800CD294
assert CROSS_REGION_BY_KEY["static:map_overlay"].japan == 0x80161D64
assert CROSS_REGION_BY_KEY["event:benkei_encounter"].japan == 0x80161DFC
assert CROSS_REGION_BY_KEY["static:pause_byte"].evidence == "disputed"
assert CROSS_REGION_BY_KEY["unlock:sasuke_battery_1_collected"].evidence == "candidate"
assert CROSS_REGION_BY_KEY["unlock:snowflake"].japan == 0x80162057
assert CROSS_REGION_BY_KEY["unlock:snowflake"].is_exception


@dataclass(frozen=True)
class CrossRegionReading:
    value: str
    raw: str
    error: str = ""


def read_cross_region_field(guest, field: CrossRegionField) -> CrossRegionReading:
    """Read only; no host or guest memory writes, no inferred semantic promotion."""
    try:
        raw = guest.read_guest(field.japan, field.width)
        if len(raw) != field.width:
            raise OSError("short guest read")
        value = int.from_bytes(raw, "big")
        if field.mask is not None:
            display = f"0x{value:0{field.width * 2}X} (&0x{field.mask:X}: {bool(value & field.mask)})"
        else:
            display = f"0x{value:0{field.width * 2}X}"
        return CrossRegionReading(display, raw.hex().upper())
    except (OSError, ValueError, RuntimeError, PermissionError) as exc:
        return CrossRegionReading("—", "—", str(exc))


def read_cross_region_fields(guest):
    return {
        field.key: read_cross_region_field(guest, field)
        for field in CROSS_REGION_FIELDS
    }


def changed_cross_region_fields(before, after):
    """Return raw-byte changes only; differences never verify field meaning."""
    return tuple(
        (field, before[field.key].raw, after[field.key].raw)
        for field in CROSS_REGION_FIELDS
        if field.key in before and field.key in after
        and not before[field.key].error and not after[field.key].error
        and before[field.key].raw != after[field.key].raw
    )

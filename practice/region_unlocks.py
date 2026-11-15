"""Explicit USA/Japan unlock identities and direct Japanese one-byte writes.

The original 34 USA rows are the canonical UI. Japanese addresses are sourced
only by exact field identity; unknown rows never borrow USA pointers. Mapped
Japanese rows can be edited directly during development (unless --read-only).
No confirmation, party-only guard, character check or ROM re-probe per click.
"""
from __future__ import annotations

from practice.unlocks import UNLOCKS, normalize_unlock_value
from practice.japanese_fields import JAPAN_FIELDS

_FIELDS = {field.key: field for field in JAPAN_FIELDS}

_JAPAN_FIELD_KEYS = {
    "sasuke_in_party": "sasuke_party",
    "yae_in_party": "yae_party",
    "triton_shell": "triton_shell",
    "lord_s_pass": "super_pass",
    "achilles_heel": "benkei_weakness",
    "cucumber": "cucumber",
    "red_fish_count": "red_fish",
    "blue_fish_count": "blue_fish",
    "yellow_fish_count": "yellow_fish",
}

JAPAN_UNLOCK_LEADS = {
    slug: _FIELDS[key] for slug, key in _JAPAN_FIELD_KEYS.items()
}
assert len({item.slug for item in UNLOCKS}) == len(UNLOCKS)
assert set(JAPAN_UNLOCK_LEADS) <= {item.slug for item in UNLOCKS}
assert len({f.address for f in JAPAN_UNLOCK_LEADS.values()}) == len(JAPAN_UNLOCK_LEADS)
assert all(field.width == 1 for field in JAPAN_UNLOCK_LEADS.values())


def japan_unlock_lead(unlock):
    """Return the exact Japanese field, or None if the address is unknown."""
    return JAPAN_UNLOCK_LEADS.get(unlock.slug)


def write_japan_unlock(rdram, unlock, target):
    """Direct mapped one-byte write, including party Off/On and item counts.

    The caller provides an already-attached Japan-0 writable host RAM view.
    This intentionally does not use the older party-specific gated writer or
    USA write policies. Its readback is for reporting success, not a consent
    or scene-state gate. Neighbor bytes are preserved by Rdram.write_guest.
    """
    lead = japan_unlock_lead(unlock)
    if lead is None:
        raise ValueError(f'{unlock.label}: Japanese address unknown')
    if lead.width != 1:
        raise ValueError(f'{unlock.label}: unsupported Japanese field width')
    target = normalize_unlock_value(unlock, target)
    before = rdram.read_guest(lead.address, 1)
    if len(before) != 1:
        raise OSError('Short Japanese unlock read')
    raw = before[0]
    if unlock.bit_mask is not None:
        target = raw | unlock.bit_mask if target else raw & ~unlock.bit_mask
    after = bytes((target,))
    if before == after:
        return False
    rdram.write_guest(lead.address, after)
    if rdram.read_guest(lead.address, 1) != after:
        raise OSError(f'{unlock.label}: Japanese write readback mismatch')
    return True


def japan_unlock_all_targets():
    """Bulk targets cover only identified Japanese equivalents (7 currently)."""
    return tuple(
        (field, field.max_value if field.quantity else field.values[-1])
        for field in UNLOCKS if japan_unlock_lead(field) is not None
    )

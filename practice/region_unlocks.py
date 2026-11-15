"""Region-specific unlock read leads for the original 34-row USA interface.

The canonical labels, grouping and controls live in practice.unlocks.UNLOCKS.
Only exact Japanese source-backed field identities are listed here. A lead
is NOT write permission: currently only the user-verified Sasuke/Yae party
flags have a guarded Japanese writer. Never infer an address from a USA delta
or identify anonymous GameShark repeat slots as specific abilities.
"""
from __future__ import annotations

from practice.unlocks import UNLOCKS
from practice.japanese_fields import JAPAN_FIELDS
from practice.japanese_party_unlock import PARTY_FLAGS

_FIELDS = {field.key: field for field in JAPAN_FIELDS}

# Canonical USA Unlock.slug -> Japanese sourced field.key.
_JAPAN_FIELD_KEYS = {
    "sasuke_in_party": "sasuke_party",
    "yae_in_party": "yae_party",
    "triton_shell": "triton_shell",
    "cucumber": "cucumber",
    "red_fish_count": "red_fish",
    "blue_fish_count": "blue_fish",
    "yellow_fish_count": "yellow_fish",
}

JAPAN_UNLOCK_LEADS = {
    slug: _FIELDS[key] for slug, key in _JAPAN_FIELD_KEYS.items()
}

# The existing one-byte, ROM/PID-validated writer is intentionally the ONLY
# Japanese writer reachable from the shared Unlocks tab.
JAPAN_WRITABLE_PARTY = {
    "sasuke_in_party": 2,
    "yae_in_party": 3,
}

assert len({item.slug for item in UNLOCKS}) == len(UNLOCKS)
assert set(JAPAN_UNLOCK_LEADS) <= {item.slug for item in UNLOCKS}
assert len({f.address for f in JAPAN_UNLOCK_LEADS.values()}) == len(JAPAN_UNLOCK_LEADS)
for slug, character in JAPAN_WRITABLE_PARTY.items():
    field = JAPAN_UNLOCK_LEADS[slug]
    assert PARTY_FLAGS[character][1] == field.address and field.width == 1


def japan_unlock_lead(unlock):
    """Return a Japanese read definition or None; never a USA fallback."""
    return JAPAN_UNLOCK_LEADS.get(unlock.slug)

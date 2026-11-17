"""Japanese unlock crosswalk for the unchanged 34-row USA interface.

Sources:
  Japanese N64 GameShark: https://gamehacking.org/game/20438
  USA unlock definitions: practice.unlocks.UNLOCKS (never modified here)

Published Japanese 50000404 cheat codes prove the four +4-byte arrays, but
not their individual English names. The individual names here follow the USA
slot order and the consistently observed +0x57F0 region offset. They are
EXPERIMENTAL candidates, not proof of gameplay semantics.

The final four treasures are assigned provisionally in source order; the
Japanese fourth is 0x80162057, NOT the naive translation of USA 0x8015C866.
Sasuke's battery event bit remains speculative. The user live-confirmed
33/34 Japanese Unlocks on 15 November 2026, including all Miracle items,
weapons, abilities, Gold Key and Fortune Doll progress. Source provenance
is retained independently of the user-reported gameplay verification.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from practice.unlocks import UNLOCKS
from practice.address_registry import guest_address, normalize_unlock_value
from practice.japanese_fields import JAPAN_FIELDS, JP_CHEATS

REGION_DELTA = 0x57F0
_FIELDS = {field.key: field for field in JAPAN_FIELDS}
_USA = {field.slug: field for field in UNLOCKS}

# Types are deliberately machine-readable for later correction from live tests:
# named = existing source-identified mapping
# array = address proven by a Japanese array cheat; individual item inferred
# offset = inferred solely from the consistent USA->Japan inventory displacement
# guess = original bit/treasure-order hypothesis (historical provenance).
# user_verified separately records the user's gameplay result, not source strength.
@dataclass(frozen=True)
class JapanUnlockLead:
    address: int
    width: int
    confidence: str
    evidence: str
    user_verified: bool = False

    @property
    def bulk_eligible(self) -> bool:
        return self.user_verified


_NAMED = {
    'sasuke_in_party': 'sasuke_party',
    'yae_in_party': 'yae_party',
    'triton_shell': 'triton_shell',
    'lord_s_pass': 'super_pass',
    'achilles_heel': 'benkei_weakness',
    'cucumber': 'cucumber',
    'red_fish_count': 'red_fish',
    'blue_fish_count': 'blue_fish',
    'yellow_fish_count': 'yellow_fish',
}

# Source-backed four-slot Japanese arrays, matched by their USA order:
# 0x80161E9F (upgrades), 0x80161EAF (super weapons),
# 0x80161EC3 (subweapons), 0x80161EDF (jutsu abilities).
_ARRAY = {
    'goemon_pipe_upgrade': 'weapon_1',
    'ebisumaru_hammer_upgrade': 'weapon_2',
    'sasuke_kunai_upgrade': 'weapon_3',
    'yae_katana_upgrade': 'weapon_4',
    'chain_pipe': 'super_weapon_1',
    'meat_saw_hammer': 'super_weapon_2',
    'fire_cracker_bomb': 'super_weapon_3',
    'flute': 'super_weapon_4',
    'windup_camera': 'sub_weapon_1',
    'ice_kunai': 'sub_weapon_2',
    'bazooka': 'sub_weapon_3',
    'medal_of_flames': 'sub_weapon_4',
    'sudden_impact': 'jutsu_1',
    'mini_ebisumaru': 'jutsu_2',
    'super_jump': 'jutsu_3',
    'magic_mermaid': 'jutsu_4',
}

# Four more scalar candidates using the same delta, no per-item JP cheat.
_OFFSET = {
    'goemon_in_party': 'party slot immediately before Sasuke/Yae',
    'ebisumaru_in_party': 'party slot immediately before Sasuke/Yae',
    'gold_key': 'Gold Key before Cucumber',
    'silver_fortune_doll_progress': 'inventory progress byte after Super Pass',
}

# Original research hypotheses retained for traceability: four treasure
# slots are now gameplay-verified, while the battery flag remains unverified.
_GUESSES = {
    'sasuke_battery_1_collected': (
        0x80161DF9,
        'unverified USA+0x57F0 event byte; 0x20 bit mask inherited from USA'),
    'star': (_FIELDS['treasure_1'].address, 'treasure slot 1; identity guessed'),
    'moon': (_FIELDS['treasure_2'].address, 'treasure slot 2; identity guessed'),
    'flower': (_FIELDS['treasure_3'].address, 'treasure slot 3; identity guessed'),
    'snowflake': (_FIELDS['treasure_4'].address,
                  'treasure slot 4; identity guessed; USA byte alignment differs'),
}

JAPAN_UNLOCK_LEADS: dict[str, JapanUnlockLead] = {}
for slug, key in _NAMED.items():
    field = _FIELDS[key]
    JAPAN_UNLOCK_LEADS[slug] = JapanUnlockLead(
        field.address, field.width, 'named',
        f'Japanese individually named cheat: {key}; {JP_CHEATS}')

for slug, key in _ARRAY.items():
    field = _FIELDS[key]
    JAPAN_UNLOCK_LEADS[slug] = JapanUnlockLead(
        field.address, field.width, 'array',
        f'Japanese 4-slot GameShark repeat at +4; {key}; '
        f'USA+0x{REGION_DELTA:X} individual identity inferred; {JP_CHEATS}')

for slug, evidence in _OFFSET.items():
    item = _USA[slug]
    JAPAN_UNLOCK_LEADS[slug] = JapanUnlockLead(
        item.address + REGION_DELTA, 1, 'offset',
        f'USA+0x{REGION_DELTA:X} address candidate: {evidence}')

for slug, (address, evidence) in _GUESSES.items():
    JAPAN_UNLOCK_LEADS[slug] = JapanUnlockLead(
        address, 1, 'guess', evidence)

# The canonical registry owns every Japanese item address. Historical
# sources above retain evidence and slot labels, not location authority.
for _slug, _lead in tuple(JAPAN_UNLOCK_LEADS.items()):
    JAPAN_UNLOCK_LEADS[_slug] = replace(
        _lead,
        address=guest_address(
            'crosswalk:japan:unlock:' + _slug,
            region='japan', width=_lead.width))

# 15 Nov 2026 live gameplay report: only Sasuke battery 1 remains unverified.
# Assert the historical 34-row size: future new fields cannot inherit this
# confirmation merely by being added to the original USA Unlocks table.
JAPAN_LIVE_VERIFIED_SLUGS = frozenset(
    item.slug for item in UNLOCKS
    if item.slug != 'sasuke_battery_1_collected'
)
assert len(JAPAN_LIVE_VERIFIED_SLUGS) == 33
for slug in JAPAN_LIVE_VERIFIED_SLUGS:
    JAPAN_UNLOCK_LEADS[slug] = replace(
        JAPAN_UNLOCK_LEADS[slug], user_verified=True)

assert len(UNLOCKS) == 34
assert len(JAPAN_UNLOCK_LEADS) == len(UNLOCKS)
assert set(JAPAN_UNLOCK_LEADS) == set(_USA)
assert len({lead.address for lead in JAPAN_UNLOCK_LEADS.values()}) == len(UNLOCKS)
assert all(lead.width == 1 for lead in JAPAN_UNLOCK_LEADS.values())
assert all(
    JAPAN_UNLOCK_LEADS[slug].address == _USA[slug].address + REGION_DELTA
    for slug in (*_NAMED, *_ARRAY, *_OFFSET)
)
assert JAPAN_UNLOCK_LEADS['bazooka'].address == 0x80161ECB
assert JAPAN_UNLOCK_LEADS['medal_of_flames'].address == 0x80161ECF
assert sum(item.user_verified for item in JAPAN_UNLOCK_LEADS.values()) == 33
assert not JAPAN_UNLOCK_LEADS['sasuke_battery_1_collected'].user_verified


def japan_unlock_lead(unlock):
    """Return an address with provenance, or None for an unmapped future row."""
    return JAPAN_UNLOCK_LEADS.get(unlock.slug)


def japan_unlock_wire_value(unlock, target):
    """Convert the existing USA-labelled button value to Japan guest bytes.

    USA Chain Pipe uses On=02; Japanese super-weapon cheat uses On=01.
    This translation never changes practice.unlocks or the USA UI values.
    """
    target = normalize_unlock_value(unlock, target)
    if unlock.slug == 'chain_pipe' and target == 2:
        return 1
    return target


def japan_unlock_display_value(unlock, raw):
    """Translate Japan guest byte for selecting the original USA UI control."""
    if unlock.bit_mask is not None:
        return int(bool(raw & unlock.bit_mask))
    if unlock.slug == 'chain_pipe' and raw in (1, 2):
        return 2
    return raw


def write_japan_unlock(rdram, unlock, target):
    """Immediate single-byte experimental edit of a named or guessed JP row."""
    lead = japan_unlock_lead(unlock)
    if lead is None:
        raise ValueError(f'{unlock.label}: Japanese address unknown')
    if lead.width != 1:
        raise ValueError(f'{unlock.label}: unsupported Japanese field width')
    target = japan_unlock_wire_value(unlock, target)
    before = rdram.read_guest(lead.address, 1)
    if len(before) != 1:
        raise OSError('Short Japanese unlock read')
    if unlock.bit_mask is not None:
        raw = before[0]
        target = raw | unlock.bit_mask if target else raw & ~unlock.bit_mask
    after = bytes((target,))
    if before == after:
        return False
    rdram.write_guest(lead.address, after)
    if rdram.read_guest(lead.address, 1) != after:
        raise OSError(f'{unlock.label}: Japanese write readback mismatch')
    return True


def japan_unlock_all_targets(*, include_speculative=False):
    """Unlock all 33 user-tested Japanese entries; skip battery only by default."""
    return tuple(
        (item, item.max_value if item.quantity else item.values[-1])
        for item in UNLOCKS
        if (lead := japan_unlock_lead(item)) is not None
        and (include_speculative or lead.bulk_eligible)
    )

"""Original N64 guest-RAM unlocks and upgrade levels, from known US mappings.

These are scalar flags, not atomic bitfields. Binary records use 00/01 except
Chain Pipe, whose documented acquired value is 02. Base weapon upgrades are
levels 00/01/02, not booleans. Values remain provisional until game-UI tested.
"""
from __future__ import annotations
from dataclasses import dataclass
from practice.inspector import INVENTORY
from practice.hex_edit import checked_write, get_policy
from practice.address_registry import guest_address


@dataclass(frozen=True)
class Unlock:
    label: str
    address: int | None
    group: str
    values: tuple[int, ...] = (0, 1)
    levels: tuple[str, ...] = ('Off', 'On')
    quantity: bool = False
    max_value: int | None = None
    bit_mask: int | None = None  # Packed event flag (logical values 0/1).

    @property
    def slug(self) -> str:
        import re
        return re.sub(r'[^a-z0-9]+', '_', self.label.lower()).strip('_')

    def __post_init__(self):
        # There is no address literal in the 34 UI definitions. The reviewed
        # registry owns addresses; the dataclass retains item-specific values.
        try:
            canonical = guest_address(
                'unlock:usa:' + self.slug, region='usa', width=1)
        except KeyError:
            if self.address is not None:
                # Tool/test-created unknown fields are allowed as objects but
                # never inherit a mapping or writer from the built-in table.
                return
            raise
        if self.address is not None and self.address != canonical:
            raise ValueError('Unlock address disagrees with canonical registry')
        object.__setattr__(self, 'address', canonical)


UNLOCKS = (
    Unlock('Goemon in party', None, 'Party'),
    Unlock('Ebisumaru in party', None, 'Party'),
    Unlock('Sasuke in party', None, 'Party'),
    Unlock('Yae in party', None, 'Party'),
    Unlock('Goemon pipe upgrade', None, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Ebisumaru hammer upgrade', None, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Sasuke kunai upgrade', None, 'Weapon upgrades', (0,1,2), ('Normal', 'Double', 'Gold')),
    Unlock('Yae katana upgrade', None, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Chain Pipe', None, 'Weapons', (0,2), ('Off', 'On')),
    Unlock('Meat Saw Hammer', None, 'Weapons'),
    Unlock('Fire Cracker Bomb', None, 'Weapons'),
    Unlock('Flute', None, 'Weapons'),
    Unlock('Windup Camera', None, 'Weapons'),
    Unlock('Ice Kunai', None, 'Weapons'),
    Unlock('Bazooka', None, 'Weapons'),
    Unlock('Medal of Flames', None, 'Abilities'),
    Unlock('Sudden Impact', None, 'Abilities'),
    Unlock('Mini Ebisumaru', None, 'Abilities'),
    Unlock('Super Jump', None, 'Abilities'),
    Unlock('Magic Mermaid', None, 'Abilities'),
    Unlock('Triton Shell', None, 'Items and keys'),
    Unlock('Gold Key', None, 'Items and keys'),
    Unlock('Cucumber', None, 'Items and keys'),
    Unlock("Lord's Pass", None, 'Items and keys'),
    Unlock('Silver Fortune Doll progress', None, 'Items and keys', (0,1,2,3,4), ('0/4','1/4','1/2','3/4','4/4 (display)')),
    Unlock('Sasuke battery 1 collected', None, 'Items and keys', bit_mask=0x20),
    Unlock("Achilles' Heel", None, 'Items and keys'),
    Unlock('Red fish count', None, 'Fish counts', quantity=True, max_value=8),
    Unlock('Blue fish count', None, 'Fish counts', quantity=True, max_value=3),
    Unlock('Yellow fish count', None, 'Fish counts', quantity=True, max_value=5),
    Unlock('Star', None, 'Miracle items'),
    Unlock('Moon', None, 'Miracle items'),
    Unlock('Flower', None, 'Miracle items'),
    Unlock('Snowflake', None, 'Miracle items'),
)

GROUPS = ('Party', 'Weapon upgrades', 'Weapons', 'Abilities', 'Items and keys', 'Fish counts', 'Miracle items')
BY_ADDRESS = {u.address: u for u in UNLOCKS}


def validate_unlocks() -> None:
    """Reject silent mapping drift or invalid toggle values at import time."""
    mapping = {addr: (width, maximum) for _, addr, width, maximum, _ in INVENTORY}
    assert len(BY_ADDRESS) == len(UNLOCKS), 'Duplicate unlock address'
    for unlock in UNLOCKS:
        assert unlock.address in mapping, f'Unmapped unlock {unlock.label}'
        assert mapping[unlock.address][0] == 1, f'Not a byte flag: {unlock.label}'
        assert all(0 <= val <= mapping[unlock.address][1] for val in unlock.values)
        assert len(unlock.values) == len(unlock.levels)
        if unlock.bit_mask is not None:
            assert 0 < unlock.bit_mask <= 255 and unlock.bit_mask.bit_count() == 1
            assert not unlock.quantity and unlock.values == (0, 1)
        if unlock.quantity:
            assert mapping[unlock.address][1] == 255
            if unlock.max_value is not None:
                assert 0 <= unlock.max_value <= 255
        assert get_policy(unlock.address) is not None


def normalize_unlock_value(unlock: Unlock, target: int) -> int:
    if not (0 <= target <= 255):
        raise ValueError(f'Unsupported value 0x{target:02X} for {unlock.label}')
    if unlock.quantity:
        if unlock.max_value is not None:
            return min(target, unlock.max_value)
        return target
    if target not in unlock.values:
        raise ValueError(f'Unsupported value 0x{target:02X} for {unlock.label}')
    return target


def read_unlock(ram, unlock: Unlock) -> int:
    raw = ram.read_guest(unlock.address, 1)[0]
    return int(bool(raw & unlock.bit_mask)) if unlock.bit_mask is not None else raw


def write_unlock(ram, unlock: Unlock, target: int) -> bool:
    """Immediate single-byte toggle, checked against current RAM and read back.

    No dialog, no checkpoint and no write to the separate saved-data mirror.
    Do not write via u32: these values live in the last byte of aligned words.
    Quantity-style fields can optionally clamp to a game-validated maximum.
    """
    target = normalize_unlock_value(unlock, target)
    before = ram.read_guest(unlock.address, 1)
    if unlock.bit_mask is not None:
        raw = before[0]
        target = (raw | unlock.bit_mask) if target else (raw & ~unlock.bit_mask)
    return checked_write(ram, unlock.address, before, bytes((target,)))


def unlock_all_known(ram):
    """One-shot mapped maximums, not story flags; partial writes remain on error."""
    from practice.checkpoints import _ensure_capture_safe
    _ensure_capture_safe(ram)
    changed = 0
    for field in UNLOCKS:
        _ensure_capture_safe(ram)
        target = field.max_value if field.quantity else field.values[-1]
        if target is None:
            raise ValueError('No validated maximum for ' + field.label)
        if write_unlock(ram, field, target):
            changed += 1
    return changed, len(UNLOCKS)


validate_unlocks()

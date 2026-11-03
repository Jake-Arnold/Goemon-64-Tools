"""Original N64 guest-RAM unlocks and upgrade levels, from known US mappings.

These are scalar flags, not atomic bitfields. Binary records use 00/01 except
Chain Pipe, whose documented acquired value is 02. Base weapon upgrades are
levels 00/01/02, not booleans. Values remain provisional until game-UI tested.
"""
from __future__ import annotations
from dataclasses import dataclass
from practice.inspector import INVENTORY
from practice.hex_edit import checked_write, get_policy


@dataclass(frozen=True)
class Unlock:
    label: str
    address: int
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


UNLOCKS = (
    Unlock('Goemon in party', 0x8015C69F, 'Party'),
    Unlock('Ebisumaru in party', 0x8015C6A3, 'Party'),
    Unlock('Sasuke in party', 0x8015C6A7, 'Party'),
    Unlock('Yae in party', 0x8015C6AB, 'Party'),
    Unlock('Goemon pipe upgrade', 0x8015C6AF, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Ebisumaru hammer upgrade', 0x8015C6B3, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Sasuke kunai upgrade', 0x8015C6B7, 'Weapon upgrades', (0,1,2), ('Normal', 'Double', 'Gold')),
    Unlock('Yae katana upgrade', 0x8015C6BB, 'Weapon upgrades', (0,1,2), ('Normal', 'Silver', 'Gold')),
    Unlock('Chain Pipe', 0x8015C6BF, 'Weapons', (0,2), ('Off', 'On')),
    Unlock('Meat Saw Hammer', 0x8015C6C3, 'Weapons'),
    Unlock('Fire Cracker Bomb', 0x8015C6C7, 'Weapons'),
    Unlock('Flute', 0x8015C6CB, 'Weapons'),
    Unlock('Windup Camera', 0x8015C6D3, 'Weapons'),
    Unlock('Ice Kunai', 0x8015C6D7, 'Weapons'),
    Unlock('Bazooka', 0x8015C6DB, 'Weapons'),
    Unlock('Medal of Flames', 0x8015C6DF, 'Abilities'),
    Unlock('Sudden Impact', 0x8015C6EF, 'Abilities'),
    Unlock('Mini Ebisumaru', 0x8015C6F3, 'Abilities'),
    Unlock('Super Jump', 0x8015C6F7, 'Abilities'),
    Unlock('Magic Mermaid', 0x8015C6FB, 'Abilities'),
    Unlock('Triton Shell', 0x8015C6FF, 'Items and keys'),
    Unlock('Gold Key', 0x8015C713, 'Items and keys'),
    Unlock('Cucumber', 0x8015C717, 'Items and keys'),
    Unlock("Lord's Pass", 0x8015C703, 'Items and keys'),
    Unlock('Silver Fortune Doll progress', 0x8015C707, 'Items and keys', (0,1,2,3,4), ('0/4','1/4','1/2','3/4','4/4 (display)')),
    Unlock('Sasuke battery 1 collected', 0x8015C609, 'Items and keys', bit_mask=0x20),
    Unlock("Achilles' Heel", 0x8015C70F, 'Items and keys'),
    Unlock('Red fish count', 0x8015C71B, 'Fish counts', quantity=True, max_value=8),
    Unlock('Blue fish count', 0x8015C723, 'Fish counts', quantity=True, max_value=3),
    Unlock('Yellow fish count', 0x8015C71F, 'Fish counts', quantity=True, max_value=5),
    Unlock('Star', 0x8015C85B, 'Miracle items'),
    Unlock('Moon', 0x8015C85F, 'Miracle items'),
    Unlock('Flower', 0x8015C863, 'Miracle items'),
    Unlock('Snowflake', 0x8015C866, 'Miracle items'),
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


validate_unlocks()

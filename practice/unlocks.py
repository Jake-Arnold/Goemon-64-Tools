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
    Unlock('Cucumber (tentative; formerly Blue Sausage)', 0x8015C717, 'Items and keys'),
    Unlock('Brown item (Achilles Heel? candidate)', 0x8015C703, 'Items and keys'),
    Unlock('Silver Fortune Doll? (candidate)', 0x8015C707, 'Items and keys'),
    Unlock('Sasuke battery? (candidate)', 0x8015C70B, 'Items and keys'),
    Unlock('Round brown item (Achilles Heel? candidate)', 0x8015C70F, 'Items and keys'),
    Unlock('Red fish count', 0x8015C71B, 'Fish counts', quantity=True),
    Unlock('Yellow fish count', 0x8015C71F, 'Fish counts', quantity=True),
    Unlock('Blue fish count', 0x8015C723, 'Fish counts', quantity=True),
    Unlock('Miracle item 1 (unidentified)', 0x8015C85B, 'Miracle items'),
    Unlock('Miracle item 2 (unidentified)', 0x8015C85F, 'Miracle items'),
    Unlock('Miracle item 3 (unidentified)', 0x8015C863, 'Miracle items'),
    Unlock('Miracle item 4 (unidentified)', 0x8015C866, 'Miracle items'),
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
        if unlock.quantity:
            assert mapping[unlock.address][1] == 255
        assert get_policy(unlock.address) is not None


def read_unlock(ram, unlock: Unlock) -> int:
    return ram.read_guest(unlock.address, 1)[0]


def write_unlock(ram, unlock: Unlock, target: int) -> bool:
    """Immediate single-byte toggle, checked against current RAM and read back.

    No dialog, no checkpoint and no write to the separate saved-data mirror.
    Do not write via u32: these values live in the last byte of aligned words.
    """
    if not (0 <= target <= 255) or (not unlock.quantity and target not in unlock.values):
        raise ValueError(f'Unsupported value 0x{target:02X} for {unlock.label}')
    before = ram.read_guest(unlock.address, 1)
    return checked_write(ram, unlock.address, before, bytes((target,)))


validate_unlocks()

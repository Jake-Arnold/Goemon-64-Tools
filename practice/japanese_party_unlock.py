"""Opt-in Japan-0 party unlocks for native character-switch research.

These are the ONLY Japanese guest writes exposed by this module. Do not write
the character-index global: changing it bypasses actor/task/model rebuilding.
The tool's caller must use a short-lived writable PID handle, verify the ROM
signatures at the already-discovered host RDRAM base, and obtain user consent.
"""
from __future__ import annotations

from dataclasses import dataclass

CHARACTER_INDEX_ADDR = 0x80161DCC
SCENE_ID_ADDR = 0x800CD2A2
PARTY_FLAGS = {
    2: ("Sasuke", 0x80161E97),
    3: ("Yae", 0x80161E9B),
}


@dataclass(frozen=True)
class PartyUnlockResult:
    character: int
    label: str
    address: int
    before: bytes
    after: bytes
    changed: bool


def unlock_japan_party_member(rdram, character: int) -> PartyUnlockResult:
    """Unlock one absent party member through its NG5J low-byte flag.

    Guest words are big-endian. The flag byte is the last byte in the
    four-byte party word; writing the whole word is disallowed. The caller
    provides a separate, ROM-validated, short-lived writable Rdram handle.

    Refuses non-gameplay screens, already-selected/unknown characters, unusual
    party entries and concurrent changes. Does not send C-Down or write 0x80161DCC.
    """
    if type(character) is not int or character not in PARTY_FLAGS:
        raise ValueError("Only Sasuke (2) or Yae (3) party unlock is supported")
    name, address = PARTY_FLAGS[character]
    if address & 3 != 3:
        raise ValueError("Party flag must be the low byte of a 4-byte entry")

    active = int.from_bytes(rdram.read_guest(CHARACTER_INDEX_ADDR, 4), "big")
    if active not in (0, 1):
        raise RuntimeError(
            "Test only while playing normally as Goemon or Ebisumaru; "
            f"current character index is {active}"
        )
    scene = int.from_bytes(rdram.read_guest(SCENE_ID_ADDR, 2), "big")
    if not 0 < scene < 0x800:
        raise RuntimeError(f"Not in a validated gameplay scene: 0x{scene:X}")

    word_start = address - 3
    before = rdram.read_guest(word_start, 4)
    if before == b"\x00\x00\x00\x01":
        return PartyUnlockResult(character, name, address, before, before, False)
    if before != b"\x00\x00\x00\x00":
        raise RuntimeError(
            f"{name} party word is {before.hex()}; expected 00000000 or 00000001. "
            "No write performed."
        )
    if rdram.read_guest(word_start, 4) != before:
        raise RuntimeError("Party state changed during validation; no write performed")
    if int.from_bytes(rdram.read_guest(CHARACTER_INDEX_ADDR, 4), "big") != active:
        raise RuntimeError("Active character changed during validation; no write performed")
    if int.from_bytes(rdram.read_guest(SCENE_ID_ADDR, 2), "big") != scene:
        raise RuntimeError("Scene changed during validation; no write performed")

    # One byte only. The shared Rdram accessor preserves other bytes in a
    # word-swapped mapping; a concurrent game write could still race with it.
    rdram.write_guest(address, b"\x01")
    after = rdram.read_guest(word_start, 4)
    if after != b"\x00\x00\x00\x01":
        raise RuntimeError(
            f"{name} write did not verify: expected 00000001, got {after.hex()}. "
            "Inspect the game before attempting another write."
        )
    return PartyUnlockResult(character, name, address, before, after, True)

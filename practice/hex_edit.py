"""Guarded editing of fixed, known N64 guest scalar fields.

The experimental scene warp MUST NOT be implemented using a plain pending-map
write plus exit flag; that sequence returns to the title screen. This module
edits only explicitly named fields, checks old bytes, and verifies readback.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import re
import struct
from practice.inspector import INVENTORY

@dataclass(frozen=True)
class HexPolicy:
    width: int
    advanced: bool = False
    max_value: int | None = None
    note: str = ''

# Safe-ish resources. Provisional inventory values remain labelled as such.
POLICIES = {
    0x8015C5E0:HexPolicy(4,max_value=127,note='Maximum health; positive values only'),
    0x8015C5E4:HexPolicy(4,max_value=127,note='Current health'),
    0x8015C5E8:HexPolicy(4,max_value=9999,note='Ryo'),
    0x8015C5EC:HexPolicy(4,max_value=99,note='Lives'),
}
for _name,_addr,_width,_max,_hint in INVENTORY:
    POLICIES[_addr] = HexPolicy(_width,max_value=_max,
        note=('PACKED progression byte: preserve other bits; ' if _addr==0x8015C609 else 'Inventory/party field: ')+_hint)

# Addresses that can desynchronise game state, crash the game, or exit to title.
ENGINE_FIELDS = {
    0x800C7A94:(1,'Top-level game state; never a warp shortcut'),
    0x800C7A9E:(1,'Inner game phase'),
    0x800C7A9F:(1,'Exit request; setting to 1 previously returned to title'),
    0x800C7AA4:(1,'Native category while state 10, gameplay submode otherwise'),
    0x800C7AB2:(2,'Current/selected absolute map; a write is not a load'),
    0x800C7AB4:(2,'Stage offset within native menu category'),
    0x800C7ABC:(2,'Previous loaded map'),
    0x800C7CA0:(2,'Pending destination; alone does not trigger scene loading'),
    0x800C7E60:(4,'Menu-entry pointer; arbitrary writes can crash'),
    0x8015C5D4:(4,'Loading flag'),
    0x8015C5DC:(4,'Active character; bypasses model/actor loader'),
    0x8015C607:(1,'Equipped weapon index: 1–3 normal for every character; other values select unintended assets'),
}
for _addr,(_width,_note) in ENGINE_FIELDS.items():
    POLICIES[_addr] = HexPolicy(_width,advanced=True,note=_note)

# Event VM lock is a four-byte game-state bitfield.
from practice.checkpoints import SCRIPT_VM_ADDR
POLICIES[SCRIPT_VM_ADDR] = HexPolicy(4,advanced=True,note='Event/script VM lock; may corrupt cutscene logic')


def parse_hex(text: str, width: int) -> bytes:
    """Canonical big-endian N64 hex, with an optional 0x prefix."""
    text=text.strip()
    if text.lower().startswith('0x'):text=text[2:]
    if not text or len(text)>width*2 or not re.fullmatch(r'[0-9a-fA-F]+',text):
        raise ValueError(f'Enter 1 to {width*2} hexadecimal digits (optional 0x prefix)')
    return int(text,16).to_bytes(width,'big')


def get_policy(address: int):
    return POLICIES.get(address)


def watch_scalar_width(watch, definitions, *, region):
    """Shared read width only; this never authorizes a memory write."""
    if region not in ('usa', 'japan'):
        raise ValueError('Select USA or Japan first')
    if watch.addr is None:
        raise ValueError('Selected watch has no fixed guest address')
    spec = next((item for item in definitions if item.row_name == watch.name), None)
    policy = get_policy(watch.addr) if region == 'usa' else None
    raw = watch.raw.removeprefix('0x').removeprefix('0X').strip()
    width = (spec.width if spec is not None else policy.width if policy is not None
             else len(raw) // 2 if len(raw) in (2, 4, 8, 16)
             and re.fullmatch(r'[0-9a-fA-F]+', raw) else 0)
    if width not in (1, 2, 4, 8):
        raise ValueError('No supported scalar width for this watch; use a typed custom watch')
    return width


def checked_write(ram, address: int, expected: bytes, new: bytes, *, allow_advanced=False, raw_override=False):
    """Single compare-before-write with post-write verification. No auto retry.

    This cannot be atomic relative to the game thread, so never advertise it as
    a replacement for a properly patched loader. Blocks transient state 0..9.
    """
    if raw_override:
        if not allow_advanced:
            raise PermissionError('Raw hex overrides require write permission')
        width=len(new)
        if width not in (1, 2, 4, 8) or len(expected)!=width:
            raise ValueError('Raw writes must be 1, 2, 4, or 8 bytes')
        if not (0x80000000 <= address and address+width <= 0x80800000):
            raise ValueError('Address is outside 8 MiB of N64 guest RDRAM')
        current=ram.read_guest(address,width)
        if current!=expected:
            raise RuntimeError('Memory changed before write; retry')
        if new==expected:return False
        ram.write_guest(address,new)
        if ram.read_guest(address,width)!=new:
            raise OSError('Raw write readback mismatch')
        return True
    policy=get_policy(address)
    if policy is None: raise ValueError(f'No approved field at 0x{address:08X}')
    if policy.advanced and not allow_advanced:
        raise PermissionError('Engine-state editing requires advanced write permission.')
    if len(expected)!=policy.width or len(new)!=policy.width:
        raise ValueError('Address width mismatch')
    value=int.from_bytes(new,'big')
    if policy.max_value is not None and value>policy.max_value:
        raise ValueError(f'Value exceeds the permitted range ({policy.max_value})')
    if address==0x8015C5E0 and value==0:
        raise ValueError('Maximum health must be greater than zero')
    state=ram.u8(0x800C7A94)
    if state not in (10,13):
        raise RuntimeError(f'Game is transitioning (state {state}); cannot edit now')
    current=ram.read_guest(address,policy.width)
    if current!=expected:
        raise RuntimeError(f'Value changed since opening editor ({current.hex().upper()}). Reopen and retry.')
    if new==expected:
        return False
    ram.write_guest(address,new)
    actual=ram.read_guest(address,policy.width)
    if actual != new:
        raise OSError(f'Write verification failed: read 0x{actual.hex().upper()} (expected 0x{new.hex().upper()})')
    return True

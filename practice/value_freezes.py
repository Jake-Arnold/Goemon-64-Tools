"""Session-only, bounded repeated writes; never saves or auto-enables locks."""
from dataclasses import dataclass

from practice.checkpoints import _ensure_capture_safe
from practice.hex_edit import checked_write

MAX_HEALTH = 0x8015C5E0
HEALTH = 0x8015C5E4
MAX_LOCKS = 32


@dataclass(frozen=True)
class ValueLock:
    address: int
    value: bytes
    label: str
    raw: bool = True


class ValueFreezes:
    def __init__(self):
        self.locks = {}
        self.keep_health = False
        self.token = None

    def clear(self):
        self.locks.clear()
        self.keep_health = False
        self.token = None

    def bind(self, token):
        if self.token is not None and self.token != token:
            self.clear()
        self.token = token

    def add(self, token, address, value, label='Raw value'):
        if type(address) is not int or not isinstance(value, bytes):
            raise ValueError('Expected a guest address and bytes')
        if len(value) not in (1, 2, 4, 8) or not 0x80000000 <= address < address+len(value) <= 0x80800000:
            raise ValueError('Use 1/2/4/8 bytes within guest RDRAM')
        if self.keep_health and address < HEALTH+4 and address+len(value) > HEALTH:
            raise ValueError('Stop Keep health at maximum before freezing that range')
        for old in self.locks.values():
            if old.address != address and address < old.address+len(old.value) and old.address < address+len(value):
                raise ValueError('Freeze overlaps another active range')
        if address not in self.locks and len(self.locks) >= MAX_LOCKS:
            raise ValueError(f'At most {MAX_LOCKS} active freezes')
        self.bind(token)
        self.locks[address] = ValueLock(address, value, label)

    def enable_health(self, token):
        self.bind(token)
        if any(lock.address < HEALTH+4 and lock.address+len(lock.value) > HEALTH for lock in self.locks.values()):
            raise ValueError('Remove the overlapping health freeze first')
        self.keep_health = True

    def poll(self, ram, token, *, writable, unsafe):
        if not self.locks and not self.keep_health:
            return 'No active freezes.'
        if ram is None or token != self.token or not writable or (self.locks and not unsafe):
            self.clear()
            return 'Freezes stopped: disconnected, connection changed, or write permission disabled.'
        try:
            try:
                _ensure_capture_safe(ram)
            except ValueError:
                return 'Freezes paused: waiting for ordinary gameplay (no writes).'
            targets = list(self.locks.values())
            if self.keep_health:
                maximum = ram.u32(MAX_HEALTH)
                if not 1 <= maximum <= 127:
                    raise ValueError('Maximum health is outside the known range')
                targets.append(ValueLock(HEALTH, maximum.to_bytes(4, 'big'), 'Maximum health', False))
            for lock in targets:
                # Recheck gameplay before every target; never write from a stale UI snapshot.
                _ensure_capture_safe(ram)
                old = ram.read_guest(lock.address, len(lock.value))
                checked_write(ram, lock.address, old, lock.value,
                              allow_advanced=unsafe, raw_override=lock.raw)
            return f'Active: {len(self.locks)} value freezes; maximum health {"on" if self.keep_health else "off"}.'
        except (OSError, ValueError, RuntimeError, PermissionError) as exc:
            self.clear()
            return f'Freezes stopped after failure: {exc}'

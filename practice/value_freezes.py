"""Session-only bounded value freezes with an independent 10 ms polling worker.

The worker does not touch Tk, and all state changes are guarded with an RLock.
Polling is best-effort; frame-perfect freezes require a game-runtime hook.
"""
from dataclasses import dataclass, replace
import queue
import threading

from practice.checkpoints import _ensure_capture_safe
from practice.hex_edit import checked_write

MAX_HEALTH = 0x8015C5E0
HEALTH = 0x8015C5E4
MAX_LOCKS = 32
FREEZE_INTERVAL_SECONDS = 0.010


@dataclass(frozen=True)
class ValueLock:
    address: int
    value: bytes
    label: str
    raw: bool = True


class ValueFreezes:
    def __init__(self):
        self.guard = threading.RLock()
        self.locks = {}
        self.keep_health = False
        self.token = None

    def clear(self):
        with self.guard:
            self.locks.clear()
            self.keep_health = False
            self.token = None

    def bind(self, token):
        with self.guard:
            if self.token is not None and self.token != token:
                self.clear()
            self.token = token

    def active(self):
        with self.guard:
            return bool(self.locks or self.keep_health)

    def snapshot(self):
        with self.guard:
            return tuple(self.locks.values())

    def get(self, address):
        with self.guard:
            return self.locks.get(address)

    def remove(self, address):
        with self.guard:
            return self.locks.pop(address, None)

    def disable_health(self):
        with self.guard:
            self.keep_health = False

    def rename_lock(self, address, original, replacement):
        with self.guard:
            lock=self.locks.get(address)
            if lock is not None and lock.label == original:
                self.locks[address]=replace(lock,label=replacement)

    def add(self, token, address, value, label='Raw value'):
        with self.guard:
            if type(address) is not int or not isinstance(value, bytes):
                raise ValueError('Expected a guest address and bytes')
            if len(value) not in (1, 2, 4, 8) or not 0x80000000 <= address < address+len(value) <= 0x80800000:
                raise ValueError('Use 1/2/4/8 bytes within guest RDRAM')
            self.bind(token)
            if self.keep_health and address < HEALTH+4 and address+len(value) > HEALTH:
                raise ValueError('Stop Keep health at maximum before freezing that range')
            for old in self.locks.values():
                if old.address != address and address < old.address+len(old.value) and old.address < address+len(value):
                    raise ValueError('Freeze overlaps another active range')
            if address not in self.locks and len(self.locks) >= MAX_LOCKS:
                raise ValueError(f'At most {MAX_LOCKS} active freezes')
            self.locks[address] = ValueLock(address, value, label)

    def enable_health(self, token):
        with self.guard:
            self.bind(token)
            if any(lock.address < HEALTH+4 and lock.address+len(lock.value) > HEALTH for lock in self.locks.values()):
                raise ValueError('Remove the overlapping health freeze first')
            self.keep_health = True

    def poll(self, ram, token, *, writable):
        with self.guard:
            if not self.locks and not self.keep_health:
                return 'No active freezes.'
            if ram is None or token != self.token or not writable:
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
                corrected = 0
                for lock in targets:
                    old = ram.read_guest(lock.address, len(lock.value))
                    if old == lock.value:
                        continue
                    # Recheck gameplay immediately before a write.
                    _ensure_capture_safe(ram)
                    if checked_write(ram, lock.address, old, lock.value,
                                     allow_advanced=True, raw_override=lock.raw):
                        corrected += 1
                return f'Active: {len(self.locks)} value freezes; maximum health {"on" if self.keep_health else "off"}.'
            except (OSError, ValueError, RuntimeError, PermissionError) as exc:
                self.clear()
                return f'Freezes stopped after failure: {exc}'


class FastFreezeWorker:
    """Detached polling loop: no Tk operations, locks never persist.

    The connection provider returns (Rdram, session token, writable) while
    ValueFreezes.guard is held. Connection changes also acquire that guard.
    """

    def __init__(self, freezes, connection, messages=None, interval=FREEZE_INTERVAL_SECONDS):
        if not 0.005 <= interval <= 0.100:
            raise ValueError('Freeze interval must be 5–100 ms')
        self.freezes = freezes
        self.connection = connection
        self.messages = messages if messages is not None else queue.SimpleQueue()
        self.interval = interval
        self._stopped = threading.Event()
        self._thread = None

    def start(self):
        if self._thread is None and not self._stopped.is_set():
            self._thread = threading.Thread(target=self.run, name='GoemonFastFreeze',
                                            daemon=True)
            self._thread.start()

    def stop(self):
        self._stopped.set()
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout=1.0)

    def run(self):
        previous = None
        while not self._stopped.is_set():
            with self.freezes.guard:
                active = self.freezes.active()
                result = None
                if active:
                    try:
                        ram, token, writable = self.connection()
                        result = self.freezes.poll(ram, token, writable=writable)
                    except Exception as exc:
                        self.freezes.clear()
                        result = f'Freezes stopped after worker failure: {exc}'
            if result is not None and result != previous:
                self.messages.put(result)
            previous = result
            self._stopped.wait(self.interval if active else 0.100)

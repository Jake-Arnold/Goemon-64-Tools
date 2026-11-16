"""Session-only bounded value freezes with an independent 10 ms polling worker.

The worker does not touch Tk, and all state changes are guarded with an RLock.
Polling is best-effort; frame-perfect freezes require a game-runtime hook.
"""
from dataclasses import dataclass, replace
import queue
import threading

from practice.checkpoints import _ensure_capture_safe
from practice.hex_edit import checked_write
from autosplitter.memory import PLAYER_TASK_PTR_ADDR

MAX_HEALTH = 0x8015C5E0
HEALTH = 0x8015C5E4
MAX_LOCKS = 32
FREEZE_INTERVAL_SECONDS = 0.010
GOD_RYO = 0x8015C5E8
GOD_LIVES = 0x8015C5EC
GOD_RYO_MAX = 9999
GOD_LIVES_MAX = 99


def _overlaps(a, size, b, other_size):
    return a < b + other_size and b < a + size
# User-observed enemy-body pass-through when the live player task has state 6.
# This is NOT an invincibility, damage-prevention or terrain-noclip control.
ENEMY_PASS_THROUGH_OFFSET = 0x30
ENEMY_PASS_THROUGH_VALUE = b'\x06'


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
        self.enemy_pass_through = False
        self.god_mode = False
        self.token = None

    def clear(self):
        with self.guard:
            self.locks.clear()
            self.keep_health = False
            self.enemy_pass_through = False
            self.god_mode = False
            self.token = None

    def bind(self, token):
        with self.guard:
            if self.token is not None and self.token != token:
                self.clear()
            self.token = token

    def active(self):
        with self.guard:
            return bool(self.locks or self.keep_health or self.enemy_pass_through or self.god_mode)

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

    def disable_enemy_pass_through(self):
        with self.guard:
            self.enemy_pass_through = False

    def enable_enemy_pass_through(self, token):
        with self.guard:
            self.bind(token)
            self.enemy_pass_through = True

    def enable_god_mode(self, token):
        """Keep current health full, lives 99 and Ryo 9999; no inventory edits."""
        with self.guard:
            self.bind(token)
            for lock in self.locks.values():
                if any(_overlaps(lock.address, len(lock.value), address, 4)
                       for address in (HEALTH, GOD_RYO, GOD_LIVES)):
                    raise ValueError('Remove resource freezes conflicting with God Mode first')
            self.god_mode = True

    def disable_god_mode(self):
        with self.guard:
            self.god_mode = False

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
            if self.god_mode and any(_overlaps(address, len(value), resource, 4)
                                     for resource in (HEALTH, GOD_RYO, GOD_LIVES)):
                raise ValueError('This freeze conflicts with God Mode')
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
            if not self.locks and not self.keep_health and not self.enemy_pass_through and not self.god_mode:
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
                enemy_address = None
                if self.enemy_pass_through:
                    # Never retain an absolute actor address. Resolve from the
                    # freshly validated player snapshot on EVERY worker poll.
                    live = _ensure_capture_safe(ram)
                    task = live['task_ptr']
                    enemy_address = task + ENEMY_PASS_THROUGH_OFFSET
                    if (not ram.is_ram_pointer(enemy_address, 1) or
                            ram.u32(PLAYER_TASK_PTR_ADDR) != task):
                        return 'Enemy pass-through paused: player task changed during sample.'
                    if any(lock.address <= enemy_address < lock.address+len(lock.value)
                           for lock in targets):
                        raise ValueError('Player collision state overlaps a fixed value freeze')
                    targets.append(ValueLock(enemy_address, ENEMY_PASS_THROUGH_VALUE,
                                             'Enemy pass-through (player task +0x30)', True))
                if self.keep_health or self.god_mode:
                    maximum = ram.u32(MAX_HEALTH)
                    if not 1 <= maximum <= 127:
                        raise ValueError('Maximum health is outside the known range')
                    targets.append(ValueLock(HEALTH, maximum.to_bytes(4, 'big'), 'Maximum health', False))
                if self.god_mode:
                    targets.extend((
                        ValueLock(GOD_LIVES, GOD_LIVES_MAX.to_bytes(4, 'big'), 'God Mode lives', False),
                        ValueLock(GOD_RYO, GOD_RYO_MAX.to_bytes(4, 'big'), 'God Mode Ryo', False),
                    ))
                corrected = 0
                for lock in targets:
                    old = ram.read_guest(lock.address, len(lock.value))
                    if old == lock.value:
                        continue
                    # Recheck gameplay immediately before a write. For the
                    # relative target, refuse stale writes if the player task
                    # changed during this poll, even within the same scene.
                    fresh = _ensure_capture_safe(ram)
                    if enemy_address == lock.address and (
                            fresh['task_ptr'] + ENEMY_PASS_THROUGH_OFFSET != enemy_address or
                            ram.u32(PLAYER_TASK_PTR_ADDR) != fresh['task_ptr']):
                        return 'Enemy pass-through paused: player task changed before write.'
                    if checked_write(ram, lock.address, old, lock.value,
                                     allow_advanced=True, raw_override=lock.raw):
                        corrected += 1
                enemy = (f'; enemy pass-through 0x{enemy_address:08X}'
                         if enemy_address is not None else '')
                return (f'Active: {len(self.locks)} value freezes; maximum health '
                        f'{"on" if self.keep_health or self.god_mode else "off"}'
                        f'; God Mode {"on" if self.god_mode else "off"}{enemy}.')
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

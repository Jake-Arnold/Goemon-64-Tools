"""Read USA Goemon N64 RAM through Windows or native Linux process memory.

Original RAM symbols are grounded in Goemon64Recomp; the Linux process adapter
is experimental and does not establish live-game compatibility on its own.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
import errno
import math
import os
import struct
import sys

# These N64 addresses are grounded in Goemon64Recomp source, USA ROM only.
SYS_POINTER_ADDR = 0x8015C5C8  # points to 0x8008CCC0 after init
SYS_EXPECTED_PTR = 0x8008CCC0
PLAYER_OBJECT_PTR_ADDR = 0x801FC60C
PLAYER_TASK_PTR_ADDR = 0x801FC604
CHARACTER_ID_ADDR = 0x8015C5DC
LOADING_FLAG_ADDR = 0x8015C5D4
SYS_ADDR = 0x8008CCC0
RDRAM_SIZE = 0x800000

# Object position starts at offset 8; PlayerTask action_id at 0xCC.
OBJECT_POSITION_OFFSET = 0x08
PLAYER_ACTION_OFFSET = 0xCC

# Win32 process APIs (Linux/macOS process readers would be different).
if os.name == "nt":
    import ctypes.wintypes as wt
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    SIZE_T = ctypes.c_size_t
    ULONG_PTR = ctypes.c_size_t
    class MEMORY_BASIC_INFORMATION(ctypes.Structure):
        _fields_ = [("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
                    ("AllocationProtect", wt.DWORD), ("PartitionId", wt.WORD),
                    ("RegionSize", SIZE_T), ("State", wt.DWORD), ("Protect", wt.DWORD),
                    ("Type", wt.DWORD)]
    kernel32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
    kernel32.OpenProcess.restype = wt.HANDLE
    kernel32.ReadProcessMemory.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, SIZE_T, ctypes.POINTER(SIZE_T)]
    kernel32.ReadProcessMemory.restype = wt.BOOL
    kernel32.WriteProcessMemory.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, SIZE_T, ctypes.POINTER(SIZE_T)]
    kernel32.WriteProcessMemory.restype = wt.BOOL
    kernel32.VirtualQueryEx.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), SIZE_T]
    kernel32.VirtualQueryEx.restype = SIZE_T
    kernel32.CloseHandle.argtypes = [wt.HANDLE]
    kernel32.CloseHandle.restype = wt.BOOL


class WindowsProcess:
    def __init__(self, pid: int, writable: bool = False):
        self.writable = writable
        if os.name != "nt":
            raise OSError("Process-memory integration runs on Windows; use --demo for tests")
        access = 0x1000 | 0x0010 | (0x0020 | 0x0008 if writable else 0)
        self.handle = kernel32.OpenProcess(access, False, pid)
        if not self.handle:
            raise OSError(f"OpenProcess({pid}) failed: {ctypes.get_last_error()}")

    def close(self):
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None

    def read(self, address: int, length: int) -> bytes:
        result = ctypes.create_string_buffer(length)
        size = SIZE_T()
        ok = kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), result,
                                        length, ctypes.byref(size))
        if not ok or size.value != length:
            raise OSError(f"ReadProcessMemory 0x{address:X} ({length} bytes) failed")
        return result.raw

    def write(self, address: int, data: bytes):
        if not self.writable:
            raise PermissionError('Process connection is read-only')
        size = SIZE_T()
        buff = ctypes.create_string_buffer(data)
        ok = kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address), buff,
                                         len(data), ctypes.byref(size))
        if not ok or size.value != len(data):
            raise OSError(f"WriteProcessMemory 0x{address:X} failed")

    def regions(self):
        pointer = 0x10000
        while pointer < 0x00007FFFFFFFFFFF:
            mbi = MEMORY_BASIC_INFORMATION()
            if not kernel32.VirtualQueryEx(self.handle, ctypes.c_void_p(pointer), ctypes.byref(mbi), ctypes.sizeof(mbi)):
                break
            start, length = mbi.BaseAddress or pointer, mbi.RegionSize
            if (mbi.State == 0x1000 and not (mbi.Protect & 0x100) and
                (mbi.Protect & 0xFF) in (0x02, 0x04, 0x08, 0x20, 0x40, 0x80)):
                yield int(start), int(length)
            pointer = int(start) + max(int(length), 0x1000)


if sys.platform == "linux":
    from .linux_process import LinuxProcess
    HostProcess = LinuxProcess
else:
    HostProcess = WindowsProcess


class Rdram:
    def __init__(self, process, host_base: int, endian: str = "wordswapped"):
        if endian not in ("wordswapped", "big"):
            raise ValueError("endian must be wordswapped or big")
        self.process, self.base, self.endian = process, host_base, endian

    @staticmethod
    def offset(n64_addr: int, length: int = 1):
        # KSEG0/KSEG1 virtual addresses map to physical first 8 MB RAM.
        if (n64_addr & 0xE0000000) not in (0x80000000, 0xA0000000):
            raise ValueError(f"Invalid N64 RDRAM pointer: 0x{n64_addr:08X}")
        n = n64_addr & 0x1FFFFFFF
        if n < 0 or n + length > RDRAM_SIZE:
            raise ValueError(f"N64 pointer outside 8MB RDRAM: 0x{n64_addr:08X}")
        return n

    def u32(self, address: int) -> int:
        offset = self.offset(address, 4)
        raw = self.process.read(self.base + offset, 4)
        return int.from_bytes(raw, "little" if self.endian == "wordswapped" else "big")

    def u8(self, address: int) -> int:
        offset = self.offset(address)
        if self.endian == "wordswapped": offset ^= 3
        return self.process.read(self.base + offset, 1)[0]

    def f32(self, address: int) -> float:
        offset = self.offset(address, 4)
        raw = self.process.read(self.base + offset, 4)
        return struct.unpack("<f" if self.endian == "wordswapped" else ">f", raw)[0]


    def read_guest(self, address: int, length: int) -> bytes:
        """Read N64 canonical big-endian bytes, independent of host layout.

        In a word-swapped host mapping each *four-byte word* is reversed. A
        single byte or unaligned region must therefore align to nearby words
        before converting, rather than simply reversing the requested slice.
        """
        if length < 0:
            raise ValueError("negative length")
        if length == 0:
            return b""
        off = self.offset(address, length)
        if off + length > getattr(self, 'rdram_size', RDRAM_SIZE):
            raise ValueError('Guest read exceeds verified emulator RDRAM size')
        if self.endian == "big":
            return self.process.read(self.base + off, length)
        start, end = off & ~3, (off + length + 3) & ~3
        raw = self.process.read(self.base + start, end - start)
        guest = b"".join(raw[i:i+4][::-1] for i in range(0, len(raw), 4))
        return guest[off-start:off-start+length]

    def write_guest(self, address: int, data: bytes):
        """Write guest bytes, preserving neighboring bytes in partial words."""
        if not data:
            return
        off = self.offset(address, len(data))
        if off + len(data) > getattr(self, 'rdram_size', RDRAM_SIZE):
            raise ValueError('Guest write exceeds verified emulator RDRAM size')
        if self.endian == "big":
            self.process.write(self.base + off, data)
            return
        start, end = off & ~3, (off + len(data) + 3) & ~3
        raw = self.process.read(self.base + start, end - start)
        guest = bytearray(b"".join(raw[i:i+4][::-1] for i in range(0, len(raw), 4)))
        guest[off-start:off-start+len(data)] = data
        changed = b"".join(guest[i:i+4][::-1] for i in range(0, len(guest), 4))
        self.process.write(self.base + start, changed)

    def u16(self, address: int) -> int:
        return int.from_bytes(self.read_guest(address, 2), "big")

    def write_f32(self, address: int, value: float):
        if not math.isfinite(value):
            raise ValueError("Non-finite position")
        raw = struct.pack("<f" if self.endian == "wordswapped" else ">f", value)
        self.process.write(self.base + self.offset(address, 4), raw)

    @classmethod
    def is_ram_pointer(cls, value: int, size: int = 1) -> bool:
        if not value:
            return False
        try:
            cls.offset(value, size)
            return True
        except ValueError:
            return False

    def snapshot(self) -> dict:
        """Fail closed if any core field is implausible.

        The old scanner verified only the system pointer, accepting a coincidental
        copy of the constant located elsewhere in the process. That produced
        bogus character IDs and empty positions in the UI.
        """
        system = self.u32(SYS_POINTER_ADDR)
        if system != SYS_EXPECTED_PTR:
            raise ValueError(f"Invalid system pointer 0x{system:08X}; wrong RAM base or ROM variant")
        char_id = self.u32(CHARACTER_ID_ADDR)
        loading = self.u8(LOADING_FLAG_ADDR)
        if loading not in (0, 1):
            raise ValueError(f"Invalid loading flag {loading}; RAM base is not validated")
        task = self.u32(PLAYER_TASK_PTR_ADDR)
        obj = self.u32(PLAYER_OBJECT_PTR_ADDR)
        # Some screens have no player and may not have a meaningful character ID.
        # Never interpret an unknown ID as a playable character when a player exists.
        if char_id > 3:
            if obj or task:
                raise ValueError(f"Invalid character ID {char_id}; player identity is not validated")
            char_id = None
        for title, ptr, size in (("player object", obj, OBJECT_POSITION_OFFSET + 12),
                                 ("player task", task, PLAYER_ACTION_OFFSET + 1)):
            if ptr and not self.is_ram_pointer(ptr, size):
                raise ValueError(f"Invalid {title} pointer 0x{ptr:08X}")

        state = {"character": char_id, "player_ptr": obj, "task_ptr": task,
                 "loading": loading, "x": None, "y": None, "z": None,
                 "action": None, "object_rotation_y": None}
        if obj:
            coords = tuple(self.f32(obj + OBJECT_POSITION_OFFSET + i*4) for i in range(3))
            if not all(math.isfinite(v) and abs(v) < 1000000 for v in coords):
                raise ValueError(f"Invalid player position: {coords}")
            state.update(zip(("x", "y", "z"), coords))
        if task:
            state["action"] = self.u8(task + PLAYER_ACTION_OFFSET)
        return state



    def snapshot_for_monitoring(self) -> dict:
        """Best-effort player snapshot for read-only scene monitoring.

        A valid RDRAM mapping is still mandatory. Title screens, Impact scenes
        and other nonstandard modes can leave the ordinary player pointers
        nonzero but unusable. Never expose such pointers to player controls.
        Call snapshot() instead for strict player-dependent operations.
        """
        try:
            state = self.snapshot()
            if (state["player_ptr"] and state["task_ptr"] and
                    state["character"] is not None and state["x"] is not None and
                    state["action"] is not None):
                return state
            reason = "Normal player object/task unavailable in this scene"
        except (ValueError, OSError) as exc:
            reason = str(exc)

        # A missing player is recoverable; a bad RAM base or invalid global
        # loading flag is not. Re-read these independent global sentinels.
        system = self.u32(SYS_POINTER_ADDR)
        if system != SYS_EXPECTED_PTR:
            raise ValueError(f"Invalid system pointer 0x{system:08X}; wrong RAM base or ROM variant")
        loading = self.u8(LOADING_FLAG_ADDR)
        if loading not in (0, 1):
            raise ValueError(f"Invalid loading flag {loading}; RAM base is not validated")
        return {
            "character": None, "player_ptr": None, "task_ptr": None,
            "loading": loading, "x": None, "y": None, "z": None,
            "action": None, "object_rotation_y": None,
            "player_unavailable_reason": reason,
        }

def readable_spans(regions):
    """Join adjacent readable regions, including Project64's protected code pages.

    Never bridge a gap: guard and inaccessible pages are excluded by regions().
    """
    pending = None
    for start, length in regions:
        if pending is not None and pending[0] + pending[1] == start:
            pending = (pending[0], pending[1] + length)
        else:
            if pending is not None:
                yield pending
            pending = (start, length)
    if pending is not None:
        yield pending


def discover_rdram(process, mode: str = "auto", max_scan_mb: int = 2048):
    """Find and *cross-check* a host RAM base, optionally checking both endians.

    Return (base, endian). Prefer a validated player when present; without one,
    accept only a unique RAM candidate with plausible state, phase and map.
    Ambiguous no-player candidates fail closed. No process-memory writes occur.
    """
    if mode not in ("auto", "wordswapped", "big"):
        raise ValueError("mode must be auto, wordswapped or big")
    modes = ("wordswapped", "big") if mode == "auto" else (mode,)
    signatures = {m: SYS_EXPECTED_PTR.to_bytes(4, "little" if m == "wordswapped" else "big")
                  for m in modes}
    scanned = 0
    rejected = 0
    permission_denied = False
    candidates = []
    no_player_candidates = []
    budget = max_scan_mb * 1048576
    for start, length in readable_spans(process.regions()):
        if length < 0x180000 or scanned >= budget:
            continue
        previous = b""
        for pos in range(start, start + length, 1048576):
            read_len = min(1048576, start + length - pos, budget - scanned)
            if read_len <= 0:
                break
            scanned += read_len
            try:
                block = previous + process.read(pos, read_len)
            except OSError as exc:
                if getattr(exc, "errno", None) in (errno.EPERM, errno.EACCES):
                    permission_denied = True
                previous = b""
                continue
            for endian, signature in signatures.items():
                idx = block.find(signature)
                while idx >= 0:
                    found = pos - len(previous) + idx
                    base = found - (SYS_POINTER_ADDR & 0x1FFFFFFF)
                    # This is a game RAM buffer: it must be at least 16-byte aligned.
                    # A page-aligned candidate is preferred, but not mandatory.
                    if base > 0 and base % 16 == 0:
                        try:
                            ram = Rdram(process, base, endian)
                            state = ram.snapshot_for_monitoring()
                            # Check both ends of the full guest mapping.
                            process.read(base, 4)
                            process.read(base + RDRAM_SIZE - 4, 4)
                            if (state["player_ptr"] and state["task_ptr"] and
                                    state["x"] is not None and state["action"] is not None):
                                candidates.append((base, endian))
                            elif not state["player_ptr"] or not state["task_ptr"]:
                                # Independently check non-player engine fields; do not
                                # infer a player, and never silently choose among copies.
                                top_state = ram.u8(0x800C7A94)
                                phase = ram.u8(0x800C7A9E)
                                map_id = ram.u16(0x800C7AB2)
                                if top_state < 18 and phase < 3 and map_id < 0x800:
                                    no_player_candidates.append((base, endian))
                        except (OSError, ValueError):
                            rejected += 1
                    else:
                        rejected += 1
                    idx = block.find(signature, idx + 1)
            previous = block[-3:]
        if scanned >= budget:
            break
    if candidates:
        candidates = sorted(set(candidates), key=lambda x: (x[0] % 4096 != 0, x[0], x[1]))
        # Multiple fully plausible copies require manual validation rather than
        # silently using the first one.
        aligned = [c for c in candidates if c[0] % 4096 == 0]
        if len(aligned) == 1:
            return aligned[0]
        if len(candidates) == 1:
            return candidates[0]
        summary = ", ".join(f"0x{b:X}/{e}" for b,e in candidates[:10])
        raise RuntimeError(f"Ambiguous RAM bases ({len(candidates)}): {summary}; use --base")
    no_player_candidates = sorted(set(no_player_candidates))
    if len(no_player_candidates) == 1:
        return no_player_candidates[0]
    if len(no_player_candidates) > 1:
        raise RuntimeError(f"Ambiguous RAM bases ({len(no_player_candidates)}) without a player; use --base")
    reason = (" Linux process-memory access was denied; see Connection panel "
              "for existing-PID permission options." if permission_denied else "")
    raise RuntimeError(
        f"No validated game RAM found ({rejected} rejected matches). "
        "Start the game and retry. "
        "Unsupported game version or memory layout is also possible." + reason
    )


def find_rdram(process, mode: str = "wordswapped", max_scan_mb: int = 2048) -> int:
    """Compatibility wrapper for code expecting an address only."""
    return discover_rdram(process, mode, max_scan_mb)[0]

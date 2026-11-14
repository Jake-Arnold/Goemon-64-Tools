"""Read-only, experimental Japanese Goemon rev0 RDRAM discovery in Mupen64Plus.

Uses the owner's verified ROM for several independent boot-time executable-code
fingerprints. Never accepts a Japan process into USA-specific gameplay tools.
Real Mupen64Plus memory layouts still require live testing.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys

from autosplitter.memory import HostProcess, Rdram
from practice.entrances import canonical_rom
from practice.emulator_savestates import find_emulator_pid, verified_emulator_pid

JP_ORIGINAL_SHA1 = "9843ee979b5f6c80f5eda85df0baed9ae7c4e73b"
JP_EXPANDED_SHA1 = "6f8745fecc3a5e7d4918c7a73353eb0726116ded"
FINGERPRINT_OFFSETS = (0x10000, 0x20000, 0x30000, 0x40000)
FINGERPRINT_LENGTH = 64
ROM_RAM_OFFSET = 0xC00
RDRAM_MIN_SIZE = 4 * 1024 * 1024
SEARCH_OFFSET = FINGERPRINT_OFFSETS[0]
BLOCK_SIZE = 1024 * 1024
MAX_BYTES = 1024 * 1024 * 1024


def checked_japan_rom(path: Path) -> bytes:
    """Require a *user-supplied*, exact Japanese rev0 cartridge/expanded image."""
    raw = path.read_bytes()
    if len(raw) not in (0x1000000, 0x2000000):
        raise ValueError("Expected 16 MiB retail or 32 MiB expanded Japanese ROM")
    canonical = canonical_rom(raw)
    expected = JP_ORIGINAL_SHA1 if len(raw) == 0x1000000 else JP_EXPANDED_SHA1
    if hashlib.sha1(canonical).hexdigest() != expected or canonical[0x3B:0x3F] != b"NG5J":
        raise ValueError("Japanese ROM revision/hash mismatch; refusing RAM attachment")
    return canonical


def _wordswapped(buf: bytes) -> bytes:
    return b"".join(buf[i:i + 4][::-1] for i in range(0, len(buf), 4))


def fingerprints(rom: bytes, endian: str) -> tuple[bytes, ...]:
    if endian not in ("big", "wordswapped"):
        raise ValueError("Invalid RDRAM endian mode")
    result = []
    for offset in FINGERPRINT_OFFSETS:
        block = rom[offset + ROM_RAM_OFFSET:offset + ROM_RAM_OFFSET + FINGERPRINT_LENGTH]
        if len(block) != FINGERPRINT_LENGTH:
            raise ValueError("Truncated executable fingerprint")
        result.append(block if endian == "big" else _wordswapped(block))
    return tuple(result)


def _writable_linux_regions(pid: int):
    """RDRAM is writable; discard read-only ROM images and executable code."""
    if sys.platform != "linux":
        raise OSError("Japanese Mupen read-only probing currently supports Linux only")
    with Path(f"/proc/{pid}/maps").open("r", encoding="ascii") as maps:
        for line in maps:
            parts = line.split(None, 5)
            if len(parts) < 2 or len(parts[1]) < 2 or parts[1][:2] != "rw":
                continue
            try:
                a, b = [int(p, 16) for p in parts[0].split("-", 1)]
            except ValueError:
                continue
            if b - a >= 0x1000:
                yield a, b - a


def find_japanese_rdram(process, rom: bytes, regions, *, max_scan_bytes: int = MAX_BYTES):
    """Return (base, endian); all matched executable anchors must be unique.

    Memory is never written. The checks exclude an intact ROM buffer aligned
    as if it were RAM; complete live emulator verification remains outstanding.
    """
    if max_scan_bytes <= 0:
        raise ValueError("Scan budget must be positive")
    fp = {e: fingerprints(rom, e) for e in ("big", "wordswapped")}
    decoy = rom[ROM_RAM_OFFSET:ROM_RAM_OFFSET + 256]
    verified = set()
    scanned = 0
    denied = False
    for start, length in regions:
        if scanned >= max_scan_bytes:
            break
        if start <= 0 or length < 0x10000 or start % 4096:
            continue
        previous = b""
        for cursor in range(start, start + length, BLOCK_SIZE):
            n = min(BLOCK_SIZE, start + length - cursor, max_scan_bytes - scanned)
            if n <= 0:
                break
            scanned += n
            try:
                block = previous + process.read(cursor, n)
            except PermissionError:
                denied = True
                previous = b""
                continue
            except OSError:
                previous = b""
                continue
            for endian, patterns in fp.items():
                needle = patterns[0]
                found = block.find(needle)
                while found >= 0:
                    pos = cursor - len(previous) + found
                    base = pos - SEARCH_OFFSET
                    if base > 0 and base % 4096 == 0:
                        try:
                            # Verify remaining code anchors independently and
                            # the complete low 4 MiB RDRAM address range.
                            if all(process.read(base + off, FINGERPRINT_LENGTH) == pattern
                                   for off, pattern in zip(FINGERPRINT_OFFSETS, patterns)):
                                process.read(base, 4)
                                process.read(base + RDRAM_MIN_SIZE - 4, 4)
                                # A loaded ROM buffer has the same code bytes but
                                # still contains bootcode at this false RAM base.
                                first = process.read(base, 256)
                                if first != (decoy if endian == "big" else _wordswapped(decoy)):
                                    verified.add((base, endian))
                        except (OSError, ValueError):
                            pass
                    found = block.find(needle, found + 1)
            previous = block[-(FINGERPRINT_LENGTH - 1):]
    if len(verified) == 1:
        return next(iter(verified))
    if verified:
        raise RuntimeError("Multiple possible Japanese RDRAM buffers; aborting without selecting")
    if denied:
        raise PermissionError("Mupen64Plus process-memory read denied; check Linux ptrace policy")
    raise RuntimeError("No verified Japanese RDRAM code anchors found in writable host memory")


def attach_japanese_mupen(pid: int, rom_path: Path, base_hint: int | None = None,
                          max_scan_bytes: int = MAX_BYTES):
    """Open only a read-only host process and return a version-isolated Rdram.

    Caller owns the returned HostProcess and must close it. Do not feed this
    handle to any USA gameplay snapshot or writer.
    """
    verified_emulator_pid(pid, "mupen64plus")
    rom = checked_japan_rom(rom_path)
    process = HostProcess(pid, writable=False)
    try:
        if base_hint is not None:
            if base_hint <= 0 or base_hint % 4096:
                raise ValueError("Manual RDRAM base must be positive and page-aligned")
            candidates = []
            for endian in ("big", "wordswapped"):
                pats = fingerprints(rom, endian)
                try:
                    if all(process.read(base_hint + off, FINGERPRINT_LENGTH) == pattern
                           for off, pattern in zip(FINGERPRINT_OFFSETS, pats)):
                        candidates.append(endian)
                except OSError:
                    pass
            if len(candidates) != 1:
                raise ValueError("Manual base did not uniquely validate against Japanese code")
            base, endian = base_hint, candidates[0]
        else:
            base, endian = find_japanese_rdram(process, rom, _writable_linux_regions(pid), max_scan_bytes=max_scan_bytes)
        memory = Rdram(process, base, endian)
        # The bootstrap is intentionally not allowed to assert Japanese
        # player pointers or run the USA snapshot validation.
        memory.read_guest(0x80030000, 4)
        return process, memory
    except BaseException:
        process.close()
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True, help="Verified Japanese rev0 ROM")
    parser.add_argument("--pid", type=int, help="Existing Mupen64Plus PID (auto if unique)")
    parser.add_argument("--base", type=lambda x: int(x, 0), help="Validate known host RDRAM base")
    parser.add_argument("--max-scan-mb", type=int, default=1024,
                        help="Maximum writable process memory to inspect")
    parser.add_argument("--address", type=lambda x: int(x, 0), default=0x80030000,
                        help="N64 memory address to read (default verified code segment)")
    parser.add_argument("--length", type=int, default=32)
    args = parser.parse_args(argv)
    if not 1 <= args.max_scan_mb <= 4096:
        parser.error("Scan limit must be 1..4096 MiB")
    if not 1 <= args.length <= 256:
        parser.error("Length must be 1..256 bytes")
    pid = args.pid or find_emulator_pid("mupen64plus")[0]
    process, mem = attach_japanese_mupen(pid, args.rom, args.base,
                                         max_scan_bytes=args.max_scan_mb * 1048576)
    try:
        raw = mem.read_guest(args.address, args.length)
        print(f"JP rev0 Mupen PID {pid}: read-only RAM base 0x{mem.base:X}, endian={mem.endian}")
        print(f"0x{args.address:08X}: {raw.hex(' ')}")
        print("USA player, scene, inventory and write controls intentionally disabled")
    finally:
        process.close()


if __name__ == "__main__":
    main()

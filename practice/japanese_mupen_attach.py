"""Read-only Japan-0 RDRAM discovery for Mupen64Plus and Windows Project64.

Require an exact verified retail Japan-0 ROM and three separate code probes.
Project64 may map 4 MiB or 8 MiB; never assume a configured fixed base is
actually live guest RAM. Discovery and validation perform no process writes.
"""
from __future__ import annotations

from pathlib import Path

from practice.game_versions import identify_rom
from practice.entrances import canonical_rom
from autosplitter.memory import RDRAM_SIZE, Rdram, readable_spans

# Japanese main executable: ROM 0x1050 maps to guest RAM 0x450.
# See klorfmorf/mnsg/config/japan_0/splat.yaml; this is not a USA live-field mapping.
ROM_TO_GUEST = 0xC00
PROBE_ROM_OFFSETS = (0x1050, 0x1200, 0x3000)
PROBE_BYTES = 64
SCAN_CHUNK = 4 << 20  # Fewer Linux/Wine process_vm_readv round trips; same 2 GiB safety budget
MIN_RDRAM_SIZE = 0x400000  # Project64 supports unexpanded 4 MiB guest RDRAM.


class VerifiedJapaneseProbes(tuple):
    """Three loaded-code probes and cartridge header for rejecting ROM copies."""

    def __new__(cls, entries, cartridge_header):
        if len(cartridge_header) != 64:
            raise ValueError('Expected 64 bytes of verified cartridge header')
        instance = super().__new__(cls, entries)
        instance.cartridge_header = bytes(cartridge_header)
        return instance


class AmbiguousJapaneseRdram(RuntimeError):
    """Report candidate base/endian pairs for explicit revalidated selection."""

    def __init__(self, candidates):
        self.candidates = tuple(sorted(candidates))
        listed = ', '.join(f'0x{base:X}/{endian}' for base, endian in self.candidates)
        super().__init__(f'Ambiguous Japanese RDRAM mappings ({len(self.candidates)}): '
                         f'{listed}; select one candidate base and reconnect')



def verified_japan_probes(path: str | Path) -> tuple[tuple[int, bytes], ...]:
    """Generate signatures only after exact SHA-1 identification of Japan-0."""
    data = Path(path).read_bytes()
    if identify_rom(data).key != 'japan':
        raise ValueError('The selected ROM is not Japan revision 0')
    rom = canonical_rom(data)
    entries = tuple((offset - ROM_TO_GUEST, rom[offset:offset + PROBE_BYTES])
                    for offset in PROBE_ROM_OFFSETS)
    return VerifiedJapaneseProbes(entries, rom[:64])


def _swapped_words(data: bytes) -> bytes:
    if len(data) % 4:
        raise ValueError('Guest code probe must be word-aligned')
    return b''.join(data[i:i+4][::-1] for i in range(0, len(data), 4))


def _swapped_pairs(data: bytes) -> bytes:
    """Reverse adjacent bytes in each guest halfword (N64 .v64 layout)."""
    if len(data) % 2:
        raise ValueError('Guest code probe must be halfword-aligned')
    return b''.join(data[i:i+2][::-1] for i in range(0, len(data), 2))


def _host_order(data: bytes, endian: str) -> bytes:
    if endian == 'wordswapped':
        return _swapped_words(data)
    if endian == 'byteswapped':
        return _swapped_pairs(data)
    if endian == 'big':
        return data
    raise ValueError('Unsupported RDRAM byte order')


def _is_cartridge_copy(process, base: int, endian: str, probes) -> bool:
    """Reject a ROM buffer masquerading as RAM because code bytes coincide.

    If the apparent RDRAM base is 0xC00 into the complete cartridge image,
    the exact verified N64 header is present 0xC00 bytes before that base.
    """
    header = getattr(probes, 'cartridge_header', None)
    if not header or base <= ROM_TO_GUEST:
        return False
    expected = _host_order(header, endian)
    try:
        return process.read(base - ROM_TO_GUEST, len(expected)) == expected
    except OSError:
        return False  # True RDRAM need not have readable memory before its base.


def validate_rdram_base(process, base: int, endian: str,
                        probes: tuple[tuple[int, bytes], ...],
                        *, allow_4mb: bool = False) -> Rdram:
    """Require three independently positioned, complete main-code probes."""
    if type(base) is not int or base <= 0 or base % 16:
        raise ValueError('RDRAM host base must be a positive 16-byte-aligned address')
    if endian not in ('wordswapped', 'byteswapped', 'big'):
        raise ValueError('Unsupported RDRAM byte order')
    if len(probes) < 3:
        raise ValueError('At least three Japanese executable probes are required')
    for offset, expected in probes:
        if not 0 <= offset < RDRAM_SIZE or offset + len(expected) > RDRAM_SIZE:
            raise ValueError('Invalid Japanese RDRAM probe offset')
        original = process.read(base + offset, len(expected))
        canonical = _host_order(original, endian)
        if canonical != expected:
            raise ValueError(f'Japanese main-code verification failed at RDRAM +0x{offset:X}')
    # Do not silently read outside an unexpanded 4 MiB Project64 mapping.
    # The default 8 MiB requirement preserves the existing Mupen behaviour.
    try:
        process.read(base + RDRAM_SIZE - 4, 4)
        mapped_size = RDRAM_SIZE
    except OSError:
        if not allow_4mb:
            raise
        process.read(base + MIN_RDRAM_SIZE - 4, 4)
        mapped_size = MIN_RDRAM_SIZE
    if _is_cartridge_copy(process, base, endian, probes):
        raise ValueError(f'Host address 0x{base:X} points into cartridge ROM, not live RDRAM')
    reader = Rdram(process, base, endian)
    reader.rdram_size = mapped_size
    return reader


def discover_japanese_mupen_rdram(process, probes, *, mode='auto',
                                  base_hint: int | None = None,
                                  max_scan_mb: int = 2048,
                                  allow_4mb: bool = False):
    """Return (Rdram, base, endian), refusing missing or ambiguous candidates.

    Scans only readable host process memory, on Windows or Linux.
    Project64 callers allow 4 MiB, Mupen keeps its existing 8 MiB minimum.
    Manual base hints must still match all three Japanese code probes.
    """
    if mode not in ('auto', 'big', 'wordswapped', 'byteswapped'):
        raise ValueError('Invalid RDRAM endian selection')
    modes = ('big', 'wordswapped', 'byteswapped') if mode == 'auto' else (mode,)
    if base_hint is not None:
        matches = []
        for endian in modes:
            try:
                matches.append((validate_rdram_base(
                    process, base_hint, endian, probes, allow_4mb=allow_4mb),
                    base_hint, endian))
            except (OSError, ValueError):
                pass
        if len(matches) != 1:
            raise RuntimeError('Manual base did not uniquely match Japan-0 executable code')
        return matches[0]
    first_offset, first_code = probes[0]
    signatures = {
        endian: _host_order(first_code, endian)
        for endian in modes
    }
    matches = set()
    scanned = 0
    budget = max_scan_mb * 1048576
    minimum_size = MIN_RDRAM_SIZE if allow_4mb else RDRAM_SIZE
    for start, length in readable_spans(process.regions()):
        if length < minimum_size or scanned >= budget:
            continue
        tail = b''
        for pos in range(start, start + length, SCAN_CHUNK):
            n = min(SCAN_CHUNK, start + length - pos, budget - scanned)
            if n <= 0:
                break
            scanned += n
            try:
                block = tail + process.read(pos, n)
            except PermissionError:
                raise
            except OSError:
                tail = b''
                continue
            for endian, sig in signatures.items():
                idx = block.find(sig)
                while idx >= 0:
                    found = pos - len(tail) + idx
                    base = found - first_offset
                    if base > 0 and base % 16 == 0:
                        try:
                            validate_rdram_base(
                                process, base, endian, probes, allow_4mb=allow_4mb)
                        except PermissionError:
                            raise
                        except (OSError, ValueError):
                            pass
                        else:
                            matches.add((base, endian))
                    idx = block.find(sig, idx + 1)
            tail = block[-(PROBE_BYTES - 1):]
    if len(matches) != 1:
        if not matches:
            raise RuntimeError(
                'No Japanese emulator RDRAM matched all three code probes; '
                'check ROM, PID, process permissions and whether the game has booted'
            )
        raise AmbiguousJapaneseRdram(matches)
    base, endian = next(iter(matches))
    return validate_rdram_base(
        process, base, endian, probes, allow_4mb=allow_4mb), base, endian

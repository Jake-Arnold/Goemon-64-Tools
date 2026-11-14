"""Read-only attachment to an already-running Japan-0 Mupen64Plus RDRAM.

A verified retail ROM supplies boot/main-code signatures; no Japanese USA
RAM address mapping is assumed and no process writes are allowed.
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
SCAN_CHUNK = 1 << 20


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


def _is_cartridge_copy(process, base: int, endian: str, probes) -> bool:
    """Reject a ROM buffer masquerading as RAM because code bytes coincide.

    If the apparent RDRAM base is 0xC00 into the complete cartridge image,
    the exact verified N64 header is present 0xC00 bytes before that base.
    """
    header = getattr(probes, 'cartridge_header', None)
    if not header or base <= ROM_TO_GUEST:
        return False
    expected = _swapped_words(header) if endian == 'wordswapped' else header
    try:
        return process.read(base - ROM_TO_GUEST, len(expected)) == expected
    except OSError:
        return False  # True RDRAM need not have readable memory before its base.


def validate_rdram_base(process, base: int, endian: str,
                        probes: tuple[tuple[int, bytes], ...]) -> Rdram:
    """Require three independently positioned, complete main-code probes."""
    if type(base) is not int or base <= 0 or base % 16:
        raise ValueError('RDRAM host base must be a positive 16-byte-aligned address')
    if endian not in ('wordswapped', 'big'):
        raise ValueError('Unsupported RDRAM byte order')
    if len(probes) < 3:
        raise ValueError('At least three Japanese executable probes are required')
    for offset, expected in probes:
        if not 0 <= offset < RDRAM_SIZE or offset + len(expected) > RDRAM_SIZE:
            raise ValueError('Invalid Japanese RDRAM probe offset')
        original = process.read(base + offset, len(expected))
        canonical = _swapped_words(original) if endian == 'wordswapped' else original
        if canonical != expected:
            raise ValueError(f'Japanese main-code verification failed at RDRAM +0x{offset:X}')
    process.read(base + RDRAM_SIZE - 4, 4)
    if _is_cartridge_copy(process, base, endian, probes):
        raise ValueError(f'Host address 0x{base:X} points into cartridge ROM, not live RDRAM')
    return Rdram(process, base, endian)


def discover_japanese_mupen_rdram(process, probes, *, mode='auto',
                                  base_hint: int | None = None,
                                  max_scan_mb: int = 2048):
    """Return (Rdram, base, endian), refusing missing or ambiguous candidates.

    Scans only memory readable through the normal Linux process permissions.
    Manual base hints must still match all three Japanese code probes.
    """
    if mode not in ('auto', 'big', 'wordswapped'):
        raise ValueError('Invalid RDRAM endian selection')
    modes = ('big', 'wordswapped') if mode == 'auto' else (mode,)
    if base_hint is not None:
        matches = []
        for endian in modes:
            try:
                matches.append((validate_rdram_base(process, base_hint, endian, probes),
                                base_hint, endian))
            except (OSError, ValueError):
                pass
        if len(matches) != 1:
            raise RuntimeError('Manual base did not uniquely match Japan-0 executable code')
        return matches[0]
    first_offset, first_code = probes[0]
    signatures = {
        endian: (_swapped_words(first_code) if endian == 'wordswapped' else first_code)
        for endian in modes
    }
    matches = set()
    scanned = 0
    budget = max_scan_mb * 1048576
    for start, length in readable_spans(process.regions()):
        if length < RDRAM_SIZE or scanned >= budget:
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
                            validate_rdram_base(process, base, endian, probes)
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
                'No Japanese Mupen64Plus RDRAM matched all three code probes; '
                'check ROM, PID, Linux permissions and whether the game has booted'
            )
        raise AmbiguousJapaneseRdram(matches)
    base, endian = next(iter(matches))
    return validate_rdram_base(process, base, endian, probes), base, endian

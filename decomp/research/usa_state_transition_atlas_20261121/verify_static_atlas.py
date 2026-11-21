"""Read-only original-USA dispatch/state-transition audit.

No emulator memory writes, ROM patches, extracted assembly, toolchain or assets.
Only original pointers and instruction *properties* are checked at fixed offsets.
The script deliberately makes no dynamic reachability claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
USA_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
STATE_SETTER_VMA = 0x80003728
STATE_INCREMENT_VMA = 0x8000378C
FILE_LOADER_VMA = 0x80001C00
ROM_SIZE = 33554432

# Original immediate-loading instruction address for each recorded original direct call.
# Annotations are evidence anchors, not executable C or reconstructed ASM.
LOADER_A0_AT = {
    0x2D7C: 0x2D80, 0x2FB8: 0x2F8C, 0x3080: 0x3070,
    0x3170: 0x3174, 0x3710: 0x3714, 0x3D64: 0x3D68,
}
INCREMENT_SITES = {0x2D20, 0x2E14, 0x2E34, 0x2F54}


def word_at(rom: bytes | bytearray | memoryview, offset: int) -> int:
    return struct.unpack_from('>I', rom, offset)[0]


def jal_target(word: int, pc: int) -> int | None:
    if word >> 26 != 0x03:
        return None
    return (((pc + 4) & 0xF0000000) | ((word & 0x03FFFFFF) << 2)) & 0xFFFFFFFF


def loads_a0_literal(word: int, value: int) -> bool:
    # addiu/ori a0, zero, value -- no assumption about other register writes
    return ((word >> 26) in (0x09, 0x0D)
            and (word >> 21) & 31 == 0
            and (word >> 16) & 31 == 4
            and word & 0xFFFF == value)


def check_atlas(rom: bytes, atlas: dict, check_sha: bool = True) -> dict:
    if len(rom) != ROM_SIZE:
        raise ValueError(f'expected {ROM_SIZE} expanded USA ROM bytes; got {len(rom)}')
    digest = hashlib.sha1(rom).hexdigest()
    if check_sha and digest != USA_SHA1:
        raise ValueError(f'wrong USA expanded ROM SHA1 {digest}')

    checks: list[dict] = []
    def check(condition: bool, label: str, offset: int) -> None:
        if not condition:
            raise ValueError(f'original ROM property mismatch: {label} at 0x{offset:X}')
        checks.append({'kind': label, 'rom_offset': f'0x{offset:X}'})

    tables = [
        (0x59508, [int(s['handler_vma'], 16) for s in atlas['states']], 'outer pointer table'),
        (0x7B48C, [int(x, 16) for x in atlas['state15_dispatch']['entry_vmas']], 'state15 pointer table'),
        (0x6A9850, [0x801CB4BC, 0x801CB53C], 'file22 overlay pointer table'),
    ]
    for start, values, label in tables:
        found = struct.unpack_from(f'>{len(values)}I', rom, start)
        check(list(found) == values, label, start)

    entries = []
    for s in atlas['states']:
        for e in s['direct_setter_calls']:
            call = int(e['call_rom_offset'], 16)
            arg = int(e['arg_instruction_offset'], 16)
            value = e['target_state']
            check(jal_target(word_at(rom, call), call + 0x80000000 - 0xC00) == STATE_SETTER_VMA,
                  f'outer setter state={s["state"]} to={value}', call)
            check(loads_a0_literal(word_at(rom, arg), value),
                  f'setter a0 load state={s["state"]} target={value}', arg)
            entries.append((s['state'], value, call))
        for offset_hex in s['increment_helper_calls']:
            site = int(offset_hex, 16)
            check(jal_target(word_at(rom, site), site + 0x80000000 - 0xC00)
                  == STATE_INCREMENT_VMA, 'outer increment helper', site)

    assert len(entries) == 20 and sum(len(s['increment_helper_calls']) for s in atlas['states']) == 4
    for s in atlas['states']:
        for e in s['loader_requests']:
            call = int(e['call_rom_offset'], 16)
            a0_off = LOADER_A0_AT[call]
            check(jal_target(word_at(rom, call), call + 0x80000000 - 0xC00)
                  == FILE_LOADER_VMA, f'file loader state={s["state"]}', call)
            check(loads_a0_literal(word_at(rom, a0_off), e['file_id']),
                  f'file ID {e["file_id"]} loaded into a0', a0_off)

    # State-3 calls file_22's active overlay entry (ROM offset not VMA of target).
    check(jal_target(word_at(rom, 0x30A8), 0x800024A8) == 0x801CB460,
          'state3 invokes overlay dispatcher', 0x30A8)
    # 0x801CB460 entry copies two pointers then indexes SYS_W+0x3ADD6.
    check((word_at(rom, 0x69E0B4) >> 26) == 0x24 and (word_at(rom, 0x69E0B4) & 0xFFFF) == 0xADD6,
          'file22 reads nested selector', 0x69E0B4)

    # State15 guards 5-entry secondary table, while outer 18-entry table has no local guard.
    guard = word_at(rom, 0x3D08)
    check((guard >> 26) == 0x0B and (guard & 0xFFFF) == 5,
          'state15 accepts five substates', 0x3D08)
    check(jal_target(word_at(rom, 0x3D64), 0x80003164) == FILE_LOADER_VMA,
          'state15 file15 request', 0x3D64)
    # Explicit file22 writes outer state via sb at offset 0x3ADD4 and resets +0x3ADD6.
    direct = word_at(rom, 0x69E1D8)
    check((direct >> 26) == 0x28 and ((direct >> 16) & 31) == 8
          and (direct & 0xFFFF) == 0xADD4,
          'file22 direct outer-state store', 0x69E1D8)
    reset = word_at(rom, 0x69E1E8)
    check((reset >> 26) == 0x28 and ((reset >> 16) & 31) == 0
          and (reset & 0xFFFF) == 0xADD6,
          'file22 reset nested selector', 0x69E1E8)
    check(loads_a0_literal(word_at(rom, 0x69E1D0), 4) is False,
          'file22 state value not fabricated as a0 argument', 0x69E1D0)
    # Exact destination register t0 is encoded in instruction at 0x69E1D0.
    t0 = word_at(rom, 0x69E1D0)
    check((t0 >> 26) == 9 and ((t0 >> 21) & 31) == 0
          and ((t0 >> 16) & 31) == 8 and (t0 & 0xFFFF) == 4,
          'file22 explicit outer state=4', 0x69E1D0)
    mask = word_at(rom, 0x69E184)
    check((mask >> 26) == 0x0C and (mask & 0xFFFF) == 0x9000,
          'file22 event-condition mask', 0x69E184)
    # The overlay path does not execute the canonical setter, and can leave
    # dependent state bytes untouched. This conclusion is local to the visible
    # branch, not a whole-program property.
    return {
        'status': 'PASS_STATIC_ROM_PROPERTIES',
        'region': 'usa', 'rom_sha1': digest, 'rom_bytes': len(rom),
        'checks': len(checks), 'direct_setter_sites': len(entries),
        'outer_increment_helper_sites': len(INCREMENT_SITES),
        'known_loader_request_sites': sum(len(s['loader_requests']) for s in atlas['states']),
        'tables': {'outer': 18, 'state15': 5, 'file22': 2},
        'direct_edges': [list(e) for e in entries],
        'note': 'Static read-only properties only; no dynamic game execution',
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--rom', required=True, type=Path, help='Private expanded original USA ROM, never exported')
    p.add_argument('--report', type=Path, help='Optional sanitized JSON output (no ROM code/data)')
    args = p.parse_args()
    atlas = json.loads((HERE / 'state_atlas.json').read_text())
    outcome = check_atlas(args.rom.read_bytes(), atlas)
    print(json.dumps(outcome, indent=2))
    if args.report:
        args.report.write_text(json.dumps(outcome, indent=2) + '\n')

if __name__ == '__main__':
    main()

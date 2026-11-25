"""Read-only map and Fortune Doll flags from instantiated USA room definitions."""
import argparse
import json
import math
from pathlib import Path
import struct

from practice.entrances import RomFiles, MAX_STAGE, ROOM_POINTERS, CODE_RAM

ACTORS = {0x86: 'Mr. Elly Fant', 0x87: 'Mr. Arrow',
          0x88: 'Silver Fortune Doll', 0x89: 'Gold Fortune Doll'}
KINDS = {'maps': frozenset((0x86,0x87)), 'dolls': frozenset((0x88,0x89)),
         'all': frozenset(ACTORS)}


def room_pickups(stage, file_id, room, instance, footer, ending, *, actor_ids=None):
    actor_ids = KINDS['maps'] if actor_ids is None else frozenset(actor_ids)
    if not actor_ids or not actor_ids <= set(ACTORS):raise ValueError('Unsupported pickup actor selection')
    if not (0 <= instance <= footer < ending <= len(room)) or instance % 16 or ending-footer != 28:
        raise ValueError('Invalid room layout')
    cells = math.prod(struct.unpack_from('>HHH', room, footer+20))
    if cells > 0x10000 or ending+4*cells > len(room):
        raise ValueError('Invalid instance grid')
    starts = {instance}
    for offset in range(ending, ending+4*cells, 4):
        pointer = struct.unpack_from('>I', room, offset)[0]
        if pointer:
            if pointer >> 16 != 0x800:
                raise ValueError('Invalid group pointer')
            starts.add(pointer & 0xFFFF)
    used = set()
    for start in starts:
        if not instance <= start < footer:
            raise ValueError('Instance group outside room')
        offset = start
        while offset+20 <= footer:
            record = room[offset:offset+20]
            offset += 20
            if not any(record):
                break
            if record[12:14] != b'\x08\x00':
                raise ValueError('Invalid instance header')
            definition = int.from_bytes(record[14:16], 'big')
            if definition % 16 or definition+16 > instance:
                raise ValueError('Invalid definition pointer')
            used.add(definition//16)
        else:
            raise ValueError('Missing group terminator')
    rows = []
    for index in sorted(used):
        record = room[index*16:index*16+16]
        actor = int.from_bytes(record[:2], 'big')
        if actor not in actor_ids:
            continue
        flag = int.from_bytes(record[4:6], 'big')
        if not 0 <= flag < 800:
            raise ValueError('Pickup flag outside saved-event bank')
        rows.append(dict(stage=stage, file_id=file_id, definition=index,
                         actor_id=actor, pickup=ACTORS[actor], flag_id=flag,
                         address=f'0x{0x8015C608+(flag>>3):08X}', mask=f'0x{1<<(flag&7):02X}'))
    return rows


def extract(data, *, kind='maps'):
    if kind not in KINDS:raise ValueError('Unsupported pickup kind')
    files = RomFiles(data)  # Validates the complete retail/decompressed ROM hash.
    code = files.file(12)
    rows = []
    for stage in range(MAX_STAGE+1):
        pointer = struct.unpack_from('>I', code, ROOM_POINTERS+stage*4)[0]
        if not pointer:
            continue
        offset = (pointer & 0x7FFFFFFF)-CODE_RAM
        if not 0 <= offset <= len(code)-28:
            raise ValueError('Room metadata outside code file')
        meta = code[offset:offset+28]
        file_id = struct.unpack_from('>H', meta, 20)[0]
        if not file_id:
            continue
        if not 0x336 <= file_id <= 0x482:
            raise ValueError('Room file outside USA range')
        if any(struct.unpack_from('>H', meta, p)[0] != 0x800 for p in (8,12,16)) or meta[22:24] != bytes(2):
            raise ValueError('Unsupported room metadata')
        instance = struct.unpack_from('>H', meta, 10)[0]
        footer = struct.unpack_from('>H', meta, 18)[0]
        ending = struct.unpack_from('>H', meta, 14)[0]
        rows.extend(room_pickups(stage, file_id, files.file(file_id), instance, footer, ending, actor_ids=KINDS[kind]))
    return dict(format='goemon-pickup-placements-v1', rom_sha1=files.sha1,
                source='Instantiated room definitions; actor flag at definition bytes 4..5', kind=kind,
                live_verified=False, pickups=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--kind', choices=tuple(KINDS), default='maps')
    parser.add_argument('--report', type=Path, required=True, help='New local metadata report')
    args = parser.parse_args()
    try:
        if args.rom.resolve() == args.report.resolve():
            raise ValueError('Report must differ from ROM')
        result = extract(args.rom.read_bytes(),kind=args.kind)
        with args.report.open('x', encoding='utf-8') as output:
            json.dump(result, output, indent=2)
            output.write('\n')
    except (OSError, ValueError, struct.error) as exc:
        parser.exit(1, str(exc)+'\n')
    print(f'{len(result["pickups"])} instantiated pickups; no live test claimed')


if __name__ == '__main__':
    main()

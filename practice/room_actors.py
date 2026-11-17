"""Read-only USA ROM actor-placement browser; never claims live actor instances.

Uses the same verified ROM table and room metadata as the entrance atlas.
Room definitions are 16 bytes; each referenced placement occupies 20 bytes.
Spatial grid references can share a group, so each record is listed once.
No guest-RAM access, actor creation, or raw ROM data is persisted.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

from practice.entrances import (RomFiles, CODE_RAM, MAX_STAGE, ROOM_POINTERS,
                                US_RETAIL_SHA1, US_DECOMPRESSED_SHA1)

SCHEMA = 'goemon-usa-room-actors-v1'
KNOWN_NAMES = {
    0x086: 'Mr. Elly Fant', 0x087: 'Mr. Arrow', 0x088: 'Silver Fortune Doll',
    0x089: 'Gold Fortune Doll', 0x08C: 'Exit', 0x193: 'Key',
    0x23E: 'Locked Door', 0x306: 'Plasma',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def actor_names(catalog=None):
    """Return (name, provenance) by ID; optional external leads are NOT verified."""
    names = {i: (name, 'code/room annotation') for i, name in KNOWN_NAMES.items()}
    if catalog is None:
        catalog = Path(__file__).resolve().parents[1] / 'research' / 'usa_external_memory_leads.json'
    try:
        parsed = json.loads(Path(catalog).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return names
    for row in parsed.get('external_actor_ids', []):
        if row.get('status') != 'EXTERNAL_UNVERIFIED':
            continue
        actor_id = int(row['actor_id'], 16)
        if 0 <= actor_id <= 0xFFFF and actor_id not in names:
            names[actor_id] = (row['label'], 'external/unverified')
    return names


def parse_room(stage, file_id, room, instance, footer, ending, *, names=None):
    """Decode referenced placement RECORDS, including repeated actor definitions.

    Each unique group is scanned once. cells shows all grid cells that reference
    the group, where -1 marks the room's unconditional/base group.
    """
    if not (0 <= instance <= footer < ending <= len(room)) or instance % 16 or ending-footer != 28:
        raise ValueError(f'Invalid actor room bounds for stage {stage}')
    if not (0 <= stage <= MAX_STAGE) or not (0x336 <= file_id <= 0x482):
        raise ValueError('Invalid stage or USA room file ID')
    dims = struct.unpack_from('>HHH', room, footer+20)
    cell_count = math.prod(dims)
    if cell_count > 0x10000 or ending+4*cell_count > len(room):
        raise ValueError('Invalid room spatial grid')
    groups = {instance: {-1}}
    for cell in range(cell_count):
        address = struct.unpack_from('>I', room, ending+4*cell)[0]
        if not address:
            continue
        if address >> 16 != 0x800:
            raise ValueError('Invalid actor group pointer prefix')
        group_offset = address & 0xFFFF
        if not instance <= group_offset < footer or group_offset % 4:
            raise ValueError('Actor group pointer outside instance region')
        groups.setdefault(group_offset, set()).add(cell)

    names = actor_names() if names is None else names
    placements = []
    for group_offset, cells in sorted(groups.items()):
        offset = group_offset
        while True:
            if offset+20 > footer:
                raise ValueError('Unterminated room actor group')
            record = room[offset:offset+20]
            if not any(record):
                break
            if record[12:14] != b'\x08\x00':
                raise ValueError('Invalid actor instance record header')
            definition_offset = struct.unpack_from('>H', record, 14)[0]
            if definition_offset % 16 or definition_offset+16 > instance:
                raise ValueError('Invalid actor definition reference')
            actor_id = struct.unpack_from('>H', room, definition_offset)[0]
            label, provenance = names.get(actor_id, (f'Actor 0x{actor_id:03X}', 'unknown'))
            placements.append(dict(
                stage=stage, room_file=file_id, actor_id=actor_id, name=label,
                name_source=provenance, definition=definition_offset//16,
                group_offset=group_offset, record_offset=offset,
                cells=sorted(cells),
            ))
            offset += 20
    return placements


def extract_actors(data, *, catalog=None):
    files = RomFiles(data)  # Full USA retail/expanded image SHA-1 gate.
    code = files.file(12)
    names = actor_names(catalog)
    rooms = []
    placements = []
    for stage in range(MAX_STAGE+1):
        table_offset = ROOM_POINTERS+4*stage
        if table_offset+4 > len(code):
            raise ValueError('Truncated room metadata pointer table')
        pointer = struct.unpack_from('>I', code, table_offset)[0]
        if not pointer:
            continue
        meta_offset = (pointer & 0x7FFFFFFF)-CODE_RAM
        if not 0 <= meta_offset <= len(code)-28:
            raise ValueError('Room metadata pointer outside code file')
        meta = code[meta_offset:meta_offset+28]
        file_id = struct.unpack_from('>H', meta, 20)[0]
        if not file_id:
            continue
        if not 0x336 <= file_id <= 0x482:
            raise ValueError('Room file ID outside USA stage range')
        if any(struct.unpack_from('>H', meta, p)[0] != 0x800 for p in (8, 12, 16)) or meta[22:24] != b'\0\0':
            raise ValueError('Unsupported room metadata pointers')
        instance, ending, footer = (struct.unpack_from('>H', meta, p)[0] for p in (10, 14, 18))
        stage_rows = parse_room(stage, file_id, files.file(file_id), instance, footer, ending, names=names)
        rooms.append(dict(stage=stage, room_file=file_id, count=len(stage_rows)))
        placements.extend(stage_rows)
    payload = dict(format=SCHEMA, region='usa', rom_sha1=files.sha1,
                   evidence='Static ROM room placement references; NOT live spawned actors',
                   rooms=rooms, placements=placements)
    return dict(payload=payload, sha256=digest(payload))


def validate_actors(atlas):
    if not isinstance(atlas, dict) or not isinstance(atlas.get('payload'), dict):
        raise ValueError('Invalid actor atlas')
    p = atlas['payload']
    if p.get('format') != SCHEMA or p.get('region') != 'usa' or p.get('rom_sha1') not in (US_RETAIL_SHA1, US_DECOMPRESSED_SHA1):
        raise ValueError('Wrong actor atlas schema or region')
    if atlas.get('sha256') != digest(p):
        raise ValueError('Actor atlas checksum mismatch')
    rooms = p.get('rooms')
    rows = p.get('placements')
    if not isinstance(rooms, list) or not isinstance(rows, list):
        raise ValueError('Invalid actor atlas collections')
    counts = {}
    for room in rooms:
        stage, file_id, count = room['stage'], room['room_file'], room['count']
        if type(stage) is not int or not 0 <= stage <= MAX_STAGE or stage in counts or type(file_id) is not int or not 0x336 <= file_id <= 0x482 or type(count) is not int or count < 0:
            raise ValueError('Invalid actor room entry')
        counts[stage] = (file_id, count)
    seen = set()
    totals = {stage: 0 for stage in counts}
    for row in rows:
        stage, file_id, actor_id = row['stage'], row['room_file'], row['actor_id']
        if type(stage) is not int or stage not in counts or file_id != counts[stage][0] or type(actor_id) is not int or not 0 <= actor_id <= 65535:
            raise ValueError('Invalid actor placement identity')
        group, record, definition = row['group_offset'], row['record_offset'], row['definition']
        cells = row['cells']
        if any(type(n) is not int or not 0 <= n <= 0xFFFF for n in (group, record, definition)) or not isinstance(cells, list) or not cells or any(type(n) is not int or not -1 <= n <= 65535 for n in cells) or cells != sorted(set(cells)):
            raise ValueError('Invalid actor placement references')
        key = (stage, group, record)
        if key in seen:
            raise ValueError('Duplicate placement')
        seen.add(key)
        if not isinstance(row.get('name'), str) or not isinstance(row.get('name_source'), str):
            raise ValueError('Invalid actor placement label')
        totals[stage] += 1
    if any(totals[stage] != counts[stage][1] for stage in counts):
        raise ValueError('Incorrect per-room actor counts')
    return atlas


def actors_for_stage(atlas, stage):
    if atlas is None or type(stage) is not int:
        return []
    return [row for row in atlas['payload']['placements'] if row['stage'] == stage]


def save_actors(path, atlas):
    validate_actors(atlas)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Cache metadata only. Never copy the user's ROM or raw placement bytes.
    import os
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, prefix='.actor-', suffix='.tmp', delete=False) as f:
        temp = Path(f.name)
        try:
            json.dump(atlas, f, indent=2)
            f.write('\n')
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def load_actors(path):
    try:
        atlas = json.loads(Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        return None
    return validate_actors(atlas)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True, help='Original USA retail or verified expanded ROM')
    stages = parser.add_mutually_exclusive_group(required=True)
    stages.add_argument('--stage', type=int, help='Stage ID in decimal')
    stages.add_argument('--all', action='store_true', help='Show all mapped stages')
    parser.add_argument('--report', type=Path, help='Write a local metadata-only JSON atlas')
    args = parser.parse_args(argv)
    try:
        atlas = extract_actors(args.rom.read_bytes())
        if args.report:
            if args.report.resolve() == args.rom.resolve():
                raise ValueError('Cannot overwrite the input ROM')
            save_actors(args.report, atlas)
        if args.stage is not None and not 0 <= args.stage <= MAX_STAGE:
            raise ValueError('Stage outside USA range')
        selected = (atlas['payload']['rooms'] if args.all else [r for r in atlas['payload']['rooms'] if r['stage'] == args.stage])
        for room in selected:
            print(f'Stage {room["stage"]}: file 0x{room["room_file"]:03X}, {room["count"]} ROM placements (NOT live actors)')
            for p in actors_for_stage(atlas, room['stage']):
                print(f'  0x{p["actor_id"]:03X} {p["name"]} [{p["name_source"]}] definition {p["definition"]} record 0x{p["record_offset"]:04X} cells {p["cells"]}')
    except (OSError, ValueError, KeyError, TypeError, struct.error) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()

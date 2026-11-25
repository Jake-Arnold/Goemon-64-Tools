"""Extract Plasma's US dialogue flag checks without exporting game text/assets."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
from practice.entrances import RomFiles, ROOM_POINTERS, CODE_RAM

STAGES = (423, 424, 425, 426)
EVENT_ID = 0x288
SCRIPT_FILE = 0x70
SCRIPT_ENTRY = 0x08002F98
SCENARIO_SHA256 = 'ac955eeb226edf51e2fc5c1bad504159037b00411585dc2ce450b395a01ac306'
ADVICE_START = 0x3208
ADVICE_END = 0x3DC0
DECOMPRESSED_FILE_START = 0x79EA30


def flag_location(flag_id):
    if not 0 <= flag_id < 800: raise ValueError('Flag outside saved event bank')
    return f'0x{0x8015C608 + (flag_id >> 3):08X}', f'0x{1 << (flag_id & 7):02X}'


def instantiated_actor_messages(room, instance, footer, end, actor):
    """Find messages only on definitions referenced by room instance groups."""
    if not (0 <= instance <= footer < end <= len(room)) or instance % 16 or end-footer != 28:
        raise ValueError('Invalid room layout')
    cells = math.prod(struct.unpack_from('>HHH', room, footer + 20))
    if cells > 0x10000 or end + 4*cells > len(room): raise ValueError('Invalid room grid')
    starts = {instance}
    for offset in range(end, end + 4*cells, 4):
        pointer = struct.unpack_from('>I', room, offset)[0]
        if pointer:
            if pointer >> 16 != 0x800: raise ValueError('Invalid instance group pointer')
            starts.add(pointer & 0xFFFF)
    used = set()
    for start in starts:
        if not instance <= start < footer: raise ValueError('Instance group outside room')
        for offset in range(start, footer-19, 20):
            record = room[offset:offset+20]
            if len(record) != 20: raise ValueError('Incomplete instance')
            if not any(record): break
            if record[12:14] != b'\x08\x00': raise ValueError('Invalid instance header')
            definition = int.from_bytes(record[14:16], 'big')
            if definition % 16 or definition + 16 > instance: raise ValueError('Invalid definition pointer')
            used.add(definition//16)
        else: raise ValueError('Unterminated instance group')
    return [dict(definition=i, message=struct.unpack_from('>H',room,i*16+10)[0])
            for i in sorted(used) if struct.unpack_from('>H',room,i*16)[0] == actor]


def scan_advice(script):
    """List aligned flag-opcode candidates in the bounded, identified advice region."""
    if len(script) < ADVICE_END: raise ValueError('Truncated Plasma script')
    if struct.unpack_from('>II', script, 0x319C) != (0x800A, 0x08003208):
        raise ValueError('Plasma advice entry jump does not match')
    rows = []
    for offset in range(ADVICE_START, ADVICE_END, 4):
        opcode = struct.unpack_from('>I',script,offset)[0]
        if opcode not in (0x8020, 0x8021, 0x8022): continue
        flag = struct.unpack_from('>I',script,offset+4)[0]
        address,mask=flag_location(flag)
        row=dict(file_offset=f'0x{offset:04X}',rom_offset=f'0x{DECOMPRESSED_FILE_START+offset:X}',
                 flag_id=f'0x{flag:03X}',address=address,mask=mask,
                 operation={0x8020:'set',0x8021:'clear',0x8022:'branch_if_set'}[opcode])
        if opcode == 0x8022:
            target=struct.unpack_from('>I',script,offset+8)[0]
            if target >> 24 != 8 or not ADVICE_START <= (target & 0xFFFFFF) < ADVICE_END:
                raise ValueError('Unexpected Plasma branch target')
            row['target_file_offset']=f'0x{target & 0xFFFFFF:04X}'
        rows.append(row)
    if sum(x['operation']=='branch_if_set' for x in rows)!=40 or sum(x['operation']=='set' for x in rows)!=11 or any(x['operation']=='clear' for x in rows):
        raise ValueError('Plasma flag-opcode inventory changed')
    return rows


def extract(data):
    files=RomFiles(data)
    entry=struct.unpack_from('>I',files.data,0x785A0+EVENT_ID*4)[0]
    script_file=struct.unpack_from('>h',files.data,0x79208+EVENT_ID*2)[0]
    if (entry,script_file)!=(SCRIPT_ENTRY,SCRIPT_FILE): raise ValueError('Plasma event mapping changed')
    script=files.file(script_file)
    if hashlib.sha256(script).hexdigest()!=SCENARIO_SHA256: raise ValueError('Unexpected Plasma scenario file')
    code=files.file(12);rooms=[]
    for stage in STAGES:
        pointer=struct.unpack_from('>I',code,ROOM_POINTERS+stage*4)[0]
        offset=(pointer & 0x7FFFFFFF)-CODE_RAM
        if not pointer or not 0<=offset<=len(code)-28: raise ValueError('Invalid room metadata')
        meta=code[offset:offset+28]
        if any(struct.unpack_from('>H',meta,x)[0]!=0x800 for x in (8,12,16)):
            raise ValueError('Unsupported room layout')
        instance, end, footer, file_id=(struct.unpack_from('>H',meta,x)[0] for x in (10,14,18,20))
        actors=instantiated_actor_messages(files.file(file_id),instance,footer,end,0x306)
        if len(actors)!=1 or actors[0]['message']!=EVENT_ID: raise ValueError('Unexpected Plasma actor binding')
        rooms.append(dict(stage=stage,room_file=f'0x{file_id:03X}',definition=actors[0]['definition'],event_id=f'0x{EVENT_ID:03X}'))
    rows=scan_advice(script)
    return dict(format='goemon-plasma-conditions-v1',scenario_file=f'0x{SCRIPT_FILE:03X}',scenario_sha256=SCENARIO_SHA256,
                event_id=f'0x{EVENT_ID:03X}',event_entry=f'0x{SCRIPT_ENTRY:08X}',rooms=rooms,
                flag_checks=sum(r['operation']=='branch_if_set' for r in rows),
                distinct_checked_flags=len({r['flag_id'] for r in rows if r['operation']=='branch_if_set'}),
                set_operations=sum(r['operation']=='set' for r in rows),operations=rows,
                limitation='Aligned opcode candidates in one verified event region; reachability and full state semantics require further validation')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.rom.resolve()==args.report.resolve(): raise ValueError('Report must differ from ROM')
        result=extract(args.rom.read_bytes())
        with args.report.open('x',encoding='utf-8') as stream:
            json.dump(result,stream,indent=2);stream.write('\n')
    except (OSError,ValueError,struct.error) as exc:parser.exit(1,f'{exc}\n')
    print(f"{result['flag_checks']} checks / {result['distinct_checked_flags']} flags / {result['set_operations']} sets")

if __name__=='__main__':main()

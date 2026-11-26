"""Experimental Project64-only frame control; controller polls are not game frames."""
from __future__ import annotations

import json
from pathlib import Path
import re
import socket
import struct
import csv

from practice.address_registry import guest_address

BUTTONS = {'A': 0x8000, 'B': 0x4000, 'Z': 0x2000, 'START': 0x1000,
           'UP': 0x0800, 'DOWN': 0x0400, 'LEFT': 0x0200, 'RIGHT': 0x0100,
           'L': 0x0020, 'R': 0x0010, 'CU': 8, 'CD': 4, 'CL': 2, 'CR': 1}
CRCS = {'usa': (0xFCBCCB21, 0x72903C6B), 'japan': (0x832C168B, 0x56A2CDAE)}


def parse_inputs(text: str, count: int, default: dict, *, max_count: int = 60) -> list[dict]:
    """Relative offset (1-based), buttons joined by +, X, Y; unspecified uses default."""
    if type(count) is not int or not 1 <= count <= max_count:
        raise ValueError(f'Step count must be 1..{max_count}')
    result = [dict(default) for _ in range(count)]
    seen = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        off, buttons, x, y = line.split()
        n = int(off)
        if not 1 <= n <= count or n in seen:
            raise ValueError('Timeline offsets must be unique and within the step count')
        seen.add(n)
        names = [] if buttons == '-' else buttons.upper().split('+')
        if any(name not in BUTTONS for name in names):
            raise ValueError('Unknown N64 button')
        result[n - 1] = controller_input(names, int(x), int(y))
    return result


def controller_input(names, x: int, y: int) -> dict:
    if type(x) is not int or type(y) is not int or not (-80 <= x <= 80 and -80 <= y <= 80):
        raise ValueError('Stick coordinates must be integers from -80 to 80')
    mask = 0
    for name in names:
        mask |= BUTTONS[name]
    return {'buttons': mask, 'x': x, 'y': y}


def validate_connection(port: int, token: str):
    if type(port) is not int or not 1024 <= port <= 65535:
        raise ValueError('Port must be 1024..65535')
    if not re.fullmatch(r'[0-9a-f]{32}', token):
        raise ValueError('Expected a 32-character hexadecimal session token')


WATCH_TYPES = {'u8': 1, 'u16': 2, 'u32': 4, 'f32': 4}
TRACE_COLUMNS = ('step', 'phase', 'buttons', 'x', 'y', 'polls')
TRACE_METADATA = ('region', 'mode', 'pc', 'watches', 'trap')


def parse_watches(text, region):
    """Explicit addresses or @catalogue IDs; never infer dynamic pointers."""
    watches = []
    for line in text.splitlines():
        if not line.strip():
            continue
        name, kind, address = line.split()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,23}', name) or kind not in WATCH_TYPES:
            raise ValueError('Watch format: name u8/u16/u32/f32 address or @catalogue_id')
        width = WATCH_TYPES[kind]
        if address.startswith('@'):
            ids = address[1:].split('|')
            if len(ids) not in (1, 2):
                raise ValueError('Catalogue mapping: @usa_id|japan_id')
            addr = guest_address(ids[0 if len(ids) == 1 or region == 'usa' else 1], region=region, width=width)
        else:
            addr = int(address, 16)
        if not 0x80000000 <= addr <= 0x80400000 - width or addr % width:
            raise ValueError('Watch must be aligned within the first 4 MiB of guest RAM')
        if name in TRACE_COLUMNS + TRACE_METADATA + ('error',) or len(watches) >= 12 or any(w['name'] == name for w in watches):
            raise ValueError('Maximum 12 unique watch names')
        watches.append(dict(name=name, kind=kind, address=addr))
    return watches


def decoded_watch(watch, word):
    if word is None:
        return None
    if type(word) is not int or not 0 <= word <= 0xFFFFFFFF:
        raise ValueError('Invalid raw watch word')
    width = WATCH_TYPES[watch['kind']]
    value = (word >> ((4 - width - watch['address'] % 4) * 8)) & ((1 << (width * 8)) - 1)
    if watch['kind'] == 'f32':
        return format(struct.unpack('>f', value.to_bytes(4, 'big'))[0], '.9g')
    return value


def trace_rows(status):
    watches = status.get('watches', [])
    rows = []
    samples=status.get('trace', [])
    if not isinstance(samples,list) or len(samples)>600:
        raise ValueError('Invalid or oversized trace')
    for sample in samples:
        if len(sample['words']) != len(watches):
            raise ValueError('Trace sample/watch count mismatch')
        inp = sample['input'] or {}
        row = dict(step=sample['step'], phase=sample['phase'], buttons=inp.get('buttons'), x=inp.get('x'), y=inp.get('y'), polls=sample['polls'])
        row.update({w['name']: decoded_watch(w, v) for w, v in zip(watches, sample['words'])})
        rows.append(row)
    return rows


def export_trace(path, status):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        rows = trace_rows(status)
        with path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['region', 'mode', 'pc', 'error'] + list(TRACE_COLUMNS) + [w['name'] for w in status['watches']])
            writer.writeheader(); writer.writerows(dict(row, **{k:status[k] for k in ('region','mode','pc','error')}) for row in rows)
    else:
        path.write_text(json.dumps({k: status[k] for k in TRACE_METADATA + ('trace', 'error', 'hit')}, indent=2), encoding='utf-8')


def parse_trap(text, pc):
    if not text.strip():
        return None
    kind, value = text.split()
    address = int(value, 16)
    if kind not in ('exec', 'write') or not 0x80000000 <= address < 0x80400000 or (kind == 'exec' and (address % 4 or address == pc)):
        raise ValueError('Breakpoint: exec aligned_pc (not boundary) or write exact_address in first 4 MiB')
    return dict(kind=kind, address=address)


def append_trace(capture, status):
    # Append one completed batch without duplicating its baseline.
    if not status.get('trace') or status.get('pending') or status.get('batchGeneration') != status['generation']:
        return capture
    if capture is None:
        return {**{k:status[k] for k in TRACE_METADATA}, 'epoch':status['epoch'], 'generation':status['generation'],
                'trace':list(status['trace']), 'error':status['error'], 'hit':status['hit']}
    if any(capture[k] != status[k] for k in TRACE_METADATA + ('epoch',)):
        raise ValueError('Recording session changed; export before starting another')
    if capture['generation'] == status['generation']:
        return capture
    old, new = capture['trace'], status['trace']
    if new[0]['phase'] != 'baseline' or old[-1]['step'] != new[0]['step'] or old[-1]['words'] != new[0]['words']:
        raise ValueError('Recording discontinuity; previous capture retained')
    if len(old) + len(new) - 1 > 600:
        raise ValueError('Recording limit of 600 samples reached; export previous capture')
    return {**capture, 'generation':status['generation'], 'trace':old + new[1:], 'error':status['error'], 'hit':status['hit']}


def export_script(region: str, port: int, token: str, pc: str = '', watches: str = '', trap: str = '') -> str:
    validate_connection(port, token)
    crc1, crc2 = CRCS[region]
    address = int(pc, 16) if pc.strip() else 0
    if pc.strip() and (address < 0x80000000 or address >= 0x80800000 or address % 4):
        raise ValueError('Execution hook must be an aligned KSEG0 RDRAM PC')
    config = dict(region=region, crc1=crc1, crc2=crc2, port=port, token=token, pc=address, watches=parse_watches(watches, region), trap=parse_trap(trap, address))
    template = Path(__file__).with_name('pj64_frame_bridge.js').read_text(encoding='utf-8')
    return template.replace('__GOEMON_CONFIG__', json.dumps(config), 1)


def request(port: int, token: str, op: str, **fields) -> dict:
    validate_connection(port, token)
    payload = json.dumps(dict(version=1, token=token, op=op, **fields)).encode() + b'\n'
    with socket.create_connection(('127.0.0.1', port), timeout=1.0) as sock:
        sock.sendall(payload)
        with sock.makefile('rb') as stream:
            raw = stream.readline(16385)
    if len(raw) > 16384 or not raw.endswith(b'\n'):
        raise ValueError('Incomplete or oversized bridge response')
    response = json.loads(raw)
    if response.get('ok') is not True:
        raise ValueError(response.get('error', 'Bridge rejected request'))
    status = response.get('status')
    if not isinstance(status, dict) or status.get('version') != 1:
        raise ValueError('Incompatible bridge protocol')
    return status

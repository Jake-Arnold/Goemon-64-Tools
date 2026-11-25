"""Experimental Project64-only frame control; controller polls are not game frames."""
from __future__ import annotations

import json
from pathlib import Path
import re
import socket

BUTTONS = {'A': 0x8000, 'B': 0x4000, 'Z': 0x2000, 'START': 0x1000,
           'UP': 0x0800, 'DOWN': 0x0400, 'LEFT': 0x0200, 'RIGHT': 0x0100,
           'L': 0x0020, 'R': 0x0010, 'CU': 8, 'CD': 4, 'CL': 2, 'CR': 1}
CRCS = {'usa': (0xFCBCCB21, 0x72903C6B), 'japan': (0x832C168B, 0x56A2CDAE)}


def parse_inputs(text: str, count: int, default: dict) -> list[dict]:
    """Relative offset (1-based), buttons joined by +, X, Y; unspecified uses default."""
    if type(count) is not int or not 1 <= count <= 60:
        raise ValueError('Step count must be 1..60')
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


def export_script(region: str, port: int, token: str, pc: str = '') -> str:
    validate_connection(port, token)
    crc1, crc2 = CRCS[region]
    address = int(pc, 16) if pc.strip() else 0
    if pc.strip() and (address < 0x80000000 or address >= 0x80800000 or address % 4):
        raise ValueError('Execution hook must be an aligned KSEG0 RDRAM PC')
    config = dict(region=region, crc1=crc1, crc2=crc2, port=port, token=token, pc=address)
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

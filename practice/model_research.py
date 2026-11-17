"""Bounded read-only F3DEX geometry probes for *explicit* Goemon ROM resources.

NOT an RT64 renderer, actor/model database, or complete F3DEX emulator. This
extracts vertex positions/vertex colours from selected ROM file/command spans
for research while Goemon64Recomp's RT64 inspector remains the rendering truth.
No automatic actor ID -> file ID mapping is assumed or persisted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import struct

from practice.entrances import RomFiles
from practice.room_actors import JapanRomFiles

MAX_COMMANDS = 8192
MAX_FACES = 16384
MAX_DEPTH = 8
SEGMENT = 0x08


@dataclass(frozen=True)
class MeshProbe:
    # Each triangle consists of three (x, y, z) points in original Vtx space.
    triangles: tuple
    rgb: tuple
    commands: int
    vertex_loads: int
    opcodes: tuple
    warnings: tuple
    ended: bool

    @property
    def triangle_count(self):
        return len(self.triangles)

    @property
    def bounds(self):
        if not self.triangles:
            return None
        xyz = (p for tri in self.triangles for p in tri)
        xs, ys, zs = zip(*xyz)
        return ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)))

    def summary(self):
        return dict(
            triangles=self.triangle_count, commands=self.commands,
            vertex_loads=self.vertex_loads,
            opcodes={f'0x{k:02X}': v for k, v in self.opcodes},
            warnings=list(self.warnings), ended=self.ended,
            bounds=self.bounds,
            limitations='Vertex colour only; matrices, lighting, texture/TMEM, animation and culling not emulated.',
        )


def _validate_span(data, start, end):
    if type(start) is not int or type(end) is not int:
        raise ValueError('Command range must use integer offsets')
    if start < 0 or start >= end or end > len(data) or start % 8 or end % 8:
        raise ValueError('Display-list command range must be aligned, nonempty and within resource')
    if end - start > MAX_COMMANDS * 8:
        raise ValueError('Display-list command span exceeds bounded research budget')


def decode_geometry(data, start, end, *, max_commands=MAX_COMMANDS,
                    max_faces=MAX_FACES, max_depth=MAX_DEPTH):
    """Decode G_VTX/G_TRI1/G_TRI2/G_DL and G_ENDDL using RT64 F3DEX fields.

    Caller specifies the *exact research span*; it can start mid-list. Nested
    G_DL targets may be elsewhere in the same decompressed resource (segment 8).
    Commands that affect transform/lighting/texture are NOT applied. A warning
    is retained instead of asserting that the resulting geometry is complete.
    """
    _validate_span(data, start, end)
    if type(max_commands) is not int or not 1 <= max_commands <= MAX_COMMANDS:
        raise ValueError('Invalid command budget')
    if type(max_faces) is not int or not 1 <= max_faces <= MAX_FACES:
        raise ValueError('Invalid triangle budget')
    if type(max_depth) is not int or not 1 <= max_depth <= MAX_DEPTH:
        raise ValueError('Invalid display-list depth budget')

    cache = {}
    triangles = []
    rgb = []
    opcodes = Counter()
    warnings = set()
    command_count = 0
    vertex_loads = 0
    ended = False

    def address_to_offset(ptr, label, *, align):
        segment = ptr >> 24
        offset = ptr & 0x00FFFFFF
        if segment != SEGMENT or offset % align or offset >= len(data):
            raise ValueError(f'{label} must be an aligned segment-08 pointer into the resource')
        return offset

    def emit_tri(w):
        # RT64/src/gbi/rt64_gbi_f3dex.cpp: p(17,7), p(9,7), p(1,7).
        indices = ((w >> 17) & 0x7F, (w >> 9) & 0x7F, (w >> 1) & 0x7F)
        if not all(index in cache for index in indices):
            warnings.add('Triangle references vertices not loaded in the current F3DEX cache')
            return
        if len(triangles) >= max_faces:
            raise ValueError('Triangle budget exceeded')
        verts = [cache[index] for index in indices]
        triangles.append(tuple(v[0] for v in verts))
        rgb.append(tuple(sum(v[1][axis] for v in verts)//3 for axis in range(3)))

    # The root span can terminate by its explicit end instead of G_ENDDL.
    # Sub-lists terminate with G_ENDDL and return to the parent.
    stack = []
    offset = start
    while True:
        if not stack and offset >= end:
            break
        if offset < 0 or offset + 8 > len(data) or offset % 8:
            raise ValueError('Display-list command fetch outside resource')
        command_count += 1
        if command_count > max_commands:
            raise ValueError('Display-list command budget exceeded (possible loop)')
        w0, w1 = struct.unpack_from('>II', data, offset)
        opcode = w0 >> 24
        opcodes[opcode] += 1
        offset += 8
        if opcode == 0x04:  # F3DEX G_VTX; fields match RT64 F3DEX vertex().
            n = (w0 >> 10) & 0x3F
            v0 = (w0 >> 17) & 0x7F
            ptr = address_to_offset(w1, 'G_VTX', align=16)
            if not 1 <= n <= 32 or v0 + n > 32 or ptr + n * 16 > len(data):
                raise ValueError('Invalid F3DEX vertex load')
            for i in range(n):
                x, y, z, _flag, _u, _v, r, g, b, _a = struct.unpack_from('>hhhHhhBBBB', data, ptr+i*16)
                cache[v0+i] = ((x, y, z), (r, g, b))
            vertex_loads += 1
        elif opcode == 0xBF:  # F3DEX G_TRI1
            emit_tri(w1)
        elif opcode == 0xB1:  # F3DEX G_TRI2
            emit_tri(w0)
            emit_tri(w1)
        elif opcode == 0x06:  # G_DL
            branch_offset = address_to_offset(w1, 'G_DL', align=8)
            if (w0 >> 16) & 1:  # G_DL_NOPUSH
                offset = branch_offset
            else:
                if len(stack) >= max_depth:
                    raise ValueError('Nested display-list depth exceeded')
                stack.append(offset)
                offset = branch_offset
        elif opcode == 0xB8:  # G_ENDDL
            if stack:
                offset = stack.pop()
            else:
                ended = True
                break
        elif opcode == 0x01:
            warnings.add('Matrix commands encountered but not applied; use RT64 for transforms')
        # Many other RSP/RDP opcodes are intentionally skipped, never executed.
        else:
            continue
    if stack:
        raise ValueError('Nested display list did not return within command budget')
    if not ended:
        warnings.add('Research command range ended without G_ENDDL; geometry may be incomplete')
    if not triangles:
        warnings.add('No complete triangles decoded from this command range')
    warnings.add('Textures, material state and skeletal transforms require RT64; this is a vertex-colour geometry probe')
    return MeshProbe(tuple(triangles), tuple(rgb), command_count, vertex_loads,
                     tuple(sorted(opcodes.items())), tuple(sorted(warnings)), ended)


def extract_rom_probe(rom, region, file_id, start, end, **limits):
    """ROM ID/region are authenticated by region-specific file table readers."""
    if region == 'usa':
        files = RomFiles(rom)
    elif region == 'japan_0':
        files = JapanRomFiles(rom)
    else:
        raise ValueError('Unsupported region; expected usa or japan_0')
    if type(file_id) is not int or not 1 <= file_id <= 1310:
        raise ValueError('Invalid ROM file number')
    data = files.file(file_id)
    probe = decode_geometry(data, start, end, **limits)
    return dict(region=region, rom_sha1=files.sha1, file_id=file_id,
                resource_sha256=hashlib.sha256(data).hexdigest(),
                start=start, end=end, **probe.summary()), probe


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--region', choices=('usa', 'japan_0'), required=True)
    parser.add_argument('--file-id', type=int, required=True)
    parser.add_argument('--start', type=lambda s: int(s, 0), required=True)
    parser.add_argument('--end', type=lambda s: int(s, 0), required=True)
    args = parser.parse_args(argv)
    try:
        report, _mesh = extract_rom_probe(args.rom.read_bytes(), args.region,
                                          args.file_id, args.start, args.end)
        print(json.dumps(report, indent=2, sort_keys=True))
    except (OSError, ValueError, struct.error) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()

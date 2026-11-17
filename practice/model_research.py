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
SUPPORTED_SEGMENTS = (0x08, 0x09)
# Pinned by original USA and JP retail ROM file_11. First four u16 at USA
# overlay VMA 0x80204020 are g_character_graphics_file_ids, as named in
# Goemon64Recomp patches/variables.h. The adjacent four entries follow them.
PLAYER_TABLE_OFFSETS = {'usa': 0x38BC0, 'japan_0': 0x38380}
# These are confirmed small F3DEX *fragments*, not the root of a full actor.
# Each pair is (start, byte past the first G_ENDDL), with vertex data in seg 09.
PLAYER_FRAGMENT_SPANS = {
    'usa': ((0x25A8, 0x28C0), (0x24A8, 0x2670), (0x2B38, 0x2BB0), (0x2778, 0x2860)),
    'japan_0': ((0x2548, 0x2860), (0x2448, 0x2610), (0x2AD8, 0x2B50), (0x26F8, 0x27E0)),
}
EXPECTED_GRAPHICS_IDS = (0x120, 0x124, 0x128, 0x12C, 0x123, 0x127, 0x12B, 0x12F)


# Four original-USA skeleton display-list roots captured in Project64 with
# a0=0x80304BB0, a1=0x8014B0B0 in func_80018CA0_198A0. The graphics_1
# pointer (0x790047F8) resolves to segment-09 offset 0x47F8. The other three
# roots are consecutive 0x18-byte Skeleton records in this particular capture.
# Independently authenticated Japanese file-0x120 roots are 0x60 earlier.
# Not a stable Object RAM address, NPC actor mapping, full skeleton or animation.
PJ64_CAPTURED_LIMB_ROOTS_USA = (0x47F8, 0x4BB0, 0x4930, 0x4CD0)
PJ64_CAPTURED_LIMB_ROOTS_DELTA = {'usa': 0, 'japan_0': -0x60}
PJ64_CAPTURED_LIMB_FACES = (20, 20, 22, 22)
PJ64_CAPTURED_TEXTURE_REFS_USA = (0x0900B950, 0x0900B950, 0x0900C950, 0x0900C950)
PJ64_CAPTURED_PART_COLORS = ((208, 128, 103), (100, 184, 203),
                             (215, 181, 110), (153, 131, 212))


def extract_traced_player_limb_bundle(rom, region):
    """Replay four observed USA skeleton Gfx roots in authenticated regional file 0x120.

    A manual Project64 screenshot and the original ROMs prove these four
    display-list addresses. The resulting pieces are untransformed and do NOT
    reconstruct an actor's full mesh or verify an NPC actor type. No game RAM
    is required or modified; return metadata and a *coloured research* mesh.
    """
    if region not in PJ64_CAPTURED_LIMB_ROOTS_DELTA:
        raise ValueError('Captured skeleton is verified only for USA/Japan rev-0 ROM layout')
    files = RomFiles(rom) if region == 'usa' else JapanRomFiles(rom)
    player_refs = player_graphics_resources(files, region)
    if player_refs[0]['file_id'] != 0x120:
        raise ValueError('Captured skeleton source file differs from verified player resource table')
    data = files.file(0x120)
    delta = PJ64_CAPTURED_LIMB_ROOTS_DELTA[region]
    roots = tuple(offset + delta for offset in PJ64_CAPTURED_LIMB_ROOTS_USA)
    parts, meshes = [], []
    for index, (root, faces_expected, texture_ref, color) in enumerate(zip(
            roots, PJ64_CAPTURED_LIMB_FACES, PJ64_CAPTURED_TEXTURE_REFS_USA,
            PJ64_CAPTURED_PART_COLORS)):
        # Prove the display-list prologue and first texture reference instead
        # of guessing where a list begins in each region's decompressed file.
        if root < 0 or root + 16 > len(data):
            raise ValueError('Captured limb root lies outside original ROM resource')
        first, _zero, texture_opcode, texture_ptr = struct.unpack_from('>IIII', data, root)
        if first != 0xE7000000 or texture_opcode >> 24 != 0xFD:
            raise ValueError('Captured limb display-list prologue differs from verified ROM')
        if texture_ptr != texture_ref + delta:
            raise ValueError('Captured limb texture pointer differs from verified regional ROM')
        mesh = decode_geometry(data, root, min(root + 0x300, len(data) & ~7), segment=9)
        if not mesh.ended or mesh.triangle_count != faces_expected:
            raise ValueError('Captured limb display list is incomplete or geometry has changed')
        if any('not loaded' in message for message in mesh.warnings):
            raise ValueError('Captured limb references unresolved vertices')
        parts.append(dict(index=index, display_list=f'0x09{root:06X}',
                          resource_offset=root, first_texture_address=f'0x{texture_ptr:08X}',
                          triangles=mesh.triangle_count, commands=mesh.commands,
                          bounds=mesh.bounds))
        meshes.append(mesh)
    combined = MeshProbe(
        triangles=tuple(tri for mesh in meshes for tri in mesh.triangles),
        rgb=tuple(PJ64_CAPTURED_PART_COLORS[i] for i, mesh in enumerate(meshes)
                  for _ in mesh.triangles),
        commands=sum(m.commands for m in meshes),
        vertex_loads=sum(m.vertex_loads for m in meshes),
        opcodes=tuple(sorted(sum((Counter(dict(m.opcodes)) for m in meshes), Counter()).items())),
        warnings=('Four separate display lists combined without skeletal matrices; positions overlap',
                  'Colors distinguish parts and are not original game materials',
                  'Texture pointers are outside file 0x120; segment loading/TMEM requires runtime verification'),
        ended=all(m.ended for m in meshes),
    )
    return dict(region=region, rom_sha1=files.sha1, file_id=0x120,
                segment=9, source='Project64 USA Skeleton* capture + verified original regional ROM',
                resource_sha256=hashlib.sha256(data).hexdigest(),
                roots=[f'0x09{root:06X}' for root in roots], parts=parts,
                **combined.summary()), combined




def player_graphics_resources(files, region):
    """Inspect the original player graphics file-ID table, not actor IDs.

    Recomp variable naming is source evidence; there is no confirmed
    individual NPC ID or character name resolved by this function.
    """
    if region not in PLAYER_TABLE_OFFSETS:
        raise ValueError('Unsupported player graphics region')
    data = files.file(11)
    offset = PLAYER_TABLE_OFFSETS[region]
    if offset + 16 > len(data):
        raise ValueError('Player graphics file table exceeds the overlay')
    values = struct.unpack_from('>8H', data, offset)
    if values != EXPECTED_GRAPHICS_IDS:
        raise ValueError('Original player graphics file-ID table does not match verified region layout')
    result = []
    for slot in range(4):
        start, end = PLAYER_FRAGMENT_SPANS[region][slot]
        result.append(dict(slot=slot, file_id=values[slot], adjacent_file_id=values[slot+4],
                           segment=9, start=start, end=end, evidence='file_11 verified 8-entry table'))
    return result


def extract_player_fragment(rom, region, slot):
    """Decode one bounded player-resource fragment, not a full actor model."""
    if type(slot) is not int or not 0 <= slot < 4:
        raise ValueError('Player resource slot must be 0..3')
    files = RomFiles(rom) if region == 'usa' else JapanRomFiles(rom) if region == 'japan_0' else None
    if files is None:
        raise ValueError('Unsupported region')
    ref = player_graphics_resources(files, region)[slot]
    data = files.file(ref['file_id'])
    mesh = decode_geometry(data, ref['start'], ref['end'], segment=ref['segment'])
    report = dict(region=region, rom_sha1=files.sha1, **ref,
                  resource_sha256=hashlib.sha256(data).hexdigest(), **mesh.summary())
    report['limitations'] = 'Verified player resource ID, unverified full model/character identity; partial untextured segment-09 geometry.'
    return report, mesh


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
            limitations='Raw vertex RGB/normal bytes only; matrices, lighting, texture/TMEM, animation and culling not emulated.',
        )


def _validate_span(data, start, end):
    if type(start) is not int or type(end) is not int:
        raise ValueError('Command range must use integer offsets')
    if start < 0 or start >= end or end > len(data) or start % 8 or end % 8:
        raise ValueError('Display-list command range must be aligned, nonempty and within resource')
    if end - start > MAX_COMMANDS * 8:
        raise ValueError('Display-list command span exceeds bounded research budget')


def decode_geometry(data, start, end, *, segment=SEGMENT, max_commands=MAX_COMMANDS,
                    max_faces=MAX_FACES, max_depth=MAX_DEPTH):
    """Decode G_VTX/G_TRI1/G_TRI2/G_DL and G_ENDDL using RT64 F3DEX fields.

    Caller specifies the *exact research span*; it can start mid-list. Nested
    G_DL targets must resolve inside the same decompressed file and the explicitly selected segment (8 or 9).
    Commands that affect transform/lighting/texture are NOT applied. A warning
    is retained instead of asserting that the resulting geometry is complete.
    """
    _validate_span(data, start, end)
    if type(segment) is not int or segment not in SUPPORTED_SEGMENTS:
        raise ValueError('Unsupported F3DEX vertex/display-list segment; expected 8 or 9')
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

    segment_id = segment

    def address_to_offset(ptr, label, *, align):
        pointer_segment = ptr >> 24
        offset = ptr & 0x00FFFFFF
        if pointer_segment != segment_id or offset % align or offset >= len(data):
            raise ValueError(f'{label} must be an aligned segment-{segment_id:02X} pointer into the resource')
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
    warnings.add('Raw vertex RGB bytes may encode normals; textures, lighting, materials and skeletal transforms require RT64')
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
                start=start, end=end, segment=limits.get("segment", SEGMENT), **probe.summary()), probe


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--region', choices=('usa', 'japan_0'), required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--player-slot', type=int, help='Verified player graphics resource slot 0..3 (research fragment only)')
    source.add_argument('--traced-player', action='store_true', help='Replay the four 2026-11-17 USA Project64-captured limb roots (unposed geometry only)')
    source.add_argument('--file-id', type=int)
    parser.add_argument('--start', type=lambda s: int(s, 0))
    parser.add_argument('--end', type=lambda s: int(s, 0))
    parser.add_argument('--segment', type=lambda s: int(s, 0), choices=SUPPORTED_SEGMENTS, default=8)
    args = parser.parse_args(argv)
    try:
        rom = args.rom.read_bytes()
        if args.traced_player:
            if args.start is not None or args.end is not None or args.segment != SEGMENT:
                raise ValueError('--traced-player uses authenticated regional roots; omit --start, --end and --segment')
            report, _mesh = extract_traced_player_limb_bundle(rom, args.region)
        elif args.player_slot is not None:
            if args.start is not None or args.end is not None or args.segment != SEGMENT:
                raise ValueError('--player-slot uses verified fragment offsets/segment; omit --start, --end and --segment')
            report, _mesh = extract_player_fragment(rom, args.region, args.player_slot)
        else:
            if args.start is None or args.end is None:
                raise ValueError('--file-id requires --start and --end')
            report, _mesh = extract_rom_probe(rom, args.region,
                                              args.file_id, args.start, args.end, segment=args.segment)
        print(json.dumps(report, indent=2, sort_keys=True))
    except (OSError, ValueError, struct.error) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()

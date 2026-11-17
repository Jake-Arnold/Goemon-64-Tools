"""Read-only source-attested 14-node skeletal hierarchy research, USA/JP rev-0.

This extracts a real AnimatedSkeleton wrapper, follows its *relative child
links*, and decodes the geometry roots. Bone transforms are NOT applied:
encoded animation channel offsets are not direct angles/positions. No game
memory writes, actor ID assignment, ROM asset export or RT64 emulation.

Evidence: original-USA Project64 capture a0=80304BB0, a1=8014B0B0;
retail file_0x123 +0x2A590 contains AnimatedSkeleton{0x80000125,
seg07:0x29980,seg07:0x2A518}, and 14 reachable 0x18-byte Skeletons;
file_0x120 contains their segment-09 graphics display lists.
"""
from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
from pathlib import Path
import struct

from practice.entrances import RomFiles
from practice.room_actors import JapanRomFiles
from practice.model_research import MeshProbe, decode_geometry, player_graphics_resources

RIG_WRAPPER_OFFSET = 0x2A590
RIG_ROOT_OFFSET = 0x2A518
RIG_ANIMATION_STREAM_OFFSET = 0x29980
RIG_EXPECTED_FLAGS = 0x80000125
RIG_NODE_STRIDE = 0x18
RIG_MAX_NODES = 32
RIG_MIN_OFFSET = 0x2A300
RIG_EXPECTED_MESHES = 13
RIG_EXPECTED_NODES = 14
RIG_EXPECTED_TRIANGLES = 460


def encoded_channel(word: int, channel: str) -> dict:
    """Decode only source-proven immediate values; leave stream samples unresolved.

    USA MIPS func_8001A8E4 (scale), 8001AABC (translation), and
    8001AC28 (rotation): clear bit 0x4000, compare against 0xA001,
    for immediate form subtract 0xB000 (modulo 16 bits). func_80019ED8
    converts scale units by 1/256 and translation units by 1/32.
    The float-time channel streamer is func_8001B2C8, reading relative
    to global D_80168520; static offsets alone do not determine a pose.
    """
    if type(word) is not int or not 0 <= word <= 0xffff:
        raise ValueError('Channel value must be a 16-bit unsigned word')
    if channel not in ('scale', 'rotation', 'translation'):
        raise ValueError('Unknown skeleton channel type')
    masked = word & 0xBFFF
    special = bool(word & 0x4000)
    if masked >= 0xA001:
        raw = (masked - 0xB000) & 0xFFFF
        decoded = dict(kind='immediate', raw_word=f'0x{word:04X}',
                       raw_value=raw, special_bit=special)
        if channel == 'scale':
            decoded['value'] = raw / 256.0
            decoded['unit'] = 'scale factor (source-proven /256)'
        elif channel == 'translation':
            signed = raw - 0x10000 if raw & 0x8000 else raw
            decoded['value'] = signed / 32.0
            decoded['unit'] = 'translation unit (source-proven /32)'
        else:
            decoded['value'] = raw
            decoded['unit'] = 'raw rotation domain; original transform conversion needed'
        return decoded
    return dict(kind='animation_channel', raw_word=f'0x{word:04X}',
                offset=masked & 0x7FFF, special_bit=special,
                meaning='offset into runtime animation stream; sample time and buffer required')


def _source_segment_offset(ptr: int, segment: int, size: int) -> int:
    if ptr >> 24 != segment:
        raise ValueError(f'Segmented pointer requires segment 0x{segment:02X}')
    offset = ptr & 0xFFFFFF
    if offset >= size:
        raise ValueError('Segmented resource pointer exceeds authenticated file')
    return offset


def reconstruct_traced_rig(rom: bytes, region: str):
    """Traverse validated 14-node source hierarchy; return metadata + unposed mesh."""
    if region not in ('usa', 'japan_0'):
        raise ValueError('Unsupported ROM region for traced skeletal hierarchy')
    files = RomFiles(rom) if region == 'usa' else JapanRomFiles(rom)
    entries = player_graphics_resources(files, region)
    if entries[0]['file_id'] != 0x120 or entries[0]['adjacent_file_id'] != 0x123:
        raise ValueError('Original player graphics table does not identify expected resource pair')
    geom = files.file(0x120)
    animation = files.file(0x123)
    if RIG_WRAPPER_OFFSET + 12 > len(animation):
        raise ValueError('Captured animation wrapper outside resource')
    flags, animation_ptr, skeleton_ptr = struct.unpack_from('>III', animation, RIG_WRAPPER_OFFSET)
    if flags != RIG_EXPECTED_FLAGS:
        raise ValueError('Authenticated animation wrapper flags differ from observed source')
    anim_offset = _source_segment_offset(animation_ptr, 7, len(animation))
    root = _source_segment_offset(skeleton_ptr, 7, len(animation))
    if root != RIG_ROOT_OFFSET or anim_offset != RIG_ANIMATION_STREAM_OFFSET:
        raise ValueError('Animated skeleton source pointer differs from observed original ROM')

    nodes = []
    seen = set()
    visiting = set()
    all_triangles = []
    all_colours = []
    triangle_total = 0

    def visit(offset, parent=None, edge=None, depth=0):
        nonlocal triangle_total
        if depth >= RIG_MAX_NODES or len(nodes) >= RIG_MAX_NODES:
            raise ValueError('Skeleton traversal exceeded bounded node count')
        if offset in visiting or offset in seen:
            raise ValueError('Skeleton contains cycle or shared child pointer')
        if (offset < RIG_MIN_OFFSET or offset + RIG_NODE_STRIDE > RIG_WRAPPER_OFFSET
                or (offset - root) % RIG_NODE_STRIDE):
            raise ValueError('Skeleton child pointer leaves the authenticated source node array')
        visiting.add(offset)
        seen.add(offset)
        (display_ptr, right, left, *channels) = struct.unpack_from('>Ibb9h', animation, offset)
        sc, ro, tr = [tuple(v & 0xffff for v in channels[j:j+3]) for j in (0,3,6)]
        index = len(nodes)
        info = dict(index=index, source_offset=offset, parent_offset=parent, incoming=edge,
                    graphics_pointer=f'0x{display_ptr:08X}', right=right, left=left,
                    scale=[encoded_channel(v,'scale') for v in sc],
                    rotation=[encoded_channel(v,'rotation') for v in ro],
                    translation=[encoded_channel(v,'translation') for v in tr],
                    triangles=0)
        nodes.append(info)
        if display_ptr:
            gfx_offset = _source_segment_offset(display_ptr, 9, len(geom))
            if gfx_offset % 8:
                raise ValueError('Unaligned F3DEX display-list root in skeleton')
            decoded = decode_geometry(geom, gfx_offset, min(gfx_offset + 0x600, len(geom) & ~7), segment=9)
            if not decoded.ended or decoded.triangle_count == 0 or any(
                    'not loaded' in warning for warning in decoded.warnings):
                raise ValueError('Skeleton references incomplete or unresolved display-list mesh')
            info['triangles'] = decoded.triangle_count
            info['display_list_offset'] = gfx_offset
            triangle_total += decoded.triangle_count
            # Palette colours are *research overlays*, never original materials.
            hue = (index * 0.61803398875) % 1.0
            rr, gg, bb = colorsys.hsv_to_rgb(hue, 0.5, 0.90)
            artificial_color = (int(rr*255), int(gg*255), int(bb*255))
            all_triangles.extend(decoded.triangles)
            all_colours.extend(artificial_color for _ in decoded.triangles)
        # Original branch semantics: pointers are signed offsets counted in
        # units of the 0x18-byte Skeleton struct; this does NOT move vertices.
        for child_name, relative in (('right',right),('left',left)):
            if relative:
                visit(offset + relative * RIG_NODE_STRIDE,offset,child_name,depth+1)
        visiting.remove(offset)

    visit(root)
    mesh_nodes = sum(int(n['triangles'] > 0) for n in nodes)
    if (len(nodes) != RIG_EXPECTED_NODES or mesh_nodes != RIG_EXPECTED_MESHES
            or triangle_total != RIG_EXPECTED_TRIANGLES):
        raise ValueError('Skeleton hierarchy geometry differs from captured retail resources')
    immediate_scales = [v['value'] for n in nodes for v in n['scale'] if v['kind']=='immediate']
    animated_rotations = sum(v['kind']=='animation_channel' for n in nodes for v in n['rotation'])
    animated_translations = sum(v['kind']=='animation_channel' for n in nodes for v in n['translation'])
    mesh = MeshProbe(
        triangles=tuple(all_triangles),rgb=tuple(all_colours),commands=0,vertex_loads=0,
        opcodes=(),warnings=('Unposed skeleton: animation keyframes and matrices not decoded',
                             'Distinct part colours are artificial and not original textures',
                             'This is the linked source skeleton, not a verified complete character model'),ended=True)
    report = dict(format='goemon-traced-player-skeleton-structure-v1',region=region,
                  rom_sha1=files.sha1,graphics_file_id=0x120,skeleton_file_id=0x123,
                  skeleton_resource_sha256=hashlib.sha256(animation).hexdigest(),
                  graphics_resource_sha256=hashlib.sha256(geom).hexdigest(),
                  wrapper_offset=RIG_WRAPPER_OFFSET,wrapper_flags=f'0x{flags:08X}',
                  animation_stream_offset=anim_offset,root_offset=root,
                  node_count=len(nodes),mesh_node_count=mesh_nodes,triangles=triangle_total,
                  immediate_scale_count=len(immediate_scales),
                  all_immediate_scales_one=bool(immediate_scales) and all(x==1.0 for x in immediate_scales),
                  unresolved_rotation_channels=animated_rotations,
                  unresolved_translation_channels=animated_translations,
                  nodes=nodes,preview_status='Unposed, artificially coloured source rig; no character-body identification')
    return report, mesh


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    parser.add_argument('--region', choices=('usa','japan_0'),required=True)
    args = parser.parse_args(argv)
    try:
        report,_ = reconstruct_traced_rig(args.rom.read_bytes(),args.region)
        print(json.dumps(report,indent=2))
    except (OSError,ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__=='__main__':
    main()

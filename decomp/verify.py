"""Rebuild pinned mnsg in new Linux/WSL checkouts and verify reconstructed C.

Requires an existing local pinned upstream clone, the user's retail ROM, uv,
make, GCC and MIPS binutils. Never resets/deletes a checkout or overwrites a
report. ROMs, generated assembly, binaries and logs belong in local research
storage, not Git. Does not deploy, launch a game or submit upstream patches.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import subprocess

try:
    from . import overlay_file43
    from . import overlay_file12
    from . import overlay_file11
    from .research import usa_file11_noop_groups as overlay_file11_noops
    from . import overlay_file13
    from . import overlay_crossregion47
    from .elf_layout import pack_object_file, pack_heap_noop_file
    from .elf_layout import pack_file12_callback_text, pack_overlay_function_text
    from .collision_patch import prepare_collision_gate
    from .prepare_mips_binutils import configure as configure_binutils
    from .probe import Elf32
except ImportError:
    import overlay_file43
    import overlay_file12
    import overlay_file11
    from decomp.research import usa_file11_noop_groups as overlay_file11_noops
    import overlay_file13
    import overlay_crossregion47
    from elf_layout import pack_object_file, pack_heap_noop_file
    from elf_layout import pack_file12_callback_text, pack_overlay_function_text
    from collision_patch import prepare_collision_gate
    from prepare_mips_binutils import configure as configure_binutils
    from probe import Elf32

ROOT = Path(__file__).resolve().parent


def build_tool_environment(binutils_root, runtime_dir):
    """Isolate pinned cross-binutils DSOs for child build commands only.

    Never load an extracted archive libc into the verifier process itself.
    No persistent system installation, LD_LIBRARY_PATH export or shell eval.
    """
    if binutils_root is None:
        return os.environ.copy()
    return configure_binutils(Path(binutils_root), Path(runtime_dir))

# The only accepted patch of an upstream-owned C translation unit. The staged
# source hash is from the reviewed LF-only integration; changed upstream context
# must be reviewed explicitly rather than relying on an ambiguous pragma match.
COLLISION_GATE_PATCH = {
    'source': '27FE0.c',
    'candidate_source': 'candidates/collision_gate.c',
    'patched_sha256_lf': 'b6ac4275ec56796e23482765a82d3fd15d8c44f7148cd31f7cf8eb9fa408ab63',
    'function': {'name': 'func_80029E08_2AA08', 'rom_offset': 0x2AA08, 'size': 80},
}


def main_claimed_functions(manifest):
    """Claims whose addresses use the main segment's ROM/VMA mapping."""
    return [f for unit in manifest['units'] for f in unit['functions']] + [
        entry['function'] for entry in manifest.get('existing_source_patches', [])]


def manifest_file12_stages(manifest):
    """Return the ordered file_12 stages, retaining the legacy single-stage key."""
    single_present = 'overlay_file12_stage' in manifest
    multiple_present = 'overlay_file12_stages' in manifest
    if single_present and multiple_present:
        raise ValueError('Use only one file_12 stage manifest field')
    if single_present:
        stage = manifest['overlay_file12_stage']
        return [] if stage is None else [stage]
    if not multiple_present:
        return []
    stages = manifest['overlay_file12_stages']
    if not isinstance(stages, list) or not stages:
        raise ValueError('file_12 stages must be a nonempty list')
    return stages


def _file12_stage_list(stage_or_stages):
    if isinstance(stage_or_stages, dict):
        return [stage_or_stages]
    if isinstance(stage_or_stages, (list, tuple)):
        return list(stage_or_stages)
    raise ValueError('Invalid file_12 stage collection')


def file11_143_adapter():
    """Load the optional 143-C adapter only for a separately reviewed stage."""
    if __package__:
        from . import file11_143_stage
    else:
        from decomp import file11_143_stage
    return file11_143_stage


def file11_adapter(mode):
    """Versioned file_11 adapters; never repurpose the published 143-C fixture."""
    if mode == 143:
        return file11_143_adapter()
    if mode == 144:
        if __package__:
            from . import file11_144_stage
        else:
            from decomp import file11_144_stage
        return file11_144_stage
    if mode == 152:
        if __package__:
            from . import file11_152_stage
        else:
            from decomp import file11_152_stage
        return file11_152_stage
    if mode == 179:
        from . import file11_179_stage
        return file11_179_stage
    if mode == 183:
        from . import file11_183_stage
        return file11_183_stage
    raise ValueError('Unknown file_11 original-C ownership')


def file11_stage_mode(manifest):
    """Validate an optional file_11 stage version without accepting unknown fields."""
    if 'overlay_file11_stage' not in manifest:
        return None
    stage = manifest['overlay_file11_stage']
    if stage == {'format': overlay_file11.STAGE_FORMAT}:
        return 13
    if stage == {'format': overlay_file11_noops.STAGE_FORMAT}:
        return 50
    if stage == {'format': 'goemon-file11-143-central-v1'}:
        return 143
    if stage == {'format': 'goemon-file11-144-central-v1'}:
        return 144
    if stage == {'format': 'goemon-file11-152-central-v1'}:
        return 152
    if stage == {'format': 'goemon-file11-179-central-v1'}:
        return 179
    if stage == {'format': 'goemon-file11-183-central-v1'}:
        return 183
    raise ValueError('Unsupported file_11 matching-C stage contract')
def manifest_file13_stages(manifest):
    """Return the ordered file_13 stages, retaining the legacy single-stage key."""
    single_present = 'overlay_file13_stage' in manifest
    multiple_present = 'overlay_file13_stages' in manifest
    if single_present and multiple_present:
        raise ValueError('Use only one file_13 stage manifest field')
    if single_present:
        stage = manifest['overlay_file13_stage']
        return [] if stage is None else [stage]
    if not multiple_present:
        return []
    stages = manifest['overlay_file13_stages']
    if not isinstance(stages, list) or not stages:
        raise ValueError('file_13 stages must be a nonempty list')
    return stages


def _file13_stage_list(stage_or_stages):
    if isinstance(stage_or_stages, dict):
        return [stage_or_stages]
    if isinstance(stage_or_stages, (list, tuple)):
        return list(stage_or_stages)
    raise ValueError('Invalid file_13 stage collection')


def claimed_functions(manifest):
    """All C claims, with explicit overlay functions outside main mapping."""
    functions = main_claimed_functions(manifest)
    stage = manifest.get('overlay_file43_stage')
    if stage is not None:
        functions.append(stage['function'])
    functions.extend(stage['function'] for stage in manifest_file12_stages(manifest))
    mode = file11_stage_mode(manifest)
    if mode in (143,144,152,179,183):
        functions.extend(file11_adapter(mode).entries())
    elif mode is not None:
        functions.extend({'name': name, 'rom_offset': rom,
                          'vma': overlay_file11.VMA_START + rom - overlay_file11.ROM_START,
                          'size': size}
                         for name, rom, size, _ in overlay_file11.FUNCTIONS)
        if mode == 50:
            functions.extend({'name': name, 'rom_offset': rom,
                              'vma': overlay_file11.VMA_START + rom - overlay_file11.ROM_START,
                              'size': 12}
                             for name, rom in overlay_file11_noops.entries())
    functions.extend(stage['function'] for stage in manifest_file13_stages(manifest))
    if manifest.get('overlay_crossregion47_stage'):
        functions.extend({key: row[key] for key in ('name','rom_offset','vma','size')}
                         for row in overlay_crossregion47.load_fixture()['functions'])
    return functions



def digest(data,algorithm='sha1'):
    return hashlib.new(algorithm,data).hexdigest()


def validate_file43_stage_definition(stage):
    """Validate one opt-in file_43 C function without using main ROM mapping."""
    expected_keys = {'format', 'source', 'source_sha256',
                     'compiler_object_sha256', 'object_sha256', 'function'}
    if not isinstance(stage, dict) or set(stage) != expected_keys:
        raise ValueError('Invalid file_43 stage fields')
    if stage['format'] != 'goemon-file43-c-stage-v1':
        raise ValueError('Unsupported file_43 stage format')
    source = stage['source']
    relative = PurePosixPath(source) if isinstance(source, str) else None
    if (relative is None or relative.is_absolute() or
            any(part in ('', '.', '..') for part in relative.parts) or
            relative.suffix != '.c' or
            re.fullmatch(r'[a-z][a-z0-9_]*[.]c', relative.name) is None):
        raise ValueError('Unsafe file_43 C source path')
    for key in ('source_sha256', 'compiler_object_sha256', 'object_sha256'):
        if not isinstance(stage[key], str) or re.fullmatch('[0-9a-f]{64}', stage[key]) is None:
            raise ValueError('Invalid file_43 ' + key)
    function = stage['function']
    if (not isinstance(function, dict) or
            set(function) != {'name', 'rom_offset', 'vma', 'size'}):
        raise ValueError('Invalid file_43 function fields')
    name = function['name']
    expected = overlay_file43.FUNCTIONS.get(name)
    if expected is None:
        raise ValueError('Unreviewed file_43 function')
    if any(type(function[key]) is not int for key in ('rom_offset', 'vma', 'size')):
        raise ValueError('Invalid file_43 function address or size')
    if (function['vma'], function['rom_offset'], function['size']) != expected[:3]:
        raise ValueError('file_43 function identity differs from pinned extent')
    return relative


def validate_file43_stage(stage, splat_yaml, reference_rom, source_dir=ROOT):
    """Bind a staged source to the pinned file_43 reference contract."""
    relative = validate_file43_stage_definition(stage)
    source_root = Path(source_dir).resolve()
    source_path = (source_root / Path(*relative.parts)).resolve()
    if not source_path.is_relative_to(source_root) or not source_path.is_file():
        raise ValueError('Missing file_43 candidate source')
    source_bytes = source_path.read_bytes().replace(b'\r\n', b'\n')
    if digest(source_bytes, 'sha256') != stage['source_sha256']:
        raise ValueError('file_43 candidate source hash mismatch')
    if b'GLOBAL_ASM' in source_bytes:
        raise ValueError('file_43 C source may not hide assembly ownership')
    overlay_file43.validate_reference_inputs(
        splat_yaml, reference_rom, (stage['function']['name'],)
    )
    return source_path


def validate_file12_stage_definition(stage):
    """Validate one opt-in file_12 callback claim outside main ROM mapping."""
    expected_keys = {'format', 'source', 'source_sha256',
                     'compiler_object_sha256', 'object_sha256', 'function'}
    if not isinstance(stage, dict) or set(stage) != expected_keys:
        raise ValueError('Invalid file_12 stage fields')
    if stage['format'] != 'goemon-file12-c-stage-v1':
        raise ValueError('Unsupported file_12 stage format')
    source = stage['source']
    relative = PurePosixPath(source) if isinstance(source, str) else None
    if (relative is None or relative.is_absolute() or
            any(part in ('', '.', '..') for part in relative.parts) or
            relative.suffix != '.c' or
            re.fullmatch(r'[a-z][a-z0-9_]*[.]c', relative.name) is None):
        raise ValueError('Unsafe file_12 C source path')
    for key in ('source_sha256', 'compiler_object_sha256', 'object_sha256'):
        if not isinstance(stage[key], str) or re.fullmatch('[0-9a-f]{64}', stage[key]) is None:
            raise ValueError('Invalid file_12 ' + key)
    function = stage['function']
    if (not isinstance(function, dict) or
            set(function) != {'name', 'rom_offset', 'vma', 'size'}):
        raise ValueError('Invalid file_12 function fields')
    name = function['name']
    expected = overlay_file12.FUNCTIONS.get(name)
    if expected is None:
        raise ValueError('Unreviewed file_12 function')
    if any(type(function[key]) is not int for key in ('rom_offset', 'vma', 'size')):
        raise ValueError('Invalid file_12 function address or size')
    if (function['vma'], function['rom_offset'], function['size']) != expected[:3]:
        raise ValueError('file_12 function identity differs from pinned extent')
    return relative


def validate_file12_stage(stage, splat_yaml, reference_rom, source_dir=ROOT):
    """Bind a staged source to the pinned file_12 reference contract."""
    relative = validate_file12_stage_definition(stage)
    source_root = Path(source_dir).resolve()
    source_path = (source_root / Path(*relative.parts)).resolve()
    if not source_path.is_relative_to(source_root) or not source_path.is_file():
        raise ValueError('Missing file_12 candidate source')
    source_bytes = source_path.read_bytes().replace(b'\r\n', b'\n')
    if digest(source_bytes, 'sha256') != stage['source_sha256']:
        raise ValueError('file_12 candidate source hash mismatch')
    if b'GLOBAL_ASM' in source_bytes:
        raise ValueError('file_12 C source may not hide assembly ownership')
    overlay_file12.validate_reference_inputs(
        splat_yaml, reference_rom, (stage['function']['name'],)
    )
    return source_path


def validate_file13_stage_definition(stage):
    """Validate one opt-in file_13 C function outside main ROM mapping."""
    expected_keys = {'format', 'source', 'source_sha256',
                     'compiler_object_sha256', 'object_sha256', 'function'}
    if not isinstance(stage, dict) or set(stage) != expected_keys:
        raise ValueError('Invalid file_13 stage fields')
    if stage['format'] != 'goemon-file13-c-stage-v1':
        raise ValueError('Unsupported file_13 stage format')
    source = stage['source']
    relative = PurePosixPath(source) if isinstance(source, str) else None
    if (relative is None or relative.is_absolute() or
            any(part in ('', '.', '..') for part in relative.parts) or
            relative.suffix != '.c' or
            re.fullmatch(r'[a-z][a-z0-9_]*[.]c', relative.name) is None):
        raise ValueError('Unsafe file_13 C source path')
    for key in ('source_sha256', 'compiler_object_sha256', 'object_sha256'):
        if not isinstance(stage[key], str) or re.fullmatch('[0-9a-f]{64}', stage[key]) is None:
            raise ValueError('Invalid file_13 ' + key)
    function = stage['function']
    if (not isinstance(function, dict) or
            set(function) != {'name', 'rom_offset', 'vma', 'size'}):
        raise ValueError('Invalid file_13 function fields')
    name = function['name']
    expected = overlay_file13.FUNCTIONS.get(name)
    if expected is None:
        raise ValueError('Unreviewed file_13 function')
    if any(type(function[key]) is not int for key in ('rom_offset', 'vma', 'size')):
        raise ValueError('Invalid file_13 function address or size')
    if (function['vma'], function['rom_offset'], function['size']) != expected[:3]:
        raise ValueError('file_13 function identity differs from pinned extent')
    return relative


def validate_file13_stage(stage, splat_yaml, reference_rom, source_dir=ROOT):
    """Bind a staged source to the pinned file_13 reference contract."""
    relative = validate_file13_stage_definition(stage)
    source_root = Path(source_dir).resolve()
    source_path = (source_root / Path(*relative.parts)).resolve()
    if not source_path.is_relative_to(source_root) or not source_path.is_file():
        raise ValueError('Missing file_13 candidate source')
    source_bytes = source_path.read_bytes().replace(b'\r\n', b'\n')
    if digest(source_bytes, 'sha256') != stage['source_sha256']:
        raise ValueError('file_13 candidate source hash mismatch')
    if b'GLOBAL_ASM' in source_bytes:
        raise ValueError('file_13 C source may not hide assembly ownership')
    overlay_file13.validate_reference_inputs(
        splat_yaml, reference_rom, (stage['function']['name'],)
    )
    return source_path


def _file43_stage_segments(stage):
    function = stage['function']
    source_stem = PurePosixPath(stage['source']).stem
    before = f'file_43_before_{function["rom_offset"]:06X}'
    after_offset = function['rom_offset'] + function['size']
    after = f'file_43_after_{after_offset:06X}'
    lines = (
        f'    - [0x{overlay_file43.ROM_START:X}, asm, {before}]',
        f'    - [0x{function["rom_offset"]:X}, c, {source_stem}]',
        f'    - [0x{after_offset:X}, asm, {after}]',
        f'    - [0x{overlay_file43.ROM_TEXT_END:X}, rodata, file_43]',
    )
    return before, after, lines


def stage_file43_splat(text, stage):
    """Split only the named file_43 function, preserving the rodata boundary."""
    segment_names = list(re.finditer(r'(?m)^  - name: (\S+)\s*$', text))
    names = [item.group(1) for item in segment_names]
    if names.count('file_43') != 1 or names.count('file_44') != 1:
        raise ValueError('Missing or duplicate file_43 Splat segment')
    index = names.index('file_43')
    if index + 1 >= len(names) or names[index + 1] != 'file_44':
        raise ValueError('file_43 must remain adjacent to file_44')
    start, end = segment_names[index].start(), segment_names[index + 1].start()
    block = text[start:end]
    anchor = (
        '    - [0x6F34E0, asm, file_43]\n'
        '    - [0x6F9CE0, rodata, file_43]'
    )
    if block.count('    subalign: 16\n') != 1 or block.count(anchor) != 1:
        raise ValueError('Pinned file_43 Splat split anchor differs')
    before, after, replacement_lines = _file43_stage_segments(stage)
    block = block.replace('    subalign: 16\n', '    subalign: null\n', 1)
    block = block.replace(anchor, '\n'.join(replacement_lines))
    return text[:start] + block + text[end:], before, after


def _file12_stage_segments(stage):
    function = stage['function']
    source_stem = PurePosixPath(stage['source']).stem
    before = f'file_12_before_{function["rom_offset"]:06X}'
    after_offset = function['rom_offset'] + function['size']
    after = f'file_12_after_{after_offset:06X}'
    lines = (
        f'    - [0x{overlay_file12.ROM_START:X}, asm, {before}]',
        f'    - [0x{function["rom_offset"]:X}, c, {source_stem}]',
        f'    - [0x{after_offset:X}, asm, {after}]',
        f'    - [0x{overlay_file12.ROM_TEXT_END:X}, data, file_12]',
    )
    return before, after, lines


def _file12_stages_layout(stages):
    """Describe ordered callback and intervening assembly slices in file_12."""
    if not isinstance(stages, (list, tuple)) or not stages:
        raise ValueError('file_12 staging requires at least one callback')
    ordered = sorted(stages, key=lambda stage: stage['function']['rom_offset'])
    if list(stages) != ordered:
        raise ValueError('file_12 stages must follow original ROM order')
    previous_end = overlay_file12.ROM_START
    for stage in stages:
        validate_file12_stage_definition(stage)
        function = stage['function']
        if function['rom_offset'] < previous_end:
            raise ValueError('Overlapping file_12 staged functions')
        previous_end = function['rom_offset'] + function['size']
    first = stages[0]['function']
    last = stages[-1]['function']
    before = f'file_12_before_{first["rom_offset"]:06X}'
    after_offset = last['rom_offset'] + last['size']
    after = f'file_12_after_{after_offset:06X}'
    assembly = [before]
    lines = [f'    - [0x{overlay_file12.ROM_START:X}, asm, {before}]']
    c_segments = []
    for index, stage in enumerate(stages):
        function = stage['function']
        source_stem = PurePosixPath(stage['source']).stem
        c_segment = f'file_12_c_{function["rom_offset"]:06X}'
        c_segments.append(c_segment)
        lines.append(
            f'    - [0x{function["rom_offset"]:X}, c, {source_stem}]'
        )
        function_end = function['rom_offset'] + function['size']
        if index + 1 < len(stages):
            next_start = stages[index + 1]['function']['rom_offset']
            if next_start > function_end:
                gap = f'file_12_gap_{function_end:06X}_{next_start:06X}'
                assembly.append(gap)
                lines.append(f'    - [0x{function_end:X}, asm, {gap}]')
        else:
            assembly.append(after)
            lines.append(f'    - [0x{function_end:X}, asm, {after}]')
    lines.append(
        f'    - [0x{overlay_file12.ROM_TEXT_END:X}, data, file_12]'
    )
    return {
        'before': before,
        'after': after,
        'assembly': assembly,
        'c_segments': c_segments,
        'lines': tuple(lines),
    }


def stage_file12_splats(text, stages):
    """Split several file_12 callbacks while retaining every intervening byte."""
    overlay_file12.validate_layout(text)
    layout = _file12_stages_layout(stages)
    segments = list(re.finditer(r'(?m)^  - name: (\S+)\s*$', text))
    names = [item.group(1) for item in segments]
    if names.count('file_12') != 1 or names.count('file_13') != 1:
        raise ValueError('Missing or duplicate file_12 Splat segment')
    index = names.index('file_12')
    if index + 1 >= len(names) or names[index + 1] != 'file_13':
        raise ValueError('file_12 must remain adjacent to file_13')
    start, end = segments[index].start(), segments[index + 1].start()
    block = text[start:end]
    anchor = (
        f'    - [0x{overlay_file12.ROM_START:X}, asm]\n'
        f'    - [0x{overlay_file12.ROM_TEXT_END:X}, data]'
    )
    if block.count('    subalign: 16\n') != 1 or block.count(anchor) != 1:
        raise ValueError('Pinned file_12 Splat split anchor differs')
    replacement_lines = layout['lines']
    block = block.replace('    subalign: 16\n', '    subalign: null\n', 1)
    block = block.replace(anchor, '\n'.join(replacement_lines))
    return text[:start] + block + text[end:], tuple(layout['assembly'])


def stage_file12_splat(text, stage):
    """Backward-compatible single-callback splitter."""
    updated, assembly = stage_file12_splats(text, [stage])
    return updated, assembly[0], assembly[-1]


def _file13_stages_layout(stage_or_stages):
    stages = _file13_stage_list(stage_or_stages)
    if not stages:
        raise ValueError('file_13 stages must be nonempty')
    objects = []
    lines = []
    assembly = []
    names = set()
    sources = set()
    previous_end = None
    for stage in stages:
        source = validate_file13_stage_definition(stage)
        function = stage['function']
        name = function['name']
        start = function['rom_offset']
        end = start + function['size']
        if name in names or (previous_end is not None and start < previous_end):
            raise ValueError('Overlapping, duplicated, or unordered file_13 functions')
        if source.name in sources:
            raise ValueError('file_13 stages must use distinct C source files')
        if start < overlay_file13.ROM_START or end > overlay_file13.ROM_TEXT_END:
            raise ValueError('file_13 function crosses the original text boundary')
        names.add(name)
        sources.add(source.name)
        previous_end = end

    prefix = f'file_13_before_{stages[0]["function"]["rom_offset"]:06X}'
    lines.append(f'    - [0x{overlay_file13.ROM_START:X}, asm, {prefix}]')
    assembly.append(prefix)
    objects.append({
        'kind': 'asm', 'name': prefix,
        'start': overlay_file13.ROM_START,
        'end': stages[0]['function']['rom_offset'],
    })
    for index, stage in enumerate(stages):
        function = stage['function']
        start = function['rom_offset']
        end = start + function['size']
        source_stem = PurePosixPath(stage['source']).stem
        lines.append(f'    - [0x{start:X}, c, {source_stem}]')
        objects.append({
            'kind': 'c', 'name': source_stem,
            'start': start, 'end': end,
            'stage': stage,
        })
        if index + 1 < len(stages):
            next_start = stages[index + 1]['function']['rom_offset']
            if end < next_start:
                name = f'file_13_between_{end:06X}_{next_start:06X}'
                lines.append(f'    - [0x{end:X}, asm, {name}]')
                assembly.append(name)
                objects.append({
                    'kind': 'asm', 'name': name, 'start': end,
                    'end': next_start,
                })
        else:
            name = f'file_13_after_{end:06X}'
            lines.append(f'    - [0x{end:X}, asm, {name}]')
            assembly.append(name)
            objects.append({
                'kind': 'asm', 'name': name, 'start': end,
                'end': overlay_file13.ROM_TEXT_END,
            })
    lines.append(f'    - [0x{overlay_file13.ROM_TEXT_END:X}, data]')
    return {'assembly': assembly, 'objects': objects, 'lines': tuple(lines)}


def stage_file13_splat(text, stage_or_stages):
    """Split reviewed file_13 functions while retaining its data boundary."""
    overlay_file13.validate_layout(text)
    layout = _file13_stages_layout(stage_or_stages)
    segments = list(re.finditer(r'(?m)^  - name: (\S+)\s*$', text))
    names = [item.group(1) for item in segments]
    if names.count('file_13') != 1 or names.count('file_14') != 1:
        raise ValueError('Missing or duplicate file_13 Splat segment')
    index = names.index('file_13')
    if index + 1 >= len(names) or names[index + 1] != 'file_14':
        raise ValueError('file_13 must remain adjacent to file_14')
    start, end = segments[index].start(), segments[index + 1].start()
    block = text[start:end]
    anchor = (
        f'    - [0x{overlay_file13.ROM_START:X}, asm]\n'
        f'    - [0x{overlay_file13.ROM_TEXT_END:X}, data]'
    )
    if block.count('    subalign: 16\n') != 1 or block.count(anchor) != 1:
        raise ValueError('Pinned file_13 Splat split anchor differs')
    block = block.replace('    subalign: 16\n', '    subalign: null\n', 1)
    block = block.replace(anchor, '\n'.join(layout['lines']))
    return text[:start] + block + text[end:], tuple(layout['assembly'])


def patch_file12_tail_alias_sources(candidate_checkout, stage):
    """Restore Splat's original zero-size tail alias after splitting file_12."""
    stages = _file12_stage_list(stage)
    layout = _file12_stages_layout(stages)
    checkout = Path(candidate_checkout)
    before, after = layout['assembly'][0], layout['assembly'][-1]
    before_path = checkout / f'asm/usa/{before}.s'
    after_path = checkout / f'asm/usa/{after}.s'
    if not before_path.is_file() or not after_path.is_file():
        raise ValueError('Missing generated file_12 assembly for tail alias correction')
    before_text = before_path.read_text(encoding='utf-8')
    after_text = after_path.read_text(encoding='utf-8')
    rom_offset, vma, alias_name, generated_name, word = overlay_file12.TEXT_END_ALIAS
    if before_text.count(generated_name) != 4 or before_text.count(alias_name):
        raise ValueError('Unexpected file_12 prefix tail-alias references')
    old_block = (
        f'nonmatching {generated_name}, 0x4\n\n'
        f'glabel {generated_name}\n'
        f'    /* {rom_offset:06X} {vma:08X} {word} */  nop\n'
        f'endlabel {generated_name}\n'
    )
    new_block = (
        f'  alabel {alias_name}\n'
        f'    /* {rom_offset:06X} {vma:08X} {word} */  nop\n'
    )
    if (after_text.count(old_block) != 1 or
            after_text.count(generated_name) != 3 or after_text.count(alias_name)):
        raise ValueError('Unexpected file_12 suffix tail-alias block')
    staged_before = before_text.replace(generated_name, alias_name)
    staged_after = after_text.replace(old_block, new_block)
    if staged_before.count(alias_name) != 4 or generated_name in staged_before:
        raise ValueError('file_12 prefix tail-alias correction did not apply exactly')
    if staged_after.count(alias_name) != 1 or generated_name in staged_after:
        raise ValueError('file_12 suffix tail-alias correction did not apply exactly')

    before_path.write_text(staged_before, encoding='utf-8', newline='\n')
    after_path.write_text(staged_after, encoding='utf-8', newline='\n')
    return {
        'rom_offset': f'0x{rom_offset:X}',
        'vma': f'0x{vma:08X}',
        'generated_function_name': generated_name,
        'restored_alias_name': alias_name,
        'instruction_word': word,
        'prefix_reference_rewrites': 4,
        'suffix_zero_size_alias_restored': True,
        'prefix_sha256_before': digest(before_text.encode('utf-8'), 'sha256'),
        'prefix_sha256_after': digest(staged_before.encode('utf-8'), 'sha256'),
        'suffix_sha256_before': digest(after_text.encode('utf-8'), 'sha256'),
        'suffix_sha256_after': digest(staged_after.encode('utf-8'), 'sha256'),
        'instruction_bytes_changed': False,
    }


def lower_file43_text_alignment(object_bytes, expected_alignment=16, new_alignment=4):
    """Lower one ET_REL .text input alignment without changing code or relocs."""
    if (type(expected_alignment) is not int or type(new_alignment) is not int or
            expected_alignment <= 0 or new_alignment <= 0 or
            expected_alignment & (expected_alignment - 1) or
            new_alignment & (new_alignment - 1) or new_alignment >= expected_alignment):
        raise ValueError('Invalid file_43 .text alignment adjustment')
    elf = Elf32(object_bytes)
    if elf.kind != 1:
        raise ValueError('file_43 staged input must be a relocatable ELF object')
    matches = [index for index, name in enumerate(elf.names) if name == '.text']
    if len(matches) != 1:
        raise ValueError('file_43 input object must have exactly one .text section')
    index = matches[0]
    section = elf.sections[index]
    if not section[2] & 0x4 or section[8] != expected_alignment:
        raise ValueError('file_43 input .text alignment or flags differ from pinned compiler output')
    changed = bytearray(object_bytes)
    section_table = struct.unpack_from('>I', changed, 32)[0]
    struct.pack_into('>I', changed, section_table + index * 40 + 32, new_alignment)
    result = bytes(changed)
    patched = Elf32(result)
    if patched.sections[index][8] != new_alignment:
        raise ValueError('file_43 .text alignment adjustment did not take effect')
    differences = [offset for offset, (before, after) in
                   enumerate(zip(object_bytes, result)) if before != after]
    expected_offset = section_table + index * 40 + 32
    if (any(not expected_offset <= offset < expected_offset + 4 for offset in differences) or
            struct.unpack_from('>I', result, expected_offset)[0] != new_alignment):
        raise ValueError('file_43 alignment adjustment changed bytes outside section metadata')
    return result


def prepare_file43_stage_objects(candidate_checkout, stage):
    """Build and pin C/ASM objects, then align only the overlay's later inputs."""
    validate_file43_stage_definition(stage)
    checkout = Path(candidate_checkout)
    source_name = PurePosixPath(stage['source']).name
    function = stage['function']
    before, after, _ = _file43_stage_segments(stage)
    c_path = checkout / f'build/usa/src/{source_name}.o'
    before_path = checkout / f'build/usa/asm/usa/{before}.s.o'
    after_path = checkout / f'build/usa/asm/usa/{after}.s.o'
    if not c_path.is_file() or not before_path.is_file() or not after_path.is_file():
        raise ValueError('Missing compiled file_43 source or assembly slices')

    c_original = c_path.read_bytes()
    c_elf = Elf32(c_original)
    c_symbol = c_elf.function(function['name'])
    if c_symbol.size != function['size'] or c_symbol.binding != 1:
        raise ValueError('file_43 compiler object function identity differs')
    if digest(c_original, 'sha256') != stage['compiler_object_sha256']:
        raise ValueError('file_43 compiler object hash mismatch')
    after_original = after_path.read_bytes()
    after_elf = Elf32(after_original)
    if any(symbol.name == function['name'] and symbol.section != 0
           for symbol in after_elf.symbols):
        raise ValueError('Generated file_43 suffix assembly still owns staged function')
    before_elf = Elf32(before_path.read_bytes())
    before_text = [i for i, name in enumerate(before_elf.names) if name == '.text']
    if (len(before_text) != 1 or
            not before_elf.sections[before_text[0]][2] & 0x4 or
            before_elf.sections[before_text[0]][8] != 16):
        raise ValueError('file_43 prefix assembly lacks one .text section')

    c_staged = lower_file43_text_alignment(c_original)
    after_staged = lower_file43_text_alignment(after_original)
    c_hash = digest(c_staged, 'sha256')
    if c_hash != stage['object_sha256']:
        raise ValueError('file_43 staged C object hash mismatch')

    linker_script = checkout / '.splat/usa/mnsg.ld'
    script = linker_script.read_text(encoding='utf-8')
    if re.search(r'(?m)^\s*\.file_43\s+0x8000000\s*:\s*AT\(file_43_ROM_START\)\s+SUBALIGN\(', script):
        raise ValueError('file_43 linker section unexpectedly forces input alignment')
    if len(re.findall(r'(?m)^\s*\.file_43\s+0x8000000\s*:\s*AT\(file_43_ROM_START\)', script)) != 1:
        raise ValueError('Generated linker script has no unique file_43 section anchor')

    # Check all output before mutating either object, then write only the two
    # section-header alignment words. Full linked ELF and ROM proof follows.
    c_path.write_bytes(c_staged)
    after_path.write_bytes(after_staged)
    return {
        'compiler_object': f'build/usa/src/{source_name}.o',
        'compiler_object_sha256': digest(c_original, 'sha256'),
        'staged_object_sha256': c_hash,
        'adjusted_text_alignment': {'from': 16, 'to': 4},
        'adjusted_objects': [
            {'path': f'build/usa/src/{source_name}.o',
             'sha256_before': digest(c_original, 'sha256'),
             'sha256_after': c_hash},
            {'path': f'build/usa/asm/usa/{after}.s.o',
             'sha256_before': digest(after_original, 'sha256'),
             'sha256_after': digest(after_staged, 'sha256')},
        ],
        'preserved_prefix_text_alignment': before_elf.sections[
            [i for i, name in enumerate(before_elf.names) if name == '.text'][0]
        ][8],
        'linker_script_sha256': digest(script.encode('utf-8'), 'sha256'),
    }


def lower_file12_text_alignment(object_bytes):
    """Lower the adjacent file_12 suffix to its pinned 4-byte alignment."""
    elf = Elf32(object_bytes)
    if elf.kind != 1:
        raise ValueError('file_12 staged input must be a relocatable ELF object')
    matches = [index for index, name in enumerate(elf.names) if name == '.text']
    if len(matches) != 1:
        raise ValueError('file_12 input object must have exactly one .text section')
    index = matches[0]
    section = elf.sections[index]
    if not section[2] & 0x4 or section[8] != 16:
        raise ValueError('file_12 input .text alignment or flags differ from pinned compiler output')
    changed = bytearray(object_bytes)
    section_table = struct.unpack_from('>I', changed, 32)[0]
    metadata_offset = section_table + index * 40 + 32
    struct.pack_into('>I', changed, metadata_offset, 4)
    result = bytes(changed)
    patched = Elf32(result)
    if patched.sections[index][8] != 4:
        raise ValueError('file_12 .text alignment adjustment did not take effect')
    differences = [offset for offset, (before, after) in
                   enumerate(zip(object_bytes, result)) if before != after]
    if any(not metadata_offset <= offset < metadata_offset + 4
           for offset in differences):
        raise ValueError('file_12 alignment adjustment changed bytes outside section metadata')
    return result


def lower_file13_text_alignment(object_bytes):
    """Lower a file_13 suffix .text alignment without changing its bytes."""
    elf = Elf32(object_bytes)
    if elf.kind != 1:
        raise ValueError('file_13 staged input must be a relocatable MIPS object')
    matches = [index for index, name in enumerate(elf.names) if name == '.text']
    if len(matches) != 1:
        raise ValueError('file_13 input object must have exactly one .text section')
    index = matches[0]
    section = elf.sections[index]
    if not section[2] & 0x4 or section[8] != 16:
        raise ValueError('file_13 input .text alignment or flags differ from pinned compiler output')
    changed = bytearray(object_bytes)
    section_table = struct.unpack_from('>I', changed, 32)[0]
    metadata_offset = section_table + index * 40 + 32
    struct.pack_into('>I', changed, metadata_offset, 4)
    result = bytes(changed)
    patched = Elf32(result)
    if patched.sections[index][8] != 4:
        raise ValueError('file_13 .text alignment adjustment did not take effect')
    if any(before != after and not metadata_offset <= offset < metadata_offset + 4
           for offset, (before, after) in enumerate(zip(object_bytes, result))):
        raise ValueError('file_13 alignment adjustment changed bytes outside section metadata')
    return result


def prepare_file13_stage_objects(candidate_checkout, stage_or_stages):
    """Pin each staged C function and preserve every file_13 assembly extent."""
    stages = _file13_stage_list(stage_or_stages)
    layout = _file13_stages_layout(stages)
    checkout = Path(candidate_checkout)
    function_names = {stage['function']['name'] for stage in stages}
    c_layouts = []
    for stage in stages:
        validate_file13_stage_definition(stage)
        function = stage['function']
        source_name = PurePosixPath(stage['source']).name
        c_path = checkout / f'build/usa/src/{source_name}.o'
        if not c_path.is_file():
            raise ValueError('Missing compiled file_13 C object')
        c_original = c_path.read_bytes()
        if digest(c_original, 'sha256') != stage['compiler_object_sha256']:
            raise ValueError('file_13 compiler object hash mismatch')
        c_staged, pack_evidence = pack_overlay_function_text(
            c_original, function['name'], function['size'],
            overlay_file13.FUNCTION_OBJECT_PADDING[function['name']],
            overlay_file13.FUNCTION_RELOCATIONS[function['name']],
            overlay_file13.FUNCTION_RELOCATION_SYMBOLS[function['name']],
            'file_13 ' + function['name'],
            'file13_' + PurePosixPath(stage['source']).stem,
        )
        c_staged_hash = digest(c_staged, 'sha256')
        if c_staged_hash != stage['object_sha256']:
            raise ValueError('file_13 staged C object hash mismatch')
        c_elf = Elf32(c_staged)
        c_symbol = c_elf.function(function['name'])
        c_text = c_elf.sections[c_symbol.section]
        if (c_symbol.value != 0 or c_symbol.size != function['size'] or
                c_symbol.binding != 1 or c_elf.names[c_symbol.section] != '.text' or
                c_text[5] != function['size'] or c_text[8] != 4):
            raise ValueError('file_13 staged function placement or text extent differs')
        c_path.write_bytes(c_staged)
        c_layouts.append({
            'source': stage['source'],
            'compiler_object': f'build/usa/src/{source_name}.o',
            'compiler_object_sha256': digest(c_original, 'sha256'),
            'staged_object_sha256': c_staged_hash,
            'function': function['name'],
            'callback_layout': pack_evidence,
        })

    assembly_layouts = []
    for index, name in enumerate(layout['assembly']):
        object_path = checkout / f'build/usa/asm/usa/{name}.s.o'
        if not object_path.is_file():
            raise ValueError('Missing compiled file_13 assembly slice')
        original = object_path.read_bytes()
        assembly = Elf32(original)
        text_sections = [i for i, label in enumerate(assembly.names) if label == '.text']
        if (len(text_sections) != 1 or not assembly.sections[text_sections[0]][2] & 0x4 or
                assembly.sections[text_sections[0]][8] != 16):
            raise ValueError('file_13 assembly .text alignment differs from pinned compiler output')
        if any(symbol.name in function_names and symbol.section != 0
               for symbol in assembly.symbols):
            raise ValueError('file_13 assembly slice still owns a staged function')
        staged = original if index == 0 else lower_file13_text_alignment(original)
        object_path.write_bytes(staged)
        assembly_layouts.append({
            'object': f'build/usa/asm/usa/{name}.s.o',
            'sha256_before': digest(original, 'sha256'),
            'sha256_after': digest(staged, 'sha256'),
            'alignment_before': 16,
            'alignment_after': 16 if index == 0 else 4,
            'extent': next(obj for obj in layout['objects']
                           if obj['kind'] == 'asm' and obj['name'] == name),
        })

    linker_script = checkout / '.splat/usa/mnsg.ld'
    script = linker_script.read_text(encoding='utf-8')
    anchor = r'(?mi)^\s*\.file_13\s+0x801cb460\s*:\s*AT\(file_13_ROM_START\)'
    if (re.search(anchor + r'\s+SUBALIGN\(', script) or
            len(re.findall(anchor, script)) != 1):
        raise ValueError('Generated linker script does not preserve file_13 input alignment')
    return {
        'functions': c_layouts,
        'assembly_objects': assembly_layouts,
        'preserved_prefix_text_alignment': 16,
        'linker_script_sha256': digest(script.encode('utf-8'), 'sha256'),
    }


def prepare_file12_stage_objects(candidate_checkout, stage):
    """Trim each verified callback tail and align following assembly slices."""
    stages = _file12_stage_list(stage)
    layout = _file12_stages_layout(stages)
    checkout = Path(candidate_checkout)
    callback_layouts = []
    staged_names = {item['function']['name'] for item in stages}
    for item in stages:
        source_name = PurePosixPath(item['source']).name
        function = item['function']
        c_path = checkout / f'build/usa/src/{source_name}.o'
        if not c_path.is_file():
            raise ValueError('Missing compiled file_12 source object')
        c_original = c_path.read_bytes()
        if digest(c_original, 'sha256') != item['compiler_object_sha256']:
            raise ValueError('file_12 compiler object hash mismatch')
        expected_relocations = overlay_file12.FUNCTION_RELOCATIONS[function['name']]
        c_staged, pack_evidence = pack_file12_callback_text(
            c_original, function['name'], function['size'], expected_relocations,
            overlay_file12.FUNCTION_RELOCATION_SYMBOLS[function['name']],
        )
        c_staged_hash = digest(c_staged, 'sha256')
        if c_staged_hash != item['object_sha256']:
            raise ValueError('file_12 staged C object hash mismatch')
        c_path.write_bytes(c_staged)
        callback_layouts.append({
            'source': item['source'],
            'compiler_object': f'build/usa/src/{source_name}.o',
            'compiler_object_sha256': digest(c_original, 'sha256'),
            'staged_object_sha256': c_staged_hash,
            'callback_layout': pack_evidence,
        })

    adjusted_objects = []
    prefix_text_alignment = None
    for index, segment in enumerate(layout['assembly']):
        object_name = f'build/usa/asm/usa/{segment}.s.o'
        object_path = checkout / object_name
        if not object_path.is_file():
            raise ValueError('Missing generated file_12 assembly slice: ' + segment)
        original = object_path.read_bytes()
        assembly_elf = Elf32(original)
        text_sections = [i for i, name in enumerate(assembly_elf.names)
                         if name == '.text']
        if (len(text_sections) != 1 or
                not assembly_elf.sections[text_sections[0]][2] & 0x4 or
                assembly_elf.sections[text_sections[0]][8] != 16):
            raise ValueError('file_12 assembly .text layout differs for ' + segment)
        if any(symbol.name in staged_names and symbol.section != 0
               for symbol in assembly_elf.symbols):
            raise ValueError('Generated assembly still owns a staged file_12 function')
        if index == 0:
            prefix_text_alignment = assembly_elf.sections[text_sections[0]][8]
            continue
        adjusted = lower_file12_text_alignment(original)
        object_path.write_bytes(adjusted)
        adjusted_objects.append({
            'path': object_name,
            'sha256_before': digest(original, 'sha256'),
            'sha256_after': digest(adjusted, 'sha256'),
        })

    linker_script = checkout / '.splat/usa/mnsg.ld'
    script = linker_script.read_text(encoding='utf-8')
    anchor = r'(?mi)^\s*\.file_12\s+0x8020d2a0\s*:\s*AT\(file_12_ROM_START\)'
    if re.search(anchor + r'\s+SUBALIGN\(', script):
        raise ValueError('file_12 linker section unexpectedly forces input alignment')
    if len(re.findall(anchor, script)) != 1:
        raise ValueError('Generated linker script has no unique file_12 section anchor')

    result = {
        'callbacks': callback_layouts,
        'adjusted_text_alignment': {'from': 16, 'to': 4},
        'adjusted_objects': adjusted_objects,
        'preserved_prefix_text_alignment': prefix_text_alignment,
        'linker_script_sha256': digest(script.encode('utf-8'), 'sha256'),
    }
    if len(callback_layouts) == 1:
        result.update({key: callback_layouts[0][key] for key in (
            'compiler_object', 'compiler_object_sha256', 'staged_object_sha256',
            'callback_layout')})
    return result


def load_manifest(path):
    manifest=json.loads(Path(path).read_text(encoding='utf-8'))
    if manifest.get('format')!='goemon-matching-decomp-v1':raise ValueError('Unsupported manifest format')
    for key,length in (('upstream_commit',40),('retail_sha1',40),('decompressed_sha1',40)):
        if not re.fullmatch('[0-9a-f]{'+str(length)+'}',manifest.get(key,'')):raise ValueError('Invalid '+key)
    seen=set();assembly_seen=set();ranges=[]
    if not manifest.get('units'):raise ValueError('No reconstructed units')
    if manifest.get('splat_options',{}) not in ({},{'asm_jtbl_label_macro':'glabel'}):
        raise ValueError('Unsupported Splat override')
    headers=manifest.get('support_headers',[])
    if len(headers)!=len(set(headers)) or any(not re.fullmatch('[a-z][a-z0-9_]*[.]h',name) for name in headers):
        raise ValueError('Invalid support header names')
    for unit in manifest['units']:
        if not re.fullmatch('[a-z][a-z0-9_]*[.]c',unit['source']):raise ValueError('Unsafe source name')
        start,end=unit['rom_start'],unit['rom_end']
        if not 0<=start<end or start%4 or end%4:raise ValueError('Invalid unit bounds')
        ranges.append((start,end))
        no_padding=unit.get('asm_no_padding',[])
        if len(no_padding)!=len(set(no_padding)) or any(not re.fullmatch('[0-9A-F]{4,5}',name) for name in no_padding):
            raise ValueError('Invalid assembly no-padding object name')
        previous=start
        for fn in unit['functions']:
            if not re.fullmatch('func_[0-9A-F]{8}_[0-9A-F]+',fn['name']) or fn['name'] in seen or fn['name'] in assembly_seen:
                raise ValueError('Invalid/duplicate function name')
            seen.add(fn['name']);offset,size=fn['rom_offset'],fn['size']
            if offset<previous or size<=0 or offset%4 or size%4 or offset+size>end:
                raise ValueError('Invalid/overlapping function bounds')
            if int(fn['name'].split('_')[2],16)!=offset:raise ValueError('Function ROM offset disagrees with symbol')
            if int(fn['name'].split('_')[1],16)!=offset+0x7FFFF400:raise ValueError('Function guest address disagrees with main mapping')
            previous=offset+size
        assembly=unit.get('assembly_functions',[])
        if len(set(assembly))!=len(assembly) or any(name in seen or name in assembly_seen or not re.fullmatch('func_[0-9A-F]{8}_[0-9A-F]+',name) for name in assembly):
            raise ValueError('Invalid/claimed assembly placeholder')
        for name in assembly:
            offset=int(name.split('_')[2],16)
            if not start<=offset<end or int(name.split('_')[1],16)!=offset+0x7FFFF400:
                raise ValueError('Assembly placeholder outside unit/mapping')
            if any(fn['rom_offset']<=offset<fn['rom_offset']+fn['size'] for fn in unit['functions']):
                raise ValueError('Assembly placeholder overlaps claimed C')
        assembly_seen.update(assembly)
    patches = manifest.get('existing_source_patches', [])
    if patches not in ([], [COLLISION_GATE_PATCH]):
        raise ValueError('Unsupported existing-source patch; manual layout review required')
    if patches:
        if manifest['upstream_commit'] != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
            raise ValueError('Existing-source patch requires pinned upstream commit')
        fn = COLLISION_GATE_PATCH['function']
        if fn['name'] in seen or fn['name'] in assembly_seen:
            raise ValueError('Existing-source patch function already claimed')
        if any(start < fn['rom_offset']+fn['size'] and fn['rom_offset'] < end for start,end in ranges):
            raise ValueError('Existing-source patch overlaps migrated unit')
    stage = manifest.get('overlay_file43_stage')
    if stage is not None:
        stage_source = validate_file43_stage_definition(stage)
        function_name = stage['function']['name']
        if function_name in seen or function_name in assembly_seen:
            raise ValueError('Duplicate file_43 function ownership')
        if any(start < stage['function']['rom_offset'] + stage['function']['size'] and
               stage['function']['rom_offset'] < end for start, end in ranges):
            raise ValueError('file_43 function overlaps a main-segment unit')
        source_names = ({unit['source'] for unit in manifest['units']} |
                        set(manifest.get('support_headers', [])) |
                        {patch['source'] for patch in patches})
        if stage_source.name in source_names:
            raise ValueError('file_43 C source collides with a main-segment source')
    file12_stages = manifest_file12_stages(manifest)
    if file12_stages:
        file43_stage = manifest.get('overlay_file43_stage')
        source_names = ({unit['source'] for unit in manifest['units']} |
                        set(manifest.get('support_headers', [])) |
                        {patch['source'] for patch in patches})
        if file43_stage is not None:
            source_names.add(PurePosixPath(file43_stage['source']).name)
        previous_end = None
        file12_source_names = set()
        for stage in file12_stages:
            stage_source = validate_file12_stage_definition(stage)
            function = stage['function']
            function_name = function['name']
            if previous_end is not None and function['rom_offset'] < previous_end:
                raise ValueError('Overlapping or unordered file_12 functions')
            previous_end = function['rom_offset'] + function['size']
            if stage_source.name in source_names or stage_source.name in file12_source_names:
                raise ValueError('file_12 C source collides with another source')
            file12_source_names.add(stage_source.name)
            if function_name in seen or function_name in assembly_seen:
                raise ValueError('Duplicate file_12 function ownership')
            if any(start < function['rom_offset'] + function['size'] and
                   function['rom_offset'] < end for start, end in ranges):
                raise ValueError('file_12 function overlaps a main-segment unit')
            if (file43_stage is not None and
                    function['rom_offset'] <
                    file43_stage['function']['rom_offset'] + file43_stage['function']['size'] and
                    file43_stage['function']['rom_offset'] <
                    function['rom_offset'] + function['size']):
                raise ValueError('file_12 function overlaps file_43 function')
    file11_mode = file11_stage_mode(manifest)
    if file11_mode is not None:
        if file11_mode in (143,144,152,179,183):
            file11_adapter(file11_mode).reviewed_plan(manifest)
            candidates = [(f['name'], f['rom_offset'], f['size'])
                          for f in file11_adapter(file11_mode).entries()]
        else:
            candidates = [(name, rom, size) for name, rom, size, _ in overlay_file11.FUNCTIONS]
            if file11_mode == 50:
                candidates.extend((name, rom, 12) for name, rom in overlay_file11_noops.entries())
        staged = set(candidates)
        if len(staged) != len(candidates):
            raise ValueError('Duplicated pinned file_11 function identity')
        for name, rom, size in staged:
            if name in seen or name in assembly_seen:
                raise ValueError('file_11 function is already claimed or assembly placeholder')
            if any(start < rom + size and rom < end for start, end in ranges):
                raise ValueError('file_11 function overlaps main-segment unit')
    file13_stages = manifest_file13_stages(manifest)
    if file13_stages:
        source_names = ({unit['source'] for unit in manifest['units']} |
                        set(manifest.get('support_headers', [])) |
                        {patch['source'] for patch in patches})
        if file43_stage is not None:
            source_names.add(PurePosixPath(file43_stage['source']).name)
        source_names.update(PurePosixPath(stage['source']).name
                            for stage in file12_stages)
        file13_source_names = set()
        previous_end = None
        for file13_stage in file13_stages:
            stage_source = validate_file13_stage_definition(file13_stage)
            function = file13_stage['function']
            function_name = function['name']
            if function_name in seen or function_name in assembly_seen:
                raise ValueError('Duplicate file_13 function ownership')
            if previous_end is not None and function['rom_offset'] < previous_end:
                raise ValueError('Overlapping or unordered file_13 functions')
            previous_end = function['rom_offset'] + function['size']
            if any(start < function['rom_offset'] + function['size'] and
                   function['rom_offset'] < end for start, end in ranges):
                raise ValueError('file_13 function overlaps a main-segment unit')
            if (stage_source.name in source_names or
                    stage_source.name in file13_source_names):
                raise ValueError('file_13 C source collides with another source')
            file13_source_names.add(stage_source.name)
            if (file43_stage is not None and
                    function['rom_offset'] <
                    file43_stage['function']['rom_offset'] + file43_stage['function']['size'] and
                    file43_stage['function']['rom_offset'] <
                    function['rom_offset'] + function['size']):
                raise ValueError('file_13 function overlaps file_43 function')
            for stage in file12_stages:
                other = stage['function']
                if (function['rom_offset'] < other['rom_offset'] + other['size'] and
                        other['rom_offset'] < function['rom_offset'] + function['size']):
                    raise ValueError('file_13 function overlaps file_12 function')
    ranges.sort()
    if any(a[1]>b[0] for a,b in zip(ranges,ranges[1:])):raise ValueError('Overlapping units')
    if 'heap_noop_text_layout' in manifest:
        if manifest['heap_noop_text_layout'] is not True or manifest['upstream_commit'] != '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee':
            raise ValueError('Unsupported empty-function layout preset')
        targets=[u for u in manifest['units'] if u['source']=='heap_noop.c']
        if len(targets)!=1 or targets[0] != dict(
            source='heap_noop.c', rom_start=0x36984, rom_end=0x3698C,
            splat_original='[0x36750, asm]',
            splat_replacement='[0x36750, asm]\n    - [0x36984, c, heap_noop]\n    - [0x3698C, asm]',
            asm_no_padding=['3698C'],
            functions=[dict(name='func_80035D84_36984',rom_offset=0x36984,size=8)]):
            raise ValueError('Pinned empty-function split mismatch')
    if 'vm_assignment_table_layout' in manifest:
        if manifest['vm_assignment_table_layout'] is not True:
            raise ValueError('Unsupported VM table layout preset')
        vm=[u for u in manifest['units'] if u['source']=='script_vm.c']
        if (manifest['upstream_commit']!='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee' or len(vm)!=1 or
            not any(f==dict(name='func_8003DB0C_3E70C',rom_offset=0x3E70C,size=224) for f in vm[0]['functions'])):
            raise ValueError('VM table layout requires pinned assignment handler')
    crossregion47=manifest.get('overlay_crossregion47_stage')
    if crossregion47 is not None:
        if crossregion47!={'format':overlay_crossregion47.STAGE_FORMAT}:
            raise ValueError('Unsupported original-USA 47-overlay C stage version')
        if file11_stage_mode(manifest)!=183:
            raise ValueError('47 overlay C requires current pinned 183-file11 / 346-C baseline')
        reviewed=overlay_crossregion47.load_fixture()['functions']
        original=claimed_functions({k:v for k,v in manifest.items()
                                   if k!='overlay_crossregion47_stage'})
        names={f['name'] for f in original}
        intervals=[(f['rom_offset'],f['rom_offset']+f['size']) for f in original]
        if len(original)!=346 or len(names)!=346:
            raise ValueError('47 overlay stage base must own exactly 346 canonical functions')
        for row in reviewed:
            if row['name'] in names or any(a<row['rom_offset']+row['size'] and row['rom_offset']<b
                                          for a,b in intervals):
                raise ValueError('Repeated native C ownership in reviewed 47-overlay batch')
    return manifest


def apply_units(checkout,manifest,source_dir=ROOT,reference_rom=None):
    """Apply only to a newly cloned candidate; fail before writes on collisions."""
    checkout=Path(checkout);source_dir=Path(source_dir)
    config=checkout/'config/usa/splat.yaml'
    text=config.read_text(encoding='utf-8')
    file11_copies=[]
    file11_inline=[]
    file11_mode=file11_stage_mode(manifest)
    if file11_mode is not None:
        if reference_rom is None:
            raise ValueError('file_11 staging requires authenticated USA decompressed ROM')
        if file11_mode in (143,144,152,179,183):
            adapter=file11_adapter(file11_mode)
            plan=adapter.reviewed_plan(manifest,reference_rom)
            file11_inline=adapter.source_payloads(checkout,plan)
            text=adapter.stage_splat(text,plan)
        else:
            file11_copies=overlay_file11.checked_source_copies(checkout,source_dir/'research',reference_rom)
            text=overlay_file11.stage_config(text)
            if file11_mode == 50:
                file11_copies.extend(overlay_file11_noops.checked_source_copies(
                    checkout,source_dir/'research',reference_rom))
                text=overlay_file11_noops.stage_splat(text)
    file43_stage=manifest.get('overlay_file43_stage')
    file12_stages=manifest_file12_stages(manifest)
    file13_stages=manifest_file13_stages(manifest)
    file43_source=None
    file12_sources=[]
    file43_asm_objects=()
    file12_asm_objects=()
    file13_sources=[]
    file13_asm_objects=()
    if file43_stage is not None:
        if reference_rom is None:
            raise ValueError('file_43 staging requires the verified decompressed ROM')
        file43_source=validate_file43_stage(file43_stage,text,reference_rom,source_dir)
        text,before,after=stage_file43_splat(text,file43_stage)
        file43_asm_objects=(before,after)
        file43_destination=checkout/'src'/file43_source.name
        if file43_destination.exists():
            raise ValueError('Existing file_43 candidate source destination')
    if file12_stages:
        if reference_rom is None:
            raise ValueError('file_12 staging requires the verified decompressed ROM')
        for stage in file12_stages:
            source=validate_file12_stage(stage,text,reference_rom,source_dir)
            destination=checkout/'src'/source.name
            if destination.exists():
                raise ValueError('Existing file_12 candidate source destination')
            file12_sources.append(source)
        text,file12_asm_objects=stage_file12_splats(text,file12_stages)
    if file13_stages:
        if reference_rom is None:
            raise ValueError('file_13 staging requires the verified decompressed ROM')
        for file13_stage in file13_stages:
            file13_source=validate_file13_stage(
                file13_stage,text,reference_rom,source_dir
            )
            file13_destination=checkout/'src'/file13_source.name
            if file13_destination.exists():
                raise ValueError('Existing file_13 candidate source destination')
            file13_sources.append(file13_source)
        text,file13_asm_objects=stage_file13_splat(text,file13_stages)
    if manifest.get('splat_options'):
        if text.count('options:\n')!=1:raise ValueError('Missing/ambiguous Splat options anchor')
        text=text.replace('options:\n','options:\n  asm_jtbl_label_macro: glabel\n')
    makefile=None
    if manifest.get('vm_assignment_table_layout'):
        replacements={
            '    - [0x7B6F0, rodata, main_continued]':
            '    - [0x7B6F0, rodata, main_continued]\n    - [0x7DC2C, .rodata, script_vm]\n    - [0x7DC68, rodata, main_continued_after_vm_store]'}
        # Restrict subalignment to the pinned main segment only.
        main_start=text.index('    start: 0x1050')
        main_end=text.index('    subsegments:',main_start)
        header=text[main_start:main_end]
        if header.count('    subalign: 16')!=1:raise ValueError('Missing main subalignment anchor')
        text=text[:main_start]+header.replace('    subalign: 16','    subalign: 4')+text[main_end:]
        for before,after in replacements.items():
            if text.count(before)!=1:raise ValueError('Missing/ambiguous VM layout anchor')
            text=text.replace(before,after)
        makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve the 4-byte-aligned prefix before the migrated VM table.\nbuild/usa/asm/usa/data/main_continued.rodata.s.o: ASFLAGS += --no-pad-sections\n'
    no_padding=[name for unit in manifest['units'] for name in unit.get('asm_no_padding',[])]
    if no_padding:
        if len(no_padding)!=len(set(no_padding)):raise ValueError('Duplicate assembly no-padding object')
        if makefile is None:makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve exact lengths of assembly slices adjoining C functions.\n'
        for name in no_padding:
            makefile+=f'build/usa/asm/usa/{name}.s.o: ASFLAGS += --no-pad-sections\n'
    if file43_asm_objects:
        if makefile is None:makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve exact file_43 assembly slices around the staged C function.\n'
        for name in file43_asm_objects:
            makefile+=f'build/usa/asm/usa/{name}.s.o: ASFLAGS += --no-pad-sections\n'
    if file12_asm_objects:
        if makefile is None:makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve exact file_12 assembly slices around staged C functions.\n'
        for name in file12_asm_objects:
            makefile+=f'build/usa/asm/usa/{name}.s.o: ASFLAGS += --no-pad-sections\n'
    if file13_asm_objects:
        if makefile is None:makefile=(checkout/'Makefile').read_text(encoding='utf-8')
        makefile+='\n# Preserve exact file_13 assembly slices around the staged C function.\n'
        for name in file13_asm_objects:
            makefile+=f'build/usa/asm/usa/{name}.s.o: ASFLAGS += --no-pad-sections\n'
    copies=[]
    copies=list(file11_copies)
    for name in manifest.get('support_headers',[]):
        source=source_dir/name;destination=checkout/'src'/name
        if not source.is_file() or destination.exists():raise ValueError('Missing or existing support header')
        copies.append((source,destination))
    for unit in manifest['units']:
        anchor=unit['splat_original']
        if text.count(anchor)!=1:raise ValueError('Pinned assembly anchor missing/ambiguous: '+anchor)
        source=source_dir/unit['source'];destination=checkout/'src'/unit['source']
        if not source.is_file() or destination.exists():raise ValueError('Missing source or existing candidate source')
        text_source=source.read_text(encoding='utf-8')
        placeholders=re.findall(r'^#pragma GLOBAL_ASM\("[^"\n]*/(func_[0-9A-F_]+)\.s"\)',text_source,re.MULTILINE)
        if set(placeholders)!=set(unit.get('assembly_functions',[])) or text_source.count('GLOBAL_ASM')!=len(placeholders):
            raise ValueError('Undeclared assembly placeholder in C unit')
        copies.append((source,destination));text=text.replace(anchor,unit['splat_replacement'])
    if file43_source is not None:
        copies.append((file43_source,checkout/'src'/file43_source.name))
    for file12_source in file12_sources:
        copies.append((file12_source,checkout/'src'/file12_source.name))
    for file13_source in file13_sources:
        copies.append((file13_source,checkout/'src'/file13_source.name))
    staged_patches=[]
    for entry in manifest.get('existing_source_patches', []):
        destination=checkout/'src'/entry['source']
        candidate=source_dir/entry['candidate_source']
        if not destination.is_file() or not candidate.is_file():
            raise ValueError('Existing C source or reviewed candidate missing')
        staged=prepare_collision_gate(destination.read_text(encoding='utf-8'),
                                      candidate.read_text(encoding='utf-8'))
        if digest(staged.encode('utf-8'), 'sha256') != entry['patched_sha256_lf']:
            raise ValueError('Pinned collision source patch hash mismatch')
        staged_patches.append((destination,staged))
    for source,destination in copies:shutil.copyfile(source,destination)
    for destination,content in file11_inline:
        destination.write_text(content,encoding='utf-8',newline='\n')
    for destination,staged in staged_patches:
        destination.write_text(staged,encoding='utf-8',newline='\n')
    config.write_text(text,encoding='utf-8',newline='\n')
    if makefile is not None:(checkout/'Makefile').write_text(makefile,encoding='utf-8',newline='\n')


def parse_symbols(text):
    symbols={}
    for line in text.splitlines():
        match=re.fullmatch(r'([0-9a-fA-F]+)\s+[A-Za-z]\s+(\S+)',line.strip())
        if match:symbols[match[2]]=int(match[1],16)
    return symbols


def compare_images(expected,candidate,manifest,symbols):
    if digest(expected)!=manifest['decompressed_sha1']:raise ValueError('Reference ROM identity mismatch')
    functions=[]
    for unit in manifest['units']:
        if unit['rom_end']>len(expected):raise ValueError('Unit extends outside reference ROM')
    for fn in main_claimed_functions(manifest):
        if fn['rom_offset'] + fn['size'] > len(expected):
            raise ValueError('Claimed function extends outside reference ROM')
        offset,size=fn['rom_offset'],fn['size']
        expected_address=int(fn['name'].split('_')[1],16)
        address=symbols.get(fn['name'])
        actual_offset=(address-0x7FFFF400) if address is not None else -1
        actual=candidate[actual_offset:actual_offset+size] if actual_offset>=0 else b''
        matched=(address==expected_address and len(actual)==size and
                 expected[offset:offset+size]==actual and fn['name']+'.NON_MATCHING' not in symbols)
        functions.append(dict(name=fn['name'],size=size,guest_address=f'0x{expected_address:08X}',
            rom_offset=f'0x{offset:X}',matched=matched,
            expected_sha256=digest(expected[offset:offset+size],'sha256'),
            candidate_sha256=digest(actual,'sha256')))
    full_match=len(expected)==len(candidate) and digest(candidate)==manifest['decompressed_sha1']
    return dict(full_rom_match=full_match,expected_sha1=digest(expected),candidate_sha1=digest(candidate),
        rom_size=len(candidate),matched_functions=sum(f['matched'] for f in functions),
        claimed_functions=len(functions),matched_function_bytes=sum(f['size'] for f in functions if f['matched']),
        functions=functions)


def _file43_map_block(mapping):
    section = re.search(r'(?m)^\.file_43\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\b', mapping)
    if section is None:
        raise ValueError('Link map has no .file_43 output section')
    bss = re.search(r'(?m)^\.file_43_bss(?:\s|$)', mapping[section.end():])
    if bss is None:
        raise ValueError('Link map has no .file_43_bss boundary')
    return int(section.group(1), 16), int(section.group(2), 16), mapping[
        section.start():section.end() + bss.start()
    ]


def verify_file43_ownership(candidate_checkout, stage):
    """Prove the staged source object owns the function inside the .file_43 map block."""
    validate_file43_stage_definition(stage)
    checkout = Path(candidate_checkout)
    function = stage['function']
    name = function['name']
    source_name = PurePosixPath(stage['source']).name
    source_path = checkout / 'src' / source_name
    if not source_path.is_file() or digest(source_path.read_bytes().replace(b'\r\n', b'\n'), 'sha256') != stage['source_sha256']:
        raise ValueError('Staged file_43 source hash mismatch')

    c_object_name = f'build/usa/src/{source_name}.o'
    c_object = checkout / c_object_name
    if not c_object.is_file() or digest(c_object.read_bytes(), 'sha256') != stage['object_sha256']:
        raise ValueError('Staged file_43 C object hash mismatch')
    c_elf = Elf32(c_object.read_bytes())
    c_functions = [symbol for symbol in c_elf.symbols
                   if symbol.kind == 2 and symbol.size > 0 and
                   0 < symbol.section < len(c_elf.sections)]
    if len(c_functions) != 1 or c_functions[0].name != name:
        raise ValueError('file_43 C object must define only its staged function')
    if (c_functions[0].binding != 1 or c_functions[0].size != function['size'] or
            not (c_elf.sections[c_functions[0].section][2] & 0x4)):
        raise ValueError('file_43 C object function binding, extent or section differs')
    text_sections = [section for index, section in enumerate(c_elf.sections)
                     if c_elf.names[index] == '.text']
    if len(text_sections) != 1 or text_sections[0][8] != 4:
        raise ValueError('file_43 C object .text alignment differs from staged layout')

    before, after, _ = _file43_stage_segments(stage)
    assembly_objects = []
    for segment in (before, after):
        object_name = f'build/usa/asm/usa/{segment}.s.o'
        object_path = checkout / object_name
        if not object_path.is_file():
            raise ValueError('Missing generated file_43 assembly slice: ' + segment)
        assembly_elf = Elf32(object_path.read_bytes())
        text_sections = [section for index, section in enumerate(assembly_elf.sections)
                         if assembly_elf.names[index] == '.text']
        expected_alignment = 16 if segment == before else 4
        if (len(text_sections) != 1 or not text_sections[0][2] & 0x4 or
                text_sections[0][8] != expected_alignment):
            raise ValueError('file_43 assembly .text alignment differs for ' + segment)
        if any(symbol.name == name and symbol.section != 0 for symbol in assembly_elf.symbols):
            raise ValueError('Generated assembly still owns staged file_43 function')
        assembly_objects.append(object_name)

    mapping = (checkout / 'build/usa/mnsg.map').read_text(encoding='utf-8')
    section_vma, section_size, block = _file43_map_block(mapping)
    if (section_vma != overlay_file43.VMA_START or
            section_size != overlay_file43.ROM_END - overlay_file43.ROM_START):
        raise ValueError('Link map .file_43 extent differs from pinned overlay')
    expected_inputs = [c_object_name + '(.text)'] + [name + '(.text)' for name in assembly_objects]
    for input_name in expected_inputs:
        count = len(re.findall(r'(?m)^\s*' + re.escape(input_name) + r'\s*$', block))
        if count != 1:
            raise ValueError('Link map does not place the expected file_43 object exactly once: ' + input_name)
    if re.search(r'(?m)^\s*build/usa/asm/usa/file_43\.s\.o\(\.text\)\s*$', block):
        raise ValueError('Link map retains unsplit file_43 assembly text')
    symbol_lines = re.findall(
        r'(?m)^\s*0x([0-9a-fA-F]+)\s+' + re.escape(name) + r'\s*$', block
    )
    if [int(value, 16) for value in symbol_lines] != [function['vma']]:
        raise ValueError('Link map does not place the staged function at its explicit VMA')
    return {
        'source': stage['source'],
        'source_sha256': stage['source_sha256'],
        'c_object': c_object_name,
        'object_sha256': stage['object_sha256'],
        'assembly_objects': assembly_objects,
        'file_43_vma': f'0x{section_vma:08X}',
        'file_43_size': section_size,
        'function': name,
        'function_vma': f'0x{function["vma"]:08X}',
        'function_size': function['size'],
    }


def verify_file43_stage_build(baseline_checkout, candidate_checkout, stage, reference_rom):
    """Verify the staged section split, object ownership and linked ELF provenance."""
    candidate_checkout = Path(candidate_checkout)
    ownership = verify_file43_ownership(candidate_checkout, stage)
    baseline_checkout = Path(baseline_checkout)
    original_splat = (baseline_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    expected_splat, _, _ = stage_file43_splat(original_splat, stage)
    candidate_splat = (candidate_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    original_block_start = re.search(r'(?m)^  - name: file_43\s*$', expected_splat)
    candidate_block_start = re.search(r'(?m)^  - name: file_43\s*$', candidate_splat)
    if original_block_start is None or candidate_block_start is None:
        raise ValueError('Missing staged file_43 Splat block')
    expected_next = re.search(r'(?m)^  - name: file_44\s*$', expected_splat[original_block_start.start():])
    candidate_next = re.search(r'(?m)^  - name: file_44\s*$', candidate_splat[candidate_block_start.start():])
    if expected_next is None or candidate_next is None:
        raise ValueError('Missing file_43 Splat end boundary')
    expected_block = expected_splat[original_block_start.start():original_block_start.start() + expected_next.start()]
    candidate_block = candidate_splat[candidate_block_start.start():candidate_block_start.start() + candidate_next.start()]
    if candidate_block != expected_block:
        raise ValueError('Candidate file_43 Splat block differs from staged split')

    baseline_elf = (baseline_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_elf = (candidate_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_symbols = Elf32(candidate_elf)
    if any(symbol.name == stage['function']['name'] + '.NON_MATCHING'
           for symbol in candidate_symbols.symbols):
        raise ValueError('Staged file_43 function retains a NON_MATCHING marker')
    linked = overlay_file43.validate_linked_elf_provenance(
        original_splat, reference_rom, baseline_elf, candidate_elf,
        (stage['function']['name'],)
    )['linked_elf_provenance']
    return {'ownership': ownership, 'linked_elf_provenance': linked}


def append_file43_function_comparison(comparison, stage, linked_provenance):
    """Add the explicit overlay proof without applying the main-segment VMA formula."""
    function = stage['function']
    proof = linked_provenance['functions']
    if len(proof) != 1 or proof[0]['name'] != function['name']:
        raise ValueError('Linked overlay proof does not cover the staged function')
    row = proof[0]
    expected = overlay_file43.FUNCTIONS[function['name']]
    if (row.get('section') != '.file_43' or
            row.get('vma') != f'0x{function["vma"]:08X}' or
            row.get('rom_offset') != f'0x{function["rom_offset"]:X}' or
            row.get('bytes') != function['size'] or
            row.get('original_sha256') != expected[3] or
            row.get('candidate_sha256') != expected[3] or
            not row.get('candidate_code_matches_original') or
            not row.get('candidate_relocations_match_reference')):
        raise ValueError('Staged overlay function failed linked provenance')
    comparison['functions'].append({
        'name': function['name'], 'size': function['size'],
        'guest_address': f'0x{function["vma"]:08X}',
        'rom_offset': f'0x{function["rom_offset"]:X}', 'matched': True,
        'expected_sha256': row['original_sha256'],
        'candidate_sha256': row['candidate_sha256'],
        'relocation_count': row['relocation_count'],
    })
    comparison['claimed_functions'] += 1
    comparison['matched_functions'] += 1
    comparison['matched_function_bytes'] += function['size']


def require_file43_full_rom_match(comparison):
    """Keep overlay function evidence behind the mandatory complete-ROM gate."""
    if not comparison.get('full_rom_match', False):
        raise ValueError('Candidate failed complete-ROM comparison before file_43 proof')


def _file12_map_block(mapping):
    section = re.search(r'(?m)^\.file_12\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\b', mapping)
    if section is None:
        raise ValueError('Link map has no .file_12 output section')
    bss = re.search(r'(?m)^\.file_12_bss(?:\s|$)', mapping[section.end():])
    if bss is None:
        raise ValueError('Link map has no .file_12_bss boundary')
    return int(section.group(1), 16), int(section.group(2), 16), mapping[
        section.start():section.end() + bss.start()
    ]


def verify_file12_ownership(candidate_checkout, stage):
    """Prove every staged callback and assembly gap in the .file_12 map."""
    stages = _file12_stage_list(stage)
    layout = _file12_stages_layout(stages)
    checkout = Path(candidate_checkout)
    staged_names = {item['function']['name'] for item in stages}
    callback_proofs = []
    c_object_names = []
    for item in stages:
        validate_file12_stage_definition(item)
        function = item['function']
        name = function['name']
        source_name = PurePosixPath(item['source']).name
        source_path = checkout / 'src' / source_name
        if (not source_path.is_file() or
                digest(source_path.read_bytes().replace(b'\r\n', b'\n'), 'sha256') !=
                item['source_sha256']):
            raise ValueError('Staged file_12 source hash mismatch')

        c_object_name = f'build/usa/src/{source_name}.o'
        c_object_names.append(c_object_name)
        c_object = checkout / c_object_name
        if (not c_object.is_file() or
                digest(c_object.read_bytes(), 'sha256') != item['object_sha256']):
            raise ValueError('Staged file_12 C object hash mismatch')
        c_elf = Elf32(c_object.read_bytes())
        c_functions = [symbol for symbol in c_elf.symbols
                       if symbol.kind == 2 and symbol.size > 0 and
                       0 < symbol.section < len(c_elf.sections)]
        if len(c_functions) != 1 or c_functions[0].name != name:
            raise ValueError('file_12 C object must define only its staged function')
        c_symbol = c_functions[0]
        if (c_symbol.binding != 1 or c_symbol.value != 0 or
                c_symbol.size != function['size'] or
                not (c_elf.sections[c_symbol.section][2] & 0x4) or
                c_elf.names[c_symbol.section] != '.text'):
            raise ValueError('file_12 C object function binding, extent or section differs')
        c_text = c_elf.sections[c_symbol.section]
        if c_text[5] != function['size'] or c_text[8] != 4:
            raise ValueError('file_12 C object .text size or alignment differs')
        relocations = c_elf.relocations(c_symbol.section)
        observed = tuple(sorted(
            (item.offset, item.relocation_type, item.symbol.name)
            for item in relocations
        ))
        if observed != overlay_file12.FUNCTION_RELOCATIONS[name]:
            raise ValueError('file_12 C object relocation signature differs')
        callback_proofs.append({
            'source': item['source'],
            'source_sha256': item['source_sha256'],
            'c_object': c_object_name,
            'object_sha256': item['object_sha256'],
            'function': name,
            'function_vma': f'0x{function["vma"]:08X}',
            'function_size': function['size'],
        })

    assembly_objects = []
    for index, segment in enumerate(layout['assembly']):
        expected_alignment = 16 if index == 0 else 4
        object_name = f'build/usa/asm/usa/{segment}.s.o'
        object_path = checkout / object_name
        if not object_path.is_file():
            raise ValueError('Missing generated file_12 assembly slice: ' + segment)
        assembly_elf = Elf32(object_path.read_bytes())
        text_sections = [section for index, section in enumerate(assembly_elf.sections)
                         if assembly_elf.names[index] == '.text']
        if (len(text_sections) != 1 or not text_sections[0][2] & 0x4 or
                text_sections[0][8] != expected_alignment):
            raise ValueError('file_12 assembly .text alignment differs for ' + segment)
        if any(symbol.name in staged_names and symbol.section != 0
               for symbol in assembly_elf.symbols):
            raise ValueError('Generated assembly still owns staged file_12 function')
        assembly_objects.append(object_name)

    mapping = (checkout / 'build/usa/mnsg.map').read_text(encoding='utf-8')
    section_vma, section_size, block = _file12_map_block(mapping)
    if (section_vma != overlay_file12.VMA_START or
            section_size != overlay_file12.ROM_END - overlay_file12.ROM_START):
        raise ValueError('Link map .file_12 extent differs from pinned overlay')
    expected_inputs = [assembly_objects[0]]
    assembly_cursor = 1
    for index, (item, c_object_name) in enumerate(zip(stages, c_object_names)):
        expected_inputs.append(c_object_name)
        function = item['function']
        function_end = function['rom_offset'] + function['size']
        has_gap = (index + 1 < len(stages) and
                   stages[index + 1]['function']['rom_offset'] > function_end)
        if has_gap or index + 1 == len(stages):
            expected_inputs.append(assembly_objects[assembly_cursor])
            assembly_cursor += 1
    positions = []
    for input_name in expected_inputs:
        input_pattern = r'(?m)^\s*' + re.escape(input_name + '(.text)') + r'\s*$'
        hits = list(re.finditer(input_pattern, block))
        if len(hits) != 1:
            raise ValueError('Link map does not place expected file_12 object exactly once: ' + input_name)
        positions.append(hits[0].start())
    if positions != sorted(positions):
        raise ValueError('Link map file_12 objects are not in original order')
    if re.search(r'(?m)^\s*build/usa/asm/usa/5C8770\.s\.o\(\.text\)\s*$', block):
        raise ValueError('Link map retains unsplit file_12 assembly text')

    def input_text_extent(input_name):
        match = re.search(
            r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+' +
            re.escape(input_name) + r'\s*$', block
        )
        if match is None:
            raise ValueError('Link map omits file_12 input text extent: ' + input_name)
        return int(match.group(1), 16), int(match.group(2), 16)

    text_end_vma = overlay_file12.VMA_START + (
        overlay_file12.ROM_TEXT_END - overlay_file12.ROM_START
    )
    first_vma = stages[0]['function']['vma']
    if input_text_extent(assembly_objects[0]) != (
            overlay_file12.VMA_START, first_vma - overlay_file12.VMA_START):
        raise ValueError('file_12 prefix assembly does not begin at the overlay VMA')
    assembly_cursor = 1
    for index, (item, c_object_name) in enumerate(zip(stages, c_object_names)):
        function = item['function']
        name = function['name']
        if input_text_extent(c_object_name) != (function['vma'], function['size']):
            raise ValueError('Link map does not place file_12 C at its exact VMA and size')
        symbol_lines = re.findall(
            r'(?m)^\s*0x([0-9a-fA-F]+)\s+' + re.escape(name) + r'\s*$', block
        )
        if [int(value, 16) for value in symbol_lines] != [function['vma']]:
            raise ValueError('Link map does not place the staged file_12 function at its original VMA')
        function_end_vma = function['vma'] + function['size']
        if index + 1 < len(stages):
            next_function = stages[index + 1]['function']
            next_vma = next_function['vma']
        else:
            next_vma = text_end_vma
        if next_vma > function_end_vma:
            expected_extent = (function_end_vma, next_vma - function_end_vma)
            if input_text_extent(assembly_objects[assembly_cursor]) != expected_extent:
                raise ValueError('file_12 assembly gap does not preserve its original extent')
            assembly_cursor += 1
    bss_match = re.search(
        r'(?m)^\.file_12_bss\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)', mapping
    )
    if (bss_match is None or int(bss_match.group(1), 16) !=
            overlay_file12.VMA_START + section_size or int(bss_match.group(2), 16) != 0):
        raise ValueError('Link map .file_12_bss boundary differs from pinned overlay')
    result = {
        'callbacks': callback_proofs,
        'assembly_objects': assembly_objects,
        'file_12_vma': f'0x{section_vma:08X}',
        'file_12_size': section_size,
    }
    if len(callback_proofs) == 1:
        result.update(callback_proofs[0])
    return result


def verify_file12_stage_build(baseline_checkout, candidate_checkout, stage, reference_rom):
    """Verify the staged split, object ownership and linked ELF provenance."""
    stages = _file12_stage_list(stage)
    candidate_checkout = Path(candidate_checkout)
    ownership = verify_file12_ownership(candidate_checkout, stages)
    baseline_checkout = Path(baseline_checkout)
    original_splat = (baseline_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    expected_splat, _ = stage_file12_splats(original_splat, stages)
    candidate_splat = (candidate_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    original_block_start = re.search(r'(?m)^  - name: file_12\s*$', expected_splat)
    candidate_block_start = re.search(r'(?m)^  - name: file_12\s*$', candidate_splat)
    if original_block_start is None or candidate_block_start is None:
        raise ValueError('Missing staged file_12 Splat block')
    expected_next = re.search(r'(?m)^  - name: file_13\s*$',
                               expected_splat[original_block_start.start():])
    candidate_next = re.search(r'(?m)^  - name: file_13\s*$',
                               candidate_splat[candidate_block_start.start():])
    if expected_next is None or candidate_next is None:
        raise ValueError('Missing file_12 Splat end boundary')
    expected_block = expected_splat[
        original_block_start.start():original_block_start.start() + expected_next.start()
    ]
    candidate_block = candidate_splat[
        candidate_block_start.start():candidate_block_start.start() + candidate_next.start()
    ]
    if candidate_block != expected_block:
        raise ValueError('Candidate file_12 Splat block differs from staged split')

    baseline_elf = (baseline_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_elf = (candidate_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_symbols = Elf32(candidate_elf)
    if any(symbol.name in {
            item['function']['name'] + '.NON_MATCHING' for item in stages
    }
           for symbol in candidate_symbols.symbols):
        raise ValueError('Staged file_12 function retains a NON_MATCHING marker')
    linked = overlay_file12.validate_linked_elf_provenance(
        original_splat, reference_rom, baseline_elf, candidate_elf,
        tuple(item['function']['name'] for item in stages)
    )['linked_elf_provenance']
    return {'ownership': ownership, 'linked_elf_provenance': linked}


def append_file12_function_comparison(comparison, stage, linked_provenance):
    """Add the explicit file_12 function only after exact linked provenance."""
    stages = _file12_stage_list(stage)
    proof = linked_provenance['functions']
    proof_by_name = {row.get('name'): row for row in proof}
    if len(proof_by_name) != len(proof) or set(proof_by_name) != {
            item['function']['name'] for item in stages}:
        raise ValueError('Linked file_12 proof does not cover all staged functions')
    for stage_item in stages:
        function = stage_item['function']
        row = proof_by_name[function['name']]
        expected = overlay_file12.FUNCTIONS[function['name']]
        if (row.get('section') != '.file_12' or
                row.get('vma') != f'0x{function["vma"]:08X}' or
                row.get('rom_offset') != f'0x{function["rom_offset"]:X}' or
                row.get('bytes') != function['size'] or
                row.get('original_sha256') != expected[3] or
                row.get('candidate_sha256') != expected[3] or
                not row.get('candidate_code_matches_original') or
                not row.get('candidate_relocations_match_reference')):
            raise ValueError('Staged file_12 function failed linked provenance')
        comparison['functions'].append({
            'name': function['name'], 'size': function['size'],
            'guest_address': f'0x{function["vma"]:08X}',
            'rom_offset': f'0x{function["rom_offset"]:X}', 'matched': True,
            'expected_sha256': row['original_sha256'],
            'candidate_sha256': row['candidate_sha256'],
            'relocation_count': row['relocation_count'],
        })
        comparison['claimed_functions'] += 1
        comparison['matched_functions'] += 1
        comparison['matched_function_bytes'] += function['size']


def require_file12_full_rom_match(comparison):
    """Keep file_12 function evidence behind the complete-ROM gate."""
    if not comparison.get('full_rom_match', False):
        raise ValueError('Candidate failed complete-ROM comparison before file_12 proof')


def verify_file13_stage_build(baseline_checkout, candidate_checkout,
                              stage_or_stages, reference_rom):
    """Verify each file_13 C source, linked extent, and complete overlay bytes."""
    stages = _file13_stage_list(stage_or_stages)
    for stage in stages:
        validate_file13_stage_definition(stage)
    layout = _file13_stages_layout(stages)
    candidate_checkout = Path(candidate_checkout)
    function_names = [stage['function']['name'] for stage in stages]

    for stage in stages:
        source_name = PurePosixPath(stage['source']).name
        source_path = candidate_checkout / 'src' / source_name
        if (not source_path.is_file() or
                digest(source_path.read_bytes().replace(b'\r\n', b'\n'), 'sha256') !=
                stage['source_sha256']):
            raise ValueError('Staged file_13 source hash mismatch')
        c_object = f'build/usa/src/{source_name}.o'
        c_path = candidate_checkout / c_object
        if not c_path.is_file() or digest(c_path.read_bytes(), 'sha256') != stage['object_sha256']:
            raise ValueError('Staged file_13 C object hash mismatch')
        c_elf = Elf32(c_path.read_bytes())
        c_symbol = c_elf.function(stage['function']['name'])
        if (c_symbol.value, c_symbol.size, c_symbol.binding) != (
                0, stage['function']['size'], 1):
            raise ValueError('Staged file_13 C function object identity differs')

    assembly_objects = []
    for index, name in enumerate(layout['assembly']):
        object_name = f'build/usa/asm/usa/{name}.s.o'
        assembly_objects.append(object_name)
        object_path = candidate_checkout / object_name
        if not object_path.is_file():
            raise ValueError('Missing generated file_13 assembly slice')
        assembly = Elf32(object_path.read_bytes())
        text_indices = [i for i, label in enumerate(assembly.names) if label == '.text']
        expected_alignment = 16 if index == 0 else 4
        if (len(text_indices) != 1 or
                assembly.sections[text_indices[0]][8] != expected_alignment):
            raise ValueError('Generated file_13 assembly text layout differs')
        if any(symbol.name in function_names and symbol.section != 0
               for symbol in assembly.symbols):
            raise ValueError('Generated file_13 assembly still owns a C function')

    baseline_checkout = Path(baseline_checkout)
    original_splat = (baseline_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    expected_splat, _ = stage_file13_splat(original_splat, stages)
    candidate_splat = (candidate_checkout / 'config/usa/splat.yaml').read_text(encoding='utf-8')
    expected_start = re.search(r'(?m)^  - name: file_13\s*$', expected_splat)
    candidate_start = re.search(r'(?m)^  - name: file_13\s*$', candidate_splat)
    if expected_start is None or candidate_start is None:
        raise ValueError('Missing staged file_13 Splat block')
    expected_end = re.search(r'(?m)^  - name: file_14\s*$',
                              expected_splat[expected_start.start():])
    candidate_end = re.search(r'(?m)^  - name: file_14\s*$',
                              candidate_splat[candidate_start.start():])
    if expected_end is None or candidate_end is None:
        raise ValueError('Missing file_13 Splat end boundary')
    expected_block = expected_splat[
        expected_start.start():expected_start.start() + expected_end.start()
    ]
    candidate_block = candidate_splat[
        candidate_start.start():candidate_start.start() + candidate_end.start()
    ]
    if candidate_block != expected_block:
        raise ValueError('Candidate file_13 Splat block differs from staged split')

    mapping = (candidate_checkout / 'build/usa/mnsg.map').read_text(encoding='utf-8')
    section_match = re.search(
        r'(?m)^\.file_13\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\b', mapping
    )
    if section_match is None:
        raise ValueError('Link map has no .file_13 output section')
    bss_match = re.search(r'(?m)^\.file_13_bss(?:\s|$)', mapping[section_match.end():])
    if bss_match is None:
        raise ValueError('Link map has no .file_13_bss boundary')
    section_vma, section_size = (int(section_match.group(i), 16) for i in (1, 2))
    if (section_vma, section_size) != (
            overlay_file13.VMA_START, overlay_file13.ROM_END - overlay_file13.ROM_START):
        raise ValueError('Link map .file_13 VMA or extent differs from pinned overlay')
    block = mapping[section_match.start():section_match.end() + bss_match.start()]

    expected_objects = []
    for obj in layout['objects']:
        if obj['kind'] == 'asm':
            name = f'build/usa/asm/usa/{obj["name"]}.s.o'
        else:
            name = f'build/usa/src/{obj["name"]}.c.o'
        expected_objects.append((name, obj))
    positions = []
    for object_name, _ in expected_objects:
        object_pattern = r'(?m)^\s*' + re.escape(object_name + '(.text)') + r'\s*$'
        hits = list(re.finditer(object_pattern, block))
        if len(hits) != 1:
            raise ValueError('Link map does not place file_13 object exactly once: ' + object_name)
        positions.append(hits[0].start())
    if positions != sorted(positions):
        raise ValueError('Link map file_13 objects are not in original order')

    def input_text_extent(object_name):
        pattern = (
            r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+' +
            re.escape(object_name) + r'\s*$'
        )
        match = re.search(pattern, block)
        if match is None:
            raise ValueError('Link map omits file_13 input text extent: ' + object_name)
        return tuple(int(match.group(i), 16) for i in (1, 2))

    for object_name, obj in expected_objects:
        vma = overlay_file13.VMA_START + (obj['start'] - overlay_file13.ROM_START)
        expected_extent = (vma, obj['end'] - obj['start'])
        if input_text_extent(object_name) != expected_extent:
            raise ValueError('Link map file_13 input does not preserve its original extent')
    for stage in stages:
        function = stage['function']
        symbol_lines = re.findall(
            r'(?m)^\s*0x([0-9a-fA-F]+)\s+' +
            re.escape(function['name']) + r'\s*$', block
        )
        if [int(value, 16) for value in symbol_lines] != [function['vma']]:
            raise ValueError('Link map does not place file_13 C function at its original VMA')

    baseline_elf = (baseline_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_elf = (candidate_checkout / 'build/usa/mnsg.elf').read_bytes()
    candidate_symbols = Elf32(candidate_elf)
    if any(symbol.name.endswith('.NON_MATCHING') and
           symbol.name[:-len('.NON_MATCHING')] in function_names
           for symbol in candidate_symbols.symbols):
        raise ValueError('Staged file_13 function retains a NON_MATCHING marker')
    linked = overlay_file13.validate_linked_elf_provenance(
        original_splat, reference_rom, baseline_elf, candidate_elf,
        tuple(function_names)
    )
    return {
        'stages': [{
            'source': stage['source'],
            'source_sha256': stage['source_sha256'],
            'compiler_object_sha256': stage['compiler_object_sha256'],
            'staged_object_sha256': stage['object_sha256'],
            'function': stage['function']['name'],
        } for stage in stages],
        'assembly_objects': assembly_objects,
        'splat_block_matches': True,
        'link_map_objects_in_order': True,
        'link_map_original_extents': True,
        'linked_elf_provenance': linked,
    }


def append_file13_function_comparison(comparison, stage_or_stages,
                                      linked_provenance):
    """Add overlay function claims only after full-ROM and ELF proof."""
    stages = _file13_stage_list(stage_or_stages)
    rows = linked_provenance.get('functions', [])
    if (len(rows) != len(stages) or
            [row.get('name') for row in rows] !=
            [stage['function']['name'] for stage in stages]):
        raise ValueError('Linked file_13 proof does not cover all staged functions')
    for stage, row in zip(stages, rows):
        function = stage['function']
        expected = overlay_file13.FUNCTIONS[function['name']]
        if (row.get('section') != '.file_13' or
                row.get('vma') != f'0x{function["vma"]:08X}' or
                row.get('rom_offset') != f'0x{function["rom_offset"]:X}' or
                row.get('bytes') != function['size'] or
                row.get('original_sha256') != expected[3] or
                row.get('candidate_sha256') != expected[3] or
                not row.get('candidate_code_matches_original') or
                not row.get('candidate_relocations_match_reference')):
            raise ValueError('Staged file_13 function failed linked provenance')
        comparison['functions'].append({
            'name': function['name'], 'size': function['size'],
            'guest_address': f'0x{function["vma"]:08X}',
            'rom_offset': f'0x{function["rom_offset"]:X}', 'matched': True,
            'expected_sha256': row['original_sha256'],
            'candidate_sha256': row['candidate_sha256'],
            'relocation_count': row['relocation_count'],
            'overlay': 'file_13',
        })
        comparison['claimed_functions'] += 1
        comparison['matched_functions'] += 1
        comparison['matched_function_bytes'] += function['size']


def require_file13_full_rom_match(comparison):
    """Keep file_13 function evidence behind the complete-ROM gate."""
    if not comparison.get('full_rom_match', False):
        raise ValueError('Candidate failed complete-ROM comparison before file_13 proof')



def baseline_identity(checkout, manifest):
    checkout = Path(checkout)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip()
    dirty = subprocess.check_output(['git', 'diff', '--name-only'], cwd=checkout, text=True).strip()
    if revision != manifest['upstream_commit'] or dirty:
        raise ValueError('Baseline cache source identity changed')
    expected = (checkout/'config/usa/baserom.decompressed.z64').read_bytes()
    image = (checkout/'build/usa/mnsg.z64').read_bytes()
    if digest(expected) != manifest['decompressed_sha1'] or image != expected:
        raise ValueError('Baseline cache ROM identity mismatch')
    compiler = {p.name: digest(p.read_bytes(), 'sha256') for p in sorted((checkout/'tools/ido-5.3').iterdir()) if p.is_file()}
    return dict(format='goemon-baseline-cache-v1', upstream_commit=revision,
                decompressed_sha1=digest(image), elf_sha256=digest((checkout/'build/usa/mnsg.elf').read_bytes(), 'sha256'),
                compiler_sha256=digest(json.dumps(compiler, sort_keys=True).encode(), 'sha256'),
                dependency_lock_sha256=digest((checkout/'uv.lock').read_bytes(), 'sha256'))


def certify_baseline(checkout, manifest):
    proof = baseline_identity(checkout, manifest)
    with (Path(checkout)/'build/goemon-baseline-proof.json').open('x', encoding='utf-8') as output:
        json.dump(proof, output, indent=2); output.write('\n')
    return proof


def validate_baseline_cache(checkout, manifest):
    recorded = json.loads((Path(checkout)/'build/goemon-baseline-proof.json').read_text(encoding='utf-8'))
    if recorded != baseline_identity(checkout, manifest):
        raise ValueError('Baseline cache provenance changed')
    if not (Path(checkout)/'.venv/bin/python').is_file():
        raise ValueError('Baseline cache dependency environment is missing')
    return recorded


def run_build(args,manifest,report):
    if os.name=='nt':raise ValueError('Run the build verifier inside Linux/WSL, not native Windows')
    upstream=args.upstream.resolve();work=args.workdir.resolve()
    if work.exists():raise ValueError('Work directory already exists; choose a new path')
    if digest(args.retail_rom.read_bytes())!=manifest['retail_sha1']:raise ValueError('Retail ROM identity mismatch')
    tool_env=os.environ.copy()
    def capture(command,cwd=None):
        return subprocess.check_output(command,cwd=cwd,text=True,stderr=subprocess.STDOUT,env=tool_env).strip()
    if capture(['git','rev-parse','HEAD'],upstream)!=manifest['upstream_commit']:
        raise ValueError('Upstream checkout is not the pinned commit')
    binutils_root=getattr(args,'binutils_root',None)
    if binutils_root is not None:
        work.mkdir(parents=True)
        tool_env=build_tool_environment(binutils_root,work/'.binutils-runtime')
        report['binutils_runtime']='pinned_curated'
    for tool in ('git','make','gcc','mips-linux-gnu-as','mips-linux-gnu-ld','mips-linux-gnu-objcopy','mips-linux-gnu-nm'):
        if not shutil.which(tool,path=tool_env.get('PATH')):raise ValueError('Required tool unavailable: '+tool)
    uv=shutil.which(args.uv,path=tool_env.get('PATH'))
    if uv is None:raise ValueError('uv is unavailable')
    requested_cache = getattr(args, 'baseline_cache', None)
    if requested_cache and work.is_relative_to(requested_cache.resolve()):
        raise ValueError('New work directory must be outside the immutable baseline cache')
    work.mkdir(parents=True,exist_ok=binutils_root is not None)
    report.update(upstream_commit=manifest['upstream_commit'],retail_sha1=manifest['retail_sha1'],
        verifier_source_sha256_lf=digest(Path(__file__).read_bytes().replace(b'\r\n',b'\n'),'sha256'),
        tool_versions={name:capture(command).splitlines()[0] for name,command in {
            'uv':[uv,'--version'],'gcc':['gcc','--version'],'assembler':['mips-linux-gnu-as','--version']}.items()})
    def logged(stage,command,cwd):
        report['stage']=stage
        with (work/(stage+'.log')).open('w',encoding='utf-8') as log:
            subprocess.run(command,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,check=True,env=tool_env)
    cache = getattr(args, 'baseline_cache', None)
    baseline = cache.resolve() if cache else work/'baseline'
    candidate = work/'candidate'
    if cache:
        if work.is_relative_to(baseline):
            raise ValueError('New work directory must be outside the immutable baseline cache')
        proof = validate_baseline_cache(baseline, manifest)
        report['baseline_cache_used'] = True
    else:
        logged('clone-baseline',['git','clone','--no-hardlinks',str(upstream),str(baseline)],work)
        logged('dependencies',[uv,'sync','--python','3.12','--frozen'],baseline)
        shutil.copyfile(args.retail_rom,baseline/'config/usa/baserom.z64')
        logged('baseline-setup',['make','setup','UV='+uv],baseline)
        logged('baseline-build',['make','-j'+str(args.jobs),'UV='+uv],baseline)
        proof = certify_baseline(baseline, manifest)
        report['baseline_cache_used'] = False
    expected=(baseline/'config/usa/baserom.decompressed.z64').read_bytes()
    report['baseline_sha1']=proof['decompressed_sha1']
    report['baseline_provenance']=proof
    logged('clone-candidate',['git','clone','--no-hardlinks',str(upstream),str(candidate)],work)
    source_dir = getattr(args, 'source_dir', ROOT).resolve()
    apply_units(candidate,manifest,source_dir,expected)
    (candidate/'.venv').symlink_to(baseline/'.venv',target_is_directory=True)
    shutil.copyfile(args.retail_rom,candidate/'config/usa/baserom.z64')
    logged('candidate-setup',['make','setup','UV='+uv],candidate)
    if file11_stage_mode(manifest) in (50,143,144,152,179,183):
        report['overlay_file11_nop_aliases']=overlay_file11_noops.patch_synthetic_nop_aliases(candidate)
        if file11_stage_mode(manifest) in (179,183):
            report['overlay_file11_additional_nop_alias']=file11_adapter(file11_stage_mode(manifest)).normalize_added_nop_alias(candidate)
    file43_stage=manifest.get('overlay_file43_stage')
    file13_stages=manifest_file13_stages(manifest)
    if file43_stage is not None:
        before, after, _ = _file43_stage_segments(file43_stage)
        logged('candidate-file43-objects',['make','-j'+str(args.jobs),'UV='+uv,
            f'build/usa/src/{PurePosixPath(file43_stage["source"]).name}.o',
            f'build/usa/asm/usa/{before}.s.o',
            f'build/usa/asm/usa/{after}.s.o'],candidate)
        report['overlay_file43_object_layout']=prepare_file43_stage_objects(
            candidate,file43_stage
        )
    file12_stages=manifest_file12_stages(manifest)
    if file12_stages:
        report['overlay_file12_tail_alias']=patch_file12_tail_alias_sources(
            candidate,file12_stages
        )
        layout = _file12_stages_layout(file12_stages)
        object_targets = [
            f'build/usa/src/{PurePosixPath(stage["source"]).name}.o'
            for stage in file12_stages
        ] + [f'build/usa/asm/usa/{name}.s.o' for name in layout['assembly']]
        logged('candidate-file12-objects',['make','-j'+str(args.jobs),'UV='+uv,
            *object_targets],candidate)
        report['overlay_file12_object_layout']=prepare_file12_stage_objects(
            candidate,file12_stages
        )
    file11_mode=file11_stage_mode(manifest)
    if file11_mode is not None:
        if file11_mode in (143,144,152,179,183):
            file11_objects=file11_adapter(file11_mode).object_targets()
        elif file11_mode == 50:
            file11_objects=overlay_file11_noops.object_targets()
        else:
            file11_objects=overlay_file11.object_targets()
        logged('candidate-file11-objects',['make','-j'+str(args.jobs),'UV='+uv,
            *file11_objects],candidate)
        if file11_mode in (143,144,152,179,183):
            report['overlay_file11_object_layout']=file11_adapter(file11_mode).prepare_objects(candidate)
        elif file11_mode == 50:
            report['overlay_file11_object_layout']=overlay_file11_noops.trim(candidate)
        else:
            report['overlay_file11_object_layout']=overlay_file11.prepare_objects(candidate)
    if file13_stages:
        layout = _file13_stages_layout(file13_stages)
        object_targets = [
            f'build/usa/src/{PurePosixPath(stage["source"]).name}.o'
            for stage in file13_stages
        ] + [f'build/usa/asm/usa/{name}.s.o' for name in layout['assembly']]
        logged('candidate-file13-objects',
               ['make', '-j' + str(args.jobs), 'UV=' + uv, *object_targets],
               candidate)
        report['overlay_file13_object_layout']=prepare_file13_stage_objects(
            candidate,file13_stages
        )
    if manifest.get('vm_assignment_table_layout'):
        logged('candidate-vm-object',['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/script_vm.c.o','build/usa/asm/usa/data/main_continued.rodata.s.o'],candidate)
        report['object_layout']=pack_object_file(candidate/'build/usa/src/script_vm.c.o')
    if manifest.get('heap_noop_text_layout'):
        logged('candidate-heap-noop-object',['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/heap_noop.c.o','build/usa/asm/usa/3698C.s.o'],candidate)
        report['heap_noop_layout']=pack_heap_noop_file(candidate/'build/usa/src/heap_noop.c.o')
    logged('candidate-build',['make','-j'+str(args.jobs),'UV='+uv],candidate)
    symbols=parse_symbols(capture(['mips-linux-gnu-nm','-n','build/usa/mnsg.elf'],candidate))
    result=compare_images(expected,(candidate/'build/usa/mnsg.z64').read_bytes(),manifest,symbols)
    if manifest.get('vm_assignment_table_layout'):
        image=(candidate/'build/usa/mnsg.z64').read_bytes()
        report['assignment_table']=dict(rom_start='0x7DC2C',size=60,
            matched=expected[0x7DC2C:0x7DC68]==image[0x7DC2C:0x7DC68],
            sha256=digest(image[0x7DC2C:0x7DC68],'sha256'))
    report['comparison']=result
    report['retained_assembly_functions']=[name for unit in manifest['units'] for name in unit.get('assembly_functions',[])]
    source_names=[unit['source'] for unit in manifest['units']]+manifest.get('support_headers',[])+[p['source'] for p in manifest.get('existing_source_patches',[])]
    report['sources_sha256_lf']={name:digest((candidate/'src'/name).read_bytes().replace(b'\r\n',b'\n'),'sha256')
                               for name in source_names}
    if file43_stage is not None:
        staged_name=PurePosixPath(file43_stage['source']).name
        report['sources_sha256_lf'][file43_stage['source']]=digest(
            (candidate/'src'/staged_name).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    for file12_stage in file12_stages:
        staged_name=PurePosixPath(file12_stage['source']).name
        report['sources_sha256_lf'][file12_stage['source']]=digest(
            (candidate/'src'/staged_name).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    if file11_mode in (143,144,152,179,183):
        for chunk in file11_adapter(file11_mode).load_fixture()['chunks']:
            if chunk['kind'] == 'c':
                name=chunk['name']
                report['sources_sha256_lf']['research/file11_143_candidate/'+name+'.c']=digest(
                    (candidate/'src'/(name+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    elif file11_mode is not None:
        for source_name, target_name, _, _ in overlay_file11.SOURCE_SPECS:
            report['sources_sha256_lf']['research/'+source_name]=digest(
                (candidate/'src'/(target_name+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
        if file11_mode == 50:
            for _, _, name in overlay_file11_noops.GROUPS:
                report['sources_sha256_lf']['research/'+name+'.c']=digest(
                    (candidate/'src'/(name+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    for file13_stage in file13_stages:
        staged_name=PurePosixPath(file13_stage['source']).name
        report['sources_sha256_lf'][file13_stage['source']]=digest(
            (candidate/'src'/staged_name).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    mapping=(candidate/'build/usa/mnsg.map').read_text()
    for unit in manifest['units']:
        object_name='build/usa/src/'+unit['source']+'.o'
        if not (candidate/object_name).is_file() or object_name not in mapping:
            raise ValueError('Reconstructed C object absent from link evidence')
    for file13_stage in file13_stages:
        object_name='build/usa/src/'+PurePosixPath(file13_stage['source']).name+'.o'
        if not (candidate/object_name).is_file() or object_name not in mapping:
            raise ValueError('file_13 C object absent from link evidence')
    if file43_stage is not None:
        require_file43_full_rom_match(result)
        report['overlay_file43_stage']=verify_file43_stage_build(
            baseline,candidate,file43_stage,expected
        )
        append_file43_function_comparison(
            result,file43_stage,report['overlay_file43_stage']['linked_elf_provenance']
        )
        report['comparison']=result
    if file12_stages:
        require_file12_full_rom_match(result)
        file12_report=verify_file12_stage_build(
            baseline,candidate,file12_stages,expected
        )
        append_file12_function_comparison(
            result,file12_stages,file12_report['linked_elf_provenance']
        )
        report['overlay_file12_stages']=file12_report
        report['comparison']=result
    if file11_mode is not None:
        if file11_mode in (143,144,152,179,183):
            proof11=file11_adapter(file11_mode).verify_linked(
                candidate,expected,baseline/'build/usa/mnsg.elf')
            proof11['stage']=file11_adapter(file11_mode).STAGE_FORMAT
            proof_functions=[
                {'name': f['name'], 'rom_offset': f['rom_offset'],
                 'vma': f['vma'], 'size': f['size'],
                 'sha256': digest(expected[f['rom_offset']:f['rom_offset']+f['size']],'sha256')}
                for f in file11_adapter(file11_mode).entries()
            ]
        elif file11_mode == 50:
            proof11=overlay_file11_noops.verify(
                candidate,expected,baseline/'build/usa/mnsg.elf')
            proof11['stage']=overlay_file11_noops.STAGE_FORMAT
            proof_functions=[
                {'name': name, 'rom_offset': rom,
                 'vma': overlay_file11.VMA_START + rom - overlay_file11.ROM_START,
                 'size': size, 'sha256': digest(expected[rom:rom+size],'sha256')}
                for name, rom, size, _ in overlay_file11.FUNCTIONS
            ]
            proof_functions.extend(
                {'name': name, 'rom_offset': rom,
                 'vma': overlay_file11.VMA_START + rom - overlay_file11.ROM_START,
                 'size': 12, 'sha256': digest(expected[rom:rom+12],'sha256')}
                for name, rom in overlay_file11_noops.entries()
            )
        else:
            proof11=overlay_file11.verify_linked_stage(
                expected,(candidate/'build/usa/mnsg.z64').read_bytes(),
                (baseline/'build/usa/mnsg.elf').read_bytes(),
                (candidate/'build/usa/mnsg.elf').read_bytes(),
                candidate,source_dir/'research'
            )
            proof_functions=proof11['functions']
        for function in proof_functions:
            result['functions'].append({
                'name': function['name'], 'size': function['size'],
                'guest_address': f'0x{function["vma"]:08X}',
                'rom_offset': f'0x{function["rom_offset"]:X}',
                'matched': True,
                'expected_sha256': function['sha256'],
                'candidate_sha256': function['sha256'],
            })
            result['claimed_functions'] += 1
            result['matched_functions'] += 1
            result['matched_function_bytes'] += function['size']
        report['overlay_file11_stage']=proof11
    if file13_stages:
        require_file13_full_rom_match(result)
        report['overlay_file13_stages']=verify_file13_stage_build(
            baseline,candidate,file13_stages,expected
        )
        append_file13_function_comparison(
            result,file13_stages,
            report['overlay_file13_stages']['linked_elf_provenance']
        )
        report['comparison']=result
    if manifest.get('overlay_crossregion47_stage') is not None:
        if (not result['full_rom_match'] or result['matched_functions']!=346
                or result['claimed_functions']!=346):
            raise ValueError('Cross-region 47 stage requires a complete native 346-C exact-ROM proof')
        import shutil as _shutil
        before=work/'pre_crossregion47'
        if before.exists():raise ValueError('Crossregion47 snapshot already exists')
        (before/'build/usa').mkdir(parents=True)
        _shutil.copyfile(candidate/'build/usa/mnsg.elf', before/'build/usa/mnsg.elf')
        fixture=overlay_crossregion47.load_fixture()
        plan=overlay_crossregion47.stage_linker(
            candidate,expected,fixture,source_dir/'research/jp_recomp_to_c/src')
        logged('crossregion47-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*overlay_crossregion47.object_targets(plan)],
               candidate)
        packed=overlay_crossregion47.pack_objects(candidate,expected,plan)
        if packed['functions']!=47 or packed['original_c_instruction_bytes']!=2220:
            raise ValueError('Unexpected 47-overlay C compiler-object proof')
        for name in ('mnsg.elf','mnsg.z64'):
            (candidate/'build/usa'/name).unlink()
        logged('crossregion47-link',['make','-j'+str(args.jobs),'UV='+uv,'build/usa/mnsg.z64'],candidate)
        proof=overlay_crossregion47.verify_link(before,candidate,expected,plan,packed)
        reported_names={f['name'] for f in result['functions']}
        actual_symbols=parse_symbols(capture(['mips-linux-gnu-nm','-n','build/usa/mnsg.elf'],candidate))
        for e in plan['functions']:
            name=e['name']
            if (name in reported_names or actual_symbols.get(name)!=e['vma']
                    or name+'.NON_MATCHING' in actual_symbols):
                raise ValueError('New 47-overlay C ELF ownership incorrect: '+name)
            row={'name':name,'size':e['size'],'guest_address':f'0x{e["vma"]:08X}',
                 'rom_offset':f'0x{e["rom_offset"]:X}','matched':True,
                 'expected_sha256':e['original_code_sha256'],
                 'candidate_sha256':e['original_code_sha256']}
            result['functions'].append(row)
            reported_names.add(name)
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=e['size']
        report['overlay_crossregion47_stage']=proof
        report['comparison']=result
        if (result['matched_functions']!=393 or result['matched_function_bytes']!=19940
                or result['claimed_functions']!=393):
            raise ValueError('Unexpected canonical USA C total following 47-overlay stage')
    if not result['full_rom_match'] or result['matched_functions']!=result['claimed_functions']:
        raise ValueError('Candidate failed exact matching')
    report['stage']='complete';report['status']='matched'


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream',type=Path,required=True)
    parser.add_argument('--workdir',type=Path,required=True,help='New directory; never reused or deleted')
    parser.add_argument('--retail-rom',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True,help='New local/ignored JSON report')
    parser.add_argument('--uv',default='uv')
    parser.add_argument('--binutils-root',type=Path,
        default=(Path(os.environ['GOEMON_MIPS_BINUTILS_ROOT'])
                 if os.environ.get('GOEMON_MIPS_BINUTILS_ROOT') else None),
        help='Root of extracted pinned cross-binutils archive; auto-reads GOEMON_MIPS_BINUTILS_ROOT')
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--baseline-cache',type=Path,help='Immutable baseline from a completed fresh verifier run')
    parser.add_argument('--manifest',type=Path,default=ROOT/'manifest.json',help='Reviewed matching manifest')
    parser.add_argument('--source-dir',type=Path,default=ROOT,help='Reviewed source/header bundle')
    args=parser.parse_args(argv)
    if args.jobs<1:parser.error('--jobs must be positive')
    report=dict(format='goemon-matching-build-result-v1',started_utc=datetime.now(timezone.utc).isoformat(),status='failed')
    if args.report.resolve()==args.retail_rom.resolve():parser.error('Report must differ from ROM')
    try:
        # Reserve before any build changes. An existing report is never replaced.
        with args.report.open('x',encoding='utf-8') as output:
            try:run_build(args,load_manifest(args.manifest),report)
            except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:report['error']=str(exc)
            finally:
                report['ended_utc']=datetime.now(timezone.utc).isoformat()
                json.dump(report,output,indent=2);output.write('\n')
    except OSError as exc:parser.exit(1,str(exc)+'\n')
    if report['status']!='matched':parser.exit(1,report.get('error','Build failed')+'\n')
    print(f'MATCH: {report["comparison"]["matched_functions"]} functions; whole-ROM SHA-1 {report["comparison"]["candidate_sha1"]}')


if __name__=='__main__':main()

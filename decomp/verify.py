"""Rebuild pinned mnsg in new Linux/WSL checkouts and verify reconstructed C.

Requires an existing local pinned upstream clone, the user's retail ROM, uv,
make, GCC and MIPS binutils. Never resets/deletes a checkout or overwrites a
report. ROMs, generated assembly, binaries and logs belong in local research
storage, not Git. Does not deploy, launch a game or submit upstream patches.
"""
from __future__ import annotations
from collections import Counter

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
    from . import file12_registration
    from . import overlay_file11
    from .research import usa_file11_noop_groups as overlay_file11_noops
    from . import overlay_file13
    from .elf_layout import pack_object_file, pack_heap_noop_file
    from .elf_layout import pack_file12_callback_text, pack_overlay_function_text
    from .collision_patch import prepare_collision_gate
    from .prepare_mips_binutils import configure as configure_binutils
    from .probe import Elf32
except ImportError:
    import overlay_file43
    import overlay_file12
    from decomp import file12_registration
    import overlay_file11
    from decomp.research import usa_file11_noop_groups as overlay_file11_noops
    import overlay_file13
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
    if mode == 184:
        from . import file11_184_stage
        return file11_184_stage
    if mode == 187:
        from . import file11_187_stage
        return file11_187_stage
    if mode == 269:
        from . import file11_269_stage
        return file11_269_stage
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
    if stage == {'format': 'goemon-file11-184-central-v1'}:
        return 184
    if stage == {'format': 'goemon-file11-187-central-v1'}:
        return 187
    if stage == {'format': 'goemon-file11-269-central-v1'}:
        return 269
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


def crossregion47_stage(manifest):
    """Only the pinned 47-function cross-overlay research source is eligible."""
    stage=manifest.get('overlay_crossregion47_stage')
    if stage is None:return None
    from . import overlay_crossregion47 as cross
    if stage!={'format':cross.STAGE_FORMAT}:
        raise ValueError('Unreviewed cross-overlay 47 promotion contract')
    return cross.load_fixture()


def native87_stage(manifest):
    """A fixed source/ROM-pinned promotion stage, not arbitrary manifest C."""
    stage=manifest.get('overlay_native87_stage')
    if stage is None:return None
    from . import overlay_native87 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed native87 production stage contract')
    return native.load_fixture()


def highbyte26_stage(manifest):
    """A fixed 15-function source/ROM-pinned file26 promotion contract."""
    stage=manifest.get('overlay_highbyte26_stage')
    if stage is None:return None
    from . import overlay_highbyte26 as high
    if stage != {'format':high.STAGE_FORMAT}:
        raise ValueError('Unreviewed highbyte26 production stage contract')
    return high.load_fixture()



def file27_stage(manifest):
    """Fixed 21-function original-USA file27 C source/ROM promotion stage."""
    stage=manifest.get('overlay_file27_stage')
    if stage is None:return None
    from . import overlay_file27 as file27
    if stage != {'format':file27.STAGE_FORMAT}:
        raise ValueError('Unreviewed file27 production stage contract')
    return file27.load_fixture()

def wide132_stage(manifest):
    """Reviewed 132-function original-ROM-pinned additive C promotion stage."""
    stage=manifest.get('overlay_wide132_stage')
    if stage is None:return None
    from . import overlay_wide132 as wide
    if stage != {'format':wide.STAGE_FORMAT}:
        raise ValueError('Unreviewed wide132 promotion contract')
    return wide.load_fixture()


def wide109_stage(manifest):
    stage=manifest.get('overlay_wide109_stage')
    if stage is None:return None
    from . import overlay_wide109 as wide109
    if stage != {'format':wide109.STAGE_FORMAT}:
        raise ValueError('Unreviewed wide109 production stage contract')
    return wide109.load_fixture()



def resource140_stage(manifest):
    stage=manifest.get('overlay_resource140_stage')
    if stage is None:return None
    from . import overlay_resource140 as research
    if stage != {'format':research.STAGE_FORMAT}:
        raise ValueError('Unreviewed resource140 production stage contract')
    return research.load_fixture()


def graphics5_stage(manifest):
    stage=manifest.get('overlay_graphics5_stage')
    if stage is None:return None
    from . import overlay_graphics5 as graphics
    if stage != {'format':graphics.STAGE_FORMAT}:
        raise ValueError('Unreviewed graphics5 production stage contract')
    return graphics.load_fixture()


def file18_53_stage(manifest):
    stage=manifest.get('overlay_file18_53_stage')
    if stage is None:return None
    from . import overlay_file18_53 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed file18_53 production stage contract')
    return native.load_fixture()


def callbacks10_stage(manifest):
    stage=manifest.get('overlay_callbacks10_stage')
    if stage is None:return None
    from . import overlay_callbacks10 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed callbacks10 production stage contract')
    return native.load_fixture()

def main19_stage(manifest):
    stage=manifest.get('overlay_main19_stage')
    if stage is None:return None
    from . import overlay_main19 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed main19 production stage contract')
    return native.load_fixture()

def tiny9_stage(manifest):
    stage=manifest.get('overlay_tiny9_stage')
    if stage is None:return None
    from . import overlay_tiny9 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed tiny9 production stage contract')
    return native.load_fixture()

def micro2_stage(manifest):
    stage=manifest.get('overlay_micro2_stage')
    if stage is None:return None
    from . import overlay_micro2 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed micro2 production stage contract')
    return native.load_fixture()

def micro15_stage(manifest):
    stage=manifest.get('overlay_micro15_stage')
    if stage is None:return None
    from . import overlay_micro15 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed micro15 production stage contract')
    return native.load_fixture()

def micro20_stage(manifest):
    stage=manifest.get('overlay_micro20_stage')
    if stage is None:return None
    from . import overlay_micro20 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed micro20 production stage contract')
    return native.load_fixture()

def menu2_stage(manifest):
    stage=manifest.get('overlay_menu2_stage')
    if stage is None:return None
    from . import overlay_menu2 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed menu2 production stage contract')
    return native.load_fixture()

def statecopy1_stage(manifest):
    stage=manifest.get('overlay_statecopy1_stage')
    if stage is None:return None
    from . import overlay_statecopy1 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed statecopy1 production stage contract')
    return native.load_fixture()

def archive22_stage(manifest):
    stage=manifest.get('overlay_archive22_stage')
    if stage is None:return None
    from . import overlay_archive22 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed archive22 production stage contract')
    return native.load_fixture()


def archive33_stage(manifest):
    stage=manifest.get('overlay_archive33_stage')
    if stage is None:return None
    from . import overlay_archive33 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed archive33 production stage contract')
    return native.load_fixture()


def archive61_stage(manifest):
    stage=manifest.get('overlay_archive61_stage')
    if stage is None:return None
    from . import overlay_archive61 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed archive61 production stage contract')
    return native.load_fixture()


def checkpoint500_stage(manifest):
    stage=manifest.get('overlay_checkpoint500_stage')
    if stage is None:return None
    from . import overlay_checkpoint500 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed checkpoint500 production stage contract')
    return native.load_fixture()


def rediscovery5_stage(manifest):
    stage=manifest.get('overlay_rediscovery5_stage')
    if stage is None:return None
    from . import overlay_rediscovery5 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed rediscovery5 production stage contract')
    return native.load_fixture()


def native49_stage(manifest):
    stage=manifest.get('overlay_native49_stage')
    if stage is None:return None
    from . import overlay_native49 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed native49 production stage contract')
    return native.load_fixture()


def native51_stage(manifest):
    stage=manifest.get('overlay_native51_stage')
    if stage is None:return None
    from . import overlay_native51 as native
    if stage != {'format':native.STAGE_FORMAT}:
        raise ValueError('Unreviewed native51 production stage contract')
    return native.load_fixture()


def isolated233_stage(manifest):
    """Return the current cumulative main-segment stage that began as 233 C functions."""
    stage = manifest.get('overlay_isolated233_stage')
    if stage is None:
        return None
    from . import overlay_isolated233 as isolated
    if stage != {'format': isolated.FORMAT}:
        raise ValueError('Unreviewed isolated main-segment native production stage contract')
    return isolated.load_fixture()


def reconcile108_stage(manifest):
    """Reviewed canonical C union, strictly relative to the existing 1,964-C proof."""
    stage = manifest.get('overlay_reconcile108_stage')
    if stage is None:
        return None
    from . import usa_canonical_reconcile108 as reconcile
    if stage != {'format': reconcile.FORMAT}:
        raise ValueError('Unsupported canonical reconciliation stage identity')
    # Refuse old-head assumptions, source drift and any already accepted name.
    # A later crossregion7 stage must not contaminate the frozen 1964-C
    # predecessor identity of the published reconcile108 stage.
    predecessor_scope={k:v for k,v in manifest.items() if k!='overlay_crossregion7_stage'}
    reconcile.claimed_previous(predecessor_scope)
    return reconcile.fixture()


def claimed_functions(manifest):
    """All C claims, with explicit overlay functions outside main mapping."""
    if manifest.get('overlay_usa_opening_new2_stage') is not None:
        from . import usa_opening_new2_promotion as opening
        d=opening.validate_predecessor(manifest)
        predecessor={k:v for k,v in manifest.items() if k!='overlay_usa_opening_new2_stage'}
        return claimed_functions(predecessor)+[
            {k:f[k] for k in ('name','rom_offset','vma','size')} for f in d['functions']]
    if manifest.get('overlay_mini_selector_stage') is not None:
        from . import usa_mini_selector_promotion as mini_selector
        d=mini_selector.validate_predecessor(manifest)
        predecessor={k:v for k,v in manifest.items() if k!='overlay_mini_selector_stage'}
        return claimed_functions(predecessor)+[{k:f[k] for k in ('name','rom_offset','vma','size')} for f in d['functions']]
    if manifest.get('overlay_mini10_stage') is not None:
        from . import usa_mini10_promotion as mini10
        stage=mini10.validate_predecessor(manifest)
        predecessor={k:v for k,v in manifest.items() if k!='overlay_mini10_stage'}
        return claimed_functions(predecessor)+[{k:f[k] for k in ('name','rom_offset','vma','size')} for f in stage['functions']]
    functions = main_claimed_functions(manifest)
    stage = manifest.get('overlay_file43_stage')
    if stage is not None:
        functions.append(stage['function'])
    for stage in manifest_file12_stages(manifest):
        functions.extend(file12_registration.claims(stage))
    mode = file11_stage_mode(manifest)
    if mode in (143,144,152,179,183,184,187,269):
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
    cross_fixture=crossregion47_stage(manifest)
    if cross_fixture:
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in cross_fixture['functions'])
    native_fixture=native87_stage(manifest)
    if native_fixture:
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in native_fixture['functions'])
    high_fixture=highbyte26_stage(manifest)
    if high_fixture:
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in high_fixture['functions'])
    f27_fixture=file27_stage(manifest)
    if f27_fixture:
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in f27_fixture['functions'])
    wide_fixture=wide132_stage(manifest)
    if wide_fixture:
        functions.extend({'name':e['name'],'rom_offset':e['rom_offset'],
                          'vma':e['vma'],'size':e['size']}
                         for e in wide_fixture['functions'])
    w109=wide109_stage(manifest)
    if w109:
        from . import overlay_wide109 as wide109
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in wide109.functions(w109))
    resource_fixture=resource140_stage(manifest)
    if resource_fixture:
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in resource_fixture['functions'])
    gfx=graphics5_stage(manifest)
    if gfx:
        from . import overlay_graphics5 as graphics
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in graphics.functions(gfx))
    for fixture,modname in ((file18_53_stage(manifest),'overlay_file18_53'),
                            (callbacks10_stage(manifest),'overlay_callbacks10'),
                            (main19_stage(manifest),'overlay_main19'),
                            (tiny9_stage(manifest),'overlay_tiny9'),
                            (micro2_stage(manifest),'overlay_micro2'),
                            (micro15_stage(manifest),'overlay_micro15'),
                            (micro20_stage(manifest),'overlay_micro20'),
                            (menu2_stage(manifest),'overlay_menu2'),
                            (statecopy1_stage(manifest),'overlay_statecopy1'),
                            (archive22_stage(manifest),'overlay_archive22'),
                            (archive33_stage(manifest),'overlay_archive33'),
                            (archive61_stage(manifest),'overlay_archive61'),
                            (checkpoint500_stage(manifest),'overlay_checkpoint500'),
                            (rediscovery5_stage(manifest),'overlay_rediscovery5'),
                            (native49_stage(manifest),'overlay_native49'),
                            (native51_stage(manifest),'overlay_native51')):
        if fixture:
            from importlib import import_module
            mod=import_module('.'+modname,package='decomp')
            functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                              'vma':f['vma'],'size':f['size']}
                             for f in mod.functions(fixture))
    fixture = isolated233_stage(manifest)
    if fixture:
        functions.extend({'name': f['name'], 'rom_offset': f['rom_offset'],
                          'vma': f['vma'], 'size': f['size']}
                         for f in fixture['functions'])
    stage = reconcile108_stage(manifest)
    if stage:
        functions.extend({'name': f['name'], 'rom_offset': f['rom_offset'],
                          'vma': f['vma'], 'size': f['size']}
                         for f in stage['functions'])
    if manifest.get('overlay_crossregion7_stage') is not None:
        from . import usa_crossregion7 as cross7
        fixture=cross7.validate_predecessor(manifest)
        functions.extend({'name':f['name'],'rom_offset':f['rom_offset'],
                          'vma':f['vma'],'size':f['size']}
                         for f in fixture['functions'])
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
    """Validate a reviewed callback or contiguous registration group."""
    if file12_registration.is_group(stage):
        return file12_registration.validate_stage(stage)
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
        splat_yaml, reference_rom, tuple(fn['name'] for fn in file12_registration.claims(stage))
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
    """Restore the original tail alias across every pre-tail file_12 ASM slice.

    The canonical two-callback plan keeps the four references in the prefix.
    The 374-wrapper split moves them into a later intervening ASM island.
    Require the *same* four pinned reference occurrences in either case.
    """
    stages = _file12_stage_list(stage)
    layout = _file12_stages_layout(stages)
    checkout = Path(candidate_checkout)
    asm_paths = [checkout / f'asm/usa/{name}.s' for name in layout['assembly']]
    if not all(path.is_file() for path in asm_paths):
        raise ValueError('Missing generated file_12 assembly for tail alias correction')
    texts = [path.read_text(encoding='utf-8') for path in asm_paths]
    rom_offset, vma, alias_name, generated_name, word = overlay_file12.TEXT_END_ALIAS
    ref_counts = [text.count(generated_name) for text in texts[:-1]]
    if sum(ref_counts) != 4 or any(alias_name in text for text in texts):
        raise ValueError('Unexpected file_12 pre-tail references or pre-existing alias')
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
    tail = texts[-1]
    if tail.count(old_block) != 1 or tail.count(generated_name) != 3:
        raise ValueError('Unexpected file_12 suffix tail-alias block')
    staged = [text.replace(generated_name, alias_name) for text in texts[:-1]]
    staged.append(tail.replace(old_block, new_block))
    if (sum(text.count(alias_name) for text in staged[:-1]) != 4 or
            any(generated_name in text for text in staged) or
            staged[-1].count(alias_name) != 1):
        raise ValueError('file_12 tail-alias correction did not apply exactly')
    normalized_padding = None
    if any(file12_registration.is_group(item) for item in stages):
        # Splat invents a four-byte FUNC annotation for a pre-existing NOP
        # when the 374-wrapper run ends at 0x5CC7A8. The original full ELF
        # and assembly have only anonymous zero instructions here. Removing
        # the synthetic labels restores its 7,376 positive-sized FUNC entries.
        pad_candidates = [name for name in layout['assembly']
                          if name.startswith('file_12_gap_5CC7A8_')]
        if len(pad_candidates) != 1:
            raise ValueError('No unique registration-tail ASM gap')
        pad_name = pad_candidates[0]
        pad = f'asm/usa/{pad_name}.s'
        pad_path = checkout / pad
        if pad_path not in asm_paths:
            raise ValueError('Missing exact registration-tail padding slice')
        i = asm_paths.index(pad_path)
        synthetic = (
            'nonmatching func_802112D8_5CC7A8, 0x4\n\n'
            'glabel func_802112D8_5CC7A8\n'
            '    /* 5CC7A8 802112D8 00000000 */  nop\n'
            'endlabel func_802112D8_5CC7A8\n'
        )
        original_padding = '    /* 5CC7A8 802112D8 00000000 */  nop\n'
        if staged[i].count(synthetic) != 1:
            raise ValueError('Unreviewed registration-tail synthetic FUNC label')
        staged[i] = staged[i].replace(synthetic, original_padding)
        if 'func_802112D8_5CC7A8' in staged[i]:
            raise ValueError('Synthetic registration NOP ownership persisted')
        normalized_padding = {
            'rom_offset': '0x5CC7A8', 'vma': '0x802112D8',
            'bytes_preserved': 4, 'positive_sized_function_removed': True,
            'source': pad, 'source_sha256_after': digest(staged[i].encode(), 'sha256'),
        }
    for path, new_text in zip(asm_paths, staged):
        path.write_text(new_text, encoding='utf-8', newline='\n')
    return {
        'registration_tail_padding_normalized': normalized_padding,
        'rom_offset': f'0x{rom_offset:X}',
        'vma': f'0x{vma:08X}',
        'generated_function_name': generated_name,
        'restored_alias_name': alias_name,
        'instruction_word': word,
        'prefix_reference_rewrites': 4,
        'suffix_zero_size_alias_restored': True,
        'prefix_sha256_before': digest(texts[0].encode('utf-8'), 'sha256'),
        'prefix_sha256_after': digest(staged[0].encode('utf-8'), 'sha256'),
        'suffix_sha256_before': digest(texts[-1].encode('utf-8'), 'sha256'),
        'suffix_sha256_after': digest(staged[-1].encode('utf-8'), 'sha256'),
        'reference_rewrites_by_assembly_slice': dict(zip(layout['assembly'][:-1], ref_counts)),
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
    staged_names = {fn['name'] for item in stages
                    for fn in file12_registration.claims(item)}
    for item in stages:
        source_name = PurePosixPath(item['source']).name
        function = item['function']
        c_path = checkout / f'build/usa/src/{source_name}.o'
        if not c_path.is_file():
            raise ValueError('Missing compiled file_12 source object')
        c_original = c_path.read_bytes()
        if digest(c_original, 'sha256') != item['compiler_object_sha256']:
            raise ValueError('file_12 compiler object hash mismatch')
        if file12_registration.is_group(item):
            c_staged, pack_evidence = file12_registration.pack(c_original)
        else:
            expected_relocations = overlay_file12.FUNCTION_RELOCATIONS[function['name']]
            padding = (-function['size']) % 16
            if padding == 12:
                c_staged, pack_evidence = pack_file12_callback_text(
                    c_original, function['name'], function['size'], expected_relocations,
                    overlay_file12.FUNCTION_RELOCATION_SYMBOLS[function['name']],
                )
            else:
                c_staged, pack_evidence = pack_overlay_function_text(
                    c_original, function['name'], function['size'], padding,
                    expected_relocations,
                    overlay_file12.FUNCTION_RELOCATION_SYMBOLS[function['name']],
                    'file_12 callback', 'file12_callback',
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
    # Historical stages validate their frozen G2 claim counts against the
    # precise old manifest. Validate the additive isolated main-C stage separately
    # against every earlier accepted claim after all legacy guards pass.
    isolated_stage_value = manifest.pop('overlay_isolated233_stage', None)
    reconcile108_stage_value = manifest.pop('overlay_reconcile108_stage', None)
    crossregion7_stage_value = manifest.pop('overlay_crossregion7_stage', None)
    mini10_stage_value = manifest.pop('overlay_mini10_stage', None)
    selector_stage_value = manifest.pop('overlay_mini_selector_stage', None)
    opening_new2_stage_value = manifest.pop('overlay_usa_opening_new2_stage', None)
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
            if (file12_registration.is_group(stage) and
                    any(fn['name'] in seen or fn['name'] in assembly_seen
                        for fn in file12_registration.claims(stage))):
                raise ValueError('Registration wrapper overlaps already claimed function')
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
        if file11_mode in (143,144,152,179,183,184,187,269):
            file11_adapter(file11_mode).reviewed_plan({k:v for k,v in manifest.items() if k not in ('overlay_wide132_stage','overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage','overlay_native49_stage','overlay_native51_stage','overlay_isolated233_stage','overlay_reconcile108_stage')})
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
    # New multi-overlay original-C claims must remain disjoint from every
    # accepted production stage, not simply from main-code translation units.
    cross_fixture=crossregion47_stage(manifest)
    if cross_fixture:
        existing=main_claimed_functions(manifest)
        if file43_stage is not None:existing.append(file43_stage['function'])
        for row in manifest_file12_stages(manifest):existing.extend(file12_registration.claims(row))
        existing.extend(file11_adapter(file11_stage_mode(manifest)).entries()
                        if file11_stage_mode(manifest) in (143,144,152,179,183,184,187,269) else [])
        existing.extend(row['function'] for row in manifest_file13_stages(manifest))
        for row in cross_fixture['functions']:
            for earlier in existing:
                if (row['name']==earlier['name'] or
                    row['rom_offset']<earlier['rom_offset']+earlier['size'] and
                    earlier['rom_offset']<row['rom_offset']+row['size']):
                    raise ValueError('Cross-overlay candidate overlaps canonical source: '+row['name'])
        names=[x['name'] for x in cross_fixture['functions']]
        if len(set(names))!=len(names):raise ValueError('Duplicate cross-overlay source name')
    native_fixture=native87_stage(manifest)
    if native_fixture:
        existing=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_native87_stage'})
        all_old=[(e['name'],e['rom_offset'],e['size']) for e in existing]
        for row in native_fixture['functions']:
            for name,off,size in all_old:
                if row['name']==name or row['rom_offset']<off+size and off<row['rom_offset']+row['size']:
                    raise ValueError('Native87 original function overlaps accepted C: '+row['name'])
    high_fixture=highbyte26_stage(manifest)
    if high_fixture:
        previous=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_highbyte26_stage'})
        for row in high_fixture['functions']:
            if any(row['name']==e['name'] or
                   row['rom_offset']<e['rom_offset']+e['size'] and
                   e['rom_offset']<row['rom_offset']+row['size'] for e in previous):
                raise ValueError('Highbyte26 function overlaps accepted C: '+row['name'])
    f27_fixture=file27_stage(manifest)
    if f27_fixture:
        previous=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_file27_stage'})
        for row in f27_fixture['functions']:
            if any(row['name']==e['name'] or
                   row['rom_offset']<e['rom_offset']+e['size'] and
                   e['rom_offset']<row['rom_offset']+row['size'] for e in previous):
                raise ValueError('File27 function overlaps accepted C: '+row['name'])
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
    wide_fixture=wide132_stage(manifest)
    if wide_fixture:
        existing=claimed_functions({k:v for k,v in manifest.items() if k not in ('overlay_wide132_stage','overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage','overlay_native49_stage','overlay_native51_stage','overlay_isolated233_stage','overlay_reconcile108_stage')})
        existing_names={row['name'] for row in existing}
        existing_bounds=[(row['rom_offset'],row['rom_offset']+row['size']) for row in existing]
        for row in wide_fixture['functions']:
            off,end=row['rom_offset'],row['rom_offset']+row['size']
            if row['name'] in existing_names or any(off<last and first<end for first,last in existing_bounds):
                raise ValueError('Wide132 candidate already accepted/overlaps manifest: '+row['name'])
    w109=wide109_stage(manifest)
    if w109:
        from . import overlay_wide109 as wide109
        prior=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_wide109_stage'})
        seen_names={f['name'] for f in prior}
        intervals=[(f['rom_offset'],f['rom_offset']+f['size']) for f in prior]
        for f in wide109.functions(w109):
            off,end=f['rom_offset'],f['rom_offset']+f['size']
            if f['name'] in seen_names or any(off<e and s<end for s,e in intervals):
                raise ValueError('Wide109 overlaps previously accepted canonical C: '+f['name'])
    resources=resource140_stage(manifest)
    if resources:
        previous=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_resource140_stage'})
        names={f['name'] for f in previous}
        intervals=[(f['rom_offset'],f['rom_offset']+f['size']) for f in previous]
        for f in resources['functions']:
            off,end=f['rom_offset'],f['rom_offset']+f['size']
            if f['name'] in names or any(off<e and st<end for st,e in intervals):
                raise ValueError('Resource140 overlaps previously accepted C: '+f['name'])
    gfx=graphics5_stage(manifest)
    if gfx:
        from . import overlay_graphics5 as graphics
        previous=claimed_functions({k:v for k,v in manifest.items() if k!='overlay_graphics5_stage'})
        names={f['name'] for f in previous}
        intervals=[(f['rom_offset'],f['rom_offset']+f['size']) for f in previous]
        for f in graphics.functions(gfx):
            off,end=f['rom_offset'],f['rom_offset']+f['size']
            if f['name'] in names or any(off<e and st<end for st,e in intervals):
                raise ValueError('Graphics5 overlaps previously accepted C: '+f['name'])
    for key,loader,modname in (
        ('overlay_file18_53_stage',file18_53_stage,'overlay_file18_53'),
        ('overlay_callbacks10_stage',callbacks10_stage,'overlay_callbacks10'),
        ('overlay_main19_stage',main19_stage,'overlay_main19'),
        ('overlay_tiny9_stage',tiny9_stage,'overlay_tiny9'),
        ('overlay_micro2_stage',micro2_stage,'overlay_micro2'),
        ('overlay_micro15_stage',micro15_stage,'overlay_micro15'),
        ('overlay_micro20_stage',micro20_stage,'overlay_micro20'),
        ('overlay_menu2_stage',menu2_stage,'overlay_menu2'),
        ('overlay_statecopy1_stage',statecopy1_stage,'overlay_statecopy1'),
        ('overlay_archive22_stage',archive22_stage,'overlay_archive22'),
        ('overlay_archive33_stage',archive33_stage,'overlay_archive33'),
        ('overlay_checkpoint500_stage',checkpoint500_stage,'overlay_checkpoint500'),
        ('overlay_rediscovery5_stage',rediscovery5_stage,'overlay_rediscovery5')):
        fixture=loader(manifest)
        if fixture:
            from importlib import import_module
            native=import_module('.'+modname,package='decomp')
            previous=claimed_functions({k:v for k,v in manifest.items() if k not in (
                key, 'overlay_callbacks10_stage' if key=='overlay_file18_53_stage' else key, 'overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage')})
            names={f['name'] for f in previous}
            intervals=[(f['rom_offset'],f['rom_offset']+f['size']) for f in previous]
            for f in native.functions(fixture):
                off,end=f['rom_offset'],f['rom_offset']+f['size']
                if f['name'] in names or any(off<e and st<end for st,e in intervals):
                    raise ValueError('New original C overlaps accepted production: '+f['name'])
    fixture=native49_stage(manifest)
    if fixture:
        previous=claimed_functions({k:v for k,v in manifest.items() if k not in ('overlay_native49_stage',)+(('overlay_native51_stage',) if 'native49'=='native49' else ())})
        names={f['name'] for f in previous}
        spans=[(f['rom_offset'],f['rom_offset']+f['size']) for f in previous]
        for f in __import__('decomp.overlay_native49',fromlist=['functions']).functions(fixture):
            off,end=f['rom_offset'],f['rom_offset']+f['size']
            if f['name'] in names or any(off<e and start<end for start,e in spans):
                raise ValueError('New native49 overlaps accepted C '+f['name'])
    fixture=native51_stage(manifest)
    if fixture:
        previous=claimed_functions({k:v for k,v in manifest.items() if k not in ('overlay_native51_stage',)+(('overlay_native51_stage',) if 'native51'=='native49' else ())})
        names={f['name'] for f in previous}
        spans=[(f['rom_offset'],f['rom_offset']+f['size']) for f in previous]
        for f in __import__('decomp.overlay_native51',fromlist=['functions']).functions(fixture):
            off,end=f['rom_offset'],f['rom_offset']+f['size']
            if f['name'] in names or any(off<e and start<end for start,e in spans):
                raise ValueError('New native51 overlaps accepted C '+f['name'])
    if isolated_stage_value is not None:
        manifest['overlay_isolated233_stage'] = isolated_stage_value
    isolated_fixture = isolated233_stage(manifest)
    if isolated_fixture:
        # Enforce unique original-address ownership against every previously
        # accepted C function. A duplicate name, overlapping byte span or
        # original offset is rejected before staging any source.
        previous = claimed_functions({k:v for k,v in manifest.items()
                                      if k != 'overlay_isolated233_stage'})
        names = {f['name'] for f in previous}
        spans = sorted((f['rom_offset'], f['rom_offset'] + f['size']) for f in previous)
        for f in isolated_fixture['functions']:
            start, end = f['rom_offset'], f['rom_offset']+f['size']
            if f['name'] in names or any(start < hi and lo < end for lo,hi in spans):
                raise ValueError('Isolated233 duplicates accepted original C: '+f['name'])
    if reconcile108_stage_value is not None:
        manifest['overlay_reconcile108_stage'] = reconcile108_stage_value
        reconcile108_stage(manifest)
    if crossregion7_stage_value is not None:
        manifest['overlay_crossregion7_stage']=crossregion7_stage_value
        from . import usa_crossregion7 as cross7
        cross7.validate_predecessor(manifest)
    if mini10_stage_value is not None:
        manifest['overlay_mini10_stage']=mini10_stage_value
        from . import usa_mini10_promotion as mini10
        mini10.validate_predecessor(manifest)
    if selector_stage_value is not None:
        manifest['overlay_mini_selector_stage']=selector_stage_value
        from . import usa_mini_selector_promotion as mini_selector
        mini_selector.validate_predecessor(manifest)
    if opening_new2_stage_value is not None:
        manifest['overlay_usa_opening_new2_stage']=opening_new2_stage_value
        from . import usa_opening_new2_promotion as opening
        opening.validate_predecessor(manifest)
    return manifest


def apply_units(checkout,manifest,source_dir=ROOT,reference_rom=None):
    """Apply only to a newly cloned candidate; fail before writes on collisions."""
    # The final crossregion7 step replaces active ASM *after* the complete
    # 2072-C predecessor is built; it must not alter earlier stage identities.
    if "overlay_crossregion7_stage" in manifest:
        manifest={k:v for k,v in manifest.items() if k!="overlay_crossregion7_stage"}
    checkout=Path(checkout);source_dir=Path(source_dir)
    config=checkout/'config/usa/splat.yaml'
    text=config.read_text(encoding='utf-8')
    file11_copies=[]
    file11_inline=[]
    file11_mode=file11_stage_mode(manifest)
    if file11_mode is not None:
        if reference_rom is None:
            raise ValueError('file_11 staging requires authenticated USA decompressed ROM')
        if file11_mode in (143,144,152,179,183,184,187,269):
            adapter=file11_adapter(file11_mode)
            plan=adapter.reviewed_plan({k:v for k,v in manifest.items() if k not in ('overlay_wide132_stage','overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage','overlay_native49_stage','overlay_native51_stage','overlay_isolated233_stage','overlay_reconcile108_stage')},reference_rom)
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


def _verify_expanded_cross_overlay_map(block, expected_inputs, cross_plan, region,
                                       overlay_rom_start, overlay_vma_start, native_plan=None):
    """Preserve every accepted original input extent when 47 C splits refine ASM.

    Each replaced original ASM input must be covered exactly once by adjacent,
    ordered original-address C and assembly children; no holes/overlap are
    accepted, and the linked map must match all original guest addresses.
    """
    groups={}
    if cross_plan:
        for parent in cross_plan['parents']:
            if parent['section']==region:
                path='build/usa/asm/usa/'+parent['parent']+'.s.o'
                if path in groups:raise ValueError('Duplicate cross-overlay parent ownership')
                lo,hi=parent['start'],parent['end']
                children=[(item['object'],item['start'],item['end'])
                          for item in cross_plan['assembly']
                          if item['section']==region and lo<=item['start']<hi]
                children.extend(('build/usa/src/'+item['name']+'.c.o',
                                 item['rom_offset'],item['rom_offset']+item['size'])
                                for item in cross_plan['functions']
                                if item['section']==region and lo<=item['rom_offset']<hi)
                children.sort(key=lambda item:item[1])
                if (not children or children[0][1]!=lo or children[-1][2]!=hi or
                        any(a[2]!=b[1] for a,b in zip(children,children[1:]))):
                    raise ValueError('Cross-overlay split loses original ASM interval '+path)
                groups[path]=(lo,hi,children)
    expanded=[]
    for original,lo,hi in expected_inputs:
        if original in groups:
            a,b,kids=groups.pop(original)
            if (a,b)!=(lo,hi):raise ValueError('Cross-overlay source changed accepted ASM extent '+original)
            expanded.extend(kids)
        else:expanded.append((original,lo,hi))
    if groups:
        raise ValueError('Unaccounted original ASM parents in cross-overlay stage: '+repr(sorted(groups)))
    # A later original-address split can refine both legacy file_13 ASM
    # inputs and the 47-C cross-overlay split children. Preserve exact
    # coverage and object order rather than exempting them from map checks.
    native_groups={}
    if native_plan:
        for parent in native_plan['parents']:
            path='build/usa/asm/usa/'+parent['source']+'.s.o'
            native_groups[path]=(parent['start'],parent['end'],parent['children'])
        refined=[]
        for object_name,lo,hi in expanded:
            if object_name in native_groups:
                a,b,kids=native_groups.pop(object_name)
                if (a,b)!=(lo,hi) or not kids or kids[0][1]!=lo or kids[-1][2]!=hi or any(
                        left[2]!=right[1] for left,right in zip(kids,kids[1:])):
                    raise ValueError('Native87 changes accepted ASM extent '+object_name)
                refined.extend(kids)
            else:
                refined.append((object_name,lo,hi))
        expanded=refined
    positions=[]
    for object_name,lo,hi in expanded:
        namepat=re.compile(r'(?m)^\s*'+re.escape(object_name+'(.text)')+r'\s*$')
        hit=list(namepat.finditer(block))
        if len(hit)!=1:raise ValueError('Linked object not placed exactly once: '+object_name)
        positions.append(hit[0].start())
        extpat=re.compile(r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+'+re.escape(object_name)+r'\s*$')
        e=list(extpat.finditer(block))
        vma=overlay_vma_start+(lo-overlay_rom_start)
        if len(e)!=1 or (int(e[0].group(1),16),int(e[0].group(2),16))!=(vma,hi-lo):
            raise ValueError('Changed original object guest VMA/extent: '+object_name)
    if positions!=sorted(positions):
        raise ValueError('Cross-overlay stage changed original C/ASM object order')
    if cross_plan and len(expanded)<=len(expected_inputs):
        raise ValueError('No cross-overlay split linked in region '+region)
    return {'inputs_original':len(expected_inputs),'inputs_after_split':len(expanded),
            'complete_original_extent_cover':True,'original_address_map':True}


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


def verify_file12_ownership(candidate_checkout, stage, cross_plan=None, native_plan=None):
    """Prove every staged callback and assembly gap in the .file_12 map."""
    stages = _file12_stage_list(stage)
    layout = _file12_stages_layout(stages)
    checkout = Path(candidate_checkout)
    staged_names = {fn['name'] for item in stages
                    for fn in file12_registration.claims(item)}
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
        if file12_registration.is_group(item):
            group_evidence = file12_registration.validate_object(
                c_object.read_bytes(), staged=True)
        else:
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
            'function_count': file12_registration.COUNT if file12_registration.is_group(item) else 1,
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
    expected_extents=[(assembly_objects[0],overlay_file12.ROM_START,stages[0]['function']['rom_offset'])]
    next_gap=1
    for index,(item,c_object_name) in enumerate(zip(stages,c_object_names)):
        fn=item['function'];lo=fn['rom_offset'];hi=lo+fn['size']
        expected_extents.append((c_object_name,lo,hi))
        nxt=(stages[index+1]['function']['rom_offset'] if index+1<len(stages)
             else overlay_file12.ROM_TEXT_END)
        if nxt>hi:
            expected_extents.append((assembly_objects[next_gap],hi,nxt));next_gap+=1
        for claim in file12_registration.claims(item):
            symbol_lines = re.findall(
                r'(?m)^\s*0x([0-9a-fA-F]+)\s+'+re.escape(claim['name'])+r'\s*$',block)
            if [int(v,16) for v in symbol_lines]!=[claim['vma']]:
                raise ValueError('file_12 matching-C symbol no longer at its original VMA')
    if [v[0] for v in expected_extents]!=expected_inputs:
        raise ValueError('file_12 original object plan changed unexpectedly')
    map_proof=_verify_expanded_cross_overlay_map(
        block,expected_extents,cross_plan,'file_12',overlay_file12.ROM_START,overlay_file12.VMA_START,native_plan)
    if re.search(r'(?m)^\s*build/usa/asm/usa/5C8770\.s\.o\(\.text\)\s*$', block):
        raise ValueError('Link map retains unsplit original file_12 ASM')
    bss_match = re.search(
        r'(?m)^\.file_12_bss\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)', mapping
    )
    if (bss_match is None or int(bss_match.group(1), 16) !=
            overlay_file12.VMA_START + section_size or int(bss_match.group(2), 16) != 0):
        raise ValueError('Link map .file_12_bss boundary differs from pinned overlay')
    result = {
        'map_expanded_ownership':map_proof,
        'callbacks': callback_proofs,
        'assembly_objects': assembly_objects,
        'file_12_vma': f'0x{section_vma:08X}',
        'file_12_size': section_size,
    }
    if len(callback_proofs) == 1:
        result.update(callback_proofs[0])
    return result


def verify_file12_stage_build(baseline_checkout, candidate_checkout, stage, reference_rom, cross_plan=None, native_plan=None):
    """Verify the staged split, object ownership and linked ELF provenance."""
    stages = _file12_stage_list(stage)
    candidate_checkout = Path(candidate_checkout)
    ownership = verify_file12_ownership(candidate_checkout, stages, cross_plan, native_plan)
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
            fn['name'] + '.NON_MATCHING' for item in stages
            for fn in file12_registration.claims(item)
    }
           for symbol in candidate_symbols.symbols):
        raise ValueError('Staged file_12 function retains a NON_MATCHING marker')
    linked = overlay_file12.validate_linked_elf_provenance(
        original_splat, reference_rom, baseline_elf, candidate_elf,
        tuple(fn['name'] for item in stages
              for fn in file12_registration.claims(item))
    )['linked_elf_provenance']
    return {'ownership': ownership, 'linked_elf_provenance': linked}


def append_file12_function_comparison(comparison, stage, linked_provenance):
    """Count each genuine original function, never the synthetic C group span."""
    stages = _file12_stage_list(stage)
    claims = tuple(fn for item in stages for fn in file12_registration.claims(item))
    proof = linked_provenance['functions']
    proof_by_name = {row.get('name'): row for row in proof}
    if (len(proof_by_name) != len(proof) or
            set(proof_by_name) != {fn['name'] for fn in claims}):
        raise ValueError('Linked file_12 proof does not cover all staged functions')
    for function in claims:
        row = proof_by_name[function['name']]
        if (row.get('section') != '.file_12' or
                row.get('vma') != f'0x{function["vma"]:08X}' or
                row.get('rom_offset') != f'0x{function["rom_offset"]:X}' or
                row.get('bytes') != function['size'] or
                row.get('candidate_sha256') != row.get('original_sha256') or
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
                              stage_or_stages, reference_rom, cross_plan=None, native_plan=None):
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
    expected_extents=[(name,obj['start'],obj['end']) for name,obj in expected_objects]
    map_proof=_verify_expanded_cross_overlay_map(
        block,expected_extents,cross_plan,'file_13',overlay_file13.ROM_START,overlay_file13.VMA_START,native_plan)
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
        'cross_overlay_map_ownership':map_proof,
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
    opening_new2_stage_value=manifest.pop('overlay_usa_opening_new2_stage',None)
    selector_stage_value=manifest.pop('overlay_mini_selector_stage',None)
    mini10_stage_value=manifest.pop('overlay_mini10_stage',None)
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
    if file11_stage_mode(manifest) in (50,143,144,152,179,183,184,187,269):
        report['overlay_file11_nop_aliases']=overlay_file11_noops.patch_synthetic_nop_aliases(candidate)
        if file11_stage_mode(manifest) in (179,183,184,187,269):
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
        if file11_mode in (143,144,152,179,183,184,187,269):
            file11_objects=file11_adapter(file11_mode).object_targets()
        elif file11_mode == 50:
            file11_objects=overlay_file11_noops.object_targets()
        else:
            file11_objects=overlay_file11.object_targets()
        logged('candidate-file11-objects',['make','-j'+str(args.jobs),'UV='+uv,
            *file11_objects],candidate)
        if file11_mode in (143,144,152,179,183,184,187,269):
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
    cross_fixture=crossregion47_stage(manifest)
    cross_plan=None
    cross_packed=None
    if cross_fixture:
        from . import overlay_crossregion47 as cross
        # The clean Splat output has ASM sources but only selected 732-stage
        # objects have been compiled. Establish original parent-object
        # provenance before splitting any new cross-overlay chunks.
        parents=cross._subsegments((candidate/'config/usa/splat.yaml').read_text())
        original_parents=set()
        for item in cross_fixture['functions']:
            eligible=[name for name,(region,start,end) in parents.items()
                      if region==item['section'] and start<=item['rom_offset']
                      and item['rom_offset']+item['size']<=end]
            if len(eligible)!=1:
                raise ValueError('Ambiguous cross-overlay original ASM parent: '+item['name'])
            original_parents.add(eligible[0])
        logged('candidate-crossregion47-original-parents',
            ['make','-j'+str(args.jobs),'UV='+uv,
             *['build/usa/asm/usa/'+name+'.s.o' for name in sorted(original_parents)]],candidate)
        cross_plan=cross.stage_linker(candidate,expected,cross_fixture,
                      source_dir/'research/jp_recomp_to_c/src')
        report['overlay_crossregion47_source_plan']={
            'function_count':len(cross_plan['functions']),
            'original_code_bytes':sum(x['size'] for x in cross_plan['functions']),
            'split_asm_objects':len(cross_plan['assembly']),
            'parent_chunks':len(cross_plan['parents'])}
        logged('candidate-crossregion47-objects',['make','-j'+str(args.jobs),'UV='+uv,
            *cross.object_targets(cross_plan)],candidate)
        cross_packed=cross.pack_objects(candidate,expected,cross_plan)
        report['overlay_crossregion47_object_layout']=cross_packed
    native_fixture=native87_stage(manifest)
    native_plan=None
    if native_fixture:
        from . import overlay_native87 as native
        native_owners=native.find_owners(candidate,native_fixture)
        logged('candidate-native87-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*native.parent_targets(native_owners)],candidate)
        native_plan=native.stage_linker(candidate,expected,native_fixture,native_owners,
                                        source_dir/'research/usa_main_overlay_87_20261118/sources')
        report['overlay_native87_source_plan']={
            'functions':len(native_plan['functions']),'instruction_bytes':sum(f['size'] for f in native_plan['functions']),
            'retained_asm_fragments':len(native_plan['assembly'])}
        logged('candidate-native87-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*native.object_targets(native_plan)],candidate)
        report['overlay_native87_object_layout']=native.pack_objects(candidate,expected,native_plan)
    high_fixture=highbyte26_stage(manifest)
    high_plan=None
    if high_fixture:
        from . import overlay_highbyte26 as high
        owners=high.find_owners(candidate,high_fixture)
        logged('candidate-highbyte26-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*high.parent_targets(owners)],candidate)
        high_plan=high.stage_linker(candidate,expected,high_fixture,owners,
                                   source_dir/'research/highbyte_file26_20261118/sources')
        report['overlay_highbyte26_source_plan']={
            'functions':len(high_plan['functions']),
            'instruction_bytes':sum(f['size'] for f in high_plan['functions']),
            'retained_asm_fragments':len(high_plan['assembly'])}
        logged('candidate-highbyte26-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*high.object_targets(high_plan)],candidate)
        report['overlay_highbyte26_object_layout']=high.pack_objects(candidate,expected,high_plan)
    file27_fixture=file27_stage(manifest)
    file27_plan=None
    if file27_fixture:
        from . import overlay_file27 as file27
        owners=file27.find_owners(candidate,file27_fixture)
        logged('candidate-file27-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*file27.parent_targets(owners)],candidate)
        file27_plan=file27.stage_linker(candidate,expected,file27_fixture,owners,
                                       source_dir/'research/file27_promotion_20261118/sources')
        report['overlay_file27_source_plan']={
            'functions':len(file27_plan['functions']),
            'instruction_bytes':sum(f['size'] for f in file27_plan['functions']),
            'retained_asm_fragments':len(file27_plan['assembly'])}
        logged('candidate-file27-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*file27.object_targets(file27_plan)],candidate)
        report['overlay_file27_object_layout']=file27.pack_objects(candidate,expected,file27_plan)
    wide_fixture=wide132_stage(manifest)
    wide109_fixture=wide109_stage(manifest)
    wide_plan=None
    if manifest.get('vm_assignment_table_layout'):
        logged('candidate-vm-object'  ,['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/script_vm.c.o','build/usa/asm/usa/data/main_continued.rodata.s.o'],candidate)
        report['object_layout']=pack_object_file(candidate/'build/usa/src/script_vm.c.o')
    if manifest.get('heap_noop_text_layout'):
        logged('candidate-heap-noop-object',['make','-j'+str(args.jobs),'UV='+uv,
            'build/usa/src/heap_noop.c.o','build/usa/asm/usa/3698C.s.o'],candidate)
        report['heap_noop_layout']=pack_heap_noop_file(candidate/'build/usa/src/heap_noop.c.o')
    logged('candidate-build',['make','-j'+str(args.jobs),'UV='+uv],candidate)
    symbols=parse_symbols(capture(['mips-linux-gnu-nm','-n','build/usa/mnsg.elf'],candidate))
    result=compare_images(expected,(candidate/'build/usa/mnsg.z64').read_bytes(),
                          {k:v for k,v in manifest.items() if k not in ('overlay_wide109_stage','overlay_resource140_stage','overlay_graphics5_stage','overlay_file18_53_stage','overlay_callbacks10_stage','overlay_main19_stage','overlay_tiny9_stage','overlay_micro2_stage','overlay_micro15_stage','overlay_micro20_stage','overlay_menu2_stage','overlay_statecopy1_stage','overlay_archive22_stage','overlay_archive33_stage','overlay_archive61_stage','overlay_checkpoint500_stage','overlay_rediscovery5_stage','overlay_native49_stage','overlay_native51_stage','overlay_isolated233_stage','overlay_reconcile108_stage')},symbols)
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
    if file11_mode in (143,144,152,179,183,184,187,269):
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
    if cross_fixture:
        for entry in cross_fixture['functions']:
            key='research/jp_recomp_to_c/src/'+entry['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(entry['name']+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
    if native_fixture:
        for entry in native_fixture['functions']:
            key='research/usa_main_overlay_87_20261118/sources/'+entry['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(entry['name']+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
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
            baseline,candidate,file12_stages,expected,cross_plan,native_plan
        )
        append_file12_function_comparison(
            result,file12_stages,file12_report['linked_elf_provenance']
        )
        report['overlay_file12_stages']=file12_report
        report['comparison']=result
    if file11_mode is not None:
        if file11_mode in (143,144,152,179,183,184,187,269):
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
            baseline,candidate,file13_stages,expected,cross_plan,native_plan
        )
        append_file13_function_comparison(
            result,file13_stages,
            report['overlay_file13_stages']['linked_elf_provenance']
        )
        report['comparison']=result
    if cross_fixture:
        from . import overlay_crossregion47 as cross
        # Require all seven original relocation multisets, 7,376 symbol
        # identities and *only* the two already-published 732-C annotation
        # differences. The full ROM and every code byte must be exact.
        original_syms=cross._funcs(baseline/'build/usa/mnsg.elf')
        candidate_syms=cross._funcs(candidate/'build/usa/mnsg.elf')
        expected_differences=(
            ('func_8000D3B8_DFB8',0x8000D3B8,64,72),
            ('func_8003F6E8_402E8',0x8003F6E8,48,56))
        expected_removed=Counter((n,v,s) for n,v,s,_ in expected_differences)
        expected_added=Counter((n,v,s) for n,v,_,s in expected_differences)
        if (sum(original_syms.values())!=7376 or sum(candidate_syms.values())!=7376
                or original_syms-candidate_syms!=expected_removed
                or candidate_syms-original_syms!=expected_added):
            raise ValueError('Unexpected original ELF function identity change in cross-region promotion')
        original_rel=cross._relocations(baseline/'build/usa/mnsg.elf')
        candidate_rel=cross._relocations(candidate/'build/usa/mnsg.elf')
        for region,count in cross.EXACT_COUNTS.items():
            if (len(original_rel.get(region,[]))!=count or
                    len(candidate_rel.get(region,[]))!=count or
                    Counter(original_rel[region])!=Counter(candidate_rel[region])):
                raise ValueError('Cross-overlay relocation drift: '+region)
        linked_image=(candidate/'build/usa/mnsg.z64').read_bytes()
        for entry in cross_fixture['functions']:
            name,off,size,vma=entry['name'],entry['rom_offset'],entry['size'],entry['vma']
            if (symbols.get(name)!=vma or name+'.NON_MATCHING' in symbols or
                    expected[off:off+size]!=linked_image[off:off+size] or
                    name not in mapping or 'build/usa/src/'+name+'.c.o' not in mapping):
                raise ValueError('Cross-overlay original-address ownership failed: '+name)
            result['functions'].append({
                'name':name,'size':size,'guest_address':f'0x{vma:08X}',
                'rom_offset':f'0x{off:X}','matched':True,
                'expected_sha256':entry['original_code_sha256'],
                'candidate_sha256':entry['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=size
        report['overlay_crossregion47_stage']={
            'status':'PASS','format':cross.STAGE_FORMAT,
            'original_address_matching_c':47,
            'original_instruction_bytes':2220,
            'original_positive_sized_elf_entries':7376,
            'historical_elf_size_annotations':[
                {'name':n,'vma':f'0x{v:08X}','original_size':a,'candidate_size':b}
                for n,v,a,b in expected_differences],
            'exact_semantic_relocations':cross.EXACT_COUNTS,
            'original_full_rom_sha1':cross.USA_SHA1,
            'complete_rom_bytes_equal':33554432,
            'splat_split_asm_objects':len(cross_plan['assembly'])}
    if native_fixture:
        from . import overlay_native87 as native
        native_proof=native.verify_link(baseline,candidate,expected,native_plan,native_fixture)
        for entry in native_fixture['functions']:
            name,off,size,vma=entry['name'],entry['rom_offset'],entry['size'],entry['vma']
            result['functions'].append({
                'name':name,'size':size,'guest_address':f'0x{vma:08X}',
                'rom_offset':f'0x{off:X}','matched':True,
                'expected_sha256':entry['original_code_sha256'],
                'candidate_sha256':entry['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=size
        report['overlay_native87_stage']=native_proof
    if high_fixture:
        from . import overlay_highbyte26 as high
        proof=high.verify_link(baseline,candidate,expected,high_plan,high_fixture)
        for entry in high_fixture['functions']:
            name,off,size,vma=entry['name'],entry['rom_offset'],entry['size'],entry['vma']
            result['functions'].append({
                'name':name,'size':size,'guest_address':f'0x{vma:08X}',
                'rom_offset':f'0x{off:X}','matched':True,
                'expected_sha256':entry['original_code_sha256'],
                'candidate_sha256':entry['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=size
        report['overlay_highbyte26_stage']=proof
    if file27_fixture:
        from . import overlay_file27 as file27
        proof=file27.verify_link(baseline,candidate,expected,file27_plan,file27_fixture)
        for entry in file27_fixture['functions']:
            name,off,size,vma=entry['name'],entry['rom_offset'],entry['size'],entry['vma']
            result['functions'].append({
                'name':name,'size':size,'guest_address':f'0x{vma:08X}',
                'rom_offset':f'0x{off:X}','matched':True,
                'expected_sha256':entry['original_code_sha256'],
                'candidate_sha256':entry['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=size
        report['overlay_file27_stage']=proof
    if wide_fixture:
        from . import overlay_wide132 as wide
        source_cache=wide.prepare_sources(candidate,expected,wide_fixture,source_dir)
        wide_owners=wide.find_owners(candidate,wide_fixture)
        logged('candidate-wide132-original-parents',
            ['make','-j'+str(args.jobs),'UV='+uv,*wide.parent_targets(wide_owners)],candidate)
        wide_plan=wide.stage_linker(candidate,expected,wide_fixture,wide_owners,source_cache)
        report['overlay_wide132_source_plan']={
            'functions':len(wide_plan['functions']),
            'instruction_bytes':sum(e['size'] for e in wide_plan['functions']),
            'retained_asm_fragments':len(wide_plan['assembly'])}
        logged('candidate-wide132-objects',
            ['make','-j'+str(args.jobs),'UV='+uv,*wide.object_targets(wide_plan)],candidate)
        report['overlay_wide132_object_layout']=wide.pack_objects(candidate,expected,wide_plan)
        if not result['full_rom_match'] or result['matched_functions']!=987:
            raise ValueError('Historical accepted 987-C gate must pass before final wide132 stage')
        # Force one real final link with all 987 previously validated units and
        # all 132 new original-address C objects simultaneously.
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-wide132-combined-final-build',
            ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        for entry in wide_fixture['functions']:
            key='research/usa_wide132_promotion_20261118/sources/'+entry['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(entry['name']+'.c')).read_bytes().replace(b'\r\n',b'\n'),'sha256')
        report['wide132_order']='prior 987 original-ROM + all historical validators PASS, then 132 additive C final build/ROM/ELF/relocation proof'
    if wide_fixture:
        from . import overlay_wide132 as wide
        proof=wide.verify_link(baseline,candidate,expected,wide_plan,wide_fixture)
        for entry in wide_fixture['functions']:
            result['functions'].append({
                'name':entry['name'],'size':entry['size'],
                'guest_address':f'0x{entry["vma"]:08X}',
                'rom_offset':f'0x{entry["rom_offset"]:X}','matched':True,
                'expected_sha256':entry['original_code_sha256'],
                'candidate_sha256':entry['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=entry['size']
        report['overlay_wide132_stage']=proof
    if wide109_fixture:
        from . import overlay_wide109 as wide109
        if not result['full_rom_match'] or result['matched_functions']!=1119:
            raise ValueError('Authenticated 1119-function canonical gate must pass before wide109 staging')
        wide109.validate_sources(expected,wide109_fixture,source_dir/'research/usa_wide109_promotion_20261118/sources')
        # Pin the successfully verified 1119-C ELF for semantic relocation and
        # original-symbol comparisons against the additive 109-C link.
        accepted_elf=work/'accepted1119.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',accepted_elf)
        owners=wide109.find_owners(candidate,wide109_fixture)
        logged('candidate-wide109-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*wide109.parent_targets(owners)],candidate)
        plan=wide109.stage_linker(candidate,expected,wide109_fixture,owners,
               source_dir/'research/usa_wide109_promotion_20261118/sources')
        report['overlay_wide109_source_plan']={
            'functions':len(plan['functions']),'C_units':len(plan['units']),
            'instruction_bytes':sum(x['size'] for x in plan['functions']),
            'retained_asm_fragments':len(plan['assembly'])}
        logged('candidate-wide109-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*wide109.object_targets(plan)],candidate)
        report['overlay_wide109_object_layout']=wide109.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-wide109-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=wide109.verify_link(baseline,accepted_elf,candidate,expected,plan,wide109_fixture)
        for u in wide109_fixture['units']:
            key='research/usa_wide109_promotion_20261118/sources/'+u['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(u['name']+'.c')).read_bytes(),'sha256')
            for f in u['functions']:
                result['functions'].append({
                    'name':f['name'],'size':f['size'],
                    'guest_address':f'0x{f["vma"]:08X}',
                    'rom_offset':f'0x{f["rom_offset"]:X}',
                    'matched':True,
                    'expected_sha256':f['original_code_sha256'],
                    'candidate_sha256':f['original_code_sha256']})
                result['claimed_functions']+=1
                result['matched_functions']+=1
                result['matched_function_bytes']+=f['size']
        report['overlay_wide109_stage']=proof
    resource_fixture=resource140_stage(manifest)
    if resource_fixture:
        from . import overlay_resource140 as research
        if not result['full_rom_match'] or result['matched_functions']!=1225:
            raise ValueError('Authenticated 1225-function canonical gate must pass before resource140 staging')
        src=source_dir/'research/pending_resource140_20261118/sources'
        research.validate_sources(expected,resource_fixture,src)
        owners=research.find_owners(candidate,resource_fixture)
        logged('candidate-resource140-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*research.parent_targets(owners)],candidate)
        plan=research.stage_linker(candidate,expected,resource_fixture,owners,src)
        report['resource140_source_plan']={'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'retained_asm_fragments':len(plan['assembly'])}
        logged('candidate-resource140-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*research.object_targets(plan)],candidate)
        report['resource140_object_layout']=research.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-resource140-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=research.verify_link(baseline,candidate,expected,plan,resource_fixture)
        for f in resource_fixture['functions']:
            key='research/pending_resource140_20261118/sources/'+f['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(f['name']+'.c')).read_bytes(),'sha256')
            result['functions'].append({'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True, 'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_resource140_stage']=proof
    graphics_fixture=graphics5_stage(manifest)
    if graphics_fixture:
        from . import overlay_graphics5 as graphics
        if not result['full_rom_match'] or result['matched_functions']!=1365:
            raise ValueError('Authenticated 1365-function production gate must pass before graphics5')
        src=source_dir/'research/pending_graphics5_20261118/sources'
        graphics.validate_sources(expected,graphics_fixture,src)
        accepted_elf=work/'accepted1365.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',accepted_elf)
        owners=graphics.find_owners(candidate,graphics_fixture)
        logged('candidate-graphics5-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*graphics.parent_targets(owners)],candidate)
        plan=graphics.stage_linker(candidate,expected,graphics_fixture,owners,src)
        report['graphics5_source_plan']={'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'C_units':len(plan['units']),'retained_asm_fragments':len(plan['assembly'])}
        logged('candidate-graphics5-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*graphics.object_targets(plan)],candidate)
        report['graphics5_object_layout']=graphics.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-graphics5-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=graphics.verify_link(baseline,accepted_elf,candidate,expected,plan,graphics_fixture)
        for unit in graphics_fixture['units']:
            key='research/pending_graphics5_20261118/sources/'+unit['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(unit['name']+'.c')).read_bytes(),'sha256')
            for f in unit['functions']:
                result['functions'].append({'name':f['name'],'size':f['size'],
                    'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                    'matched':True, 'expected_sha256':f['original_code_sha256'],
                    'candidate_sha256':f['original_code_sha256']})
                result['claimed_functions']+=1
                result['matched_functions']+=1
                result['matched_function_bytes']+=f['size']
        report['overlay_graphics5_stage']=proof
    for fixture, native, stage_key, count, srcpath in (
            (file18_53_stage(manifest),
             __import__('decomp.overlay_file18_53',fromlist=['x']),
             'overlay_file18_53_stage',1370,'research/pending_file18_53_20261118/sources'),
            (callbacks10_stage(manifest),
             __import__('decomp.overlay_callbacks10',fromlist=['x']),
             'overlay_callbacks10_stage',1423,'research/pending_callbacks10_20261118/sources'),
            (main19_stage(manifest),
             __import__('decomp.overlay_main19',fromlist=['x']),
             'overlay_main19_stage',1433,'research/pending_main19_20261118/sources'),
            (tiny9_stage(manifest),
             __import__('decomp.overlay_tiny9',fromlist=['x']),
             'overlay_tiny9_stage',1452,'research/pending_tiny9_20261119/sources'),
            (micro2_stage(manifest),
             __import__('decomp.overlay_micro2',fromlist=['x']),
             'overlay_micro2_stage',1461,'research/pending_micro2_20261119/sources'),
            (micro15_stage(manifest),
             __import__('decomp.overlay_micro15',fromlist=['x']),
             'overlay_micro15_stage',1463,'research/pending_micro15_20261119/sources'),
            (micro20_stage(manifest),
             __import__('decomp.overlay_micro20',fromlist=['x']),
             'overlay_micro20_stage',1478,'research/pending_micro20_20261119/sources'),
            (menu2_stage(manifest),
             __import__('decomp.overlay_menu2',fromlist=['x']),
             'overlay_menu2_stage',1498,'research/pending_menu2_20261119/sources'),
            (statecopy1_stage(manifest),
             __import__('decomp.overlay_statecopy1',fromlist=['x']),
             'overlay_statecopy1_stage',1500,'research/pending_statecopy1_20261119/sources'),
            (archive22_stage(manifest),
             __import__('decomp.overlay_archive22',fromlist=['x']),
             'overlay_archive22_stage',1501,'research/pending_archive22_20261119/sources'),
            (archive33_stage(manifest),
             __import__('decomp.overlay_archive33',fromlist=['x']),
             'overlay_archive33_stage',1523,'research/pending_archive33_20261120/sources'),
            (archive61_stage(manifest),
             __import__('decomp.overlay_archive61',fromlist=['x']),
             'overlay_archive61_stage',1556,'research/pending_archive61_20261120/sources'),
            (checkpoint500_stage(manifest),
             __import__('decomp.overlay_checkpoint500',fromlist=['x']),
             'overlay_checkpoint500_stage',1617,'research/pending_checkpoint500_20261120/sources'),
            (rediscovery5_stage(manifest),
             __import__('decomp.overlay_rediscovery5',fromlist=['x']),
             'overlay_rediscovery5_stage',1618,'research/pending_rediscovery5_20261120/sources')):
        if fixture is None:continue
        if not result['full_rom_match'] or result['matched_functions']!=count:
            raise ValueError('Authenticated '+str(count)+'-function combined gate required for '+stage_key)
        src=source_dir/srcpath
        native.validate_sources(expected,fixture,src)
        accepted_elf=work/('accepted'+str(count)+'.elf')
        shutil.copyfile(candidate/'build/usa/mnsg.elf',accepted_elf)
        owners=native.find_owners(candidate,fixture)
        label='candidate-'+stage_key.removeprefix('overlay_')
        logged(label+'-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*native.parent_targets(owners)],candidate)
        plan=native.stage_linker(candidate,expected,fixture,owners,src)
        report[stage_key+'_source_plan']={'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'C_units':len(plan['units']),'retained_asm_fragments':len(plan['assembly'])}
        logged(label+'-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*native.object_targets(plan)],candidate)
        report[stage_key+'_object_layout']=native.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged(label+'-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=native.verify_link(baseline,accepted_elf,candidate,expected,plan,fixture)
        for unit in fixture['units']:
            key=srcpath+'/'+unit['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(unit['name']+'.c')).read_bytes(),'sha256')
            for f in unit['functions']:
                result['functions'].append({'name':f['name'],'size':f['size'],
                    'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                    'matched':True, 'expected_sha256':f['original_code_sha256'],
                    'candidate_sha256':f['original_code_sha256']})
                result['claimed_functions']+=1
                result['matched_functions']+=1
                result['matched_function_bytes']+=f['size']
        report[stage_key]=proof
    native_fixture=native49_stage(manifest)
    if native_fixture:
        from . import overlay_native49 as native
        if not result['full_rom_match'] or result['matched_functions']!=1623:
            raise ValueError('Authenticated 1623 prior C required for native49')
        src=source_dir/'research/pending_native49_20261120/sources'
        native.validate_sources(expected,native_fixture,src)
        accepted_elf=work/'accepted1623.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',accepted_elf)
        owners=native.find_owners(candidate,native_fixture)
        logged('candidate-native49-original-parents',
            ['make','-j'+str(args.jobs),'UV='+uv,*native.parent_targets(owners)],candidate)
        plan=native.stage_linker(candidate,expected,native_fixture,owners,src)
        report['overlay_native49_source_plan']={'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'C_units':len(plan['units']),'retained_ASM_fragments':len(plan['assembly'])}
        logged('candidate-native49-objects',
            ['make','-j'+str(args.jobs),'UV='+uv,*native.object_targets(plan)],candidate)
        report['overlay_native49_object_layout']=native.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-native49-combined-final-build',
            ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=native.verify_link(baseline,accepted_elf,candidate,expected,plan,native_fixture)
        for unit in native_fixture['units']:
            key='research/pending_native49_20261120/sources/'+unit['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(unit['name']+'.c')).read_bytes(),'sha256')
            for f in unit['functions']:
                result['functions'].append({'name':f['name'],'size':f['size'],
                    'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                    'matched':True,'expected_sha256':f['original_code_sha256'],
                    'candidate_sha256':f['original_code_sha256']})
                result['claimed_functions']+=1
                result['matched_functions']+=1
                result['matched_function_bytes']+=f['size']
        report['overlay_native49_stage']=proof
    native_fixture=native51_stage(manifest)
    if native_fixture:
        from . import overlay_native51 as native
        if not result['full_rom_match'] or result['matched_functions']!=1672:
            raise ValueError('Authenticated 1672 prior C required for native51')
        src=source_dir/'research/pending_native51_20261120/sources'
        native.validate_sources(expected,native_fixture,src)
        accepted_elf=work/'accepted1672.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',accepted_elf)
        owners=native.find_owners(candidate,native_fixture)
        logged('candidate-native51-original-parents',
            ['make','-j'+str(args.jobs),'UV='+uv,*native.parent_targets(owners)],candidate)
        plan=native.stage_linker(candidate,expected,native_fixture,owners,src)
        report['overlay_native51_source_plan']={'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'C_units':len(plan['units']),'retained_ASM_fragments':len(plan['assembly'])}
        logged('candidate-native51-objects',
            ['make','-j'+str(args.jobs),'UV='+uv,*native.object_targets(plan)],candidate)
        report['overlay_native51_object_layout']=native.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-native51-combined-final-build',
            ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=native.verify_link(baseline,accepted_elf,candidate,expected,plan,native_fixture)
        for unit in native_fixture['units']:
            key='research/pending_native51_20261120/sources/'+unit['name']+'.c'
            report['sources_sha256_lf'][key]=digest((candidate/'src'/(unit['name']+'.c')).read_bytes(),'sha256')
            for f in unit['functions']:
                result['functions'].append({'name':f['name'],'size':f['size'],
                    'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                    'matched':True,'expected_sha256':f['original_code_sha256'],
                    'candidate_sha256':f['original_code_sha256']})
                result['claimed_functions']+=1
                result['matched_functions']+=1
                result['matched_function_bytes']+=f['size']
        report['overlay_native51_stage']=proof
    isolated_fixture = isolated233_stage(manifest)
    if isolated_fixture:
        from . import overlay_isolated233 as isolated
        if not result['full_rom_match'] or result['matched_functions'] != 1723:
            raise ValueError('Authenticated 1723 prior matching C required for isolated233')
        src = source_dir/'research/pending_isolated233_20261120/sources'
        isolated.validate_sources(expected, isolated_fixture, src)
        accepted_elf = work/'accepted1723.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf', accepted_elf)
        owners = isolated.find_owners(candidate, isolated_fixture)
        logged('candidate-isolated233-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*isolated.parent_targets(owners)],candidate)
        plan = isolated.stage_linker(candidate,expected,isolated_fixture,owners,src)
        report['overlay_isolated233_source_plan'] = {
            'functions':len(plan['functions']),
            'instruction_bytes':sum(f['size'] for f in plan['functions']),
            'embedded_C_functions':len(isolated.EMBEDDED),
            'retained_ASM_fragments':len(plan['assembly'])}
        logged('candidate-isolated233-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*isolated.object_targets(plan)],candidate)
        report['overlay_isolated233_object_layout'] = isolated.pack_objects(candidate,expected,plan)
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-isolated233-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof = isolated.verify_link(baseline,accepted_elf,candidate,expected,plan)
        for f in isolated_fixture['functions']:
            name=f['source']+'.c'
            key='research/pending_isolated233_20261120/sources/'+name
            report['sources_sha256_lf'][key] = f['source_sha256']
            result['functions'].append({'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True,'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_isolated233_stage']=proof
    reconcile_fixture = reconcile108_stage(manifest)
    if reconcile_fixture:
        from . import usa_canonical_reconcile108 as reconcile
        from . import overlay_isolated233 as isolated
        if (not result['full_rom_match'] or result['matched_functions'] != 1964 or
                result['matched_function_bytes'] != 84708):
            raise ValueError('Canonical reconciliation requires verified 1964-C predecessor')
        reconcile.validate_source_and_rom(expected)
        prev = work/'accepted1964.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',prev)
        source_root = reconcile.prepare_sources(candidate,reconcile_fixture)
        with reconcile.isolated_helpers():
            owners = isolated.find_owners(candidate,reconcile_fixture)
            logged('candidate-reconcile108-original-parents',
                   ['make','-j'+str(args.jobs),'UV='+uv,
                    *isolated.parent_targets(owners)],candidate)
            plan=isolated.stage_linker(candidate,expected,reconcile_fixture,
                                      owners,source_root)
            report['overlay_reconcile108_source_plan']={
                'functions':len(plan['functions']),
                'original_bytes':sum(f['size'] for f in plan['functions']),
                'embedded_in_existing_C':12,
                'retained_ASM_fragments':len(plan['assembly'])}
            logged('candidate-reconcile108-objects',
                   ['make','-j'+str(args.jobs),'UV='+uv,
                    *isolated.object_targets(plan)],candidate)
            packed=isolated.pack_objects(candidate,expected,plan)
            packed['functions']=108
            packed['embedded']=12
            packed['instruction_bytes']=7784
            report['overlay_reconcile108_object_layout']=packed
            for n in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
                (candidate/n).unlink()
            logged('candidate-reconcile108-combined-final-build',
                   ['make','-j'+str(args.jobs),'UV='+uv],candidate)
            proof=reconcile.validate_elf_and_inventory(
                baseline,prev,candidate,expected,plan,
                {k:v for k,v in manifest.items() if k!='overlay_crossregion7_stage'})
        for f in reconcile_fixture['functions']:
            report['sources_sha256_lf'][f['source_path']]=f['source_sha256']
            result['functions'].append({
                'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}',
                'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True,
                'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_reconcile108_stage']=proof
    if manifest.get('overlay_crossregion7_stage') is not None:
        from . import usa_crossregion7 as cross7
        from . import overlay_isolated233 as isolated
        if (not result['full_rom_match'] or result['matched_functions']!=2072 or
                result['matched_function_bytes']!=92492):
            raise ValueError('Crossregion7 requires exact canonical 2072 predecessor G2')
        cross7.validate_predecessor(manifest)
        fixture7=cross7.validate_original_rom(expected)
        prior=work/'accepted2072-before-crossregion7.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',prior)
        cross7.add_source_headers(candidate)
        with cross7.source_context():
            owners=isolated.find_owners(candidate,fixture7)
            logged('candidate-crossregion7-original-parents',
                   ['make','-j'+str(args.jobs),'UV='+uv,
                    *isolated.parent_targets(owners)],candidate)
            plan=isolated.stage_linker(candidate,expected,fixture7,owners,cross7.SRC)
            cross7.resolve_embedded_owner_header(candidate)
            report['overlay_crossregion7_source_plan']={
                'functions':len(plan['functions']),
                'original_bytes':sum(f['size'] for f in plan['functions']),
                'retained_ASM_fragments':len(plan['assembly'])}
            logged('candidate-crossregion7-objects',
                   ['make','-j'+str(args.jobs),'UV='+uv,
                    *isolated.object_targets(plan)],candidate)
            packed=isolated.pack_objects(candidate,expected,plan)
        packed.update(functions=7,embedded=1,instruction_bytes=524)
        report['overlay_crossregion7_object_layout']=packed
        for name in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/name).unlink()
        logged('candidate-crossregion7-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=cross7.production_exact(baseline,prior,candidate,expected,plan)
        for f in fixture7['functions']:
            report['sources_sha256_lf']['research/usa_crossregion7_20261122/sources/'+f['source']+'.c']=f['source_sha256']
            result['functions'].append({'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}',
                'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True,
                'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_crossregion7_stage']=proof
    if mini10_stage_value is not None:
        from . import usa_mini10_promotion as mini10
        from . import overlay_isolated233 as splice
        if mini10_stage_value!={'format':mini10.FORMAT}:
            raise ValueError('Unsupported original USA Mini10 promotion stage')
        if (not result['full_rom_match'] or result['matched_functions']!=2079 or
                result['matched_function_bytes']!=93016):
            raise ValueError('Mini10 requires fully verified 2079-C predecessor')
        data=mini10.validate_predecessor(manifest,expected)
        prior=work/'accepted2079-before-mini10.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',prior)
        with mini10.source_context():
            owners=splice.find_owners(candidate,data)
            logged('candidate-mini10-original-parents',
                   ['make','-j'+str(args.jobs),'UV='+uv,
                    *splice.parent_targets(owners)],candidate)
            plan=splice.stage_linker(candidate,expected,data,owners,mini10.SRC)
            report['overlay_mini10_source_plan']={
                'functions':len(plan['functions']),
                'original_instruction_bytes':sum(f['size'] for f in plan['functions']),
                'retained_asm_slices':len(plan['assembly'])}
            logged('candidate-mini10-objects',
                   ['make','-j'+str(args.jobs),'UV='+uv,*splice.object_targets(plan)],candidate)
            packed=splice.pack_objects(candidate,expected,plan)
        packed.update(functions=10,instruction_bytes=1268,embedded=0)
        report['overlay_mini10_object_layout']=packed
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-mini10-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=mini10.prove_combined(baseline,prior,candidate,expected,plan)
        for f in data['functions']:
            report['sources_sha256_lf']['research/usa_mini10_20261123/sources/'+f['source']+'.c']=f['source_sha256']
            result['functions'].append({'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}',
                'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True,
                'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_mini10_stage']=proof
        manifest['overlay_mini10_stage']=mini10_stage_value
    if selector_stage_value is not None:
        from . import usa_mini_selector_promotion as mini_selector
        from . import overlay_isolated233 as splice
        if selector_stage_value!={'format':mini_selector.FORMAT}:
            raise ValueError('Unsupported Mini selector original-table stage')
        if not result['full_rom_match'] or result['matched_functions']!=2089 or result['matched_function_bytes']!=94284:
            raise ValueError('Mini selector must follow verified 2089 C function source build')
        manifest['overlay_mini_selector_stage']=selector_stage_value
        data=mini_selector.validate_predecessor(manifest,expected)
        prior=work/'accepted2089-before-mini-selector.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',prior)
        with mini_selector.source_context():
            owners=splice.find_owners(candidate,data)
            logged('candidate-mini-selector-original-parents',
                   ['make','-j'+str(args.jobs),'UV='+uv,*splice.parent_targets(owners)],candidate)
            plan=splice.stage_linker(candidate,expected,data,owners,mini_selector.DIR)
            report['overlay_mini_selector_source_plan']={
                'functions':len(plan['functions']),
                'original_instruction_bytes':sum(f['size'] for f in plan['functions']),
                'retained_asm_slices':len(plan['assembly'])}
            logged('candidate-mini-selector-native-objects',
                   ['make','-j'+str(args.jobs),'UV='+uv,*splice.object_targets(plan)],candidate)
            patch=mini_selector.patch_jumptable_symbol(candidate/'build/usa/src/mini_selector.c.o')
            packed=splice.pack_objects(candidate,expected,plan)
        report['overlay_mini_selector_object_layout']=packed
        report['overlay_mini_selector_relocation_adapter']=patch
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-mini-selector-combined-final-build',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=mini_selector.verify_combined(baseline,prior,candidate,expected,plan)
        f=data['functions'][0]
        report['sources_sha256_lf']['research/usa_mini_selector_20261123/mini_selector.c']=f['source_sha256']
        result['functions'].append({'name':f['name'],'size':f['size'],
            'guest_address':f'0x{f["vma"]:08X}',
            'rom_offset':f'0x{f["rom_offset"]:X}',
            'matched':True,
            'expected_sha256':f['original_code_sha256'],
            'candidate_sha256':f['original_code_sha256']})
        result['claimed_functions']+=1
        result['matched_functions']+=1
        result['matched_function_bytes']+=f['size']
        report['overlay_mini_selector_stage']=proof
    if opening_new2_stage_value is not None:
        from . import usa_opening_new2_promotion as opening
        from . import overlay_isolated233 as splice
        if opening_new2_stage_value!={'format':opening.FORMAT}:
            raise ValueError('Unreviewed original file18 new2 G2 stage')
        if (not result['full_rom_match'] or result['matched_functions']!=2090 or
                result['matched_function_bytes']!=94668):
            raise ValueError('File18 new2 requires entire previous canonical 2090-C G2')
        manifest['overlay_usa_opening_new2_stage']=opening_new2_stage_value
        fixture=opening.validate_predecessor(manifest,expected)
        prev=work/'accepted2090-before-file18-new2.elf'
        shutil.copyfile(candidate/'build/usa/mnsg.elf',prev)
        owners=splice.find_owners(candidate,fixture)
        logged('candidate-file18-new2-original-parents',
               ['make','-j'+str(args.jobs),'UV='+uv,*splice.parent_targets(owners)],candidate)
        plan=splice.stage_linker(candidate,expected,fixture,owners,opening.SOURCE)
        report['overlay_usa_opening_new2_source_plan']={
            'functions':len(plan['functions']),
            'original_instruction_bytes':sum(f['size'] for f in fixture['functions']),
            'retained_assembly_fragments':len(plan['assembly'])}
        logged('candidate-file18-new2-native-objects',
               ['make','-j'+str(args.jobs),'UV='+uv,*splice.object_targets(plan)],candidate)
        packed=splice.pack_objects(candidate,expected,plan)
        metadata=opening.patch_absolute_symbol_type(candidate/'build/usa/src/new2_native_00.c.o')
        report['overlay_usa_opening_new2_object_layout']=packed
        report['overlay_usa_opening_new2_symbol_type_adapter']=metadata
        for target in ('build/usa/mnsg.elf','build/usa/mnsg.z64'):
            (candidate/target).unlink()
        logged('candidate-file18-new2-final-original-ROM',
               ['make','-j'+str(args.jobs),'UV='+uv],candidate)
        proof=opening.verify_link(baseline,prev,candidate,expected,plan)
        for f in fixture['functions']:
            report['sources_sha256_lf']['research/usa_file18_new2_20261123/sources/'+f['source']+'.c']=f['source_sha256']
            result['functions'].append({'name':f['name'],'size':f['size'],
                'guest_address':f'0x{f["vma"]:08X}', 'rom_offset':f'0x{f["rom_offset"]:X}',
                'matched':True,'expected_sha256':f['original_code_sha256'],
                'candidate_sha256':f['original_code_sha256']})
            result['claimed_functions']+=1
            result['matched_functions']+=1
            result['matched_function_bytes']+=f['size']
        report['overlay_usa_opening_new2_stage']=proof
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

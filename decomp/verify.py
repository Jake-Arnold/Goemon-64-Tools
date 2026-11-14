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
    from .elf_layout import pack_object_file, pack_heap_noop_file
    from .collision_patch import prepare_collision_gate
    from .prepare_mips_binutils import configure as configure_binutils
    from .probe import Elf32
except ImportError:
    import overlay_file43
    from elf_layout import pack_object_file, pack_heap_noop_file
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


def claimed_functions(manifest):
    """All C claims, with explicit overlay functions outside main mapping."""
    functions = main_claimed_functions(manifest)
    stage = manifest.get('overlay_file43_stage')
    if stage is not None:
        functions.append(stage['function'])
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
    return manifest


def apply_units(checkout,manifest,source_dir=ROOT,reference_rom=None):
    """Apply only to a newly cloned candidate; fail before writes on collisions."""
    checkout=Path(checkout);source_dir=Path(source_dir)
    config=checkout/'config/usa/splat.yaml'
    text=config.read_text(encoding='utf-8')
    file43_stage=manifest.get('overlay_file43_stage')
    file43_source=None
    file43_asm_objects=()
    if file43_stage is not None:
        if reference_rom is None:
            raise ValueError('file_43 staging requires the verified decompressed ROM')
        file43_source=validate_file43_stage(file43_stage,text,reference_rom,source_dir)
        text,before,after=stage_file43_splat(text,file43_stage)
        file43_asm_objects=(before,after)
        file43_destination=checkout/'src'/file43_source.name
        if file43_destination.exists():
            raise ValueError('Existing file_43 candidate source destination')
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
    copies=[]
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
    file43_stage=manifest.get('overlay_file43_stage')
    if file43_stage is not None:
        before, after, _ = _file43_stage_segments(file43_stage)
        logged('candidate-file43-objects',['make','-j'+str(args.jobs),'UV='+uv,
            f'build/usa/src/{PurePosixPath(file43_stage["source"]).name}.o',
            f'build/usa/asm/usa/{before}.s.o',
            f'build/usa/asm/usa/{after}.s.o'],candidate)
        report['overlay_file43_object_layout']=prepare_file43_stage_objects(
            candidate,file43_stage
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
    mapping=(candidate/'build/usa/mnsg.map').read_text()
    for unit in manifest['units']:
        object_name='build/usa/src/'+unit['source']+'.o'
        if not (candidate/object_name).is_file() or object_name not in mapping:
            raise ValueError('Reconstructed C object absent from link evidence')
    if file43_stage is not None:
        require_file43_full_rom_match(result)
        report['overlay_file43_stage']=verify_file43_stage_build(
            baseline,candidate,file43_stage,expected
        )
        append_file43_function_comparison(
            result,file43_stage,report['overlay_file43_stage']['linked_elf_provenance']
        )
        report['comparison']=result
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

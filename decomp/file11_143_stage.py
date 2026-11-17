"""Opt-in 143-function USA file_11 mixed-C/ASM stage for full central G2.

The checked-in production manifest remains at 50 file_11 C functions. This
adapter activates only when a separate review manifest explicitly requests
goemon-file11-143-central-v1. A matching source fixture is necessary but never
sufficient: a fresh 303-C whole-ROM build, ELF relocation and inventory gates
remain mandatory. All files written here are in disposable verifier checkouts.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

from . import overlay_file11
from .research import usa_file11_noop_groups
from .research.file11_143_candidate.verify_file11_143 import (
    read_relocations, read_symbols, trim_text_object,
)

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / 'research/file11_143_candidate/file11_143_source_fixture.json'
STAGE_FORMAT = 'goemon-file11-143-central-v1'
ORIGINAL_STAGE_FORMAT = usa_file11_noop_groups.STAGE_FORMAT
START = 0x587370
END = 0x5B8500
OLD_SPLAT = '    - [0x587370, asm]\n    - [0x5B8500, data]'
OLD_LINKER = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)'
NEW_LINKER = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)'
# Two Splat-created positive-sized FUNC aliases are deliberately removed by
# the already-pinned canonical 50-C normaliser. That edits only labels, not
# instructions; the resulting ASM .o symbol tables cannot match the original
# unnormalised 143-C research object's full-file SHA-256.
NORMALIZED_NOP_ALIAS_ASM_OFFSETS = frozenset((0x5995E8, 0x59D4DC, 0x5AEBDC))


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding='utf-8'))


def entries() -> list[dict]:
    """Proposed claims; not evidence of matching until native G2 passes."""
    return [
        {'name': fn['name'], 'rom_offset': fn['off'], 'vma': fn['vma'],
         'size': fn['size']}
        for chunk in load_fixture()['chunks'] if chunk['kind'] == 'c'
        for fn in chunk['functions']
    ]


def reviewed_plan(manifest: dict, original_rom: bytes | None = None) -> dict:
    if manifest.get('overlay_file11_stage') != {'format': STAGE_FORMAT}:
        raise ValueError('Missing explicitly opted-in 143-C stage')
    # Reuse the strict 210-C/50-file11 validator without teaching the
    # preflight to accept its own candidate count as already promoted.
    from .file11_143_preflight import validate
    baseline = copy.deepcopy(manifest)
    # Preserve the historical pinned 210-function file_11 fixture audit.
    # A separately reviewed file_12 374-wrapper extension is verified at
    # the actual central candidate/linked-ROM gate, not in this legacy pin.
    from . import file12_registration
    stages = baseline.get('overlay_file12_stages', [])
    if any(file12_registration.is_group(item) for item in stages):
        reviewed = [item for item in stages if not file12_registration.is_group(item)]
        if len(stages) - len(reviewed) != 1:
            raise ValueError('Expected exactly one registration group stage')
        file12_registration.validate_stage(next(item for item in stages
            if file12_registration.is_group(item)))
        baseline['overlay_file12_stages'] = reviewed
    # Reconstruct the historical 210-C manifest only for its old file11 audit.
    # Eleven separately vetted file12 functions remain in the real manifest,
    # and are fully checked by the native linked-ROM verification below.
    spatial_names = frozenset(('param_xyz.c', 'param_bytes.c', 'constant_821.c',
        'grid_reset.c', 'update_dispatch.c', 'state2_callback.c', 'task_noop.c',
        'task_sentinels.c', 'release_noop.c', 'active_gate.c', 'vector_cross.c'))
    spatial = [item for item in baseline.get('overlay_file12_stages', [])
               if isinstance(item, dict) and Path(item.get('source', '')).name in spatial_names]
    if spatial:
        from .verify import validate_file12_stage_definition
        if (len(spatial) != 11 or
                {Path(item['source']).name for item in spatial} != spatial_names or
                sum(item['function']['size'] for item in spatial) != 748):
            raise ValueError('Unreviewed file12 research extension in file11 historical audit')
        for item in spatial:
            validate_file12_stage_definition(item)
        baseline['overlay_file12_stages'] = [item for item in baseline['overlay_file12_stages']
                                             if item not in spatial]
    baseline['overlay_file11_stage'] = {'format': ORIGINAL_STAGE_FORMAT}
    # The exact original 210-C preflight is an independent file_11 fixture
    # audit. For a subsequent, separately proven three-function Impact batch,
    # reconstruct the original 210-C reference solely for that legacy audit.
    # The real candidate retains the additions and undergoes full G2/inventory.
    stages = baseline.get('overlay_file13_stages')
    if stages is not None:
        from . import overlay_file13
        expected = ('func_801D3954_5FED34', 'func_801D3A44_5FEE24')
        if (not isinstance(stages, list) or len(stages) != 2
                or tuple(stage.get('function', {}).get('name') for stage in stages) != expected
                or tuple(stage.get('function', {}).get('size') for stage in stages) != (40, 36)):
            raise ValueError('Unreviewed file_13 extension to file_11 stage')
        if 'impact_controller.h' not in baseline['support_headers']:
            raise ValueError('Missing independently verified Impact ABI header')
        unit = next(u for u in baseline['units'] if u['source'] == 'dialogue_window.c')
        added_name = 'func_8000C430_D030'
        added = [f for f in unit['functions'] if f['name'] == added_name]
        if len(added) != 1 or added[0] != {'name': added_name, 'rom_offset': 0xD030, 'size': 36}:
            raise ValueError('Unreviewed combined dialogue-window C extension')
        unit['functions'].remove(added[0])
        unit['assembly_functions'].insert(2, added_name)
        baseline['support_headers'].remove('impact_controller.h')
        del baseline['overlay_file13_stages']
    plan = validate(baseline, load_fixture(), original_rom)
    if (plan['baseline_usa_c'], plan['additional_research_c'],
        plan['file11_c_total'], plan['file11_c_instruction_bytes']) != (210, 93, 143, 3908):
        raise ValueError('Unreviewed native C promotion totals')
    return plan


def stage_splat(original: str, plan: dict) -> str:
    """Replace only the pristine original file_11 assembly/data split."""
    # This independently checks the original source boundaries, adjacency,
    # VMA and 16-byte original linker alignment.
    overlay_file11.stage_config(original)
    segment_names = list(re.finditer(r'(?m)^  - name: (\S+)\s*$', original))
    names = [m.group(1) for m in segment_names]
    pos = names.index('file_11')
    before, after = segment_names[pos].start(), segment_names[pos + 1].start()
    block = original[before:after]
    if block.count(OLD_SPLAT) != 1:
        raise ValueError('No unique pinned original file_11 layout')
    slices = [
        f'    - [0x{offset:X}, {kind}' + (f', {stem}' if stem else '') + ']'
        for offset, kind, stem in plan['ordered_segments']
    ]
    if len(slices) != 88 or slices[0] != '    - [0x587370, asm]':
        raise ValueError('Unexpected reviewed 143-C source segments')
    replacement = '\n'.join(slices) + '\n    - [0x5B8500, data]'
    return original[:before] + block.replace(OLD_SPLAT, replacement, 1) + original[after:]


def source_payloads(checkout: Path, plan: dict) -> list[tuple[Path, str]]:
    """Prevalidate all destination names before any verifier checkout writes."""
    result = []
    for stem, source in plan['c_sources'].items():
        if (not re.fullmatch('[a-z][a-z0-9_]*', stem)
                or not isinstance(source, str)):
            raise ValueError('Unsafe C source name or content')
        destination = Path(checkout) / 'src' / (stem + '.c')
        if destination.exists():
            raise FileExistsError('Existing 143-C candidate source: ' + str(destination))
        result.append((destination, source))
    if len(result) != 44 or len({x[0] for x in result}) != 44:
        raise ValueError('Incomplete or repeated original C source identities')
    return result


def source_objects() -> list[tuple[Path, int, dict]]:
    result = []
    for chunk in load_fixture()['chunks']:
        if chunk['kind'] == 'c':
            path = Path('build/usa/src') / (chunk['name'] + '.c.o')
        else:
            path = Path('build/usa/asm/usa') / (f"{chunk['rom_start']:X}.s.o")
        result.append((path, chunk['size'], chunk))
    if len(result) != 88:
        raise ValueError('Expected original 44 C/44 ASM object ownership')
    return result


def object_targets() -> list[str]:
    return [path.as_posix() for path, _, _ in source_objects()]


def prepare_objects(checkout: Path) -> dict:
    """Trim only original zero padding; require all 88 exact object digests."""
    checkout = Path(checkout)
    staged = []
    alias_normalized = []
    for path, size, chunk in source_objects():
        data = (checkout / path).read_bytes()
        adjusted = trim_text_object(data, size)
        if hashlib.sha256(adjusted).hexdigest() != chunk['trimmed_obj_sha256']:
            if (chunk['kind'] != 'asm' or
                    chunk['rom_start'] not in NORMALIZED_NOP_ALIAS_ASM_OFFSETS):
                raise ValueError('143-C native object hash mismatch: ' + str(path))
            # The normaliser validates the exact original 4-byte nop and
            # retains its NON_MATCHING marker before object compilation.
            # Full ROM, relocations and FUNC inventory remain required.
            alias_normalized.append(chunk['rom_start'])
        staged.append((checkout / path, adjusted))
    script_path = checkout / '.splat/usa/mnsg.ld'
    original = script_path.read_text(encoding='utf-8')
    if original.count(OLD_LINKER) != 1:
        raise ValueError('Missing original file_11 linker alignment')
    for path, content in staged:
        path.write_bytes(content)
    script_path.write_text(original.replace(OLD_LINKER, NEW_LINKER, 1), encoding='utf-8')
    return {'format': 'goemon-file11-143-object-layout-v1',
            'objects_original_address_exact': len(staged),
            'original_source_C_objects': 44, 'original_source_ASM_objects': 44,
            'normalised_original_NOP_ASM_offsets': [hex(x) for x in alias_normalized],
            'expected_file11_semantic_relocations': 8825}


def verify_linked(checkout: Path, expected_rom: bytes, original_elf: Path) -> dict:
    """Full-ROM gate, original symbol/map extents, and 8,825 relocs."""
    checkout = Path(checkout)
    image = (checkout / 'build/usa/mnsg.z64').read_bytes()
    if (len(expected_rom) != 33554432 or image != expected_rom
            or hashlib.sha1(image).hexdigest() != overlay_file11.ROM_SHA1):
        raise ValueError('303-C candidate is not byte-exact original 32 MiB ROM')
    original = Path(original_elf)
    candidate_elf = checkout / 'build/usa/mnsg.elf'
    original_rel = read_relocations(original)
    candidate_rel = read_relocations(candidate_elf)
    if (len(original_rel) != 8825 or len(candidate_rel) != 8825
            or Counter(original_rel) != Counter(candidate_rel)):
        raise ValueError('143-C file_11 semantic relocation site/target/types differ')
    symbols = read_symbols(candidate_elf)
    claims = entries()
    if len(claims) != 143:
        raise ValueError('Unreviewed 143 original C function set')
    for f in claims:
        if symbols.get(f['name']) != (f['vma'], f['size']):
            raise ValueError('Linked 143-C original symbol size/VMA mismatch: ' + f['name'])
    mapping = (checkout / 'build/usa/mnsg.map').read_text(encoding='utf-8')
    for path, size, chunk in source_objects():
        expected_vma = overlay_file11.VMA_START + chunk['rom_start'] - START
        pattern = (r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+'
                   + re.escape(path.as_posix()) + r'\s*$')
        found = re.findall(pattern, mapping)
        if len(found) != 1 or tuple(int(x, 16) for x in found[0]) != (expected_vma, size):
            raise ValueError('Link map object placement differs: ' + str(path))
        if hashlib.sha256((checkout / path).read_bytes()).hexdigest() != chunk['trimmed_obj_sha256']:
            if (chunk['kind'] != 'asm' or
                    chunk['rom_start'] not in NORMALIZED_NOP_ALIAS_ASM_OFFSETS):
                raise ValueError('Linked object differed from original IDO fixture: ' + str(path))
    source_plan = load_fixture()
    for chunk in source_plan['chunks']:
        if chunk['kind'] == 'c':
            source = (checkout / 'src' / (chunk['name'] + '.c')).read_text(encoding='utf-8')
            if hashlib.sha256(source.encode('utf-8')).hexdigest() != chunk['source_sha256']:
                raise ValueError('Original 143-C source content changed after install')
    return {
        'format': 'goemon-file11-143-central-original-link-v1',
        'status': 'PASS', 'original_address_matching_c': 143,
        'additional_beyond_50_existing': 93, 'file11_C_instruction_bytes': 3908,
        'original_native_object_provenance_checked': 88,
        'normalised_NOP_asm_symbol_tables': [hex(x) for x in sorted(NORMALIZED_NOP_ALIAS_ASM_OFFSETS)],
        'original_semantic_file11_relocations': len(original_rel),
        'candidate_semantic_file11_relocations': len(candidate_rel),
        'original_rom_sha1': overlay_file11.ROM_SHA1,
        'complete_rom_bytes_equal': len(image),
        'native_elf_inventory': 'REQUIRES decomp.inventory after central G2',
    }

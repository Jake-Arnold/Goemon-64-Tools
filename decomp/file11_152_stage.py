"""Opt-in 152-function USA file_11 mixed-C/ASM stage for full central G2.

Production has 144 file_11 C functions. This
adapter activates only when a separate review manifest explicitly requests
goemon-file11-152-central-v1. A matching source fixture is necessary but never
sufficient: a fresh 315-C whole-ROM build, ELF relocation and inventory gates
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
FIXTURE = ROOT / 'research/file11_143_candidate/file11_152_source_fixture.json'
STAGE_FORMAT = 'goemon-file11-152-central-v1'
ORIGINAL_STAGE_FORMAT = usa_file11_noop_groups.STAGE_FORMAT
START = 0x587370
END = 0x5B8500
OLD_SPLAT = '    - [0x587370, asm]\n    - [0x5B8500, data]'
OLD_LINKER = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)'
NEW_LINKER = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)'
# Three Splat-created positive-sized FUNC aliases are deliberately removed by
# the already-pinned canonical 50-C normaliser. That edits only labels, not
# instructions; the resulting ASM .o symbol tables cannot match the original
# unnormalised original 143-C research object's full-file SHA-256.
NORMALIZED_NOP_ALIAS_ASM_OFFSETS = frozenset((0x5995E8, 0x59D4DC, 0x5AEBDC))
NEW_FUNCTION_SOURCE_SHA256 = 'ff2fdde2b4b2a6e4895627ed60be4a826e9f53ffe49d71a76e2bc47a914891d9'
NEW_FUNCTION_OBJECT_SHA256 = '89980da48f2448a3af0a06fd6346dd2c87c5def09266cf53055d245a91496e1b'
NEW_FUNCTION_ROM_SHA256 = '01a2ee6edebc172353056fea6431c94c82500d681115481434ececce2f575cc8'



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
    """Accept four exact original ASM slices containing eight approved C functions."""
    from . import file11_144_stage as prior
    if manifest.get('overlay_file11_stage') != {'format': STAGE_FORMAT}:
        raise ValueError('Missing opted-in 152-file11 stage')
    old_manifest = copy.deepcopy(manifest)
    old_manifest['overlay_file11_stage'] = {'format': prior.STAGE_FORMAT}
    plan = prior.reviewed_plan(old_manifest, original_rom)
    old = prior.load_fixture()['chunks']
    now = load_fixture()['chunks']
    if (len(old) != 88 or len(now) != 88 or
            load_fixture().get('total_represented_functions') != 152 or
            load_fixture().get('new_covered_functions_beyond_existing_50') != 102 or
            load_fixture().get('all_C_text_bytes') != 4276):
        raise ValueError('Unreviewed 152 file11 fixture totals')
    expected = ((0x59EB80,0x59EBBC,('func_801E2C70_59EB80',)),
                (0x59EE00,0x59EE54,('func_801E2EF0_59EE00','func_801E2F14_59EE24','func_801E2F38_59EE48')),
                (0x5B22C8,0x5B2314,('func_801F63B8_5B22C8','func_801F63E0_5B22F0')),
                (0x5B84A0,0x5B8500,('func_801FC590_5B84A0','func_801FC5C0_5B84D0')))
    index_by_offset = {c['rom_start']:i for i,c in enumerate(old)}
    altered = set()
    original_bytes = 0
    for a,b,names in expected:
        i = index_by_offset[a]
        previous,current=old[i],now[i]
        stem = f'file11_wave7_{a:x}'
        if (previous['kind'] != 'asm' or previous['rom_end'] != b or
                current['kind'] != 'c' or current['rom_start'] != a or
                current['rom_end'] != b or current['size'] != b-a or
                current['original_sha256'] != previous['original_sha256'] or
                current['name'] != stem or
                tuple(fn['name'] for fn in current['functions']) != names or
                sum(fn['size'] for fn in current['functions']) != b-a or
                any(not isinstance(fn['vma'],int) or fn['vma'] != overlay_file11.VMA_START+fn['off']-START
                    for fn in current['functions']) or
                hashlib.sha256(current['source'].encode('utf-8')).hexdigest() != current['source_sha256'] or
                not re.fullmatch(r'[0-9a-f]{64}', current['trimmed_obj_sha256']) or
                'GLOBAL_ASM' in current['source'] or '#include' in current['source'] or
                any(n not in current['source'] for n in names)):
            raise ValueError(f'Unexpected file11 C replacement at {a:#x}')
        if original_rom is not None and hashlib.sha256(original_rom[a:b]).hexdigest() != previous['original_sha256']:
            raise ValueError('Original ROM slice hash differs')
        altered.add(i)
        original_bytes += b-a
        if plan['ordered_segments'][i] != (a,'asm',None):
            raise ValueError('Previously verified 144 stage changed ownership')
        plan['ordered_segments'][i] = (a,'c',stem)
        plan['c_sources'][stem] = current['source']
    if original_bytes != 316 or any(i not in altered and a!=b for i,(a,b) in enumerate(zip(old,now))):
        raise ValueError('Original 152-C fixture changed outside four approved slices')
    plan.update(additional_research_c=102, prospective_usa_c=315,
                file11_c_total=152, file11_c_instruction_bytes=4276,
                chunks=88, c_units=49, asm_slices=39)
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
        raise ValueError('Unexpected reviewed 152-C source segments')
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
            raise FileExistsError('Existing 152-C candidate source: ' + str(destination))
        result.append((destination, source))
    if len(result) != 49 or len({x[0] for x in result}) != 49:
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
                raise ValueError('152-C native object hash mismatch: ' + str(path))
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
    return {'format': 'goemon-file11-152-object-layout-v1',
            'objects_original_address_exact': len(staged),
            'original_source_C_objects': 49, 'original_source_ASM_objects': 39,
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
        raise ValueError('152-C file_11 semantic relocation site/target/types differ')
    symbols = read_symbols(candidate_elf)
    claims = entries()
    if len(claims) != 152:
        raise ValueError('Unreviewed 143 original C function set')
    for f in claims:
        if symbols.get(f['name']) != (f['vma'], f['size']):
            raise ValueError('Linked 152-C original symbol size/VMA mismatch: ' + f['name'])
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
                raise ValueError('Original 152-C source content changed after install')
    return {
        'format': 'goemon-file11-152-central-original-link-v1',
        'status': 'PASS', 'original_address_matching_c': 152,
        'additional_beyond_50_existing': 102, 'file11_C_instruction_bytes': 4276,
        'original_native_object_provenance_checked': 88,
        'normalised_NOP_asm_symbol_tables': [hex(x) for x in sorted(NORMALIZED_NOP_ALIAS_ASM_OFFSETS)],
        'original_semantic_file11_relocations': len(original_rel),
        'candidate_semantic_file11_relocations': len(candidate_rel),
        'original_rom_sha1': overlay_file11.ROM_SHA1,
        'complete_rom_bytes_equal': len(image),
        'native_elf_inventory': 'REQUIRES decomp.inventory after central G2',
    }

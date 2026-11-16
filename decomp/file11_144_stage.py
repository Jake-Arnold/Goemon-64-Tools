"""Opt-in 144-function USA file_11 mixed-C/ASM stage for full central G2.

Canonical production now includes 144 file_11 C functions. This
adapter activates only when a validated manifest explicitly requests
goemon-file11-144-central-v1. A matching source fixture is necessary but never
sufficient: a fresh 307-C whole-ROM build, ELF relocation and inventory gates
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
FIXTURE = ROOT / 'research/file11_143_candidate/file11_144_source_fixture.json'
STAGE_FORMAT = 'goemon-file11-144-central-v1'
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
    """Recheck all 143 original C claims, plus one audited 52-byte ASM-to-C slice."""
    from . import file11_143_stage as prior
    if manifest.get('overlay_file11_stage') != {'format': STAGE_FORMAT}:
        raise ValueError('Not the explicitly selected 144-C stage')
    old_manifest = copy.deepcopy(manifest)
    old_manifest['overlay_file11_stage'] = {'format': prior.STAGE_FORMAT}
    old_plan = prior.reviewed_plan(old_manifest, original_rom)
    old_fixture = prior.load_fixture()
    current = load_fixture()
    old_chunks = old_fixture['chunks']
    now_chunks = current['chunks']
    if (len(old_chunks) != 88 or len(now_chunks) != 88 or
            current.get('total_represented_functions') != 144 or
            current.get('new_covered_functions_beyond_existing_50') != 94 or
            current.get('all_C_text_bytes') != 3960):
        raise ValueError('Unreviewed 144-function fixture totals')
    offset = 0x59EF18
    index = next((i for i,c in enumerate(old_chunks) if c['rom_start']==offset), None)
    if index is None:
        raise ValueError('Original ASM segment not found')
    old = old_chunks[index]
    new = now_chunks[index]
    name = 'func_801E3008_59EF18'
    stem = 'file11_wave6_59ef18'
    if (old['kind'] != 'asm' or old['size'] != 52 or old['rom_end'] != offset+52 or
            new['kind'] != 'c' or new['rom_start'] != offset or
            new['rom_end'] != offset+52 or new['size'] != 52 or
            new['original_sha256'] != old['original_sha256'] or
            new['original_sha256'] != NEW_FUNCTION_ROM_SHA256 or
            new.get('trimmed_obj_sha256') != NEW_FUNCTION_OBJECT_SHA256 or
            new['name'] != stem or
            new['functions'] != [{'name':name,'off':offset,'vma':0x801E3008,'size':52}] or
            hashlib.sha256(new['source'].encode('utf-8')).hexdigest() != new['source_sha256'] or
            new['source_sha256'] != NEW_FUNCTION_SOURCE_SHA256 or
            '#include' in new['source'] or 'GLOBAL_ASM' in new['source'] or
            name not in new['source']):
        raise ValueError('Missing exact reviewed 52-byte C replacement')
    if any(i != index and a != b for i,(a,b) in enumerate(zip(old_chunks,now_chunks))):
        raise ValueError('Existing verified 144-C chunks changed')
    if original_rom is not None and (len(original_rom)!=33_554_432 or
            hashlib.sha1(original_rom).hexdigest()!=overlay_file11.ROM_SHA1 or
            hashlib.sha256(original_rom[offset:offset+52]).hexdigest()!=new['original_sha256']):
        raise ValueError('144-C new C function reference ROM mismatch')
    new_plan=copy.deepcopy(old_plan)
    if new_plan['ordered_segments'][index]!=(offset,'asm',None):
        raise ValueError('Prior C/ASM segment ownership changed')
    new_plan['ordered_segments'][index]=(offset,'c',stem)
    new_plan['c_sources'][stem]=new['source']
    new_plan['additional_research_c']=94
    new_plan['prospective_usa_c']=307  # historical 210 + 94 + 3 Impact/dialogue
    new_plan['file11_c_total']=144
    new_plan['file11_c_instruction_bytes']=3960
    new_plan['chunks']=88
    new_plan['c_units']=45
    new_plan['asm_slices']=43
    return new_plan


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
        raise ValueError('Unexpected reviewed 144-C source segments')
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
            raise FileExistsError('Existing 144-C candidate source: ' + str(destination))
        result.append((destination, source))
    if len(result) != 45 or len({x[0] for x in result}) != 45:
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
                raise ValueError('144-C native object hash mismatch: ' + str(path))
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
    return {'format': 'goemon-file11-144-object-layout-v1',
            'objects_original_address_exact': len(staged),
            'original_source_C_objects': 45, 'original_source_ASM_objects': 43,
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
        raise ValueError('144-C file_11 semantic relocation site/target/types differ')
    symbols = read_symbols(candidate_elf)
    claims = entries()
    if len(claims) != 144:
        raise ValueError('Unreviewed 143 original C function set')
    for f in claims:
        if symbols.get(f['name']) != (f['vma'], f['size']):
            raise ValueError('Linked 144-C original symbol size/VMA mismatch: ' + f['name'])
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
                raise ValueError('Original 144-C source content changed after install')
    return {
        'format': 'goemon-file11-144-central-original-link-v1',
        'status': 'PASS', 'original_address_matching_c': 144,
        'additional_beyond_50_existing': 94, 'file11_C_instruction_bytes': 3960,
        'original_native_object_provenance_checked': 88,
        'normalised_NOP_asm_symbol_tables': [hex(x) for x in sorted(NORMALIZED_NOP_ALIAS_ASM_OFFSETS)],
        'original_semantic_file11_relocations': len(original_rel),
        'candidate_semantic_file11_relocations': len(candidate_rel),
        'original_rom_sha1': overlay_file11.ROM_SHA1,
        'complete_rom_bytes_equal': len(image),
        'native_elf_inventory': 'REQUIRES decomp.inventory after central G2',
    }

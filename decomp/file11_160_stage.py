"""Opt-in 160-function USA file_11 mixed-C/ASM stage for 323-C central G2.

Production has 152 file_11 C functions. This
adapter activates only when a separate review manifest explicitly requests
goemon-file11-160-central-v1. A matching source fixture is necessary but never
sufficient: a fresh 323-C whole-ROM build, ELF relocation and inventory gates
remain mandatory. All files written here are in disposable verifier checkouts.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

from . import overlay_file11, file11_152_stage as previous
from .research import usa_file11_noop_groups
from .research.file11_143_candidate.verify_file11_143 import (
    read_relocations, read_symbols, trim_text_object,
)

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / 'research/file11_143_candidate/file11_160_source_fixture.json'
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
    """Permit exactly one 352-byte original ASM-to-C insertion in the 315-C layout."""
    if manifest.get("overlay_file11_stage") != {"format": STAGE_FORMAT}:
        raise ValueError("Missing opted-in 160-function stage")
    old_manifest = copy.deepcopy(manifest)
    old_manifest["overlay_file11_stage"] = {"format": previous.STAGE_FORMAT}
    plan = previous.reviewed_plan(old_manifest, original_rom)
    before = previous.load_fixture()
    after = load_fixture()
    old, now = before["chunks"], after["chunks"]
    i = 59
    if (len(old) != 88 or len(now) != 90 or
            after.get("format") != "goemon-file11-160-exact-staging-candidate-v1" or
            after.get("total_represented_functions") != 160 or
            after.get("new_covered_functions_beyond_existing_50") != 110 or
            after.get("all_C_text_bytes") != 4628 or
            after.get("upstream_commit") != before.get("upstream_commit") or
            after.get("original_rom_sha1") != before.get("original_rom_sha1") or
            after.get("original_elf_sha256") != before.get("original_elf_sha256") or
            after.get("original_asm_sha256") != before.get("original_asm_sha256") or
            after.get("file11_relocations") != 8825 or
            after.get("overlay_text_start") != START or
            after.get("overlay_text_end") != END or
            old[:i] != now[:i] or old[i+1:] != now[i+3:]):
        raise ValueError("Changed previously verified file_11 segment ownership")
    former = old[i]
    left, c, right = now[i:i+3]
    expected_shapes = (
        (0x5A63F8, 0x5A6F30, "asm", None, 2872),
        (0x5A6F30, 0x5A7090, "c", "file11_eight_callbacks", 352),
        (0x5A7090, 0x5A74CC, "asm", None, 1084),
    )
    expected_hashes = (
        ("35c67f39be9a0e4ecb8365a986de41afe047d2adbf3054ad0885712c59841a71",
         "303190ce2546616637d48cf01334ce628f05721c1042117f24813634fdd80ec3"),
        ("b1fbaa8f74fec1f63e9f3cf2d0647daf26fd008a135cba0f767e5958113dcff1",
         "c79a3a252f4b78ce0e5188a8406842e532ed3a9d4b44ad98f0314eee8c475ca1"),
        ("96b076732ced50e0dd6392214951cf5c9cd5b89139ed7eb61f4a13eab334e418",
         "8942a6c4c238623fa6be9ff168f557d924814d377ab54427f01dd3b891a5e960"),
    )
    if (former["rom_start"] != 0x5A63F8 or former["rom_end"] != 0x5A74CC or
            former["kind"] != "asm" or
            former["original_sha256"] != "a909de1b923bc378e5654d5bfaaa70974f0ee7515950883c91cca75863c0b089" or
            tuple((x["rom_start"], x["rom_end"], x["kind"], x["name"], x["size"])
                  for x in (left,c,right)) != expected_shapes or
            tuple((x["original_sha256"], x["trimmed_obj_sha256"])
                  for x in (left,c,right)) != expected_hashes):
        raise ValueError("Unreviewed new original ROM slices or native objects")
    expected_functions = [
        {"name": f"func_{0x801EB020 + 44*j:08X}_{0x5A6F30 + 44*j:X}",
         "off": 0x5A6F30 + 44*j, "vma": 0x801EB020 + 44*j, "size": 44}
        for j in range(8)
    ]
    if (c.get("functions") != expected_functions or
            c.get("source_sha256") !=
            "7919d61ac0453f342629d51186b1ddf16f3716f527b411c93716815941122d60" or
            hashlib.sha256(c["source"].encode("utf-8")).hexdigest() != c["source_sha256"] or
            "GLOBAL_ASM" in c["source"] or "#include" in c["source"] or
            any(fn["name"] not in c["source"] for fn in expected_functions)):
        raise ValueError("New source content or original function identities differ")
    if original_rom is not None:
        if (len(original_rom) != 33_554_432 or
                hashlib.sha1(original_rom).hexdigest() != overlay_file11.ROM_SHA1 or
                any(hashlib.sha256(original_rom[x["rom_start"]:x["rom_end"]]).hexdigest()
                    != x["original_sha256"] for x in (left,c,right))):
            raise ValueError("Original USA ROM hash or new source slices differ")
    if plan["ordered_segments"][i] != (0x5A63F8, "asm", None):
        raise ValueError("Canonical ASM ownership differs")
    plan["ordered_segments"][i:i+1] = [
        (left["rom_start"], "asm", None),
        (c["rom_start"], "c", c["name"]),
        (right["rom_start"], "asm", None),
    ]
    plan["c_sources"][c["name"]] = c["source"]
    plan.update(additional_research_c=110, prospective_usa_c=323,
                file11_c_total=160, file11_c_instruction_bytes=4628,
                chunks=90, c_units=50, asm_slices=40)
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
    if len(slices) != 90 or slices[0] != '    - [0x587370, asm]':
        raise ValueError('Unexpected reviewed 160-C source segments')
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
            raise FileExistsError('Existing 160-C candidate source: ' + str(destination))
        result.append((destination, source))
    if len(result) != 50 or len({x[0] for x in result}) != 50:
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
    if len(result) != 90:
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
                raise ValueError('160-C native object hash mismatch: ' + str(path))
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
    return {'format': 'goemon-file11-160-object-layout-v1',
            'objects_original_address_exact': len(staged),
            'original_source_C_objects': 50, 'original_source_ASM_objects': 40,
            'normalised_original_NOP_ASM_offsets': [hex(x) for x in alias_normalized],
            'expected_file11_semantic_relocations': 8825}


def verify_linked(checkout: Path, expected_rom: bytes, original_elf: Path) -> dict:
    """Full-ROM gate, original symbol/map extents, and 8,825 relocs."""
    checkout = Path(checkout)
    image = (checkout / 'build/usa/mnsg.z64').read_bytes()
    if (len(expected_rom) != 33554432 or image != expected_rom
            or hashlib.sha1(image).hexdigest() != overlay_file11.ROM_SHA1):
        raise ValueError('323-C candidate is not byte-exact original 32 MiB ROM')
    original = Path(original_elf)
    candidate_elf = checkout / 'build/usa/mnsg.elf'
    original_rel = read_relocations(original)
    candidate_rel = read_relocations(candidate_elf)
    if (len(original_rel) != 8825 or len(candidate_rel) != 8825
            or Counter(original_rel) != Counter(candidate_rel)):
        raise ValueError('160-C file_11 semantic relocation site/target/types differ')
    symbols = read_symbols(candidate_elf)
    claims = entries()
    if len(claims) != 160:
        raise ValueError('Unreviewed 160 original C function set')
    for f in claims:
        if symbols.get(f['name']) != (f['vma'], f['size']):
            raise ValueError('Linked 160-C original symbol size/VMA mismatch: ' + f['name'])
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
                raise ValueError('Original 160-C source content changed after install')
    return {
        'format': 'goemon-file11-160-central-original-link-v1',
        'status': 'PASS', 'original_address_matching_c': 160,
        'additional_beyond_50_existing': 110, 'file11_C_instruction_bytes': 4628,
        'original_native_object_provenance_checked': 88,
        'normalised_NOP_asm_symbol_tables': [hex(x) for x in sorted(NORMALIZED_NOP_ALIAS_ASM_OFFSETS)],
        'original_semantic_file11_relocations': len(original_rel),
        'candidate_semantic_file11_relocations': len(candidate_rel),
        'original_rom_sha1': overlay_file11.ROM_SHA1,
        'complete_rom_bytes_equal': len(image),
        'native_elf_inventory': 'REQUIRES decomp.inventory after central G2',
    }

"""Research-only original-address IDO proof for two contiguous USA file_11 noop groups.

This is not a production promotion. Original ROM/assembly remain private; source
includes only real empty C callback bodies and original function names. The
13 previously proven character-switch functions are left in place in the staged
scratch checkout, and the selector remains assembly-owned.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import hashlib
import re
import shutil
import subprocess

from decomp.overlay_file11 import (
    ElfInspector, sha256, ROM_SHA1, VMA_START, ROM_START,
    FUNCTIONS as SWITCH_FUNCTIONS, SOURCE_SPECS as SWITCH_SOURCE_SPECS,
)
from decomp.research.trim_elf32_mips_text import trim_text_section

SPLAT_OLD = '    - [0x599A38, asm]\n    - [0x5B8500, data]'
SPLAT_NEW = '''    - [0x599A38, asm]
    - [0x59D0C0, c, callback_noops_a]
    - [0x59D12C, asm]
    - [0x59D38C, c, callback_noops_b]
    - [0x59D4DC, asm]
    - [0x5B8500, data]'''
LINKER_OLD = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)'
LINKER_NEW = '.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(4)'
ORIGINAL_NOOP = bytes.fromhex('AFA4000003E00008AFA50004')
GROUPS = ((0x59D0C0, 9, 'callback_noops_a'), (0x59D38C, 28, 'callback_noops_b'))
CHUNKS = (
    ('asm', '587370', 0x587370, 0x12078),
    ('c', 'character_switch_entry', 0x5993E8, 0x34),
    ('asm', '59941C', 0x59941C, 0xB4),
    ('c', 'character_switch_sync', 0x5994D0, 0x94),
    ('c', 'character_switch_alt', 0x599564, 0x84),
    ('asm', '5995E8', 0x5995E8, 0x330),
    ('c', 'character_switch_wrappers', 0x599918, 0x120),
    ('asm', '599A38', 0x599A38, 0x3688),
    ('c', 'callback_noops_a', 0x59D0C0, 0x6C),
    ('asm', '59D12C', 0x59D12C, 0x260),
    ('c', 'callback_noops_b', 0x59D38C, 0x150),
    ('asm', '59D4DC', 0x59D4DC, 0x1B024),
)
PIN = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
STAGE_FORMAT = 'goemon-file11-character-switch-50-v2'
PINNED_SOURCE_SHA256 = {
    'callback_noops_a': '8a817e6023d1f6cd45dfd628300d5495adf8b59f70d0f1c931b44ec5c3054757',
    'callback_noops_b': 'd39424ba83477114587a320987ad5516fbfee6277fc05fdd2dc1c9fc3059415b',
}

TRIMMED_C_OBJECT_SHA256 = {
    'callback_noops_a': 'c125dea48c318b5af19d3c9ac2897c788ff907ef82122303f93055df03ca2963',
    'callback_noops_b': '8879a28b89af1ee5c783d3b7abb63b7d77de407fe916107170b28e80c9b9ba51',
}



def entries() -> tuple[tuple[str, int], ...]:
    return tuple((f'func_{0x801CB460 + offset - ROM_START:08X}_{offset:X}',offset)
                 for start, n, _ in GROUPS for offset in (start + 12*i for i in range(n)))


def validate_reference(reference: bytes) -> None:
    if len(reference) != 0x2000000 or hashlib.sha1(reference).hexdigest() != ROM_SHA1:
        raise ValueError('USA decompressed reference ROM identity changed')
    for name, offset in entries():
        if reference[offset:offset+12] != ORIGINAL_NOOP:
            raise ValueError('Function is not the verified 12-byte callback: '+name)


def render(name: str, count: int, start: int) -> str:
    header = '/* Exact C bodies of original unused two-argument actor callbacks. */\n'
    return header + '\n'.join(f'void func_{0x801CB460 + start + 12*i - ROM_START:08X}_{start+12*i:X}(void *a0, void *a1) {{}}'
                              for i in range(count)) + '\n'


def objects() -> list[tuple[Path, int]]:
    return [(Path('build/usa') / ('src/'+name+'.c.o' if kind == 'c' else 'asm/usa/'+name+'.s.o'), size)
            for kind, name, _, size in CHUNKS]



def stage_splat(text: str) -> str:
    """Version 2 extension of the already-verified 13-function file_11 Splat split."""
    if text.count(SPLAT_OLD) != 1 or text.count('    - [0x599918, c, character_switch_wrappers]') != 1:
        raise ValueError('Expected pristine 13-function staged Splat layout')
    return text.replace(SPLAT_OLD, SPLAT_NEW)


def checked_source_copies(checkout: Path, research_dir: Path,
                          reference_rom: bytes) -> list[tuple[Path, Path]]:
    """Prevalidate the two new C source copies without mutating checkout."""
    validate_reference(reference_rom)
    sources = []
    for start, count, name in GROUPS:
        original = Path(research_dir)/(name+'.c')
        destination = Path(checkout)/'src'/(name+'.c')
        if not original.is_file() or destination.exists():
            raise ValueError('Missing or colliding callback source: '+name)
        data = original.read_bytes().replace(b'\r\n',b'\n')
        if (sha256(data) != PINNED_SOURCE_SHA256[name] or
                data.decode('utf-8') != render(name,count,start)):
            raise ValueError('Unreviewed callback source bytes: '+name)
        sources.append((original,destination))
    return sources


def object_targets() -> list[str]:
    return [path.as_posix() for path,_ in objects()]


def prepare(checkout: Path, reference: bytes) -> None:
    validate_reference(reference)
    rev = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    if rev != PIN:
        raise ValueError('Not the pinned upstream checkout')
    cfg = checkout/'config/usa/splat.yaml'
    text = cfg.read_text()
    text=stage_splat(text)
    for source,dest in checked_source_copies(checkout,Path(__file__).parent,reference):
        shutil.copyfile(source,dest)
    cfg.write_text(text)


def trim(checkout: Path) -> dict:
    linker=checkout/'.splat/usa/mnsg.ld'
    original=linker.read_text()
    if original.count(LINKER_OLD)!=1: raise ValueError('Unexpected linker SUBALIGN before trim')
    modified=[]
    for path,length in objects():
        full=checkout/path
        result=trim_text_section(full.read_bytes(),length)
        if path.stem[:-2] in TRIMMED_C_OBJECT_SHA256 and sha256(result) != TRIMMED_C_OBJECT_SHA256[path.stem[:-2]]:
            raise ValueError('Original IDO callback object hash changed: ' + str(path))
        modified.append((full,result))
    for full, data in modified:full.write_bytes(data)
    linker.write_text(original.replace(LINKER_OLD,LINKER_NEW))
    return {'trimmed':len(modified)}


def verify(checkout: Path, reference: bytes, baseline_elf: Path) -> dict:
    validate_reference(reference)
    rebuilt=(checkout/'build/usa/mnsg.z64').read_bytes()
    if rebuilt!=reference: raise ValueError('Rebuilt full 32 MiB USA image differs')
    original=ElfInspector(baseline_elf.read_bytes())
    candidate=ElfInspector((checkout/'build/usa/mnsg.elf').read_bytes())
    if original.overlay_info()[1][5]!=candidate.overlay_info()[1][5]: raise ValueError('Overlay size changed')
    original_rel=original.relocations()
    candidate_rel=candidate.relocations()
    if len(original_rel)!=8825 or Counter(original_rel)!=Counter(candidate_rel):
        raise ValueError('Original relocation records differ')
    config=(checkout/'config/usa/splat.yaml').read_text()
    if config.count(SPLAT_NEW)!=1:
        raise ValueError('Staged callback Splat ownership missing or changed')
    linker=(checkout/'.splat/usa/mnsg.ld').read_text()
    if linker.count(LINKER_NEW)!=1:
        raise ValueError('Pinned linker file_11 SUBALIGN(4) missing')
    linked_map=(checkout/'build/usa/mnsg.map').read_text()
    match=re.search(r'(?m)^\.file_11\s+0x([0-9A-Fa-f]+)\s+0x([0-9A-Fa-f]+)',linked_map)
    if not match or (int(match.group(1),16),int(match.group(2),16)) != (VMA_START,0x41400):
        raise ValueError('Wrong linked file_11 text+data section extent')
    end=re.search(r'(?m)^\.file_11_bss(?:\s|$)', linked_map[match.end():])
    if not end: raise ValueError('No file_11 BSS boundary')
    block=linked_map[match.end():match.end()+end.start()]
    positions=[]
    for (kind,name,rom,size),(path,_) in zip(CHUNKS,objects()):
        target=path.as_posix()
        label=target+'(.text)'
        hits=list(re.finditer(r'(?m)^\s*'+re.escape(label)+r'\s*$',block))
        expected_vma=VMA_START+rom-ROM_START
        extent=re.search(r'(?m)^\s*\.text\s+0x([0-9A-Fa-f]+)\s+0x([0-9A-Fa-f]+)\s+'+re.escape(target)+r'\s*$',block)
        if (len(hits)!=1 or extent is None or
                (int(extent.group(1),16),int(extent.group(2),16)) != (expected_vma,size)):
            raise ValueError('file_11 linked source ownership/extent mismatch: '+target)
        positions.append(hits[0].start())
    if positions != sorted(positions):
        raise ValueError('file_11 callback group objects reordered')
    for start,count,name in GROUPS:
        source=(checkout/'src'/(name+'.c')).read_text()
        if source != render(name,count,start):
            raise ValueError('Callback C source does not match the tested implementation')
        native_object=(checkout/'build/usa/src'/(name+'.c.o')).read_bytes()
        if sha256(native_object) != TRIMMED_C_OBJECT_SHA256[name]:
            raise ValueError('Callback object differs from verified original IDO output')
    symbols=candidate.symbols();section=candidate.overlay_info()[0]
    for name,offset in entries():
        vma=VMA_START+offset-ROM_START
        occurrences=[row for row in symbols if row[0]==name and row[1]==vma and row[2]==12 and row[4]==section and (row[3]&15)==2]
        if len(occurrences)!=1 or rebuilt[offset:offset+12]!=ORIGINAL_NOOP:
            raise ValueError('Missing original C-owned function: '+name)
    # The same expanded candidate must retain all thirteen prior matching-C
    # character-switch functions, not only the additional empty callbacks.
    for name, rom, size, original_hash in SWITCH_FUNCTIONS:
        address = VMA_START + rom - ROM_START
        matches = [row for row in symbols if row[0] == name and row[1] == address and
                   row[2] == size and row[4] == section and (row[3] & 15) == 2]
        if len(matches) != 1 or sha256(rebuilt[rom:rom + size]) != original_hash:
            raise ValueError('Previously verified character-switch C function changed: ' + name)
    for source_name, target_name, expected_source, expected_object in SWITCH_SOURCE_SPECS:
        source = checkout/'src'/(target_name+'.c')
        obj = checkout/'build/usa/src'/(target_name+'.c.o')
        if (sha256(source.read_bytes().replace(b'\r\n', b'\n')) != expected_source or
                sha256(obj.read_bytes()) != expected_object):
            raise ValueError('Original character-switch C object changed: ' + target_name)
    return {'original_address_c_functions':len(entries()),'original_address_c_bytes':12*len(entries()),
            'total_overlay_c_functions':len(entries())+len(SWITCH_FUNCTIONS),
            'total_overlay_c_bytes':12*len(entries())+sum(x[2] for x in SWITCH_FUNCTIONS),
            'ordered_linker_objects':len(positions),
            'rom_bytes':len(rebuilt),'rom_sha1':hashlib.sha1(rebuilt).hexdigest(),
            'relocations':len(original_rel),'relocations_same_order':original_rel==candidate_rel,
            'linked_elf_sha256':sha256((checkout/'build/usa/mnsg.elf').read_bytes())}


def main(argv=None) -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--checkout',type=Path,required=True)
    parser.add_argument('--baseline-elf',type=Path)
    parser.add_argument('--phase',choices=('prepare','trim','verify'),required=True)
    opts=parser.parse_args(argv)
    base=opts.checkout.resolve()
    reference=(base/'config/usa/baserom.decompressed.z64').read_bytes()
    if opts.phase=='prepare':prepare(base,reference)
    elif opts.phase=='trim':print(trim(base))
    else:
        if opts.baseline_elf is None: raise ValueError('--baseline-elf required')
        print(verify(base,reference,opts.baseline_elf))

if __name__=='__main__': main()
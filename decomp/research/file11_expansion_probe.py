"""Read-only discovery and original-IDO proof for USA file_11 callback families.

The authenticated original ROM and baseline ELF are user-supplied inputs; no
binary, game asset, raw disassembly or toolchain is generated in the repo.
Only original-VMA native codegen matches are reported. This does *not* certify
the linked mixed-C/ASM overlay, complete-ROM G2 or production matching-C claims.

Example (in the pinned Linux environment):

    python3 -m decomp.research.file11_expansion_probe \\
      --rom /path/to/baserom.decompressed.z64 --elf /path/to/baseline/mnsg.elf \\
      --cc /path/to/ido-5.3/cc --ld /path/to/mips-linux-gnu-ld \\
      --objcopy /path/to/mips-linux-gnu-objcopy \\
      --report /tmp/file11-expansion-native-probe.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

from decomp.overlay_file11 import (
    ElfInspector, FUNCTIONS as PROMOTED_CHARACTER_FUNCTIONS,
    ROM_SHA1, ROM_START, TEXT_END, VMA_START,
)
from decomp.research.usa_file11_noop_groups import (
    ORIGINAL_NOOP, entries as PROMOTED_NOOP_ENTRIES,
)

PINNED_BASELINE_ELF_SHA256 = '83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038'
ROM_LENGTH = 0x2000000
DIRECT_CALL_SIZE = 32
FLOAT_RESET_NAMES = (
    ('func_801E2FE0_59EEF0', 0x59EEF0),
    ('func_801E2FF4_59EF04', 0x59EF04),
)
FLOAT_RESET_SOURCE = (
    'typedef struct { unsigned char pad[0xE4]; float x, y; } Actor;\n'
    'void func_801E2FE0_59EEF0(Actor *a) { a->x = 0.0f; a->y = 0.0f; }\n'
    'void func_801E2FF4_59EF04(Actor *a) { a->x = 0.0f; a->y = 0.0f; }\n'
)
# A typical nonleaf actor callback (8 words): stack adjustment, save $ra,
# JAL, optional single delay-slot argument instruction, restore and return.
PREFIX = (0x27BDFFE8, 0xAFBF0014)
SUFFIX = (0x8FBF0014, 0x27BD0018, 0x03E00008, 0)
PROMOTED_WRAPPERS = {
    name for name, _, size, _ in PROMOTED_CHARACTER_FUNCTIONS if size == 32
}
PROMOTED_NOOPS = {name for name, _ in PROMOTED_NOOP_ENTRIES()}


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def checked_inputs(rom: bytes, baseline_elf: bytes) -> ElfInspector:
    if len(rom) != ROM_LENGTH or hashlib.sha1(rom).hexdigest() != ROM_SHA1:
        raise ValueError('Wrong authentic USA 32 MiB decompressed ROM')
    if sha256(baseline_elf) != PINNED_BASELINE_ELF_SHA256:
        raise ValueError('Wrong original linked ELF; do not use a reconstructed candidate')
    return ElfInspector(baseline_elf)


def identify_direct_wrapper(data: bytes):
    """Identify the complete exact 8-word shape; infer only observed arguments."""
    if len(data) != DIRECT_CALL_SIZE:
        return None
    words = struct.unpack('>8I', data)
    if (words[:2] != PREFIX or words[4:] != SUFFIX or words[2] >> 26 != 3):
        return None
    delay = words[3]
    target = 0x80000000 | ((words[2] & 0x3FFFFFF) << 2)
    if delay == 0xAFA5001C:
        mode = 'two_arg'
    elif delay == 0:
        mode = 'one_arg'
    elif (delay & 0xFFFF0000) == 0x24050000:
        mode = 'constant_arg'
    elif delay == 0x00002025:
        mode = 'null_arg'
    else:
        return None
    return {'target_vma': target, 'mode': mode,
            'constant': (delay & 0xFFFF) if mode == 'constant_arg' else None}


def discover(rom: bytes, elf: ElfInspector):
    """Use positive-size original ELF FUNC ownership, not blind byte matching."""
    wrappers, noops = [], []
    visited = set()
    for name, vma, size, info, section in elf.symbols():
        offset = ROM_START + vma - VMA_START
        if (not name.startswith('func_') or not (info & 15) == 2 or
                not ROM_START <= offset < TEXT_END or
                offset + size > TEXT_END or name in visited):
            continue
        visited.add(name)
        if size == DIRECT_CALL_SIZE and name not in PROMOTED_WRAPPERS:
            pattern = identify_direct_wrapper(rom[offset:offset + size])
            if pattern:
                wrappers.append(dict(name=name, rom_offset=offset, vma=vma,
                                     size=size, original_sha256=sha256(rom[offset:offset + size]), **pattern))
        if (size == 12 and name not in PROMOTED_NOOPS and
                rom[offset:offset + size] == ORIGINAL_NOOP):
            noops.append(dict(name=name, rom_offset=offset, vma=vma, size=size,
                              original_sha256=sha256(rom[offset:offset + size])))
    wrappers.sort(key=lambda x: x['rom_offset'])
    noops.sort(key=lambda x: x['rom_offset'])
    if len({e['rom_offset'] for e in wrappers + noops}) != len(wrappers) + len(noops):
        raise ValueError('Overlapping callback candidates')
    return wrappers, noops


def render_wrapper(entry):
    name = entry['name']
    mode = entry['mode']
    if mode == 'two_arg':
        args = 'void *actor, unsigned int unused'
        decl, expr = 'extern void handler(void *);', 'handler(actor);'
    elif mode == 'one_arg':
        args = 'void *actor'
        decl, expr = 'extern void handler(void *);', 'handler(actor);'
    elif mode == 'constant_arg':
        args = 'void *actor'
        decl = 'extern void handler(void *, unsigned int);'
        expr = f'handler(actor, {entry["constant"]});'
    elif mode == 'null_arg':
        # Zero incoming arguments: otherwise IDO spills the (unused) $a0
        # and emits a different 48-byte wrapper, not the original 32 bytes.
        args = 'void'
        decl, expr = 'extern void handler(void *);', 'handler((void *)0);'
    else:
        raise ValueError('Unsupported native wrapper mode')
    return f'{decl}\nvoid {name}({args}) {{ {expr} }}\n'


def render_noop(entry):
    return f'void {entry["name"]}(void *a0, void *a1) {{}}\n'


def native_probe(source: str, vma: int, symbols: dict, cc: Path, ld: Path,
                 objcopy: Path, work: Path, expected: bytes, env: dict):
    src, obj, exe, binary, script = [work / name for name in
                                   ('source.c', 'candidate.o', 'candidate.elf', 'candidate.bin', 'link.ld')]
    src.write_text(source, encoding='utf-8', newline='\n')
    decls = '\n'.join(f'{name} = 0x{addr:08X};' for name, addr in symbols.items())
    script.write_text('OUTPUT_ARCH(mips)\n' + decls + '\n'
                      + f'SECTIONS {{ . = 0x{vma:08X}; .text : {{ *(.text) }} '
                        '/DISCARD/ : { *(.comment) *(.note*) } }\n')
    commands = [
        [str(cc), '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm',
         '-O2', '-mips2', '-c', '-o', str(obj), str(src)],
        [str(ld), '-T', str(script), '--no-check-sections', '-o', str(exe), str(obj)],
        [str(objcopy), '-j', '.text', '-O', 'binary', str(exe), str(binary)],
    ]
    for command in commands:
        subprocess.run(command, check=True, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    compiled = binary.read_bytes()
    # IDO pads the *final* .text section to 16 bytes. Size-lock to the original
    # function extent; padding after it is not part of the original function.
    if len(compiled) < len(expected):
        raise ValueError('Native compiler emitted fewer bytes than original')
    original_code = compiled[:len(expected)]
    return {'exact': original_code == expected,
            'candidate_size': len(compiled),
            'matching_instruction_words': sum(
                expected[i:i + 4] == original_code[i:i + 4]
                for i in range(0, len(expected), 4)),
            'candidate_sha256': sha256(original_code)}


def verify(rom: bytes, elf: ElfInspector, cc: Path, ld: Path,
           objcopy: Path, env=None):
    env = dict(os.environ if env is None else env)
    wrappers, noops = discover(rom, elf)
    proof = []
    with tempfile.TemporaryDirectory(prefix='goemon-file11-expand-') as directory:
        work = Path(directory)
        for entry in wrappers:
            found = native_probe(render_wrapper(entry), entry['vma'],
                                 {'handler': entry['target_vma']}, cc, ld,
                                 objcopy, work,
                                 rom[entry['rom_offset']:entry['rom_offset']+32], env)
            proof.append(dict(**entry, **found, category='direct_call_wrapper'))
        for entry in noops:
            found = native_probe(render_noop(entry), entry['vma'], {}, cc, ld,
                                 objcopy, work,
                                 rom[entry['rom_offset']:entry['rom_offset']+12], env)
            proof.append(dict(**entry, **found, category='empty_callback'))
        reset_offset = FLOAT_RESET_NAMES[0][1]
        reset_vma = VMA_START + reset_offset - ROM_START
        expected = rom[reset_offset:reset_offset + 40]
        found = native_probe(FLOAT_RESET_SOURCE, reset_vma, {}, cc, ld,
                             objcopy, work, expected, env)
        # Two 20-byte functions are contiguous. Verify both independently.
        for i, (name, offset) in enumerate(FLOAT_RESET_NAMES):
            if not any(x[0] == name and x[1] == reset_vma + 20*i and x[2] == 20 and (x[3]&15)==2
                       for x in elf.symbols()):
                raise ValueError('Expected original 20-byte actor reset FUNC symbol missing')
            proof.append({'name': name, 'rom_offset': offset,
                          'vma': reset_vma + 20*i, 'size': 20,
                          'original_sha256': sha256(rom[offset:offset + 20]),
                          'category': 'actor_float_reset',
                          'exact': found['exact'] and
                                   found['candidate_sha256'] == sha256(expected),
                          'matching_instruction_words': 5 if found['exact'] else 0})
    proof.sort(key=lambda x: x['rom_offset'])
    counts = Counter(item['category'] for item in proof)
    exact = [p for p in proof if p['exact']]
    return {
        'format': 'goemon-file11-expansion-native-ido-research-v1',
        'original_rom_sha1': ROM_SHA1,
        'original_baseline_elf_sha256': PINNED_BASELINE_ELF_SHA256,
        'compiler': 'original IDO 5.3 -O2 -mips2 -G0',
        'original_vma_checks': len(proof),
        'exact_matching_functions': len(exact),
        'exact_matching_bytes': sum(p['size'] for p in exact),
        'categories': dict(counts),
        'wrapper_modes': dict(Counter(p['mode'] for p in proof if p['category']=='direct_call_wrapper')),
        'failed': [p['name'] for p in proof if not p['exact']],
        'functions': proof,
        'official_promotion': False,
        'limitations': 'isolated original-address IDO comparisons, not full-ROM G2/inventory or in-game verification',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('rom', 'elf', 'cc', 'ld', 'objcopy', 'report'):
        parser.add_argument('--' + flag, type=Path, required=True)
    args = parser.parse_args(argv)
    rom = args.rom.read_bytes()
    elf_bytes = args.elf.read_bytes()
    elf = checked_inputs(rom, elf_bytes)
    result = verify(rom, elf, args.cc, args.ld, args.objcopy)
    if result['failed']:
        raise ValueError('Failed isolated original-ROM IDO match: ' + ', '.join(result['failed']))
    # Never silently overwrite native research evidence.
    with args.report.open('x', encoding='utf-8') as report:
        json.dump(result, report, indent=2)
        report.write('\n')
    print(f"Exact native functions: {result['exact_matching_functions']}/"
          f"{result['original_vma_checks']}, bytes: {result['exact_matching_bytes']}")


if __name__ == '__main__':
    main()

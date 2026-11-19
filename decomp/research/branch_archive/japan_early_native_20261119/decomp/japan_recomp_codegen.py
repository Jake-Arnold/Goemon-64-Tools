"""Prepare auditable Japanese N64Recomp *candidate* inputs from an exact linked ELF.

This is not a native PC executable. Original N64 ROM bytes remain outside output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

SOURCE_COMMIT = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
JAPAN_SHA1 = '6f8745fecc3a5e7d4918c7a73353eb0726116ded'
MAIN_ENTRY_VMA = 0x80000400
ROM_SIZE = 0x2000000
CODE_SECTIONS = re.compile(r'\.(?:entry|main|file_\d+)\Z')
SECTION_LINE = re.compile(
    r'^\s*\d+\s+(\.\S+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+'
    r'([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+2\*\*\d+\s*$'
)
OVERLAY_NAMES = tuple(f'.file_{n}' for n in range(24, 81))


def parse_sections(output: str) -> dict[str, dict[str, int]]:
    """GNU MIPS objdump -h output; use ROM physical LMA, not ELF file offset."""
    lines = output.splitlines()
    sections = {}
    for i, line in enumerate(lines):
        found = SECTION_LINE.match(line)
        if not found or not CODE_SECTIONS.fullmatch(found[1]):
            continue
        name, size, vma, lma, filepos = found.groups()
        if i + 1 >= len(lines) or not re.search(r'\bCODE\b', lines[i+1]):
            continue  # Non-executable .file_1/.file_2/etc. remain data only.
        if name in sections:
            raise ValueError(f'Duplicate ELF section: {name}')
        section = {'rom': int(lma, 16), 'vram': int(vma, 16), 'size': int(size, 16)}
        if (section['rom'] < 0x1000 or section['rom'] + section['size'] > ROM_SIZE or
            section['size'] < 4 or any(x % 4 for x in section.values())):
            raise ValueError(f'Invalid original Japanese code section {name}: {section}')
        sections[name] = section
    if '.main' not in sections or '.entry' not in sections:
        raise ValueError('Japanese original ELF is missing entry/main code')
    if sections['.entry']['vram'] != MAIN_ENTRY_VMA:
        raise ValueError('Wrong Japanese program entrypoint')
    ranges = sorted((v['rom'], v['rom'] + v['size'], k) for k, v in sections.items())
    for previous, current in zip(ranges, ranges[1:]):
        if previous[1] > current[0]:
            raise ValueError(f'Overlapping Japanese ROM section ranges: {previous[2]} and {current[2]}')
    missing = set(OVERLAY_NAMES) - sections.keys()
    if missing:
        raise ValueError(f'Missing Japanese recompiler overlay: {sorted(missing)[:5]}')
    return sections


def parse_functions(output: str, sections: dict[str, dict[str, int]]) -> dict[str, list[dict]]:
    functions = {name: [] for name in sections}
    all_names = set()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) != 6 or parts[2] != 'F' or parts[3] not in sections:
            continue
        address, _binding, _kind, section_name, size, name = parts
        if not re.fullmatch('[0-9A-Fa-f]+', address) or not re.fullmatch('[0-9A-Fa-f]+', size):
            raise ValueError('Invalid MIPS function symbol address/size')
        vma, size = int(address, 16), int(size, 16)
        if not size:
            continue
        spec = sections[section_name]
        if name in all_names or vma % 4 or size % 4 or vma < spec['vram'] or vma + size > spec['vram'] + spec['size']:
            raise ValueError(f'Invalid, duplicate or outside Japanese function {name}')
        if not re.fullmatch('[A-Za-z_.$][A-Za-z0-9_.$]*', name):
            raise ValueError(f'Unsafe Japanese function symbol {name}')
        all_names.add(name)
        functions[section_name].append({'name': name, 'vram': vma, 'size': size})
    for section_name, rows in functions.items():
        rows.sort(key=lambda v: (v['vram'], v['name']))
        if not rows:
            raise ValueError(f'No original functions found in code section {section_name}')
        for prev, current in zip(rows, rows[1:]):
            if prev['vram'] + prev['size'] > current['vram']:
                raise ValueError(f'Overlapping Japanese function symbols in {section_name}')
    entry = functions['.entry']
    if len(entry) != 1 or entry[0]['vram'] != MAIN_ENTRY_VMA or entry[0]['name'] != 'func_80000400_1000':
        raise ValueError('Missing unique boot entry function in .entry')
    return functions


def render_symbol_table(sections: dict, functions: dict) -> str:
    lines = ['# Generated Japanese rev0 N64Recomp candidate symbols; NOT a bootable PC port.',
             '# Source is the exact original-address linked Japanese N64 ELF.', '']
    for name, spec in sections.items():
        lines.extend(('[[section]]', f'name = "{name}"', f'rom = 0x{spec["rom"]:08X}',
                      f'vram = 0x{spec["vram"]:08X}', f'size = 0x{spec["size"]:X}', '', 'functions = ['))
        for fn in functions[name]:
            identifier = ('recomp_entrypoint' if name == '.entry' else fn['name'])
            lines.append(f'    {{ name = "{identifier}", vram = 0x{fn["vram"]:08X}, size = 0x{fn["size"]:X} }},')
        lines.extend((']', ''))
    return '\n'.join(lines)


def render_codegen_config() -> str:
    return ('# Japanese rev0 preliminary N64Recomp code generation input.\n'
            '# Do NOT register a Japanese GameEntry against USA functions.\n'
            '[input]\nentrypoint = 0x80000400\n'
            'output_func_path = "RecompiledFuncsJapan"\n'
            'relocatable_sections_path = "mnsg.japan_0.overlays.txt"\n'
            'symbols_file_path = "mnsg.japan_0.syms.toml"\n'
            'rom_file_path = "mnsg.japan_0.z64"\n'
            'trace_mode = true\nbss_section_suffix = "_bss"\n\n'
            '[patches]\nstubs = []\nignored = []\n')


def assemble(elf_sections: str, elf_symbols: str) -> tuple[dict[str, str], dict]:
    sections = parse_sections(elf_sections)
    functions = parse_functions(elf_symbols, sections)
    texts = {'mnsg.japan_0.syms.toml': render_symbol_table(sections, functions),
             'mnsg.japan_0.overlays.txt': '\n'.join(OVERLAY_NAMES) + '\n',
             'mnsg.japan_0.toml': render_codegen_config()}
    count = sum(len(v) for v in functions.values())
    digest = hashlib.sha256(texts['mnsg.japan_0.syms.toml'].encode()).hexdigest()
    report = {'format': 'goemon-japan-n64recomp-preparation-v1',
              'region': 'japan_0', 'status': 'PREPARED_NOT_EXECUTED',
              'source_upstream_commit': SOURCE_COMMIT,
              'decompressed_rom_sha1': JAPAN_SHA1,
              'function_symbols': count, 'sections': len(sections),
              'overlay_sections': len(OVERLAY_NAMES),
              'entrypoint': f'0x{MAIN_ENTRY_VMA:08X}',
              'symbol_table_sha256': digest,
              'missing': ['N64Recomp execution against generated symbols',
                          'Japanese overlays/patches linkage', 'Japanese GameEntry registration',
                          'Japanese native renderer/audio/gameplay test'],
              'notes': ['Symbols originate from original-address ELF, not from USA guesses.',
                        'The Japanese symbols are a candidate input; N64Recomp may reject or require more patch symbols.',
                        'No USA instruction patches copied into Japanese configuration.']}
    return texts, report


def prepare(checkout: Path, output_dir: Path, objdump: str = 'mips-linux-gnu-objdump') -> dict:
    checkout = checkout.resolve(strict=True)
    output_dir = output_dir.resolve()
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError('Output directory already exists; refusing overwrite')
    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout, text=True).strip() != SOURCE_COMMIT:
        raise ValueError('Unexpected mnsg checkout revision')
    if subprocess.run(['git', 'diff', '--quiet'], cwd=checkout).returncode:
        raise ValueError('Pinned upstream checkout contains tracked modifications')
    expanded = checkout / 'build/japan_0/mnsg.z64'
    reference = checkout / 'config/japan_0/baserom.decompressed.z64'
    for image in (expanded, reference):
        data = image.read_bytes()
        if len(data) != ROM_SIZE or hashlib.sha1(data).hexdigest() != JAPAN_SHA1:
            raise ValueError(f'Wrong linked or original Japanese image: {image.name}')
    if expanded.read_bytes() != reference.read_bytes():
        raise ValueError('Japanese linked ROM differs from original')
    elf = checkout / 'build/japan_0/mnsg.elf'
    if not elf.is_file():
        raise ValueError('Missing original-address Japanese MIPS ELF')
    headers = subprocess.check_output([objdump, '-h', str(elf)], text=True)
    symbol_text = subprocess.check_output([objdump, '-t', str(elf)], text=True)
    files, report = assemble(headers, symbol_text)
    output_dir.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        (output_dir / name).write_text(data, encoding='utf-8')
    (output_dir / 'proof.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--objdump', default='mips-linux-gnu-objdump')
    args = parser.parse_args(argv)
    print(json.dumps(prepare(args.checkout, args.output_dir, args.objdump), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

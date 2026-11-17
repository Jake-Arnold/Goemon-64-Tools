"""Reconcile Splat-bounded Japanese JAL anchors against real USA N64Recomp symbols.

Full structural equality is deliberately weaker than behavioural compatibility:
MIPS immediates, branches and J/JAL targets differ between releases.
The output is NOT a Japanese N64Recomp symbols TOML and contains no ROM data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from decomp.japan_function_map import (
    SHA1, SIGNATURE_WORDS, _informative, _signature,
    japan_signature_index, normalized_instruction, read_verified_rom,
)
from decomp.japan_overlay_map import original_symbols, splat_text_sections

CANDIDATE_FORMAT = 'goemon-japan-overlay-direct-jal-anchors-v1'
FORMAT = 'goemon-japan-symbol-reconciliation-v1'


def _integer_hex(s: str) -> int:
    if not isinstance(s, str) or not s.startswith('0x'):
        raise ValueError('Expected a 0x-prefixed hexadecimal address')
    return int(s, 16)


def reconcile(usa: bytes, japan: bytes, usa_splat: Path, japan_splat: Path,
              original_syms: Path, candidates: dict) -> dict:
    if not isinstance(candidates, dict) or candidates.get('format') != CANDIDATE_FORMAT:
        raise ValueError('Unknown JAL candidate report format')
    if candidates.get('sha1') != SHA1 or candidates.get('signature_words') != SIGNATURE_WORDS:
        raise ValueError('JAL candidate report has incompatible ROM hashes/signature length')
    us_sections = splat_text_sections(usa_splat, 'usa')
    jp_sections = splat_text_sections(japan_splat, 'japan_0')
    symbols = original_symbols(original_syms)
    by_section: dict[str, list[dict]] = defaultdict(list)
    for row in candidates.get('mappings', []):
        section = row.get('section')
        if not isinstance(section, str) or section not in us_sections or section not in jp_sections:
            raise ValueError('JAL candidate references unknown executable section')
        by_section[section].append(row)
    report = []
    section_reports = []
    totals: Counter = Counter()
    for name, section in us_sections.items():
        if name not in jp_sections or name not in symbols:
            continue
        jp_section = jp_sections[name]
        sym_section, entries = symbols[name]
        if (sym_section.get('rom'), sym_section.get('vram')) != (section.rom, section.vram):
            raise ValueError(f'USA symbol table disagrees with Splat for {name}')
        us_words, jp_words = section.words(usa), jp_section.words(japan)
        jp_index = japan_signature_index(jp_words)
        named = {}
        for f in entries:
            vram, size, fn_name = f.get('vram'), f.get('size'), f.get('name')
            if type(vram) is not int or type(size) is not int or not isinstance(fn_name, str):
                raise ValueError(f'Invalid USA symbol in {name}')
            if vram % 4 or size <= 0 or size % 4:
                raise ValueError(f'Unaligned USA symbol in {name}')
            if vram in named:
                raise ValueError(f'Duplicate original USA symbol at {vram:X} in {name}')
            named[vram] = f
        summary: Counter = Counter(original_symbol_count=len(named))
        seen_usa, seen_jp = set(), set()
        for row in by_section[name]:
            usa_addr, jp_addr = _integer_hex(row.get('usa_vram')), _integer_hex(row.get('japan_vram'))
            usa_rom, jp_rom = _integer_hex(row.get('usa_rom')), _integer_hex(row.get('japan_rom'))
            if usa_addr in seen_usa or jp_addr in seen_jp:
                raise ValueError(f'Duplicate candidate source or destination in {name}')
            seen_usa.add(usa_addr)
            seen_jp.add(jp_addr)
            if ((usa_addr - section.vram) % 4 or (jp_addr - jp_section.vram) % 4
                    or (usa_addr - section.vram) + section.rom != usa_rom
                    or (jp_addr - jp_section.vram) + jp_section.rom != jp_rom):
                raise ValueError(f'Candidate ROM/VRAM identity mismatch in {name}')
            us_pos = (usa_addr - section.vram) // 4
            jp_pos = (jp_addr - jp_section.vram) // 4
            if (us_pos < 0 or jp_pos < 0 or us_pos + SIGNATURE_WORDS > len(us_words)
                    or jp_pos + SIGNATURE_WORDS > len(jp_words)):
                raise ValueError(f'Candidate outside executable bounds in {name}')
            signature = _signature(us_words, us_pos)
            if not _informative(signature) or jp_index.get(signature) != [jp_pos]:
                raise ValueError(f'Unverified or non-unique candidate anchor in {name}')
            summary['verified_jal_anchors'] += 1
            f = named.get(usa_addr)
            if f is None:
                summary['not_a_named_usa_function_start'] += 1
                continue
            size_words = f['size'] // 4
            if us_pos + size_words > len(us_words):
                summary['usa_function_outside_code'] += 1
                continue
            if size_words < SIGNATURE_WORDS:
                summary['too_short_for_full_validation'] += 1
                continue
            if jp_pos + size_words > len(jp_words):
                summary['japanese_function_outside_code'] += 1
                continue
            a, b = us_words[us_pos:us_pos + size_words], jp_words[jp_pos:jp_pos + size_words]
            if any(normalized_instruction(x) != normalized_instruction(y) for x, y in zip(a, b)):
                summary['full_structure_mismatch'] += 1
                continue
            exact = sum(x == y for x, y in zip(a, b))
            summary['full_structure_match'] += 1
            summary['full_structure_bytes'] += f['size']
            summary['exact_instruction_words'] += exact
            if exact == size_words:
                summary['byte_identical_functions'] += 1
            report.append({
                'section': name,
                'usa_symbol': f['name'],
                'usa_vram': f'0x{usa_addr:08X}',
                'japan_vram': f'0x{jp_addr:08X}',
                'usa_rom': f'0x{usa_rom:X}',
                'japan_rom': f'0x{jp_rom:X}',
                'size_bytes': f['size'],
                'instruction_words': size_words,
                'exact_instruction_words': exact,
                'classification': 'full_normalized_mips_structure_only',
            })
        summary['symbols_without_jal_anchor'] = len(named) - sum(v in named for v in seen_usa)
        totals.update(summary)
        section_reports.append({'name': name, 'counts': dict(summary)})
    # Ensure every externally supplied JAL entry was checked against a section.
    unchecked = set(by_section).difference({x['name'] for x in section_reports})
    if unchecked:
        raise ValueError(f'Candidate sections lack original USA symbol metadata: {sorted(unchecked)}')
    return {
        'format': FORMAT,
        'sha1': dict(SHA1),
        'source_candidate_format': CANDIDATE_FORMAT,
        'classification_notes': [
            'A unique 16-instruction JAL anchor with complete matching code shape is not runtime equivalence.',
            'I-format immediate values, branch offsets, and J/JAL targets are deliberately masked.',
            'Functions shorter than 16 instructions are excluded, even if candidate anchors overlap following functions.',
            'Names and sizes come from original USA N64Recomp symbols; Japanese function sizes are not independently verified.',
            'Do NOT feed this incomplete list to N64Recomp as a Japanese symbol configuration.',
        ],
        'totals': dict(totals),
        'sections': section_reports,
        'matches': sorted(report, key=lambda x: (x['section'], int(x['usa_vram'], 16))),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('usa_decompressed', type=Path)
    parser.add_argument('japan_decompressed', type=Path)
    parser.add_argument('--us-splat', required=True, type=Path)
    parser.add_argument('--jp-splat', required=True, type=Path)
    parser.add_argument('--us-symbols', required=True, type=Path)
    parser.add_argument('--jal-candidates', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    report = reconcile(
        read_verified_rom(args.usa_decompressed, 'usa'),
        read_verified_rom(args.japan_decompressed, 'japan_0'),
        args.us_splat, args.jp_splat, args.us_symbols,
        json.loads(args.jal_candidates.read_text(encoding='utf-8')),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(report['totals'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Conservative, read-only cross-region MIPS address-context comparison.

A matched code pattern supports a regional *word* correspondence only. Neither
matching instructions nor a GameShark repeat cheat establishes a byte's named
item identity, bit mask, or acquired value. Never emit ROM instructions/bytes.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import struct

OPS = {0x20: 'lb', 0x21: 'lh', 0x23: 'lw', 0x24: 'lbu',
       0x25: 'lhu', 0x27: 'lwu', 0x28: 'sb', 0x29: 'sh',
       0x2B: 'sw', 0x31: 'lwc1', 0x39: 'swc1'}
STORES = {0x28, 0x29, 0x2B, 0x39}
BRANCHES = {1, 2, 3, 4, 5, 6, 7, 0x14, 0x15, 0x16, 0x17}


def _signed16(value):
    value &= 0xFFFF
    return value if value < 0x8000 else value - 0x10000


def _word(data, offset):
    return struct.unpack_from('>I', data, offset)[0]


def tracked_word_refs(data: bytes, targets, window: int = 64):
    """Track known LUI-based register constants along a straight-line window.

    Stops after a branch or jump delay slot; does not follow control flow,
    pointers in memory, dynamic indexing, or indirect register values. It
    invalidates registers when a load or unhandled arithmetic overwrites them.
    The scanned image is not guaranteed to contain only executable code.
    """
    if len(data) % 4:
        raise ValueError('Instruction scan needs a word-aligned image')
    if not 1 <= window <= 128:
        raise ValueError('Window must be 1-128 instructions')
    targets = frozenset(targets)
    highs = {((address + 0x8000) >> 16) & 0xFFFF for address in targets}
    highs |= {(address >> 16) & 0xFFFF for address in targets}
    matches = defaultdict(dict)
    end = len(data) - 3
    for i in range(0, end, 4):
        instruction = _word(data, i)
        if (instruction >> 26) != 0x0F:
            continue
        reg = (instruction >> 16) & 31
        hi = instruction & 0xFFFF
        if reg == 0 or hi not in highs:
            continue
        known = {0: 0, reg: hi << 16}
        delay_done = False
        for j in range(i + 4, min(i + 4 * (window + 1), end), 4):
            word = _word(data, j)
            op, rs, rt, rd = word >> 26, (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
            funct, imm = word & 63, word & 0xFFFF
            branch = op in BRANCHES or (op == 0 and funct in (8, 9))
            if op in OPS and rs in known:
                address = (known[rs] + _signed16(imm)) & 0xFFFFFFFF
                if address in targets:
                    matches[address][(j, OPS[op])] = {
                        'rom_offset': f'0x{j:08X}', 'operation': OPS[op]}
            dest, value = None, None
            if op == 0x0F:
                dest, value = rt, imm << 16
            elif op in (8, 9, 24, 25):
                dest = rt
                if rs in known:
                    value = (known[rs] + _signed16(imm)) & 0xFFFFFFFF
            elif op == 13:
                dest = rt
                if rs in known:
                    value = known[rs] | imm
            elif op == 12:
                dest = rt
                if rs in known:
                    value = known[rs] & imm
            elif op == 14:
                dest = rt
                if rs in known:
                    value = known[rs] ^ imm
            elif op == 0:
                if funct in (0x21, 0x2D, 0x25):
                    dest = rd
                    if rs in known and rt in known:
                        value = ((known[rs] + known[rt]) if funct in (0x21, 0x2D)
                                 else (known[rs] | known[rt])) & 0xFFFFFFFF
                elif funct in (0, 2, 3):
                    dest = rd
                    if funct == 0 and rt in known:
                        value = known[rt] << ((word >> 6) & 31) & 0xFFFFFFFF
                elif funct == 9:
                    dest = rd or 31
                elif funct not in (8, 0x0C, 0x0D):
                    dest = rd
            elif op in OPS:
                if op not in STORES:
                    dest = rt
            elif op in (0x0A, 0x0B, 0x1A, 0x1B):
                dest = rt
            elif op == 3:
                dest = 31
            if dest is not None and dest != 0:
                if value is None:
                    known.pop(dest, None)
                else:
                    known[dest] = value
            if delay_done:
                break
            if branch:
                delay_done = True
            if len(known) == 1:
                break
    return {address: list(entries.values()) for address, entries in matches.items()}


def _shape(word):
    """Instruction registers/opcode, masking literal immediates and targets."""
    op = word >> 26
    if op == 0:
        return word
    if op in (2, 3):
        return word & 0xFC000000
    if op in (16, 17, 18, 19):
        return word  # COP instructions include function bits in low fields
    return word & 0xFFFF0000


def _context(data, offset, radius):
    if offset < radius * 4 or offset + (radius + 1) * 4 > len(data):
        return None
    return tuple(_shape(_word(data, offset + i * 4))
                 for i in range(-radius, radius + 1))


def best_context_pair(usa, japan, usa_refs, japan_refs, radius=5):
    """Return paired site offsets and matching shape counts, never raw bytes."""
    if not 1 <= radius <= 12:
        raise ValueError('Radius must be 1-12 instructions')
    best = None
    for left in usa_refs:
        offset_a = int(left['rom_offset'], 16)
        signature_a = _context(usa, offset_a, radius)
        if signature_a is None:
            continue
        for right in japan_refs:
            if left['operation'] != right['operation']:
                continue
            offset_b = int(right['rom_offset'], 16)
            signature_b = _context(japan, offset_b, radius)
            if signature_b is None:
                continue
            count = sum(a == b for a, b in zip(signature_a, signature_b))
            if best is None or count > best['matching_instructions']:
                best = {
                    'matching_instructions': count,
                    'window_instructions': 2 * radius + 1,
                    'operation': left['operation'],
                    'usa_rom_offset': left['rom_offset'],
                    'japan_rom_offset': right['rom_offset'],
                }
    return best


def compare_contexts(usa, japan, rows, *, window=64, radius=5):
    """Compare [(slug, USA guest byte, JP guest byte, mapping provenance)]."""
    rows = list(rows)
    us = tracked_word_refs(usa, {address & ~3 for _, address, _, _ in rows}, window)
    jp = tracked_word_refs(japan, {address & ~3 for _, _, address, _ in rows}, window)
    results = []
    for slug, usa_byte, japan_byte, provenance in rows:
        a, b = us.get(usa_byte & ~3, ()), jp.get(japan_byte & ~3, ())
        count_a = dict(sorted(Counter(item['operation'] for item in a).items()))
        count_b = dict(sorted(Counter(item['operation'] for item in b).items()))
        context = best_context_pair(usa, japan, a, b, radius)
        read_context = best_context_pair(
            usa, japan,
            [site for site in a if site['operation'].startswith('l')],
            [site for site in b if site['operation'].startswith('l')], radius)
        results.append({
            'slug': slug,
            'mapping_provenance': provenance,
            'usa_guest_byte': f'0x{usa_byte:08X}',
            'japan_guest_byte': f'0x{japan_byte:08X}',
            'usa_operation_counts': count_a,
            'japan_operation_counts': count_b,
            'same_operation_counts': bool(count_a and count_a == count_b),
            'matching_context': bool(context and
                                     context['matching_instructions'] == 2 * radius + 1),
            'matching_read_context': bool(
                read_context and
                read_context['matching_instructions'] == 2 * radius + 1),
            'best_context': context,
        })
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--usa', type=Path, required=True)
    parser.add_argument('--japan', type=Path, required=True)
    parser.add_argument('--output', type=Path, help='Optional metadata-only JSON')
    parser.add_argument('--summary', action='store_true')
    args = parser.parse_args(argv)
    from practice.rom_layout_audit import load_verified
    from practice.unlocks import UNLOCKS
    from practice.region_unlocks import japan_unlock_lead
    rows = [(row.slug, row.address, lead.address, lead.confidence)
            for row in UNLOCKS if (lead := japan_unlock_lead(row)) is not None]
    items = compare_contexts(load_verified(args.usa, 'usa'),
                             load_verified(args.japan, 'japan_0'), rows)
    matched = sum(item['matching_context'] for item in items)
    matched_reads = sum(item['matching_read_context'] for item in items)
    same_counts = sum(item['same_operation_counts'] for item in items)
    result = {
        'note': 'Code-shape correlation only; DOES NOT identify individual item bytes or bit masks',
        'candidate_count': len(items),
        'paired_context_count': matched,
        'paired_read_context_count': matched_reads,
        'same_operation_counts': same_counts,
        'candidates': items,
    }
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if args.summary:
        print(f'MIPS tracked reference context pairs: {matched}/{len(items)} '
              f'(read contexts: {matched_reads}/{len(items)}; '
              f'equal operation counts: {same_counts}/{len(items)})')
    elif not args.output:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

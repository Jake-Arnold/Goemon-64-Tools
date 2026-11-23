#!/usr/bin/env python3
"""Conservative static original-Japanese-ASM dataflow scan of stage D0..D3.

Usage: python3 scan_stage_orig.py --asm-dir /private/pinned/mnsg/asm/japan_0
This is a local, original-ROM-derived scan; scan results contain no MIPS bytes.
It does NOT establish absence of aliased/indirect readers, overlays, DMA or VM access.
"""
import argparse
import collections
import json
import pathlib
import re

SYM = 'D_80162420_163020'
INSTR = re.compile(r'^\s*/\*\s*([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+[0-9a-fA-F]{8}\s*\*/\s*([\w.]+)\s*(.*?)\s*$')
MEMOPS = {'lb', 'lbu', 'sb', 'lh', 'lhu', 'sh', 'lw', 'sw', 'lwc1', 'swc1', 'ld', 'sd'}
WRITEOPS = {'sb', 'sh', 'sw', 'swc1', 'sd'}


def scan(root):
    files = sorted(pathlib.Path(root).rglob('*.s'))
    if not files:
        raise ValueError('No extracted original ASM; verify --asm-dir')
    hits, referenced = [], []
    total = 0
    for fn in files:
        vals = {}
        func = 'unknown'
        refs = 0
        for line in fn.read_text(errors='replace').splitlines():
            st = line.strip()
            if st.startswith('glabel '):
                func = st.split()[1]
                vals = {}
                continue
            m = INSTR.match(line)
            if not m:
                continue
            off, pc, op, operands = m.groups()
            total += 1
            args = [a.strip() for a in operands.split(',')]
            if SYM in operands:
                refs += 1
            if op in MEMOPS and len(args) >= 2:
                mm = re.match(r'(-?0x[0-9a-fA-F]+|-?\d+)\(\$(\w+)\)', args[-1])
                if mm:
                    disp, base = int(mm.group(1), 0), mm.group(2)
                    val = vals.get(base)
                    if val is not None:
                        addr = (val + disp) & 0xffffffff
                        if 0x801624F0 <= addr <= 0x801624F3:
                            hits.append({'function': func, 'pc': '0x' + pc.upper(),
                                         'rom_offset': '0x' + off.upper(),
                                         'op': op, 'kind': 'write' if op in WRITEOPS else 'read',
                                         'address': f'0x{addr:08X}'})
            if args and args[0].startswith('$'):
                dst = args[0][1:]
                if op == 'lui':
                    if SYM in operands:
                        vals[dst] = 0x80160000
                    else:
                        im = re.search(r'0x[\da-fA-F]+', args[1]) if len(args) > 1 else None
                        vals[dst] = (int(im.group(), 16) & 0xffff) << 16 if im else None
                elif op in ('addiu', 'ori', 'andi') and len(args) > 2:
                    src, imm = args[1].lstrip('$'), args[2]
                    if SYM in imm and '%lo(' in imm:
                        val = 0x2420
                    else:
                        try:
                            val = int(imm, 0)
                        except ValueError:
                            val = None
                    prev = vals.get(src)
                    if prev is None or val is None:
                        vals.pop(dst, None)
                    elif op == 'addiu':
                        vals[dst] = (prev + ((val + 0x8000) % 0x10000 - 0x8000)) & 0xffffffff
                    elif op == 'ori':
                        vals[dst] = prev | (val & 0xffff)
                    else:
                        vals[dst] = prev & (val & 0xffff)
                elif op in ('or', 'addu') and len(args) >= 3:
                    x, y = args[1].lstrip('$'), args[2].lstrip('$')
                    if x == 'zero':
                        vals[dst] = vals.get(y)
                    elif y == 'zero':
                        vals[dst] = vals.get(x)
                    elif op == 'or':
                        vals.pop(dst, None)
                    else:
                        vals.pop(dst, None)
                elif op not in WRITEOPS:
                    vals.pop(dst, None)
        if refs:
            referenced.append({'file': fn.name, 'symbol_references': refs})
    return {'status': 'STATIC_SYMBOLIC_BASE_REGISTER_SCAN_ONLY',
            'limits': 'Not exhaustive for indirect, aliased, interprocedural, DMA or VM reads',
            'asm_files_scanned': len(files), 'instructions_scanned': total,
            'files_referencing_stage_symbol': referenced, 'stage_d0_d3_direct_hits': hits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--asm-dir', type=pathlib.Path, required=True)
    ap.add_argument('--out', type=pathlib.Path)
    args = ap.parse_args()
    result = scan(args.asm_dir)
    data = json.dumps(result, indent=2) + '\n'
    if args.out:
        args.out.write_text(data)
    else:
        print(data, end='')

if __name__ == '__main__':
    main()

"""USA file_12 original-upstream 385-function C/ASM research preflight.

Stages 374 contiguous registration wrappers as one generated C source plus
8 neighboring C helpers and the previous 3 C lifecycle sources. Sources are
verified by pinned SHA-256 before building in a new copy of pristine upstream.
The original ROM and assembly remain in the caller's private checkout.
This does NOT promote 315+385 C in the canonical decomp verifier.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('file12_fullrom_base',ROOT/'integrate_fullrom.py')
BASE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BASE)

# source, original symbol, decompressed ROM start, original size, source SHA-256
SPECS = (
 ('reg_374', 'func_8020DE40_5C9310', 0x5C9310, 374*0x24, '046af7d8140efca107fd45b79ea7a08cd8562ad857b9dcbde9323754a6aa639a'),
 ('param_xyz', 'func_80218D7C_5D424C', 0x5D424C, 0x14, '0ab7ac707da850646f80b92c0b8538f0380478c4d269003a870a5c1cd9cda77c'),
 ('param_bytes', 'func_80218D90_5D4260', 0x5D4260, 0x18, '8af0d184306b502633d5f510e41c414ac0bf5a29016a938212100a8b6ac3621b'),
 ('constant_821', 'func_80218DF8_5D42C8', 0x5D42C8, 0xC, '4f1235bb7005e5e656f99fa394cbb78b0c4c2907d7720bfce98fb49cfba5c4f3'),
 ('grid_reset', 'func_80218E04_5D42D4', 0x5D42D4, 0x78, '4d14a4e7040db16899d4cb5703b04e06d00502188f11d386907ee8d8f72f2cb3'),
 ('update_dispatch', 'func_80218E7C_5D434C', 0x5D434C, 0xB4, 'c89c568ba7a1cd590526ea901f2673b0563cd95e081a639ef0f8a68b6529a533'),
 ('state2_callback', 'func_80218F30_5D4400', 0x5D4400, 0xB8, 'a5a18d9ff5bda797ac7b6645eaca77a89ffc422032199a4fed167ad81fcd719f'),
 ('task_noop', 'func_8021A308_5D57D8', 0x5D57D8, 0x8, '003d600cb9cb7a39cb530ed275f63f3746a45704c1ccc856393660549fd49b25'),
 ('task_sentinels', 'func_8021A310_5D57E0', 0x5D57E0, 0x18, '688d5ee4a27432011fb8fe53cacb70b16c7872fa5416c4d44dff6bc950507283'),
 ('release_noop', 'func_8021A4DC_5D59AC', 0x5D59AC, 0x8, '5fc4eced2053d32f716d31491d0408b862b25cc9929fd65101b4709c1e4295a4'),
 ('active_gate', 'func_8021A644_5D5B14', 0x5D5B14, 0x38, '6d8df03a1dccbae56a1b7f88b8d430e02023eb0e9e14b5381c317a6ff4dbd0ba'),
 ('vector_cross', 'func_8021A7E8_5D5CB8', 0x5D5CB8, 0x70, '14aa6a995aeae17946b27a8cd5544a964f8e0ab707508d7d2bf764b7c9c3102e'),
)
WRAPPER_FIRST = 0x8020DE40
WRAPPER_COUNT = 374
WRAPPER_BYTES = WRAPPER_COUNT*0x24


def generate_wrapper_source(asm: str) -> str:
    """Read original Splat symbols, never store the asset bytes or disassembly."""
    source = ('typedef unsigned char u8; typedef unsigned short u16; typedef short s16; '
              'typedef int s32; typedef unsigned int u32;\n'
              'extern void func_80013AC4_146C4(void*);\n')
    current = WRAPPER_FIRST
    names = []
    pattern = r'^nonmatching (func_([0-9A-F]{8})_([0-9A-F]+)), 0x24\n\nglabel \1\n(.+?)\nendlabel \1'
    for entry in re.finditer(pattern, asm, re.M | re.S):
        name, vma, rom, body = entry.groups()
        if int(vma,16)!=current:
            continue
        expected_rom = 0x5C9310 + (current-WRAPPER_FIRST)
        if int(rom,16)!=expected_rom:
            raise ValueError('Registration wrapper ROM/VRAM mapping changed')
        globals_found = set(re.findall(r'%hi\((D_[A-Za-z0-9_]+)\)', body))
        calls = set(re.findall(r'\bjal\s+(func_[A-Za-z0-9_]+)',body))
        if len(globals_found)!=1 or calls!={'func_80013AC4_146C4'}:
            raise ValueError('Registration wrapper no longer has one pinned descriptor and one call')
        symbol = next(iter(globals_found))
        source += f'extern u8 {symbol}[];void {name}(void){{func_80013AC4_146C4({symbol});}}\n'
        names.append(name)
        current += 0x24
    if len(names)!=WRAPPER_COUNT or current != 0x802112D8:
        raise ValueError('Incomplete 374-wrapper original-USA contiguous run')
    if hashlib.sha256(source.encode()).hexdigest()!=SPECS[0][4]:
        raise ValueError('Exact pinned 374-wrapper source text changed')
    return source


def stage_inputs(upstream: Path, temp: Path) -> Path:
    source_dir=temp/'sources';source_dir.mkdir()
    original_asm=(upstream/'asm/usa/5C8770.s').read_text()
    (source_dir/'reg_374.c').write_text(generate_wrapper_source(original_asm))
    for name,_,_,_,sha in SPECS[1:]:
        source = ROOT / (name+'.c') if (ROOT/(name+'.c')).exists() else ROOT/'adjacent'/(name+'.c')
        content=source.read_bytes()
        if hashlib.sha256(content).hexdigest()!=sha:
            raise ValueError('Pinned source hash differs: '+name)
        (source_dir/(name+'.c')).write_bytes(content)
    return source_dir


def build_layout(source_dir:Path):
    funcs=[];layout=[];previous=0x5C8770
    for name,symbol,start,size,digest in SPECS:
        if start<previous:raise ValueError('C source intervals overlap')
        if start>previous:
            layout.append(('asm',f'file12_gap_{previous:06X}_{start:06X}',previous,start))
        path=source_dir/(name+'.c')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('Pinned C input identity mismatch: '+name)
        funcs.append((name,symbol,start,size,digest))
        layout.append(('c',name,start,start+size))
        previous=start+size
    if previous<0x5E3C90:
        layout.append(('asm',f'file12_gap_{previous:06X}_5E3C90',previous,0x5E3C90))
    if sum(end-start for _,_,start,end in layout)!=0x5E3C90-0x5C8770:
        raise ValueError('file12 original text not completely covered')
    return tuple(funcs),tuple(layout)


def split_original_assembly(original_text:str,candidate:Path)->None:
    """Retain each original ASM gap, its instructions and trailing data alias."""
    positions={}
    for match in re.finditer(r'(?m)^nonmatching func_[0-9A-F]{8}_([0-9A-F]+), 0x[0-9A-F]+$',original_text):
        key=int(match.group(1),16)
        if key in positions:raise ValueError('Duplicate function position')
        positions[key]=match.start()
    for match in re.finditer(r'(?m)^\s*/\* ([0-9A-F]{6}) [0-9A-F]{8} [0-9A-F]{8} \*/',original_text):
        positions.setdefault(int(match.group(1),16),match.start())
    if 0x5C8770 not in positions or 0x5E3C8C not in positions:
        raise ValueError('Pinned file12 ASM endpoints missing')
    preamble=original_text[:positions[0x5C8770]]
    if '.section .text' not in preamble:
        raise ValueError('Missing original assembly section preamble')
    slices=[(start,end,name) for kind,name,start,end in BASE.LAYOUT if kind=='asm']
    for start,end,name in slices:
        first = 0 if start==0x5C8770 else positions[start]
        last = len(original_text) if end==0x5E3C90 else positions[end]
        if first>=last:raise ValueError('Invalid ASM gap source boundaries')
        piece=original_text[first:last]
        if start!=0x5C8770:piece=preamble+piece
        dest=candidate/'asm/usa'/(name+'.s')
        if dest.exists():raise ValueError('Existing staged ASM source')
        dest.write_text(piece)
    if (candidate/'asm/usa'/(slices[-1][2]+'.s')).read_text().count('alabel D_802287BC_5E3C8C')!=1:
        raise ValueError('Original file12 zero-size tail data alias not preserved')


def integrate_385(upstream:Path,candidate:Path,jobs:int=4):
    upstream=upstream.resolve()
    with tempfile.TemporaryDirectory(prefix='goemon-file12-expanded-sources-') as t:
        sources=stage_inputs(upstream,Path(t))
        functions,layout=build_layout(sources)
        BASE.FUNCTIONS=functions
        BASE.LAYOUT=layout
        BASE.split_original_assembly=split_original_assembly
        entries=['    - [0x5C8770, asm, '+layout[0][1]+']']
        for kind,name,start,end in layout[1:]:
            entries.append(f'    - [0x{start:X}, '+('c, '+name if kind=='c' else 'asm, '+name)+']')
        BASE.DEST_BLOCK='\n'.join(['    subalign: null','    overlay: yes','    exclusive_ram_id: static_overlay_2','    subsegments:',*entries,'    - [0x5E3C90, data, file_12]'])
        result=BASE.integrate(upstream,candidate,sources,jobs)
    result.update({
        'status':'exact_original_usa_385_c_overlay_integrated_on_upstream',
        'scope':'Original upstream ASM plus 385 file_12 C functions; NOT canonical 315+385 G2',
        'reconstructed_source_objects':len(functions),
        'reconstructed_function_count':WRAPPER_COUNT+len(functions)-1,
        'reconstructed_original_code_bytes':sum(f[3] for f in functions),
        'contiguous_wrapper_functions':WRAPPER_COUNT,
        'contiguous_wrapper_code_bytes':WRAPPER_BYTES,
        'limitations':'No canonical 315-C coexistence, central decomp.verify, decomp.inventory or full local_ci acceptance',
    })
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',type=Path,required=True)
    p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=4)
    a=p.parse_args()
    if not 1<=a.jobs<=32:raise ValueError('Invalid parallelism')
    report=integrate_385(a.upstream,a.candidate,a.jobs)
    if a.report.exists():raise FileExistsError('Proof output must be new')
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='objects'},indent=2))

if __name__=='__main__':main()

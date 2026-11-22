#!/usr/bin/env python3
"""Read-only Japanese original-address IDO isolated comparison. NOT full G2.

No original ROM/code bytes or binaries are written outside temporary local scratch.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path

def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'FAILED {args!r}\n{p.stderr[-2000:]}')
    return p.stdout

def address(name:str)->int:
    if name=='g_system_ptr':return 0x80161DB8
    m=re.match(r'(?:D|func)_([0-9a-fA-F]{4,8})(?:_|$)',name)
    if not m:raise ValueError('Unknown linker symbol '+name)
    return int(m.group(1),16)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',required=True,type=Path,help='Your original expanded Japan rev-0 32 MiB ROM')
    ap.add_argument('--cc',required=True,type=Path,help='Original SGI IDO 5.3 cc')
    ap.add_argument('--ld',default='mips-linux-gnu-ld')
    ap.add_argument('--objdump',default='mips-linux-gnu-objdump')
    ap.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'manifest.json').read_text())
    rom=args.rom.read_bytes()
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=manifest['original_expanded_rom_sha1']:
        raise AssertionError('Original Japanese expanded ROM not authenticated')
    results=[]
    with tempfile.TemporaryDirectory(prefix='goemon-unique12-') as scratch:
        wd=Path(scratch)
        for row in manifest['functions']:
            name=row['name'];off=int(row['rom_offset'],16);vma=int(row['guest_vma'],16);sz=row['size']
            original=rom[off:off+sz];source=root/'sources'/row['source']
            if hashlib.sha256(source.read_bytes()).hexdigest()!=row['source_sha256'] or hashlib.sha256(original).hexdigest()!=row['original_sha256']:
                raise AssertionError(name+': source or original instruction digest drift')
            obj=wd/'candidate.o'; elf=wd/'candidate.elf'; ldscript=wd/'target.ld'; binary=wd/'candidate.bin'
            run([args.cc,'-c','-non_shared','-G','0','-O2','-mips2','-o',obj,source])
            reloc=run([args.objdump,'-r',obj]); matches=re.findall(r'^\s*([0-9a-fA-F]{8})\s+(R_MIPS_\w+)\s+(\S+)',reloc,re.M)
            observed=sorted((int(off0,16),kind,symbol) for off0,kind,symbol in matches)
            wanted=sorted((r['offset'],r['type'],r['symbol']) for r in row['original_relocations'])
            if observed!=wanted:raise AssertionError(f'{name}: original relocation mismatch {observed!r} vs {wanted!r}')
            names=set(x[2] for x in observed)
            ldscript.write_text(''.join(f'{s} = 0x{address(s):X};\n' for s in sorted(names))+f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(1) {{ *(.text) }} /DISCARD/ : {{ *(.comment) *(.note*) }} }}\n')
            run([args.ld,'-T',ldscript,'-o',elf,obj]);sym=run([args.objdump,'-t',elf])
            pattern='^'+f'{vma:08x}'+r'\s+g\s+F\s+\.text\s+\S+\s+'+re.escape(name)+r'$'
            if not re.search(pattern,sym,re.M):raise AssertionError(f'{name}: original VMA or function symbol identity lost')
            run([args.objcopy,'-O','binary','--only-section=.text',elf,binary])
            code=binary.read_bytes()
            if len(code)<sz or code[:sz]!=original or any(code[sz:]):
                pos=next((i for i in range(min(len(code),sz)) if code[i]!=original[i]),min(len(code),sz))
                raise AssertionError(f'{name}: first original instruction byte mismatch +0x{pos:X}; native text len={len(code)}')
            print(f'PASS {name} offset={row["rom_offset"]} extent={sz}/{sz} original-bytes relocs={len(wanted)}/{len(wanted)}')
            results.append({'function':name,'rom_offset':row['rom_offset'],'exact_bytes':sz,'original_vma':row['guest_vma'],'relocations':len(wanted),'compiled_text_bytes':len(code),'trailing_zero_padding_bytes':len(code)-sz,'outcome':'ISOLATED_NATIVE_EXACT'})
    report={'status':'PASSED_ISOLATED_NATIVE / RESEARCH_ONLY','region':'japan_0','original_rom_sha1':manifest['original_expanded_rom_sha1'], 'original_rom_bytes':len(rom),'native_compiler':'SGI IDO 5.3 -O2 -mips2 -G 0','matched_original_code_bytes':sum(r['exact_bytes'] for r in results),'matched_unique_functions':len(results),'original_object_relocations':sum(r['relocations'] for r in results),'full_rom_G2':'NOT_RUN','all_original_ELF_functions':'NOT_RUN','all_semantic_relocations':'NOT_RUN','strict_inventory':'NOT_RUN','full_local_ci':'NOT_RUN','accepted_C_delta':0,'records':results}
    if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASSED_ISOLATED_NATIVE: {len(results)} unique candidates; {report["matched_original_code_bytes"]} original instruction bytes; {report["original_object_relocations"]} original relocations. NO COMBINED G2 CLAIM.')

if __name__=='__main__':main()

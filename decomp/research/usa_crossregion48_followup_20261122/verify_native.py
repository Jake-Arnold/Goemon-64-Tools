#!/usr/bin/env python3
"""Fail-closed USA isolated original-address native-ID0 verifier.

This only proves 48 isolated functions, NOT integrated USA G2 acceptance.
You must provide your own authentic decompressed USA ROM and pinned toolchain.
No ROM, original ASM, compiler, binaries or private assets are included.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, tempfile, os
from pathlib import Path

ROM_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
RELOC=re.compile(r'^\s*([0-9A-Fa-f]{8})\s+(R_MIPS_\w+)\s+(\S+)',re.M)

def run(args,env):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=env)
 if p.returncode:
  raise RuntimeError('FAILED '+str(args)+'\n'+p.stderr[-2000:])
 return p.stdout

def symbol_addr(s):
 if s=='g_system_ptr':return 0x8015C5C8
 m=re.fullmatch(r'(?:D|func)_([0-9A-Fa-f]+)(?:_[0-9A-Fa-f]+)?',s)
 if m:return int(m.group(1),16)
 raise ValueError('Undefined or ambiguous target symbol '+s)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--rom',type=Path,required=True)
 p.add_argument('--cc',type=Path,required=True)
 p.add_argument('--ld',default='mips-linux-gnu-ld')
 p.add_argument('--objcopy',default='mips-linux-gnu-objcopy')
 p.add_argument('--objdump',default='mips-linux-gnu-objdump')
 p.add_argument('--report',type=Path)
 args=p.parse_args()
 root=Path(__file__).resolve().parent
 manifest=json.loads((root/'manifest.json').read_text())
 rom=args.rom.read_bytes()
 if len(rom)!=33_554_432 or hashlib.sha1(rom).hexdigest()!=ROM_SHA1:raise AssertionError('Wrong USA source ROM identity')
 passed=[]
 env=os.environ.copy()
 with tempfile.TemporaryDirectory(prefix='goemon-usa48-') as dirname:
  d=Path(dirname)
  for entry in manifest['functions']:
   name=entry['name'];offset=int(entry['original_usa_rom_offset'],16)
   size=entry['size'];vma=int(entry['original_guest_vma'],16)
   original=rom[offset:offset+size];source=root/entry['source']
   if hashlib.sha256(original).hexdigest()!=entry['original_rom_code_sha256']:raise AssertionError(name+' source ROM extent mismatch')
   if hashlib.sha256(source.read_bytes()).hexdigest()!=entry['usa_source_sha256']:raise AssertionError(name+' source C hash mismatch')
   obj=d/'candidate.o';linked=d/'candidate.elf';binary=d/'candidate.bin';script=d/'target.ld'
   run([args.cc,'-c','-G','0','-non_shared','-O2','-mips2','-I',root/'sources','-o',obj,source],env)
   reloc=run([args.objdump,'-r',obj],env)
   obs=sorted((int(a,16),b,c) for a,b,c in RELOC.findall(reloc))
   want=sorted((r['offset'],r['type'],r['symbol']) for r in entry['original_symbolic_relocations'])
   if obs!=want:raise AssertionError(f'{name} symbolic reloc mismatch\nGOT {obs}\nWANT {want}')
   symbols={s for _,_,s in obs}
   script.write_text(''.join(f'{s} = 0x{symbol_addr(s):X};\n' for s in sorted(symbols))+f'SECTIONS {{ .text 0x{vma:X} : SUBALIGN(1) {{ *(.text) }} /DISCARD/ : {{ *(.comment) *(.note*) }} }}\n')
   run([args.ld,'-T',script,'-o',linked,obj],env)
   run([args.objcopy,'-O','binary','--only-section=.text',linked,binary],env)
   code=binary.read_bytes()
   if len(code)<size or code[:size]!=original or any(code[size:]):
    n=next((i for i,(a,b) in enumerate(zip(code,original)) if a!=b),min(len(code),size))
    raise AssertionError(f'{name}: first mismatch at +0x{n:X}; compiled size {len(code)} vs original {size}')
   symbols_dump=run([args.objdump,'-t',linked],env)
   if not re.search(r'(?m)^'+f'{vma:08x}'+r'\s+g\s+F\s+\.text\s+\S+\s+'+re.escape(name)+r'$',symbols_dump):
    raise AssertionError(name+' linked VMA/function identity mismatch')
   passed.append({'name':name,'rom_offset':entry['original_usa_rom_offset'],'bytes':size,'relocs':len(obs),'status':'PASSED_ISOLATED_NATIVE'})
   print(f'PASS {len(passed):02d}/48 {name} {size}/{size} bytes {len(obs)} original relocations')
 result={'status':'PASSED_ISOLATED_NATIVE / RESEARCH_ONLY','usa_rom_sha1':ROM_SHA1,'verified':len(passed),'original_machine_code_bytes':sum(x['bytes'] for x in passed),'original_symbolic_relocations':sum(x['relocs'] for x in passed),'full_usa_ROM_G2':'NOT_RUN','all_ELF_functions':'NOT_RUN','all_semantic_relocations':'NOT_RUN','full_local_CI':'NOT_RUN','official_usa_promotions':0,'functions':passed}
 if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
 print('PASS isolated USA functions:',result['verified'],'bytes:',result['original_machine_code_bytes'],'original relocs:',result['original_symbolic_relocations'],'/ NOT official G2')

if __name__=='__main__':main()

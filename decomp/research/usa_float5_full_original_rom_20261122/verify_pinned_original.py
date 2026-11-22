#!/usr/bin/env python3
"""Fail-closed native IDO 5.3 original-ROM/ELF replay for five new USA C functions.

Uses *only* a user-provided, already extracted & rebuilt pinned original USA
mnsg checkout. No copyrighted materials, binary artifacts, ROMs, or toolchains
are distributed. Fresh scratch output is required. This is not the canonical
modern decomp.verify staging adapter.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PIN = '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
RETAIL = 'df8083a54296b8c151917c5333e1c85f014a2a66'
EXPANDED = '6ea0ed71032ce08fc2745f412d84936382197494'
ELF_ORIGINAL = '83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038'
# Original absolute ROM offsets / positive-size FUNC extents; do not infer from .text alignment.
TARGETS = {
 'func_80012500_13100': (0x13100, 24),
 'func_800127FC_133FC': (0x133FC, 28),
 'func_8001285C_1345C': (0x1345C, 28),
 'func_8001C9BC_1D5BC': (0x1D5BC, 28),
 'func_8001C9D8_1D5D8': (0x1D5D8, 52),
}
SPLITS = (
 ('12760', 'research_mixed_12760', 0x14000),
 ('1D570', 'research_mixed_1d570', 0x204B0),
)

def digest(path:Path, kind='sha1'):
 h=hashlib.new(kind)
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()

def exec_logged(cmd,cwd,env,path):
 with path.open('w') as f:result=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError('Native command FAILED (see private log '+str(path)+'): '+str(cmd))

def elf_records(path):
 funcs,relocs=[],[]
 s=subprocess.check_output(['readelf','-sW',str(path)],text=True)
 r=subprocess.check_output(['readelf','-rW',str(path)],text=True)
 for line in s.splitlines():
  m=re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)',line)
  if m and int(m.group(2))>0:
   funcs.append((m.group(6),int(m.group(1),16),int(m.group(2)),m.group(3),m.group(4),m.group(5)))
 section=''
 for line in r.splitlines():
  x=re.match(r"^Relocation section '([^']+)'",line)
  if x:section=x.group(1)
  m=re.match(r'^\s*([0-9a-fA-F]+)\s+[0-9a-fA-F]+\s+(R_MIPS_\S+)\s+[0-9a-fA-F]+\s+(\S+)',line)
  if m:relocs.append((section,int(m.group(1),16),m.group(2),m.group(3)))
 return funcs,relocs

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for flag in ('checkout','deps','runtime','output'):
  p.add_argument('--'+flag,type=Path,required=True)
 p.add_argument('--jobs',type=int,default=6)
 p.add_argument('--also-92f0',action='store_true',help='Native-test the three previously proved 92F0 C functions in the same complete ROM as the five new functions')
 a=p.parse_args()
 source=Path(__file__).resolve().parent
 checkout=a.checkout.resolve();out=a.output.resolve()
 if out.exists():raise SystemExit('Refusing pre-existing output path')
 if not (checkout/'src/92F0.c').exists():raise SystemExit('Not a complete pinned upstream checkout')
 pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()
 assert pin==PIN,('Wrong upstream pin',pin)
 rom16=checkout/'config/usa/baserom.z64'
 rom32=checkout/'config/usa/baserom.decompressed.z64'
 original_build=checkout/'build/usa/mnsg.z64'
 original_elf=checkout/'build/usa/mnsg.elf'
 assert digest(rom16)==RETAIL and rom16.stat().st_size==16*1024*1024
 assert digest(rom32)==EXPANDED and rom32.stat().st_size==32*1024*1024
 assert original_build.read_bytes()==rom32.read_bytes(),'Original upstream build is not authenticated'
 assert digest(original_elf,'sha256')==ELF_ORIGINAL,'Original ELF SHA mismatch'
 assert (checkout/'tools/ido-5.3/cc').is_file()
 # No ROM or generated binary may be written back into the pinned original checkout.
 out.mkdir(parents=True)
 work=out/'pinned_source_copy'
 shutil.copytree(checkout,work,symlinks=True)
 config=work/'config/usa/splat.yaml';config_text=config.read_text()
 assert config_text.count('    - [0x12760, asm]')==1
 assert config_text.count('    - [0x1D570, asm]')==1
 assert config_text.count('    - [0x14540, c, wave_uty]')==1
 config_text=config_text.replace('    - [0x12760, asm]','    - [0x12760, c, research_mixed_12760]\n    - [0x14000, asm]',1)
 config_text=config_text.replace('    - [0x1D570, asm]','    - [0x1D570, c, research_mixed_1d570]',1)
 config.write_text(config_text)
 for old,unit,stop in SPLITS:
  raw=(checkout/'asm/usa'/f'{old}.s').read_text()
  names=re.findall(r'^nonmatching (func_\w+),',raw,re.M)
  assert names and len(names)==37
  names=[n for n in names if int(n.rsplit('_',1)[1],16)<stop]
  out_parts=['#include "common.h"']
  for name in names:
   c=source/'source'/f'{name}.c'
   if name in TARGETS:
    assert c.is_file()
    body=c.read_text().replace('#include "common.h"','').strip()
    out_parts.append(body)
   else:
    assert not c.exists(),'Unexpected C file for original ASM-owned function'
    out_parts.append(f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/{unit}/{name}.s")')
  (work/'src'/f'{unit}.c').write_text('\n\n'.join(out_parts)+'\n')
 assert sum(1 for f in (source/'source').glob('*.c'))==len(TARGETS)
 env=os.environ.copy()
 env['PYTHONHOME']=str(a.runtime.resolve()/'python')
 env['PYTHONPATH']=str(a.deps.resolve()/'.venv/lib/python3.12/site-packages')
 env['LD_LIBRARY_PATH']=str(a.runtime.resolve()/'lib')+os.pathsep+env.get('LD_LIBRARY_PATH','')
 env['PATH']=str(a.deps.resolve()/'bin')+os.pathsep+env.get('PATH','')
 python=a.runtime.resolve()/'python/bin/python3.12'
 splat=a.deps.resolve()/'.venv/bin/splat'
 exec_logged([str(python),str(splat),'split','config/usa/splat.yaml'],work,env,out/'splat.log')
 # These two stale monolithic ASM files are inherited from copied baseline.
 # The new C-linked mixed units own their original ranges in the new linker script.
 for old,_,_ in SPLITS:(work/'asm/usa'/f'{old}.s').unlink(missing_ok=True)
 exec_logged(['make',f'-j{a.jobs}','VERSION=usa','build/usa/mnsg.z64'],work,env,out/'native_build.log')
 candidate=work/'build/usa/mnsg.z64';candidate_elf=work/'build/usa/mnsg.elf'
 assert candidate.stat().st_size==33554432
 assert candidate.read_bytes()==rom32.read_bytes(),'FAILED_ROM: original vs new complete ROM differ'
 fs0,rs0=elf_records(original_elf);fs1,rs1=elf_records(candidate_elf)
 assert len(fs0)==len(fs1)==7376 and Counter(fs0)==Counter(fs1),'FAILED_ELF: original-positive-size FUNC identities differ'
 assert len(rs0)==len(rs1)==82216 and Counter(rs0)==Counter(rs1),'FAILED_RELOC: original ELF relocation tuples differ'
 known={f[0]:(f[1],f[2]) for f in fs1}
 for name,(rom_offset,size) in TARGETS.items():
  assert known[name]==(0x80000000+rom_offset-0xC00,size),(name,known[name])
 # Optional second native integration in the SAME scratch checkout: 8 total new C functions.
 prior={
  'func_80008798_9398':(0x9398,44),
  'func_8000A0F0_ACF0':(0xACF0,64),
  'func_8000A18C_AD8C':(0xAD8C,48),
 }
 if a.also_92f0:
  path=work/'src/92F0.c'
  content=path.read_text()
  for name in prior:
   prior_source=source/'source92f0'/f'{name}.c'
   assert prior_source.is_file()
   marker=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/{name}.s")'
   assert content.count(marker)==1
   content=content.replace(marker,prior_source.read_text().replace('#include "common.h"','').strip())
  path.write_text(content)
  exec_logged(['make',f'-j{a.jobs}','VERSION=usa','build/usa/mnsg.z64'],work,env,out/'native_build_combined_eight.log')
  assert candidate.read_bytes()==rom32.read_bytes(),'FAILED_ROM: combined 8 C functions changed original ROM'
  fs8,rs8=elf_records(candidate_elf)
  assert len(fs8)==len(fs0)==7376 and Counter(fs8)==Counter(fs0),'FAILED_ELF: combined eight C sources'
  assert len(rs8)==len(rs0)==82216 and Counter(rs8)==Counter(rs0),'FAILED_RELOC: combined eight C sources'
  defined={n:(v,s) for n,v,s,*rest in fs8}
  for name,(off,length) in prior.items():
   assert defined[name]==(0x80000000+off-0xC00,length),(name,defined[name])
 report={
  'status':'RESEARCH_ONLY_WHOLE_ORIGINAL_UPSTREAM_ROM_EXACT',
  'original_rom_sha1':EXPANDED,'new_rom_sha1':digest(candidate),
  'original_rom_size':33554432,'new_rom_size':candidate.stat().st_size,
  'elf_original_sha256':ELF_ORIGINAL,'elf_new_sha256':digest(candidate_elf,'sha256'),
  'original_elf_functions':len(fs0),'candidate_elf_functions':len(fs1),'positive_function_identities_equal':True,
  'original_elf_relocations':len(rs0),'candidate_elf_relocations':len(rs1),'relocation_identities_equal':True,
  'new_original_C_functions':[{ 'name':name,'rom_offset':hex(start),'original_bytes':size,'source_sha256':digest(source/'source'/f'{name}.c','sha256') } for name,(start,size) in TARGETS.items()],
  'new_original_instruction_bytes':sum(s for _,s in TARGETS.values()),
  'combined_92f0_three':a.also_92f0,
  'combined_unique_C_functions':8 if a.also_92f0 else 5,
  'combined_original_bytes':316 if a.also_92f0 else 160,
  'prior_92f0_original_C_functions':[{ 'name':name,'rom_offset':hex(start),'original_bytes':size,'source_sha256':digest(source/'source92f0'/f'{name}.c','sha256') } for name,(start,size) in prior.items()] if a.also_92f0 else [],
  'canonical_decomp_verify':'NOT_RUN','canonical_inventory':'NOT_RUN','full_decomp_local_ci':'NOT_RUN',
  'accepted_count_delta':0,'accepted_byte_delta':0,
 }
 (out/'original_upstream_proof.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS 33,554,432/33,554,432 expanded USA original ROM exact')
 print('PASS 7,376/7,376 ELF positive function identities')
 print('PASS 82,216/82,216 original upstream ELF relocation tuples')
 print('PASS five new C source functions, 160 original bytes, intact ASM remainder')
 if a.also_92f0:print('PASS eight combined C functions, 316 original bytes, full-ROM/ELF/relocations exact')
 print('RESEARCH_ONLY: canonical decomp.verify/inventory/full CI NOT RUN')

if __name__=='__main__':main()

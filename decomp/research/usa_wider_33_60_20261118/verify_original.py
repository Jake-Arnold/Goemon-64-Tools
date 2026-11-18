#!/usr/bin/env python3
"""Original USA file33-60 69-candidate native byte verifier; requires user's owned ROM."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, tempfile, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
SHA='6ea0ed71032ce08fc2745f412d84936382197494'

def run(args,env=None):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=env)
 if p.returncode:raise RuntimeError(f"{args}: code {p.returncode}\n{(p.stdout+p.stderr)[-3000:]}")
 return p.stdout

def check_source(row):
 s=(ROOT/row['source_path']).read_bytes()
 if hashlib.sha256(s).hexdigest()!=row['source_sha256']:raise ValueError('source sha256 mismatch: '+row['source_path'])
 if hashlib.sha1(b'blob '+str(len(s)).encode()+b'\0'+s).hexdigest()!=row['source_git_blob_sha1']:raise ValueError('source Git blob mismatch: '+row['source_path'])
 return s

def verify(rom,ido,report):
 if not rom:raise ValueError('required --rom')
 b=pathlib.Path(rom).read_bytes()
 if len(b)!=33554432 or hashlib.sha1(b).hexdigest()!=SHA:raise ValueError('USA 32 MiB original ROM identity mismatch')
 manifest=json.loads((ROOT/'manifest.json').read_text());records=manifest['functions'];assert len(records)==69
 env=os.environ.copy();results=[]
 with tempfile.TemporaryDirectory(prefix='goemon-wider69-') as tmp:
  d=pathlib.Path(tmp)
  for idx,row in enumerate(records):
   src=ROOT/row['source_path'];check_source(row);name=row['name'];vm=int(row['original_vma'],16);romoff=int(row['original_rom_offset'],16);size=row['original_instruction_bytes']
   obj=d/f'f_{idx}.o';ld=d/f'f_{idx}.ld';elf=d/f'f_{idx}.elf';binary=d/f'f_{idx}.bin'
   ld.write_text(f'SECTIONS {{ .text 0x{vm:08X} : SUBALIGN(4) {{ *(.text) *(.text.*) }} /DISCARD/ : {{ *(.note*) *(.comment*) }} }}\n')
   run([ido,*FLAGS,'-o',obj,src],env)
   text=src.read_text();syms=set(re.findall(r'\b(?:func|D)_[0-9A-F]{8}(?:_[0-9A-F]{4,8})?',text));syms.discard(name)
   defs=[f'--defsym={s}=0x{int(s.split("_")[1],16):08X}' for s in sorted(syms)]
   run(['mips-linux-gnu-ld','-T',ld,*defs,'-o',elf,obj],env)
   run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binary],env)
   got=binary.read_bytes();want=b[romoff:romoff+size]
   if len(got)<size or got[:size]!=want or any(got[size:]):raise AssertionError(f'FAIL original MIPS {name} at 0x{romoff:X}, generated {len(got)}, original {size}')
   results.append({'function':name,'rom_offset':f'0x{romoff:X}','original_bytes':size,'status':'EXACT'})
 output={'format':'goemon-wider69-native-replay-v1','status':'PASS','original_rom_sha1':SHA,'functions_exact':len(results),'original_bytes_exact':sum(x['original_bytes'] for x in results),'results':results,'upstream_whole_rom_integration':'NOT_RUN_BY_THIS_SCRIPT','canonical_production_gates':'NOT_RUN'}
 if report:pathlib.Path(report).write_text(json.dumps(output,indent=2)+'\n')
 return output

def host():
 import shutil
 cc=shutil.which('gcc');assert cc, 'gcc unavailable'
 m=json.loads((ROOT/'manifest.json').read_text());paths=[ROOT/x['source_path'] for x in m['functions']]
 for x in m['functions']:check_source(x)
 with tempfile.TemporaryDirectory(prefix='goemon-wider69-host-') as tmp:
  exe=pathlib.Path(tmp)/'actual_source_host_test'
  run([cc,'-std=gnu11','-O1','-g','-Wall','-Wextra','-Wno-unused-parameter','-fno-omit-frame-pointer','-fsanitize=address,undefined','-fno-pie','-no-pie',*paths,ROOT/'test_native_wide_33_60.c','-o',exe])
  return run([exe]).strip()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom');p.add_argument('--ido');p.add_argument('--report');p.add_argument('--host-test-only',action='store_true');a=p.parse_args()
 try:
  if a.host_test_only:print(host());sys.exit(0)
  if not a.ido:raise ValueError('--ido required')
  o=verify(a.rom,a.ido,a.report);print(f"PASS: {o['functions_exact']} functions, {o['original_bytes_exact']} native-original bytes")
 except Exception as e:print('FAIL:',repr(e),file=sys.stderr);sys.exit(1)

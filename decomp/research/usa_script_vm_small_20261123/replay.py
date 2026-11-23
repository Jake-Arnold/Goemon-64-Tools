#!/usr/bin/env python3
"""Read-only original-address native comparison; no canonical acceptance."""
import argparse, hashlib, os, subprocess, sys, json
from collections import Counter
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--compiler',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--binutils',type=Path,required=True);p.add_argument('--lib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--source',type=Path,nargs='*');a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True)
sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32,compare_code,linker_script
SHA=lambda b:hashlib.sha256(b).hexdigest()
ROM='6ea0ed71032ce08fc2745f412d84936382197494';UP='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
rom=(a.baseline/'config/usa/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM and (a.baseline/'build/usa/mnsg.z64').read_bytes()==rom
for d in (a.compiler,a.baseline):
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()==UP
 assert not subprocess.check_output(['git','diff','--name-only'],cwd=d,text=True).strip()
cc=a.compiler.resolve()/'tools/ido-5.3/cc';assert SHA(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
flags='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Iinclude -Ilibultra/include -Ilibultra/include/PR -Isrc -I. -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
env=os.environ.copy();env['LD_LIBRARY_PATH']=str(a.lib.resolve())+':'+env.get('LD_LIBRARY_PATH','');ld=a.binutils.resolve()/'mips-linux-gnu-ld'
old=Elf32((a.baseline/'build/usa/asm/usa/3DBA0.s.o').read_bytes());ref=Elf32((a.baseline/'build/usa/mnsg.elf').read_bytes());g=ref.globals()
meta={'F6E8':('func_8003F6E8_402E8',48),'F038':('func_8003F038_3FC38',196),'F480':('func_8003F480_40080',164),'DE80':('func_8003DE80_3EA80',232)}
def rel(e,f):return Counter((x.offset-f.value,x.relocation_type,x.symbol.name or e.names[x.symbol.section]) for x in e.relocations(f.section) if f.value<=x.offset<f.value+f.size)
rows=[]
for s in sorted(a.source or (Path(__file__).parent/'sources').glob('*.c')):
 ledger=(a.repo/'decomp/COMPILER_QUIRKS.md').read_bytes() # read verified ledger for each invocation
 n,size=meta[s.stem.split('_')[0]];of=old.function(n);rf=ref.function(n);addr=rf.value;offset=addr-0x80000000+0xc00;assert of.size==size
 expect=rom[offset:offset+size];obj=a.out/(s.stem+'.o');elf=a.out/(s.stem+'.elf');script=a.out/(s.stem+'.ld')
 cmd=[str(cc),*flags,str(s.resolve()),'-o',str(obj.resolve())]
 row={'source':s.name,'source_sha256':SHA(s.read_bytes()),'function':n,'region':'usa','vma':hex(addr),'rom_offset':hex(offset),'expected_size':size,'ledger_sha256':SHA(ledger),'flags':flags,'compiler_sha256':SHA(cc.read_bytes()),'compiler_quirk_outcome':'NO_NEW_COMPILER_FINDING'}
 with (a.out/(s.stem+'.log')).open('w') as log:
  pr=subprocess.run(cmd,cwd=a.compiler,env=env,stdout=log,stderr=subprocess.STDOUT)
  if pr.returncode:row.update(status='COMPILE_FAILED',exit=pr.returncode);rows.append(row);continue
  e=Elf32(obj.read_bytes());f=e.function(n);rr=rel(e,f);ro=rel(old,of)
  script.write_text(linker_script(n,addr,e.undefined(),g))
  subprocess.run([str(ld),'-T',str(script.resolve()),'--emit-relocs','-o',str(elf.resolve()),str(obj.resolve())],cwd=a.compiler,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  l=Elf32(elf.read_bytes());lf=l.function(n);actual=l.code(lf);cmp=compare_code(expect,actual)
 row.update(cmp);row.update(original_relocations=sum(ro.values()),candidate_relocations=sum(rr.values()),named_relocations_exact=ro==rr,removed_relocation_count=sum((ro-rr).values()),added_relocation_count=sum((rr-ro).values()),status='ISOLATED_EXACT' if cmp['word_differences']==0 and rr==ro else 'RESEARCH_ONLY')
 first=cmp['first_mismatch_offset'];row['exact_prefix_bytes']=first if first is not None else size
 if first is not None:
  k=s.stem.split('_')[0]
  row['first_mismatch_class']={'F6E8':'extent','F038':'register_allocation' if first==40 else 'branch_target_extent','F480':'relocation_and_instruction_scheduling','DE80':'stack_frame' if first==0 else 'saved_register_scheduling'}[k]
  row['first_expected_word']=expect[first:first+4].hex() or None
  row['first_candidate_word']=actual[first:first+4].hex() or None
 delta=(ro-rr)+(rr-ro)
 row['first_relocation_mismatch_offset']=min((x[0] for x in delta),default=None)
 if s.stem in ('F038_reorder','F480_direct_call'):
  row['compiler_quirk_outcome']='EXISTING_QUIRK_REPRODUCED'
  row['ledger_observation']='EBAC declaration/spill-home order' if s.stem=='F038_reorder' else 'source expression-order scheduling'
 elif s.stem in ('DE80_group_lines','F480_separate_lines'):
  row['compiler_quirk_outcome']='EXISTING_QUIRK_NOT_APPLICABLE'
  row['ledger_observation']='physical source-line grouping unchanged native bytes'
 else:row['ledger_observation']='none newly reproduced'
 rows.append(row)
 print(s.name, 'size',len(actual),'different words',cmp['word_differences'],'prefix',row['exact_prefix_bytes'],'relocs',row['named_relocations_exact'],flush=True)
(a.out/'evidence.json').write_text(json.dumps(rows,indent=2)+'\n')

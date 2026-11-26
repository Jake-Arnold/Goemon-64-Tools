#!/usr/bin/env python3
"""Independent named and local-pool references from private original ASM, not candidate object data.
No production code, data, or relocation records are edited. Isolated proof only.
"""
import argparse, hashlib, json, re, sys
from collections import Counter
from pathlib import Path
from replay import META, ROM, COMPILER, sha, run

BASE='8b195d8ce5a31723a71af428ee4f7bccf32b0bf8'
DATA={'usa':'5E3C90','japan_0':'5E8AC0'}
ASFLAGS='-EB -mtune=vr4300 -march=vr4300 -mabi=32 -Iinclude -I.'.split()
def main():
 if not __debug__:raise RuntimeError("assertions required")
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(a.repo))
 from decomp.consolidated_batch_promotion import FLAGS, rels, text, probe, jp55
 from decomp.probe import Elf32
 sources=Path(__file__).parent/'sources';ledger=a.repo/'decomp/COMPILER_QUIRKS.md';proof=[]
 for r,co in [('usa',a.usa),('japan_0',a.jp)]:
  rom=(co/f'config/{r}/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM[r][1];assert hashlib.sha1((co/f'config/{r}/baserom.z64').read_bytes()).hexdigest()==ROM[r][0]
  assert sha((co/'tools/ido-5.3/cc').read_bytes())==COMPILER and run(['git','rev-parse','HEAD'],co).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
  data=(co/f'asm/{r}/data/{DATA[r]}.data.s').read_text()
  for n,z,owner,symbol,*_ in META[r]:
   w=a.work/n;w.mkdir();v,off=map(lambda x:int(x,16),n.split('_')[1:]);pv,po=map(lambda x:int(x,16),symbol.split('_')[1:]);code=rom[off:off+z]
   own=co/f'asm/{r}/{owner}.s';probe.get_original_splat_lines(own,n,off,v,z,code);raw=own.read_text();m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(m)==1;body=m[0].group()
   dm=re.search(r'^dlabel '+symbol+r'\n([^\n]+)',data,re.M);assert dm and '.float' in dm[1] and f'{po:X} {pv:08X}' in dm[1];float_line=dm[1].split('*/',1)[1].strip()
   hi=f'%hi({symbol})';lo=f'%lo({symbol})';local='.Lphase2_pool';lhi=f'%hi({local})';llo=f'%lo({local})';assert body.count(hi)==body.count(lo)==1
   shadow=body.replace(hi,lhi).replace(lo,llo);assert shadow.replace(lhi,hi).replace(llo,lo)==body
   header='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n';pool=f'\n.section .rodata, "a"\n.balign 4\n{local}:\n{float_line}\n'
   def assemble(label,src):
    p=w/(label+'.s');p.write_text(src);obj=w/(label+'.o');run(['mips-linux-gnu-as',*ASFLAGS,'-o',obj,p],co);return obj
   named=assemble('named',header+body+pool);local_obj=assemble('local',header+shadow+pool)
   def compile(label,source):
    lb=ledger.read_bytes();obj=w/(label+'.o');run([co/'tools/ido-5.3/cc',*FLAGS,'-o',obj,source.resolve()],co);return obj,sha(lb)
   source=sources/n/'02_literal_chain.c';native,lh=compile('native',source);other,lh2=compile('native_local',sources/n/'03_literal_local.c');bad_source=sources/n/'06_negative_wrong_float.c';bad,lh3=compile('negative',bad_source)
   named_rel=Counter(rels(named));shadow_rel=Counter(rels(local_obj));native_rel=Counter(rels(native));removed=named_rel-shadow_rel;added=shadow_rel-named_rel
   assert len(removed)==len(added)==2 and {x[1] for x in removed}=={'R_MIPS_HI16','R_MIPS_LO16'} and all(x[2]==symbol for x in removed) and all(x[2]=='.rodata' for x in added)
   assert shadow_rel==native_rel==Counter(rels(other))
   assert text(named)[:z]==text(local_obj)[:z]==text(native)[:z]==text(other)[:z] and not any(text(native)[z:])
   names={x[2] for x in named_rel};defs={}
   for path in list((co/f'config/{r}/symbol_addrs').rglob('*.txt'))+list((co/f'.splat/{r}').glob('undefined*.ld')):
    for k,x in re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9a-fA-F]+)\s*;',path.read_text(),re.M):defs[k]=int(x,16)
   for k in names:
    if k not in defs:
     m=re.match(r'^(?:func|D)_([0-9A-Fa-f]+)(?:_|$)',k);assert m,k;defs[k]=int(m[1],16)
   assert defs[symbol]==pv
   def link(label,obj,addr=pv):
    ld=w/(label+'.ld');ld.write_text('\n'.join(f'{k} = 0x{defs[k]:X};' for k in sorted(names))+'\n'+f'SECTIONS {{ .text 0x{v:X} : SUBALIGN(4) {{ *(.text) }} .rodata 0x{addr:X} : SUBALIGN(4) {{ *(.rodata) }} /DISCARD/ : {{ *(*) }} }}\n');elf=w/(label+'.elf');run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','--emit-relocs','-T',ld,'-o',elf,obj],co);return Elf32(elf.read_bytes())
   def verify(e):
    f=e.function(n);assert f.value==v and f.size==z and e.code(f)==code,'original text/extent';idx=e.names.index('.rodata');assert e.sections[idx][3]==pv and e.payload(idx)[:4]==rom[po:po+4] and not any(e.payload(idx)[4:]),'original pool';assert e.globals()[symbol]==pv,'pool symbol'
   for label,obj in [('named_link',named),('local_link',local_obj),('native_link',native),('native_local_link',other)]:verify(link(label,obj))
   negatives=[]
   wrongpool=assemble('wrong_pool',header+shadow+pool.replace(float_line,'.float 0.3'))
   wrongadd=assemble('wrong_addend',header+shadow.replace(llo,f'%lo({local}+4)')+pool)
   for label,obj,addr in [('wrong_pool_address',local_obj,pv+4),('wrong_pool_word',wrongpool,pv),('wrong_pool_addend',wrongadd,pv),('altered_C_float',bad,pv)]:
    try:verify(link(label,obj,addr))
    except AssertionError as e:negatives.append({'control':label,'rejected':True,'reason':str(e)})
    else:raise AssertionError('negative accepted '+label)
   row={'region':r,'name':n,'original_vma':v,'rom_offset':off,'original_bytes':z,'original_code_sha256':sha(code),'pool_symbol':symbol,'pool_vma':pv,'pool_rom_offset':po,'pool_word_sha256':sha(rom[po:po+4]),'original_asm_sha256':sha(body.encode()),'original_data_line_sha256':sha(dm[1].encode()),'independent_local_asm_sha256':sha(shadow.encode()),'native_sha256':sha(source.read_bytes()),'compiler_sha256':COMPILER,'flags':FLAGS,'ledger_sha256':lh,'named_relocations':sum(named_rel.values()),'local_relocations':sum(shadow_rel.values()),'native_relocations':sum(native_rel.values()),'named_removed':[list(x) for x in sorted(removed.elements())],'local_added':[list(x) for x in sorted(added.elements())],'named_original_gate_exact':False,'raw_local_text_and_relocations_exact':True,'linked_original_text_and_extent_exact':True,'original_pool_exact':True,'second_source_independent_replay_exact':True,'attempts':[{'source':str(source.relative_to(sources)),'sha256':sha(source.read_bytes()),'ledger_sha256':lh,'outcome':'EXISTING_QUIRK_REPRODUCED','first_named_mismatch_category':'relocation','first_named_mismatch_offset':min(x[0] for x in removed)},{'source':str((sources/n/'03_literal_local.c').relative_to(sources)),'sha256':sha((sources/n/'03_literal_local.c').read_bytes()),'ledger_sha256':lh2,'outcome':'EXISTING_QUIRK_REPRODUCED','first_named_mismatch_category':'relocation','first_named_mismatch_offset':min(x[0] for x in removed)},{'source':str(bad_source.relative_to(sources)),'sha256':sha(bad_source.read_bytes()),'ledger_sha256':lh3,'outcome':'NO_NEW_COMPILER_FINDING','negative':True,'first_mismatch_category':'literal_pool','first_mismatch_offset':po}],'negative_controls':negatives,'status':'RESEARCH_ONLY_INDEPENDENT_ASM_REFERENCE_EXACT','full_g2':'NOT_RUN'};proof.append(row);(a.work/'pool-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(n,z,len(native_rel),len(negatives),'PASS',flush=True)
if __name__=='__main__':main()

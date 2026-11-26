#!/usr/bin/env python3
"""Private original/mixed text-owner replay, independent of canonical G2."""
import argparse, hashlib, json, re, shutil, subprocess
from pathlib import Path
from collections import defaultdict
from decomp.consolidated_batch_promotion import text, rels, jp55, glitch, cross
from replay import run, sha
HEADER='.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'
WORD=re.compile(r'/\* ([0-9A-Fa-f]{5,8}) ([0-9A-Fa-f]{8}) ([0-9A-Fa-f]{8}) \*/')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--isolated',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
 rows=json.loads((a.isolated/'isolated-replay.json').read_text());groups=defaultdict(list);results=[]
 for x in rows:
  assert x['attempts'][0]['exact_raw'] and x['attempts'][0]['linked_original_rom_exact'] and not x['attempts'][1]['exact_raw']
  owner=Path(x['owner']);key=owner.parent if 'nonmatchings' in owner.parts else owner;groups[(x['region'],key)].append(x)
 for (r,owner),entries in sorted(groups.items(),key=lambda x:str(x[0])):
  co=a.usa if r=='usa' else a.jp;rom=(co/f'config/{r}/baserom.decompressed.z64').read_bytes();prefix=owner.stem;wd=a.work/(r+'-'+prefix);wd.mkdir();res={'region':r,'owner':str(owner),'targets':sorted(x['name'] for x in entries),'status':'FAILED'}
  try:
   if (co/owner).is_dir():
    src=co/'src'/f'{owner.name}.c';files=re.findall(r'^#pragma GLOBAL_ASM\("([^"]+)"\)',src.read_text(),re.M);assert files and all(Path(x).parent==owner for x in files);raw='\n'.join((co/x).read_text() for x in files);raw=HEADER+raw
   else:raw=(co/owner).read_text()
   words=[(int(o,16),int(v,16),int(w,16)) for o,v,w in WORD.findall(raw)];start,va=words[0][:2];end=words[-1][0]+4;original=rom[start:end];assert len(words)==(end-start)//4 and all(o==start+4*i and v==va+4*i and rom[o:o+4]==w.to_bytes(4,'big') for i,(o,v,w) in enumerate(words)), 'original owner comments not contiguous/authentic';res.update(rom_offset=start,vma=va,text_bytes=end-start,original_sha256=sha(original))
   def asm_obj(src,k,size):
    path=wd/(k+'.s');obj=wd/(k+'.o');path.write_text(src);run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',obj,path],co,wd/(k+'.as.log'));cross._trim_object(obj,size,b'');return obj
   ref=asm_obj(raw,'original',end-start);syms={}
   for path in list((co/f'config/{r}/symbol_addrs').rglob('*.txt'))+list((co/f'.splat/{r}').glob('undefined*.ld')):
    for k,x in re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9a-fA-F]+)\s*;',path.read_text(),re.M):syms[k]=int(x,16)
   undefined=set()
   for line in subprocess.check_output(['readelf','-Ws',ref],text=True).splitlines():
    q=line.split()
    if len(q)>=8 and q[6]=='UND':undefined.add(q[7])
   for name in undefined:
    if name not in syms:
     match=re.match(r'^(?:func|D|jtbl)_([0-9a-fA-F]+)(?:_|$)',name);assert match,('unresolved named symbol',name);syms[name]=int(match[1],16)
   ld=wd/'owner.ld';ld.write_text('\n'.join(f'{k} = 0x{syms[k]:X};' for k in sorted(undefined))+'\n'+f'SECTIONS {{ . = 0x{va:X}; .text : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(*) }} }}\n')
   def link(objs,k):
    elf=wd/(k+'.elf');binfile=wd/(k+'.bin');run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','--emit-relocs','-T',ld,'-o',elf,*objs],co,wd/(k+'.link.log'));run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binfile],co,wd/(k+'.copy.log'));return elf,binfile.read_bytes()
   refelf,refbytes=link([ref],'original');assert refbytes==original,'independent complete owner fails original ROM'
   blocks={m['name']:m for m in jp55.BLOCK.finditer(raw)};objs=[];cursor=0;off=start
   for i,x in enumerate(sorted(entries,key=lambda x:x['rom_offset'])):
    n=x['name'];m=blocks[n];assert x['rom_offset']>=off and m.start()>=cursor;frag=raw[cursor:m.start()];z=x['rom_offset']-off
    if z:
     assert jp55.word_span(frag)==(off,x['rom_offset']);objs.append(asm_obj(HEADER+frag,f'frag{i}',z))
    else:assert not WORD.search(frag),'unexpected original prefix bytes'
    obj=wd/(n+'.o');shutil.copyfile(a.isolated/(n+'.candidate.o'),obj);cross._trim_object(obj,x['original_bytes'],b'');objs.append(obj);off=x['rom_offset']+x['original_bytes'];cursor=m.end()
   if off<end:
    frag=raw[cursor:];assert jp55.word_span(frag)==(off,end);objs.append(asm_obj(HEADER+frag,'tail',end-off))
   else:assert not WORD.search(raw[cursor:])
   candelf,candbytes=link(objs,'mixed');res['mixed_text_sha256']=sha(candbytes);res['rom_exact']=candbytes==original
   f0,f1=cross._funcs(refelf),cross._funcs(candelf);res.update(original_functions=sum(f0.values()),mixed_functions=sum(f1.values()),function_identities_exact=f0==f1)
   rel0,n0,h0=glitch.all_semantic_relocations(refelf);rel1,n1,h1=glitch.all_semantic_relocations(candelf);res.update(original_relocations=n0,mixed_relocations=n1,original_reloc_sha256=h0,mixed_reloc_sha256=h1,semantic_relocations_exact=rel0==rel1)
   if rel0!=rel1:res.update(removed_relocations=[list(k)+[v] for k,v in (rel0-rel1).items()][:20],added_relocations=[list(k)+[v] for k,v in (rel1-rel0).items()][:20])
   res['status']='UNIT_TEXT_EXACT' if res['rom_exact'] and res['function_identities_exact'] and res['semantic_relocations_exact'] else 'FAILED'
  except (OSError,AssertionError,ValueError,KeyError,subprocess.CalledProcessError) as e:res['error']=str(e)
  results.append(res);(a.work/'owner-replay.json').write_text(json.dumps(results,indent=2)+'\n');print(r,owner,res['status'],{k:res.get(k) for k in ('text_bytes','original_functions','original_relocations','rom_exact','function_identities_exact','semantic_relocations_exact','error')},flush=True)
 if any(x['status']!='UNIT_TEXT_EXACT' for x in results):raise SystemExit(1)
if __name__=='__main__':main()

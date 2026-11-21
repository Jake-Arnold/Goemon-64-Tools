"""Fail-closed Japanese original-ROM trial integration for short/repeated native C.

Research source bundles are local inputs. This module does not make an isolated
match official. Promote only after exact ROM, ELF, all semantic relocs, and CI.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess
from collections import defaultdict
from pathlib import Path
from . import japan_noop_port as jp329
from . import japan_thirtyfour_c as jp34
from . import glitch_g2_promotion as glitch
from . import vm_g2_promotion as vm
from . import overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
SHA1='6f8745fecc3a5e7d4918c7a73353eb0726116ded'

DEFAULT_BUNDLES=ROOT/'research/jp_tiny7_20261121'
BLOCK=re.compile(r'(?ms)^nonmatching (?P<name>[A-Za-z_][A-Za-z_0-9]*), 0x(?P<size>[0-9a-fA-F]+)\s*\n.*?^endlabel (?P=name)[^\n]*\n')
STAGE=Path('build/japan_0/jptiny7-stage.json')

def sha(b):return hashlib.sha256(b).hexdigest()
def original(co):
 b=(co/'config/japan_0/baserom.decompressed.z64').read_bytes()
 if len(b)!=33554432 or hashlib.sha1(b).hexdigest()!=SHA1:raise ValueError('Wrong Japanese original ROM')
 return b

def load_sources(basedir):
 j=json.loads((basedir/'manifest.json').read_text())
 rows=[]
 for rec in j['functions']:
  src=basedir/'sources'/(rec['name']+'.c')
  if not src.exists() or sha(src.read_bytes())!=rec['source_sha256']:
   raise ValueError('Source SHA-256 drift '+rec['name'])
  rows.append(dict(name=rec['name'],off=int(rec['rom_offset'],16),size=rec['size'],original_sha=rec['original_sha256'],source_sha=rec['source_sha256'],relocations=rec['relocations'],source=src,batch='tiny7'))
 if len(rows)!=7 or len({r['name'] for r in rows})!=7 or len({r['off'] for r in rows})!=7:
  raise ValueError('Incorrect tiny7 target count or duplicate offsets')
 return sorted(rows,key=lambda x:x['off'])

def parse_owner(co,ld,targets):
 owners=re.findall(r'(?m)^\s*build/japan_0/(asm/japan_0/[^\s()]+\.s)\.o\(\.text\);',ld)
 maps={}; cache={}
 for own in owners:
  raw=(co/own).read_text()
  ms=list(BLOCK.finditer(raw))
  if not ms:continue
  cache[own]=(raw,ms)
  for m in ms:
   if m['name'] not in targets:continue
   if m['name'] in maps:raise ValueError('Duplicate ASM active target '+m['name'])
   maps[m['name']]=(own,m)
 return maps,cache

def word_span(raw):
 from . import overlay_wide132 as wide
 words=[int(x,16) for x in wide.TEXT_WORD.findall(raw)]
 if not words or any(b-a!=4 for a,b in zip(words,words[1:])):
  raise ValueError('Non-contiguous generated ASM source span')
 return words[0],words[-1]+4

def plan(co,basedir,selected=None):
 rom=original(co); linker=co/'.splat/japan_0/mnsg.ld';ld=linker.read_text()
 if not (co/'build/japan_0/vm-g2-stage.json').is_file():raise ValueError('Missing published JP2123 baseline stage')
 if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom:raise ValueError('Prior JP2123 baseline not exact')
 rows=load_sources(basedir)
 if selected is not None: rows=[r for r in rows if r['name'] in selected]
 if not rows:raise ValueError('Empty candidate selection')
 maps,cache=parse_owner(co,ld,{r["name"] for r in rows})
 byowner=defaultdict(list); blocked=[]
 for r in rows:
  n=r['name'];off=r['off'];size=r['size']
  if sha(rom[off:off+size])!=r['original_sha']:raise ValueError('Original ROM function hash drift '+n)
  if n not in maps:blocked.append({'name':n,'reason':'No active exact ASM owner'});continue
  owner,m=maps[n]
  if int(m['size'],16)!=size or word_span(cache[owner][0][m.start():m.end()])!=(off,off+size):
   blocked.append({'name':n,'reason':'Owner size or ROM extent mismatch'});continue
  byowner[owner].append(r)
 # Require a bounded, truthful selection: never silently claim that blocked rows were staged.
 return {'rom':rom,'linker':linker,'ld':ld,'byowner':byowner,'cache':cache,'blocked':blocked,'requested':len(rows)}

def stage(co,basedir,selected=None):
 x=plan(co,basedir,selected)
 root=co/'src/jptiny7'
 if root.exists() or (co/STAGE).exists():raise ValueError('Stale JP jptiny7 stage')
 ld=x['ld'];entries=[];fragments=[];skipped=list(x['blocked']);owners=[]
 for owner,rows in sorted(x['byowner'].items()):
  raw,ms=x['cache'][owner];rows.sort(key=lambda r:r['off'])
  oldobj=co/f'build/japan_0/{owner}.o'
  try:
   glitch.check_nontext(oldobj)
   _o,size,code,align=jp329.text_section(oldobj)
   oldfirst=word_span(raw[ms[0].start():ms[0].end()])[0]
   oldend=oldfirst+size
   # Original object text includes no unanchored bytes beyond its terminal span.
   last=word_span(raw[ms[-1].start():ms[-1].end()])[1]
   if last!=oldend:
    suffix=raw[ms[-1].end():]
    # Preserve original alignment NOPs as ASM, not fabricated C or patched ROM.
    if word_span(suffix)!=(last,oldend):raise ValueError('Unowned trailing bytes')
    if x['rom'][last:oldend]!=bytes(oldend-last):raise ValueError('Nonzero trailing original code')
    if code[-(oldend-last):]!=bytes(oldend-last):raise ValueError('Nonzero trailing original ASM owner code')
   if any(r['name'] not in {m['name'] for m in ms} for r in rows):raise ValueError('Unowned candidate')
   replacement=[];cursor=ms[0].start();before=oldfirst;header=raw[:ms[0].start()];byname={m['name']:m for m in ms}
   local=[];pieces=[]
   for idx,r in enumerate(rows):
    m=byname[r['name']];off=r['off'];after=off+r['size']
    if off<before or m.start()<cursor:raise ValueError('Overlapping candidate blocks')
    if off>before:
     frag=raw[cursor:m.start()]
     if word_span(frag)!=(before,off):raise ValueError('ASM gap not contiguous')
     name=f'jptiny7_{Path(owner).stem.replace(".","_")}_{idx:02}.s'
     path=f'asm/japan_0/{name}'
     pieces.append(('asm',path,header+frag,before,off))
     replacement.append(f'build/japan_0/{path}.o')
    elif re.search(r'(?m)^\s*/\*\s*[A-F0-9]{4}',raw[cursor:m.start()]):raise ValueError('Unowned instructions in boundary')
    path=f'src/jptiny7/{r["name"]}.c';pieces.append(('c',path,r['source'].read_bytes(),off,after))
    replacement.append(f'build/japan_0/{path}.o')
    local.append(dict(name=r['name'],rom_offset=off,size=r['size'],source=path,
       source_sha256=r['source_sha'],original_code_sha256=r['original_sha'],owner=owner,
       relocations=r['relocations'],batch=r['batch']))
    cursor=m.end();before=after
   if before<oldend:
    frag=raw[cursor:]
    if word_span(frag)!=(before,oldend):raise ValueError('Trailing ASM gap not contiguous')
    name=f'jptiny7_{Path(owner).stem.replace(".","_")}_tail.s';path=f'asm/japan_0/{name}'
    pieces.append(('asm',path,header+frag,before,oldend));replacement.append(f'build/japan_0/{path}.o')
   needle=f'build/japan_0/{owner}.o(.text);'
   if ld.count(needle)!=1:raise ValueError('ASM owner linked in non-unique .text')
   for sec in ('.data','.rodata','.bss','.sdata','.sbss'):
    if ld.count(f'build/japan_0/{owner}.o({sec});')>1:raise ValueError('Nontext owner duplicated')
   owners.append((owner,replacement,pieces,local))
  except Exception as e:
   for r in rows:skipped.append({'name':r['name'],'reason':str(e)})
 if not owners:raise ValueError('No replaceable original ASM owners: '+str(skipped[:7]))
 root.mkdir(parents=True)
 for owner,replacement,pieces,local in owners:
  needle=f'build/japan_0/{owner}.o(.text);'
  ld=ld.replace(needle,'\n'.join('        '+q+'(.text);' for q in replacement),1)
  for sec in ('.data','.rodata','.bss','.sdata','.sbss'):
   ld=ld.replace(f'build/japan_0/{owner}.o({sec});','')
  if f'build/japan_0/{owner}.o(' in ld:raise ValueError('Unexpected original owner residual '+owner)
  for kind,path,data,start,end in pieces:
   dest=co/path;dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():raise ValueError('Candidate path collision '+path)
   dest.write_bytes(data if isinstance(data,bytes) else data.encode())
   if kind=='asm':fragments.append(dict(path=path,start=start,end=end))
  entries+=local
 x['linker'].write_text(ld)
 record={'format':'goemon-jp-tiny7-integrated-trial-v1','status':'STAGED_ONLY','requested':x['requested'],
   'staged_count':len(entries),'functions':entries,'skipped':skipped,'asm_fragments':fragments,
   'original_rom_sha1':SHA1,'baseline_c':2282,'expected_elf':7376,'expected_relocations':80747}
 (co/STAGE).write_text(json.dumps(record,indent=2)+'\n')
 return record

def build(co,deps,runtime):
 report=json.loads((co/STAGE).read_text())
 if not report['functions']:raise ValueError('No C to build')
 env=jp329.env_for(deps,runtime)
 pre=json.loads((co/'build/japan_0/glitch-g2-stage.json').read_text())
 v=json.loads((co/'build/japan_0/vm-g2-stage.json').read_text())
 sources=[e['source'] for e in pre['new_functions']]+[e['source'] for e in v['functions']]+[e['source'] for e in report['functions']]
 args=glitch.makeargs(co,'japan_0',{'new_functions':[{'source':s} for s in sources]})
 objects=['build/japan_0/'+e['source']+'.o' for e in report['functions']]
 objects+=['build/japan_0/'+p['path']+'.o' for p in report['asm_fragments']]
 subprocess.run(args+objects,env=env,cwd=co,check=True,stdout=subprocess.DEVNULL)
 from .japan_thirtyfour_c import pack_text_metadata
 for e in report['functions']:
  obj=co/f'build/japan_0/{e["source"]}.o'
  if sha((co/e['source']).read_bytes())!=e['source_sha256']:raise ValueError('Compiled source changed '+e['name'])
  _,n,_,align=jp329.text_section(obj)
  if n not in (e['size'],(e['size']+15)&~15) or align not in (4,16):raise ValueError('Wrong C code size/align '+e['name']+f' got {n}/{align}')
  if n!=e['size'] or align!=4:obj.write_bytes(pack_text_metadata(obj.read_bytes(),e['size'])[0])
  _,n,_,align=jp329.text_section(obj)
  if n!=e['size'] or align!=4:raise ValueError('C final object invalid '+e['name'])
 for p in report['asm_fragments']:
  obj=co/f'build/japan_0/{p["path"]}.o';expected=p['end']-p['start']
  _,n,_,align=jp329.text_section(obj)
  if n not in (expected,(expected+15)&~15) or align not in (4,16):raise ValueError('ASM fragment wrong extent '+p['path']+f' got {n}/{align}')
  if n!=expected or align!=4:obj.write_bytes(pack_text_metadata(obj.read_bytes(),expected)[0])
 for target in ('mnsg.elf','mnsg.z64'):
  f=co/'build/japan_0'/target
  if f.exists():f.unlink()
 subprocess.run(args+['build/japan_0/mnsg.z64'],env=env,cwd=co,check=True,stdout=subprocess.DEVNULL)
 rom=original(co);actual=(co/'build/japan_0/mnsg.z64').read_bytes()
 first=next((i for i,(a,b) in enumerate(zip(rom,actual)) if a!=b),None)
 result={'status':'FULL_ROM_BYTE_IDENTICAL' if first is None and len(rom)==len(actual) else 'FAILED_ROM',
   'original_rom_bytes':len(rom),'produced_rom_bytes':len(actual),'first_mismatch':first,
   'rebuilt_sha1':hashlib.sha1(actual).hexdigest()}
 (co/'build/japan_0/jptiny7-build.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def verify(co,base):
 report=json.loads((co/STAGE).read_text())
 rom=original(co)
 if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom or (base/'build/japan_0/mnsg.z64').read_bytes()!=rom:
  raise ValueError('FAILED_ROM: complete 32 MiB mismatch')
 oldelf=base/'build/japan_0/mnsg.elf';newelf=co/'build/japan_0/mnsg.elf'
 oldid=cross._funcs(oldelf);newid=cross._funcs(newelf)
 if oldid!=newid or sum(newid.values())!=7376:raise ValueError('FAILED_ELF: original function identities changed')
 old,n,h=glitch.all_semantic_relocations(oldelf);new,n2,h2=glitch.all_semantic_relocations(newelf)
 if n!=80747 or n2!=n or old!=new:
  raise ValueError(f'FAILED_RELOC: {n}/{n2} removed={list((old-new).items())[:5]} added={list((new-old).items())[:5]}')
 # Must preserve the original canonical relocation digest from JP2123 too.
 if h!='e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20' or h2!=h:
  raise ValueError('FAILED_RELOC: original relocation digest drift')
 def classified(elf):
  from . import japan_1686_promotion as jp1686
  text=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(elf)],text=True)
  funcs={}; marked=set()
  for line in text.splitlines():
   m=jp1686.jp39.F_SYMBOL.fullmatch(line)
   if not m:continue
   ad,kind,sec,size,name=m.groups()
   if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
   if kind=='F' and int(size,16)>0:funcs[name]=(sec,int(ad,16),int(size,16))
   elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
  return set(funcs)-marked
 before=classified(oldelf);after=classified(newelf)
 expected={e['name'] for e in report['functions']}
 if len(before)!=2282 or len(after)!=2282+len(expected) or after-before!=expected or before-after:
  raise ValueError(f'FAILED_INVENTORY: baseline {len(before)} final {len(after)} +{len(after-before)} -{len(before-after)}')
 result={'status':'PASSED_G2_LOCAL','matched_c_before':2282,'matched_c_after':len(after),
   'new_matching_c':len(expected),'new_original_code_bytes':sum(e['size'] for e in report['functions']),
   'matching_c_bytes':122124+sum(e['size'] for e in report['functions']),
   'assembly_remaining':7376-len(after),'rom_bytes':len(rom),'rom_sha1':SHA1,
   'elf_identities':7376,'semantic_relocations':n,'semantic_relocation_sha256':h,
   'names':sorted(expected),'skipped':report['skipped'],'publication':'NOT_YET'}
 (co/'build/japan_0/jptiny7-g2-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def cli():
 p=argparse.ArgumentParser();p.add_argument('action',choices=('plan','stage','build','verify'))
 p.add_argument('--checkout',required=True,type=Path);p.add_argument('--base',type=Path)
 p.add_argument('--bundles',type=Path,default=DEFAULT_BUNDLES);p.add_argument('--selection',type=Path)
 p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path)
 a=p.parse_args();co=a.checkout.resolve()
 selected={n.strip() for n in a.selection.read_text().splitlines() if n.strip()} if a.selection else None
 if a.action=='plan':
  x=plan(co,a.bundles.resolve(),selected)
  result=dict(requested=x['requested'],replaceable=sum(map(len,x['byowner'].values())),owner_count=len(x['byowner']),blocked=x['blocked'])
 elif a.action=='stage':result=stage(co,a.bundles.resolve(),selected)
 elif a.action=='build':result=build(co,a.deps.resolve(),a.runtime.resolve())
 else:result=verify(co,a.base.resolve())
 if a.action!='stage':print(json.dumps(result,indent=2)[:20000])
 else:print(json.dumps({k:v for k,v in result.items() if k not in ('functions','asm_fragments')},indent=2)[:20000])
if __name__=='__main__':cli()

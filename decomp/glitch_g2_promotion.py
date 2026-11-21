"""Fail-closed original-ROM integration of five verified Start/VM functions.

Run *after* a full, independently verified existing JP2118 or USA1956 build.
ROMs, generated assembly, linked binaries remain local, outside Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from . import japan_noop_port as jp329
from . import japan_thirtyfour_c as jp34
from . import japan_usa_main_three as jp432
from . import japan_1686_promotion as jp1686
from . import overlay_crossregion47 as cross
from . import overlay_wide132 as wide

ROOT=Path(__file__).resolve().parent
SOURCES=ROOT/'research/glitch_g2_20261121/sources'
REGIONS={
 'japan_0':dict(rom_sha1='6f8745fecc3a5e7d4918c7a73353eb0726116ded',baseline=2118,oldbytes=111856,expected_relocs=80747,reloc_sha256='e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20',c_offset=0,targets=[
  ('func_8001F580_20180',0x20180,100,'jp_gameplay_dispatch.c'),
  ('func_8001F610_20210',0x20210,252,'jp_gameplay_start.c'),
  ('func_8003EE44_3FA44',0x3FA44,36,'jp_vm_busy.c')]),
 'usa':dict(rom_sha1='6ea0ed71032ce08fc2745f412d84936382197494',baseline=1956,oldbytes=83940,expected_relocs=82103,reloc_sha256='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97',c_offset=13,targets=[
  ('func_8001F8B0_204B0',0x204B0,100,'usa_rotation_angles.c'),
  ('func_8001F940_20540',0x20540,252,'usa_rotation_angles.c')])}

def sha1(blob):return hashlib.sha1(blob).hexdigest()
def sha256(blob):return hashlib.sha256(blob).hexdigest()
def org(checkout,region):
 p=checkout/f'config/{region}/baserom.decompressed.z64'
 b=p.read_bytes()
 assert len(b)==33554432 and sha1(b)==REGIONS[region]['rom_sha1'], 'Wrong original ROM'
 return b

def current_stage_parts(checkout,region):
 if region=='japan_0':
  p=checkout/'build/japan_0/jp1686-stage.json'
  assert p.exists(), 'Missing verified JP1686 pre-stage'
  d=json.loads(p.read_text());assert d['candidate_count']==1686
  return d
 p=checkout/'build/usa/mnsg.z64';assert p.exists(),'Missing USA1956 staged ROM'
 return {}

def text_blocks(raw):
 ms=list(jp329.BLOCK.finditer(raw))
 if not ms:raise ValueError('No original ASM function definitions')
 return ms

def asm_span(piece):
 words=[int(x,16) for x in wide.TEXT_WORD.findall(piece)]
 if not words or any(b-a!=4 for a,b in zip(words,words[1:])):
  raise ValueError('Fragment has non-contiguous original ASM instruction comments')
 return words[0],words[-1]+4

def check_nontext(obj):
 # Require a purely text function-owner object; only then remove its .bss link.
 o=subprocess.check_output(['readelf','-SW',str(obj)],text=True)
 for x in o.splitlines():
  m=re.search(r'\]\s+\.(?:data|rodata|bss|sdata|sbss)\s+\S+\s+\S+\s+\S+\s+([0-9a-fA-F]{6,})\s+',x)
  if m and int(m[1],16):raise ValueError('Nonzero original nontext owner '+str(obj))

def stage_usa(checkout):
 """Promote two original USA pragmas within their existing mixed C/ASM owner.

 Unlike Japan, USA's original region already links rotation_angles.c (which
 includes three accepted C functions and an unrelated retained ASM pragma).
 """
 region='usa'
 checkout=Path(checkout).resolve();cfg=REGIONS[region];rom=org(checkout,region)
 current_stage_parts(checkout,region)
 if (checkout/'build/usa/mnsg.z64').read_bytes()!=rom:
  raise ValueError('USA baseline ROM not exact before promotion')
 stage_file=checkout/'build/usa/glitch-g2-stage.json'
 dest=checkout/'src/rotation_angles.c'
 original=dest.read_bytes()
 original_sha='80357db43c81ae9d794f95da4e2e836dd9f729f083b3204c5e46d8d641fb947e'
 if stage_file.exists() or sha256(original)!=original_sha:
  raise ValueError('USA mixed owner source is not the pinned accepted baseline')
 for name,off,size,source in cfg['targets']:
  pragma=f'#pragma GLOBAL_ASM("asm/usa/nonmatchings/rotation_angles/{name}.s")'
  if original.decode().count(pragma)!=1:
   raise ValueError('Missing original USA ASM pragma '+name)
 new=(SOURCES/'usa_rotation_angles.c').read_bytes()
 new_sha='72742e59bf097de609062aac468e8dd3a11473939e67134f7853bc6c19050710'
 if sha256(new)!=new_sha or any(name not in new.decode() for name,_,_,_ in cfg['targets']):
  raise ValueError('USA replacement mixed C/ASM owner drift')
 if b'func_8001FA80_20680.s' not in new:
  raise ValueError('USA unrelated pause handler must remain original ASM')
 dest.write_bytes(new)
 rows=[]
 for name,off,size,source in cfg['targets']:
  rows.append(dict(name=name,rom_offset=off,vma=int(name.split('_')[1],16),size=size,
       source='src/rotation_angles.c',source_sha256=new_sha,
       original_code_sha256=sha256(rom[off:off+size]),owner='rotation_angles.c'))
 stage_data={'format':'goemon-start-five-g2-stage-v1','region':'usa','old_c_count':cfg['baseline'],
  'new_functions':rows,'asm_fragments':[],'original_sha1':cfg['rom_sha1'],
  'previous_owner_sha256':original_sha,'staged_owner_sha256':new_sha}
 stage_file.write_text(json.dumps(stage_data,indent=2)+'\n')
 return stage_data

def stage(checkout,region):
 if region=='usa':return stage_usa(checkout)
 checkout=Path(checkout).resolve();cfg=REGIONS[region];rom=org(checkout,region)
 current_stage_parts(checkout,region)
 old=(checkout/f'build/{region}/mnsg.z64').read_bytes()
 if old!=rom:raise ValueError('Existing region not full-ROM exact before staging')
 root=checkout/'src/glitch_g2'
 out=checkout/f'build/{region}/glitch-g2-stage.json'
 if root.exists() or out.exists():raise ValueError('Stale glitch G2 stage')
 linker=checkout/f'.splat/{region}/mnsg.ld'
 ld=linker.read_text()
 active=re.findall(r'(?m)^\s*build/'+region+r'/asm/'+region+r'/([^\s()]+\.s)\.o\(\.text\);',ld)
 owners={};by_owner=defaultdict(list)
 targets=cfg['targets']
 for name,off,size,source in targets:
  assert off+size<=len(rom)
  romslice=rom[off:off+size]
  if len(romslice)!=size:raise ValueError('Outside original image')
  assert (SOURCES/source).is_file()
  found=[]
  for a in active:
   path=checkout/'asm'/region/a
   if not path.exists():raise ValueError('Missing referenced ASM '+a)
   s=path.read_text()
   m=re.search(r'(?m)^nonmatching '+re.escape(name)+r', 0x([0-9a-fA-F]+)$',s)
   if m:found.append((a,int(m[1],16)))
  if len(found)!=1 or found[0][1]!=size:
   raise ValueError('Target missing/duplicate in currently owned original ASM: '+name+': '+repr(found))
  own=found[0][0]
  if name in owners:raise ValueError('Duplicate target')
  owners[name]=own;by_owner[own].append((name,off,size,source))
 if len(owners)!=len(targets):raise ValueError('Lost target')
 root.mkdir(parents=True)
 entries=[];splits=[]
 for oldname,rows in sorted(by_owner.items()):
  rows.sort(key=lambda x:x[1])
  path=checkout/'asm'/region/oldname
  raw=path.read_text()
  ms=text_blocks(raw)
  header=raw[:ms[0].start()]
  check_nontext(checkout/f'build/{region}/asm/{region}/{oldname}.o')
  all_names={m['name']:m for m in ms}
  for name,off,size,source in rows:
   match=all_names.get(name)
   if match is None or int(match['size'],16)!=size:
    raise ValueError('Original Splat name, extent drift: '+name)
   if asm_span(raw[match.start():match.end()])!=(off,off+size):
    raise ValueError('Original instruction span changed '+name)
  prefix=f'build/{region}/asm/{region}/{oldname}.o'
  marker=prefix+'(.text);'
  if ld.count(marker)!=1:raise ValueError('Original ASM owner not unique in linker '+oldname)
  replacements=[];cursor=ms[0].start()
  old_first=asm_span(raw[ms[0].start():ms[0].end()])[0]
  previous=old_first
  for i,(name,off,size,source) in enumerate(rows):
   m=all_names[name]
   if off<previous or m.start()<cursor:raise ValueError('Overlap in original owner '+oldname)
   if off>previous:
    frag=raw[cursor:m.start()]
    if asm_span(frag)!=(previous,off):raise ValueError('Unowned ASM gap '+oldname)
    part=f'glitch_{oldname[:-2]}_{i:02}.s';outasm=checkout/'asm'/region/part
    if outasm.exists():raise ValueError('Fragment collision')
    outasm.write_text(header+frag)
    replacements.append(f'build/{region}/asm/{region}/{part}.o')
    splits.append({'path':f'asm/{region}/{part}','start':previous,'end':off})
   elif wide.TEXT_WORD.search(raw[cursor:m.start()]):raise ValueError('Unexpected instruction before C '+name)
   srcroot=root/source
   if srcroot.exists():raise ValueError('Duplicate source '+source)
   content=(SOURCES/source).read_bytes();srcroot.write_bytes(content)
   replacements.append(f'build/{region}/src/glitch_g2/{source}.o')
   entries.append({'name':name,'rom_offset':off,'vma':int(name.split('_')[1],16),'size':size,
                   'source':str(srcroot.relative_to(checkout)),'source_sha256':sha256(content),
                   'original_code_sha256':sha256(rom[off:off+size]),'owner':oldname})
   previous=off+size;cursor=m.end()
  last_end=asm_span(raw[ms[-1].start():ms[-1].end()])[1]
  if last_end>previous:
   frag=raw[cursor:]
   if asm_span(frag)!=(previous,last_end):raise ValueError('Lost trailing ASM '+oldname)
   part=f'glitch_{oldname[:-2]}_tail.s';outasm=checkout/'asm'/region/part
   if outasm.exists():raise ValueError('ASM tail collision')
   outasm.write_text(header+frag)
   replacements.append(f'build/{region}/asm/{region}/{part}.o')
   splits.append({'path':f'asm/{region}/{part}','start':previous,'end':last_end})
  if len(set(replacements))!=len(replacements):raise ValueError('Duplicate object')
  ld=ld.replace(marker,'\n'.join('        '+item+'(.text);' for item in replacements),1)
  for sect in ('.data','.rodata','.bss','.sdata','.sbss'):
   needle=prefix+f'({sect});'
   if ld.count(needle)>1:raise ValueError('Unreviewed repeated nontext owner '+oldname)
   ld=ld.replace(needle,'')
  # Ensure none of original owner's ELF sections remain linked.
  if prefix+'(' in ld:raise ValueError('Original owner still linked in unexpected section '+oldname)
 linker.write_text(ld)
 assert len(entries)==len(targets)
 result={'format':'goemon-start-five-g2-stage-v1','region':region,'old_c_count':cfg['baseline'],
         'new_functions':entries,'asm_fragments':splits,'original_sha1':cfg['rom_sha1']}
 out.write_text(json.dumps(result,indent=2)+'\n')
 return result

def makeargs(checkout,region,plan):
 if region=='usa':return ['make','-j3','VERSION=usa']
 bas=jp432.jp429.full_c_list(checkout,jp432.jp429.manifest())
 bas+=' '+' '.join('src/jp_main3/'+r['jp']+'.c' for r in jp432.manifest()['functions'])
 jpstage=json.loads((checkout/'build/japan_0/jp1686-stage.json').read_text())
 prev=sorted(set(p['path'] for p in jpstage['parts'] if p['kind']=='c'))
 new=[f['source'] for f in plan['new_functions']]
 return ['make','-j3','VERSION=japan_0','C_FILES='+bas+' '+' '.join(prev+new)]

def do_build_usa(checkout,deps,runtime):
 checkout=Path(checkout).resolve();region='usa'
 data=json.loads((checkout/'build/usa/glitch-g2-stage.json').read_text())
 expected=data['staged_owner_sha256']
 owner=checkout/'src/rotation_angles.c'
 if sha256(owner.read_bytes())!=expected or len(data['new_functions'])!=2:
  raise ValueError('USA staged owner has drifted')
 env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
 # Existing USA baseline already contains all other accepted C and ASM owners.
 obj=checkout/'build/usa/src/rotation_angles.c.o'
 if obj.exists():obj.unlink()
 subprocess.run(['make','-j3','VERSION=usa','build/usa/src/rotation_angles.c.o'],
                cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 for fn in data['new_functions']:
  syms=subprocess.check_output(['readelf','-Ws',str(obj)],text=True,env=env)
  found=[]
  for row in syms.splitlines():
   q=row.split()
   if len(q)>7 and q[3]=='FUNC' and q[7]==fn['name'] and q[6] not in ('ABS','UND'):
    found.append(int(q[2]))
  if found!=[fn['size']]:raise ValueError('USA C compiled function size drift '+fn['name']+repr(found))
 for name in ('mnsg.elf','mnsg.z64'):
  p=checkout/'build/usa'/name
  if p.exists():p.unlink()
 subprocess.run(['make','-j3','VERSION=usa','build/usa/mnsg.z64'],
                cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 rom=org(checkout,region);new=(checkout/'build/usa/mnsg.z64').read_bytes()
 if new!=rom:raise ValueError('FAILED_ROM USA original 32 MiB not exact')
 result={'stage':'native-build','full_rom_bytes':len(rom),'full_rom_sha1':sha1(new),
         'new_c_objects':[{'function':r['name'],'object':'build/usa/src/rotation_angles.c.o'} for r in data['new_functions']],
         'asm_fragments':0}
 (checkout/'build/usa/glitch-g2-built.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def do_build(checkout,region,deps,runtime):
 if region=='usa':return do_build_usa(checkout,deps,runtime)
 checkout=Path(checkout).resolve();stage=json.loads((checkout/f'build/{region}/glitch-g2-stage.json').read_text())
 env=jp329.env_for(Path(deps).resolve(),Path(runtime).resolve())
 base=makeargs(checkout,region,stage)
 sourceobjs=[f'build/{region}/{e["source"]}.o' for e in stage['new_functions']]
 asmobjs=[f'build/{region}/{p["path"]}.o' for p in stage['asm_fragments']]
 subprocess.run(base+sourceobjs+asmobjs,cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 rom=org(checkout,region)
 objs=[]
 for ent in stage['new_functions']:
  obj=checkout/f'build/{region}/{ent["source"]}.o'
  if sha256((checkout/ent['source']).read_bytes())!=ent['source_sha256']:
   raise ValueError('Compiled Japanese C source drift '+ent['name'])
  # Original C may have R_MIPS relocations; linked ROM AND all relocations are authoritative.
  _o,n,contents,align=jp329.text_section(obj)
  size=ent['size']
  if n not in (size,(size+15)&~15) or align not in (4,16):
   raise ValueError(f'Native C object extent/align mismatch {ent["name"]}: {n}/{align} vs {size}')
  if n!=size or align!=4:
   obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),size)[0])
  _,n,contents,a=jp329.text_section(obj)
  if n!=size or a!=4:raise ValueError('C object packing changed original extent')
  syms=subprocess.check_output(['readelf','-Ws',str(obj)],env=env,text=True)
  matches=[]
  for row in syms.splitlines():
   parts=row.split()
   if len(parts)>7 and parts[3]=='FUNC' and parts[7]==ent['name'] and parts[6] not in ('UND','ABS'):
    matches.append((int(parts[1],16),int(parts[2])))
  if matches!=[(0,size)]:raise ValueError('C ELF symbol name/VMA extent mismatch '+ent['name']+repr(matches))
  objs.append({'function':ent['name'],'text_bytes':n,'object':str(obj.relative_to(checkout))})
 for p in stage['asm_fragments']:
  obj=checkout/f'build/{region}/{p["path"]}.o'
  _o,n,c,align=jp329.text_section(obj)
  expected=p['end']-p['start']
  if n not in (expected,(expected+15)&~15) or align not in (4,16):
   raise ValueError('ASM fragment extent differs '+str(p))
  if n!=expected or align!=4:obj.write_bytes(jp34.pack_text_metadata(obj.read_bytes(),expected)[0])
  _,n,c,align=jp329.text_section(obj)
  if n!=expected or align!=4:raise ValueError('ASM fragment final metadata differed')
 # Force fresh ELF/ROM from modified linker.
 for name in ('mnsg.elf','mnsg.z64'):
  p=checkout/f'build/{region}/{name}'
  if p.is_file():p.unlink()
 subprocess.run(base+[f'build/{region}/mnsg.z64'],cwd=checkout,env=env,check=True,stdout=subprocess.DEVNULL)
 actual=(checkout/f'build/{region}/mnsg.z64').read_bytes()
 mismatch=next((i for i,(a,b) in enumerate(zip(actual,rom)) if a!=b),None)
 if len(actual)!=len(rom) or mismatch is not None:
  raise ValueError(f'FAILED_ROM region={region} size={len(actual)} first_mismatch={mismatch} actual_sha1={sha1(actual)}')
 result={'stage':'native-build','full_rom_bytes':len(rom),'full_rom_sha1':sha1(actual),'new_c_objects':objs,'asm_fragments':len(stage['asm_fragments'])}
 (checkout/f'build/{region}/glitch-g2-built.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def all_semantic_relocations(elf):
 """Read *all* ELF .rel sections, including the original .rel.main.

 The older cross._relocations helper covers overlay sections only and would
 silently accept lost R_MIPS_HI16/LO16 pairs in main code.
 """
 raw=subprocess.check_output(['readelf','-r','-W',str(elf)],text=True)
 section='';result=[]
 for line in raw.splitlines():
  sec=re.search(r"^Relocation section '([^']+)'",line)
  if sec:section=sec.group(1);continue
  m=re.match(r'^\s*([0-9a-fA-F]{8,16})\s+([0-9a-fA-F]{8})\s+(R_MIPS_[A-Z0-9_]+)\s+([0-9a-fA-F]{8,16})\s+(\S+)',line)
  if m:
   addr,_,kind,value,name=m.groups()
   result.append((section,int(addr,16),kind,int(value,16),name))
 out=sorted(result)
 payload='\n'.join(f'{sec}|{addr:08x}|{kind}|{value:08x}|{name}' for sec,addr,kind,value,name in out)+'\n'
 return Counter(result),len(result),sha256(payload.encode())

def verify(checkout,baseline,region):
 checkout=Path(checkout).resolve();baseline=Path(baseline).resolve()
 rom=org(checkout,region)
 new=(checkout/f'build/{region}/mnsg.z64').read_bytes()
 old=(baseline/f'build/{region}/mnsg.z64').read_bytes()
 assert new==old==rom and sha1(new)==REGIONS[region]['rom_sha1'], 'FAILED_ROM full 32 MiB image mismatch'
 newelf=checkout/f'build/{region}/mnsg.elf'
 oldelf=baseline/f'build/{region}/mnsg.elf'
 if not oldelf.exists():raise ValueError('No original accepted baseline ELF')
 before=cross._funcs(oldelf);after=cross._funcs(newelf)
 if before!=after or sum(after.values())!=7376:
  a=before-after;b=after-before
  raise ValueError(f'ELF original function identities changed: -{list(a.items())[:5]} +{list(b.items())[:5]}')
 oldrel,n_old,h_old=all_semantic_relocations(oldelf)
 newrel,n_new,h_new=all_semantic_relocations(newelf)
 if n_old!=REGIONS[region]['expected_relocs'] or n_old!=n_new or oldrel!=newrel or h_old!=h_new or h_old!=REGIONS[region]['reloc_sha256']:
  raise ValueError(f'FAILED_RELOC region={region}: baseline={n_old}/{h_old}, new={n_new}/{h_new}, removed={(oldrel-newrel).most_common(6)}, added={(newrel-oldrel).most_common(6)}')
 stage=json.loads((checkout/f'build/{region}/glitch-g2-stage.json').read_text())
 import subprocess
 symbols=subprocess.check_output(['readelf','-W','-s',str(newelf)],text=True)
 for e in stage['new_functions']:
  if e['name'] not in symbols:raise ValueError('Missing new original ELF name: '+e['name'])
  if rom[e['rom_offset']:e['rom_offset']+e['size']]!=new[e['rom_offset']:e['rom_offset']+e['size']]:
   raise ValueError('New function original ROM bytes mismatch '+e['name'])
 # Strict source status: old marked as ASM and new no longer marked as ASM.
 def c_labels(elf):
  text=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(elf)],text=True)
  funcs={};marked=set()
  for line in text.splitlines():
   q=jp1686.jp39.F_SYMBOL.fullmatch(line)
   if not q:continue
   adr,kind,sec,size,name=q.groups()
   if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
   if kind=='F' and int(size,16)>0:funcs[name]=(sec,int(adr,16),int(size,16))
   elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
  return set(funcs)-marked
 old_c=c_labels(oldelf);new_c=c_labels(newelf)
 expected_new={r['name'] for r in stage['new_functions']}
 if (new_c-old_c)!=expected_new or (old_c-new_c) or len(old_c)!=REGIONS[region]['baseline']+REGIONS[region]['c_offset']:
  raise ValueError(f'Strict C/ASM identity mismatch: old={len(old_c)} new={len(new_c)} added={(new_c-old_c)} removed={(old_c-new_c)}')
 if len(new_c)!=REGIONS[region]['baseline']+REGIONS[region]['c_offset']+len(expected_new):raise ValueError('New inventory count differs')
 result={'status':'PASSED_G2_LOCAL','region':region,'original_rom_bytes':len(rom),
         'original_rom_sha1':sha1(rom),'original_elf_function_identities':sum(after.values()),
         'original_elf_identity_same':True,'relocation_multiset_same':True,
         'all_semantic_relocation_count':n_new,'all_semantic_relocation_sha256':h_new,
         'prior_matched_c_functions':REGIONS[region]['baseline'],'new_matched_c_functions':len(expected_new),
         'matched_c_functions':REGIONS[region]['baseline']+len(expected_new),'full_elf_unmarked_including_upstream':len(new_c),'matched_c_instruction_bytes':REGIONS[region]['oldbytes']+sum(x['size'] for x in stage['new_functions']),
         'assembly_remaining':7376-len(new_c),'functions':stage['new_functions']}
 (checkout/f'build/{region}/glitch-g2-proof.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=['stage','build','verify']);a.add_argument('--checkout',type=Path,required=True)
 a.add_argument('--region',choices=tuple(REGIONS),required=True);a.add_argument('--baseline',type=Path)
 a.add_argument('--deps',type=Path);a.add_argument('--runtime',type=Path)
 args=a.parse_args()
 if args.action=='stage':out=stage(args.checkout,args.region)
 elif args.action=='build':
  if not args.deps or not args.runtime:a.error('build requires deps/runtime')
  out=do_build(args.checkout,args.region,args.deps,args.runtime)
 else:
  if not args.baseline:a.error('verify requires --baseline')
  out=verify(args.checkout,args.baseline,args.region)
 print(json.dumps({k:v for k,v in out.items() if k!='asm_fragments' and k!='new_functions'},indent=2)[:8000])
if __name__=='__main__':main()

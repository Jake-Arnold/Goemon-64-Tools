#!/usr/bin/env python3
"""Original-address genuine-ID0 MIPS matching-C replay for five USA Mini routines.
Requires the user's authenticated expanded ROM, original ELF, pinned original
upstream source/IDO 5.3 and MIPS binutils; no private code/assets are bundled.
Isolated native proof ONLY: not canonical combined decomp.verify/G2 or CI.
"""
import argparse,hashlib,json,re,subprocess,tempfile,os
from pathlib import Path
EXPECTED_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
PINNED='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
FUNCTIONS=[
 ('func_801E28D8_59E7E8',0x59E7E8,0x801E28D8,68,1),
 ('func_801E2B54_59EA64',0x59EA64,0x801E2B54,84,4),
 ('func_801E31A8_59F0B8',0x59F0B8,0x801E31A8,52,3),
 ('func_801E3244_59F154',0x59F154,0x801E3244,52,3),
 ('func_801E3278_59F188',0x59F188,0x801E3278,92,5),
]
FLAGS=['-c','-G','0','-non_shared','-Xfullwarn','-Xcpluscomm','-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.','-Wab,-r4300_mul','-woff','649,838,712','-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-O2','-mips2']

def cmd(args,cwd=None):
 return subprocess.check_output([str(x) for x in args],cwd=cwd,text=True,stderr=subprocess.PIPE)

def symbol_table(elf):
 ret={}
 for l in cmd(['readelf','-Ws',elf]).splitlines():
  m=re.match(r'\s*\d+:\s*([0-9A-Fa-f]+)\s+(\d+)\s+(\w+)\s+\w+\s+\w+\s+(\S+)\s+(\S+)',l)
  if m:
   addr,sz,kind,section,name=m.groups();ret.setdefault(name,[]).append((int(addr,16),int(sz),kind,section))
 return ret

def relocations(elf,section,origin=0,start=0,size=0):
 entries=[];current=''
 for line in cmd(['readelf','-rW',elf]).splitlines():
  m=re.search(r"^Relocation section '([^']+)'",line)
  if m: current=m.group(1)
  m=re.match(r'\s*([0-9a-fA-F]{8})\s+[0-9a-fA-F]+\s+(R_MIPS_\w+)\s+[0-9a-fA-F]+\s+(\S+)',line)
  if m and current==section:
   offset,typ,sym=m.groups();offset=int(offset,16)
   if (not size) or start<=offset<start+size:entries.append((offset-origin,typ,sym))
 return entries

def extract_one(source,name):
 pat=re.compile(r'\bvoid\s+(func_[A-Z0-9a-z_]+)\s*\(')
 spans=[]
 for m in pat.finditer(source):
  a=m.end();brace=source.find('{',a);semic=source.find(';',a)
  if brace<0 or 0<=semic<brace:continue
  depth=1;end=brace+1
  while depth:
   assert end<len(source),'Unclosed C body'
   if source[end]=='{':depth+=1
   if source[end]=='}':depth-=1
   end+=1
  spans.append((m.start(),end,m.group(1)))
 assert any(x[2]==name for x in spans),name
 out=source
 for start,end,fn in reversed(spans):
  if fn!=name:out=out[:start]+out[end:]
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--elf',type=Path,required=True);p.add_argument('--built-rom',type=Path,required=True);p.add_argument('--source',type=Path,default=Path(__file__).with_name('exact_five.c'));p.add_argument('--ld',default='mips-linux-gnu-ld');p.add_argument('--objcopy',default='mips-linux-gnu-objcopy');p.add_argument('--json',type=Path);a=p.parse_args()
 u=a.upstream.resolve();assert cmd(['git','-C',u,'rev-parse','HEAD']).strip()==PINNED
 rom=a.rom.read_bytes();built=a.built_rom.read_bytes();assert len(rom)==33554432 and rom==built and hashlib.sha1(rom).hexdigest()==EXPECTED_SHA
 original_sym=symbol_table(a.elf);fullsrc=a.source.read_text();result=[]
 with tempfile.TemporaryDirectory(prefix='goemon_native5_') as td:
  d=Path(td)
  for name,rom_offset,vma,size,expected_relos in FUNCTIONS:
   assert (vma,size,'FUNC', '16') in original_sym.get(name,[]),(name,original_sym.get(name))
   src=d/(name+'.c');obj=d/(name+'.o');align=d/(name+'.align.o');output=d/(name+'.elf');outbin=d/(name+'.text');script=d/(name+'.ld')
   src.write_text(extract_one(fullsrc,name))
   cc=u/'tools/ido-5.3/cc';cmd([cc,*FLAGS,'-o',obj,src],cwd=u)
   sy=symbol_table(obj);assert any(x[1]==size and x[2]=='FUNC' for x in sy[name]),(name,sy[name])
   crel=relocations(obj,'.rel.text')
   orel=relocations(a.elf,'.rel.file_11',origin=vma,start=vma,size=size)
   assert sorted(crel)==sorted(orel),(name,'relocation mismatch',crel,orel)
   assert len(crel)==expected_relos,(name,crel)
   # Lower only the object-section alignment metadata: leave every instruction
   # and relocation untouched. File11 original function starts are 4-byte-aligned.
   cmd([a.objcopy,'--set-section-alignment','.text=4',obj,align])
   external=set(x[2] for x in crel)
   for s in external:assert re.match(r'^(D|func)_[0-9A-Fa-f]{8}_[0-9A-Fa-f]+$',s),s
   defs=['--defsym='+s+'=0x'+s.split('_')[1] for s in sorted(external)]
   script.write_text('OUTPUT_ARCH(mips)\nSECTIONS {\n . = 0x%08X;\n .text : { *(.text) }\n /DISCARD/ : { *(.mdebug) *(.reginfo) *(.options) *(.note*) *(.comment) }\n}\n'%vma)
   cmd([a.ld,'-m','elf32btsmip','-T',script,*defs,'-o',output,align])
   ls=symbol_table(output)
   assert any(x[0]==vma and x[1]==size and x[2]=='FUNC' for x in ls[name]),(name,ls[name])
   cmd([a.objcopy,'-O','binary','-j','.text',output,outbin]);candidate=outbin.read_bytes()[:size]
   original=rom[rom_offset:rom_offset+size]
   assert len(candidate)==len(original)==size
   assert candidate==original,(name,'native linked MIPS differs',[hex(i) for i in range(0,size,4) if candidate[i:i+4]!=original[i:i+4]][:8])
   result.append({'name':name,'original_rom_offset':f'0x{rom_offset:06X}','original_vma':f'0x{vma:08X}','linked_instruction_bytes_exact':size,'original_sha256':hashlib.sha256(original).hexdigest(),'relocations_exact':len(crel),'status':'PASSED_ISOLATED_LINKED_NATIVE'})
 total=sum(r['linked_instruction_bytes_exact'] for r in result);relos=sum(r['relocations_exact'] for r in result)
 assert (len(result),total,relos)==(5,348,16)
 out={'status':'PASSED_ISOLATED_LINKED_NATIVE_RESEARCH_ONLY','original_sha1':EXPECTED_SHA,'original_rom_rebuild_bytes_exact':33554432,'authentic_compiler':'SGI IDO 5.3','pinned_upstream':PINNED,'functions':result,'totals':{'previously_asm_owned_new_functions':5,'complete_linked_original_native_instruction_bytes':total,'matching_original_relocations':relos},'combined_decomp_verify':'NOT_RUN','decomp_inventory':'NOT_RUN','full_decomp_local_ci':'NOT_RUN','promotion':'NOT_PERMITTED'}
 if a.json:a.json.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()

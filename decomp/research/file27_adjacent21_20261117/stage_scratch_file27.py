#!/usr/bin/env python3
"""Reproducible read-only-original upstream scratch integration of resource25/27 IDO C research.

All original ROM/ELF bytes read-only. Mutates only a dedicated disposable upstream
scratch checkout. Disallows instruction or nonzero padding edits. Fails closed.
Not an integration into the connected branch's production 782-C manifest.
"""
from pathlib import Path
import os,sys,subprocess,struct,hashlib,json,re
sys.path.insert(0,'/tmp/goemon-new-candidates')
from stage_file26_upstream_scratch import trim_padding_elf
from verify_scratch_file26 import identities,readelf

W=Path('/tmp/goemon-adjacent27'); BASE=Path('/tmp/goemon-flagwork/mnsg-japan'); SCR=Path('/tmp/goemon-scratch-adjacent27/mnsg-japan')
ENV=os.environ.copy();ENV['PATH']='/tmp/goemon-flagwork/env/goemon-dependencies/bin:'+ENV['PATH'];ENV['LD_LIBRARY_PATH']='/tmp/goemon-flagwork/env/goemon-runtime-additions/lib';ENV['PYTHONHOME']='/tmp/goemon-flagwork/env/goemon-runtime-additions/python';ENV['PYTHONPATH']='/tmp/goemon-flagwork/env/goemon-dependencies/.venv/lib/python3.12/site-packages'
PY='/tmp/goemon-flagwork/env/goemon-runtime-additions/python/bin/python3.12'
FLAGS='-c -G 0 -non_shared -Xfullwarn -Xcpluscomm -Wab,-r4300_mul -woff 649,838,712 -D_LANGUAGE_C -D_FINALROM -DF3DEX_GBI -D__sgi -DNDEBUG -O2 -mips2'.split()
ROM_SHA='6ea0ed71032ce08fc2745f412d84936382197494'
HEADER='\n'.join(['.include "macro.inc"','.set noat','.set noreorder','.set gp=64','.section .text, "ax"','',''])

def run(args):
 p=subprocess.run([str(a) for a in args],cwd=SCR,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(f'{args}: rc={p.returncode}\n{p.stdout[-6500:]}')
 return p.stdout

def marker(region,addr):
 for m in re.finditer(r'nonmatching\s+(func_0800[0-9A-Fa-f]{4}_[0-9A-Fa-f]{6}),\s+0x([0-9A-Fa-f]+)',region):
  symbol=m.group(1)
  if int(symbol.split('_')[1],16)-0x08000000==addr:return m.start()
 raise AssertionError(f'No source marker for 0x{addr:x}')

def section_sizes(obj):
 b=obj.read_bytes();assert b[:6]==b'\x7fELF\x01\x02'
 off=struct.unpack_from('>I',b,32)[0];sz=struct.unpack_from('>H',b,46)[0];num=struct.unpack_from('>H',b,48)[0]
 a=[]
 for i in range(1,num):
  h=off+i*sz
  if struct.unpack_from('>I',b,h+4)[0]==1 and struct.unpack_from('>I',b,h+8)[0]&4:
   a.append((struct.unpack_from('>I',b,h+20)[0],struct.unpack_from('>I',b,h+32)[0]))
 assert len(a)==1, (obj,a)
 return a[0]

def compile_segment(fileid,letter,source,kind,expected_bytes):
 src_dir=SCR/('src' if kind=='c' else 'asm/usa');out_dir=SCR/('build/usa/src' if kind=='c' else 'build/usa/asm/usa');out_dir.mkdir(parents=True,exist_ok=True)
 dst=src_dir/f'file_{fileid}_{letter}.{kind if kind=="c" else "s"}'
 if kind=='c':
  dst.write_bytes((W/source).read_bytes())
  obj=out_dir/(dst.name+'.o');run([SCR/'tools/ido-5.3/cc',*FLAGS,'-o',obj,dst])
 else:
  dst.write_text(source)
  obj=out_dir/(dst.name+'.o');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',obj,dst])
 section,align=section_sizes(obj)
 if section>expected_bytes:
  assert section==((expected_bytes+15)//16)*16,(fileid,letter,section,expected_bytes)
  trim_padding_elf(obj,section,expected_bytes)
 else:
  assert section==expected_bytes,(fileid,letter,section,expected_bytes)
 obj.touch()
 print(f'  {fileid}/{letter} {kind}: native .text {section} -> {expected_bytes} bytes',flush=True)
 return f'build/usa/{"src" if kind=="c" else "asm/usa"}/{dst.name}.o'

def stage_file(fileid,segments):
 s=(SCR/f'asm/usa/file_{fileid}.s').read_text()
 src=s
 segs=[]
 for i,(kind,name,start,end) in enumerate(segments):
  assert start<end
  if kind=='asm':
   at=marker(src,start) if start else 0
   stop=marker(src,end) if end is not None and end!=0x3860 else len(src)
   snippet=(src[at:stop] if start==0 else HEADER+src[at:stop])
   assert snippet.strip()
   obj=compile_segment(fileid,f'piece_{i:02d}',snippet,'s',end-start)
  else:
   obj=compile_segment(fileid,f'piece_{i:02d}',name,'c',end-start)
  segs.append(obj)
 # ensure segments are contiguous and code range complete
 assert segments[0][2]==0
 for a,b in zip(segments,segments[1:]):assert a[3]==b[2],(a,b)
 asm=SCR/f'asm/usa/file_{fileid}.s';backup=SCR/f'file_{fileid}_original.research_backup.s';backup.write_text(s);asm.unlink()
 ld=SCR/'.splat/usa/mnsg.ld';text=ld.read_text();key=f'    file_{fileid}_ROM_START = __romPos;';start=text.index(key);end=text.index(f'    file_{fileid+1}_ROM_START = __romPos;',start)
 part=text[start:end]
 assert f'.file_{fileid} 0x8000000 : AT(file_{fileid}_ROM_START) SUBALIGN(16)' in part
 part=part.replace(f'.file_{fileid} 0x8000000 : AT(file_{fileid}_ROM_START) SUBALIGN(16)',f'.file_{fileid} 0x8000000 : AT(file_{fileid}_ROM_START) SUBALIGN(4)')
 orig=f'build/usa/asm/usa/file_{fileid}.s.o(.text);';assert orig in part
 part=part.replace(orig,'\n        '.join(x+'(.text);' for x in segs))
 for sec in ('data','bss'):
  part=part.replace(f'build/usa/asm/usa/file_{fileid}.s.o(.{sec});',f'{segs[0]}(.{sec});')
 ld.write_text(text[:start]+part+text[end:])
 return segs

def original_rel(s,label):
 key=f"Relocation section '.rel.file_{label}'"
 assert key in s,key
 chunk=s.split(key,1)[1].split('\nRelocation section',1)[0]
 rows=[]
 for line in chunk.splitlines():
  cols=line.split()
  if len(cols)>=5 and re.fullmatch('[0-9a-fA-F]{8}',cols[0]) and cols[2].startswith('R_MIPS'):
   rows.append((int(cols[0],16),cols[2],cols[4]))
 return sorted(rows)

def main():
 assert run(['git','rev-parse','HEAD']).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
 original=(BASE/'config/usa/baserom.decompressed.z64').read_bytes()
 assert len(original)==33554432 and hashlib.sha1(original).hexdigest()==ROM_SHA
 assert original==(BASE/'build/usa/mnsg.z64').read_bytes()==(SCR/'build/usa/mnsg.z64').read_bytes()
 seg25=[('asm',None,0,0x1228),('c','file25_last_v3.c',0x1228,0x1270)]
 seg27=[
 ('asm',None,0,0x490),('c','group490.c',0x490,0x4FC),
 ('asm',None,0x4FC,0x59C),('c','group59c.c',0x59C,0x648),
 ('asm',None,0x648,0x8C4),('c','group8c4.c',0x8C4,0x9D8),
 ('asm',None,0x9D8,0xA7C),('c','groupa7c.c',0xA7C,0xBF8),
 ('asm',None,0xBF8,0x1380),('c','group1380.c',0x1380,0x14B0),
 ('asm',None,0x14B0,0x172C),('c','wrapper172c_v1.c',0x172C,0x176C),
 ('asm',None,0x176C,0x37EC),('c','noop37ec_v1.c',0x37EC,0x37F8),
 ('asm',None,0x37F8,0x3860)
 ]
 o25=[] # file25 symbol-address constant needs separate relocation-resolution research
 print('Staging 21 exact C functions in original file 27...',flush=True);o27=stage_file(27,seg27)
 for p in o25+o27:(SCR/p).touch()
 print('Full upstream 32 MiB build beginning',flush=True)
 out=run(['make','-j8','VERSION=usa','PYTHON='+PY,'build/usa/mnsg.z64'])
 (W/'upstream_scratch_build.log').write_text(out)
 rom=(SCR/'build/usa/mnsg.z64').read_bytes()
 if rom!=original:
  i=next(i for i,(a,b) in enumerate(zip(original,rom)) if a!=b)
  raise AssertionError(f'ROM mismatch at {i:#x}: orig {original[i:i+24].hex()} vs built {rom[i:i+24].hex()}, len={len(rom)}')
 assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==ROM_SHA
 s0=identities(readelf(BASE,'-s'));s1=identities(readelf(SCR,'-s'));assert s0==s1 and len(s1)==7376
 oldrel=readelf(BASE,'-r');newrel=readelf(SCR,'-r')
 counts={}
 for f in (27,):
  old=original_rel(oldrel,f);new=original_rel(newrel,f);assert old==new,(f,len(old),len(new),list(set(old)-set(new))[:10]);counts[str(f)]=len(old)
 proof={'status':'UPSTREAM_SCRATCH_FULL_ROM_EXACT','production_promoted':0,'sources_orig_rom_sha1':ROM_SHA,'original_upstream_sha':'7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee','exact_rom_bytes':len(rom),'verified_positive_sized_ELF_functions':len(s1),'original_semantic_relocations_preserved':counts,'new_original_address_exact_C':21,'new_file27_C':21,'new_file25_C':0,'new_original_machine_code_bytes':sum((b-a) for k,n,a,b in seg27 if k=='c'),'canonical_production_gate':'NOT_RUN'}
 (W/'scratch25_27_proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()

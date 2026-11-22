#!/usr/bin/env python3
"""Read-only comparison of a private original-USA ROM/ELF against a native IDO C object.
No ROM bytes, disassembly or object code are written into its JSON report.
"""
import argparse, hashlib, json, re, struct, subprocess, tempfile
from pathlib import Path

VMA=0x801CD310
ROM=0x589220
SIZE=4320
RELOC_RE=re.compile(r'^\s*([0-9a-f]{8})\s+[0-9a-f]{8}\s+(R_MIPS_\w+)\s+[0-9a-f]+\s+(\S+)')

def relocs(elf,section):
 text=subprocess.check_output(['readelf','-rW',str(elf)],text=True)
 label=f"Relocation section '.rel.{section}'"
 part=text.split(label,1)[1].split('Relocation section ',1)[0]
 return [(int(m.group(1),16),m.group(2),m.group(3)) for ln in part.splitlines() if (m:=RELOC_RE.match(ln))]

def secs(obj):
 s=subprocess.check_output(['readelf','-sW',str(obj)],text=True)
 pat=re.compile(r'\s+[0-9]+:\s+([0-9a-f]+)\s+(\d+)\s+FUNC\s+\w+\s+\w+\s+\d+\s+func_801CD310_589220')
 m=pat.search(s)
 if not m: raise ValueError('expected native ELF FUNC is missing')
 return int(m.group(1),16),int(m.group(2))

def native_section(obj,section):
 with tempfile.NamedTemporaryFile() as f:
  subprocess.check_call(['mips-linux-gnu-objcopy','-O','binary','-j','.'+section,str(obj),f.name])
  return Path(f.name).read_bytes()

def is_sqrt(w): return ((w>>26)==0x11 and ((w>>21)&31)==0x10 and (w&63)==4)

def run(rom,elf,obj,source):
 b=rom.read_bytes();assert len(b)==33554432
 sh=hashlib.sha1(b).hexdigest();assert sh=='6ea0ed71032ce08fc2745f412d84936382197494',sh
 old=b[ROM:ROM+SIZE]
 start,n=secs(obj); a=native_section(obj,'text');assert start+n<=len(a)
 a=a[start:start+n]
 orig_rel=[(off-VMA,t,sym) for off,t,sym in relocs(elf,'file_11') if VMA<=off<VMA+SIZE]
 cand_rel=relocs(obj,'text')
 assert len(orig_rel)==101,('incorrect original relocs',len(orig_rel))
 omit={off for off,_,_ in orig_rel}|{off for off,_,_ in cand_rel}
 lim=min(n,SIZE)
 comparable=[i for i in range(0,lim,4) if i not in omit]
 equal=[i for i in comparable if old[i:i+4]==a[i:i+4]]
 same_trip=[(o,t,s) for o,t,s in orig_rel if (o,t,s) in cand_rel]
 type_sym=[(t,s) for _,t,s in orig_rel]
 nat_type_sym=[(t,s) for _,t,s in cand_rel]
 type_sym_strict=sum(x==y for x,y in zip(type_sym,nat_type_sym))
 type_sym_match=sum(x==y or (x[1]=='jtbl_8020A85C_5C676C' and y[1]=='.rodata' and x[0]==y[0]) for x,y in zip(type_sym,nat_type_sym))
 original_jtable=struct.unpack_from('>18I',b,0x5C676C)
 candidate_jtable=struct.unpack_from('>18I',native_section(obj,'rodata'))
 orig_targets=[v-VMA for v in original_jtable]
 cand_targets=list(candidate_jtable)
 jump_drift=[new-old for old,new in zip(orig_targets,cand_targets)]
 same_groups=[orig_targets.index(v) for v in orig_targets]==[cand_targets.index(v) for v in cand_targets]
 sp=int.from_bytes(a[2:4],'big',signed=True)
 frame=-sp
 win=[]
 for lo,hi in [(0,0x3c),(0x50,0x90),(0x90,0x1b4),(0x1b4,0x260),(0x260,0x9b0),(0x9b0,0xde4),(0xde4,0x10e0)]:
  v=[i for i in comparable if lo<=i<hi]
  w=[i for i in equal if lo<=i<hi]
  win.append({'start':hex(lo),'end':hex(hi),'matching':len(w),'comparable':len(v)})
 return {'status':'FAILED_NATIVE' if n!=SIZE or len(equal)!=len(comparable) else 'PROBE_INSTRUCTION_MATCH_UNLINKED',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_vma':hex(VMA),'original_rom_offset':hex(ROM),
 'original_bytes':SIZE,'candidate_bytes':n,'frame_bytes':frame,
 'original_relocations':len(orig_rel),'candidate_relocations':len(cand_rel),
 'relocation_type_symbol_strict_in_order':type_sym_strict,
 'relocation_type_symbol_including_generated_rodata_equivalent':type_sym_match,
 'jump_table_entries':len(cand_targets),'jump_table_target_groups_same':same_groups,
 'jump_table_destination_relative_drift_bytes':sorted(set(jump_drift)),
 'relocation_offset_type_symbol_identical':len(same_trip),
 'calls_original':sum(t=='R_MIPS_26' for _,t,_ in orig_rel),
 'calls_candidate':sum(t=='R_MIPS_26' for _,t,_ in cand_rel),
 'sqrt_original':sum(map(is_sqrt,struct.unpack('>'+str(SIZE//4)+'I',old))),
 'sqrt_candidate':sum(map(is_sqrt,struct.unpack('>'+str(n//4)+'I',a))),
 'words_comparable':len(comparable),'words_matching':len(equal),
 'first_nonreloc_mismatch':next((hex(i) for i in comparable if i not in equal),None),
 'windows':win,
 'candidate_full_rom_integration':'NOT_RUN','combined_decomp_verify':'NOT_RUN','strict_inventory':'NOT_RUN','full_local_ci':'NOT_RUN'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--elf',type=Path,required=True);p.add_argument('--object',type=Path,required=True);p.add_argument('--source',type=Path,required=True)
 a=p.parse_args();print(json.dumps(run(a.rom,a.elf,a.object,a.source),indent=2))

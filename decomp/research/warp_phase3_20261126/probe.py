import argparse,hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from decomp.consolidated_batch_promotion import exact,FLAGS,rels,text,probe,jp55
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--selected-only',action='store_true');a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
assert __debug__
kit=Path(__file__).resolve().parent; ledger=a.repo/'decomp/COMPILER_QUIRKS.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd,co):return subprocess.run([str(x) for x in cmd],cwd=co,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True).stdout
regions=[('usa',a.usa,'func_801CB5D0_5874E0','6ea0ed71032ce08fc2745f412d84936382197494'),('japan_0',a.jp,'func_801D0D00_58CCD0','6f8745fecc3a5e7d4918c7a73353eb0726116ded')]
rows=[]
for r,co,n,h in regions:
 v,off=[int(x,16) for x in n.split('_')[1:]];z=472;rom=(co/f'config/{r}/baserom.decompressed.z64').read_bytes();assert hashlib.sha1(rom).hexdigest()==h;assert sha((co/'tools/ido-5.3/cc').read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0';assert run(['git','rev-parse','HEAD'],co).decode().strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee';owner=next(x for x in (co/f'asm/{r}').glob('*.s') if f'glabel {n}\n' in x.read_text());code=rom[off:off+z];probe.get_original_splat_lines(owner,n,off,v,z,code);raw=owner.read_text();m=next(m for m in jp55.BLOCK.finditer(raw) if m['name']==n);ref=a.work/f'{r}.ref.o';s=ref.with_suffix('.s');s.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text,"ax"\n'+raw[m.start():m.end()]+'\n');run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,s],co);refb=text(ref);refrel=rels(ref)
 syms={}
 for path in list((co/f'config/{r}/symbol_addrs').rglob('*.txt'))+list((co/f'.splat/{r}').glob('undefined*.ld')):
  for k,x in re.findall(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9a-fA-F]+)\s*;',path.read_text(),re.M):syms[k]=int(x,16)
 for _,_,name in refrel:
  if name not in syms:syms[name]=int(re.match(r'^(?:func|D)_([0-9a-fA-F]+)(?:_|$)',name)[1],16)
 ld=a.work/f'{r}.ld';ld.write_text('\n'.join(f'{k} = 0x{syms[k]:X};' for k in sorted({x[2] for x in refrel}))+'\n'+f'SECTIONS {{ . = 0x{v:X}; .text : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(*) }} }}\n')
 def link(obj):
  elf=obj.with_suffix('.elf');binfile=obj.with_suffix('.bin');run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','-T',ld,'-o',elf,obj],co);run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binfile],co);return binfile.read_bytes()
 assert link(ref)[:z]==code
 for src in sorted((kit/'sources').glob(r+'_*.c')):
  if a.selected_only and src.stem not in [r+'_'+x for x in ('scale','candidate','negative_bound','negative_value')]:continue
  obj=a.work/(src.stem+'.o');ldhash=sha(ledger.read_bytes());cmd=[co/'tools/ido-5.3/cc',*FLAGS,'-o',obj,src];rec=dict(region=r,name=n,rom_offset=off,vma=v,owner=str(owner.relative_to(co)),original_bytes=z,original_code_sha256=sha(code),source=src.name,source_sha256=sha(src.read_bytes()),source_git_blob_sha1=hashlib.sha1(b'blob '+str(len(src.read_bytes())).encode()+b'\0'+src.read_bytes()).hexdigest(),compiler_sha256=sha((co/'tools/ido-5.3/cc').read_bytes()),flags=FLAGS,ledger_sha256=ldhash,reference_relocations=len(refrel))
  try:
   run(cmd,co);b=text(obj);rr=rels(obj);diff=[i for i in range(0,z,4) if b[i:i+4]!=refb[i:i+4]];sizeok,_=probe.check_size(run(['readelf','-Ws',obj],co).decode(),n,z);linked=link(obj);matches=sum(linked[i:i+4]==code[i:i+4] for i in range(0,z,4));rec.update(raw_matching_words=z//4-len(diff),linked_matching_words=matches,extent_exact=sizeok,raw_first_difference=diff[0] if diff else None,raw_difference_offsets=diff,named_relocations_exact=rr==refrel,relocation_count=len(rr),exact=exact(obj,ref,rec|{'relocation_count':len(refrel)}) and linked[:z]==code,compiler_outcome='NEW_REPRODUCIBLE_QUIRK' if src.stem==r+'_candidate' and not diff and sizeok and rr==refrel and linked[:z]==code else 'NO_NEW_COMPILER_FINDING',first_mismatch_category=('NONE' if not diff and sizeok and rr==refrel else 'REGISTER_ALLOCATION' if src.stem==r+'_scale' else 'CONTROL_OR_VARIANT_MISMATCH'))
  except subprocess.CalledProcessError as e:rec.update(error=e.stdout.decode(errors='replace')[:1500].replace(str(kit),'<kit>').replace(str(a.work),'<work>'),exact=False,compiler_outcome='NO_NEW_COMPILER_FINDING',first_mismatch_category='COMPILER_OR_LINK_REJECTED')
  rows.append(rec);print(r,src.name,rec.get('linked_matching_words'),rec.get('raw_difference_offsets'),rec.get('named_relocations_exact'),rec.get('error',''),flush=True)
(a.work/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
owner=[]
for r,co,n,h in regions:
 group=[x for x in rows if x['region']==r];pos=next(x for x in group if x['source']==r+'_candidate.c');controls=[next(x for x in group if x['source']==r+'_'+s+'.c') for s in ('scale','negative_bound','negative_value')];assert pos['exact'] and all(not x['exact'] and 'error' not in x for x in controls);shutil.copyfile(a.work/(r+'_candidate.o'),a.work/(n+'.candidate.o'));owner.append({**pos,'attempts':[{'exact_raw':pos['exact'],'linked_original_rom_exact':pos['linked_matching_words']==118}]+[{'exact_raw':x['exact'],'source':x['source'],'source_sha256':x['source_sha256']} for x in controls]})
(a.work/'isolated-replay.json').write_text(json.dumps(owner,indent=2)+'\n')
